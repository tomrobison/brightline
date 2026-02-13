#!/usr/bin/env python3
"""
Main resume tailoring script - generates customized DOCX resume.

Usage:
    python tailor_resume.py --job-config jobs/example/tailoring-config.yaml \
                           --base-resume source/base-resume.yaml \
                           --experiences data/experiences/ \
                           --output output/example-company-2026-02.docx
"""

import argparse
import os
import yaml
from datetime import datetime
from utils.docx_handler import (
    create_ats_document, add_contact_header, add_section_header,
    add_experience_entry, add_skills_section, add_education_entry,
    add_project_entry, estimate_page_count, save_document
)
from utils.markdown_parser import (
    load_all_experiences, parse_experience_file, format_date
)
from utils.keyword_matcher import calculate_match_score
from utils.length_optimizer import (
    reduce_to_target_length, prioritize_content,
    select_experience_version, estimate_content_length
)


def load_config(config_path):
    """Load tailoring configuration from YAML file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def load_base_resume(base_path):
    """Load base resume data from YAML file."""
    with open(base_path, 'r') as f:
        return yaml.safe_load(f)


def select_and_load_experiences(config, experiences_dir, all_experiences):
    """
    Select and load experiences based on configuration.

    Returns:
        List of experience dictionaries with selected content
    """
    selection = config.get('selection', {})
    selected_exps = selection.get('experiences', [])

    if not selected_exps:
        # No explicit selection - use top experiences by priority
        return all_experiences[:4]

    loaded_experiences = []

    for exp_config in selected_exps:
        slug = exp_config.get('slug')
        version = exp_config.get('version', 'standard')

        # Find the experience
        exp = next((e for e in all_experiences if e.get('slug') == slug), None)

        if not exp:
            print(f"Warning: Experience '{slug}' not found")
            continue

        # Select appropriate bullets based on version
        versions = exp.get('versions', {})
        bullet_count = versions.get(version, 3)

        # Get bullets and sort by priority
        bullets = exp.get('bullets', [])
        bullets_sorted = sorted(bullets, key=lambda b: b.get('priority', 999))

        # Select top N bullets
        selected_bullets = bullets_sorted[:bullet_count]

        # Create experience entry
        exp_entry = {
            'company': exp.get('company'),
            'position': exp.get('position'),
            'location': exp.get('location'),
            'startDate': format_date(exp.get('startDate', '')),
            'endDate': format_date(exp.get('endDate', 'Present')),
            'summary': exp.get('content', '').split('## Summary')[1].split('##')[0].strip() if '## Summary' in exp.get('content', '') else '',
            'bullets': [b['text'] for b in selected_bullets],
            'selected_version': version
        }

        loaded_experiences.append(exp_entry)

    return loaded_experiences


def customize_summary(base_resume, config):
    """
    Customize professional summary for the specific job.

    Returns:
        Customized summary text
    """
    custom_summary = config.get('resume', {}).get('summary', '')

    if custom_summary and not custom_summary.startswith('#'):
        return custom_summary

    # Use base resume summary as fallback
    return base_resume.get('basics', {}).get('summary', '')


def filter_and_prioritize_skills(base_resume, config, keywords):
    """
    Filter and prioritize skills based on job requirements.

    Returns:
        List of skill categories, prioritized and filtered
    """
    all_skills = base_resume.get('skills', [])
    selection = config.get('selection', {}).get('skills', {})

    priority_categories = selection.get('priority_categories', [])
    highlight_keywords = selection.get('highlight_keywords', [])

    # If no priority specified, return all skills
    if not priority_categories:
        return all_skills

    # Reorder skills to put priority categories first
    prioritized = []
    remaining = []

    for skill_cat in all_skills:
        if skill_cat.get('category') in priority_categories:
            prioritized.append(skill_cat)
        else:
            remaining.append(skill_cat)

    return prioritized + remaining


def optimize_for_keywords(content, required_keywords, preferred_keywords):
    """
    Ensure required keywords are present and optimize distribution.

    Returns:
        Tuple of (optimized_content, keyword_coverage_report)
    """
    # Build resume text
    resume_parts = []

    if content.get('summary'):
        resume_parts.append(content['summary'])

    for exp in content.get('experiences', []):
        resume_parts.append(exp.get('company', ''))
        resume_parts.append(exp.get('position', ''))
        for bullet in exp.get('bullets', []):
            resume_parts.append(bullet)

    for skill_cat in content.get('skills', []):
        resume_parts.extend(skill_cat.get('keywords', []))

    resume_text = '\n'.join(resume_parts)

    # Calculate match
    match_result = calculate_match_score(resume_text, required_keywords, preferred_keywords)

    return content, match_result


def apply_length_optimization(content, config, keywords):
    """
    Apply length optimization to fit target page count.

    Returns:
        Tuple of (optimized_content, list_of_changes)
    """
    optimization = config.get('optimization', {})
    max_pages = optimization.get('max_pages', 2)

    # Get preserve keywords
    required_keywords = config.get('keywords', {}).get('required', [])

    # Estimate current length
    current_length = estimate_content_length(content)

    print(f"Current estimated length: {current_length:.1f} pages (target: {max_pages})")

    if current_length <= max_pages * 1.05:
        print("✓ Content within target length")
        return content, []

    print("Applying length optimization...")
    optimized, changes = reduce_to_target_length(content, max_pages, required_keywords)

    return optimized, changes


def generate_resume_docx(content, output_path):
    """
    Generate the final DOCX resume file.
    """
    doc = create_ats_document()

    # Add contact header
    basics = content.get('basics', {})
    add_contact_header(doc, basics)

    # Add summary/objective
    if content.get('summary'):
        add_section_header(doc, 'Professional Summary')
        summary_para = doc.add_paragraph(content['summary'])
        summary_para.runs[0].font.size = 10
        doc.add_paragraph()

    # Add experience section
    if content.get('experiences'):
        add_section_header(doc, 'Experience')
        for exp in content['experiences']:
            add_experience_entry(doc, exp)

    # Add skills section
    if content.get('skills'):
        add_section_header(doc, 'Skills')
        add_skills_section(doc, content['skills'])
        doc.add_paragraph()

    # Add projects section
    if content.get('projects'):
        add_section_header(doc, 'Projects')
        for project in content['projects']:
            add_project_entry(doc, project)
        doc.add_paragraph()

    # Add education section
    if content.get('education'):
        add_section_header(doc, 'Education')
        for edu in content['education']:
            add_education_entry(doc, edu)

    # Save document
    save_document(doc, output_path)

    # Estimate final page count
    final_estimate = estimate_page_count(doc)

    return final_estimate


def generate_report(match_result, length_changes, final_pages, config):
    """
    Generate a summary report of the tailoring process.
    """
    print("\n" + "="*60)
    print("RESUME TAILORING REPORT")
    print("="*60)

    job = config.get('job', {})
    print(f"\nJob: {job.get('position', 'N/A')} at {job.get('company', 'N/A')}")

    print(f"\nKeyword Match Score: {match_result['overall_score']}%")
    print(f"  - Required keywords: {match_result['required_score']}%")
    print(f"  - Preferred keywords: {match_result['preferred_score']}%")

    print(f"\nMatched Keywords ({len(match_result['required_matched'])}):")
    for kw in match_result['required_matched'][:10]:
        print(f"  ✓ {kw}")

    if match_result['required_missing']:
        print(f"\nMissing Keywords ({len(match_result['required_missing'])}):")
        for kw in match_result['required_missing'][:5]:
            print(f"  ✗ {kw}")

    print(f"\nFinal Resume Length: ~{final_pages:.1f} pages")

    if length_changes:
        print(f"\nOptimizations Applied:")
        for change in length_changes:
            print(f"  - {change}")

    target_score = config.get('optimization', {}).get('target_match_score', 85)
    if match_result['overall_score'] >= target_score:
        print(f"\n✓ Target match score achieved ({target_score}%)")
    else:
        print(f"\n⚠ Below target match score ({target_score}%)")
        print("  Consider emphasizing missing keywords")

    print("\n" + "="*60)


def main():
    parser = argparse.ArgumentParser(description='Generate tailored resume')
    parser.add_argument('--job-config', required=True, help='Job tailoring config YAML')
    parser.add_argument('--base-resume', required=True, help='Base resume YAML')
    parser.add_argument('--experiences-dir', default='data/experiences', help='Experiences directory')
    parser.add_argument('--output', required=True, help='Output DOCX file path')

    args = parser.parse_args()

    print("Loading configuration...")
    config = load_config(args.job_config)
    base_resume = load_base_resume(args.base_resume)

    print("Loading experiences...")
    all_experiences = load_all_experiences(args.experiences_dir)

    print("Selecting content based on configuration...")
    selected_experiences = select_and_load_experiences(config, args.experiences_dir, all_experiences)

    print(f"Selected {len(selected_experiences)} experiences")

    # Build content structure
    content = {
        'basics': base_resume.get('basics', {}),
        'summary': customize_summary(base_resume, config),
        'experiences': selected_experiences,
        'skills': filter_and_prioritize_skills(base_resume, config, config.get('keywords', {})),
        'projects': [],  # TODO: Add project selection
        'education': base_resume.get('education', [])
    }

    # Phase 1: Keyword Optimization
    print("\nPhase 1: Analyzing keyword match...")
    keywords = config.get('keywords', {})
    content, match_result = optimize_for_keywords(
        content,
        keywords.get('required', []),
        keywords.get('preferred', [])
    )

    # Phase 2: Length Optimization
    print("\nPhase 2: Optimizing length...")
    content, length_changes = apply_length_optimization(content, config, keywords)

    # Phase 3: Generate DOCX
    print("\nPhase 3: Generating DOCX resume...")
    final_pages = generate_resume_docx(content, args.output)

    # Generate report
    generate_report(match_result, length_changes, final_pages, config)

    print(f"\n✓ Resume generated: {args.output}")
    print("\nNext steps:")
    print("1. Review the generated DOCX file")
    print("2. Make manual adjustments if needed")
    print("3. If match score is low, update tailoring-config.yaml and regenerate")


if __name__ == '__main__':
    main()
