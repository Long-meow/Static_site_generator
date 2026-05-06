import unittest 

from textnode import TextNode, TextType 

class TestTextNode(unittest.TestCase): 
  def test_text_eq(self): 
    node1 = TextNode("This is a text node", TextType.BOLD)
    node2 = TextNode("This is a text node", TextType.BOLD)
    self.assertEqual(node1, node2) 
  
  def test_text_not_eq(self): 
    node1 = TextNode("this is node1", TextType.BOLD)
    node2 = TextNode("this is node2", TextType.BOLD)
    self.assertNotEqual(node1, node2)
    
  def test_type_not_eq(self): 
    node1 = TextNode("this is node", TextType.ITALIC)
    node2 = TextNode("this is node", TextType.BOLD)
    self.assertNotEqual(node1, node2)
  
  def test_url_not_eq(self): 
    node1 = TextNode("this is node", TextType.BOLD, "hello.com")
    node2 = TextNode("this is node", TextType.BOLD, "meow.com")
    self.assertNotEqual(node1, node2)
    
  def test_text_node_to_html_node_text(self): 
    text_node = TextNode("this is a meow", TextType.TEXT)
    html_node = text_node.text_node_to_html_node() 
    self.assertEqual((html_node.value, html_node.tag, html_node.props), ("this is a meow", None, None))
    
  def test_text_node_to_html_node_bold(self): 
    text_node = TextNode("this is a meow", TextType.BOLD)
    html_node = text_node.text_node_to_html_node() 
    self.assertEqual((html_node.value, html_node.tag, html_node.props), ("this is a meow", "b", None))
    
  def test_text_node_to_html_node_italic(self): 
    text_node = TextNode("this is a meow", TextType.ITALIC)
    html_node = text_node.text_node_to_html_node() 
    self.assertEqual((html_node.value, html_node.tag, html_node.props), ("this is a meow", "i", None))
    
  def test_text_node_to_html_node_code(self): 
    text_node = TextNode("this is a meow", TextType.CODE)
    html_node = text_node.text_node_to_html_node() 
    self.assertEqual((html_node.value, html_node.tag, html_node.props), ("this is a meow", "code", None))
    
  def test_text_node_to_html_node_link(self): 
    text_node = TextNode("this is a meow", TextType.LINK, url="hello kitty")
    html_node = text_node.text_node_to_html_node() 
    self.assertEqual((html_node.value, html_node.tag, html_node.props), ("this is a meow", "a", {"href": "hello kitty"}))
    
  def test_text_node_to_html_node_image(self): 
    text_node = TextNode("this is a meow", TextType.IMAGE, url="hello kitty")
    html_node = text_node.text_node_to_html_node() 
    self.assertEqual((html_node.value, html_node.tag, html_node.props), ("this is a meow", "img", {
      "src": "hello kitty",
      "alt": "this is a meow"
    }))
    
  
if __name__ == "__main__": 
  unittest.main()