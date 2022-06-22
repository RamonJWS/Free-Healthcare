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
    IMAGE_UNZIP_TEST = os.path.join(DATA_PATH,"ISIC2018_Task3_Test_Images.zip")
    CLASSES = ['bkl', 'nv', 'df', 'mel', 'vasc', 'bcc', 'akiec']

    # unzip folders:
    # create folder for all data
    image_folder_dir = os.path.join(DATA_PATH,"image")
    if not os.path.isdir(image_folder_dir):
        os.mkdir(image_folder_dir)
    
        list_of_unzip_files = [IMAGE_UNZIP_1, IMAGE_UNZIP_2]
        for file in list_of_unzip_files:
            with zipfile.ZipFile(file, 'r') as zip_ref:
                zip_ref.extractall(image_folder_dir)

    # create all the folders for the images
    for file in ["Train","Validation","Test"]:
        folder_dir = os.path.join(DATA_PATH, file)
        if not os.path.isdir(folder_dir):
            os.mkdir(folder_dir)
            for target in CLASSES:
                os.mkdir(os.path.join(folder_dir, target))

    # unzip testing images into Test folder
    # need to fix issue with unzipping all data in zip file, only need ISIC2018_Task3_Test_Images...
    test_folder_dir = os.path.join(DATA_PATH,"Test")
    # checks to see if path folder exists
    if len(os.listdir(test_folder_dir)) == len(CLASSES):
        with zipfile.ZipFile(IMAGE_UNZIP_TEST, 'r') as zip_ref:
            # gets a list of all the files in the unzip folder
            all_files_in_unzip = zip_ref.namelist()
            # splits all file directories but "/", we want everything beginning with "ISIC..."
            unzip_files_split = [x.split("/") for x in all_files_in_unzip]
            files_to_keep = []
            for idx, prefix in enumerate(unzip_files_split):
                if prefix[0] == "ISIC2018_Task3_Test_Images":
                    files_to_keep.append(all_files_in_unzip[idx])
            # specify what files to keep and where to send the unzipped files.
            zip_ref.extractall(path=test_folder_dir, members=files_to_keep) 