---
name: resume-and-interview-prep
description: Use when improving resumes, CVs, cover letters, portfolio summaries, LinkedIn profiles, job application materials, interview answers, mock interview plans, STAR stories, recruiter messages, or career transition narratives. Prefer this Skill when the task needs role fit, evidence, achievement framing, concise wording, interview structure, or application strategy. Do not use for fabricating experience, credential claims, or discriminatory hiring decisions.
meta:
  version: 1
  display_name: 简历与面试准备
---

# Resume And Interview Prep

## Purpose

Help users present real experience clearly for a target role and prepare evidence-backed interview answers.

## Use When

Use for:

- resume or CV editing
- cover letters
- LinkedIn profile summaries
- portfolio summaries
- job application tailoring
- interview answer prep
- STAR story building
- recruiter messages

## Material Gate

Identify:

- target role, job description, seniority, industry, and geography when relevant
- user's real experience, projects, impact, metrics, and constraints
- application format, length, and tone

Do not fabricate employment, education, certifications, metrics, responsibilities, or endorsements.

## Workflow

1. Extract target role requirements.
2. Map user's real evidence to role needs.
3. Rewrite bullets with action, scope, impact, and evidence.
4. Make gaps visible and suggest honest ways to frame transferable experience.
5. Prepare interview stories with situation, task, action, result, and reflection.
6. Draft concise application or recruiter messages when requested.
7. Use `html-report-builder` only for portfolio-style summary reports when useful.

## Checks

- Every claim is grounded in user-provided experience.
- Metrics are real or removed.
- Tone is confident but not inflated.
- Resume content is targeted, not generic.
- Interview answers include evidence and learning.

## Outputs

- resume rewrite
- cover letter
- profile summary
- achievement bullets
- interview answer bank
- STAR stories
- recruiter message

## Boundary

This Skill owns career material writing, role-fit framing, and interview preparation. It does not own hiring decisions, background checks, credential verification, immigration/legal advice, or job application submission.

It must not run shell, Python, Node, npm, curl, MCP, ATS, LinkedIn, email, job board, package install, submit, or external API commands by itself; those actions belong to XAgent tools visible in the current session.
