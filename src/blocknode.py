from enum import Enum
from converter import text_to_nodes
from htmlnode import ParentNode

class BlockType(Enum): 
  PARAGRAPH = "paragraph"
  HEADING = "heading"
  CODE = "code"
  QUOTE = "quote"
  ORDERED_LIST = "ordered_list" 
  UNORDERED_LIST = "unordered_list"

def block_to_block_type(text_block): 
  count_sign = 0
  while count_sign < len(text_block) and text_block[count_sign] == '#': 
    count_sign += 1
  if count_sign < len(text_block) and text_block[count_sign] == ' ' and count_sign > 0 and count_sign < 7:
    return BlockType.HEADING 
  if text_block[:3] == "```" and text_block[-3:] == "```": 
    return BlockType.CODE
  lines = text_block.split("\n") 
  starter = lines[0][:2] 
  checker = True 
  for line in lines: 
    if line[:2] != starter: 
      checker = False 
  if starter == "> " and checker: 
    return BlockType.QUOTE  
  if starter == "- " and checker: 
    return BlockType.UNORDERED_LIST
  numbers = "0123456789" 
  for i in range(0, len(lines)):
    num = ""
    index = 0
    while index < len(lines[i]) - 2 and lines[i][index] in numbers: 
      num += lines[i][index] 
      index += 1
    if not num.isdigit(): 
      checker = False 
      break
    if lines[i][index] == '.' and lines[i][index + 1] == ' ' and int(num) == i + 1: 
      checker = True 
    else: 
      checker = False 
      break
    
  if not checker: 
    return BlockType.PARAGRAPH 
  else: 
    return BlockType.ORDERED_LIST 
  
class BlockNode: 
  def __init__(self, text_content_block): 
    self.block_type = block_to_block_type(text_content_block) 
    self.text = text_content_block 
  
  def block_node_to_html_node(self): 
    
    if self.block_type == BlockType.PARAGRAPH: 
      nodes = text_to_nodes(self.text)
      html_nodes = [node.text_node_to_html_node() for node in nodes]
      return ParentNode(tag="p", children=html_nodes)
    if self.block_type == BlockType.HEADING: 
      count_sign = 0
      while count_sign < len(self.text) - 2 and self.text[count_sign] == '#': 
        count_sign += 1
      nodes = text_to_nodes(self.text[count_sign + 1:])
      html_nodes = [node.text_node_to_html_node() for node in nodes]
      return ParentNode(tag=f"h{count_sign}", children=html_nodes)
    if self.block_type == BlockType.CODE: 
      nodes = text_to_nodes(self.text[3:-3])
      html_nodes = [node.text_node_to_html_node() for node in nodes]
      return ParentNode(tag="code", children=html_nodes)
    if self.block_type == BlockType.QUOTE: 
      lines = self.text.split("\n")
      list_nodes = []
      for line in lines: 
        list_text_nodes = text_to_nodes(line[2:])
        lists_html_nodes = [node.text_node_to_html_node() for node in list_text_nodes]
        list_nodes.append(ParentNode(tag="blockquote", children=lists_html_nodes))
      return ParentNode(tag="div", children=list_nodes) 
    if self.block_type == BlockType.UNORDERED_LIST: 
      lines = self.text.split("\n") 
      list_nodes = []
      for line in lines: 
        list_text_nodes = text_to_nodes(line[2:])
        lists_html_nodes = [node.text_node_to_html_node() for node in list_text_nodes]
        list_nodes.append(ParentNode(tag="li", children=lists_html_nodes))
      return ParentNode(tag="ul", children=list_nodes) 
    if self.block_type == BlockType.ORDERED_LIST: 
      lines = self.text.split("\n") 
      list_nodes = []
      for i in range(0, len(lines)):
        list_text_nodes = text_to_nodes(lines[i][len(str(i)) + 2:])
        lists_html_nodes = [node.text_node_to_html_node() for node in list_text_nodes]
        list_nodes.append(ParentNode(tag="li", children=lists_html_nodes))
      return ParentNode(tag="ol", children=list_nodes)     
    
    
def markdown_to_blocks(markdown_document): 
  blocks = [item.strip() for item in markdown_document.split("\n\n")]
  new_blocks = [] 
  for block in blocks: 
    if block != "": 
      new_blocks.append(block)
  return new_blocks

def markdown_to_html(markdown_document): 
  blocks = markdown_to_blocks(markdown_document) 
  list_block_node = []
  list_block_html_node = []
  for block in blocks: 
    list_block_node.append(BlockNode(block))
  for block_node in list_block_node: 
    list_block_html_node.append(block_node.block_node_to_html_node()) 
  html_string = "" 
  for html_block_node in list_block_html_node: 
    html_string += html_block_node.to_html() 
  return f"<div>{html_string}</div>"
    

    
      