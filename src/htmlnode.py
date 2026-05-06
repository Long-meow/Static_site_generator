

class HTMLNode: 
  
  def __init__(self, tag = None, value = None, children = None, props = None):
    self.tag = tag 
    self.value = value 
    self.children = children 
    self.props = props 
    
  def to_html(self): 
    raise NotImplementedError()

  def props_to_html(self): 
    result_html_string = ""
    if self.props == None: 
      return result_html_string
    for prop_key, prop_value in self.props.items(): 
      if prop_value == None: 
        continue
      result_html_string += f"{prop_key}=\"{prop_value}\" "
    return result_html_string 

  def __repr__(self):
    return (f"tag: {self.tag}\n value: {self.value}\n children: {self.children}\n props: {self.props}")
  
class LeafNode(HTMLNode): 
  def __init__(self, tag=None, value=None, props=None):
    super().__init__(tag=tag, value=value, props=props)
  def to_html(self):
    if self.value == None: 
      raise ValueError("must have at least a value")
    if self.tag == None: 
      return self.value 
    return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>" if self.props != None else f"<{self.tag}>{self.value}</{self.tag}>"

  def __repr__(self):
    return (f"tag: {self.tag}\n value: {self.value}\n props: {self.props}")
  
class ParentNode(HTMLNode): 
  def __init__(self, tag=None, children=None, props=None):
    super().__init__(tag= tag, children= children, props= props)
    
  def to_html(self):
    if not self.tag: 
      raise ValueError("Not have a tag")  
    if self.children == None: 
      raise ValueError("Not including any child")
    result_html_string = ""
    for child in self.children: 
      result_html_string += child.to_html()
    return_string = f"<{self.tag}>{result_html_string}</{self.tag}>" if self.props == None else f"<{self.tag} {self.props_to_html()}>{result_html_string}</{self.tag}>"
    return return_string
  
  def __repr__(self):
    return f"tag: {self.tag}\nvalue: {self.value}\nchildren: {self.children}\nprops: {self.props}" 