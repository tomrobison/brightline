---
name: compare-versions
description: |
  Compare multiple tailored resume versions side-by-side, showing differences
  in content, keywords, and optimization choices. Use when: (1) Comparing
  resumes for different job applications, (2) A/B testing resume variations,
  (3) Understanding tailoring decisions across versions.
---

## Purpose

Provide side-by-side comparison of different resume versions to help understand tailoring decisions and optimize strategy.

## Process

When this skill is invoked, analyze and compare resume versions:

1. **Identify versions to compare**:
   - List available job configurations in `jobs/`
   - Ask user which versions to compare (2-3 versions recommended)
   - Load the corresponding `tailoring-config.yaml` and `keywords.yaml` files

2. **Analyze each version**:
   For each selected job:
   - Load the tailoring configuration
   - Read keyword analysis results
   - Identify selected experiences and bullet counts
   - Note target length and customizations

3. **Generate comparison**:
   Create a side-by-side comparison showing:
   - Job details (company, position)
   - Keyword match scores
   - Resume length targets
   - Experiences included (and versions used)
   - Skills emphasized
   - Summary customizations

4. **Highlight key differences**:
   - Which experiences appear in which versions
   - Keyword emphasis differences
   - Length optimization strategies
   - Match score variations

5. **Provide insights**:
   - Identify patterns (e.g., "Tech lead roles emphasize leadership keywords")
   - Suggest optimizations based on successful versions
   - Note which experiences are most versatile

## Interactive Prompts

Ask the user:
- "Which resume versions would you like to compare?" (show list)
- "I can compare up to 3 versions at once. Select 2-3 jobs."
- After comparison: "Version A emphasizes [X], while Version B emphasizes [Y]. Do you want to adopt any strategies from one version to another?"
- "Based on the comparison, would you like me to suggest improvements to any of these versions?"

## Comparison Report Format

Generate a report like this:

```markdown
## Resume Version Comparison

### Version A: [Company] - [Position]
- **Match Score**: [X]%
- **Target Length**: [N]-page
- **Experiences**: [List with versions]
- **Top Keywords**: [Top 5]
- **Summary Focus**: [Brief description]

### Version B: [Company] - [Position]
- **Match Score**: [Y]%
- **Target Length**: [N]-page
- **Experiences**: [List with versions]
- **Top Keywords**: [Top 5]
- **Summary Focus**: [Brief description]

---

## Key Differences

**Experiences**:
- Both include: [Common experiences]
- A only: [Unique to A]
- B only: [Unique to B]

**Keywords**:
- A emphasizes: [Keywords unique or stronger in A]
- B emphasizes: [Keywords unique or stronger in B]

**Strategy**:
- Version A: [Characterize the approach]
- Version B: [Characterize the approach]

---

## Insights

- [Observation 1]
- [Observation 2]
- [Suggestion for improvement]
```

## Use Cases

1. **Cross-role comparison**: Compare tech lead vs. senior engineer roles
2. **Same role, different companies**: See what varies across similar positions
3. **Optimization learning**: Understand which strategies work best
4. **Template development**: Identify experiences that work across multiple roles

## Validation

After comparison:
- Report is clear and actionable
- Differences are highlighted
- User understands the strategic choices in each version
- Insights are relevant and helpful

## Tips for Users

Share these insights:
- **Versatile experiences**: Experiences that appear across multiple versions are your strongest
- **Keyword clusters**: Notice patterns in which keywords go together for certain roles
- **Match score patterns**: Higher scores don't always mean better - ensure the right keywords match
- **Length trade-offs**: Compare what gets condensed and whether it impacts the message
