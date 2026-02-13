# Adding a Job Description - User Guide

A step-by-step guide to tailoring your resume for a specific job application using the resume tailoring system.

## Overview

This guide walks you through the process of:
1. Finding and saving a job description
2. Analyzing the job requirements
3. Customizing your resume for the role
4. Generating a tailored DOCX resume
5. Reviewing and iterating

**Time estimate:** 15-20 minutes for your first job, 10 minutes for subsequent jobs

## Prerequisites

Before starting, ensure:
- ✅ You've extracted your resume data (run `extract-resume` or `extract_resume.py`)
- ✅ Your experience files in `data/experiences/` are enhanced with keywords and priorities
- ✅ Python virtual environment is set up (`python3 -m venv venv`)
- ✅ Dependencies are installed (`pip install -r requirements.txt`)

## Step 1: Find and Copy the Job Description

### Where to Find Job Descriptions

**Job Boards:**
- LinkedIn Jobs
- Indeed
- Glassdoor
- AngelList (startups)
- Company career pages

**What to Copy:**

Copy the **entire job posting** including:
- Job title and company name
- Location and employment type
- Job summary/overview
- Responsibilities and duties
- Required qualifications
- Preferred qualifications
- Benefits and perks
- Application instructions

**Pro tip:** Copy everything! The analysis script will extract what matters, and having extra context helps with keyword matching.

### Example Job Posting

```
Senior DevOps Engineer - TechCorp Inc.

Location: Remote (US)
Type: Full-time
Posted: February 13, 2026

About the Role:
We're seeking a Senior DevOps Engineer to lead our cloud infrastructure...

Responsibilities:
• Design and maintain AWS infrastructure serving 10M+ users
• Implement CI/CD pipelines using Jenkins and GitHub Actions
• Manage Kubernetes clusters and containerized applications
• Collaborate with development teams on infrastructure needs
• Ensure 99.99% uptime through monitoring and automation

Required Qualifications:
• 5+ years of DevOps/Infrastructure experience
• Expert knowledge of AWS (EC2, S3, RDS, Lambda, CloudFormation)
• Strong experience with Kubernetes and Docker
• Proficiency in Python, Bash, or Go
• Experience with CI/CD tools (Jenkins, GitHub Actions, CircleCI)

Preferred Qualifications:
• Experience with Infrastructure as Code (Terraform, CloudFormation)
• Background in security and compliance (SOC2, ISO)
• PostgreSQL database management
• Monitoring tools (DataDog, Splunk, CloudWatch)
```

## Step 2: Create Job Directory and Save Description

### Create Directory Structure

Use this naming convention for job directories:

```
jobs/[company-slug]-[role-slug]-YYYY-MM/
```

**Examples:**
- `jobs/techcorp-senior-devops-2026-02/`
- `jobs/acme-platform-engineer-2026-03/`
- `jobs/startup-infrastructure-lead-2026-02/`

**Create the directory:**

```bash
mkdir -p jobs/techcorp-senior-devops-2026-02
```

### Save the Job Description

Create a file called `job-description.md` in the job directory:

```bash
# Using a text editor
vim jobs/techcorp-senior-devops-2026-02/job-description.md

# Or using echo (for smaller descriptions)
cat > jobs/techcorp-senior-devops-2026-02/job-description.md << 'EOF'
[Paste your job description here]
EOF
```

**File structure should look like:**

```
jobs/techcorp-senior-devops-2026-02/
└── job-description.md
```

### Add Optional Frontmatter (Recommended)

You can add YAML frontmatter to organize job metadata:

```markdown
---
company: "TechCorp Inc."
position: "Senior DevOps Engineer"
location: "Remote (US)"
posted_date: "2026-02-13"
application_deadline: "2026-03-15"
salary_range: "$140K - $180K"
source: "LinkedIn Jobs"
url: "https://linkedin.com/jobs/12345"
---

# Senior DevOps Engineer - TechCorp Inc.

[Rest of job description...]
```

**Why add frontmatter?**
- Tracks application details
- Makes it easy to search your job history later
- Helps you remember context months from now

## Step 3: Run the Job Analysis Script

### Activate Virtual Environment

