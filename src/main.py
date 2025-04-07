from textnode import TextNode, TextType
from copypaste import copy_paste
from pagegen import generate_page, recursive_pagegen
import sys

dir_path_static = "./static"
dir_path_docs = "./docs"
dir_path_content = "./content"
templat_path = "./template.html"

try:
    BASEPATH = sys.argv[1]
except IndexError:
    BASEPATH = "/"

def main():
    #copy_paste will need to be updated to handle different filepaths
    copy_paste(dir_path_static, dir_path_docs)
    recursive_pagegen(dir_path_content, "template.html", dir_path_docs, BASEPATH)


main()
