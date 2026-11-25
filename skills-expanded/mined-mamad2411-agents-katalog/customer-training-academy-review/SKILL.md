---
name: customer-training-academy-review
description: Design and audit customer training academies for onboarding, admin enablement, role-based curricula, certification, labs, templates, webinars, office hours, self-serve courses, localization, accessibility, lifecycle triggers, partner/customer education, adoption metrics, support deflection, and content governance. Use when education must improve activation, retention, expansion, and support quality.
---

# Customer Training Academy Review

Use this skill to convert customer training academy, education, certification, curriculum, adoption, support deflection, and governance questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify learner personas, jobs-to-be-done, activation blockers, product complexity, support drivers, success milestones, segments, languages, accessibility needs, and delivery channels.
2. Read `references/customer-training-academy-patterns.md`.
3. Classify education as onboarding, admin setup, role-based workflow, advanced practice, certification, partner enablement, release education, or remediation.
4. Define curriculum map, prerequisites, formats, labs/templates, assessment, certification, lifecycle triggers, localization, content ownership, and measurement.
5. Produce academy plan, state machine, decision table, event schema, curriculum checklist, and content operations cadence.

## Guardrails

- Do not use training to compensate for broken onboarding, confusing IA, missing defaults, or poor product copy without product fixes.
- Do not measure academy success only by course completion; connect learning to activation, adoption, support reduction, retention, and expansion.
- Do not ship certification or partner training without assessment quality, anti-cheat expectations, and versioned product knowledge.
- Do not ignore accessibility, localization, role differences, and admin/end-user separation.

## Output format

```text
Training academy context:
Audience / source of truth / risk boundary:

Academy operating plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Curriculum, triggers, and success metrics:
- <trigger> -> <policy, metric, edge case, support note>
```