```bash
cd /path/to/resume
source venv/bin/activate
```

### Run Analysis

```bash
python3 scripts/analyze_job.py \
  --job-description jobs/techcorp-senior-devops-2026-02/job-description.md \
  --base-resume source/base-resume.yaml \
  --experiences-dir data/experiences \
  --output-dir jobs/techcorp-senior-devops-2026-02/
```

**What the script does:**
1. Reads the job description
2. Extracts keywords using frequency analysis and pattern matching
3. Separates required vs. preferred qualifications
4. Categorizes keywords (technical skills, soft skills, industry terms)
5. Compares against your current resume
6. Calculates match score
7. Identifies your most relevant experiences
8. Generates recommendations
9. Creates initial tailoring configuration

### Expected Output

```
Analyzing job description: jobs/techcorp-senior-devops-2026-02/job-description.md
Extracting keywords and requirements...
Found 15 required and 8 preferred keywords

Analyzing match against current resume...

✓ Overall Match Score: 78%
  - Required keywords: 82%
  - Preferred keywords: 68%

Generating tailoring recommendations...
✓ Saved keyword analysis: jobs/techcorp-senior-devops-2026-02/keywords.yaml
✓ Created tailoring config: jobs/techcorp-senior-devops-2026-02/tailoring-config.yaml

✓ Analysis complete!

Recommendations:
  - Consider emphasizing: Kubernetes, Infrastructure as Code, monitoring

Next steps:
1. Review and customize: jobs/techcorp-senior-devops-2026-02/tailoring-config.yaml
2. Update the summary section for this specific role
3. Run tailor_resume.py to generate the tailored resume
```

### Files Created

After analysis, your job directory will contain:

```
jobs/techcorp-senior-devops-2026-02/
├── job-description.md          # Your saved job posting
├── keywords.yaml                # Extracted keywords + analysis
└── tailoring-config.yaml        # Resume customization settings
```

## Step 4: Review the Keyword Analysis

Open `keywords.yaml` to see what the script found:

```bash
cat jobs/techcorp-senior-devops-2026-02/keywords.yaml
```

**What to look for:**

```yaml
job_title: "Senior DevOps Engineer"
company: "TechCorp Inc."
analyzed_date: "2026-02-13"

keywords:
  technical_skills:
    - keyword: "aws"
      frequency: 8
      priority: "required"
      contexts: ["AWS infrastructure", "EC2, S3, RDS, Lambda"]

    - keyword: "kubernetes"
      frequency: 6
      priority: "required"
      contexts: ["Kubernetes clusters", "containerized applications"]

    - keyword: "python"
      frequency: 4
      priority: "required"

  soft_skills:
    - keyword: "collaboration"
      frequency: 3
      priority: "preferred"

match_analysis:
  overall_score: 78
  required_score: 82
  preferred_score: 68

  required_matched:
    - "aws"
    - "kubernetes"
    - "docker"
    - "python"
    - "jenkins"

  required_missing:
    - "github actions"
    - "monitoring"

  experience_matches:
    - slug: "idme-director-devops"
      company: "ID.me"
      score: 92
      matched_keywords: ["aws", "jenkins", "python", "infrastructure"]
```

**Key metrics to understand:**
- **Overall score**: 78% means you match 78% of the job requirements
- **Required vs. Preferred**: Focus on required keywords first
- **Experience matches**: Shows which of your experiences are most relevant
- **Missing keywords**: Gaps you might want to address (if you actually have that experience)

## Step 5: Customize the Tailoring Configuration

This is the **most important step** - customize your resume for this specific role.

Open the tailoring config:

```bash
vim jobs/techcorp-senior-devops-2026-02/tailoring-config.yaml
```

### Section 1: Job Metadata

```yaml
job:
  company: "TechCorp Inc."
  position: "Senior DevOps Engineer"
  application_date: "2026-02-13"
```

✅ Usually correct as-is. Update application_date if applying later.

### Section 2: Resume Settings

```yaml
resume:
  version: "senior-engineer"        # Which persona to use
  length: "2-page"                  # Target: "1-page" or "2-page"
  summary: "# Customize this summary for the specific role"
```

**🔴 CRITICAL: Write a custom summary**

