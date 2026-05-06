from textnode import TextNode, TextType
from blocknode import markdown_to_html
import os, shutil
from pathlib import Path

def main(): 
  if os.path.exists("public"): 
    shutil.rmtree("public") 
  shutil.copytree("static", "public")
  base_content_dir = Path("content")
  for file_path in base_content_dir.rglob("index.md"):
    generate_page(file_path, "template.html", Path(str(file_path).replace("content", "public").replace(".md", ".html")))
  
def extract_title(markdown): 
  lines = markdown.split("\n") 
  for line in lines: 
    if line[:2] == "# ": 
      return line[2:].strip()
    
def generate_page(from_path, template_path, dest_path): 
  print(f"Generating page from {from_path} to {dest_path} using {template_path}")
  with open(from_path, 'r') as file: 
    content = file.read() 
  html_content = markdown_to_html(content) 
  title = extract_title(content) 
  with open(template_path, 'r') as file: 
    template_content = file.read() 
  full_template_content = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content) 
  dest_path.parent.mkdir(parents=True, exist_ok=True)
  dest_path.write_text(full_template_content)
  
if __name__ == "__main__": 
  main()

