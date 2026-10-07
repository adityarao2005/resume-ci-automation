---
name: resume-review
description: >-
  Use this skill to review and score the generated resume PDF (out/resume.pdf).
  Builds the latest PDF via the resume-automation workflow, then performs a dual-track
  evaluation: an ATS Parsability Audit (machine extraction, icon glyphs, keywords) and
  a Recruiter Visual & Interactive Review (browser/PDF viewer scannability, clickable
  links, weighted impact criteria) targeting top-tier SWE internship/co-op roles.
---

# Resume Review Skill

## Prerequisites

Before reviewing, you **must** build the latest resume PDF. Follow the
[resume-automation](../resume-automation/SKILL.md) skill to compile:

```bash
docker compose up --build
```

This produces [out/resume.pdf](file:///home/aditya/projects/resume-ci-automation/out/resume.pdf).

## Review Methodology

Top tech companies (Google, Amazon, Meta, Microsoft, Apple, IBM, Bloomberg, Uber, etc.) evaluate resumes through a two-stage pipeline:
1. **The Machine Gate (ATS)**: Automated ingestion, text extraction, tokenization, and keyword matching.
2. **The Human Gate (Recruiter / Hiring Manager)**: A quick 6–10 second visual scan in a browser PDF viewer or desktop reader, followed by clicking portfolio/GitHub links and checking engineering depth.

A complete review must evaluate **both** dimensions.

---

## Review Procedure

### Step 1: Text Extraction & ATS Ingestion Check

Extract the raw text from `out/resume.pdf` using `pdftotext` to simulate what an ATS parser ingests:

```bash
pdftotext out/resume.pdf -
```

Check for:
- **Font & Icon Corruption**: Do FontAwesome / LaTeX icons decode as strange symbols (e.g. `ƒ`, `ï`, `§`, `€`) that corrupt contact info or project titles?
- **Text Flow & Parsing**: Are columns, dates, titles, and institutions properly grouped, or do lines interleave?
- **Contact Extraction**: Can a parser cleanly extract name, email, phone number, LinkedIn, GitHub, and portfolio URL?
- **Standard Section Headings**: Are headings recognizable standard ATS sections (Education, Experience, Projects, Technical Skills)?
- **Keyword Density**: Are core SWE keywords indexed (e.g., specific languages, distributed systems, containerization, cloud, testing, CI/CD)?

### Step 2: Recruiter Visual & Interactive Review

Simulate opening the PDF in a web browser (Chrome/Edge/Firefox PDF viewer) or standard PDF reader.

Assess:
- **First 7-Second Scan**: Does the visual hierarchy immediately draw the eye to the strongest achievements (top companies, high GPA, stand-out metrics)?
- **Whitespace & Density**: Is the layout balanced? Does it cleanly fill exactly one page without underfilling or spilling onto page 2?
- **Clickable Links & Interactivity**:
  - Verify every hyperlink configured in [resume.yaml](file:///home/aditya/projects/resume-ci-automation/data/resume.yaml) and rendered via [resume_template.tex.j2](file:///home/aditya/projects/resume-ci-automation/templates/resume_template.tex.j2):
    - Email (`mailto:`)
    - LinkedIn (`https://linkedin.com/...`)
    - GitHub profile (`https://github.com/...`)
    - Personal website / portfolio
    - Project repository links (GitHub icons / URLs)
    - Company / startup links
  - Verify that links are valid, click targets are well-positioned, and URLs are properly prefixed (e.g., `https://`).
- **Typography & Polish**: Consistent margins, clean bullet alignment, appropriate font scaling.

### Step 3: Content Scoring (Weighted Criteria)

Evaluate the resume content targeting **Software Engineering Internship / Co-op** roles across four weighted categories:

| Category | Max Score | Assessment Criteria |
| :--- | :---: | :--- |
| **Impact & Results** | 40 | Quantified outcomes, measurable metrics (latency, throughput, users, hours saved), scope of shipped systems. Vague bullets score low. |
| **Clarity & Conciseness** | 20 | Action-verb quality, strong bullet structure (Action + Context + Impact), readability, scannability under rapid recruiter review. |
| **Technical Relevance** | 20 | Alignment with modern SWE expectations at major tech companies (systems programming, cloud-native tech, modern stacks, testing, CI/CD). |
| **Leadership & Initiative** | 20 | Open-source contributions, student leadership, TA/mentorship, independent engineering initiatives, ownership beyond routine tasks. |

#### Calibration Scale
- **0–49% (Reject)**: Unreadable, missing key sections, no metrics, broken formatting.
- **50–69% (Average)**: Meets baseline requirements, but generic; unlikely to stand out in high-volume applicant pools.
- **70–84% (Strong)**: Clear impact, verified links, relevant modern tech, solid leadership signals; competitive for top tech screens.
- **85–100% (Exceptional / Instant Screen)**: World-class achievements, undeniable engineering depth, top-tier quantification, flawless presentation.

---

## Output Format

When executing `/resume-review`, provide the report structured as follows:

### 1. ATS Parsability Audit
- **Extraction Fidelity**: Pass / Warning / Fail (note any icon artifacts, encoding glitches, or corrupted contact strings).
- **Section & Contact Extraction**: Assessment of how cleanly ATS parsers extract name, contact details, education, and job history.
- **Keyword & Searchability Index**: Key technical tokens detected vs. expected for targeted SWE roles.

### 2. Recruiter Visual & Interactive Review
- **Visual Presentation & Scannability**: First-glance impression, layout balance, whitespace, one-page constraint.
- **Interactive Links Check**:
  - List of all interactive links found (Email, LinkedIn, GitHub, Portfolio, Projects).
  - Status of each link (format, target URL, clickability).

### 3. Content Scoring Breakdown
- **Impact & Results**: Score (`X / 40`) with 2–4 detailed points of praise/critique.
- **Clarity & Conciseness**: Score (`X / 20`) with 2–4 detailed points.
- **Technical Relevance**: Score (`X / 20`) with 2–4 detailed points.
- **Leadership & Initiative**: Score (`X / 20`) with 2–4 detailed points.

### 4. Overall Score & Verdict
- **Overall Score**: `X.X / 10` (mapped from total percentage) with a 1–2 sentence justification.
- **Recruiter Verdict**: **Yes / Borderline / No** with a clear rationale.
- **Top 3 Strengths**: Core competitive advantages of the resume.
- **Top 3 Actionable Fixes**: Exact, high-impact edits with file and line references to [data/resume.yaml](file:///home/aditya/projects/resume-ci-automation/data/resume.yaml) or [templates/resume_template.tex.j2](file:///home/aditya/projects/resume-ci-automation/templates/resume_template.tex.j2).
