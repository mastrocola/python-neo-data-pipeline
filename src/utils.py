import os


def verify_folder_and_create_if_not_exists(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
