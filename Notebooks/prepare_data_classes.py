import os
import shutil
import zipfile
from sys import platform
import numpy as np
import pandas as pd
import random

random.seed(10) # can set to any integer
TRAIN_VALIDATION_SPLIT = 0.8 # controls the train validation split

class UnzipFiles:
    """
    Used to unzip files to specified locations

    Attributes:
    - Data_directory: The location of the folder with all the zipped files, the unzipped files will also be
                      found in this location.

    Methods:
    - unzip_to_location(location): Unzips the zip file to a specified location.
    """

    Data_directory = os.path.join(os.getcwd(),"Data")

    def __init__(self, zip_folder_name: str) -> None:
        """
        Attributes:
        - zip_location: This is the location of the zipped data
        """
        self.zip_location = os.path.join(UnzipFiles.Data_directory, zip_folder_name)

    def unzip_to_location(self, location: str) -> None:
        """
        Use: Copies over all the images from the specified unzip folder into a designated location.
             The function also ensures that no duplicate images are copied across.
             The images are copied to a folder in the Data directory (user has no control over location atm).

        Args: location - the name of the file the images are copied to.

        Returns: None
        """
        self.unzip_location = os.path.join(self.Data_directory, location)
        # "if" used to ensure process is skipped if all images already in "Image" folder
        if os.path.exists(self.unzip_location) and len(os.listdir(self.unzip_location)) >= 10000:
            pass
        else:
            with zipfile.ZipFile(self.zip_location, "r") as zip_ref:
                all_files_in_unzip = zip_ref.namelist()
                if os.path.exists(self.unzip_location):
                    images_extract = [image for image in all_files_in_unzip if image not in os.listdir(self.unzip_location)]
                    zip_ref.extractall(self.unzip_location, members=images_extract)
                else:
                    zip_ref.extractall(self.unzip_location)

class TestCleanUp(UnzipFiles):
    """
    This class inherits from UnzipFiles. Used to unzip and clean the test images as there are several
    unwanted files in the unzip.

    Attributes:
    - Data_directory: The location of the folder with all the zipped files, the unzipped files will also be
                      found in this location.

    Methods:
    - unzip_to_location(location): Unzips the zip file to a specified location.
    """

    def __init__(self, zip_folder_name: str):
        UnzipFiles.__init__(self, zip_folder_name)

    def _os_check(self) -> int:
        """
        Use: Check what operating system user has. Based on operating system different files need to be extracted and deleted

        Args: None

        Returns: int - 0 for windows and -1 for mac or linux
        """
        if platform == "win32":
            return 0
        return -1
    
    def clean_folder(self) -> None:
        """
        Use: Removes unused files and moves all images up a folder.
             Unzipped files are "__MACOSX" and "ISIC2018_Task3_Test_Images", the first should only be used for mac os

        Args: None

        Returns: None
        """
        sub_folders = [os.path.join(self.unzip_location, "__MACOSX"),
                            os.path.join(self.unzip_location, "ISIC2018_Task3_Test_Images")]
        os_check = self._os_check()
        shutil.rmtree(sub_folders[os_check])
        image_names = [x for x in os.listdir(sub_folders[-1]) if x.split(".")[os_check+1] == "jpg"]
        for image_name in image_names:
            shutil.move(os.path.join(sub_folders[-1], image_name), self.unzip_location)
        shutil.rmtree(sub_folders[os_check+1])


class PopulateSubDirectories:
    """
    A class used to create train and validation subdirectories with a folders for each class of skin cancer.
    The class is also used to create a mapping from the meta data to the images so each image has a known class.
    The images can then be split into train and validation and moved to the corresponding class folders.

    Attributes:
    - Data_directory: The location of all the data.
    - Image_directory: The location where all the images are.
    - classes: A list of all the skin cancer classes.

    Methods:
    - create_sub_folders(): Uses the class attribute classes to create the required subfolders.
    - map_images_to_folders(train_validation_split): From a specified training split ratio this splits the data into
                                                     training and validation data. The method then creates a mapping
                                                     from the meta data to each image so the class is known. Finally
                                                     the method moved the image to the correct subfolder based on its
                                                     class.
    """
    
    Data_directory = os.path.join(os.getcwd(),"Data")
    Image_directory = os.path.join(Data_directory, "Images")
    classes = ['bkl', 'nv', 'df', 'mel', 'vasc', 'bcc', 'akiec']

    def __init__(self, location) -> None:
        """
        Attributes:
        - location: This is the location to create subfolders and later populate them.
        """
        self.location = os.path.join(PopulateSubDirectories.Data_directory, location)

    def create_sub_folders(self) -> None:
        """
        Use: To create a subfolder for each type of skin cancer

        Args: None

        Returns: None
        """
        
        if not os.path.exists(self.location):
            os.mkdir(self.location)
            for target in PopulateSubDirectories.classes:
                if not os.path.exists(os.path.join(self.location, target)):
                    os.mkdir(os.path.join(self.location, target))

    def map_images_to_folders(self, train_validation_split: float) -> None:
        """
        Use: To create a mapping of the images to the classes of skin cancer. The images are then copied to the 
             subfolders created by "create_sub_folders".

        Args: None

        Returns: None
        """

        list_of_images = os.listdir(PopulateSubDirectories.Image_directory)
        train_images = random.sample(list_of_images, int(train_validation_split*len(list_of_images)))
        validation_image = np.setdiff1d(list_of_images, train_images)

        df = pd.read_csv(os.path.join(PopulateSubDirectories.Data_directory, "HAM10000_metadata"))

        class_list = []
        image_list_in_classes = []
        for target in PopulateSubDirectories.classes:
            df_temp = df[df.dx == target]
            image_list_in_classes.append(list(df_temp.image_id.values))
            class_list.append(target)
        
        mapping_dict = dict(zip(class_list, image_list_in_classes))

        if self.location.split("\\")[-1] == "Train":
            image_set = train_images
        else:
            image_set = validation_image

        for target in class_list:
            for image in image_set:
                if image.split(".")[0] in mapping_dict[target]:
                    current_dir = os.path.join(PopulateSubDirectories.Image_directory, image)
                    target_dir = os.path.join(os.path.join(self.location, target), image)
                    shutil.copyfile(current_dir, target_dir)

if __name__ == "__main__":
    # the zipped folders that contain images
    folders_to_unzip = ["HAM10000_images_part_1.zip", "HAM10000_images_part_2.zip", "ISIC2018_Task3_Test_Images.zip"]
    # the 3 folders we want to create
    data_splits = ["Train","Validation","Test"]

    for zipped_folder, split in zip(folders_to_unzip, data_splits):
        if zipped_folder == "ISIC2018_Task3_Test_Images.zip":
            clean_test_folder = TestCleanUp(zipped_folder)
            clean_test_folder.unzip_to_location(split)
            clean_test_folder.clean_folder()
        else:
            UnzipFiles(zipped_folder).unzip_to_location("Images")
            populate_split_folders = PopulateSubDirectories(split)
            populate_split_folders.create_sub_folders()
            
    for file in ["Train","Validation"]:
        PopulateSubDirectories(file).map_images_to_folders(TRAIN_VALIDATION_SPLIT)

    # removed the "Image" folder once all files copied across to train and validation subdirectories.
    shutil.rmtree(PopulateSubDirectories.Image_directory)