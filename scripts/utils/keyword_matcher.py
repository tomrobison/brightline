"""
Keyword matching and optimization algorithms for resume tailoring.
"""

import re
from typing import Dict, List, Tuple, Set
from collections import Counter


def normalize_keyword(keyword: str) -> List[str]:
    """
    Generate keyword variations for better matching.

    Returns variations including:
    - Original keyword
    - Lowercase version
    - Common acronyms and expansions
    - Plural forms

    Args:
        keyword: Keyword to normalize

    Returns:
        List of keyword variations
    """
    variations = [keyword, keyword.lower()]

    # Add plural forms
    if not keyword.endswith('s'):
        variations.append(keyword + 's')
        variations.append(keyword.lower() + 's')

    # Common tech acronym expansions
    acronym_map = {
        'AI': ['AI', 'Artificial Intelligence', 'A.I.'],
        'ML': ['ML', 'Machine Learning', 'M.L.'],
        'API': ['API', 'APIs', 'Application Programming Interface'],
        'CI/CD': ['CI/CD', 'CI', 'CD', 'Continuous Integration', 'Continuous Deployment'],
        'AWS': ['AWS', 'Amazon Web Services'],
        'GCP': ['GCP', 'Google Cloud Platform'],
        'SQL': ['SQL', 'Structured Query Language'],
        'REST': ['REST', 'RESTful', 'REST API'],
        'JS': ['JS', 'JavaScript'],
        'TS': ['TS', 'TypeScript'],
        'CSS': ['CSS', 'Cascading Style Sheets'],
        'HTML': ['HTML', 'HyperText Markup Language'],
    }

    keyword_upper = keyword.upper()
    if keyword_upper in acronym_map:
        variations.extend(acronym_map[keyword_upper])

    return list(set(variations))


def extract_keywords_from_text(text: str, min_frequency: int = 2) -> List[Tuple[str, int]]:
    """
    Extract important keywords from text using frequency analysis.

    Args:
        text: Input text to analyze
        min_frequency: Minimum frequency for a keyword to be included

    Returns:
        List of (keyword, frequency) tuples, sorted by frequency
    """
    # Convert to lowercase
    text_lower = text.lower()

    # Remove common stop words
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
        'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
        'should', 'could', 'may', 'might', 'must', 'can', 'this', 'that',
        'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
        'my', 'your', 'his', 'her', 'its', 'our', 'their'
    }

    # Extract words (including hyphenated words and acronyms)
    words = re.findall(r'\b[a-z][a-z0-9\-/+#]*\b', text_lower)

    # Filter stop words and short words
    filtered_words = [w for w in words if w not in stop_words and len(w) > 2]

    # Count frequencies
    word_freq = Counter(filtered_words)

    # Filter by minimum frequency and sort
    keywords = [(word, freq) for word, freq in word_freq.items() if freq >= min_frequency]
    keywords.sort(key=lambda x: x[1], reverse=True)

    return keywords


def calculate_match_score(
    resume_text: str,
    required_keywords: List[str],
    preferred_keywords: List[str] = None
) -> Dict[str, any]:
    """
    Calculate keyword match score between resume and job requirements.

    Args:
        resume_text: Full text of resume
        required_keywords: List of required keywords from job description
        preferred_keywords: List of preferred keywords from job description

    Returns:
        Dictionary with match analysis
    """
    if preferred_keywords is None:
        preferred_keywords = []

    resume_lower = resume_text.lower()

    # Check required keywords
    required_matched = []
    required_missing = []

    for keyword in required_keywords:
        variations = normalize_keyword(keyword)
        found = any(var.lower() in resume_lower for var in variations)

        if found:
            required_matched.append(keyword)
        else:
            required_missing.append(keyword)

    # Check preferred keywords
    preferred_matched = []
    preferred_missing = []

    for keyword in preferred_keywords:
        variations = normalize_keyword(keyword)
        found = any(var.lower() in resume_lower for var in variations)

        if found:
            preferred_matched.append(keyword)
        else:
            preferred_missing.append(keyword)

    # Calculate overall score
    # Required keywords: 70% weight, Preferred: 30% weight
    required_score = (len(required_matched) / len(required_keywords) * 100) if required_keywords else 100
    preferred_score = (len(preferred_matched) / len(preferred_keywords) * 100) if preferred_keywords else 100

    overall_score = (required_score * 0.7) + (preferred_score * 0.3)

    return {
        'overall_score': round(overall_score, 1),
        'required_score': round(required_score, 1),
        'preferred_score': round(preferred_score, 1),
        'required_matched': required_matched,
        'required_missing': required_missing,
        'preferred_matched': preferred_matched,
        'preferred_missing': preferred_missing,
        'total_required': len(required_keywords),
        'total_preferred': len(preferred_keywords)
    }


def find_keyword_contexts(text: str, keyword: str, context_chars: int = 50) -> List[str]:
    """
    Find all occurrences of a keyword with surrounding context.

    Args:
        text: Text to search
        keyword: Keyword to find
        context_chars: Number of characters of context on each side

    Returns:
        List of context snippets
    """
    contexts = []
    variations = normalize_keyword(keyword)

    for var in variations:
        pattern = re.compile(re.escape(var), re.IGNORECASE)

        for match in pattern.finditer(text):
            start = max(0, match.start() - context_chars)
            end = min(len(text), match.end() + context_chars)

            context = text[start:end].strip()
            contexts.append(f"...{context}...")

    return contexts[:5]  # Limit to 5 contexts


def suggest_keyword_placements(
    experiences: List[Dict],
    missing_keywords: List[str],
    max_suggestions: int = 5
) -> List[Dict[str, any]]:
    """
    Suggest where missing keywords could be naturally added.

    Args:
        experiences: List of experience dictionaries
        missing_keywords: Keywords not currently in resume
        max_suggestions: Maximum number of suggestions to return

    Returns:
        List of placement suggestions
    """
    suggestions = []

    for keyword in missing_keywords[:max_suggestions]:
        # Find experiences that might relate to this keyword
        keyword_lower = keyword.lower()

        for exp in experiences:
            exp_keywords = [k.lower() for k in exp.get('keywords', [])]

            # Check if experience is related to the missing keyword
            if any(kw in keyword_lower or keyword_lower in kw for kw in exp_keywords):
                suggestions.append({
                    'keyword': keyword,
                    'experience_slug': exp.get('slug'),
                    'company': exp.get('company'),
                    'position': exp.get('position'),
                    'reason': f"Experience uses related skills: {', '.join(exp.get('keywords', [])[:3])}"
                })
                break

    return suggestions


def optimize_keyword_distribution(
    sections: Dict[str, str],
    keywords: List[str],
    target_density: float = 0.02
) -> Dict[str, List[str]]:
    """
    Analyze keyword distribution across resume sections.

    Args:
        sections: Dictionary of section name -> text content
        keywords: List of important keywords
        target_density: Target keyword density (keywords per 100 words)

    Returns:
        Analysis of keyword distribution by section
    """
    analysis = {}

    for section_name, section_text in sections.items():
        word_count = len(section_text.split())
        found_keywords = []

        for keyword in keywords:
            variations = normalize_keyword(keyword)
            if any(var.lower() in section_text.lower() for var in variations):
                found_keywords.append(keyword)

        keyword_density = len(found_keywords) / word_count if word_count > 0 else 0

        analysis[section_name] = {
            'keywords': found_keywords,
            'keyword_count': len(found_keywords),
            'word_count': word_count,
            'density': round(keyword_density, 3),
            'meets_target': keyword_density >= target_density
        }

    return analysis
