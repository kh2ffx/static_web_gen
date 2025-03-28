from enum import Enum
from htmlnode import LeafNode
import re

class TextType(Enum):
    TEXT = "text"
    BOLD_TEXT = "bold"
    ITALIC_TEXT = "italic"
    CODE_TEXT = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if (
                self.text == other.text and self.text_type == other.text_type 
                and self.url == other.url): 
            return True
        else:
            return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD_TEXT: 
            return LeafNode("b", text_node.text)
        case TextType.ITALIC_TEXT: 
            return LeafNode("i", text_node.text)
        case TextType.CODE_TEXT: 
            return LeafNode("code", text_node.text)
        case TextType.LINK: 
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE: 
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError("type not recognized")
    ### I'm too sleepy and this is too annoying

# function to split list of text nodes along delimiter ex. "**Bold**" and return 
# list of LeafNodes with text and delimiters organized  
#def split_nodes_delimiter (old_nodes, delimiter, text_type):
#    new_nodes = []
#    for node in old_nodes:
#        new_nodes_text = node.text.split(delimiter)
#        new_nodes_text.append(new_nodes_text)
#        new_nodes.append(TextNode(new_nodes_text[0], TextType.TEXT))
#        new_nodes.append(TextNode(new_nodes_text[1], text_type))
#        new_nodes.append(TextNode(new_nodes_text[2], TextType.TEXT))
#    return new_nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT: 
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0: # splitting node should produce 3 nodes
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT: 
            new_nodes.append(old_node)
            continue
        old_node_text = old_node.text
        split_nodes = []
        found_links = extract_markdown_images(old_node_text)
        if len(found_links) == 0:
            new_nodes.append(old_node)
            continue
        for i in range(0, len(found_links)):
            sections = old_node_text.split(f"![{found_links[i][0]}]({found_links[i][1]})")
            if sections[0] != "":
                split_nodes.append(TextNode(sections[0], TextType.TEXT))
            split_nodes.append(TextNode(found_links[i][0], TextType.IMAGE, found_links[i][1]))
            if i+1 < len(found_links):
                old_node_text = sections[1]
            else:
                if sections[1] == "":
                    continue
                split_nodes.append(TextNode(sections[i+1], TextType.TEXT))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT: 
            new_nodes.append(old_node)
            continue
        old_node_text = old_node.text
        split_nodes = []
        found_links = extract_markdown_links(old_node_text)
        if len(found_links) == 0:
            new_nodes.append(old_node)
            continue
        for i in range(0, len(found_links)):
            sections = old_node_text.split(f"[{found_links[i][0]}]({found_links[i][1]})")
            if sections[0] != "":
                split_nodes.append(TextNode(sections[0], TextType.TEXT))
            split_nodes.append(TextNode(found_links[i][0], TextType.LINK, found_links[i][1]))
            if i+1 < len(found_links):
                old_node_text = sections[1]
            else:
                if sections[1] == "":
                    continue
                split_nodes.append(TextNode(sections[1], TextType.TEXT))
        new_nodes.extend(split_nodes)
    return new_nodes

def text_to_textnodes(text):
    text_nodes = [TextNode(text, TextType.TEXT)]
    text_nodes = split_nodes_delimiter(text_nodes, "**", TextType.BOLD_TEXT)
    text_nodes = split_nodes_delimiter(text_nodes, "_", TextType.ITALIC_TEXT)
    text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.CODE_TEXT)
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)
    return text_nodes

