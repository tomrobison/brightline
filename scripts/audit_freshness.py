#!/usr/bin/env python3
"""
Audit resume freshness by analyzing modification dates.

Scans experience files and uses git history to identify stale content
that needs updating.

Usage:
    python scripts/audit_freshness.py
    python scripts/audit_freshness.py --current-role-threshold 60
    python scripts/audit_freshness.py --recent-role-threshold 120
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from utils.markdown_parser import parse_experience_file
from utils.freshness_checker import (
    get_file_git_history,
    validate_threshold
)


def get_last_modified_date(file_path: str) -> datetime:
    """
    Get last modification date for file (git history or filesystem).

    Args:
        file_path: Path to file

    Returns:
        Datetime of last modification
    """
    # Try git history first
    git_date = get_file_git_history(file_path)
    if git_date:
        return git_date

    # Fallback to file modification time
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
        Dictionary with:
            is_stale: bool
            days_since_update: int
            category: str ('current_role', 'recent', 'older')
            threshold: int
    """
    # Make last_modified timezone-naive for comparison
    if last_modified.tzinfo is not None:
        last_modified = last_modified.replace(tzinfo=None)

    days_since = (datetime.now() - last_modified).days

    # Determine category
    if experience.get('endDate') == 'present':
        category = 'current_role'
    else:
        try:
            end_date = datetime.fromisoformat(experience['endDate'])
            years_ago = (datetime.now() - end_date).days / 365
            category = 'recent' if years_ago < 2 else 'older'
        except (ValueError, KeyError):
            # If we can't parse endDate, treat as older
            category = 'older'

    threshold = thresholds[category]

    return {
        'is_stale': days_since > threshold,
        'days_since_update': days_since,
        'category': category,
        'threshold': threshold
    }


def main():
    """Run freshness audit."""
    parser = argparse.ArgumentParser(
        description='Audit resume freshness by analyzing modification dates'
    )
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

    # Validate thresholds
    if not all([
        validate_threshold(args.current_role_threshold),
        validate_threshold(args.recent_role_threshold),
        validate_threshold(args.older_role_threshold)
    ]):
        print("❌ Error: Thresholds must be positive integers between 1-999")
        sys.exit(1)

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
        sys.exit(0)

    results = []
    skipped = []

    for exp_file in sorted(exp_dir.glob('*.md')):
        # Skip template and hidden files
        if exp_file.name.startswith('_'):
            continue

        try:
            experience = parse_experience_file(str(exp_file))

            # Validate required fields
            if not experience.get('endDate'):
                skipped.append(f"{exp_file.name}: Missing endDate field")
                continue

            # Validate date format
            if experience['endDate'] != 'present':
                try:
                    datetime.fromisoformat(experience['endDate'])
                except ValueError:
                    skipped.append(
                        f"{exp_file.name}: Invalid date format '{experience['endDate']}'"
                    )
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
        sys.exit(0)

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
            print(f"  Last updated: {item['last_modified'].strftime('%Y-%m-%d')} "
                  f"({item['days_since_update']} days ago)")
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

    else:
        print("✅ All experiences are up to date!")

    # Show skipped files if any
    if skipped:
        print("\n" + "="*60)
        print("SKIPPED FILES")
        print("="*60)
        for msg in skipped:
            print(f"  ⚠️  {msg}")

    print("\n" + "="*60)


if __name__ == '__main__':
    main()
