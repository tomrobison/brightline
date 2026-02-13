---
title: Implementing explore-candidate skill for resume content freshness audit
type: feature_implementation
component: skills
date: 2026-02-13
tags:
  - resume-tailoring
  - skills
  - git
  - python
  - yaml
  - content-audit
  - gap-analysis
technologies:
  - Python
  - git
  - YAML
  - markdown
  - python-docx
  - PyYAML
  - python-frontmatter
symptom: Need skill to identify stale resume content and guide updates based on git history
solution_approach: Created explore-candidate skill using git worktree, implemented staleness detection via git log, interactive workflow for content review
key_insights:
  - Gap analysis redefined as time since last content update
  - Git history provides objective staleness metric
  - Interactive workflow guides user through outdated experiences
  - Follows repository skill patterns and conventions
related_issues: []
status: completed
---

## Problem

The user needed a way to identify stale resume content before applying to jobs. As time passes, experiences need updating - current roles should reflect recent achievements, recent roles need keyword refinement, and older roles may need archival. Without a systematic approach to auditing freshness, the resume becomes outdated and less competitive.

The user wanted:
1. An automated way to detect which experiences haven't been updated recently
2. Different staleness thresholds based on role type (current vs. recent vs. older)
3. Interactive guidance through reviewing and updating stale content
4. Integration with the existing resume tailoring workflow

## Investigation

Several approaches were considered for tracking freshness:

**Approach 1: Manual timestamp tracking**
- Add a `last_reviewed` field to experience frontmatter
- Requires manual updates, easy to forget
- Doesn't track actual content changes

**Approach 2: File modification time only**
- Use filesystem mtime
- Simple but unreliable (changes with file copies, git operations)
- No historical tracking

**Approach 3: Git history with fallback (CHOSEN)**
- Primary: Use `git log` to get last commit date for each file
- Fallback: Use filesystem mtime if file not in git history
- Provides reliable, automatic tracking
- Works with existing workflow (users commit changes)

**Staleness categorization approaches:**
- Fixed threshold for all experiences: Too simplistic
- Dynamic based on role age and priority (CHOSEN): More nuanced
  - Current role (endDate: present): 90 days
  - Recent roles (<2 years old): 180 days
  - Older roles (2+ years old): 365 days

## Root Cause / Design Decision

The chosen approach uses git history as the source of truth for freshness because:

1. **Automatic tracking**: Users already commit changes via the existing workflow
2. **Reliable**: Git timestamps don't change with file operations
3. **Historical context**: Can extend to show full edit history if needed
4. **Graceful degradation**: Falls back to mtime for uncommitted files
5. **Zero configuration**: No manual field updates required

The three-tier categorization system reflects how resume content ages:
- **Current roles** need frequent updates (90 days) to capture ongoing achievements
- **Recent roles** need periodic review (180 days) to maintain keyword accuracy
- **Older roles** need annual review (365 days) to decide if still relevant

## Solution

### Step 1: Create the freshness checker utility module

Create `scripts/utils/freshness_checker.py`:

```python
"""
Utility functions for checking resume content freshness.

Provides functions to determine staleness based on git history
and experience metadata.
"""

from datetime import datetime, timedelta
from typing import Dict, Optional
import subprocess
from pathlib import Path


def get_file_git_history(file_path: str) -> Optional[datetime]:
    """
    Get last commit date for a file from git history.

    Args:
        file_path: Path to file to check

    Returns:
        Datetime of last commit, or None if file not in git history
    """
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%aI", "--", file_path],
            capture_output=True,
            text=True,
            check=False
        )

        if result.returncode == 0 and result.stdout.strip():
            # Parse ISO 8601 datetime with timezone
            return datetime.fromisoformat(result.stdout.strip().replace('Z', '+00:00'))
        return None
    except Exception:
        return None


def get_recommended_review_frequency(experience: Dict) -> int:
    """
    Determine recommended review frequency in days based on experience type.

    Args:
        experience: Experience data with startDate, endDate, priority

    Returns:
        Days between reviews (90, 180, or 365)
    """
    # Current role: review every 90 days
    if experience.get('endDate') == 'present':
        return 90

    # High priority experiences: review every 180 days
    if experience.get('priority', 5) <= 2:
        return 180

    # Everything else: annual review
    return 365


def validate_threshold(value: int) -> bool:
    """
    Validate threshold argument is within acceptable range.

    Args:
        value: Threshold value in days

    Returns:
        True if valid (positive integer between 1-999)
    """
    return isinstance(value, int) and 1 <= value <= 999
```

**Key implementation details:**
- `get_file_git_history()`: Uses `git log -1 --format=%aI` to get ISO 8601 timestamp
- Returns `None` for files not in git, allowing fallback to filesystem mtime
- Handles timezone-aware datetime parsing
- `validate_threshold()`: Ensures user-provided thresholds are reasonable

### Step 2: Create the audit script

Create `scripts/audit_freshness.py` with:
- Git history tracking with filesystem fallback
- Configurable thresholds via CLI arguments (90/180/365 day defaults)
- Robust error handling for empty directories, malformed YAML, invalid dates
- Categorization logic (current_role/recent/older)
- Formatted report output with recommendations

See full implementation in the pull request.

### Step 3: Create the Claude skill

Create `skills/explore-candidate/SKILL.md` following repository conventions:
- YAML frontmatter with name and description
- Interactive workflow prompts for Claude to follow
- Process steps for running audit and reviewing results
- Validation checklist

