---
name: resume-ats-optimizer
description: Optimize resumes for Applicant Tracking Systems, check ATS compatibility, and analyze keyword match
category: resume
---

# Resume ATS Optimizer

## When to Use This Skill

Use when the user wants to optimize their resume for ATS, check compatibility, or understand why applications get no response.

## Core Capabilities

- Parse resume and test ATS compatibility
- Extract and analyze keywords against job descriptions
- Identify formatting issues that break ATS parsers
- Calculate match scores between resume and job postings
- Suggest keyword additions and placements

## The ATS Problem

75% of resumes are rejected by ATS before a human sees them. Common failure reasons:
1. Poor formatting (tables, columns, headers/footers)
2. Missing keywords from job description
3. Inconsistent section headers
4. Non-standard fonts or special characters
5. Text embedded in images

## Compatibility Checklist

- Use .docx or .pdf (not .pages, .odt)
- PDF must be text-based, not scanned image
- Standard fonts: Arial, Calibri, Georgia, Times New Roman
- Font size: 10-12pt body, 14-16pt headers
- No text boxes, tables, or columns
- No headers/footers (contact info in body)
- No images, graphics, or charts
- Standard section headers (Experience, Education, Skills)

## Keyword Optimization Process

1. Extract keywords from job description (hard skills, soft skills, industry terms)
2. Match against resume
3. Calculate match score = (keywords matched / total required) x 100
4. Suggest placements: summary > skills section > experience bullets

## Analysis Output Format

Provide a structured report with:
- Overall score out of 100
- File format check
- Formatting issues list
- Keyword gap analysis
- Specific rewrite suggestions
- Estimated new match score

## Implementation Checklist

1. Scan resume for ATS issues
2. Analyze job description keywords
3. Calculate current match score
4. Identify missing keywords
5. Suggest exact placements
6. Flag formatting problems
7. Provide before/after examples
8. Re-score after changes
