import unittest

from markdown_to_html_node_helper import markdown_to_html_node


class test_markdown_to_html_node(unittest.TestCase):
    def test_markdown_to_html_return(self):
        markdown = """## This is a heading

        This is a paragraph of text. It has some **bold** and *italic* words inside of it.

        ```some code block```

        >quote\n>quote2\n>quote3


        * list item\n* list item\n* list item

        1. ol item\n2. ol item\n3. ol item\n4. ol item
       
       """

        result = markdown_to_html_node(markdown)
        print(result)
