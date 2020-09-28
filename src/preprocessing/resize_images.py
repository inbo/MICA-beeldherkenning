import glob 
import os
import pandas as pd
from PIL import Image

import yaml

root = os.getcwd()
if 'mica-beeldherkenning' in root:
    print(root)
else:
    root = os.path.join(os.getcwd(),'mica-beeldherkenning')

print(root)
config_path = os.path.join(root,'src', 'config.yml')

from src.preprocessing.def_functions import remove_dup_columns, black_border, standard_box, size_box, devide_box

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

print(general_folder_path)
print(resized_folder_path)
print(preprocessing_output_path)

def resize_images(general_folder_path, resized_folder_path):
    
    """ Function to resize the original camera trap images.

    Parameters
    ----------
    general_folder_path : string (filepath)
        path to folder containing the raw data (the images and the Agouti export files)
    resized_folder_path : string (filepath)
        path to folder where the resized images will be saved
    
    """
    
    #Load Agouti export with observation
    observations = pd.read_csv(os.path.join(general_folder_path, 'observations.csv'))
    
    
    #Loop over every deployment
    deployments = observations.deploymentID.unique()
    
    for folder in os.listdir(general_folder_path):
        imageFolderPath = os.path.join(general_folder_path, folder)
        
        #Check if it is a folder, not a file and if deployment is annotated
        if os.path.isdir(imageFolderPath) and folder in deployments:
            imagePath = glob.glob(imageFolderPath + '/*.JPG')
            
            if not os.path.exists(os.path.join(resized_folder_path, folder)):
                os.makedirs(os.path.join(resized_folder_path, folder))
                  
            #Import all images
            for img in imagePath:
                im = Image.open(img)
                size =im.size   # get the size of the input image
                RATIO = 0.5  # reduced the size to 50% of the input image
                reduced_size = int(size[0] * RATIO), int(size[1] * RATIO)     
                
                im_resized = im.resize(reduced_size)
                image_name = (im.filename).split('\\')[-1]
                im_resized.save(os.path.join(resized_folder_path,folder,image_name))

if __name__ == '__main__':
    resize_images(general_folder_path, resized_folder_path)