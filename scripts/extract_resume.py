#!/usr/bin/env python3
"""
Extract structured data from DOCX resume file.

Usage:
    python extract_resume.py --input source/resume.docx \
                            --output-base source/base-resume.yaml \
                            --output-experiences data/experiences/
"""

import argparse
import os
import re
import yaml
from datetime import datetime
from utils.docx_handler import read_docx_paragraphs


def identify_sections(paragraphs):
    """
    Identify major resume sections from paragraphs.

    Returns:
        Dictionary mapping section names to paragraph indices
    """
    sections = {}
    current_section = None

    common_headers = [
        'experience', 'work experience', 'employment', 'professional experience',
        'education', 'skills', 'technical skills', 'projects', 'certifications',
        'summary', 'objective', 'profile'
    ]

    for i, para in enumerate(paragraphs):
        text = para['text'].strip().lower()

        # Check if this looks like a section header
        if text and len(text) < 50:
            for header in common_headers:
                if header in text:
                    section_name = header.replace(' ', '_')
                    sections[section_name] = {'start': i, 'end': None}

                    # Close previous section
                    if current_section and sections[current_section]['end'] is None:
                        sections[current_section]['end'] = i - 1

                    current_section = section_name
                    break

    # Close last section
    if current_section and sections[current_section]['end'] is None:
        sections[current_section]['end'] = len(paragraphs) - 1

    return sections


def extract_contact_info(paragraphs):
    """
    Extract contact information from top of resume.

    Returns:
        Dictionary with name, email, phone, location, etc.
    """
    basics = {}

    # Look in first 10 paragraphs for contact info
    contact_text = '\n'.join([p['text'] for p in paragraphs[:10]])

    # Extract email
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', contact_text)
    if email_match:
        basics['email'] = email_match.group(0)

    # Extract phone
    phone_match = re.search(r'[\(]?\d{3}[\)]?[-.\s]?\d{3}[-.\s]?\d{4}', contact_text)
    if phone_match:
        basics['phone'] = phone_match.group(0)

    # Extract name (usually first non-empty paragraph)
    for para in paragraphs[:5]:
        text = para['text'].strip()
        if text and len(text) < 100 and not '@' in text:
            # Check if it looks like a name (2-4 words, capitalized)
            words = text.split()
            if 2 <= len(words) <= 4 and all(w[0].isupper() for w in words if w):
                basics['name'] = text
                break

    # Extract LinkedIn/URL
    url_match = re.search(r'https?://[^\s]+', contact_text)
    if url_match:
        url = url_match.group(0)
        if 'linkedin.com' in url.lower():
            basics['profiles'] = [{'network': 'LinkedIn', 'url': url}]
        else:
            basics['url'] = url

    return basics


def extract_experiences(paragraphs, section_range):
    """
    Extract work experience entries from section.

    Returns:
        List of experience dictionaries
    """
    experiences = []

    if not section_range:
        return experiences

    start_idx = section_range['start'] + 1  # Skip header
    end_idx = section_range['end']

    current_exp = None
    current_bullets = []

    for i in range(start_idx, end_idx + 1):
        if i >= len(paragraphs):
            break

        para = paragraphs[i]
        text = para['text'].strip()

        if not text:
            # Empty paragraph might signal end of experience
            if current_exp and current_bullets:
                current_exp['bullets'] = current_bullets
                experiences.append(current_exp)
                current_exp = None
                current_bullets = []
            continue

        # Check if this looks like a company/position header
        # Usually bold or larger font in first run
        is_header = False
        if para['runs']:
            first_run = para['runs'][0]
            if first_run.get('bold') or (first_run.get('font_size') and first_run['font_size'] > 11):
                is_header = True

        if is_header and not text.startswith('•') and not text.startswith('-'):
            # Save previous experience
            if current_exp and current_bullets:
                current_exp['bullets'] = current_bullets
                experiences.append(current_exp)

            # Start new experience
            # Try to parse company | position format
            if '|' in text:
                parts = [p.strip() for p in text.split('|')]
                current_exp = {
                    'position': parts[0],
                    'company': parts[1] if len(parts) > 1 else ''
                }
            else:
                current_exp = {
                    'position': text,
                    'company': ''
                }

            current_bullets = []

        elif text.startswith('•') or text.startswith('-') or para['style'] == 'List Bullet':
            # This is a bullet point
            bullet_text = text.lstrip('•-–— ').strip()
            if bullet_text:
                current_bullets.append(bullet_text)

        elif current_exp and not current_exp.get('dates'):
            # This might be the dates/location line
            # Look for date patterns
            if re.search(r'\d{4}', text) or 'present' in text.lower():
                current_exp['dates'] = text
            elif i == start_idx:
                # First line after company might be dates
                current_exp['dates'] = text

    # Save last experience
    if current_exp and current_bullets:
        current_exp['bullets'] = current_bullets
        experiences.append(current_exp)

    return experiences


def extract_skills(paragraphs, section_range):
    """
    Extract skills from section.

    Returns:
        List of skill categories
    """
    skills = []

    if not section_range:
        return skills

    start_idx = section_range['start'] + 1
    end_idx = section_range['end']

    # Collect all skills text
    skills_text = []
    for i in range(start_idx, end_idx + 1):
        if i < len(paragraphs):
            text = paragraphs[i]['text'].strip()
            if text:
                skills_text.append(text)

    # Parse skills (often comma-separated or bullet lists)
    all_skills = []
    for text in skills_text:
        # Split by common separators
        if ',' in text:
            all_skills.extend([s.strip() for s in text.split(',') if s.strip()])
        elif '|' in text:
            all_skills.extend([s.strip() for s in text.split('|') if s.strip()])
        elif text.startswith('•') or text.startswith('-'):
            all_skills.append(text.lstrip('•-–— ').strip())
        else:
            # Check if it's a category: keyword format
            if ':' in text:
                parts = text.split(':', 1)
                skills.append({
                    'category': parts[0].strip(),
                    'keywords': [k.strip() for k in parts[1].split(',') if k.strip()]
                })
            else:
                all_skills.append(text)

    # If no categories found, create default category
    if not skills and all_skills:
        skills.append({
            'category': 'Technical Skills',
            'keywords': all_skills
        })

    return skills


