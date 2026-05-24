# resume-ci-automation
A resume as code automation platform which leverages Python, docker, the power of Git, and GH Actions to version and generate resumes.

The goal of this project is to separate the config/data of your resume and the view/template/UI of your resume.

Want to run it locally? Modify the `data/resume.yaml` and `templates/resume_template.tex.j2` to your liking and just run and find the resume in `out/resume.pdf`:
```
docker compose up --build
```

If you want a standalone watcher loop while you iterate locally, run:
```
uv run python -m resume_ci_automation.watch_resume
```
It will generate the PDF once, then keep watching `data/resume.yaml` and `templates/resume_template.tex.j2`, regenerate after a short debounce, and exit cleanly with `q` or `Ctrl-C`.

Want to have it automated? Already built in, clone & push or fork the repository, modify the `data/resume.yaml` and `templates/resume_template.tex.j2` then push your commits to your repository on GH Actions and watch as GH Actions builds the resume for you in the build artifacts.