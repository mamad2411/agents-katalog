---
name: Atomizer API Rules
globs: ["**/*api*.py", "**/api/**/*.py", "**/*routes*.py", "**/*schemas*.py"]
alwaysApply: false
description: Rules for the Atomizer API, creator handoff and ops endpoints.
---

# Atomizer API Rules

The Atomizer API must expose existing data and trigger existing orchestration. It must not create duplicate systems.

## API scope

The API may expose:

- runs
- assets
- atoms
- quality
- errors
- healthchecks
- JSON exports
- Markdown exports
- creator handoff packages

## Do not build

- No new export system.
- No duplicate asset storage.
- No duplicate Markdown generation.
- No TXT endpoint.
- No CSV endpoint.
- No publishing endpoint.
- No platform upload endpoint.
- No auto-publishing.
- No hidden legacy fallback.

## Required behavior

- Use existing run/storage/export structures.
- Return existing JSON/Markdown exports where available.
- Trigger runs through the existing orchestrator.
- Reject `legacy_heuristics_enabled=true`.
- Require `pipeline_mode=prompt_driven`.
- Reject invalid formats with a clear 400 response.
- Return 404 for unknown run IDs.
- Return 404 for unknown asset IDs.
- Never leak secrets.

## Creator handoff

Creator handoff packages must be built from existing run, asset, atom and quality data.

They must include:

- `run_id`
- `asset_id`
- `requested_format`
- `target_creator`
- `handoff_status`
- `asset_status`
- `review_status`
- `publish_status`
- `quality_score`
- `human_review_required`
- `used_atom_ids`
- `source_references`
- `source_excerpts`
- `asset`
- `quality_issues`
- `risk_notes`
- `creator_instructions`
- `allowed_actions`
- `blocked_actions`

## Handoff status rules

- Generated + approved + no human review required => `ready_for_creator`
- Generated + human review required => `needs_human_review`
- Rejected quality/review => `rejected`
- `insufficient_atoms` => `insufficient_atoms`
- Failed asset => `failed`

## Safety

Never mark the following as ready:

- rejected assets
- failed assets
- insufficient assets
- assets requiring human review

Never return:

- `OPENAI_API_KEY`
- Authorization headers
- provider request secrets
- environment secrets
- raw sensitive config

## Ops scope

Ops is minimal:

- healthchecks
- errors
- runs

No large monitoring suite.
No alerting system.
No release automation.

## Tests

API changes must include or preserve tests for:

- health
- runs
- assets
- atoms
- quality
- errors
- exports
- handoff
- invalid requests
- no TXT/CSV endpoints
- no publishing endpoint
- no leaked secrets
