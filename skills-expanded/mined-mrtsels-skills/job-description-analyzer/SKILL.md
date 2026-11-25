---
name: job-description-analyzer
description: Analyze job postings, calculate match scores, identify gaps, and create application strategy
category: resume
---

# Job Description Analyzer

## When to Use

Use when the user pastes a job description and wants to know if they should apply or how to tailor their application.

## Core Capabilities

- Parse job postings into structured requirements
- Calculate match score against resume
- Identify gaps and strengths
- Create application strategy
- Detect red flags in job postings

## Analysis Process

1. Extract: hard skills, soft skills, years of experience, education, certifications
2. Categorize: must-have vs nice-to-have
3. Match against resume with three levels: exact match, partial match, missing
4. Score: (weighted matches / total weighted requirements) x 100
5. Strategy: which gaps to address, which to ignore, how to position

## Output Format

Provide a structured analysis with match score, key strengths, critical gaps, red flags, and a go/no-go recommendation with customization strategy.
