---
name: Resume Customizer
description: Tailor a resume for a specific job posting without fabricating experience. Use this skill when someone wants to customize, tailor, or target their resume for a particular job, reorder resume content for relevance, match resume language to a job description, or create a role-specific version of their resume. Also trigger for "adjust my resume for this job", "make my resume match", or any request to align resume content with a specific posting.
---

# Resume Customizer

Adjust a resume to match a specific job posting by reorganizing, rewording, and emphasizing -- never inventing.

## Core Principle

Tailoring is selection, not fabrication. You are choosing which true facts to foreground, which language to adopt, and which sections to reorder. You are never adding skills you do not have, inflating titles, or inventing experiences.

## Customization Workflow

### 1. Extract Target Keywords

From the job posting, pull:
- The exact job title and any variations used
- Technical skills mentioned (use their exact phrasing)
- Soft skills and competencies emphasized
- Industry or domain terms
- Metrics language ("data-driven", "revenue-focused", "customer-centric")

### 2. Rewrite the Summary

The professional summary is the highest-impact customization point. Rewrite it for every application using this template:

"[Target role title] with [X years] of experience in [their top 2-3 requirements]. Track record of [strongest relevant achievement with a number]. Skilled in [3-5 keywords from their posting that you genuinely possess]."

### 3. Reorder the Skills Section

Move skills that appear in the job posting to the top. If the posting emphasizes Python, SQL, and Tableau, those go first even if your strongest skill is something else.

### 4. Adjust Experience Bullets

For each role, lead with the bullet most relevant to the target job. If you have 5 bullets and only 2 are relevant, move those two to the top. You can swap bullet order between applications without changing any facts.

Adjust language to mirror the posting:
- If they say "stakeholder management" and you wrote "coordinating with teams", change to "managed stakeholder relationships across X departments"
- If they say "Agile" and you wrote "sprint-based development", add "Agile" explicitly

### 5. Add or Remove Sections

- Include a Projects section if the role values hands-on work and your experience section is light
- Include Certifications prominently if the posting lists specific ones
- Remove irrelevant sections (e.g., drop a Volunteer section if space is tight and it does not support the target role)

### 6. Verify the Changes

After customization, check:
- Every fact is still true
- The resume reads naturally, not like a keyword dump
- ATS formatting is preserved (no tables, columns, or images introduced)
- The file is named properly: `Lastname_Firstname_TargetRole_Company.pdf`

## What Is Acceptable vs. Not

**Acceptable:**
- Reordering bullets to lead with relevance
- Adopting the posting's terminology for things you genuinely did
- Removing irrelevant content to make space
- Rewriting your summary for each application
- Adding context to vague bullets ("managed projects" becomes "managed 8 concurrent projects with combined $2M budget")

**Not acceptable:**
- Adding skills you do not have
- Changing job titles
- Inventing metrics
- Claiming certifications you have not earned
- Describing someone else's work as your own

## Output Format

```
CUSTOMIZATION PLAN FOR [Role] AT [Company]

SUMMARY
Before: [current]
After: [rewritten]

SKILLS REORDER
New order: [list, most relevant first]
Keywords added: [list, only ones that are genuinely held]

EXPERIENCE ADJUSTMENTS
[Company/Role]:
  - Lead bullet changed to: [which bullet moves to position 1]
  - Language adjustment: "[old phrase]" changed to "[new phrase]"
  - Bullet removed for space: [which one, if any]

OTHER CHANGES
- [section added/removed/reordered]

KEYWORD COVERAGE
Before customization: X/Y required keywords present
After customization: X/Y required keywords present
```
