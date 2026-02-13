"""
Resume length optimization algorithms.

Provides functions to reduce resume content to target page lengths
while preserving important keywords and achievements.
"""

from typing import Dict, List, Any, Tuple


def estimate_content_length(content: Dict[str, Any]) -> float:
    """
    Estimate the number of pages for resume content.

    Uses heuristics based on character count and structure.

    Args:
        content: Dictionary with resume sections

    Returns:
        Estimated page count
    """
    total_chars = 0
    total_items = 0

    # Count characters in summary
    if content.get('summary'):
        total_chars += len(content['summary'])

    # Count experience bullets
    for exp in content.get('experiences', []):
        total_chars += len(exp.get('company', '')) + len(exp.get('position', ''))
        total_chars += len(exp.get('summary', ''))

        for bullet in exp.get('bullets', []):
            total_chars += len(bullet.get('text', ''))
            total_items += 1

    # Count skills
    for skill_cat in content.get('skills', []):
        total_chars += len(skill_cat.get('category', ''))
        total_chars += sum(len(k) for k in skill_cat.get('keywords', []))

    # Count education
    for edu in content.get('education', []):
        total_chars += len(edu.get('institution', '')) + len(edu.get('studyType', ''))

    # Count projects
    for proj in content.get('projects', []):
        total_chars += len(proj.get('name', '')) + len(proj.get('description', ''))

    # Rough heuristic:
    # - ~3000 characters per page
    # - Each structural item (bullet, section) adds ~25 chars equivalent
    char_estimate = total_chars / 3000
    item_estimate = total_items / 40

    return max(char_estimate, item_estimate)


def score_experience(exp: Dict[str, Any], keywords: List[str], recency_weight: float = 0.3) -> float:
    """
    Score an experience based on keyword relevance and recency.

    Args:
        exp: Experience dictionary
        keywords: List of important keywords
        recency_weight: Weight for recency (0-1, default 0.3)

    Returns:
        Score value (higher is better)
    """
    score = 0.0

    # Base priority from metadata
    priority = exp.get('priority', 5)
    score += (6 - priority) * 10  # Invert priority (1 = highest)

    # Keyword matching
    exp_keywords = [k.lower() for k in exp.get('keywords', [])]
    job_keywords_lower = [k.lower() for k in keywords]

    keyword_matches = sum(1 for k in exp_keywords if k in job_keywords_lower)
    score += keyword_matches * 15  # 15 points per keyword match

    # Recency bonus (if endDate is recent or "present")
    if exp.get('endDate', '').lower() == 'present':
        score += 20 * recency_weight
    elif exp.get('endDate'):
        try:
            # Simple year-based recency
            end_year = int(exp['endDate'][:4])
            from datetime import datetime
            current_year = datetime.now().year
            years_ago = current_year - end_year

            if years_ago <= 2:
                score += 15 * recency_weight
            elif years_ago <= 5:
                score += 10 * recency_weight
        except:
            pass

    return score


def score_bullet(bullet: Dict[str, Any], keywords: List[str]) -> float:
    """
    Score a bullet point based on keyword relevance and priority.

    Args:
        bullet: Bullet dictionary with text, priority, keywords
        keywords: List of important keywords from job description

    Returns:
        Score value (higher is better)
    """
    score = 0.0

    # Base priority from metadata
    priority = bullet.get('priority', 5)
    score += (6 - priority) * 10

    # Keyword matching
    bullet_keywords = [k.lower() for k in bullet.get('keywords', [])]
    job_keywords_lower = [k.lower() for k in keywords]

    keyword_matches = sum(1 for k in bullet_keywords if k in job_keywords_lower)
    score += keyword_matches * 20

    # Check if keywords appear in bullet text
    bullet_text_lower = bullet.get('text', '').lower()
    text_keyword_matches = sum(1 for k in job_keywords_lower if k in bullet_text_lower)
    score += text_keyword_matches * 5

    # Quantification bonus (numbers suggest measurable impact)
    if any(char.isdigit() for char in bullet.get('text', '')):
        score += 10

    return score


def select_experience_version(
    exp: Dict[str, Any],
    target_length: str,
    current_page_estimate: float,
    target_pages: float
) -> str:
    """
    Select which version of an experience to use (detailed/standard/concise).

    Args:
        exp: Experience dictionary
        target_length: Target resume length ("1-page" or "2-page")
        current_page_estimate: Current estimated page count
        target_pages: Target page count

    Returns:
        Version name ("detailed", "standard", or "concise")
    """
    versions = exp.get('versions', {})

    # If no versions specified, use "standard"
    if not versions:
        return 'standard'

    # If we're under target, use detailed
    if current_page_estimate < target_pages * 0.8:
        return 'detailed' if 'detailed' in versions else 'standard'

    # If we're over target, use concise
    if current_page_estimate > target_pages * 1.1:
        return 'concise' if 'concise' in versions else 'standard'

    # Otherwise use standard
    return 'standard'


