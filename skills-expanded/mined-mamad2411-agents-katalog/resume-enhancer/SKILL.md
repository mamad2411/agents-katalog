---
name: resume-enhancer
description: "Rewrite and optimize resumes for target roles with stronger impact bullets and ATS keyword alignment. USE WHEN a task matches the Craft workspace workflow for resume-enhancer."
cluster: business-content
version: 1.0.0
origin: "craft-agent workspace"
globs:
  - "**/resume*.md"
  - "**/cv*.md"
  - "**/*resume*.txt"
  - "**/*cv*.txt"
alwaysAllow:
  - "Read"
---

# Resume Enhancer

Use this skill when the user wants to improve a resume for specific roles, improve ATS fit, and increase interview conversion.

## Trigger Conditions
- User asks to improve or rewrite resume
- User asks for ATS optimization
- User wants role-specific resume tailoring

## Required Inputs
1. Existing resume text
2. Target role(s) and job descriptions
3. Key achievements and measurable outcomes
4. Preferred geography/industry (optional)

## Workflow
1. **Target extraction**: identify keywords, required skills, and role expectations.
2. **Resume audit**: assess clarity, relevance, and quantification.
3. **Rewrite**: improve summary, experience bullets, and skills section.
4. **ATS optimization**: map keywords naturally and remove weak phrasing.
5. **Final polish**: consistency check for formatting and impact.

## Output Format
- Before/after improvement summary
- Rewritten resume sections
- ATS keyword match list
- Top 5 additional edits user should make

## Guardrails
- Never invent companies, titles, or achievements.
- Prefer quantified outcomes and concrete verbs.
- Avoid stuffing keywords unnaturally.
