---
name: analyze-job
description: |
  Analyze job description to extract keywords, requirements, and generate
  tailoring recommendations for resume optimization. Use when: (1) Starting a
  new job application, (2) Analyzing job posting for keyword optimization,
  (3) Generating resume tailoring strategy based on job requirements.
---

## Purpose

Analyze a job description to identify keywords, requirements, and generate intelligent recommendations for resume tailoring.

## Process

When this skill is invoked, guide the user through job analysis:

1. **Collect job information**:
   - Ask user to provide the job posting (paste text or provide file)
   - Gather key details:
     - Company name
     - Position title
     - Target application date (default to today)

2. **Create job directory**:
   - Create directory: `jobs/[company-slug]-[position-slug]-YYYY-MM/`
   - Save job description to `job-description.md`

3. **Run analysis script**:
   ```bash
   python3 scripts/analyze_job.py \
     --job-description jobs/[dir]/job-description.md \
     --base-resume source/base-resume.yaml \
     --experiences-dir data/experiences \
     --output-dir jobs/[dir]/
   ```

4. **Review results with user**:
   - Display the keyword match score
   - Show matched vs. missing keywords
   - Present top matching experiences
   - Explain recommendations

5. **Guide customization**:
   - Show the generated `tailoring-config.yaml`
   - Explain key sections:
     - `resume.summary`: Should be customized for this role
     - `selection.experiences`: Which experiences to include
     - `keywords`: Required vs. preferred keywords
   - Ask if user wants to customize now or proceed with defaults

## Interactive Prompts

Ask the user:
- "Please paste the job description, or let me know if you've saved it to a file"
- "What company is this position for?"
- "What's the position title?"
- After analysis: "Your current resume matches [X]% of the requirements. The top matching experiences are: [list]. Does this look right?"
- "I've created a tailoring configuration at `jobs/[dir]/tailoring-config.yaml`. Would you like to customize the summary section before generating the resume, or proceed with the current configuration?"

## Output Files Created

- `jobs/[company-role-date]/job-description.md` - Saved job posting
- `jobs/[company-role-date]/keywords.yaml` - Extracted keywords and analysis
- `jobs/[company-role-date]/tailoring-config.yaml` - Initial configuration (editable)

## Next Steps

After analysis, guide the user to either:
1. Customize the tailoring config (especially the summary)
2. Run the `tailor-resume` skill to generate the final DOCX

## Validation

Verify:
- Job directory was created successfully
- Keywords were extracted (at least 5-10 keywords)
- Match score was calculated
- Tailoring config was generated with reasonable defaults
- User understands they should customize the summary
