---
name: learning-path-sre
description: >-
  Guide an SRE learning path from Google canonical books through practical skills in this pack: sequenced study + practice projects. Use when onboarding, self-study, or building a curriculum.
---

# Learning Path SRE

**Domain:** `organization`  
**Sources:** SRE Book 1e, Workbook, SRE Book 2e, BSRS

## When to use

- New SRE onboarding curriculum
- Self-study plan
- 'What should I read/do next?'

## Principles

- Read principle then practice (Book ↔ Workbook pairs).
- Learn by shipping: SLO, alert, postmortem, canary, automation.
- Add 2e AI/cloud chapters once foundations are solid.
- Security+reliability is part of modern SRE literacy.

## Workflow

1. Assess level: aspiring / practitioner / leader.
2. Assign path from docs/learning-paths/.
3. Pair each reading with a hands-on skill exercise.
4. Review artifacts (SLO doc, noise report, PM) with a mentor.
5. Graduate to AI and platform skills.

## Decision guide

- If no production access → use historical incident reports + design exercises (NALSD).

## Output template

```markdown
# Personal SRE curriculum
- Level:
- 4-week plan (read + exercise):
- Artifacts to produce:
- Mentor checkpoints:
```

## Anti-patterns

- Only reading with no practice.
- Jumping to AIOps before SLOs.

## Suggested 6-week practitioner path

1. Foundations + risk + SLIs/SLOs → produce SLO doc
2. Monitoring + burn alerts + noise reduction → alert PR
3. On-call + incident + troubleshooting → tabletop
4. Postmortem + error budget policy → policy draft
5. Canary + config + overload → design review notes
6. Automation + AI-assist principles → small toil bot (shadow)


## Related skills

`sre-foundations`, `sli-slo-design`, `incident-management`, `ai-supports-sre`

## Canonical references

- [SRE Book TOC](https://sre.google/sre-book/table-of-contents/)
- [Workbook TOC](https://sre.google/workbook/table-of-contents/)
- [SRE books hub](https://sre.google/books/)
- [BSRS](https://google.github.io/building-secure-and-reliable-systems/)

## Agent notes

- Prefer live data (metrics, tickets, pages) over generic advice.
- Cite which Google SRE source informed a recommendation when useful.
- Keep outputs tactical: decisions, owners, next actions.
