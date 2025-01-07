import unittest

from markdown_to_html_node_helper import extract_title

class test_extract_title(unittest.TestCase):
    def test_extract_title(self):
        markdown = """# This is a title
        This is content


        >this is a quote


        * this is a ul list
        * list item


        
        """
        result = extract_title(markdown)
        expected = "This is a title"
        self.assertEqual(result, expected)



        