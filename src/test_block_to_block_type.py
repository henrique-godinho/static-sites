import unittest

from main import block_to_block_type

class test_block_to_block_type(unittest.TestCase):
    def test_return_value_block(self):
        block = "# this is a heading"
        block2 = "## this is a heading"
        block3 = "### this is a heading"
        block4 = "#### this is a heading"
        block5 = "##### this is a headgin"
        block6 = "###### this is a heading"
        block7 = "####### this is NOT a heading"

        result = block_to_block_type(block)
        result2 = block_to_block_type(block2)
        result3 = block_to_block_type(block3)
        result4 = block_to_block_type(block4)
        result5 = block_to_block_type(block5)
        result6 = block_to_block_type(block6)
        result7 = block_to_block_type(block7)

        expected = "heading"
        self.assertEqual(result, expected)
        self.assertEqual(result2, expected)
        self.assertEqual(result3, expected)
        self.assertEqual(result4, expected)
        self.assertEqual(result5, expected)
        self.assertEqual(result6, expected)
        self.assertNotEqual(result7, expected)
    
    def test_return_value_code(self):
        block = "```This is a code block```"
        result = block_to_block_type(block)
        expected = "code"
        self.assertEqual(result, expected)

        block2 = "```This is is missing closing ticks"
        result2 = block_to_block_type(block2)
        self.assertNotEqual(result2, expected)
    
    def test_return_value_quote(self):
        block = ">quote1\n>quote2\n>quote3"
        result = block_to_block_type(block)
        expected = "quote"

        self.assertEqual(result, expected)

        block2 = "quote\n>quote2\n>quote3"
        result2 = block_to_block_type(block2)
        self.assertNotEqual(result2, expected)

    def test_return_value_ul(self):
        expected = "ul"
        block = "* item\n* item\n* item"
        result = block_to_block_type(block)
        self.assertEqual(result, expected)

        block2 = "- item\n- item\n- item\n- item"
        result2 = block_to_block_type(block2)
        self.assertEqual(result2, expected)

        block3 = "* item\n* item\n*item"
        result3 = block_to_block_type(block3)
        self.assertNotEqual(result3, expected)

        block4 = "- item\n-item\n- item\n- item"
        result4 = block_to_block_type(block4)
        self.assertNotEqual(result4, expected)

    def test_return_value_ol(self):
        expected = "ol"
        block = "1. item\n2. item\n3. item"
        result = block_to_block_type(block)
        self.assertEqual(result, expected)

        block2 = "1.item\n2.item\n3.item"
        result2 = block_to_block_type(block2)
        self.assertNotEqual(result2, expected)

    def test_return_value_p(self):
        expected = "paragraph"
        block = "Hello, is it me you're looking for?"
        result = block_to_block_type(block)
        self.assertEqual(result, expected)

        block2 = "-milk\n-bread"
        result2 = block_to_block_type(block2)
        self.assertEqual(result2, expected)

        block3 = "1.item\n2.item\n3.item"
        result3 = block_to_block_type(block3)
        self.assertEqual(result3, expected)
        
