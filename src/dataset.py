import pandas as pd
from utils import  download_image, download_images
import os
from pathlib import Path


DOWNLOAD_FOLDER = "images/train/"
DATASET_PATH = "dataset/train.csv"

def downloadImageDataset():
    # ITERATION_DOWNLOAD_RATE = 1000
    # start = 168500
    ITERATION_DOWNLOAD_RATE = 100
    start = 0

    df = pd.read_csv(DATASET_PATH)
    dataSize = df.shape[0]

    Path(DOWNLOAD_FOLDER).mkdir(parents=True, exist_ok=True)
    while(start < dataSize):
        print("start: ", start, "end: ", start + ITERATION_DOWNLOAD_RATE)
        links = df['image_link'].iloc[start:start + ITERATION_DOWNLOAD_RATE]
        download_images(links.values, DOWNLOAD_FOLDER)
        
        start = start + ITERATION_DOWNLOAD_RATE
        print(f"successfully downloaded {ITERATION_DOWNLOAD_RATE} images\n")

def validateImages(end = None,download=True):
    if not Path(DOWNLOAD_FOLDER).exists():
        print("Error: directory doesn't exists")
        return
    
    df = pd.read_csv(DATASET_PATH)
    if end == None:
        end = df.shape[0]

    links = df['image_link'].iloc[0:end+1].values
    allExists = True
    for link in links:
        fname = Path(link).name
        path = os.path.join(DOWNLOAD_FOLDER,fname)
        if not os.path.exists(path):
            print("Missing image: ",link)
            t = False
            try:
                if download:
                    download_image(link,DOWNLOAD_FOLDER)
                    print("image downloaded")
                    t = True
            except:
                print("Error on downloading image")
            
            allExists = t and allExists
    if allExists:
        print("All images exists")
    else: 
        print("Mentioned images are missing please download them.")        


if __name__ == "__main__":
    # downloadImageDataset()

    limit = 100_000
    validateImages(end=limit)