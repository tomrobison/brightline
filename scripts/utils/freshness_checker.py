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


def validate_threshold(value: int) -> bool:
    """
    Validate threshold argument is within acceptable range.

    Args:
        value: Threshold value in days

    Returns:
        True if valid (positive integer between 1-999)
    """
    return isinstance(value, int) and 1 <= value <= 999