Replace the placeholder with a 2-3 sentence summary tailored to this role:

```yaml
resume:
  version: "devops-director"
  length: "2-page"
  summary: |
    DevOps leader with 10+ years architecting AWS cloud infrastructure serving
    millions of users. Expert in Kubernetes, CI/CD automation, and infrastructure
    as code. Proven track record migrating datacenters to AWS, achieving 99.99%
    uptime, and leading high-performing engineering teams.
```

**Tips for writing summaries:**
- Lead with your strongest qualification for THIS role
- Include specific keywords from required qualifications
- Quantify when possible (years, scale, impact)
- Mention the technologies they care about most
- Keep it 2-3 sentences (not a paragraph)

### Section 3: Keywords

```yaml
keywords:
  required:
    - "aws"
    - "kubernetes"
    - "docker"
    - "jenkins"
    - "python"
    - "ci/cd"

  preferred:
    - "terraform"
    - "cloudformation"
    - "postgresql"
    - "monitoring"

  industry_terms:
    - "infrastructure as code"
    - "containerization"
```

✅ Usually good as-is. The script extracted these from the job description.

**Optional tweaks:**
- Remove keywords you don't actually have experience with
- Add variations you want to emphasize (e.g., "AWS Lambda" if they mentioned it)

### Section 4: Experience Selection

**This is where you choose which experiences to include:**

```yaml
selection:
  experiences:
    - slug: "idme-director-devops"
      version: "detailed"           # detailed (5 bullets), standard (3), or concise (2)
      customize:
        emphasis: ["aws", "kubernetes", "jenkins"]

    - slug: "idme-director-security"
      version: "standard"
      customize:
        emphasis: ["infrastructure", "monitoring"]

    - slug: "cerner-software-engineer"
      version: "concise"
```

**How to decide:**

1. **Check `keywords.yaml`** for `experience_matches` - it ranks your experiences by relevance score
2. **Include your top 3-4 most relevant experiences**
3. **Use version strategically:**
   - `detailed` (5 bullets): Your most relevant experience for this role
   - `standard` (3 bullets): Supporting experiences
   - `concise` (2 bullets): Less relevant but still valuable

**Example decisions:**

| Experience | Relevance | Version | Why |
|------------|-----------|---------|-----|
| ID.me Director DevOps | 92% match | detailed | Perfect match - AWS, K8s, Jenkins |
| ID.me Director Security | 75% match | standard | Shows infrastructure + monitoring |
| Cerner Software Engineer | 65% match | concise | Relevant but older |
| ukoot Developer | 50% match | exclude | Too old, less relevant |

### Section 5: Skills

```yaml
selection:
  skills:
    priority_categories:
      - "Cloud Platforms"
      - "DevOps & Automation"
      - "Programming Languages"

    highlight_keywords:
      - "AWS"
      - "Kubernetes"
      - "Docker"
      - "Jenkins"
```

**Priority categories**: Skills section will be reordered to show these categories first

**Highlight keywords**: These skills will be emphasized (could be bolded or listed first)

### Section 6: Optimization Settings

```yaml
optimization:
  target_match_score: 85            # Goal for keyword coverage
  max_pages: 2                      # Hard limit
  bullet_point_strategy: "keyword-dense"  # or "achievement-focused"

  constraints:
    max_bullets_per_experience: 5
    max_experiences: 4
    max_projects: 3
```

**Usually good as-is**, but you can adjust:
- `target_match_score`: Lower to 80 if you're struggling to fit keywords naturally
- `max_pages`: Set to 1 for more junior roles or startup applications
- `bullet_point_strategy`:
  - `keyword-dense`: Optimize for ATS (recommended for most jobs)
  - `achievement-focused`: Emphasize impact over keywords (for recruiter screening)

## Step 6: Generate the Tailored Resume

### Run the Tailoring Script

```bash
python3 scripts/tailor_resume.py \
  --job-config jobs/techcorp-senior-devops-2026-02/tailoring-config.yaml \
  --base-resume source/base-resume.yaml \
  --experiences-dir data/experiences \
  --output output/techcorp-senior-devops-2026-02.docx
```

### What Happens

The script executes a **four-phase process**:

