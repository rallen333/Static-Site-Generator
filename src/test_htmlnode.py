import unittest
from htmlnode import *

from textnode import TextNode, TextType

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        props_dict = {"href": "https://www.google.com",  "target": "_blank",}
        a = HTMLNode()
        b = HTMLNode()
        node = HTMLNode("1", "2", [a, b], props_dict)
        node2 = HTMLNode("1", "2", [a, b], props_dict)
        self.assertEqual(node, node2)
    def test_uneq(self):
        node = HTMLNode(tag="a", value="b")
        node2 = HTMLNode(tag="a", value="c")
        self.assertNotEqual(node, node2)
    def test_none_values(self):
        node = HTMLNode(None, "b")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)
        self.assertIsNone(node.tag)
    def test_repr(self):
        node = HTMLNode("div", "content")
        expected = 'HTMLNode(tag=div, value=content, children=None, props=None)'
        self.assertEqual(repr(node), expected)

class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        leaf = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        leaf2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(leaf, leaf2)
    def test_uneq(self):
        leaf = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        leaf2 = LeafNode("p", "This is a paragraph of text.")
        self.assertNotEqual(leaf, leaf2)
    def test_no_value(self):
        leaf = LeafNode(None, None)
        self.assertRaises(ValueError)
    def test_to_html_no_children(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

class TestParentNode(unittest.TestCase):
    def test_eq(self):
        node = ParentNode(
    "p",
    [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
    ],
)
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")
    
    def test_no_children(self):
        node = ("p", [])
        self.assertRaises(ValueError)
    
    def test_nested_parents(self):
        node = ParentNode(
    "p",
    [
        ParentNode(
    "p",
    [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
    ],
)
    ],
)
        node2 = ParentNode(
    "p",
    [
        ParentNode(
    "p",
    [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
    ],
)
    ],
)
        self.assertEqual(node, node2)

    def test_headings(self):
            node = ParentNode(
                "h2",
                [
                    LeafNode("b", "Bold text"),
                    LeafNode(None, "Normal text"),
                    LeafNode("i", "italic text"),
                    LeafNode(None, "Normal text"),
                ],
            )
            self.assertEqual(
                node.to_html(),
                "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
            )