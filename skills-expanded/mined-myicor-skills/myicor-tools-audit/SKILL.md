---
name: myicor-tools-audit
description: Audit the user's myICOR tool stack for coverage gaps. Invoke when the user asks whether their tool stack is complete, what tools or categories they are missing, which of their tools are weak or under-used, or wants a recommendation for which lesson to take next based on their stack.
---

# myICOR Tool Stack Audit

This skill teaches you (the AI agent) how to run a coverage audit of the
user's myICOR tool stack with the official `myicor` CLI.

myICOR organizes tools across four core categories — **PKM** (Personal
Knowledge Management), **BKM** (Business Knowledge Management), **PPM**
(Personal Productivity Management), and **BPM** (Business Process
Management) — and 13 Venn "centroid" zones that capture overlaps between
them. A healthy stack covers the categories the user actually needs without
critical gaps or redundant overlaps.

## Prerequisites

1. **CLI installed and authenticated.** See the `myicor-cli-quickstart`
   skill. If a command prints `Not logged in. Run: myicor auth login`, walk
   the user through `myicor auth login` once.
2. A **paid myICOR membership** (monthly tier or above). Free-tier accounts
   get a `403` with an upgrade message.

## When to invoke

| User intent | Run |
|---|---|
| "Is my tool stack complete?" / "What am I missing?" | `myicor tools audit` |
| "Audit my tools" / "Any gaps in my stack?" | `myicor tools audit` |
| "Which tools of mine are weak?" | `myicor tools audit` |
| "What lesson should I take next?" (stack-driven) | `myicor tools audit` |
| Programmatic / parsing | `myicor tools audit --json` |

## Command reference

### `myicor tools audit [--json]`

Audits the signed-in member's own tool stack. There is no way to audit
another user — the underlying MCP tool always scopes to the caller.

`--json` returns the raw audit payload:

```json
{
  "total_tools": 14,
  "has_critical_gaps": true,
  "core_category_coverage": { "pkm": true, "bkm": false, "ppm": true, "bpm": false },
  "centroid_coverage": { "covered": [ ... ], "missing": [ ... ] },
  "weak_areas": {
    "low_rated_tools": [ { "id": "...", "name": "..." } ],
    "exploring_tools": [ ... ],
    "seeking_alternatives": [ ... ]
  },
  "critical_overlaps": [ ... ],
  "recommended_assignments": [ { "title": "...", "url": "https://app.myicor.com/..." } ]
}
```

Field meaning:
- **`has_critical_gaps`** — the headline. `true` means at least one core
  category or critical overlap is uncovered.
- **`core_category_coverage`** — a presence flag per core category. A
  `false` is a real gap worth raising.
- **`centroid_coverage`** — covered vs. missing across the 13 Venn zones.
- **`weak_areas`** — tools the user rated low, is still exploring, or wants
  to replace. Good candidates for a focused conversation.
- **`recommended_assignments`** — myICOR lessons that close the detected
  gaps. Each has a deep link into `app.myicor.com`.

Exit code: `0` on success, `1` on error (not authenticated, network, 403).

## How to use the output

1. Lead with `has_critical_gaps`. If `true`, name the missing core
   categories from `core_category_coverage`.
2. Call out `weak_areas` only if non-empty — these are coaching
   opportunities, not failures.
3. Offer the first one or two `recommended_assignments` as concrete next
   steps, with their deep links.
4. Don't overwhelm the user with all 13 centroid zones — summarize the
   count and name only the missing ones.

## Don'ts

- Don't call `app.myicor.com` endpoints directly — use the CLI, which
  handles token refresh and retries.
- Don't try to audit another user's stack. The command is self-scoped by
  design.

## Repository

This skill lives at https://github.com/myicor/skills under
`skills/myicor-tools-audit/`.
