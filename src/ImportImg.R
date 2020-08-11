### ----------------------------------------------------------------------------
### Importing images from Agouti into folders
### Emma Cartuyvels
### ----------------------------------------------------------------------------

library(imager)

assets <- read.csv(file = "./CameravallenCode-master/data/raw/assets.csv")
assets$url <- as.character(assets$url)
assets$originalFilename <- as.character(assets$originalFilename)

for (i in 1:1000){
  ifelse(dir.exists(paste0("./CameravallenCode-master/data/raw/",
                           assets$deploymentid[i])),
         FALSE,
         dir.create(paste0("./CameravallenCode-master/data/raw/",
                           assets$deploymentid[i])))
  download.file(assets$url[i],
                destfile = paste0("./CameravallenCode-master/data/raw/",
                                  assets$deploymentid[i],
                                  "/",
                                  assets$originalFilename[i]),
                method = "curl")
}


### ----------------------------------------------------------------------------
### Changing datasets

assetsCOR <- read.csv("./assets.csv", sep = ";")
observationsCOR <- read.csv("./observations.csv", sep = ";")
pickup_setupCOR <- read.csv("./pickup_setup.csv", sep = ";")

# Make them empty


# Get new data fitted into old format
assetsNEW <- read.csv("./CameravallenCode-master/data/raw/assets.csv")
observationsNEW <- read.csv("./CameravallenCode-master/data/raw/observations.csv")
pickup_setupNEW <- read.csv("./CameravallenCode-master/data/raw/pickup_setup.csv")

# assets
assets <- setNames(data.frame(matrix(ncol = ncol(assetsCOR),
                                     nrow = nrow(assetsNEW))),
                   names(assetsCOR))
assets$sequence = assetsNEW$sequence
assets$type = "image"
assets$originalFilename = assetsNEW$originalFilename
assets$deployment = assetsNEW$deploymentid

# observations
observations <- setNames(data.frame(matrix(ncol = ncol(observationsCOR),
                                     nrow = nrow(observationsNEW))),
                   names(observationsCOR))
observations$observationID = observationsNEW$observation_id
observations$observationPerson = observationsNEW$observer
observations$animalCount = observationsNEW$animalCount
observations$animalIsDomesticated = observationsNEW$animalIsDomesticated
observations$animalScientificName = observationsNEW$animalScientificName
observations$animalVernacularName = observationsNEW$animalVernacularName
observations$animalSex = observationsNEW$animalSex
observations$animalAge = observationsNEW$animalAge
observations$animalBehavior = observationsNEW$animalBehavior
observations$sequenceID = observationsNEW$sequenceID
observations$sequenceStart = observationsNEW$sequence_start
observations$sequenceIsBlank = observationsNEW$isBlank
observations$sequenceIsSetupPickup = observationsNEW$isSetupPickup
observations$sequenceIsUnknown = observationsNEW$isUnknown
observations$deploymentID = observationsNEW$deploymentID
observations$deploymentStart = observationsNEW$startDate
observations$deploymentEnd = observationsNEW$endDate
observations$deploymentLatitude = observationsNEW$lat
observations$deploymentLongitude = observationsNEW$lng

# pickup setup
pickup_setup <- setNames(data.frame(matrix(ncol = ncol(pickup_setupCOR),
                                           nrow = nrow(pickup_setupNEW))),
                         names(pickup_setupCOR))
pickup_setup$sequenceId = pickup_setupNEW$sequenceId
pickup_setup$deploymentId = pickup_setupNEW$deploymentid
pickup_setup$isBlank = pickup_setupNEW$isblank
pickup_setup$isSetupPickup = pickup_setupNEW$issetuppickup
pickup_setup$isTimeLapse = "ONWAAR"

# Save new datasets
write.csv(assets, "CameravallenCode-master/assets.csv")
write.csv(observations, "CameravallenCode-master/observations.csv")
write.csv(pickup_setup, "CameravallenCode-master/pickup_setup.csv")
