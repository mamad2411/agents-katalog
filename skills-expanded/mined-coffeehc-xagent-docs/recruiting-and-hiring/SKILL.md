---
name: recruiting-and-hiring
description: Use when creating, reviewing, or improving job descriptions, candidate scorecards, interview plans, screening criteria, interview questions, candidate summaries, hiring debriefs, offer rationale, or recruiting process material. Prefer this Skill when the task needs role clarity, fair evaluation, structured evidence, bias reduction, or hiring process discipline. Do not use for discriminatory screening, legal approval, or automated hiring decisions.
meta:
  version: 1
  display_name: 招聘与面试
---

# Recruiting And Hiring

## Purpose

Create fair, structured hiring material that evaluates candidates against job-relevant criteria and preserves evidence.

## Use When

Use for:

- job description drafts
- candidate scorecards
- interview plans
- screening rubrics
- interview question banks
- candidate summaries
- hiring debriefs
- offer rationale drafts

## Material Gate

Identify:

- role, level, team, responsibilities, must-have skills, nice-to-have skills, and constraints
- interview stages, evaluators, criteria, and legal or policy boundaries
- candidate evidence if reviewing a candidate

Do not use protected characteristics or proxies as evaluation criteria.

## Workflow

1. Define role outcomes and level expectations.
2. Separate must-have criteria from nice-to-have signals.
3. Build structured evaluation dimensions.
4. Draft interview questions tied to each dimension.
5. Summarize candidate evidence against criteria, not vibes.
6. Flag missing evidence and bias risks.
7. Use `html-report-builder` for hiring process or candidate comparison reports when needed.

## Checks

- Criteria are job-relevant and observable.
- Questions avoid protected characteristics.
- Candidate assessments cite evidence.
- Missing evidence is not treated as negative evidence.
- Final decision language remains human-review oriented.

## Outputs

- job description
- interview plan
- candidate scorecard
- interview questions
- candidate summary
- hiring debrief
- recruiting process review

## Boundary

This Skill owns hiring material structure, role clarity, interview planning, and evidence-based summaries. It does not own legal approval, HR policy, background checks, offer approval, compensation approval, or automated employment decisions.

It must not run shell, Python, Node, npm, curl, MCP, ATS, background-check, email, calendar, HRIS, package install, or external API commands by itself; those actions belong to XAgent tools visible in the current session.
