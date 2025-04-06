from textnode import TextNode, TextType
from copypaste import copy_paste
from pagegen import generate_page

def main():
    #copy_paste will need to be updated to handle different filepaths
    source = "static"
    destination = "public"
    copy_paste(source, destination)
    generate_page(f"content/index.md", "template.html", f"{destination}/index.html")
    generate_page(f"content/blog/glorfindel/index.md", "template.html", "public/blog/glorfindel/index.html")
    generate_page(f"content/blog/majesty/index.md", "template.html", "public/blog/majesty/index.html")
    generate_page(f"content/blog/tom/index.md", "template.html", "public/blog/tom/index.html")
    generate_page(f"content/contact/index.md", "template.html", "public/contact/index.html")


main()
