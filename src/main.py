from textnode import TextNode, TextType
from copypaste import copy_paste
from pagegen import generate_page, recursive_pagegen

def main():
    #copy_paste will need to be updated to handle different filepaths
    source = "static"
    destination = "public"
    copy_paste(source, destination)
    generate_page(f"content/index.md", 
                  "template.html", 
                  f"{destination}/index.html")
    recursive_pagegen("content", "template.html", "public")


main()
