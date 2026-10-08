---
name: retrieve-business-context
description: Select the smallest authoritative and permitted set of business sources without loading the whole workspace. Use when Dan or an employee needs confirmed company, customer, offer, voice, sales, delivery, constraint, operation, or proof context; when business truth must be cross-checked; or when creating a metadata-only context pack from the manifest-selected Business Context catalog.
---

# Retrieve Business Context

Select source paths before reading source contents. Keep employee instructions,
workflows, operational records, and business truth separate.

## Required inputs

- employee ID, name, or alias;
- compact task or business question;
- project only when not the manifest default;
- sensitivity ceiling, default `internal`.

## Workflow

1. Read `workspace/WORKSPACE_MANIFEST.json` and its organization/catalog paths.
2. Resolve the employee to its canonical ID and department.
3. Form a compact query from the outcome and missing concepts; never paste a
   transcript or raw dump into the query.
4. Run:

   ```bash
   python3 workspace/skills/retrieve-business-context/scripts/query_catalog.py \
     --employee <employee-or-alias> --query "<task concepts>"
   ```

5. Inspect onboarding status first. Ordinary retrieval excludes `candidate`
   entries; if onboarding is not ready, return the gap instead of widening.
6. Load only selected files or sections required for the outcome.
7. Prefer canonical truth. Supporting evidence adds detail but cannot override.
8. Recheck `review-on-use` and refresh `time-sensitive` claims before material
   decisions or public use.
9. Use `--json --output <ignored-path>` for a durable metadata-only context
   pack. It is selection evidence, not business truth.
10. Return selected sources, warnings, missing context, and sources actually
    read.

## Access rules

- Default to public/internal sources.
- Private or restricted sources require an explicitly authorized task.
- Never search the private inbox as ordinary employee context.
- Never merge another business workspace or allow paths outside this repo.
- Never infer a fact from a catalog summary; read the source.
- A zero-result response is a catalog gap, not permission to search everything.

Read `references/retrieval-contract.md` when changing filters or diagnosing an
empty or conflicting result.
