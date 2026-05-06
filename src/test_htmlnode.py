import unittest 
from htmlnode import HTMLNode, LeafNode, ParentNode

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
    node = LeafNode("a", "Click me!", props={"href": "https://www.google.com"})
    self.assertEqual(node.to_html(), '<a href="https://www.google.com" >Click me!</a>')
  
  def test_repr(self): 
    node = LeafNode("a", "Click me!", {"href": "https://www.google.com"}) 
    self.assertEqual(repr(node), f'tag: a\n value: Click me!\n props: {node.props}')
    
class TestParentNode(unittest.TestCase): 
  def test_to_html_without_tag(self): 
    node = ParentNode(tag = None, children=None)
    self.assertRaises(ValueError, node.to_html)
  
  def test_to_html_without_child(self): 
    node = ParentNode(tag="p", children=None)
    self.assertRaises(ValueError, node.to_html)
  
  def test_to_html_with_children(self):
    child_node = LeafNode("span", "child")
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

  def test_to_html_with_grandchildren(self):
      grandchild_node = LeafNode("b", "grandchild")
      child_node = ParentNode("span", [grandchild_node])
      parent_node = ParentNode("div", [child_node])
      self.assertEqual(
          parent_node.to_html(),
          "<div><span><b>grandchild</b></span></div>",
      )
      
  def test_to_html_with_multiple_children(self):
    grandchild_node1 = LeafNode("b", "grandchild1")
    child_node2 = ParentNode("span", [])
    grandchild_node2 = LeafNode("i", "grandchild2")
    child_node1 = ParentNode("span", [grandchild_node1, grandchild_node2])
    parent_node = ParentNode("p", [child_node1, child_node2])
    self.assertEqual(
      parent_node.to_html(), 
      "<p><span><b>grandchild1</b><i>grandchild2</i></span><span></span></p>"
    )