def extract_education(paragraphs, section_range):
    """
    Extract education entries from section.

    Returns:
        List of education dictionaries
    """
    education = []

    if not section_range:
        return education

    start_idx = section_range['start'] + 1
    end_idx = section_range['end']

    current_edu = None

    for i in range(start_idx, end_idx + 1):
        if i >= len(paragraphs):
            break

        para = paragraphs[i]
        text = para['text'].strip()

        if not text:
            if current_edu:
                education.append(current_edu)
                current_edu = None
            continue

        # Check if this is an institution/degree header
        is_header = False
        if para['runs'] and para['runs'][0].get('bold'):
            is_header = True

        if is_header:
            if current_edu:
                education.append(current_edu)

            current_edu = {
                'institution': text,
                'studyType': 'Bachelor',  # Default
                'area': ''
            }

        elif current_edu:
            # This might be additional info
            if re.search(r'\d{4}', text):
                current_edu['endDate'] = text
            elif 'gpa' in text.lower():
                gpa_match = re.search(r'(\d\.\d+)', text)
                if gpa_match:
                    current_edu['gpa'] = gpa_match.group(1)

    if current_edu:
        education.append(current_edu)

    return education


def create_base_resume_yaml(data, output_path):
    """
    Create base-resume.yaml file with extracted data.
    """
    base_resume = {
        'basics': data.get('basics', {}),
        'work': [],
        'skills': data.get('skills', []),
        'education': data.get('education', []),
        'projects': [],
        'metadata': {
            'default_length': '2-page',
            'highlight_skills': [],
            'versions': ['senior-engineer', 'tech-lead']
        }
    }

    # Add experience references
    for i, exp in enumerate(data.get('experiences', [])):
        slug = f"experience-{i+1}"
        base_resume['work'].append({
            'slug': slug,
            'company': exp.get('company', ''),
            'position': exp.get('position', '')
        })

    with open(output_path, 'w') as f:
        yaml.dump(base_resume, f, default_flow_style=False, sort_keys=False)

    print(f"✓ Created base resume: {output_path}")


def create_experience_files(experiences, output_dir):
    """
    Create individual markdown files for each experience.
    """
    os.makedirs(output_dir, exist_ok=True)

    for i, exp in enumerate(experiences):
        # Create slug from company name
        company = exp.get('company', f'company-{i+1}')
        slug = re.sub(r'[^a-z0-9]+', '-', company.lower()).strip('-')
        if not slug:
            slug = f'experience-{i+1}'

        file_path = os.path.join(output_dir, f'{slug}.md')

        # Create frontmatter
        frontmatter = {
            'company': exp.get('company', ''),
            'position': exp.get('position', ''),
            'location': '',
            'startDate': '',
            'endDate': 'present',
            'keywords': [],
            'relevant_for': ['senior-engineer'],
            'priority': i + 1,
            'versions': {
                'detailed': min(len(exp.get('bullets', [])), 5),
                'standard': min(len(exp.get('bullets', [])), 3),
                'concise': 2
            }
        }

        # Create content
        content = "## Summary\nBrief summary of role and impact.\n\n## Achievements\n\n"

        for j, bullet in enumerate(exp.get('bullets', []), 1):
            content += f"### {j}. Achievement Title [priority:{j}, keywords:]\n{bullet}\n\n"

        # Write file
        with open(file_path, 'w') as f:
            f.write('---\n')
            yaml.dump(frontmatter, f, default_flow_style=False, sort_keys=False)
            f.write('---\n\n')
            f.write(content)

        print(f"✓ Created experience: {file_path}")


def main():
    parser = argparse.ArgumentParser(description='Extract resume data from DOCX')
    parser.add_argument('--input', required=True, help='Input DOCX file path')
    parser.add_argument('--output-base', required=True, help='Output base-resume.yaml path')
    parser.add_argument('--output-experiences', required=True, help='Output experiences directory')

    args = parser.parse_args()

    print(f"Reading resume: {args.input}")
    paragraphs = read_docx_paragraphs(args.input)

    print("Identifying sections...")
    sections = identify_sections(paragraphs)
    print(f"Found sections: {', '.join(sections.keys())}")

    print("Extracting contact information...")
    basics = extract_contact_info(paragraphs)

    print("Extracting work experience...")
    experience_section = sections.get('experience') or sections.get('work_experience')
    experiences = extract_experiences(paragraphs, experience_section)
    print(f"Found {len(experiences)} experience entries")

    print("Extracting skills...")
    skills_section = sections.get('skills') or sections.get('technical_skills')
    skills = extract_skills(paragraphs, skills_section)

    print("Extracting education...")
    education_section = sections.get('education')
    education = extract_education(paragraphs, education_section)

    # Create output files
    data = {
        'basics': basics,
        'experiences': experiences,
        'skills': skills,
        'education': education
    }

    print("\nCreating output files...")
    create_base_resume_yaml(data, args.output_base)
    create_experience_files(experiences, args.output_experiences)

    print("\n✓ Extraction complete!")
    print(f"\nNext steps:")
    print(f"1. Review and enhance experience files in: {args.output_experiences}")
    print(f"2. Add keywords, priorities, and summaries to each experience")
    print(f"3. Update base-resume.yaml with your information")


if __name__ == '__main__':
    main()
