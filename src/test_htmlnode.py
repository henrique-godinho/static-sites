import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_type(self):
        dict = {"href": "www.google.com", "target":"_blank"}
        node = HTMLNode(props=dict)
        attributes = node.props_to_html()
        test_type = "string"
        self.assertEqual(type(attributes), type(test_type))
    
    def test_none_type(self):
        node = HTMLNode()
        self.assertEqual(node.tag, node.children)
        self.assertEqual(node.value, node.props)
    
    def test_repr(self):
        node = HTMLNode("<a>", "link", "<img>")
        repr = node.__repr__()
        self.assertIsNotNone(repr)
    
    def test_leaf_eq(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        node2 = LeafNode("p", "This is a paragraph of text.")
        self.assertNotEqual(node, node2)
    
    def test_leaf_none_value(self):
        node = LeafNode("a")
        self.assertRaises(ValueError, node.to_html)
    
    def test_parent_tag_raise(self):
        node = ParentNode("", "")
        self.assertRaises(ValueError, node.to_html)
    