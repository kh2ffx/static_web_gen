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
def make_destination(file_path):
    os.mkdir(file_path, mode=0o777)

# does Not do what it says ৻( •̀ ᗜ •́ ৻)
# takes file path "source"
# returns dictionary every folder inside is a dictionary with folder name
# as key.  Files have value None
# fatal flaw: does not return original source at head of dictionary, should fix later
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

def copy_tree(file_tree, source, destination):
    for folder in file_tree:
        if file_tree[folder] == None:
           shutil.copy(source + "/" + folder, destination)
        else:
            make_destination(destination + "/" + folder)
            copy_tree(file_tree[folder], source + "/" + folder, destination + "/" + folder)

def copy_paste(source, destination):
    # Step 1: delete current destination
    if os.path.exists(destination):
        delete_destination(destination)

    # Step 2: get a list of files in the source
    files_to_copy = list_paths(source)

    # Step 3: parse files and find out which are folder.  Make folders in destination
    make_destination(destination)
    copy_tree(files_to_copy, source, destination)            


