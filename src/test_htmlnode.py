import unittest 
from htmlnode import HTMLNode

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
    
  