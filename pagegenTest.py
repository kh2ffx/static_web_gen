import sys

sys.path.append("/home/t/Source/git/static_web_gen/src")
#/home/t/Source/git/static_web_gen/src/pagegen.py
from pagegen import generate_page

from_path = "content/index.md"
template_path = "template.html"
dest_path = "public/test.html"

generate_page(from_path, template_path, dest_path)
