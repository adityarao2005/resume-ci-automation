---
name: resume-automation
description: Workflow and instructions for compiling the resume PDF, editing resume data in data/resume.yaml, and updating the LaTeX template in templates/resume_template.tex.j2.
---

# Resume Automation Skill

## Core Overview
This repository manages a resume as code. The resume content is separated from visual layout and formatting.

- **Data File**: [resume.yaml](file:///home/aditya/projects/resume-ci-automation/data/resume.yaml)
- **Template File**: [resume_template.tex.j2](file:///home/aditya/projects/resume-ci-automation/templates/resume_template.tex.j2)
- **Output PDF**: `out/resume.pdf`

## Key Operations

### 1. Compiling the Resume PDF
To compile the resume into a PDF, run:
```bash
docker compose up --build
```
This renders `data/resume.yaml` using `templates/resume_template.tex.j2` inside a Docker container and writes `out/resume.pdf`.

### 2. Updating Resume Content
Edit [data/resume.yaml](file:///home/aditya/projects/resume-ci-automation/data/resume.yaml) to modify entries for work experience, skills, education, projects, or contact info.

### 3. Modifying Layout or Formatting
Edit [templates/resume_template.tex.j2](file:///home/aditya/projects/resume-ci-automation/templates/resume_template.tex.j2) to modify LaTeX layout, margins, typography, or styling.

### 4. Local Watch Mode
For local development with auto-compilation on file changes:
```bash
uv run python -m resume_ci_automation.watch_resume
```
