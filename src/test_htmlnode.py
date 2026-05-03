import unittest 
from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase): 
  def test_to_html(self): 
    node = HTMLNode(props= {"meow": "hello meow", "class": "meow"})
    self.assertRaises(NotImplementedError, node.to_html)
    
  def test_props_to_html(self): 
    node = HTMLNode(props= {
    "href": "https://www.google.com",
    "target": "_blank",
    })
    self.assertEqual(node.props_to_html(), "href=\"https://www.google.com\" target=\"_blank\" ")
    
  def test_repr(self): 
    node = HTMLNode(props= {
    "href": "https://www.google.com",
    "target": "_blank",
    })
    self.assertEqual(repr(node),f"tag: None\n value: None\n children: None\n props: {node.props}")
    
class TestLeafNode(unittest.TestCase): 
  def test_to_html_without_value(self): 
    node = LeafNode(tag="p")
    self.assertRaises(ValueError, node.to_html)
    
  def test_to_html_without_tag(self): 
    node = LeafNode(value="hello meow meow") 
    self.assertEqual(node.to_html(), "hello meow meow")
    
  def test_to_html_full_node(self): 
    node = LeafNode("a", "Click me!", {"href": "https://www.google.com"}) 
    self.assertEqual(node.to_html(), '<a href="https://www.google.com" >Click me!</a>')
  
  def test_repr(self): 
    node = LeafNode("a", "Click me!", {"href": "https://www.google.com"}) 
    self.assertEqual(repr(node), f'tag: a\n value: Click me!\n props: {node.props}')
    