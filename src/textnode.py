from enum import Enum
from htmlnode import *
from extract_links import *

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):           
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other_node):
        if self.text_type == other_node.text_type and self.text == other_node.text and self.url == other_node.url:
            return True
        
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    def to_html(self):
        if self.text_type == TextType.TEXT:
            return self.text
        elif self.text_type == TextType.BOLD:
            return f"<b>{self.text}</b>"
        elif self.text_type == TextType.ITALIC:
            return f"<i>{self.text}</i>"
        elif self.text_type == TextType.CODE:
            return f"<code>{self.text}</code>"
        elif self.text_type == TextType.LINK:
            return f"<a href=\"{self.url}\">{self.text}</a>"
        else:
            raise ValueError(f"Invalid text type: {self.text_type}")
    

        
def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text, None)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text, None)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text, None)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text, None)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
        raise Exception("Invalid TextNode type")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
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


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        text = node.text
        extracted_info = extract_markdown_images(text)
        
        if extracted_info == []:
            new_nodes.append(node)
            continue

        for tuple in extracted_info:

            sections = text.split(f"![{tuple[0]}]({tuple[1]})", 1)
            first_node = TextNode(sections[0], TextType.TEXT)
            image_node = TextNode(tuple[0], TextType.IMAGE, tuple[1])
            text = sections[1]

            if first_node.text != "":
                new_nodes.append(first_node)
            new_nodes.append(image_node)
        if text != "":
            final_node = TextNode(text, TextType.TEXT)
            new_nodes.append(final_node)

    return new_nodes
 

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        text = node.text
        extracted_info = extract_markdown_links(text)

        if extracted_info == []:
            new_nodes.append(node)
            continue

        for tuple in extracted_info:

            sections = text.split(f"[{tuple[0]}]({tuple[1]})", 1)
            first_node = TextNode(sections[0], TextType.TEXT)
            link_node = TextNode(tuple[0], TextType.LINK, tuple[1])
            text = sections[1]

            if first_node.text != "":
                new_nodes.append(first_node)
            new_nodes.append(link_node)
        if text != "":
            final_node = TextNode(text, TextType.TEXT)
            new_nodes.append(final_node)


    return new_nodes


def text_to_textnodes(text):
    initial_node = TextNode(text, TextType.TEXT)
    return split_nodes_link(
        split_nodes_image(
        split_nodes_delimiter(
        split_nodes_delimiter(
        split_nodes_delimiter([initial_node], "**", TextType.BOLD), 
        "*", TextType.ITALIC), "`", TextType.CODE)))
    