---
name: tailor-resume
description: |
  Generate a tailored resume DOCX file based on job-specific configuration,
  optimizing for keywords, length, and relevance. Use when: (1) Ready to
  generate final resume for job application, (2) Creating multiple resume
  versions for different roles, (3) Optimizing resume for ATS and keyword
  matching.
---

## Purpose

Generate a professionally tailored resume DOCX file optimized for a specific job application.

## Process

When this skill is invoked, orchestrate the resume generation:

1. **Select job configuration**:
   - List available job directories in `jobs/`
   - Ask user which job to tailor for
   - Or accept specific path if provided

2. **Verify configuration**:
   - Read the `tailoring-config.yaml`
   - Check if summary has been customized (warn if it's still a placeholder)
   - Confirm key settings:
     - Target length (1-page or 2-page)
     - Selected experiences
     - Keyword requirements

3. **Run tailoring script**:
   ```bash
   python3 scripts/tailor_resume.py \
     --job-config jobs/[dir]/tailoring-config.yaml \
     --base-resume source/base-resume.yaml \
     --experiences-dir data/experiences \
     --output output/[company-position-date].docx
   ```

4. **Review generation report**:
   - Display keyword match score
   - Show final page count
   - List any optimizations applied
   - Highlight if target match score was achieved

5. **Quality check prompts**:
   - Ask if user wants to review the DOCX
   - If match score is below target, suggest adjustments:
     - Emphasize specific keywords
     - Include additional relevant experiences
     - Customize bullet points
   - If length is over target, show what was condensed

6. **Iterate if needed**:
   - If user wants changes, help them edit `tailoring-config.yaml`
   - Re-run the script with updated configuration
   - Repeat until satisfied

## Interactive Prompts

Ask the user:
- "I found [N] job configurations. Which one should I generate a resume for?" (list options)
- Before generation: "The summary in your config is: '[summary preview]'. Does this look good, or should we customize it first?"
- After generation: "✓ Resume generated with [X]% keyword match. The resume is approximately [Y] pages. Would you like to review it, or make adjustments?"
- If score is low: "The keyword match is [X]%, below your target of [T]%. Would you like me to suggest improvements?"
- If length is over: "The resume is slightly over [N] pages. I've condensed [changes]. Is this acceptable, or should we reduce it further?"

## Output

- Tailored DOCX resume file in `output/` directory
- Generation report showing:
  - Keyword match score (required and preferred)
  - Matched and missing keywords
  - Final page count estimate
  - Optimizations applied
  - Quality assessment

## Iteration Support

If user wants to regenerate:
1. Ask what they want to change
2. Help them edit the appropriate section of `tailoring-config.yaml`:
   - Summary customization
   - Experience selection/versions
   - Bullet point count limits
   - Target page length
3. Re-run the generation script
4. Compare new results with previous version

## Validation

After generation, verify:
- DOCX file was created successfully
- Keyword match score is reasonable (>60%)
- Page count is within acceptable range
- No errors in generation process
- User is satisfied with the output or knows how to iterate

## Tips for Users

Share these tips:
- **Match score >85%**: Excellent, likely to pass ATS
- **Match score 70-85%**: Good, may want to emphasize a few more keywords
- **Match score <70%**: Consider adding more relevant experiences or keywords
- **Length optimization**: If resume is condensed, review to ensure key achievements remain
- **Iteration is expected**: Most users generate 2-3 versions before finalizing
