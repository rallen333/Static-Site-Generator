from textnode import *
from extract_links import *
import re
from markdown_to_blocks import *
import shutil
import os



def copy_to_dest_dir(source_dir, final_dir):
    shutil.rmtree(path=final_dir)
    if os.path.exists(final_dir) == False:
        os.mkdir(final_dir)
    
    copy_list = os.listdir(path=source_dir)
    for file in copy_list:
        source_path = os.path.join(source_dir, file)
        dest_path = os.path.join(final_dir, file)
        
        
        if os.path.isfile(source_path):
            shutil.copy(source_path, dest_path)
        else:
            os.mkdir(dest_path)
            copy_to_dest_dir(source_path, dest_path)

def extract_title(markdown):
    if not isinstance(markdown, str):
        raise Exception("Input must be a string")
    
    lines = markdown.split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith('# ') and not line.startswith('## '):
            return line[2:].strip()  
    raise Exception("No h1 heading in markdown")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path) as file:
        content = file.read()
        title = extract_title(content)
    
    with open(template_path) as file:
        template_content = file.read() 
    
    html_nodes = markdown_to_html_node(content)
    html_string = html_nodes.to_html()
    
    
    result = (template_content.replace("{{ Title }}", title)).replace("{{ Content }}", html_string) 

    final_dir = os.path.dirname(dest_path)

    if not os.path.exists(final_dir):
        os.makedirs(final_dir)

    with open(dest_path, "w") as file:
        file.write(result)
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    content_dir = os.listdir(dir_path_content)
    for object in content_dir:
        
        source_path = os.path.join(dir_path_content, object)
        dest_path = os.path.join(dest_dir_path, object)
        
        if not os.path.isfile(source_path):
            os.makedirs(dest_path, exist_ok=True)
            generate_pages_recursive(source_path, template_path, dest_path)
        
        else:
            if object.endswith("md"):
                html_file = object.replace(".md", ".html")
                dest_path = os.path.join(dest_dir_path, html_file)
                generate_page(source_path, template_path, dest_path) 
           

    


def main():
    generate_pages_recursive("./content", "./template.html", "./public")
if __name__ == "__main__":
    main()



       
        