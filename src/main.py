#!/usr/bin/env python3

from textnode import TextNode, TextType

def main():
    text = TextNode("this is some anchor text", TextType.LINK, "http://localhost:8888")
    print(text)

main()
