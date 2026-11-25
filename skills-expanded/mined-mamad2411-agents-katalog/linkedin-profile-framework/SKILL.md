---
name: linkedin-profile-framework
description: Build a deeply personalized LinkedIn improvement framework from CV/PDF/profile exports, user-supplied sources, current web research, and real professional context. Use at most 3 subagents, gather domain intelligence about the user's work, and produce one final markdown file: GUIA_FINAL_MELHORIA_LINKEDIN.md.
---

# LinkedIn Profile Framework

Use this skill when the user wants a surgical, personalized diagnosis and rewrite plan for a LinkedIn profile based on their real background, provided documents, and updated market research.

## Core Goal

Produce one final markdown file, `GUIA_FINAL_MELHORIA_LINKEDIN.md`, that is:

- personalized to the user's actual background
- critical, specific, and non-generic
- actionable across headline, About, Experience, Skills, Featured, projects, education, and activity
- grounded in current market evidence with citations for every market claim

## Non-Negotiable Rules

- Use at most 3 subagents.
- Do not invent experience, seniority, or results.
- Separate:
  - text changes
  - structural changes
  - positioning changes
  - learning priorities
  - proof needed
  - content to publish
  - content to remove or reduce
- Every recommendation tied to current market conditions must cite a source.
- Prefer strong, specific guidance over broad advice.

## Orchestration Model

Use up to three specialized subagents:

1. Architecture / copy / positioning
   - profile architecture
   - first impression
   - headline, About, URL, banner, photo, Featured
   - microcomponent-level diagnosis
2. Market / trends / skills
   - current market demand
   - recruiter expectations
   - relevant technologies, concepts, keywords, and adjacent skills
   - what is hype versus useful signal
3. Technical diagnosis / proof / execution plan
   - experience quality
   - evidence density
   - ownership, architecture, performance, security, quality
   - rewrite plan and prioritized execution

## Domain Intelligence Requirement

Before judging the profile, build a `domain intelligence map` for what the user actually works with.

That map must include:

- technologies
- terminology
- frameworks and tools
- technical depth signals
- job titles and adjacent roles
- common recruiter keywords
- market expectations for that domain
- proof artifacts that matter in that market

This map is mandatory. It feeds the whole framework and prevents generic advice.

## Required Inputs

Use the user's:

- PDF / CV / exported LinkedIn profile
- sources pasted in chat
- current web research
- real professional context
- target role or desired repositioning, when available

If something is missing, infer only what is safe and label the assumption.

## Workflow

1. Parse the intake material and build the domain intelligence map.
2. Run the 3 subagents with distinct scopes.
3. Merge findings into a single diagnosis.
4. Separate current-state diagnosis from future-state recommendations.
5. Rank every issue by `critical`, `high`, `medium`, or `low`.
6. Produce one markdown file only.

## Evidence Rules

- Use citations for all current-market claims.
- Prefer primary sources, official docs, reputable recruitment/career sources, and current web evidence.
- Treat community content as support, not as the main basis for market claims.

## Final Deliverable

The final markdown must include, at minimum:

- executive summary
- what the profile communicates today
- per-microcomponent diagnosis
- skills by microcomponent
- skills to learn or deepen
- market gaps
- concrete rewrite suggestions
- proof gaps and portfolio priorities
- prioritized action plan
- final checklist

Use the output structure reference file for the exact shape.

