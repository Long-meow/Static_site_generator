import converter 
import unittest
from textnode import TextNode, TextType
from blocknode import block_to_block_type, BlockType, markdown_to_blocks, markdown_to_html

class TestConverter(unittest.TestCase): 
  def test_split_nodes_delimiter_invalid_text_type(self): 
    node1 = TextNode("this is **meow**", TextType.TEXT) 
    
    self.assertRaises(Exception, converter.split_nodes_delimiter, [node1], "**", "mow")
    
  def test_split_nodes_delimiter_bold(self): 
    node1 = TextNode("this is **meow**", TextType.TEXT) 
    new_list = converter.split_nodes_delimiter([node1], "**", TextType.BOLD) 
    self.assertEqual(new_list, [
      TextNode("this is ", TextType.TEXT),
      TextNode("meow", TextType.BOLD),
    ])
    
  def test_split_nodes_delimiter_code_multiple_items(self): 
    node1 = TextNode("this is **meow**", TextType.TEXT) 
    node2 = TextNode("this is `code meow` meow", TextType.TEXT)
    new_list = converter.split_nodes_delimiter([node1, node2], "`", TextType.CODE) 
    self.assertEqual(new_list, [
      TextNode("this is **meow**", TextType.TEXT),
      TextNode("this is ", TextType.TEXT), 
      TextNode("code meow", TextType.CODE), 
      TextNode(" meow", TextType.TEXT) 
    ])
    
  def test_extract_markdown_images(self):
    matches = converter.extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
    self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
  def test_extract_markdown_links(self):
    matches = converter.extract_markdown_links(
        "This is text with an [image](https://i.imgur.com/zjjcJKZ.png)"
    )
    self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
  def test_extract_multiple_markdown_images(self):
    matches = converter.extract_markdown_images(
        "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    )
    self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)
    
  def test_extract_multiple_markdown_links(self):
    matches = converter.extract_markdown_links(
        "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    )
    self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)
    
  def test_split_images(self): 
    node1 = TextNode(text_content="This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)")
    old_nodes = [node1] 
    new_list = converter.split_nodes_images(old_nodes) 
    self.assertListEqual(new_list,[
      TextNode("This is text with an "),
      TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
      TextNode(" and another "),
      TextNode(
          "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
      ),
    ])
    
  def test_split_links(self): 
    node1 = TextNode(text_content="This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)")
    old_nodes = [node1] 
    new_list = converter.split_nodes_links(old_nodes) 
    self.assertListEqual(new_list,[
      TextNode("This is text with an "),
      TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
      TextNode(" and another "),
      TextNode(
          "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
      ),
    ])
    
  def test_text_to_nodes(self): 
    test_text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    nodes = converter.text_to_nodes(test_text) 
    self.assertListEqual(nodes, [
      TextNode("This is ", TextType.TEXT),
      TextNode("text", TextType.BOLD),
      TextNode(" with an ", TextType.TEXT),
      TextNode("italic", TextType.ITALIC),
      TextNode(" word and a ", TextType.TEXT),
      TextNode("code block", TextType.CODE),
      TextNode(" and an ", TextType.TEXT),
      TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
      TextNode(" and a ", TextType.TEXT),
      TextNode("link", TextType.LINK, "https://boot.dev"),
    ])
    
  def test_markdown_to_blocks(self):
    md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
    blocks = markdown_to_blocks(md)
    self.assertEqual(
        blocks,
        [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ],
    )
    
  def test_block_to_block_type_heading(self): 
    text_block = "#### MEOW MEOW" 
    block_type = block_to_block_type(text_block)
    self.assertEqual(block_type, BlockType.HEADING)
    
  def test_block_to_block_type_code(self): 
    text_block1 = "```mewo meow mmeoweowmemow ```" 
    text_block2 = """```
    meow meow meow 
    ```"""
    
    block_type = block_to_block_type(text_block1)
    self.assertEqual(block_type, BlockType.CODE)
    block_type = block_to_block_type(text_block2)
    self.assertEqual(block_type, BlockType.CODE)
    
  def test_block_to_block_type_quote(self): 
    text_block = """> hello meow meow\n> meow meow meow\n> meow ys meow"""
    block_type = block_to_block_type(text_block)
    self.assertEqual(block_type, BlockType.QUOTE)
    
  def test_block_to_block_type_unordered_list(self): 
    text_block = """- hello meow meow\n- meow meow meow\n- meow ys meow"""
    block_type = block_to_block_type(text_block)
    self.assertEqual(block_type, BlockType.UNORDERED_LIST)
    
  def test_block_to_block_type_ordered_list(self): 
    text_block = """1. hello meow meow\n2. meow meow meow\n3. meow ys meow"""
    invalid_text_block = "01. hello meow meow\n2. meow meow meow\n2. meow ys meow"
    block_type = block_to_block_type(text_block)
    self.assertEqual(block_type, BlockType.ORDERED_LIST)
    block_type = block_to_block_type(invalid_text_block) 
    self.assertNotEqual(block_type, BlockType.ORDERED_LIST)
    
  def test_paragraphs(self):
    md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

    html = markdown_to_html(md)
    self.assertEqual(
        html,
        "<div><p>This is <b>bolded</b> paragraph\ntext in a p\ntag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )

  def test_codeblock(self):
      md = """```This is text that _should_ remain the **same** even with inline stuff```"""

      html = markdown_to_html(md)
      self.assertEqual(
          html,
          "<div><code>This is text that <i>should</i> remain the <b>same</b> even with inline stuff</code></div>",
      )