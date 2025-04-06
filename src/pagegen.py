import os
from blocks import markdown_to_html_node, extract_title
from htmlnode import LeafNode 

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
    
    destination = dest_path.split("/")
    folder_count = 0
    final_destination = "" 
    print(0000, destination)
    while folder_count < len(destination) - 1:
        print(9999, destination[folder_count], final_destination)
        if not os.path.exists(f"{destination[folder_count]}") and folder_count == 0:
            print(1111)
            os.mkdir(f"destination[0]")
        if not os.path.exists(f"{final_destination}/{destination[folder_count]}") and folder_count > 0:
            print(2222, final_destination, destination[folder_count])
            os.mkdir(f"{final_destination}/{destination[folder_count]}")
        final_destination += f"{destination[folder_count]}/"
        folder_count += 1
            
    # Need to create dest directories if they don't exist
    dest_file_ptr = open(dest_path, "w")
    dest_file_ptr.write(final_file)
    dest_file_ptr.close()


