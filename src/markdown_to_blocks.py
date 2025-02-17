from textnode import *


def markdown_to_blocks(markdown):
    lines = markdown.split("\n\n")
    block_list = []
    for line in lines:
            new_line = line.strip()
            if new_line != "":
                block_list.append(new_line)
    return block_list
    

def block_to_block_type(block):

    def check_order_list(block):
        ordered_list_check = block.split("\n")
        order_list = []
        for line in ordered_list_check:
            if ". " in line:
                period_position = line.find(".")
                if line != "" and line[:period_position].isdigit():
                    order_list.append(int(line[:period_position]))
        expected_sequence = list(range(1, len(order_list)+1))   
        if order_list != [] and order_list[0] == 1 and order_list == expected_sequence:
            return True
        return False
        
    def check_heading(block):
        text = block.strip("#")
        count = 0 
        for char in block:
            if char == "#":
                count += 1
        if count > 0 and count <= 6 and text[0] == " " and text[1:].strip():
            return True
        return False
    
    def check_quotes(block):
        lines = block.split("\n")
        actual = []
        for line in lines:
            if line[0] == ">":
                actual.append(line)
        if lines == actual:
            return True
        return False
    
    def check_unordered_list(block):
        lines = block.split("\n")
        actual = []
        for line in lines:
            if line.startswith("* ") or line.startswith("- "):
                actual.append(line)
        if lines == actual:
            return True
        return False

    


    if check_heading(block) == True:
        block = "heading"
    elif block.startswith("```") and block.endswith("```"):
        block = "code"
    elif check_quotes(block) == True:
        block = "quote"
    elif check_unordered_list(block) == True:
        block = "unordered_list"
    elif check_order_list(block) == True:
        block = "ordered_list"
    else:
        block = "paragraph"

    return block
                   
          
    

def markdown_to_html_node(markdown):
    parent_node = HTMLNode("div", "", [])
    block_list = markdown_to_blocks(markdown)
    for block in block_list:
        type = block_to_block_type(block)
        if type == "heading":
            node = md_block_to_html_heading(block)
            parent_node.children.append(node)
        elif type == "code":
            node1 = HTMLNode("code", strip_backticks(block))
            node = HTMLNode("pre", "", [])
            node.children.append(node1)
            parent_node.children.append(node)
        elif type == "ordered_list":
            node = md_block_to_html_olist(block)
            parent_node.children.append(node)
        elif type == "paragraph":
            node = HTMLNode("p", "", [])
            node.children.extend(text_to_children(block))
            parent_node.children.append(node)
        elif type == "quote":
            node = HTMLNode("blockquote", "", [])
            node.children.extend(text_to_children(block[1:].strip()))
            parent_node.children.append(node)
        elif type == "unordered_list":
            node = md_block_to_html_ulist(block)
            parent_node.children.append(node)
        else:
            raise ValueError(f"Unknown block type encountered: {type}") 

    return parent_node

def md_block_to_html_olist(block):
        lines = block.split("\n")
        ord_list = HTMLNode("ol", "", [])
        for line in lines:
            if len(line) >= 3 and line[0].isdigit() and line[1] == "." and line[2] == " ":
                line_node = HTMLNode("li", line[3:], text_to_children(line[3:]))
                ord_list.children.append(line_node)
        return ord_list
    
def md_block_to_html_ulist(block):
        lines = block.split("\n")
        unord_list = HTMLNode("ul", "", [])
        for line in lines:
            if len(line) >= 3 and (line[0] == "*" or line[0] == "-") and line[1] == " ": 
                line_node = HTMLNode("li", line[2:], text_to_children(line[2:]))
                unord_list.children.append(line_node)
        return unord_list

def text_to_children(text):
    tnodes_list = text_to_textnodes(text)
    html_nodes = []
    for tnode in tnodes_list:
        html_node = text_node_to_html_node(tnode)
        html_nodes.append(html_node)
    return html_nodes
    
def md_block_to_html_heading(block):
        if block.startswith("# "):
            return ParentNode("h1", text_to_children(block[2:]))                    
        elif block.startswith("## "):
            node = HTMLNode("h2", "", text_to_children(block[3:]))
        elif block.startswith("### "):
            node = HTMLNode("h3", "", text_to_children(block[4:]))
        elif block.startswith("#### "):
            node = HTMLNode("h4", "", text_to_children(block[5:]))
        elif block.startswith("##### "):
            node = HTMLNode("h5", "", text_to_children(block[6:]))
        elif block.startswith("###### "):
            node = HTMLNode("h6", "", text_to_children(block[7:]))
        else:
            raise ValueError(f"Invalid heading format: {block}")
        return node

def strip_backticks(block):
        backtick_count = 0
        for char in block:
            if char == "`":
                backtick_count += 1
            else:
                break
        if block[-backtick_count:] != "`" * backtick_count:
            raise ValueError("Mismatched backticks!")
        return block[backtick_count:-backtick_count].strip()
    
    

    