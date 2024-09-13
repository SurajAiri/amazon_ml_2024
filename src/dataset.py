import pandas as pd
import os
from pathlib import Path
import argparse
from utils import download_image, download_images

def downloadImageDataset(dataset_path, download_folder, iteration_download_rate=100, start=0, end=None):
    df = pd.read_csv(dataset_path)
    
    # If data_size is not provided, download all available images
    if end is None or end > df.shape[0]:
        end = df.shape[0]

    Path(download_folder).mkdir(parents=True, exist_ok=True)
    while start < end:
        print("start: ", start, "end: ", min(start + iteration_download_rate, end))
        links = df['image_link'].iloc[start:min(start + iteration_download_rate, end)]
        download_images(links.values, download_folder)

        start = start + iteration_download_rate
        print(f"Successfully downloaded {min(iteration_download_rate, end - start)} images\n")


def validateImages(dataset_path, download_folder,start=0, end=None, download_missing=True):
    if not Path(download_folder).exists():
        print("Error: directory doesn't exist")
        return

    df = pd.read_csv(dataset_path)
    if end is None or end > df.shape[0]:
        end = df.shape[0]

    links = df['image_link'].iloc[start:end].values
    missingCount = 0
    for link in links:
        fname = Path(link).name
        path = os.path.join(download_folder, fname)
        if not os.path.exists(path):
            # print(list(links).index(link))
            print("Missing image: ", link)
            missing = True
            try:
                if download_missing:
                    download_image(link, download_folder)
                    print("Image downloaded")
                    missing = False
            except:
                print("Error downloading image")

            if missing:
                missingCount += 1
            
    if missingCount < 1:
        print("All images exist")
    else:
        print("Some images are missing, please download them.")
        print("Missing images count: ",missingCount)


if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Download and validate images.")
    
    # Add arguments with aliases
    parser.add_argument("-m", "--mode", choices=["download", "validate"], required=True,
                        help="Mode to run the script in: 'download' or 'validate'.")
    parser.add_argument("-dp", "--dataset_path", default="dataset/train.csv", 
                        help="Path to the CSV file containing image links.")
    parser.add_argument("-df", "--download_folder", default="images/train/", 
                        help="Folder to save the downloaded images.")
    parser.add_argument("-s", "--start", type=int, default=0, 
                        help="Start index for downloading/validating images.")
    parser.add_argument("-e", "--end", type=int, default=None, 
                        help="End index for downloading/validating images.")
    
    # Parameters for downloading images
    parser.add_argument("-idr", "--iteration_download_rate", type=int, default=1000, 
                        help="Number of images to download per iteration.")
    
    # Parameters for validating images
    parser.add_argument("-im", "--ignore_missing", action="store_true", 
                        help="Won't download missing images during validation.")

    # Parse the arguments
    args = parser.parse_args()

    # Run the corresponding function based on the mode
    if args.mode == "download":
        downloadImageDataset(args.dataset_path, args.download_folder, args.iteration_download_rate, args.start, args.end)
    elif args.mode == "validate":
        validateImages(args.dataset_path, args.download_folder, start=args.start, end=args.end, download_missing=not args.ignore_missing)