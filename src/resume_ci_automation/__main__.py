import subprocess
import yaml
from jinja2 import Environment, FileSystemLoader
import os
import shutil
from pathlib import Path

# Load YAML data
with open("data/resume.yaml", "r") as file:
    data = yaml.safe_load(file)

# Render template with custom delimiters to avoid conflicts with LaTeX
env = Environment(
    loader=FileSystemLoader("templates"),
    block_start_string='<BLOCK>',
    block_end_string='</BLOCK>',
    variable_start_string='<VAR>',
    variable_end_string='</VAR>',
    comment_start_string='<#',
    comment_end_string='#>',
    trim_blocks=True,
    autoescape=False
)
template = env.get_template("resume_template.tex.j2")
output = template.render(**data)

if __name__ == "__main__":

    with open("resume.tex", "w") as f:
        f.write(output)

    # Run pdflatex
    result = subprocess.run(["pdflatex", "-interaction=nonstopmode", "resume.tex"], 
                          capture_output=True, text=True)
    
    if result.returncode != 0:
        print("LaTeX compilation failed:")
        print(result.stdout)
        print(result.stderr)
        exit(1)
    
    # Create output directory if it doesn't exist
    Path("out").mkdir(exist_ok=True)
    
    # Move the PDF to out/ directory
    if Path("resume.pdf").exists():
        shutil.copy2("resume.pdf", "out/resume.pdf")
        print(f"Resume generated: {os.path.abspath('out/resume.pdf')}")
    else:
        print("Error: resume.pdf was not created")
        exit(1)