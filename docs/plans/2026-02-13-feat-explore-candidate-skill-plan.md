---
title: Add explore-candidate skill for resume freshness audit
type: feat
date: 2026-02-13
---

# Add explore-candidate skill for resume freshness audit

Create a Claude Code skill that audits resume freshness by analyzing when experiences were last updated and prompting the user to review stale content.

## Problem Statement

Resume content becomes stale over time:
- Current role achievements aren't added regularly
- Old experiences remain unchanged for months/years
- Skills and keywords become outdated
- No systematic way to identify what needs updating

**User insight:** "Some gap analysis should be time since the resume was last updated"

## Proposed Solution

Build an **interactive freshness audit skill** that:
1. Scans experience files and checks last modification dates (via git history)
2. Identifies stale content based on thresholds (e.g., 3+ months for current role)
3. Prompts user interactively to update specific experiences
4. Optionally tracks explicit review dates in YAML frontmatter

## Acceptance Criteria

### Core Functionality
- [x] Skill exists at `skills/explore-candidate/SKILL.md` following repository conventions
- [x] Python script `scripts/audit_freshness.py` performs staleness detection
- [x] Uses git history to determine last modification dates for experience files
- [x] Flags experiences that haven't been updated in configurable timeframes:
  - Current role: 90 days (default)
  - Recent roles (within 2 years): 180 days (default)
  - Older roles: 365 days (default)
- [x] Generates summary report showing:
  - Total experiences analyzed
  - Number of stale items by category
  - Specific experiences needing review
  - Suggested actions (add achievements, update keywords, etc.)

### Error Handling & Validation
- [x] Handles empty `data/experiences/` directory gracefully with helpful message
- [x] Validates experience file frontmatter before processing
- [x] Catches and reports malformed YAML without crashing entire audit
- [x] Handles missing or invalid `endDate` fields (skip with warning)
- [x] Validates date format (ISO 8601 or "present")
- [x] Falls back to file modification time if git history unavailable
- [x] Skips template files (`_TEMPLATE.md` or files starting with `_`)

### Interactive Workflow
- [x] After report, prompts: "Would you like to review any stale experiences now?"
- [x] For each selected experience:
  - Shows current content using Read tool
  - Prompts for what to update (achievements, bullets, keywords)
  - Asks if user wants to mark as reviewed
- [ ] Optionally updates `last_reviewed_date` field in frontmatter after review (deferred for future enhancement)

### User Experience
- [x] CLI validates threshold arguments (positive integers 1-999)
- [x] Clear error messages for common issues (no git repo, invalid input)
- [x] Reports complete in < 5 seconds for typical resume (7-10 experiences)

## Technical Approach

### Data Sources
1. **Git history**: Use `git log -1 --format=%aI -- <file>` to get last modification
2. **Experience frontmatter**: Check `startDate`, `endDate`, `priority` to determine review frequency
3. **Optional metadata**: Add `last_reviewed_date` and `review_frequency` fields

### Architecture
```
Claude Skill (SKILL.md)
    ↓
Python Script (audit_freshness.py)
    ↓
Utility Module (scripts/utils/freshness_checker.py)
    ↓
Existing Parser (scripts/utils/markdown_parser.py)
```

### Key Components

**1. Skill: `skills/explore-candidate/SKILL.md`**
```markdown
---
name: explore-candidate
description: Audit resume freshness and identify stale content
---

## Purpose
Identify experiences and content that need updating based on staleness analysis.

## Process
1. Scan experience files in data/experiences/
2. Check git history for last modification dates
3. Calculate staleness scores
4. Present interactive report with recommendations
5. Guide user through updates

## Interactive Prompts
- "I found [N] experiences. [X] haven't been updated in 3+ months."
- "Your current role at [Company] was last updated [date]. Add recent achievements?"
- "Would you like to review experience [slug] now?"
```

