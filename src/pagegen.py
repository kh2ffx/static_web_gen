import os
from blocks import markdown_to_html_node, extract_title
from htmlnode import LeafNode 
from copypaste import copy_tree, list_paths

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    #open
    from_file_ptr = open(from_path, "r")
    template_file_ptr = open(template_path, "r")
    #make variable
    from_file = from_file_ptr.read()
    template_file = template_file_ptr.read()
    #close
    from_file_ptr.close()
    template_file_ptr.close()
    title = extract_title(from_file)

    from_file = markdown_to_html_node(from_file)
    file_contents = from_file.to_html()

    template_file_two = template_file.replace("{{ Title }}", title)
    final_file = template_file_two.replace("{{ Content }}", file_contents)
    
    # I hate the whole idea of this and I've probably done it in a stupid way
    # I will fix this one day (probably not)
    destination = dest_path.split("/")
    folder_count = 0
    final_destination = "" 
    while folder_count < len(destination) - 1:
        if not os.path.exists(f"{destination[folder_count]}") and folder_count == 0:
            os.mkdir(f"destination[0]")
        if not os.path.exists(f"{final_destination}/{destination[folder_count]}") and folder_count > 0:
            os.mkdir(f"{final_destination}/{destination[folder_count]}")
        final_destination += f"{destination[folder_count]}/"
        folder_count += 1
            
    # Need to create dest directories if they don't exist
    dest_file_ptr = open(dest_path, "w")
    dest_file_ptr.write(final_file)
    dest_file_ptr.close()

# adding this here, but I should replace a function in copypaste with this one
def recursive_pagegen_helper(directory, template_path):
    for file in os.listdir(directory):
        filepath = os.path.join(directory, file)
        if os.path.isfile(filepath) and file[len(file) - 3 :] == ".md":
            generate_page(filepath, template_path, 
            f"{filepath[:len(filepath) - 3]}.html")
            #delete .md file later
        elif not os.path.isfile(filepath):
            recursive_pagegen_helper(filepath, template_path)

def recursive_pagegen(from_path_directory, 
                      template_path, 
                      destination_path_directory):
    # copy everything from content directory to public 
    copy_tree(list_paths(from_path_directory), 
              from_path_directory, 
              destination_path_directory)
    # Now I need to convert the markdown ".md" files in the public
    # directory to html 
    recursive_pagegen_helper(destination_path_directory, template_path)
