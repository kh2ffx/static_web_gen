#!/usr/bin/env python3

############################################################################
# children - A list of HTMLNode objects representing the children of this node
############################################################################
# props - A dictionary of key-value pairs representing the attributes of the 
# HTML tag. For example, a link (<a> tag) might have 
# {"href": "https://www.google.com"}
############################################################################
class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        if self.props is None:
            return ""
        prop_string = ""
        for key in self.props:
            prop_string += f' {key}="{self.props[key]}"'
        return prop_string

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

class LeafNode(HTMLNode):
                            #Value Required for Leafs
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError(f"{self} must have a value")
        
        # format first tag with string from props attribute
        open_tag = self.tag
        if self.props is not None:
            open_tag = f"{self.tag}{self.props_to_html()}"
        
        if self.tag is None:
            return self.value
        else:
            return f"<{open_tag}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError(f"{self} must have a tag value")
        if self.children is None:
            raise ValueError(f"{self} must have a children value")
        return f"<{self.tag}{self.props_to_html()}>{self.recursed_children()}</{self.tag}>"

    def recursed_children(self):
        return_text = ""
        for node in self.children:
            if self.children is ParentNode:
               node.recursed_children()
            return_text += (node.to_html()) 
        return return_text

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"   