**2. Python Script: `scripts/audit_freshness.py`**
```python
"""
Audit resume freshness by analyzing modification dates.

Usage:
    python scripts/audit_freshness.py
    python scripts/audit_freshness.py --current-role-threshold 90
"""

import argparse
from pathlib import Path
from datetime import datetime, timedelta
import subprocess
from typing import Dict, List
from utils.markdown_parser import load_experience_file

def get_last_modified_date(file_path: str) -> datetime:
    """Get last git commit date for file."""
    result = subprocess.run(
        ["git", "log", "-1", "--format=%aI", "--", file_path],
        capture_output=True,
        text=True
    )
    if result.returncode == 0 and result.stdout.strip():
        return datetime.fromisoformat(result.stdout.strip())
    # Fallback to file modification time if not in git
    return datetime.fromtimestamp(Path(file_path).stat().st_mtime)

def calculate_staleness(
    experience: Dict,
    last_modified: datetime,
    thresholds: Dict[str, int]
) -> Dict:
    """
    Calculate staleness score and category.

    Args:
        experience: Parsed experience data with frontmatter
        last_modified: Last modification datetime
        thresholds: Days thresholds by category

    Returns:
        {
            'is_stale': bool,
            'days_since_update': int,
            'category': str,
            'threshold': int
        }
    """
    days_since = (datetime.now() - last_modified).days

    # Determine category
    if experience.get('endDate') == 'present':
        category = 'current_role'
    else:
        end_date = datetime.fromisoformat(experience['endDate'])
        years_ago = (datetime.now() - end_date).days / 365
        category = 'recent' if years_ago < 2 else 'older'

    threshold = thresholds[category]

    return {
        'is_stale': days_since > threshold,
        'days_since_update': days_since,
        'category': category,
        'threshold': threshold
    }

def main():
    parser = argparse.ArgumentParser(description='Audit resume freshness')
    parser.add_argument(
        '--current-role-threshold',
        type=int,
        default=90,
        help='Days threshold for current role (default: 90)'
    )
    parser.add_argument(
        '--recent-role-threshold',
        type=int,
        default=180,
        help='Days threshold for recent roles (default: 180)'
    )
    parser.add_argument(
        '--older-role-threshold',
        type=int,
        default=365,
        help='Days threshold for older roles (default: 365)'
    )

    args = parser.parse_args()

    thresholds = {
        'current_role': args.current_role_threshold,
        'recent': args.recent_role_threshold,
        'older': args.older_role_threshold
    }

    # Scan experiences
    exp_dir = Path('data/experiences')

    # Handle empty directory
    if not exp_dir.exists():
        print("\n⚠️  No experiences directory found at data/experiences/")
        print("Run /extract-resume first to populate your resume data.")
        return

    results = []
    skipped = []

    for exp_file in exp_dir.glob('*.md'):
        # Skip template and hidden files
        if exp_file.name.startswith('_'):
            continue

        try:
            experience = load_experience_file(exp_file)

            # Validate required fields
            if not experience.get('endDate'):
                skipped.append(f"{exp_file.name}: Missing endDate field")
                continue

            # Validate date format
            if experience['endDate'] != 'present':
                try:
                    datetime.fromisoformat(experience['endDate'])
                except ValueError:
                    skipped.append(f"{exp_file.name}: Invalid date format '{experience['endDate']}'")
                    continue

            last_modified = get_last_modified_date(str(exp_file))
            staleness = calculate_staleness(experience, last_modified, thresholds)

            results.append({
                'file': exp_file.name,
                'company': experience.get('company', 'Unknown'),
                'position': experience.get('position', 'Unknown'),
                'last_modified': last_modified,
                **staleness
            })

        except Exception as e:
            skipped.append(f"{exp_file.name}: {str(e)}")

    # Exit if no valid experiences found
    if not results:
        print("\n⚠️  No valid experience files found.")
        if skipped:
            print("\nSkipped files:")
            for msg in skipped:
                print(f"  • {msg}")
        return

    # Print report
    print("\n" + "="*60)
    print("RESUME FRESHNESS AUDIT")
    print("="*60)

    stale_items = [r for r in results if r['is_stale']]

    print(f"\n✓ Analyzed {len(results)} experiences")
    print(f"⚠️  Found {len(stale_items)} stale items\n")

    if stale_items:
        print("Stale Experiences:")
        print("-"*60)
        for item in sorted(stale_items, key=lambda x: x['days_since_update'], reverse=True):
            print(f"\n{item['company']} - {item['position']}")
            print(f"  Last updated: {item['last_modified'].strftime('%Y-%m-%d')} ({item['days_since_update']} days ago)")
            print(f"  Category: {item['category']} (threshold: {item['threshold']} days)")
            print(f"  File: {item['file']}")

    print("\n" + "="*60)
    print("RECOMMENDATIONS")
    print("="*60)

    for item in stale_items:
        if item['category'] == 'current_role':
            print(f"• Update {item['company']}: Add recent achievements and projects")
        elif item['category'] == 'recent':
            print(f"• Review {item['company']}: Verify keywords and bullet accuracy")
        else:
            print(f"• Consider {item['company']}: Check if still relevant or archive")

if __name__ == '__main__':
    main()
```

