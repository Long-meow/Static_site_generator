from enum import Enum 
from htmlnode import ParentNode, LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode: 
  
  def __init__(self, text_content, text_type, url = None, alt_text = None):
    self.text = text_content
    self.text_type = text_type 
    self.url = url
    self.alt_text = alt_text

  def __eq__(self, other_text_node):
    return (self.text == other_text_node.text and
            self.text_type == other_text_node.text_type and
            self.url == other_text_node.url)
    
  def text_node_to_html_node(self): 
    if self.text_type not in TextType: 
      raise Exception("Not have this text type") 
    
    match self.text_type: 
      case TextType.TEXT: 
        return LeafNode(value=self.text)
      case TextType.BOLD: 
        return LeafNode(tag="b", value=self.text)
      case TextType.ITALIC: 
        return LeafNode(tag="i", value=self.text)
      case TextType.CODE: 
        return LeafNode(tag="code", value=self.text) 
      case TextType.LINK: 
        return LeafNode(tag="a", value=self.text, props={"href": self.url})
      case TextType.IMAGE: 
        return LeafNode(tag="img", value=self.text, props={
          "src": self.url,
          "alt": self.alt_text
        })
      
  def __repr__(self):
    return f"TextNode({self.text}, {self.text_type.value}, {self.url})"