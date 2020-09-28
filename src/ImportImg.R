### ----------------------------------------------------------------------------
### Importing images from Agouti into folders
### Emma Cartuyvels
### ----------------------------------------------------------------------------

importIMG <- function(sequences = "all", deployment = "all", n = "all"){
  
  require(imager)
  require(tidyverse)
  assets <- read_csv(file = "./data/Agouti_raw/assets.csv")
  
  assets$url <- as.character(assets$url)
  assets$originalFilename <- as.character(assets$originalFilename)
  
  data <- assets
  
  if(sequences %in% c("all")){
    data <- data
  }else{
    data <- data %>% 
      filter(sequence %in% sequences)
  }
  
  if(deployment %in% c("all")){
    data <- data
  }else{
    data <- data %>% 
      filter(deploymentid %in% deployment)
  }
  
  if(n == "all"){
    n <-  nrow(data)
  }else{
    if(!is.integer(n)){
      n  <-  as.integer(n)
      if(is.na(n)){
        stop("n - vallue is not usable, provide a integer or all")
      }
    }
  }
  
  print(nrow(data))
  
  for (i in 1:n){
    ifelse(dir.exists(paste0("./data/raw/",
                             data$deploymentid[i])),
           FALSE,
           dir.create(paste0("./data/raw/",
                             data$deploymentid[i])))
    download.file(data$url[i],
                  destfile = paste0("./data/raw/",
                                    data$deploymentid[i],
                                    "/",
                                    data$originalFilename[i]),
                  method = "curl")
  }
}


#test

importIMG(sequences = c("f9ad783b-f310-4560-86c0-86ceff691660", "54a68c1c-a3b7-4bc1-9afa-8a2d270915a7"))


