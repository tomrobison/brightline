---
name: explore-candidate
description: |
  Audit resume freshness by analyzing when experiences were last updated and
  identify stale content. Use when: (1) Before starting job applications,
  (2) Periodically reviewing resume content (monthly/quarterly),
  (3) Checking if achievements need updating.
---

## Purpose

Identify experiences and resume content that need updating based on staleness analysis using git history and modification dates.

## Process

When this skill is invoked, guide the user through freshness audit:

1. **Run freshness audit script**:
   ```bash
   # Activate venv if not already active
   source venv/bin/activate

   python3 scripts/audit_freshness.py
   ```

   Optional: Customize thresholds
   ```bash
   python3 scripts/audit_freshness.py \
     --current-role-threshold 60 \
     --recent-role-threshold 120 \
     --older-role-threshold 365
   ```

2. **Review the audit report**:
   - The script will display:
     - Total experiences analyzed
     - Number of stale items by category (current/recent/older)
     - Specific experiences needing review
     - Last update date for each stale item
     - Recommended actions

3. **Offer interactive review**:
   - Ask: "I found [N] experiences. [X] haven't been updated in 90+ days. Would you like to review any stale experiences now?"
   - If yes, proceed to step 4
   - If no, provide summary and exit

4. **Guide user through stale experiences** (one at a time, prioritized by staleness):
   - For each stale experience:
     - Use Read tool to show the experience file content
     - Say: "This experience at [Company] - [Position] hasn't been updated in [N] days."
     - Ask: "What would you like to do?"
       - a) Add recent achievements (guide user to add new bullets)
       - b) Update existing bullets (guide user to refine content)
       - c) Mark as reviewed - no changes needed (skip for now)
       - d) Skip for now

5. **After user updates** (for options a or b):
   - Remind user to commit changes so git history reflects the update
   - Move to next stale experience or complete review

6. **Provide final summary**:
   ```
   Review complete!
   ✓ [X] files reviewed
   ✓ [Y] files updated
   - [Z] files skipped

   Run /explore-candidate again anytime to check freshness.
   ```

## Interactive Prompts

Ask the user:
- "I found [N] experiences. [X] haven't been updated in 90+ days. Would you like to review any stale experiences now?"
- "Let me show you: [filename]. This experience hasn't been updated in [N] days."
- "What would you like to do? (a) Add recent achievements, (b) Update existing bullets, (c) Mark as reviewed, (d) Skip"
- After updates: "Great! Remember to commit these changes so the git history reflects your update."

## Understanding the Categories

- **Current role** (threshold: 90 days): Experiences with `endDate: present`
- **Recent roles** (threshold: 180 days): Experiences within last 2 years
- **Older roles** (threshold: 365 days): Experiences from 2+ years ago

## Common Scenarios

**Before job application:**
Run this skill to ensure your resume reflects your latest achievements and skills.

**Quarterly review:**
Set a reminder to run this every 3 months to keep content fresh.

**After major project:**
Update current role experiences when completing significant projects or achieving new results.

## Validation

Verify:
- Audit script runs successfully
- Git history is used for timestamps (or file modification times as fallback)
- Stale experiences are correctly categorized
- User understands what needs updating and why
- Interactive review helps user focus on highest-priority updates

## Next Steps

After updating experiences:
1. Commit changes: `git add data/experiences/*.md && git commit -m "Update stale experiences"`
2. Run `/analyze-job` if preparing for specific application
3. Schedule next freshness review (90 days for current role, 6-12 months otherwise)
