import pandas as pd
from utils import  download_images
import os
import pathlib


DOWNLOAD_FOLDER = "images/train/"
PATH = "dataset/train.csv"
ITERATION_DOWNLOAD_RATE = 1000
start = 0


if __name__ == "__main__":
    df = pd.read_csv(PATH)
    dataSize = df.shape[0]

    pathlib.Path(DOWNLOAD_FOLDER).mkdir(parents=True, exist_ok=True)
    # while(start < df.shape[0]):
    # while(start < dataSize):
    #     print("start: ", start, "end: ", start + ITERATION_DOWNLOAD_RATE)
    #     links = df['image_link'].iloc[start:start + ITERATION_DOWNLOAD_RATE]
    #     # download_images(links.values, DOWNLOAD_FOLDER)
        
    #     start = start + ITERATION_DOWNLOAD_RATE
    #     print(f"successfully downloaded {ITERATION_DOWNLOAD_RATE} images\n")