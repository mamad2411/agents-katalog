---
name: code-review
description: >
  Severity scale, verdict rule, review checklist, and spec-review lenses for pull-request
  inspection. Use when reviewing a PR, deciding a verdict, or writing a finding.
---

# Code Review

## Severity scale

| Severity | Definition | Harness example |
|----------|------------|-----------------|
| `blocker` | Correctness, security, or test-baseline violation | Test deleted or skipped in the diff |
| `major` | Spec boundary or non-negotiable violated | File in the spec's `Out:` scope modified; density floor missed |
| `minor` | Co-change missing or consistency gap | Contract file updated without bumping its dependent handler |
| `nit` | Style or naming, non-blocking | Identifier doesn't follow the project's naming convention |

## Verdict rule

Any `blocker` → `CHANGES_REQUESTED`. Any `major` without a documented waiver →
`CHANGES_REQUESTED`. Only `minor` or `nit` findings → `APPROVED`.

Waiver format — place in the PR body, one line per waived finding:

```
Waived: <exact major finding> — <why this is acceptable> — @<approver>
```

A waiver without `@<who>` does not count.

## Review checklist

For code PRs, every item below is a finding when violated.

| Check | Severity |
|-------|----------|
| Every `UC-<n>` in the spec has a passing test carrying its id | `blocker` |
| Full CI matrix for every touched stack is green; skip count is zero | `blocker` |
| New tests sit at the lowest tier that can observe their result; no higher tier re-asserts a behaviour a lower one pins | `minor` |
| No file listed in the spec's `Out:` scope was modified | `major` |
| `qa-report.md` present and says `PASS` with an explicit "Not verified" section | `major` |
| Contract directory changed in the same commit as any handler whose contract moved | `minor` |
| PR is a draft, labelled, riskiest changes called out by `file:line` | `nit` |
| No hardcoded credentials; unvalidated input does not reach exec/eval; no new permissions without a spec row | `blocker` |
| Every operation the diff touches is traceable to a SKILL.md entry or spec row | `minor` |
| A new endpoint or schema field introduces a second error shape instead of the API's existing envelope (`rest-api-design`, `graphql-api-design`) | `major` |
| A published path, field, enum value or error code was removed, renamed or retyped in place, with no deprecation | `blocker` |
| A collection endpoint or list field ships with no bounded page size | `major` |

| Branch inside its `Change budget:` (or the repo default) for added lines, files and modules | `major` |
| Added lines past the repo's hard ceiling, or a scope report naming shotgun surgery | `blocker` |
| Mechanical change (rename, codemod, generated update) mixed into a behaviour change | `major` |
### Slop-guard rule

When `.aisdlc/slop-guard/report.json` exists, or the path configured under `slop-guard:` in
`.claude/sdlc.md` exists, import every item it marks as a blocker as a `blocker` finding.
Never re-implement the check; consume the file.

### Size rule

Size findings come from `specs/<TICKET>/scope-report.md` `## Size`, written by the
`scope-check` phase; do not re-measure. A breach is a decomposition finding, never a request
for a more careful reviewer: the remedy named in the finding is `/sdlc:decompose <TICKET>`.
A spec that declared a wider `Change budget:` for a mechanical slice is compliant — the budget
it set is the budget that applies.

### Structure rule

Structure findings come from `specs/<TICKET>/scope-report.md` `## Structure`, written by the
`scope-check` phase (requires `lizard` on the runner PATH). Import as follows:
- `erosion:` finding → `[major]`; remedy is splitting the function or `/sdlc:decompose`
- `new hotspot:` finding → `[major]`; remedy is splitting the function or `/sdlc:decompose`
- `hotspot over 25:` finding → `[blocker]`; remedy is splitting the function or `/sdlc:decompose`

When `## Structure` says `skipped: …`, no structure findings are imported.
Structure never causes `BLOCKED`; it promotes `PASS` → `GAPS` only.

## Spec-review lenses

When every changed file is under `specs/`, skip the code checklist and apply these lenses:

| Lens | What to look for |
|------|-----------------|
| Risks | Runtime failures if this spec ships as written |
| Compatibility | Changes that break a contract surface, label set, or API shape |
| Gaps | UCs lacking an observable result, a test column entry, or marked e2e without a critical journey |
| Improvements | Simpler ways to express the same intent |
| Simplicity | Constraints that over-specify without adding safety |

Report each finding with its lens name and `<section>:<line>` reference.

## Finding format

```
[blocker] <description> — `file:line`
[major]   <description> — `file:line`   [Waived: … — @<who>]
[minor]   <description> — `file:line`
[nit]     <description> — `file:line`
```

Rank: blockers first, then majors, minors, nits. End the review body with exactly:

```
Verdict: APPROVED
```

or

```
Verdict: CHANGES_REQUESTED
```

Never emit both; never paraphrase the tokens.