**Phase 1: Content Selection**
```
Loading configuration...
Loading experiences...
Selected 3 experiences

Selecting content based on configuration...
Selected 3 experiences
```

Loads your experiences and selects the ones specified in the config.

**Phase 2: Keyword Optimization**
```
Phase 1: Analyzing keyword match...
```

Ensures required keywords appear in your resume. Checks:
- Are all required keywords present?
- Is keyword density appropriate?
- Are keywords distributed naturally across sections?

**Phase 3: Length Optimization**
```
Phase 2: Optimizing length...
Current estimated length: 2.3 pages (target: 2)
Applying length optimization...
```

If resume is over target length, applies reduction strategies:
1. Switch experiences from detailed to standard versions
2. Remove lowest-scoring bullet points
3. Condense lengthy bullets while preserving keywords

**Phase 4: DOCX Generation**
```
Phase 3: Generating DOCX resume...
✓ Resume saved to: output/techcorp-senior-devops-2026-02.docx
```

Creates the formatted Word document with ATS-compatible styling.

### Expected Output

```
============================================================
RESUME TAILORING REPORT
============================================================

Job: Senior DevOps Engineer at TechCorp Inc.

Keyword Match Score: 87%
  - Required keywords: 91%
  - Preferred keywords: 78%

Matched Keywords (14):
  ✓ aws
  ✓ kubernetes
  ✓ docker
  ✓ jenkins
  ✓ python
  ✓ ci/cd
  ✓ terraform
  ✓ postgresql
  ✓ monitoring
  ✓ infrastructure
  [...]

Missing Keywords (2):
  ✗ github actions
  ✗ cloudformation

Final Resume Length: ~1.9 pages

Optimizations Applied:
  - Shortened ID.me Director IT from detailed to standard
  - Condensed lengthy bullet in ID.me Director Security

✓ Target match score achieved (85%)

============================================================

✓ Resume generated: output/techcorp-senior-devops-2026-02.docx

Next steps:
1. Review the generated DOCX file
2. Make manual adjustments if needed
3. If match score is low, update tailoring-config.yaml and regenerate
```

### Understanding the Match Score

**What's a good score?**

| Score | Meaning | Action |
|-------|---------|--------|
| 85%+ | Excellent | Strong ATS match, proceed with confidence |
| 70-84% | Good | Solid match, consider emphasizing 1-2 more keywords |
| 60-69% | Fair | Review missing keywords - do you have that experience? |
| <60% | Poor | Either wrong role for you, or config needs significant revision |

**If score is below target:**
1. Check **Missing Keywords** list
2. If you have that experience, add it to relevant bullet points
3. If you don't have it, consider if this role is a good fit
4. Regenerate and check new score

## Step 7: Review the Generated Resume

### Open the DOCX File

```bash
open output/techcorp-senior-devops-2026-02.docx
```

### What to Check

**✅ Formatting Quality:**
- [ ] Contact information is clear and prominent
- [ ] Section headers are bold and well-spaced
- [ ] Bullet points are properly indented
- [ ] Fonts are standard (Arial, Calibri)
- [ ] No weird spacing or alignment issues
- [ ] Page breaks are in reasonable places

**✅ Content Accuracy:**
- [ ] All job titles and companies are correct
- [ ] Dates are accurate
- [ ] No typos or grammatical errors
- [ ] Technical terms are spelled correctly
- [ ] Bullet points make sense and flow well

**✅ Keyword Integration:**
- [ ] Required keywords appear naturally (not stuffed)
- [ ] Keywords are in context (not just listed)
- [ ] Summary includes key terms
- [ ] Skills section is prominent

**✅ Length:**
- [ ] Fits within target (1-page or 2-page)
- [ ] Content is not too cramped or too sparse
- [ ] All critical information is included

### Common Issues and Fixes

**Issue: "Resume is 2.3 pages, over my 2-page target"**

**Fix options:**
1. Edit `tailoring-config.yaml` and change versions to more concise:
   ```yaml
   - slug: "idme-director-it"
     version: "concise"  # was "standard"
   ```

2. Reduce max bullets per experience:
   ```yaml
   constraints:
     max_bullets_per_experience: 4  # was 5
   ```

