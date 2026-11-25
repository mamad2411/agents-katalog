---
name: brain-taxonomist
description: Decide where new local brain pages belong before they are written, using repo conventions and any available schema guidance.
---

# Brain Taxonomist

Use this skill before creating a new `brain/` page when the right category, slug, or page type is uncertain.

Upstream GBrain reads the active schema pack. This Codex port first uses the repo-local brain layout and can consult `gbrain schema show --json` when the upstream CLI is available.

## Workflow

1. Identify the primary subject:
   - person
   - company or organization
   - concept
   - source material
   - idea
   - meeting
   - report
   - task or workflow
2. Prefer existing local conventions:
   - `brain/people/` for people
   - `brain/concepts/` for reusable concepts, skills, tools, and projects
   - `brain/sources/` for source documents and imported references
   - `brain/ideas/` for original proposals or sketches
   - `brain/.raw/` for preserved raw input
3. If `gbrain` is installed, inspect active schema metadata before inventing a new location.
4. Produce a filing recommendation:
   - path
   - slug
   - page type
   - required backlinks or citations
5. If no existing category fits, recommend `schema-author` before writing.

Use `routing-eval.jsonl` as the deterministic routing fixture. Each JSON object must identify an expected packaged skill; any `ambiguous_with` targets must also exist in the package.

## Guardrails

- Do not hardcode a new directory if an active schema says otherwise.
- Do not create the page unless the calling task asked you to write it.
- Do not refile existing user pages without explicit permission.
