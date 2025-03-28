from enum import Enum
from textnode import text_to_textnodes, text_node_to_html_node
from htmlnode import LeafNode, ParentNode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

# markdown argument is a string representing a full document in markdown format
# markdown_to_blocks is meant to split sections delineated by double newline ("\n\n")
# into separate strings, format them and return them in a list

# returns a list of blocks
def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    new_blocks = []
    for block in blocks:
        if block == "":
            continue
        new_block = block.strip('\n ')
        new_blocks.append(new_block)
    return new_blocks

# takes a block and decides what kind of block it is
def block_to_blocktype(markdown_text):
    if "# " in markdown_text[0:7]:
        return BlockType.HEADING
    if (
            "```" in markdown_text[0:3] and
            "```" in markdown_text[len(markdown_text):len(markdown_text) -4 : -1]
        ):
        return BlockType.CODE
    markdown_text_split_newline = markdown_text.split("\n")
    quote = 0
    unordered_list = 0
    ordered_list = 0
    for newline in markdown_text_split_newline:
        if len(newline) == 0:
            continue
        if newline[0] == ">":
            quote += 1
        if newline[0:2] == "- ":
            unordered_list += 1
        if newline[1:3] == ". " and int(newline[0]) == ordered_list + 1:
            # I read the assignment backwards 𓁹‿𓁹 HEH.
            ordered_list += 1
    if quote == len(markdown_text_split_newline):
        return BlockType.QUOTE
    if unordered_list == len(markdown_text_split_newline):
        return BlockType.UNORDERED_LIST
    if ordered_list == len(markdown_text_split_newline):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

# takes block and formats html inside block
def block_text_to_html(block_text):
    new_block_text = ""
    # take text from blocktype and split into lists of textnodes 
    # to add bold, italic, etc html formatting *textnodes is a list*
    textnodes = text_to_textnodes(block_text)
    for textnode in textnodes:
        # this part will format the text
        new_text = text_node_to_html_node(textnode).to_html()
        #add it to a new text string
        new_block_text += new_text
    #return new block_text
    return new_block_text

def find_the_header_number(line):
    header_number = 0
    for char in line:
        if char == "#":
            header_number += 1
        else:
            continue
    return header_number

# function to strip quote and list tags from individual lines 
# will update to handle header level
def line_stripper(blocktype, block):
    if blocktype == BlockType.CODE:
        return block.strip("```\n")
    new_block = ""
    counter = 0
    lines = block.split("\n")
    for line in lines:
        match blocktype:
            case BlockType.HEADING:
                new_block += block.strip("# ")
            case BlockType.QUOTE:
                if counter > 0:
                    new_block += (" " + line.strip("> "))
                else:
                    new_block += (line.strip("> "))    
                counter += 1
            case BlockType.UNORDERED_LIST:
                new_block += (line.replace("- ", "<li>") + "</li>")
            case BlockType.ORDERED_LIST:
                new_block += (line.replace(f"{counter + 1}. ", "<li>") + "</li>")
                counter += 1
            case BlockType.PARAGRAPH:
                if line == "\n":
                    continue
                if counter == 0:
                    new_block += line
                else:
                    new_block += " " + line
                counter += 1

    return new_block

# take markdown block and turn into hmtl block
def block_to_htmlblock(blocktype, block):
    match blocktype:
        case BlockType.PARAGRAPH:
            return LeafNode("p", f"{line_stripper(blocktype, block_text_to_html(block))}")
        case BlockType.HEADING:
            # This should probably be updated at some point to take into consideration
            # the type of heading (level of heading?)
            return LeafNode(f"h{find_the_header_number(block)}",
                            f"{line_stripper(blocktype, block_text_to_html(block))}")
        case BlockType.CODE:
            return LeafNode("pre", f"<code>{line_stripper(blocktype,block)}\n</code>")
        case BlockType.QUOTE:
            return LeafNode("blockquote", f"{block_text_to_html(line_stripper(blocktype,block))}")
        case BlockType.UNORDERED_LIST:
            return LeafNode("ul", f"{block_text_to_html(line_stripper(blocktype,block))}")
        case BlockType.ORDERED_LIST:
            return LeafNode("ol", f"{block_text_to_html(line_stripper(blocktype, block))}")

#takes all Leafs as list and contains them in a <div> tag
def LeafNodes_to_ParentNodes(LeafNodes):
    return ParentNode("div", LeafNodes) # (╭ರ_•́)

#this is the function that pulls all the parts together
#It will take a full markdown doc and use the previous methods to turn it into an HTML node
def markdown_to_html_node(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    future_parent = [] #empty list to contain leafnodes from following loop
    for block in markdown_blocks:
        blocktype = block_to_blocktype(block)
        future_child = block_to_htmlblock(blocktype, block)
        future_parent.append(future_child)
    return ParentNode("div", future_parent)


