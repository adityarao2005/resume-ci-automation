# Repository Guidelines & Context

## Project Structure & Architecture
- **Resume Data**: [resume.yaml](file:///home/aditya/projects/resume-ci-automation/data/resume.yaml) contains the structured resume data (contact details, experience, education, skills, etc.).
- **LaTeX View / Template**: [resume_template.tex.j2](file:///home/aditya/projects/resume-ci-automation/templates/resume_template.tex.j2) is the Jinja2 LaTeX template used for rendering.
- **Output PDF**: `out/resume.pdf` is the generated resume PDF.

## Standard Commands & Workflow
- **Compile Resume PDF**: Run `docker compose up --build` to compile the YAML data and LaTeX template into `out/resume.pdf`.
- **Local Watch Mode**: Run `uv run python -m resume_ci_automation.watch_resume` to watch files and auto-regenerate on changes.
