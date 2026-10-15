---
name: api-changelog-summarizer
description: Vendor-neutral skill to convert an API diff (before/after schemas or endpoints) into a structured changelog with breaking changes and migration guidance.
---

## When to invoke
- You have an API change (OpenAPI fragments, endpoint lists, or schema diffs) and need a human-readable changelog.
- You want release notes with clear breaking vs non-breaking classification.

## Inputs needed
- A JSON diff describing changes (added/removed/modified endpoints and fields).
- Optional release metadata: version, date, owner.

## Workflow
1. Validate diff structure and normalize identifiers.
2. Classify each change as breaking / behavioral / non-breaking.
3. Group by endpoint or component.
4. Generate migration notes (what to update in clients).
5. Output a Markdown changelog with concise bullets.

## Output format
Markdown with:
- Release header
- Breaking changes
- Behavioral changes
- Non-breaking changes
- Deprecations
- Migration notes

## Guardrails
- If the diff does not include enough information to classify a change, mark it as "needs review".
- Do not invent endpoints or fields.

## Reference code
- `summarize_api_diff.py` reads a JSON diff and writes Markdown changelog.
