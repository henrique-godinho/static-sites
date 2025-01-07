from htmlnode import *
from textnode import *
from htmlnode import *
import re


def text_node_to_html_node(text_node):
    match text_node.text_type.value:
        case "text":
            return LeafNode(None, text_node.text)
        case "bold":
            return LeafNode("b", text_node.text)
        case "italic":
            return LeafNode("i", text_node.text)
        case "code":
            return LeafNode("code", text_node.text)
        case "link":
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case "image":
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Invalid Type")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL_TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.NORMAL_TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return images


def extract_markdown_links(text):
    links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return links


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL_TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.NORMAL_TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGES,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.NORMAL_TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL_TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.NORMAL_TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINKS, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.NORMAL_TEXT))
    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.NORMAL_TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD_TEXT)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC_TEXT)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE_TEXT)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    blocks = []
    split = markdown.split("\n\n")
    for item in split:
        if len(item) != 0:
            stripped_item = item.strip()
            blocks.append(stripped_item)
    return blocks

def block_to_block_type(block):
    if "# " in block[:7]:
        return "heading"
    if block.startswith("```") and block.endswith("```"):
        return "code"
    multi_line_block = block.split("\n")
    if all(item.startswith(">") for item in multi_line_block):
        return "quote"
    if all(item.startswith("* ") or item.startswith("- ") for item in multi_line_block):
        return "ul"
    counter = 1
    truthy = []
    for item in multi_line_block:
        if item.startswith(f"{counter}. "):
            truthy.append(True)
            counter += 1
    if truthy:
        if len(truthy) == len(multi_line_block):
            return "ol"
    return "paragraph"

def markdown_to_html_node(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    children = []  # List to collect all block nodes
    
    for block in markdown_blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case "heading":
                children.append(header_block_type(block))
            case "code":
                children.append(code_block_type(block))
            case "quote":
                children.append(quote_block_type(block))
            case "ul":
                children.append(ul_block_type(block))
            case "ol":
                children.append(ol_block_type(block))
            case "paragraph":
                children.append(paragraph_block_type(block))
    
    # Create and return a div containing all blocks
    return ParentNode("div", children)


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def header_block_type(block):
    block_array = block.split(" ", 1)
    heading_size = len(block_array[0])
    tag = f"h{heading_size}"
    children = text_to_children(block_array[1])
    header_node = ParentNode(tag, children)
    return header_node

def code_block_type(block):
    tag = "code"
    children = text_to_children(block[3:-3])
    code_node = ParentNode(tag, children)
    parent = ParentNode("pre", [code_node])
    return parent

def quote_block_type(block):
    tag = "blockquote"
    block_array = block.split("\n")
    text = " ".join(line[1:].strip() for line in block_array)
    children = text_to_children(text)
    return ParentNode(tag, children)

def ul_block_type(block):
    children = []
    block_array = block.split("\n")
    for item in block_array:
        item_text = item[2:].strip()
        item_children = text_to_children(item_text)
        li_node = ParentNode("li", item_children)
        children.append(li_node)
    return ParentNode("ul", children)


def ol_block_type(block):
    children = []
    block_array = block.split("\n")
    for item in block_array:
        # Remove the "1. " prefix (or "2. ", "3. ", etc)
        item_text = item[3:].strip()
        # Process any markdown inside the list item
        item_children = text_to_children(item_text)
        # Create li node with the processed children
        li_node = ParentNode("li", item_children)
        children.append(li_node)
    return ParentNode("ol", children)

def paragraph_block_type(block):
    children = text_to_children(block)
    return ParentNode("p", children)

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            line = line.lstrip("# ")
            return line
        raise Exception("No Title found")
