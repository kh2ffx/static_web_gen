#!/usr/bin/env python3
# remove this shebang and make file not executable when finished

import os
import shutil

#source directory will be "static", destination directory will be "public"

# first delete contents of destination directory
# deletes destination directory as well ( ˶°ㅁ°) !!
def delete_destination(path_to_destination):
    if os.path.exists(path_to_destination):
        shutil.rmtree(path_to_destination)
        print(f"{path_to_destination} deleted ˗ˏˋ ✸ ˎˊ˗")
    else:
        raise ValueError(f"{path_to_destination} does not exist")

# will take list of file paths
def make_destinations(file_paths):
    for file_path in file_paths:
        path = file_path.split("/")
        
    os.mkdir(path_to_destination, mode=0o777)

# does Not do what it says ৻( •̀ ᗜ •́ ৻)
# takes file path "source"
# returns dictionary every folder inside is a dictionary with folder name
# as key.  Files have value None
def list_paths(source):

    if os.path.isfile(source):
        return source
    file_list = os.listdir(source)
    final_dict = {}
    for file in file_list:
        if os.path.isfile(source + "/" + file):
            final_dict[file] = None
        else:
            final_dict[file] = list_paths(source + "/" + file)
    return final_dict


path_to_destination = "public"
path_to_source = "static"
#delete_destination(path_to_destination)
#make_destination(path_to_destination)
print(list_paths(path_to_source))
