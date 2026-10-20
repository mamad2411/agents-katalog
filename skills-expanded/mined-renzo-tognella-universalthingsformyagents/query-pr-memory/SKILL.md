---
name: query-pr-memory
description: Use when retrieving operational memory about pull requests by repo, PR number, work item, changed file, area, or implementation scope.
---

# Query PR Memory

## Overview

Query PR memory for implementation history and impact tracing.

Use this when the question is really “which PR changed this and what did it do?”

## When to Use

- You want to find a PR by number or repo
- You want PRs that touched a file or area
- You want PRs linked to a work item
- You want prior PRs related to a rule, pattern, or decision

Do not use this as the default query path for conceptual memory.

## Common Filters

- `project`
- `repo`
- `pr_number`
- `work_item_id`
- `area`
- `changed_file_contains`
- `status`

## Retrieval Strategy

1. Narrow by `project` first.
2. Use exact identifiers when available (`repo`, `pr_number`, `work_item_id`).
3. Use `changed_file_contains` for artifact-oriented recall.
4. Expand to linked rules, patterns, or PRs only after finding the primary PR memory.

## What to Return

Return the smallest useful answer:

- PR identity
- title
- summary
- changed files or matching file subset
- work item link
- linked memories when relevant

## Good Query Shapes

```text
Find PR memory for ModulusCore #14.
```

```text
Find PRs in MODULUS that changed proposal-detail.tsx.
```

```text
Find PR memories linked to Jira ENG-1234.
```

## Common Mistakes

- Searching PR memory when a business rule lookup is what you actually need
- Returning huge file lists when only the matching area matters
- Ignoring linked memories after locating the main PR
