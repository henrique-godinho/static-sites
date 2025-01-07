import unittest

from markdown_to_html_node_helper import text_to_textnodes

class test_text_to_textnodes(unittest.TestCase):
    def test_text_to_textnode_return(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        pass