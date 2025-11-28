import subprocess
import yaml
from jinja2 import Environment, FileSystemLoader
import os
import shutil

# Load YAML data
with open("data/resume.yaml", "r") as file:
    data = yaml.safe_load(file)

# Render template
env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("resume_template.tex.j2")
output = template.render(**data)

if __name__ == "__main__":

    with open("resume.tex", "w") as f:
        f.write(output)

    subprocess.run(["pdflatex", "resume.tex", "-o", "resume.pdf"])
    shutil.move("resume.pdf", "out/resume.pdf")
    