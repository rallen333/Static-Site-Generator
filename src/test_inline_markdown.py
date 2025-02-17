import unittest
from textnode import (
    split_nodes_delimiter,
)

from textnode import TextNode, TextType
from  markdown_to_blocks import *
from main import *

class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        # Test basic blocks
        markdown1 = "# Heading\n\nParagraph text"
        assert markdown_to_blocks(markdown1) == ["# Heading", "Paragraph text"]

        # Test with multiple newlines
        markdown2 = "Block1\n\n\n\nBlock2"
        assert markdown_to_blocks(markdown2) == ["Block1", "Block2"]

        # Test with list items
        markdown3 = "# Header\n\n* List item 1\n* List item 2"
        assert markdown_to_blocks(markdown3) == ["# Header", "* List item 1\n* List item 2"]

        # Test with whitespace
        markdown4 = "   Spaces before\n\nSpaces after   "
        assert markdown_to_blocks(markdown4) == ["Spaces before", "Spaces after"]

        # Test empty document
        markdown5 = ""
        assert markdown_to_blocks(markdown5) == []


class TestBlocktoBlockType(unittest.TestCase):
    
    def test_heading(self):
        block = "# "
        block2 = "### Heading"
        self.assertEqual(block_to_block_type(block), "paragraph")
        self.assertEqual(block_to_block_type(block2), "heading")

    def test_code(self):
        block = "``invalid code``"
        block2 = "```valid code```"
        self.assertEqual(block_to_block_type(block), "paragraph")
        self.assertEqual(block_to_block_type(block2), "code")
    

    def test_unordered_list(self):
        block = "* First item\nSecond item"
        block2 = "* First item\n- Second item"
        self.assertEqual(block_to_block_type(block), "paragraph")
        self.assertEqual(block_to_block_type(block2), "unordered_list")


    def test_ordered_list(self):
        block = "1. First\n3. Third"
        block2 = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(block), "paragraph")
        self.assertEqual(block_to_block_type(block2), "ordered_list")

    def test_quote(self):
        block = ">First line\nSecond line"
        block2 = ">First line\n>Second line"
        self.assertEqual(block_to_block_type(block), "paragraph")
        self.assertEqual(block_to_block_type(block2), "quote")



class TestMarkdownToHTMLNode(unittest.TestCase):

    def test_heading_conversion(self):
        markdown = "# Heading 1"
        result = markdown_to_html_node(markdown)

        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 1)
        child = result.children[0]
        self.assertEqual(child.tag, "h1")   
        self.assertEqual(child.value, "Heading 1")

    def test_paragraph_conversion(self):
        markdown = "This is a paragraph."
        result = markdown_to_html_node(markdown)

        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 1)
        child = result.children[0]
        self.assertEqual(child.tag, "p")
        self.assertEqual(child.value, "")
        self.assertEqual(len(child.children), 1)
        self.assertEqual(child.children[0].text, "This is a paragraph.")

    def test_unordered_list_conversion(self):
        markdown = "- Item 1\n- Item 2\n- Item 3"
        result = markdown_to_html_node(markdown)

        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 1)
        ul = result.children[0]
        self.assertEqual(ul.tag, "ul")
        self.assertEqual(len(ul.children), 3)
        self.assertEqual(ul.children[0].value, "Item 1")
        self.assertEqual(ul.children[2].value, "Item 3")

    def test_ordered_list_conversion(self):
        markdown = "1. First\n2. Second\n3. Third"
        result = markdown_to_html_node(markdown)

        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 1)
        ol = result.children[0]
        self.assertEqual(ol.tag, "ol")
        self.assertEqual(len(ol.children), 3)
        self.assertEqual(ol.children[0].value, "First")
        self.assertEqual(ol.children[1].value, "Second")
        self.assertEqual(ol.children[2].value, "Third")


class TestExtractTitle(unittest.TestCase):
    def test_heading(self):
        markdown = "# Heading 1"
        markdown2 = "# Header\n\n* List item 1\n* List item 2"
        markdown3 = "## Heading 1"  
        self.assertEqual(extract_title(markdown), "Heading 1")
        self.assertEqual(extract_title(markdown2), "Header")
        

if __name__ == "__main__":
    unittest.main()
