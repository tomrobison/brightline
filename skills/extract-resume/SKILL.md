---
name: extract-resume
description: |
  Extract resume content from DOCX file into structured YAML and Markdown files
  for resume tailoring. Use when the user wants to: (1) Convert existing resume
  to structured data format, (2) Initialize the resume tailoring repository,
  (3) Parse resume DOCX into editable components.
---

## Purpose

Extract structured data from an existing resume DOCX file and organize it into the resume tailoring repository format.

## Process

When this skill is invoked, guide the user through the extraction process:

1. **Confirm source file**: Identify the DOCX resume file to extract (check `source/` directory)

2. **Run extraction script**: Execute the extraction Python script:
   ```bash
   python3 scripts/extract_resume.py \
     --input source/[filename].docx \
     --output-base source/base-resume.yaml \
     --output-experiences data/experiences/
   ```

3. **Review extracted data**:
   - Show the user what was extracted
   - Read and display a sample experience file
   - Read the base-resume.yaml to verify basics were captured

4. **Guide enhancement**:
   - Explain that experience files need manual enhancement
   - Point out where to add:
     - Keywords for each experience
     - Priority levels
     - Relevant_for tags (which resume versions)
     - Better summaries for each role

5. **Next steps**:
   - Suggest reviewing and enhancing the experience files
   - Recommend organizing skills if needed
   - Explain they can now use `analyze-job` skill for job applications

## Interactive Guidance

Ask the user:
- "I found a resume file at `source/[filename].docx`. Should I extract data from this file?"
- After extraction: "I've created [N] experience files. Would you like me to show you one so you can see what to enhance?"
- "The extraction is complete! Your next step is to review and enhance the experience files in `data/experiences/`. Would you like help with that now, or are you ready to analyze a job description?"

## Validation

After extraction, verify:
- `source/base-resume.yaml` exists and contains basics (name, email, etc.)
- Experience files were created in `data/experiences/`
- Each experience file has frontmatter with metadata
- User understands next steps for enhancement
