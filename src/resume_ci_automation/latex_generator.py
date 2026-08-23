
import yaml
from jinja2 import Environment, FileSystemLoader


# Function to escape LaTeX special characters
def latex_escape(text):
    """Escape special LaTeX characters"""
    if not isinstance(text, str):
        return text
    replacements = {
        '\\': r'\textbackslash{}',
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        "<": r'\textless',
        ">": r'\textgreater',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'$\sim$',
        '^': r'\^{}',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def generate_latex_resume() -> str:
    # Load YAML data
    try:
        with open("data/resume.yaml", "r") as file:
            data = yaml.safe_load(file)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        exit(1)
    except FileNotFoundError:
        print("Error: data/resume.yaml not found")
        exit(1)

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

    # Add latex_escape filter
    env.filters['latex_escape'] = latex_escape

    template = env.get_template("resume_template.tex.j2")
    output = template.render(**data)
    return output