**Interactive workflow pattern:**
1. Run audit script to generate report
2. Offer interactive review of stale items
3. Guide user through updating each stale experience
4. Remind user to commit changes for git tracking

### Step 4: Update CLAUDE.md

Add `explore-candidate` to the Available Skills section.

## Prevention Strategies

### 1. Establish review cadence
- **Current role**: Review every 90 days (quarterly)
- **Recent roles**: Review every 180 days (semi-annually)
- **Older roles**: Review annually

### 2. Commit changes immediately
Always commit experience updates right after making them:
```bash
git add data/experiences/company-role.md
git commit -m "Update Company role with Q4 achievements"
```

This ensures git history accurately reflects freshness.

### 3. Use the skill before job applications
Make it part of your job application workflow:
1. `/explore-candidate` - Check for stale content
2. Update any stale experiences
3. `/analyze-job` - Analyze specific job
4. `/tailor-resume` - Generate tailored resume

### 4. Add achievements as they happen
Don't wait for the audit to prompt you. Add achievements to current role experiences in real-time.

### 5. Customize thresholds per use case
Adjust based on your career stage:
- **Active job seeker**: More aggressive thresholds (60/90/180)
- **Passive candidate**: Standard thresholds (90/180/365)
- **Not looking**: Conservative thresholds (180/365/730)

## Best Practices

### Skill Development Pattern

**1. Structure**:
```
skills/[skill-name]/
├── SKILL.md          # Skill metadata and instructions
└── (optional files)  # Additional resources if needed
```

**2. SKILL.md Format**:
```markdown
---
name: skill-name
description: |
  Clear description of what this skill does. Use when: (1) Use case 1,
  (2) Use case 2, (3) Use case 3.
---

## Purpose
[One-sentence purpose]

## Process
[Step-by-step workflow with Claude instructions]

## Interactive Prompts
[Example questions to ask users]

## Validation
[How to verify success]
```

**3. Python Script Integration**:
- Skills invoke Python scripts via Bash tool
- Scripts live in `scripts/` directory
- Utility functions go in `scripts/utils/`
- Each script has clear `--help` and usage documentation
- Scripts print progress and return structured output

**4. Error Handling Pattern**:
- Check if directories exist before processing
- Validate YAML structure after loading
- Skip malformed files with warnings (don't crash)
- Provide helpful error messages that guide users
- Use try-except with specific exception types

### Code Organization

**Separation of Concerns**:
- `skills/` - Claude skill definitions
- `scripts/` - Main executable scripts
- `scripts/utils/` - Reusable utility modules
- `data/` - Structured data
- `jobs/` - Job-specific configurations

**Data Flow Pattern**:
```
User Input → Skill → Python Script → Utils → YAML/DOCX
```

## Testing Recommendations

### Virtual Environment Setup
```bash
# Create isolated environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Manual Testing Checklist

**For Each Skill**:
- [ ] Test with empty directories
- [ ] Test with missing files
- [ ] Test with malformed YAML
- [ ] Test with missing required fields
- [ ] Test with minimal valid input
- [ ] Verify error messages are helpful
- [ ] Verify output files are created correctly

**For This Skill Specifically**:
- [ ] Test with files recently committed (should show as fresh)
- [ ] Test with custom thresholds via CLI arguments
- [ ] Verify git history is used for timestamps
- [ ] Test fallback to file mtime for uncommitted files
- [ ] Verify categorization (current/recent/older) is correct

## Related Documentation

### Skills Following Same Pattern
- `skills/extract-resume/SKILL.md` - Extract DOCX resume into structured data
- `skills/analyze-job/SKILL.md` - Analyze job descriptions and extract keywords
- `skills/tailor-resume/SKILL.md` - Generate tailored DOCX resumes
- `skills/compare-versions/SKILL.md` - Compare resume versions

### Related Python Utilities
- `scripts/utils/markdown_parser.py` - Used for parsing markdown files with frontmatter
- `scripts/utils/keyword_matcher.py` - Keyword extraction patterns
- `scripts/utils/docx_handler.py` - DOCX generation patterns

### Documentation
- `CLAUDE.md` - Claude-specific instructions and workflow guidance
- `README.md` - Main project overview
- `docs/plans/2026-02-13-feat-resume-tailoring-system-plan.md` - System architecture

### Pull Request
- GitHub PR #1: https://github.com/tomrobison/brightline/pull/1

## Key Takeaways

1. **Git history is reliable**: Using `git log` for timestamps provides automatic, reliable freshness tracking
2. **Three-tier thresholds work well**: Different review frequencies for current/recent/older roles matches real-world needs
3. **Error handling is critical**: Gracefully handling empty directories, malformed YAML, and invalid dates prevents user frustration
4. **Interactive workflows guide users**: Following the established skill pattern (prompt → run → review → next steps) creates consistent UX
5. **Reuse existing utilities**: The `markdown_parser.py` module handled frontmatter parsing - no need to reinvent

## Future Enhancements

Deferred for later:
- Optional `last_reviewed_date` field tracking in frontmatter (explicit review dates vs. git history)
- Integration hooks with `analyze-job` skill to warn about stale content before tailoring
- Persistent configuration file for custom thresholds per user
- Visual timeline showing when each experience was last updated
- Batch update mode for marking multiple experiences as reviewed
