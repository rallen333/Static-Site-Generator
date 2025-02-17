import re


def extract_markdown_images(text):
    extracted_info = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return extracted_info

def extract_markdown_links(text):
    extracted_info = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return extracted_info
