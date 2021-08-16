import tkinter as tk
from tkinter import filedialog
import os
from PIL import Image
from PIL.ExifTags import TAGS

root = tk.Tk() # Initializes Tkinter window for file selection.
root.withdraw() # Hides window until get_file_path function is called.

IMAGE_TYPES = ['png', 'jpg', 'tiff','jpeg']


def get_file_path():
    """Returns file path of images from user input."""
    file_path = filedialog.askdirectory()
    return file_path


def get_photo_location_path():
    """Returns file path of images from user input."""
    location_path = filedialog.askdirectory()
    return location_path


def check_if_image(image):
    """Checks the file extension if it is an image. Returns filename of if it is an
    image, else returns None."""
    name_reversed = image[::-1] # Reverses the name to find full stop easier.
    index = 0
    for i in range(len(name_reversed)): # Finds the index of the full stop.
        if name_reversed[i] == ".":
            index = i

        # Returns true if the the file is an image.
        if image[len(image) - index:] in IMAGE_TYPES:
            return True
    return False


def get_image_list(file_path):
    """Returns all of the images in the directory."""
    files = os.listdir(file_path)
    images = [file for file in files if check_if_image(file)]
    return images


def get_image_data(image):
    """Takes an image file and returns a dict of all of the metadata tags and their values.

    Args:
        image (string): The path to the image.
    """
    image = Image.open(image)
    exifdata = image.getexif()
    exif_data_dict = dict()
    for tag_id in exifdata:
        key, value = TAGS.get(tag_id, tag_id), exifdata.get(tag_id)
        if isinstance(value, bytes):
            value = value.decode()
        exif_data_dict[key] = value
    return exif_data_dict


def sort_date(image_date):
    """Sorts the image by the date it was taken.
    Args:
        image_date (string): The date the image was taken.
    """



def sort_name(image_list):
    """Sorts the image list by the name.

    Args:
        image_list (list): The unsorted list of images.
    """
    sorted_list = sorted(image_list)
    return sorted_list


def main():
    """Main."""
    from_path = get_file_path()
    image_list = get_image_list(from_path)
    print(image_list)
    for image in image_list:
        data = get_image_data(f"{from_path}/{image}")
        print(data)
    to_path = get_photo_location_path()
    print(sort_name(image_list))


main()
