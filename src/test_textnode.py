import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)

    def test_url_eq(self):
        node = TextNode("This is an url node", TextType.LINKS, "https://www.google.com")
        node2 = TextNode("This is an url node", TextType.LINKS, "https://www.google.com")
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is text node", TextType.NORMAL_TEXT)
        node2 = TextNode("This is a text node", TextType.LINKS, "https://www.google.com")
        self.assertNotEqual(node, node2)
    
    def test_text_not_eq(self):
        node = TextNode("this is an image node", TextType.NORMAL_TEXT)
        node2 = TextNode("This is a link node", TextType.NORMAL_TEXT)
        self.assertNotEqual(node, node2)
    
    def test_type_not_eq(self):
        node = TextNode("This is a text node", TextType.NORMAL_TEXT)
        node2 = TextNode("This is a text node", TextType.IMAGES)
        self.assertNotEqual(node, node2)
    
    def test_url_not_eq(self):
        node = TextNode("This is an url node", TextType.LINKS, "https://google.com")
        node2 = TextNode("This is an url node", TextType.LINKS, "http://google.co.uk")
        self.assertNotEqual(node, node2)
    
    


if __name__ == "__main__":
    unittest.main()