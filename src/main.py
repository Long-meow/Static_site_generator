from textnode import TextNode, TextType
from blocknode import markdown_to_html
import os, shutil
from pathlib import Path
import sys 

def main(): 
  basepath = sys.argv[1] if len(sys.argv) > 0 else "/"
  if os.path.exists("docs"): 
    shutil.rmtree("docs") 
  shutil.copytree("static", "docs")
  base_content_dir = Path("content")
  for file_path in base_content_dir.rglob("index.md"):
    generate_page(file_path, "template.html", Path(str(file_path).replace("content", "docs").replace(".md", ".html")), basepath)
  
def extract_title(markdown): 
  lines = markdown.split("\n") 
  for line in lines: 
    if line[:2] == "# ": 
      return line[2:].strip()
    
def generate_page(from_path, template_path, dest_path, basepath): 
  print(f"Generating page from {from_path} to {dest_path} using {template_path}")
  with open(from_path, 'r') as file: 
    content = file.read() 
  html_content = markdown_to_html(content) 
  title = extract_title(content) 
  with open(template_path, 'r') as file: 
    template_content = file.read() 
  full_template_content = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
  full_template_content = full_template_content.replace("href=\"", f"href=\"{basepath}").replace("src=\"", f"src=\"{basepath}")
  dest_path.parent.mkdir(parents=True, exist_ok=True)
  dest_path.write_text(full_template_content)
  
if __name__ == "__main__": 
  main()

