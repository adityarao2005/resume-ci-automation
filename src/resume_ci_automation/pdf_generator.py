import subprocess
import os
import shutil
from pathlib import Path
from latex_generator import generate_latex_resume

def generate_pdf():
    output = generate_latex_resume()
    
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
