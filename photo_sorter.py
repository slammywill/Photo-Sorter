"""Sorting ++ Aplication.

Sorts photos based on their metadata.

Author: Sam Willems
"""

import tkinter as tk
from tkinter import filedialog
import os
from PIL import Image
from PIL.ExifTags import TAGS
from pyglet import *


root = tk.Tk() # Initializes Tkinter window for file selection.
root.withdraw() # Hides window until get_file_path function is called.


# Pyglet initialisation for GUI.
WINDOW_SIZE = (400, 550)
TITLE = 'Sorting ++'
WINDOW = window.Window(*WINDOW_SIZE, TITLE)
resource.path = ["resources"]
resource.reindex()

# Constant declaration.
IMAGE_TYPES   = ['png', 'jpg', 'tiff','jpeg']
SEL_BTN_1_POS = (WINDOW_SIZE[0] // 2, 283)
SEL_BTN_2_POS = (WINDOW_SIZE[0] // 2, 133)
GO_BTN_POS    = (85, 38)

# Global variable declaration.
path_to_photos   = ''
path_to_location = ''


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
    """Returns all of the images in the directory.

    Args:
        file_path (string): The path to the file containing the images.
    """
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


def draw():
    """Initialises the background and the buttons to draw to the window every frame.
    """
    background = sprite.Sprite(img=resource.image("background.png"), x=0, y=0)
    background.draw()


def check_button_click(b_x, b_y, m_x, m_y):
    """Checks whether a button was pressed on click.

    Args:
        b_x (int): x-position of button.
        b_y (int): y-position of button.
        m_x (int): x-position of mouse.
        m_y (int): y-position of mouse.
    """
    if b_x - 72 < m_x < b_x + 72:
        if b_y - 22 < m_y < b_y + 22:
            return True
    return False


@WINDOW.event
def on_mouse_press(x, y, button, modifiers):
    """Called when mouse clicks.
    """
    if check_button_click(*SEL_BTN_1_POS, x, y):
        print("Select button 1 clicked!")
        path_to_photos = get_file_path()
        path_to_location = get_photo_location_path()
    elif check_button_click(*SEL_BTN_2_POS, x, y):
        print("Select button 2 clicked!")
    elif check_button_click(*GO_BTN_POS, x, y):
        print("Go button clicked!")


@WINDOW.event
def on_draw():
    """Renders the pyglet window.
    """
    WINDOW.clear()
    draw()


def main():
    """Main."""
    app.run() # Run pyglet window.
    # from_path = get_file_path()
    # image_list = get_image_list(from_path)
    # print(image_list)
    # for image in image_list:
    #     data = get_image_data(f"{from_path}/{image}")
    #     print(data)
    # to_path = get_photo_location_path()
    # print(sort_name(image_list))


main()


# TODO: Add error exception for file path.