3. Exclude less relevant experience:
   ```yaml
   experiences:
     # Remove or comment out lowest-relevance experience
     # - slug: "ukoot-developer"
   ```

Then regenerate: `python3 scripts/tailor_resume.py ...`

**Issue: "Match score is only 68%, below my 85% target"**

**Fix:**
1. Review missing keywords in the report
2. Check if you have that experience:
   - **YES** → Add to relevant experience file, update bullet points
   - **NO** → Lower your target score or accept the gap

3. Example: Missing "GitHub Actions"
   ```markdown
   # Edit: data/experiences/idme-director-devops.md

   ### 3. CI/CD Pipeline Implementation [priority:2, keywords:Jenkins,GitHub Actions,automation]
   Designed and implemented automated CI/CD pipelines using Jenkins and GitHub Actions,
   reducing deployment time from 2 hours to 15 minutes.
   ```

4. Regenerate resume

**Issue: "Keywords feel stuffed/unnatural"**

**Fix:** Change bullet point strategy:
```yaml
optimization:
  bullet_point_strategy: "achievement-focused"  # was "keyword-dense"
```

This prioritizes readability over keyword density.

## Step 8: Iterate (If Needed)

### When to Iterate

Iterate if:
- ❌ Match score is below target and you can improve it
- ❌ Resume length is over target
- ❌ Content doesn't flow well
- ❌ Missing a critical achievement or skill
- ❌ Keywords feel unnatural

### How to Iterate

1. **Make changes** to `tailoring-config.yaml` or experience files
2. **Regenerate** with the same command
3. **Compare** new output with previous version
4. **Repeat** until satisfied

### Version Control Tip

If you want to keep multiple versions:

```bash
# First attempt
output/techcorp-senior-devops-2026-02-v1.docx

# After iteration
output/techcorp-senior-devops-2026-02-v2.docx

# Final version (rename when done)
output/techcorp-senior-devops-2026-02-final.docx
```

## Step 9: Finalize and Track

### Save Your Configuration

Your job directory now contains:

```
jobs/techcorp-senior-devops-2026-02/
├── job-description.md           # Original posting
├── keywords.yaml                 # Analysis results
└── tailoring-config.yaml         # Your customizations
```

**This is your historical record!** Keep it for:
- Reference if you get an interview
- Learning what works for future applications
- Updating resume if you reapply later

### Track Application

Add application tracking to `job-description.md`:

```markdown
---
company: "TechCorp Inc."
position: "Senior DevOps Engineer"
application_date: "2026-02-13"
status: "applied"
resume_version: "techcorp-senior-devops-2026-02.docx"
match_score: 87
---

# Application Notes

**Applied:** 2026-02-13
**Method:** LinkedIn Easy Apply
**Contact:** recruiter@techcorp.com
**Resume version:** output/techcorp-senior-devops-2026-02.docx
**Cover letter:** Yes (emphasized AWS migration experience)

## Interview Prep

Focus areas based on resume:
- AWS infrastructure architecture (they'll ask about the 100+ server migration)
- Kubernetes deployment strategies
- CI/CD pipeline design
```

### Commit to Git (Optional)

```bash
git add jobs/techcorp-senior-devops-2026-02/
git commit -m "Add TechCorp Senior DevOps application (87% match)

Tailored for AWS/Kubernetes role. Emphasized:
- ID.me DevOps work (detailed version)
- 100+ server AWS migration
- CI/CD pipeline with Jenkins

Match score: 87% (target 85%)"
```

## Quick Reference: Complete Workflow

```bash
# 1. Create job directory
mkdir -p jobs/company-role-YYYY-MM

# 2. Save job description
vim jobs/company-role-YYYY-MM/job-description.md

# 3. Analyze job
source venv/bin/activate
python3 scripts/analyze_job.py \
  --job-description jobs/company-role-YYYY-MM/job-description.md \
  --base-resume source/base-resume.yaml \
  --output-dir jobs/company-role-YYYY-MM/

# 4. Customize config
vim jobs/company-role-YYYY-MM/tailoring-config.yaml
# - Write custom summary
# - Select experiences (3-4 most relevant)
# - Choose versions (detailed/standard/concise)

# 5. Generate resume
python3 scripts/tailor_resume.py \
  --job-config jobs/company-role-YYYY-MM/tailoring-config.yaml \
  --base-resume source/base-resume.yaml \
  --output output/company-role-YYYY-MM.docx

# 6. Review output
open output/company-role-YYYY-MM.docx

# 7. Iterate if needed (edit config, regenerate)

# 8. Apply!
```