**3. Utility: `scripts/utils/freshness_checker.py`**
```python
"""
Utility functions for checking resume content freshness.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
import subprocess
from pathlib import Path

def get_file_git_history(file_path: str) -> Optional[datetime]:
    """Get last commit date for a file from git history."""
    result = subprocess.run(
        ["git", "log", "-1", "--format=%aI", "--", file_path],
        capture_output=True,
        text=True,
        cwd=Path(file_path).parent
    )

    if result.returncode == 0 and result.stdout.strip():
        return datetime.fromisoformat(result.stdout.strip())
    return None

def get_recommended_review_frequency(experience: Dict) -> int:
    """
    Determine recommended review frequency in days based on experience type.

    Args:
        experience: Experience data with startDate, endDate, priority

    Returns:
        Days between reviews
    """
    # Current role: review every 90 days
    if experience.get('endDate') == 'present':
        return 90

    # High priority experiences: review every 180 days
    if experience.get('priority', 5) <= 2:
        return 180

    # Everything else: annual review
    return 365

def should_review(
    last_modified: datetime,
    experience: Dict,
    custom_threshold: Optional[int] = None
) -> bool:
    """
    Determine if an experience should be reviewed.

    Args:
        last_modified: Last modification datetime
        experience: Experience data
        custom_threshold: Override default threshold (days)

    Returns:
        True if review is needed
    """
    threshold = custom_threshold or get_recommended_review_frequency(experience)
    days_since = (datetime.now() - last_modified).days
    return days_since > threshold
```

## Interactive Workflow (Post-Report)

After displaying the freshness audit report, the skill should guide interactive review:

**1. Initial Prompt**
```
I found [N] experiences. [X] haven't been updated in 90+ days.
Would you like to review any stale experiences now? (y/n)
```

**2. If Yes - For Each Stale Experience** (prioritized by staleness)
```
Let me show you: [company-position-slug.md]
[Display file content with Read tool]

This experience hasn't been updated in [N] days.
What would you like to do?
  a) Add recent achievements
  b) Update existing bullets
  c) Mark as reviewed (no changes needed)
  d) Skip for now
```

**3. After User Makes Changes** (for options a or b)
```
Would you like me to update the last_reviewed_date field? (y/n)
[If yes, add/update frontmatter: last_reviewed_date: YYYY-MM-DD]
```

**4. Final Summary**
```
Review complete!
✓ [X] files reviewed
✓ [Y] files updated
- [Z] files skipped

Run /explore-candidate again anytime to check freshness.
```

## Context

### Existing Patterns to Follow
- **Skill structure**: YAML frontmatter + numbered process steps (see `skills/analyze-job/SKILL.md`)
- **Python integration**: Scripts in `scripts/` with argparse CLI (see `scripts/analyze_job.py`)
- **Utility reuse**: Import `markdown_parser.py` to load experience files
- **Interactive prompts**: Ask questions, show results, offer next steps

### File Paths
- Skill definition: `skills/explore-candidate/SKILL.md`
- Python script: `scripts/audit_freshness.py`
- Utility module: `scripts/utils/freshness_checker.py`
- Experience files: `data/experiences/*.md`

### Error Handling Guidelines
**Empty Directory**: Show friendly message directing user to run `/extract-resume`
**Malformed YAML**: Skip file with warning, continue processing others
**Invalid Dates**: Skip file with warning showing problematic date value
**Missing Git Repo**: Fall back to file modification times with warning
**Invalid Thresholds**: Validate CLI args are positive integers (1-999)

### Validation Requirements
```python
# Required frontmatter fields
required_fields = ['endDate', 'company', 'position']

# Valid endDate formats
- ISO 8601: "YYYY-MM-DD" (e.g., "2023-12-15")
- Current role: "present"

# Threshold validation
def validate_threshold(value: int) -> bool:
    return isinstance(value, int) and 1 <= value <= 999
```

### Integration Points
**Future Enhancement**: Consider adding freshness checks to:
- `analyze-job` skill: Warn if top-matched experiences are stale
- `tailor-resume` skill: Flag if selected experiences haven't been reviewed recently

### Optional Enhancement
Add explicit review tracking to experience frontmatter:
```yaml
---
company: "Company Name"
position: "Position"
# ... existing fields ...
last_reviewed_date: "2026-02-13"
review_frequency: "quarterly"  # or "monthly", "semi-annual", "annual"
next_review_due: "2026-05-13"
---
```

## Success Metrics

- User can identify stale content in < 30 seconds
- Freshness audit takes < 5 seconds to run
- Interactive prompts reduce manual file searching
- Git history provides accurate timestamps without manual metadata

## References

- Existing skills: `skills/*/SKILL.md` (4 examples)
- Python scripts: `scripts/analyze_job.py`, `scripts/tailor_resume.py`
- Markdown parser: `scripts/utils/markdown_parser.py`
- Experience format: `data/experiences/_TEMPLATE.md`
- Repository conventions: `CLAUDE.md`, `README.md`
