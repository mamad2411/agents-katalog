---
name: compliance-cert-planner
description: Plan and sequence security and privacy compliance certifications (SOC 2, ISO 27001, GDPR, HIPAA, PCI DSS, CASA, etc.). Use when the user needs to scope which frameworks apply, classify each one, identify shared controls, and produce a roadmap.
---

# Compliance Certification Planner

Help the user decide which compliance frameworks apply to their organization, what shared controls cover multiple frameworks, and in what order to pursue them.

## When to use

- "Which compliance certifications do we need?"
- "Should we do SOC 2 or ISO 27001 first?"
- "How do GDPR and HIPAA overlap for our product?"
- "Build me a roadmap for our security compliance work."

## Workflow

1. **Gather context** — industry, geography of customers, data types handled (PHI, PCI, EU personal data, children's data), customer asks, contractual obligations, target launch dates.
2. **Fill the applicability matrix** — use `templates/applicability-matrix.md` to mark which frameworks apply, what triggered them, and confidence level.
3. **Classify each applicable framework** — use `templates/framework-classification.md` per framework (type, issuer, mandatory vs. voluntary, timeline, renewal cycle, external auditor needed).
4. **Map shared controls** — use `templates/shared-controls-checklist.md` to identify governance, access, asset, engineering, privacy, and AI-specific controls that satisfy multiple frameworks at once.
5. **Produce the roadmap** — use `templates/roadmap.md` to sequence work, batching frameworks that share controls and respecting external constraints (audit windows, customer deadlines).

## Templates

- `templates/applicability-matrix.md` — one-page yes/no/why grid across common frameworks
- `templates/framework-classification.md` — per-framework deep dive
- `templates/shared-controls-checklist.md` — cross-framework control inventory
- `templates/roadmap.md` — sequenced implementation plan

## Output expectations

Default deliverable is a single Markdown brief containing: applicability matrix, one classification block per applicable framework, the shared-controls checklist marked up for current state, and the roadmap. Flag any framework where confidence is low or where external counsel / auditor input is required before committing.