## Tips for Success

### Keyword Strategy

**DO:**
✅ Use keywords naturally in context
✅ Include both acronyms and full terms (AWS and Amazon Web Services)
✅ Put key terms in your summary
✅ Match the job's language exactly (they say "Kubernetes" not "K8s" → use "Kubernetes")

**DON'T:**
❌ Keyword stuff (unnatural repetition)
❌ List keywords without context
❌ Add skills you don't actually have
❌ Use synonyms if the job uses specific terms

### Experience Selection

**Prioritize:**
1. Most recent experience (usually most relevant)
2. Highest keyword match score (check keywords.yaml)
3. Most impressive achievements
4. Best demonstration of required skills

**Consider excluding:**
- Very old experiences (10+ years unless highly relevant)
- Unrelated roles (if you have enough relevant experience)
- Internships or short-term contracts (if you have substantial full-time experience)

### Summary Writing

**Formula:**
```
[Role/Level] with [Years] experience in [Key Technology/Domain].
[Specific expertise in 2-3 job requirements]. [Quantified achievement
or relevant impact].
```

**Example:**
```
Senior DevOps Engineer with 10+ years architecting cloud infrastructure
at scale. Expert in AWS, Kubernetes, and CI/CD automation with proven
track record of achieving 99.99% uptime and reducing deployment time
by 85%.
```

### Time Management

- **First job**: 20-30 minutes (includes learning the system)
- **Second job**: 15 minutes
- **Third+ jobs**: 10 minutes (you know what you're doing now)

**Speed tips:**
- Keep a template summary you can quickly adapt
- Use previous tailoring-configs as starting points
- Focus your time on the summary and experience selection
- Don't obsess over 85% vs 87% match score

## Troubleshooting

### "Script says match score is 45%"

**Likely causes:**
1. Wrong role for your background (DevOps job but you're a frontend developer)
2. Job description has unusual/niche requirements
3. Your experience files need better keywords

**Action:**
- Check if you're qualified for this role
- Review missing keywords - do you have ANY of that experience?
- If yes, update experience files with those keywords and regenerate
- If no, consider if this is the right opportunity

### "Resume is 3.2 pages, way over target"

**Likely causes:**
1. Too many experiences selected
2. All using "detailed" versions
3. Wordy bullet points

**Quick fixes:**
```yaml
# Reduce experience count
experiences:
  - slug: "most-relevant-1"
  - slug: "most-relevant-2"
  - slug: "most-relevant-3"
  # Remove 4th+ experiences

# Use more concise versions
experiences:
  - slug: "experience-1"
    version: "standard"  # was "detailed"
  - slug: "experience-2"
    version: "concise"   # was "standard"

# Reduce max bullets
constraints:
  max_bullets_per_experience: 3  # was 5
```

### "Keywords don't appear naturally"

Try achievement-focused strategy:
```yaml
optimization:
  bullet_point_strategy: "achievement-focused"
```

Or manually edit the generated DOCX to improve flow.

## Next Steps

Now that you know the process:

1. **Build a job library**: Apply to 3-5 jobs to build experience with the system
2. **Track what works**: Note which resume versions get responses
3. **Refine your experiences**: Update bullet points based on what resonates
4. **Experiment**: Try different summaries, experience selections, keyword strategies
5. **Iterate on your base data**: As you learn what works, improve your experience files

## Getting Help

If you run into issues:

1. **Check the error message** - scripts provide helpful error details
2. **Review `README.md`** - comprehensive reference
3. **Check `CLAUDE.md`** - project-specific guidance
4. **Examine generated files** - keywords.yaml shows what the script found
5. **Compare with examples** - look at _TEMPLATE.md for proper format

---

**You're ready to apply!** This system takes a bit of setup the first time, but once you've done one job, subsequent applications are quick and easy. Good luck with your job search! 🚀
