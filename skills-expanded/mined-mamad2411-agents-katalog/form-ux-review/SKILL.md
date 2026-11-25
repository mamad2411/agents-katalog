---
name: form-ux-review
description: Review and design form UX for signup, checkout, onboarding, settings, support, enterprise lead forms, creator submission, marketplace listing, payment, cancellation, data export, and admin workflows across web, mobile, and desktop. Use when improving form completion, clarity, accessibility, validation, errors, field order, progressive disclosure, autosave, trust, fraud controls, and support evidence.
---

# Form UX Review

Use this skill to make forms easier, safer, and more trustworthy without hiding important terms.

## Workflow

1. Identify form goal, user intent, risk level, platform, data sensitivity, and completion metric.
2. Read `references/form-ux-systems.md`.
3. Map fields, steps, validation, error recovery, save/resume, accessibility, security, and support evidence.
4. Separate friction that protects users from friction that only reflects internal data needs.
5. Produce prioritized fixes with metrics and validation checks.

## Guardrails

- Do not remove fields needed for safety, legal, payment, privacy, or support without another control.
- Do not hide material terms behind prechecked boxes or vague copy.
- Do not optimize completion if it increases bad-fit leads, refunds, fraud, or support burden.

## Output format

```text
Form context:
Primary task:

Findings:
- P0 <issue> -> fix, validation, metric
- P1 <issue> -> fix, validation, metric

Field/step map:
- <field> -> why needed, validation, recovery

Instrumentation:
- <event/property>
```
