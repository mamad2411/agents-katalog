---
name: huicrew
description: >
  Decision guide for delegating to hui-style subagents. Tells main thread when
  to spawn `huicrew-investigator` (locate code), `huicrew-builder` (1-2 file
  edit), or `huicrew-reviewer` (diff review) instead of working inline.
  Subagents return intentionally terse structured findings. This skill does not
  measure or guarantee token, context, cost, latency, or quality outcomes.
  Trigger: "delegate to subagent", "use huicrew", "spawn investigator/builder/reviewer".
---

Huicrew = three subagent presets that emit concise structured output. Role semantics are portable; exact agent names, tool access, and host behavior depend on the installed host integration.

## When to use huicrew vs alternatives

| Task | Use |
|---|---|
| "Where is X defined / what calls Y / list uses of Z" | `huicrew-investigator` |
| Same but you also want suggestions/architecture commentary | Host exploration agent or main thread |
| Surgical edit, ≤2 files, scope obvious | `huicrew-builder` |
| New feature / 3+ files / cross-cutting refactor | Main thread or host architecture workflow |
| Review diff, branch, or file for bugs | `huicrew-reviewer` |
| Deep review with rationale + alternatives | Host code-review workflow |
| One-line answer already known | Main thread, no subagent |

Use Huicrew when a terse structured result is enough. Use host exploration/review workflows when detailed reasoning or prose is needed.

## Output contracts

**`huicrew-investigator`**

```
<Header>:
- path:line — `symbol` — short note
totals: <counts>.
```

Or `No match.` File-path-first, line-number-attached, backticked symbols.

**`huicrew-builder`**

```
<path:line-range> — <change ≤10 words>.
verified: <re-read OK | mismatch @ path:line>.
```

Or: `too-big.` / `needs-confirm.` / `ambiguous.` / `regressed.`

**`huicrew-reviewer`**

```
path:line: <emoji> <severity>: <problem>. <fix>.
totals: N🔴 N🟡 N🔵 N❓
```

Or `No issues.` Findings sorted file then line.

## Chaining patterns

**Locate → fix → verify**

1. `huicrew-investigator` returns candidate sites.
2. Main thread selects one or two scoped edits for `huicrew-builder`.
3. `huicrew-reviewer` audits resulting diff.

**Parallel scout**

Spawn separate investigator calls for definitions, callers, and tests. Aggregate in main thread.

**Single-shot edit**

When site is known, give exact `path:line` to builder directly.

## Boundaries

- Builder refuses scopes above two files.
- Investigator is read-only and does not propose fixes.
- Reviewer returns findings, not architecture decisions.
- Concise output can be cryptic. Paraphrase before presenting it directly to a human when needed.
- Security warnings, irreversible operations, and ambiguous instructions use normal clear language.
