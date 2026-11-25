---
name: case-study-writer
description: Generate case study HTML pages for portfolio projects. Use when creating new case studies or updating existing ones in case-studies/ directory.
---

# Case Study Writer

## Required Sections

Every case study must include:

1. **Impact metrics** - Quantified outcomes with business translation
2. **Problem** - Business problem (not technical)
3. **Solution** - Technical approach + business justification
4. **Architecture** - High-level diagram or description (optional)
5. **Key engineering highlights** - 4-5 bullets with action verbs + outcomes
6. **Tech stack** - Grouped by category
7. **CTA** - Contact + CV download

## Business Value Translation

Always translate metrics:

| Technical | Business |
|-----------|----------|
| 40% downtime reduction | £X annual cost avoidance |
| 94% query success | Decision time: 12min → 30sec |
| 20% infra savings | £X/year optimization |

## File Naming

- Use kebab-case: `client-name-project.html`
- Location: `case-studies/`

## Template

See [template.html](template.html) for the full HTML structure.

After creating, remind to add link in `index.html` project section.
