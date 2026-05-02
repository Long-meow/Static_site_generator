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
  
if __name__ == "__main__": 
  unittest.main()