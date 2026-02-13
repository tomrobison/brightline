"""
Markdown file parsing utilities for experience and project files.

Parses markdown files with YAML frontmatter to extract structured data.
"""

import os
import re
from typing import Dict, List, Any
import frontmatter


def parse_experience_file(file_path: str) -> Dict[str, Any]:
    """
    Parse an experience markdown file with frontmatter.

    Args:
        file_path: Path to the experience markdown file

    Returns:
        Dictionary with metadata and content
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        post = frontmatter.load(f)

    data = dict(post.metadata)
    data['content'] = post.content
    data['slug'] = os.path.splitext(os.path.basename(file_path))[0]

    # Parse bullets from content
    data['bullets'] = parse_bullets_from_markdown(post.content, data.get('versions', {}))

    return data


def parse_bullets_from_markdown(content: str, versions: Dict[str, int]) -> List[Dict[str, Any]]:
    """
    Parse bullet points from markdown content with metadata.

    Extracts bullets with priority and keywords from format:
    ### 1. Title [priority:1, keywords:Python,AWS]

    Args:
        content: Markdown content
        versions: Dictionary with version names and bullet counts

    Returns:
        List of bullet dictionaries with text, priority, keywords
    """
    bullets = []

    # Pattern to match bullet headers with optional metadata
    pattern = r'###\s+\d+\.\s+(.+?)(?:\[(.+?)\])?\n((?:.+\n)*?)(?=###|\Z)'

    matches = re.finditer(pattern, content, re.MULTILINE)

    for i, match in enumerate(matches, 1):
        title = match.group(1).strip()
        metadata_str = match.group(2) if match.group(2) else ''
        description = match.group(3).strip()

        # Parse metadata
        priority = i  # Default priority based on order
        keywords = []

        if metadata_str:
            # Extract priority
            priority_match = re.search(r'priority:(\d+)', metadata_str)
            if priority_match:
                priority = int(priority_match.group(1))

            # Extract keywords
            keywords_match = re.search(r'keywords:([^,\]]+(?:,[^,\]]+)*)', metadata_str)
            if keywords_match:
                keywords = [k.strip() for k in keywords_match.group(1).split(',')]

        # Full text for bullet point
        full_text = f"{title}. {description}" if description else title

        bullets.append({
            'title': title,
            'description': description,
            'text': full_text,
            'priority': priority,
            'keywords': keywords
        })

    return bullets


def load_all_experiences(experiences_dir: str) -> List[Dict[str, Any]]:
    """
    Load all experience files from a directory.

    Args:
        experiences_dir: Path to experiences directory

    Returns:
        List of experience dictionaries
    """
    experiences = []

    if not os.path.exists(experiences_dir):
        return experiences

    for filename in os.listdir(experiences_dir):
        if filename.endswith('.md'):
            file_path = os.path.join(experiences_dir, filename)
            try:
                exp = parse_experience_file(file_path)
                experiences.append(exp)
            except Exception as e:
                print(f"Warning: Could not parse {filename}: {e}")

    # Sort by priority (lower number = higher priority)
    experiences.sort(key=lambda x: x.get('priority', 999))

    return experiences


def load_skills_file(skills_file: str) -> List[Dict[str, Any]]:
    """
    Load skills from a markdown file.

    Args:
        skills_file: Path to skills markdown file

    Returns:
        List of skill categories
    """
    if not os.path.exists(skills_file):
        return []

    with open(skills_file, 'r', encoding='utf-8') as f:
        post = frontmatter.load(f)

    # Parse skills from content
    skills = []
    current_category = None
    current_keywords = []

    for line in post.content.split('\n'):
        line = line.strip()

        # Section headers become categories
        if line.startswith('##'):
            if current_category and current_keywords:
                skills.append({
                    'category': current_category,
                    'keywords': current_keywords
                })

            current_category = line.lstrip('#').strip()
            current_keywords = []

        # List items become keywords
        elif line.startswith('-') or line.startswith('*'):
            keyword = line.lstrip('-*').strip()
            if keyword:
                current_keywords.append(keyword)

    # Add last category
    if current_category and current_keywords:
        skills.append({
            'category': current_category,
            'keywords': current_keywords
        })

    return skills


def parse_project_file(file_path: str) -> Dict[str, Any]:
    """
    Parse a project markdown file with frontmatter.

    Args:
        file_path: Path to the project markdown file

    Returns:
        Dictionary with project data
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        post = frontmatter.load(f)

    data = dict(post.metadata)
    data['description'] = post.content.strip()
    data['slug'] = os.path.splitext(os.path.basename(file_path))[0]

    return data


def format_date(date_str: str) -> str:
    """
    Format date string for resume display.

    Converts YYYY-MM-DD to "Month YYYY" format.

    Args:
        date_str: Date string (YYYY-MM-DD or already formatted)

    Returns:
        Formatted date string
    """
    if not date_str or date_str.lower() == 'present':
        return date_str

    # If already formatted, return as-is
    if '-' not in date_str:
        return date_str

    # Parse YYYY-MM-DD
    try:
        from datetime import datetime
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%B %Y')
    except:
        return date_str
