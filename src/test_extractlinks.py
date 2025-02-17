import unittest
from extract_links import *
from textnode import *


class TestExtractLinks(unittest.TestCase):

    def test_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_markdown_links(text), [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])
    def test_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text), [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])


class TestSplitNodes(unittest.TestCase):

    def test_multiple_images(self):
        # Create a node with multiple images in the text
        node = TextNode(
            "This is ![first](image1.png) and ![second](image2.png)",
            TextType.TEXT
        )
        
        # Call the function
        actual = split_nodes_image([node])
        
        # Create expected result
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("first", TextType.IMAGE, "image1.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("second", TextType.IMAGE, "image2.png")
        ]
        
        # Assert they're equal
        self.assertEqual(actual, expected)
    
    def test_multiple_links(self):
    # Input node
        node = TextNode(
            "Here is a [first link](https://first.com) and here is [another one](https://second.com)!",
            TextType.TEXT
        )
        
        # Expected result after splitting
        expected = [
            TextNode("Here is a ", TextType.TEXT),
            TextNode("first link", TextType.LINK, "https://first.com"),
            TextNode(" and here is ", TextType.TEXT),
            TextNode("another one", TextType.LINK, "https://second.com"),
            TextNode("!", TextType.TEXT)
        ]

        actual = split_nodes_link([node])
        self.assertEqual(actual, expected)

    def test_no_images(self):
    # Input node with plain text, no images
        node = TextNode(
            "This is just plain text without any images in it.",
            TextType.TEXT
        )
        
        # Expected result should be the same node, since there's nothing to split
        expected = [node]

        actual = split_nodes_image([node])
        self.assertEqual(actual, expected)