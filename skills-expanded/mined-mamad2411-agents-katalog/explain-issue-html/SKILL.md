---
name: explain-issue-html
description: Create standalone HTML explanation artifacts for confusing bugs, incidents, code behavior, API/cache/state issues, or technical problems the user does not understand. Use when the user asks to explain a problem from scratch, teach like a beginner or high school student, create a docs HTML artifact, use ASCII diagrams, show before/after snippets, point to the broken field/line, or explain why a fix works.
---

# Explain Issue HTML

## Overview

Create a self-contained HTML document that teaches a confusing technical issue visually and concretely. Prefer this skill when the user says they do not understand a bug, fix, cache behavior, query shape, state flow, or API behavior and wants an artifact they can re-open later.

Use `assets/explainer-template.html` as a starting structure when it helps, but adapt the sections to the actual problem.

## Workflow

1. Gather evidence before writing the artifact.
   - Read the relevant code, queries, logs, responses, tests, and docs.
   - Identify the exact symptom, trigger, data flow, broken line or field, root cause, fix, and verification signal.
   - If the cause is not proven, label it as a hypothesis instead of presenting it as fact.

2. Build the teaching model.
   - Explain the system as a beginner-friendly mental model first.
   - Use concrete names from the issue: real IDs, query names, fields, files, functions, URLs, or events.
   - Prefer "what happened before / what happened after" over abstract theory.

3. Create a standalone HTML artifact.
   - Save to the path the user requested.
   - If no path is given, use `docs/<short-issue-name>.html`.
   - Keep CSS inline in the file. Do not require app assets, servers, bundlers, or external CDNs.

4. Include these sections unless the task clearly does not need one:
   - Plain-language title and one-sentence summary.
   - Beginner mental model.
   - Full relevant query/code/data shape.
   - Direct marker on the broken line or field, using labels like `[BUG]`, `[FIX]`, or `[IMPORTANT]`.
   - Before diagram using ASCII art.
   - Why it breaks, step by step.
   - After/fix snippet.
   - After diagram using ASCII art.
   - Verification checklist or how to recognize the issue is fixed.

5. Write for someone new to the topic.
   - Use short sentences.
   - Define unfamiliar words before using them heavily.
   - Avoid vague phrases like "cache issue" without showing the exact record or field.
   - Show one concrete example before general rules.

## Artifact Style

- Use readable typography, restrained colors, and strong labels.
- Keep diagrams in `<pre><code>` blocks so spacing stays exact.
- Make broken things visually distinct from fixed things.
- Use responsive layouts so the artifact works on laptop and mobile.
- Do not use visible in-app instructions like "click here" unless the artifact is intentionally interactive.
- Keep the artifact practical rather than decorative.

## Explanation Pattern

For cache/state/data bugs, prefer this structure:

```text
1. Page/API/event A writes complete data.
2. Page/API/event B references the same entity or state key.
3. B writes a smaller or different shape.
4. The shared record/state is now incomplete or changed.
5. The watcher/UI/query sees missing or changed data.
6. The system refetches, rerenders, resets, or shows the wrong value.
7. The fix keeps the shared shape consistent or changes the merge/update rule.
```

For GraphQL/Apollo bugs, explicitly show:

```text
Entity cache key:
  __typename + id

Example:
  __typename: "Debtor"
  id: "abc123"

Apollo cache key:
  Debtor:abc123
```

Then show what happens when a nested object has no ID:

```text
Parent entity:
  Debtor:abc123

Nested value object:
  invoiceAmount has no id

Result:
  Apollo stores invoiceAmount inside Debtor:abc123
  A later invoiceAmount write can replace that small object
```

## Template

The optional starter template is:

```text
assets/explainer-template.html
```

Use it by reading the file, then replacing placeholders with the real issue. Do not leave placeholder text in the final artifact.
