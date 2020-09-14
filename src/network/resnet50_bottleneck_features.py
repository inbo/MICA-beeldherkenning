import os
from ast import literal_eval
import pandas as pd
import numpy as np
import yaml
import tensorflow as tf

from sklearn.preprocessing import LabelEncoder
from keras.applications import ResNet50

from src.network.functions_network import (group_birds,
                                       DataGenerator, 
                                       split_train_val_test_bottleneck)

#from tensorflow.python.client import device_lib
 #print(device_lib.list_local_devices())



if tf.test.is_gpu_available():
    print("using GPU")
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        try:
            tf.config.experimental.set_virtual_device_configuration(gpus[0], [
                tf.config.experimental.VirtualDeviceConfiguration(memory_limit=1024)])
        except RuntimeError as e:
            print(e)

# Load configuration file
root = os.getcwd()
if 'mica-beeldherkenning' in root:
    print(root)
else:
    root = os.path.join(os.getcwd(),'mica-beeldherkenning')

print(root)
config_path = os.path.join(root,'src', 'config.yml')

with open(config_path) as file:
    config = yaml.load(file, Loader=yaml.FullLoader)
print(config)

general_folder_path = config['general_folder_path']
general_folder_path = general_folder_path.replace("../", "")
general_folder_path = general_folder_path.replace("/", os.sep)
general_folder_path = os.path.join(root, general_folder_path)
resized_folder_path = config['resized_folder_path']
resized_folder_path = resized_folder_path.replace("../", "")
resized_folder_path = resized_folder_path.replace("/", os.sep)
resized_folder_path = os.path.join(root, resized_folder_path)
preprocessing_output_path = config['preprocessing_output_path']
preprocessing_output_path = preprocessing_output_path.replace("../", "")
preprocessing_output_path = preprocessing_output_path.replace("/", os.sep)
preprocessing_output_path = os.path.join(root, preprocessing_output_path)
bottleneck_features_output_path = config['bottleneck_features_output_path']
bottleneck_features_output_path = bottleneck_features_output_path.replace("../", "")
bottleneck_features_output_path = bottleneck_features_output_path.replace("/", os.sep)
bottleneck_features_output_path = os.path.join(root, bottleneck_features_output_path)

print(general_folder_path)
print(resized_folder_path)
print(preprocessing_output_path)
    
#Import preprocessing data
data = pd.read_csv(os.path.join(preprocessing_output_path,'boxes_preprocessing_single.csv'), sep=';')
data['annotation_literal'] = data['annotation']
#data['box_standard'] = data['box_standard'].apply(literal_eval)

#Select sequences with only one label
data = data.loc[data['annotation_literal'].str.len() == 1] 

#Group all bird species into one class
data['ann_animal'] = ""
data['ann_animal'] = data['annotation_literal'].apply(group_birds)

#Encode labels
le = LabelEncoder()
le.fit(data.ann_animal)
data['label'] = le.transform(data.ann_animal)
map_classes = dict(zip(le.classes_, range(len(le.classes_))))
classes = len(map_classes)

#Save data corresponding to the bottleneck features
data.to_csv(os.path.join(bottleneck_features_output_path,'bottleneck_data.csv'), index=False, sep=';')

#Image size
dim_x = 270
dim_y = 480
dim_z = 3

#Parameters
batch_size = 100
steps_per_epoch = np.ceil(len(data) / batch_size)

#Build the ResNet50 network
model = ResNet50(include_top=False, weights='imagenet')

#Create generator
generator = DataGenerator(data, dim_x = dim_x, dim_y = dim_y, dim_z = dim_z, 
                          batch_size=batch_size, augmentation=False, shuffle=False, mode='train').generate()

#Extract and save bottleneck features
bottleneck_features = model.predict(generator, steps_per_epoch)
np.save(os.path.join(bottleneck_features_output_path, 'bottleneck_features.npy'), bottleneck_features)

#When training:
#Split bottleneck features and data into training, validation and test data
train, validation, test, bottleneck_features_train, bottleneck_features_validation, bottleneck_features_test = split_train_val_test_bottleneck(data, bottleneck_features, 0.5, 0.25, bottleneck_features_output_path)