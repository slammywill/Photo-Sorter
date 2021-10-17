"""Sorting ++ Aplication.

Sorts photos based on their EXIF metadata.

Author: Sam Willems
"""

import tkinter as tk
from tkinter import filedialog
import os
import shutil
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

# Global variables.
old_path = "/"
new_path = "/"
image_list = []
sorting_type = ""
show_selection_box = False
allow_sort_click = False


def get_file_path():
    """Sets the old file path of images from user input."""
    return filedialog.askdirectory()


def get_photo_location_path():
    """Sets the new file path of images from user input."""
    return filedialog.askdirectory()


def get_sorting_type():
    """Creates a window to ask the user which sorting algorithm they want to use."""
    global show_selection_box
    show_selection_box = True


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


def sort_date_taken():
    """Sorts the image by the date it was taken.
    Args:
        image_date (string): The date the image was taken.
    """
    image_data = dict()
    for image in image_list:
        image_data[image] = get_image_data(f"{old_path}/{image}")
    new_list = sorted(image_data.items(), key=get_date)
    sorted_list = list()
    for i in new_list:
        sorted_list.append(i[0])
    return new_list


def get_date(image):
    """Returns the date an image was taken, 0 if not provided.

    Args:
        image (tuple): The image tuple containing its name and metadata.
        """
    if "DateTime" not in image[1]:
        image[1]["DateTime"] = "999999999" # Moves image to end of list if no DateTime given.
    return image[1]["DateTime"]



def sort_name():
    """Sorts the image list by the name.

    Args:
        image_list (list): The unsorted list of images.
    """
    sorted_list = sorted(image_list)
    return sorted_list


def draw():
    """Initialises the background and the buttons to draw to the window every frame.
    """
    background_image = resource.image("background.png")
    background_image.width, background_image.height = WINDOW_SIZE[0], WINDOW_SIZE[1]
    background_image.blit(x=0, y=0, z=-1)

    selection_box = resource.image("selection_box.png")
    selection_box.width, selection_box.height = 187, 77
    if show_selection_box:
        selection_box.blit(x=115, y=90, z=1)

    from_path_label    = text.Label(f"{old_path[:37]}", font_name="Menlo", font_size=10, x=75, y=349, color=(150,150,150,255))
    to_path_label      = text.Label(f"{new_path[:37]}", font_name="Menlo", font_size=10, x=75, y=322, color=(150,150,150,255))
    sorting_type_label = text.Label(f"{sorting_type.capitalize()}",  font_name="Menlo", font_size=10, x=75, y=173, color=(150,150,150,255))

    to_path_label.draw()
    from_path_label.draw()
    sorting_type_label.draw()



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


def get_sort_type_from_selection(m_x, m_y):
    """Returns which sorting algorithm was selected.

    Args:
        m_x (int): x-position of the mouse.
        m_y (int): y-position of the mouse.
        """
    if  280 > m_x > 115:
        if 170 > m_y > 125:
            return 'name'
        elif 125 > m_y > 95:
            return 'date taken'
    return None

@WINDOW.event
def on_mouse_press(x, y, b, m):
    """Called when mouse clicks.

    Args:
        x (int): x-position of the mouse.
        y (int): y-position of the mouse.
        b & m: Not used, required for mouse press module function.
    """
    global allow_sort_click, show_selection_box, old_path, new_path, image_list, sorting_type
    if allow_sort_click:
        sorting_type = get_sort_type_from_selection(x, y)
        if sorting_type == None:
            sorting_type = ""
        allow_sort_click = False
        show_selection_box = False
        if sorting_type == 'name':
            image_list = sort_name()
        elif sorting_type == 'date taken':
            image_list = sort_date_taken()
    elif check_button_click(*SEL_BTN_1_POS, x, y):
        old_path = get_file_path()
        new_path = get_photo_location_path()
        image_list = get_image_list(old_path)
    elif check_button_click(*SEL_BTN_2_POS, x, y):
        get_sorting_type()
        allow_sort_click = True
    elif check_button_click(*GO_BTN_POS, x, y):
        move_images(old_path, new_path, image_list)


def move_images(path_from, path_to, images):
    """Moves the images from their current location to the new location specified
    by the user.

    Args:
        path_from (string): file path that the images are coming from.
        path_to (string): file path that the images are going to.
        images (list): The list of all images."""

    for image in images:
        shutil.copy(f"{path_from}/{image[0]}", f"{path_to}/{image[0]}")
        os.remove(f"{path_from}/{image[0]}")


@WINDOW.event
def on_draw():
    """Renders the pyglet window.
    """
    WINDOW.clear()
    draw()


def main():
    """Main."""
    app.run()


main()
