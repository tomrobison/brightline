#!/usr/bin/env python3
"""
Analyze job description and extract keywords/requirements.

Usage:
    python analyze_job.py --job-description jobs/example/job-description.md \
                         --base-resume source/base-resume.yaml \
                         --output jobs/example/keywords.yaml
"""

import argparse
import os
import yaml
import re
from datetime import datetime
from utils.keyword_matcher import extract_keywords_from_text, calculate_match_score, normalize_keyword
from utils.markdown_parser import load_all_experiences


def parse_job_description(file_path):
    """
    Parse job description markdown file and extract structured data.

    Returns:
        Dictionary with job details and requirements
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract basic info from filename or content
    job_data = {
        'title': '',
        'company': '',
        'location': '',
        'text': content
    }

    # Look for common job posting patterns
    lines = content.split('\n')
    for line in lines[:10]:
        if any(word in line.lower() for word in ['position:', 'role:', 'title:']):
            job_data['title'] = line.split(':', 1)[1].strip() if ':' in line else line

    return job_data


def extract_required_vs_preferred(text):
    """
    Identify required vs. preferred qualifications from job description.

    Returns:
        Tuple of (required_keywords, preferred_keywords)
    """
    required_keywords = []
    preferred_keywords = []

    # Split into sections
    text_lower = text.lower()

    # Find required section
    required_patterns = [
        r'required[^\n]*:(.+?)(?=preferred|nice to have|bonus|\Z)',
        r'requirements[^\n]*:(.+?)(?=preferred|nice to have|bonus|\Z)',
        r'minimum qualifications[^\n]*:(.+?)(?=preferred|nice to have|bonus|\Z)',
        r'must have[^\n]*:(.+?)(?=preferred|nice to have|bonus|\Z)'
    ]

    required_text = ''
    for pattern in required_patterns:
        match = re.search(pattern, text_lower, re.DOTALL | re.IGNORECASE)
        if match:
            required_text = match.group(1)
            break

    # Find preferred section
    preferred_patterns = [
        r'preferred[^\n]*:(.+?)(?=\n#{1,3}\s|\Z)',
        r'nice to have[^\n]*:(.+?)(?=\n#{1,3}\s|\Z)',
        r'bonus[^\n]*:(.+?)(?=\n#{1,3}\s|\Z)',
        r'desired[^\n]*:(.+?)(?=\n#{1,3}\s|\Z)'
    ]

    preferred_text = ''
    for pattern in preferred_patterns:
        match = re.search(pattern, text_lower, re.DOTALL | re.IGNORECASE)
        if match:
            preferred_text = match.group(1)
            break

    # Extract keywords from each section
    if required_text:
        required_keywords = [kw for kw, _ in extract_keywords_from_text(required_text, min_frequency=1)[:20]]

    if preferred_text:
        preferred_keywords = [kw for kw, _ in extract_keywords_from_text(preferred_text, min_frequency=1)[:15]]

    # If no clear sections, use frequency analysis on full text
    if not required_keywords:
        all_keywords = extract_keywords_from_text(text, min_frequency=2)
        # Top 15 are "required", next 10 are "preferred"
        required_keywords = [kw for kw, _ in all_keywords[:15]]
        preferred_keywords = [kw for kw, _ in all_keywords[15:25]]

    return required_keywords, preferred_keywords


def categorize_keywords(keywords, text):
    """
    Categorize keywords into technical, soft skills, etc.

    Returns:
        Dictionary with categorized keywords
    """
    tech_keywords = []
    soft_keywords = []
    industry_keywords = []

    # Common technical indicators
    tech_patterns = [
        r'\b(python|java|javascript|ruby|go|rust|c\+\+|typescript|sql|html|css)\b',
        r'\b(aws|gcp|azure|docker|kubernetes|jenkins|git)\b',
        r'\b(react|angular|vue|django|flask|spring|rails)\b',
        r'\b(api|rest|graphql|microservices|database|frontend|backend)\b'
    ]

    # Common soft skill indicators
    soft_patterns = [
        r'\b(leadership|communication|collaboration|teamwork|mentoring)\b',
        r'\b(problem-solving|analytical|creative|organized|detail-oriented)\b',
        r'\b(agile|scrum|management|planning|strategy)\b'
    ]

    text_lower = text.lower()

    for keyword in keywords:
        keyword_lower = keyword.lower()

        # Check if technical
        if any(re.search(pattern, keyword_lower, re.IGNORECASE) for pattern in tech_patterns):
            tech_keywords.append(keyword)
        # Check if soft skill
        elif any(re.search(pattern, keyword_lower, re.IGNORECASE) for pattern in soft_patterns):
            soft_keywords.append(keyword)
        else:
            industry_keywords.append(keyword)

    return {
        'technical_skills': tech_keywords,
        'soft_skills': soft_keywords,
        'industry_terms': industry_keywords
    }


def analyze_match_against_resume(keywords, base_resume_path, experiences_dir):
    """
    Analyze how well current resume matches job requirements.

    Returns:
        Match analysis dictionary
    """
    # Load base resume
    with open(base_resume_path, 'r') as f:
        base_resume = yaml.safe_load(f)

    # Load experiences
    experiences = load_all_experiences(experiences_dir)

    # Build resume text
    resume_parts = []

    # Add basics
    basics = base_resume.get('basics', {})
    if basics.get('summary'):
        resume_parts.append(basics['summary'])

    # Add experience content
    for exp in experiences:
        resume_parts.append(exp.get('company', ''))
        resume_parts.append(exp.get('position', ''))
        resume_parts.append(exp.get('content', ''))

    # Add skills
    for skill_cat in base_resume.get('skills', []):
        resume_parts.extend(skill_cat.get('keywords', []))

    resume_text = '\n'.join(resume_parts)

    # Calculate match
    required = keywords.get('required', [])
    preferred = keywords.get('preferred', [])

    match_result = calculate_match_score(resume_text, required, preferred)

    # Add experience-level matching
    exp_matches = []
    for exp in experiences:
        exp_text = f"{exp.get('company', '')} {exp.get('position', '')} {exp.get('content', '')}"
        exp_score = calculate_match_score(exp_text, required, preferred)

        exp_matches.append({
            'slug': exp.get('slug'),
            'company': exp.get('company'),
            'score': exp_score['overall_score'],
            'matched_keywords': exp_score['required_matched'][:5]
        })

    # Sort by score
    exp_matches.sort(key=lambda x: x['score'], reverse=True)
    match_result['experience_matches'] = exp_matches[:5]

    return match_result


def generate_tailoring_recommendations(match_analysis, experiences):
    """
    Generate intelligent recommendations for resume tailoring.

    Returns:
        Recommendations dictionary
    """
    recommendations = {
        'summary': '',
        'experiences_to_include': [],
        'emphasis': [],
        'target_length': '2-page',
        'notes': []
    }

    # Recommend experiences based on match scores
    for exp_match in match_analysis.get('experience_matches', [])[:4]:
        recommendations['experiences_to_include'].append({
            'slug': exp_match['slug'],
            'version': 'detailed' if exp_match['score'] > 70 else 'standard',
            'reason': f"High keyword match ({exp_match['score']}%)"
        })

    # Recommend keyword emphasis
    matched = match_analysis.get('required_matched', [])
    recommendations['emphasis'] = matched[:5]

    # Notes on missing keywords
    missing = match_analysis.get('required_missing', [])
    if missing:
        recommendations['notes'].append(
            f"Consider emphasizing: {', '.join(missing[:3])}"
        )

    # Overall match assessment
    overall_score = match_analysis.get('overall_score', 0)
    if overall_score >= 80:
        recommendations['summary'] = "Strong match - emphasize relevant experiences"
    elif overall_score >= 60:
        recommendations['summary'] = "Good match - highlight key technical skills"
    else:
        recommendations['summary'] = "Moderate match - focus on transferable skills"

    return recommendations


def create_initial_config(job_data, keywords, recommendations, output_path):
    """
    Create initial tailoring-config.yaml file.
    """
    config = {
        'job': {
            'company': job_data.get('company', 'Company Name'),
            'position': job_data.get('title', 'Position'),
            'application_date': datetime.now().strftime('%Y-%m-%d')
        },
        'resume': {
            'version': 'senior-engineer',
            'length': recommendations.get('target_length', '2-page'),
            'summary': '# Customize this summary for the specific role'
        },
        'keywords': {
            'required': keywords.get('required', [])[:10],
            'preferred': keywords.get('preferred', [])[:8],
            'industry_terms': []
        },
        'selection': {
            'experiences': recommendations.get('experiences_to_include', []),
            'projects': [],
            'skills': {
                'priority_categories': [],
                'highlight_keywords': recommendations.get('emphasis', [])
            }
        },
        'optimization': {
            'target_match_score': 85,
            'max_pages': 2,
            'bullet_point_strategy': 'keyword-dense',
            'constraints': {
                'max_bullets_per_experience': 5,
                'max_experiences': 4,
                'max_projects': 3
            }
        }
    }

    with open(output_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)

    print(f"✓ Created tailoring config: {output_path}")


def main():
    parser = argparse.ArgumentParser(description='Analyze job description')
    parser.add_argument('--job-description', required=True, help='Job description markdown file')
    parser.add_argument('--base-resume', required=True, help='Base resume YAML file')
    parser.add_argument('--experiences-dir', default='data/experiences', help='Experiences directory')
    parser.add_argument('--output-dir', required=True, help='Output directory for job files')

    args = parser.parse_args()

    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)

    print(f"Analyzing job description: {args.job_description}")
    job_data = parse_job_description(args.job_description)

    print("Extracting keywords and requirements...")
    required_kw, preferred_kw = extract_required_vs_preferred(job_data['text'])

    print(f"Found {len(required_kw)} required and {len(preferred_kw)} preferred keywords")

    # Categorize keywords
    all_keywords = required_kw + preferred_kw
    categorized = categorize_keywords(all_keywords, job_data['text'])

    print("Analyzing match against current resume...")
    experiences = load_all_experiences(args.experiences_dir)

    keywords_dict = {
        'required': required_kw,
        'preferred': preferred_kw
    }

    match_analysis = analyze_match_against_resume(
        keywords_dict,
        args.base_resume,
        args.experiences_dir
    )

    print(f"\n✓ Overall Match Score: {match_analysis['overall_score']}%")
    print(f"  - Required keywords: {match_analysis['required_score']}%")
    print(f"  - Preferred keywords: {match_analysis['preferred_score']}%")

    print("\nGenerating tailoring recommendations...")
    recommendations = generate_tailoring_recommendations(match_analysis, experiences)

    # Save outputs
    keywords_output = os.path.join(args.output_dir, 'keywords.yaml')
    keywords_data = {
        'job_title': job_data.get('title', 'Position'),
        'company': job_data.get('company', 'Company'),
        'analyzed_date': datetime.now().strftime('%Y-%m-%d'),
        'keywords': {
            'technical_skills': [
                {'keyword': kw, 'priority': 'required' if kw in required_kw else 'preferred'}
                for kw in categorized['technical_skills']
            ],
            'soft_skills': [
                {'keyword': kw, 'priority': 'required' if kw in required_kw else 'preferred'}
                for kw in categorized['soft_skills']
            ]
        },
        'match_analysis': match_analysis
    }

    with open(keywords_output, 'w') as f:
        yaml.dump(keywords_data, f, default_flow_style=False, sort_keys=False)

    print(f"✓ Saved keyword analysis: {keywords_output}")

    # Create initial config
    config_output = os.path.join(args.output_dir, 'tailoring-config.yaml')
    create_initial_config(job_data, keywords_dict, recommendations, config_output)

    print("\n✓ Analysis complete!")
    print(f"\nRecommendations:")
    for note in recommendations.get('notes', []):
        print(f"  - {note}")

    print(f"\nNext steps:")
    print(f"1. Review and customize: {config_output}")
    print(f"2. Update the summary section for this specific role")
    print(f"3. Run tailor_resume.py to generate the tailored resume")


if __name__ == '__main__':
    main()
