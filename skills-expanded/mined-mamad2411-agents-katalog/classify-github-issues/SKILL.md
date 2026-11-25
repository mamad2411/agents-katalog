---
name: classify-github-issues
description: >-
  Map triaged findings to GitHub Issues with the correct labels, milestone, and
  body, and emit github_backlog_input.json ready for creation. Use this AFTER
  triage and BEFORE creating issues — when the user asks "what labels should these
  get", "turn these findings into GitHub issues", "classify these for GitHub", or
  "build the github backlog input". Maps severity to priority labels (P0-P3),
  kind to type labels (bug/enhancement/task), and hours to size labels
  (size:XS-XL). Creates a milestone for the batch. Hands off to
  github-create-issues.
effort: max
---

# classify-github-issues

Turn findings (from `github-extract-findings` + `github-triage-findings`) into a
`github_backlog_input.json` that `github-create-issues` can create. Unlike ADO,
GitHub Issues are flat — type, priority, and size are expressed as labels; the
batch grouping is a milestone; the parent tracker is a tracking issue created last.

Schemas live in `references/data-contracts.md` — read it for the exact shapes.

## 1. Map findings to label sets

For each finding, assign three labels:

**Type label** (pick one):

| finding kind | label |
|---|---|
| `rename` / `disambiguation` / wrong/mislabeled existing thing | `bug` |
| `missing` / net-new capability | `enhancement` |
| process / administrative work | `task` |
| docs-only change | `documentation` |

When a finding is ambiguous between `bug` and `enhancement`, ask the user.

**Priority label** (based on `severity`):

| severity | label |
|---|---|
| Critical | `P0` |
| High | `P1` |
| Medium | `P2` |
| Low | `P3` |
| (none) | `P2` — default Medium, note it |

**Size label** (based on estimated hours):

| hours | label |
|---|---|
| ≤ 2h | `size:XS` |
| 3–4h | `size:S` |
| 5–8h | `size:M` |
| 9–16h | `size:L` |
| > 16h | `size:XL` |

Use these work-kind anchors:

| kind | baseline |
|---|---|
| rename (one spot) | 1–2h |
| rename (multi-screen) | 3–4h |
| disambiguation / mapping | 4–8h |
| missing field (UI + submit) | 6–8h |
| structural / new column | 4–6h |

If an item exceeds ~16h, propose splitting it instead.

## 2. Write the issue title

Specific and self-contained. Name the thing and the expected state:
- Good: `Portal label "Auto" should display "Automotive Cargo"`
- Bad: `Fix naming`

## 3. Write the issue body (Markdown)

```markdown
## Finding

**Current:** <current value>
**Expected:** <expected value>
**Section:** <section>

**Recommendation:** <recommendation>

<notes if any>

**Estimate:** Xh
```

The raw hour estimate goes at the bottom of the body as `**Estimate:** Xh` so it
survives label changes.

## 4. Propose a milestone

Name the batch milestone (e.g. `Audit Wave 1`, `Security Findings Q2 2026`). Ask
the user to confirm or rename it. `create_github_issues.py` creates the milestone
if it doesn't exist.

## 5. Decide assignees

A fresh backlog is usually created *unassigned* (assigned later in planning).
**Ask the user:** leave unassigned, assign to themselves, or map per-row. Use GitHub
username strings in `assignees[]`.

## 6. Show estimates table and get approval

Before writing the JSON, show a table and wait for explicit OK:

```
 key  | title (truncated)               | type        | priority | size   | est
------|---------------------------------|-------------|----------|--------|-----
 1    | Portal label "Auto" should...   | bug         | P1       | size:S | 4h
 2    | Add rate limiting to API        | enhancement | P2       | size:M | 6h
                                                                          ----
                                                                          ~10h
```

Let the user adjust any value before proceeding to the dry-run.

## 7. Write github_backlog_input.json

Assemble the full JSON per the contract in
`references/data-contracts.md` and write
it next to the findings file. Every item must have a `key`, a non-empty `title`,
at least one label of each type/priority/size dimension, and a populated `body`.

Then hand off to **github-create-issues** for the visual dry-run and creation.
