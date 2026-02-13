# Resume Tailoring Repository - Claude Instructions

This is a resume tailoring system that helps create optimized, job-specific resumes.

## Available Skills

When the user wants to work with resumes, use these skills:

- **`extract-resume`**: Extract DOCX resume into structured markdown/YAML files
- **`analyze-job`**: Analyze job description and extract keywords
- **`tailor-resume`**: Generate tailored DOCX resume for specific job
- **`compare-versions`**: Compare multiple resume versions side-by-side
- **`explore-candidate`**: Audit resume freshness and identify stale content

## Workflow

### Initial Setup (One-time)
1. User invokes `extract-resume` skill
2. Extract source DOCX into structured data
3. Guide user to enhance experience files with keywords and priorities

### Per Job Application
1. User invokes `analyze-job` skill with job description
2. Create job directory and analyze keywords
3. Generate tailoring configuration
4. User customizes summary (important!)
5. User invokes `tailor-resume` skill
6. Generate optimized DOCX resume
7. Review match score and iterate if needed

## Directory Structure

```
source/          - Original resume and base data
data/            - Structured resume content (experiences, skills, etc.)
jobs/            - Job-specific configurations
output/          - Generated tailored resumes
scripts/         - Python automation scripts
skills/          - Claude Code skills
```

## Data Files

- **`source/base-resume.yaml`**: Core resume data (name, contact, education)
- **`data/experiences/*.md`**: Individual work experiences with metadata
- **`jobs/[company-role-date]/tailoring-config.yaml`**: Per-job customization
- **`jobs/[company-role-date]/keywords.yaml`**: Extracted keywords and analysis

## Key Features

1. **Multiple Resume Versions**: Support different professional personas
2. **Job Description Matching**: Automatic keyword extraction and scoring
3. **Skill Filtering**: Prioritize relevant skills per job
4. **Length Optimization**: Automatically fit 1-page or 2-page targets

## Python Dependencies

Install with: `pip install -r requirements.txt`

Required packages:
- python-docx: DOCX file manipulation
- PyYAML: YAML parsing
- python-frontmatter: Markdown frontmatter parsing

## Best Practices

### For Experience Files
- Add specific keywords for each role (technologies, skills, domains)
- Set priority levels (1 = most important)
- Tag with `relevant_for` to indicate which resume versions
- Define versions: detailed (5 bullets), standard (3), concise (2)
- Quantify achievements with numbers when possible

### For Job Analysis
- Always customize the summary in `tailoring-config.yaml`
- Review and adjust experience selection
- Target match score: 85%+ is excellent, 70-85% is good
- Don't keyword stuff - maintain natural language

### For Resume Generation
- Review generated DOCX before submitting
- Iterate on configuration if match score is low
- Check that critical keywords appear naturally
- Verify page count meets expectations (within 0.2 pages)

## Troubleshooting

**Low match score (<70%)**:
- Add more relevant experiences
- Emphasize specific keywords in bullets
- Customize summary to include key terms

**Resume too long**:
- Use concise versions of experiences
- Reduce bullet count per experience
- Limit number of experiences included

**Missing keywords**:
- Check if keywords exist in experience files
- Consider if truly relevant (don't add irrelevant keywords)
- Use suggestions from keyword analysis

## File Naming Conventions

- Experience files: `company-role-slug.md` (lowercase, hyphens)
- Job directories: `company-role-YYYY-MM/`
- Output resumes: `company-position-YYYY-MM-DD.docx`

## When User Asks For Help

- Direct them to `README.md` for overview
- Explain the workflow: extract → analyze → customize → generate
- Show example files if they're confused about format
- Use skills to guide them through the process interactively
