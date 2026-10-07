---
name: resume-review
description: >-
  Use this skill to review and score the generated resume PDF (out/resume.pdf).
  Builds the latest PDF via the resume-automation workflow, then evaluates it
  against weighted criteria targeting SWE internship/co-op roles at major tech
  companies (Google, Amazon, Microsoft, Meta, Apple, IBM, etc.).
---

# Resume Review Skill

## Prerequisites

Before reviewing, you **must** build the latest resume PDF. Follow the
[resume-automation](../resume-automation/SKILL.md) skill to compile:

```bash
docker compose up --build
```

This produces [out/resume.pdf](file:///home/aditya/projects/resume-ci-automation/out/resume.pdf).

## Review Procedure

### 1. Open the Resume

Read the generated PDF at `out/resume.pdf`.

### 2. Target Profile

This resume targets **software engineering internship / co-op positions** at
major technology companies including but not limited to:

- Google, Amazon, Microsoft, Meta, Apple, IBM, Netflix, Salesforce, Oracle,
  Adobe, Uber, Stripe, Databricks, Palantir, etc.

Applicable roles include: Software Development Intern, Software Engineering
Intern, Full Stack Developer Intern, Full Stack Engineer Intern, Backend
Engineer Intern, DevOps Intern, and any SWE-adjacent co-op role.

### 3. Scoring Criteria

Evaluate the resume across four weighted categories. Be **harsh** where the
resume falls short but **recognize genuine achievements**. Think like a
recruiter at a top-tier tech company — would you advance this candidate?

| Category                   | Max Score | What to Assess |
| :------------------------- | --------: | :------------- |
| **Impact & Results**       |        40 | Quantified outcomes, measurable achievements, scope of contributions. Does the candidate demonstrate they shipped real impact? Vague claims with no metrics score low. |
| **Clarity & Conciseness**  |        20 | Bullet quality, action-verb usage, readability, formatting, whitespace balance, and overall scannability. A recruiter spends ~7 seconds on a first pass — does this resume survive? |
| **Technical Relevance**    |        20 | Alignment of skills, technologies, and projects with what top tech companies look for in SWE interns. Relevant tech stacks, system design awareness, and modern tooling. |
| **Leadership & Initiative** |        20 | Evidence of ownership, mentorship, open-source contributions, club/org leadership, hackathon wins, or going beyond the job description. |

### 4. Calibration Scale

Use this calibration to anchor your scores:

- **0 %** — Absolute reject. Resume is irrelevant, unreadable, or empty.
- **25 %** — Below average. Missing key sections, no metrics, poor formatting.
- **50 %** — Average. Meets baseline expectations but nothing stands out.
- **75 %** — Strong. Clear impact, good formatting, relevant tech, some leadership signals.
- **100 %** — Instant hire. Think world-class candidates (e.g., Andrej Karpathy
  or Yann LeCun applying for an intern role at OpenAI/Anthropic — undeniable
  domain mastery and accomplishments).

### 5. Output Format

Produce a structured review with:

1. **Per-category breakdown**: For each of the four categories, provide:
   - The score (e.g., `32 / 40`)
   - 2–4 bullet points of specific praise or critique with references to actual
     resume content
2. **Overall Score**: A single score **out of 10**, derived from the weighted
   category totals (sum the four category scores to get a percentage, then map
   to the 0–10 scale). Justify this score in 1–2 sentences.
3. **Top 3 Strengths**: What this resume does best.
4. **Top 3 Areas for Improvement**: Actionable, specific suggestions (not
   generic advice like "add more metrics" — point to *which* bullets need it).
5. **Recruiter Verdict**: A one-line gut-check: _"Would I advance this candidate
   to a phone screen?"_ — Yes / Borderline / No, with a brief rationale.

### 6. Review Context

- The resume source data lives in
  [data/resume.yaml](file:///home/aditya/projects/resume-ci-automation/data/resume.yaml).
- The LaTeX template is at
  [templates/resume_template.tex.j2](file:///home/aditya/projects/resume-ci-automation/templates/resume_template.tex.j2).
- When suggesting improvements, reference specific YAML keys or bullet text so
  the user can act on feedback immediately.
