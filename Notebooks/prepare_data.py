import os
import zipfile

"""
1). I want to use data augmentation for this task. This requires for the data to be put
    into folders. The images should be in a train, validation and test folders. Within
    these folders there should be a folder for each class of  pigmented skin lesions.
    EX:

    train - 'bkl'
          - 'nv'
          - 'df'
          - 'mel'
          - 'vasc'
          - 'bcc'
          - 'akiec'

2). unzip data and move all images into one folder.
3). add check for corrupted images.
3). create appropriate folders (train, validation, test) with subfolders.
4). match image ids with meta data in "HAM10000_metadata" dataset
"""
if __name__ == "__main__":

    BASE_DIR = os.getcwd()
    DATA_PATH = os.path.join(BASE_DIR, "Data")
    META_DATA_PATH = os.path.join(DATA_PATH,"HAM10000_metadata")
    IMAGE_UNZIP_1 = os.path.join(DATA_PATH,"HAM10000_images_part_1.zip")
    IMAGE_UNZIP_2 = os.path.join(DATA_PATH,"HAM10000_images_part_2.zip")

    # unzip folders:
    # create folder for all data
    image_folder_dir = os.path.join(DATA_PATH,"image")
    if not os.path.isdir(image_folder_dir):
        os.mkdir(image_folder_dir)
    