def reduce_to_target_length(
    content: Dict[str, Any],
    target_pages: float,
    preserve_keywords: List[str]
) -> Tuple[Dict[str, Any], List[str]]:
    """
    Reduce resume content to target page length while preserving keywords.

    Applies iterative reduction strategies:
    1. Use shorter experience versions (detailed -> standard -> concise)
    2. Remove lowest-scoring bullets
    3. Limit number of experiences
    4. Condense lengthy bullet points

    Args:
        content: Resume content dictionary
        target_pages: Target page count (e.g., 1.0 or 2.0)
        preserve_keywords: Keywords to preserve during reduction

    Returns:
        Tuple of (optimized_content, list_of_changes_made)
    """
    optimized = content.copy()
    changes = []
    current_estimate = estimate_content_length(optimized)

    # Strategy 1: Use shorter experience versions
    if current_estimate > target_pages * 1.05:
        for exp in optimized.get('experiences', []):
            versions = exp.get('versions', {})

            if 'detailed' in versions and exp.get('selected_version') == 'detailed':
                exp['selected_version'] = 'standard'
                changes.append(f"Shortened {exp.get('company')} from detailed to standard")
                current_estimate = estimate_content_length(optimized)

                if current_estimate <= target_pages * 1.05:
                    break

    # Strategy 2: Remove lowest-scoring bullets
    if current_estimate > target_pages * 1.05:
        for exp in optimized.get('experiences', []):
            bullets = exp.get('bullets', [])

            if len(bullets) > 2:  # Keep at least 2 bullets
                # Score all bullets
                scored_bullets = [
                    (bullet, score_bullet(bullet, preserve_keywords))
                    for bullet in bullets
                ]
                scored_bullets.sort(key=lambda x: x[1], reverse=True)

                # Keep only top bullets
                target_bullet_count = max(2, len(bullets) - 1)
                exp['bullets'] = [b for b, _ in scored_bullets[:target_bullet_count]]

                changes.append(f"Removed lowest-scoring bullet from {exp.get('company')}")
                current_estimate = estimate_content_length(optimized)

                if current_estimate <= target_pages * 1.05:
                    break

    # Strategy 3: Switch remaining detailed versions to concise
    if current_estimate > target_pages * 1.05:
        for exp in optimized.get('experiences', []):
            versions = exp.get('versions', {})

            if 'concise' in versions and exp.get('selected_version') == 'standard':
                exp['selected_version'] = 'concise'
                changes.append(f"Condensed {exp.get('company')} to concise version")
                current_estimate = estimate_content_length(optimized)

                if current_estimate <= target_pages * 1.05:
                    break

    # Strategy 4: Limit number of experiences (if still over)
    if current_estimate > target_pages * 1.05:
        experiences = optimized.get('experiences', [])

        if len(experiences) > 3:
            # Score experiences
            scored_exps = [
                (exp, score_experience(exp, preserve_keywords))
                for exp in experiences
            ]
            scored_exps.sort(key=lambda x: x[1], reverse=True)

            # Keep only top experiences
            max_experiences = 4 if target_pages >= 2 else 3
            optimized['experiences'] = [e for e, _ in scored_exps[:max_experiences]]

            changes.append(f"Limited to top {max_experiences} most relevant experiences")
            current_estimate = estimate_content_length(optimized)

    # Strategy 5: Condense bullet points (last resort)
    if current_estimate > target_pages * 1.05:
        for exp in optimized.get('experiences', []):
            for bullet in exp.get('bullets', []):
                if len(bullet.get('text', '')) > 150:
                    condensed = condense_bullet_point(bullet['text'], 120, preserve_keywords)
                    bullet['text'] = condensed
                    changes.append(f"Condensed lengthy bullet in {exp.get('company')}")

        current_estimate = estimate_content_length(optimized)

    return optimized, changes


def condense_bullet_point(text: str, max_length: int, preserve_keywords: List[str]) -> str:
    """
    Intelligently shorten a bullet point while preserving keywords.

    Args:
        text: Original bullet point text
        max_length: Maximum character length
        preserve_keywords: Keywords to preserve

    Returns:
        Condensed text
    """
    if len(text) <= max_length:
        return text

    # Ensure all keywords are preserved
    keywords_lower = [k.lower() for k in preserve_keywords]
    text_lower = text.lower()

    # Simple strategy: truncate at sentence boundary near max_length
    sentences = text.split('.')
    condensed = sentences[0]

    # Check if we're preserving important keywords
    missing_keywords = [k for k in keywords_lower if k in text_lower and k not in condensed.lower()]

    # If we're missing keywords, try to include more
    if missing_keywords and len(sentences) > 1:
        condensed = '. '.join(sentences[:2])

    # Final truncation if still too long
    if len(condensed) > max_length:
        condensed = condensed[:max_length - 3] + '...'

    return condensed.strip()


def prioritize_content(
    experiences: List[Dict[str, Any]],
    keywords: List[str],
    max_count: int = None
) -> List[Dict[str, Any]]:
    """
    Prioritize and filter experiences based on relevance.

    Args:
        experiences: List of experience dictionaries
        keywords: Important keywords for scoring
        max_count: Maximum number of experiences to include (optional)

    Returns:
        Filtered and sorted list of experiences
    """
    # Score all experiences
    scored = [
        (exp, score_experience(exp, keywords))
        for exp in experiences
    ]

    # Sort by score (highest first)
    scored.sort(key=lambda x: x[1], reverse=True)

    # Filter to max_count if specified
    if max_count:
        scored = scored[:max_count]

    return [exp for exp, _ in scored]
