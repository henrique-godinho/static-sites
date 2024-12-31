import unittest


from main import markdown_to_blocks

class test_markdown_to_blocks(unittest.TestCase):
    def test_return(self):
        markdown_string = """# This is a heading

        This is a paragraph of text. It has some **bold** and *italic* words inside of it.

        * This is the first list item in a list block
        * This is a list item
        * This is another list item"""
        test_result = ['# This is a heading', 'This is a paragraph of text. It has some **bold** and *italic* words inside of it.', '* This is the first list item in a list block\n        * This is a list item\n        * This is another list item']
        result = markdown_to_blocks(markdown_string)
        self.assertEqual(test_result, result)
    
    def test_type(self):
        markdown_string = """# This is a heading

        This is a paragraph of text. It has some **bold** and *italic* words inside of it.

        * This is the first list item in a list block
        * This is a list item
        * This is another list item"""
        result = markdown_to_blocks(markdown_string)
        self.assertIsInstance(result, list)