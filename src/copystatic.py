import os
import shutil
from pathlib import Path
from markdown_to_html_node_helper import markdown_to_html_node, extract_title

def copy_static(origin_path="static/", destination_path="public/"):

    if os.path.exists(destination_path):
        shutil.rmtree(destination_path)
    os.mkdir(destination_path)
    origin_contents = os.listdir(origin_path)

    for file in origin_contents:
        source = os.path.join(origin_path, file)
        dest = os.path.join(destination_path, file)
        print(f"  *  {source} -> {dest}")
        if os.path.isfile(source):
            shutil.copy(source, dest)
        else:
            os.mkdir(dest)
            copy_static(source, dest)

def generate_page(from_path="content/index.md", template_path="./template.html", dest_path="public/index.html"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    md_file = open(from_path)
    html_file = open(template_path)
    markdown = md_file.read()
    html_template = html_file.read()

    html_node = markdown_to_html_node(markdown)
    html_string = html_node.to_html()
    page_title = extract_title(markdown)
    html_with_title = html_template.replace("{{ Title }}", page_title)
    html = html_with_title.replace("{{ Content }}", html_string)
    
    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    public_html = open(dest_path, "w")
    public_html.write(html)

    md_file.close()
    html_file.close()
    public_html.close()

def generate_page_recursive(dir_path_content="content/", template_path="./template.html", dest_dir_path="public/"):
    if os.path.isfile(dir_path_content):
        # Replace 'content/' with 'public/' and '.md' with '.html'
        dest_path = dir_path_content.replace('content/', 'public/').replace('.md', '.html')
        generate_page(dir_path_content, template_path, dest_path)
        return
        
    if os.path.isdir(dir_path_content):
        contents = os.listdir(dir_path_content)
        for content in contents:
            content_path = os.path.join(dir_path_content, content)
            generate_page_recursive(content_path, template_path, dest_dir_path)
    