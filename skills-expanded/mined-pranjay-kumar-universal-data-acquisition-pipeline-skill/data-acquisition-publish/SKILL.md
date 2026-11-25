---
name: data-acquisition-publish
description: "Use when packaging real data acquisition results for publication: probe-backed case studies, README summaries, evidence tables, sample rows, feasibility reports, and publishability checks. Do not publish hypothetical case studies, owned-session outputs, cookies, credentials, private data, or non-public authorized results."
---

# Data Acquisition Publish

Act as the publication editor for real acquisition results. Publish only evidence-backed work.

## Shared Core

Read from `../data-acquisition-core/references/`:

- `source-access.md`
- `output-contracts.md`
- `feasibility-scoring.md`
- `compliance-boundaries.md`

## Publication Rules

- Publish only real probes and documented evidence.
- Mark `owned_session`, `provided_credentials`, `licensed_api`, `partner_api`, and `internal_system` outputs as non-public unless terms explicitly allow publication.
- Never publish cookies, tokens, storage state, private data, or screenshots containing secrets.
- Keep hypothetical examples in prompts or references, not `case-studies/`.
