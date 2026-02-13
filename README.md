# Resume Tailoring Repository

An intelligent resume tailoring system that helps you create optimized, job-specific resumes from structured data.

## Features

- **Extract Resume Data**: Convert DOCX resumes into structured YAML and Markdown files
- **Analyze Job Descriptions**: Automatically extract keywords and requirements from job postings
- **Generate Tailored Resumes**: Create optimized resumes with keyword matching and length optimization
- **Multiple Versions**: Maintain different resume versions for different roles (e.g., Senior Engineer, Tech Lead)
- **Compare Versions**: Side-by-side comparison of different tailored resumes

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Extract Your Resume

Use the `extract-resume` Claude Code skill:

```
User: "Extract my resume"
Claude: (guides you through extraction process)
```

Or run manually:

```bash
python3 scripts/extract_resume.py \
  --input source/your-resume.docx \
  --output-base source/base-resume.yaml \
  --output-experiences data/experiences/
```

### 3. Analyze a Job Description

Use the `analyze-job` Claude Code skill:

```
User: "Analyze this job description [paste text]"
Claude: (analyzes keywords and creates tailoring config)
```

### 4. Generate Tailored Resume

Use the `tailor-resume` Claude Code skill:

```
User: "Generate tailored resume for [company]"
Claude: (generates optimized DOCX resume)
```

## Directory Structure

```
.
├── source/                      # Source resume and base data
│   ├── base-resume.yaml         # Structured resume data
│   └── your-resume.docx         # Original resume
│
├── data/                        # Organized resume content
│   ├── experiences/             # Work experience entries
│   ├── skills/                  # Skills by category
│   ├── projects/                # Notable projects
│   └── education/               # Education and certifications
│
├── jobs/                        # Job-specific configurations
│   └── company-role-YYYY-MM/    # Per-job directory
│       ├── job-description.md
│       ├── keywords.yaml
│       └── tailoring-config.yaml
│
├── output/                      # Generated resumes
│   └── company-role-YYYY-MM.docx
│
├── scripts/                     # Python automation
│   ├── extract_resume.py
│   ├── analyze_job.py
│   ├── tailor_resume.py
│   └── utils/
│
└── skills/                      # Claude Code skills
    ├── extract-resume/
    ├── analyze-job/
    ├── tailor-resume/
    └── compare-versions/
```

## Claude Code Skills

This repository includes four Claude Code skills for interactive resume management:

- **extract-resume**: Extract structured data from DOCX resume
- **analyze-job**: Analyze job description and extract keywords
- **tailor-resume**: Generate tailored resume for specific job
- **compare-versions**: Compare multiple resume versions side-by-side

## Data Schema

### Experience File Format

Each work experience is stored in `data/experiences/company-role.md`:

```markdown
---
company: "Acme Corporation"
position: "Senior Software Engineer"
location: "San Francisco, CA"
startDate: "2020-06-01"
endDate: "2023-12-31"
keywords: ["Python", "microservices", "AWS"]
relevant_for: ["senior-engineer", "tech-lead"]
priority: 1

versions:
  detailed: 5
  standard: 3
  concise: 2
---

## Summary
Brief summary of role and impact.

## Achievements

### 1. Achievement Title [priority:1, keywords:Python,AWS]
Description of achievement with quantified results.
```

### Tailoring Configuration

Each job application has a `tailoring-config.yaml`:

```yaml
job:
  company: "Example Company"
  position: "Senior Engineer"

resume:
  version: "senior-backend-engineer"
  length: "2-page"
  summary: "Custom summary for this role..."

keywords:
  required: ["Python", "AWS", "microservices"]
  preferred: ["Docker", "Kubernetes"]

selection:
  experiences:
    - slug: "acme-corp-senior-engineer"
      version: "detailed"
```

## Tailoring Features

1. **Multiple Resume Versions**: Create different professional personas (e.g., "senior-engineer", "tech-lead")
2. **Job Description Matching**: Automatic keyword extraction and match scoring (target: 85%+)
3. **Skill Filtering**: Prioritize and emphasize relevant skills based on job requirements
4. **Length Optimization**: Automatically fit content to 1-page or 2-page targets while preserving keywords

## License

MIT
