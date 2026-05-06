from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
  list_new_node = []
  if text_type not in TextType: 
    raise Exception("invalid text type") 
  for node in old_nodes: 
    if node.text_type != TextType.TEXT: 
      list_new_node.append(node) 
    else: 
      node_strings_list = node.text.split(delimiter) 
      for i in range(0, len(node_strings_list), 2): 
        if node_strings_list[i] != "": 
          list_new_node.append(TextNode(node_strings_list[i], TextType.TEXT)) 
        if i + 1 < len(node_strings_list): 
          list_new_node.append(TextNode(node_strings_list[i+1], text_type))
          
  return list_new_node

def extract_markdown_images(text): 
  matches = re.findall(r"\!\[(.*?)\]\((.*?)\)", text)
  return matches

def extract_markdown_links(text): 
  matches = re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)
  return matches

def split_nodes_images(old_nodes): 
  new_node_list = []
  for node in old_nodes: 
    if node.text_type != TextType.TEXT: 
      new_node_list.append(node) 
      continue
    list_images_info = extract_markdown_images(node.text) 
    image_node_list = [] 
    for image_info in list_images_info: 
      image_node_list.append(TextNode(text_content=image_info[0], text_type=TextType.IMAGE, url=image_info[1])) 
    list_text_node_content = re.split(r"\!\[.*?\]\(.*?\)", node.text) 
    text_node_list = [TextNode(text_content=node_content) for node_content in list_text_node_content] 
    for i in range(0, len(image_node_list)): 
      if text_node_list[i].text != "":
        new_node_list.append(text_node_list[i]) 
      new_node_list.append(image_node_list[i]) 
    if text_node_list[-1].text != "":
      new_node_list.append(text_node_list[-1])
  
  return new_node_list

def split_nodes_links(old_nodes): 
  new_node_list = []
  for node in old_nodes: 
    if node.text_type != TextType.TEXT: 
      new_node_list.append(node) 
      continue
    list_links_info = extract_markdown_links(node.text) 
    image_node_list = [] 
    for image_info in list_links_info: 
      image_node_list.append(TextNode(text_content=image_info[0], text_type=TextType.LINK, url=image_info[1])) 
    list_text_node_content = re.split(r"(?<!\!)\[.*?\]\(.*?\)", node.text) 
    text_node_list = [TextNode(text_content=node_content) for node_content in list_text_node_content] 
    for i in range(0, len(image_node_list)): 
      if text_node_list[i].text != "": 
        new_node_list.append(text_node_list[i]) 
      new_node_list.append(image_node_list[i]) 
    if text_node_list[-1].text != "": 
      new_node_list.append(text_node_list[-1])
  
  return new_node_list

def text_to_nodes(text): 
  nodes = [TextNode(text_content=text)] 
  nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD) 
  nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC) 
  nodes = split_nodes_delimiter(nodes, "`", TextType.CODE) 
  nodes = split_nodes_links(nodes) 
  nodes = split_nodes_images(nodes) 
  return nodes
  

    
    

      
      
    
    
  
