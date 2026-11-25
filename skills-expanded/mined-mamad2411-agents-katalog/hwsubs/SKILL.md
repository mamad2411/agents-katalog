---
name: hwsubs
description: Orchestrate HireWire job discovery, validation, tailoring, cover letters, application QA, storage, and tracking while delegating all resume work to the Resume skill.
---

# HireWire Subagents

## Codex popup behavior
Expose this skill in the Codex plugin/skills popup as **HireWire Subagents** with invocation `/hwsubs`.

## Non-conflict contract
`/hwsubs` must never independently generate, resize, restyle, or approve a resume.

For every resume task, `/hwsubs` must delegate in this order:
1. `/resume build <job>`
2. `/resume audit <output>`
3. If failed: `/resume rebuild <output>`
4. `/resume verify <output>`
5. Continue only after PASS.

`/resume` wins every conflict involving typography, margins, spacing, page utilization, chronology, ATS safety, employer-safe exclusions, or branding.

## Employer-facing pack
A released application pack may contain only:
1. tailored resume;
2. tailored cover letter.

Candidate profiles, scores, CTP, readiness briefs, gaps, hard gates, strategy, and internal notes remain internal-only.
