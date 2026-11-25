---
id: skill-evidence-classification
type: agent-skill
status: reviewed
created: 2026-05-30
updated: 2026-05-30
name: evidence-classification
description: Classify claims as fact, opinion, marketing, hypothesis or open question before using them in agent memory or standards.
version: 0.1.0
topics:
  - agent-skills
  - evidence
  - assessment
tools:
  - Pritha
  - Markdown
sources:
  - 04_standards/expert-information-assessment.md
  - 07_workflows/expert-information-assessment.md
  - 08_templates/assessment.md
related:
  workflows:
    - 07_workflows/agent-skill-pack-selection.md
source: pritha-memory
source_paths:
  - 04_standards/expert-information-assessment.md
  - 07_workflows/expert-information-assessment.md
  - 08_templates/assessment.md
review_status: reviewed
trust_level: local-reviewed
requires_toolsets:
  - filesystem
  - markdown
risk_level: low
tags:
  - evidence
  - assessment
  - standards
---

# Evidence Classification

## When to Use

Use when converting a source, user note, transcript, article, repository or external claim into curated agent knowledge.

## Procedure

1. Separate facts, opinions, marketing claims, hypotheses and unknowns.
2. Prefer primary sources for volatile technical claims.
3. Record source date, retrieved date, verified date and version context when available.
4. Compare the claim with existing briefs, reviews, decisions and standards.
5. Promote only well-supported, reusable conclusions into standards or decisions.

## Pitfalls

- Do not treat generated wiki pages as evidence.
- Do not collapse "interesting" and "adopt now" into the same recommendation.
- Do not hide weak evidence behind confident language.

## Verification

- Evidence quality is stated.
- Alternatives or trade-offs are named.
- Open questions remain explicit.
- Techscope/Agents Mother fit is recorded when relevant.
