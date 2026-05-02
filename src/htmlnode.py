

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
    for prop_key, prop_value in self.props.items(): 
      if prop_value == None: 
        continue
      result_html_string += f"{prop_key}=\"{prop_value}\" "
    return result_html_string 

  def __repr__(self):
    return (f"tag: {self.tag}\n value: {self.value}\n children: {self.children}\n props: {self.props}")
