import pandas as pd
from utils import download_images
path = "dataset/train.csv"



if __name__ == "__main__":
    df = pd.read_csv(path)

    url = []
    for id in df['group_id'].unique():
        url.append(df[df['group_id'] == id].iloc[0]['image_link'])

    # print(url)
    dir_path = "unique_images/"
    download_images(url, dir_path)
    print("Downloaded unique images to ", dir_path)