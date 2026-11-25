---
name: resume-prompt-kit
description: Build a full resume end to end using 10 structured prompts — career-goal positioning, an information-gathering checklist, professional summary variants, ATS-friendly experience bullets, JD-matched skills, certifications placement, education formatting, a proofreading/ATS audit, tailoring to a specific job posting, and a matching cover letter. Use when someone needs to write or overhaul a resume, wants ATS-safe formatting, is tailoring an existing resume to a specific job description, or needs a cover letter to go with it.
---

# Resume Prompt Kit

Source: reviewed from an uploaded infographic — "ChatGPT Prompts for
Building a Standout Resume — Executive Cheat Sheet" (smarterwithai.news).
10 literal prompts, quoted verbatim below, each usable standalone or run
in sequence via `/build-resume`.

This is a deeper, template-driven companion to the bare `/resume-review`
command already in this repo (a one-line "improve this resume" pass) —
reach for this kit when building or overhauling a resume from scratch, or
tailoring one to a specific posting, not just polishing an existing draft.

## The 10 prompts

### 1. Define career goals

Identifies career direction — target role, industry, seniority — and
decides which achievements, skills, and attributes to highlight.

```text
Act as a career coach. My target role is [TARGET ROLE] in [INDUSTRY], level [JUNIOR/MID/SENIOR]. Here are my top achievements: [ACHIEVEMENTS] and strengths: [SKILLS/TRAITS]. Recommend a resume positioning statement and the 5-7 themes I should emphasize. Avoid generic claims.
```

### 2. Gather basic information

Collects essential details (contact, links, work history) as a minimal,
complete intake — before drafting anything.

```text
Create a resume intake checklist for me. Ask only the minimum questions needed to build a complete resume for [TARGET ROLE]. Include contact info, links, work history, education, certifications, projects, and measurable achievements. Output as a fill-in template.
```

### 3. Write a professional summary

Concise, high-impact summary reflecting experience level, core strengths,
and aspirations aligned to the role/industry.

```text
Write 3 versions of a professional summary for [TARGET ROLE] in [INDUSTRY]. Audience: hiring manager for [TARGET ROLE]. My background: [YEARS] years in [FUNCTION], key wins: [2-3 WINS], strengths: [TOP 5], goal: [CAREER GOAL]. Keep each version 3-4 lines, measurable and specific.
```

### 4. Outline work experience

Structures roles with company/dates/responsibilities/achievements as
clear, quantified impact statements — not a duties list.

```text
Turn my work notes into ATS-friendly experience entries for [TARGET ROLE]. For each role: [ROLE, COMPANY, DATES, NOTES]. Write 4-6 bullets per role using action verbs, scope, and metrics (%, $, time, volume). Separate responsibilities vs achievements and prioritize impact.
```

### 5. Highlight skills

Lists technical and soft skills relevant to the job, matched against the
actual job description rather than a generic skills dump.

```text
From this job description: [PASTE JD], extract the top required skills and keywords. Compare them to my skills: [YOUR SKILLS]. Output: (1) 'Must-have' skills I match, (2) gaps to address honestly, (3) a prioritized Skills section (10-16 items) grouped by category.
```

### 6. Certifications and awards

Places credentials for maximum credibility without cluttering the resume
with low-relevance items.

```text
Given my target role [TARGET ROLE] and these credentials: [LIST CERTS/AWARDS], recommend the best placement (top / separate section / within education). Rewrite each item in a consistent format (name, issuer, year, credential ID if applicable). Flag anything low-relevance.
```

### 7. Education section

Presents degrees, honors, and coursework clearly, tailored to support the
target role rather than listed exhaustively.

```text
Format my Education section for [TARGET ROLE]. Details: [DEGREE, SCHOOL, YEAR], honors: [HONORS], coursework: [COURSEWORK], projects: [PROJECTS], certs: [CERTS]. Recommend what to include/omit to best support the role and keep it concise.
```

### 8. Proofread and format

Reviews clarity, consistency, grammar, and visual balance, with an
explicit ATS-safety pass (tables/columns/symbols that break parsers).

```text
Audit my resume for formatting and clarity. Here is the resume: [PASTE TEXT]. Check: consistency of tense, punctuation, dates, bullet structure, whitespace, section order, and ATS risks (tables, columns, symbols). Output a prioritized fix list + a cleaned version.
```

### 9. Tailor to a job description

Adjusts an existing resume to a specific posting — matching keywords and
emphasis without inventing or exaggerating anything.

```text
Tailor my resume to this job posting: [PASTE JD]. Here is my current resume text: [PASTE RESUME]. Rewrite bullets to highlight matching experience, add missing keywords naturally, and keep all claims truthful. Provide: updated summary, updated top skills, and 6-10 improved experience bullets with metrics.
```

### 10. Craft a cover letter

A role-specific cover letter aligned with the tailored resume — company
fit and a clear call-to-action, not a restated resume in prose.

```text
Write a tailored cover letter for [COMPANY] for the role [TARGET ROLE]. Use this job description: [PASTE JD]. Here is my current resume text and my top achievements: [3 ACHIEVEMENTS]. Keep to 250-350 words, confident and specific, include why this company, and end with a clear call-to-action.
```

## Run order

For a resume built from scratch: 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8. Steps 9
and 10 are per-application — run them each time against a new posting,
not once for the whole resume. `/build-resume` runs 1–8 in sequence, then
offers 9–10 for a named target job if one was given.

## Related skills in this repo

- **career-ops** (if installed/available in the environment): a broader
  career-management skill — this kit is scoped specifically to the
  resume/cover-letter artifact itself.
- Existing `/resume-review`, `/interview`, `/mockinterview`, `/hr`,
  `/salary`, `/skills-to-learn` commands (from an earlier reviewed
  shorthand-command batch) cover adjacent single-purpose career tasks —
  this kit is the deeper, multi-step version specifically for building or
  tailoring the resume document itself.
- **humanizer**: run on the drafted summary/bullets/cover letter before
  sending — AI-resume-writing tells (inflated language, repetitive
  sentence openers) are exactly what this catches.
