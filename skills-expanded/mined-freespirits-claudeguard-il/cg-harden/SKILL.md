---
name: cg-harden
description: Generate paste-ready hardening code (guards) for ClaudeGuardIL findings and for the coverage rows the rules could not decide, without modifying files. Use when the user types /cg-harden or asks for the fix, the guard, RLS policy, validation, headers, or middleware for a finding.
argument-hint: "[finding-id | domain | all]"
allowed-tools: [Read, Glob, Grep]
user-invocable: true
---

# /cg-harden — generate guards (no file changes)

Produce the concrete fix for one or more findings, tailored to the user's actual code. This
**does not edit anything** — it outputs code to paste. To apply automatically, use `/cg-fix`.

Argument: `$ARGUMENTS` — a finding id (`CG-DB-001`), a domain (`web`), or `all` (default: the
findings and coverage from the most recent grader run).

## Your input is the graded output

`grader.mjs` returns `findings` and `coverage`. Both are guard targets, for different reasons.

Per finding, the fields you need:

- **`guard`** — `guard-recipes/<name>.md#<anchor>`, resolved against
  `${CLAUDE_PLUGIN_ROOT}/skills/claudeguard/references/`. That anchor is the recipe. Open it.
- **`evidence`** — **an object**: `{ strength, nameOnly, why, at: [...] }`. `evidence.at[]` holds
  `{ file, line, snippet }` — where the guard goes. `evidence.why` is the mechanism, and it belongs
  in your summary. (In v1 `evidence` was the bare array that is now `evidence.at`.)
- **`severity`**, **`confidence`**, **`provenance`**, **`assumption`** — for ordering and for
  telling the user how much to trust the finding you are about to have them act on. Do not
  recompute them; the grader is the only authority on severity and confidence.

Unlike `/cg-fix`, you are not restricted to `confirmed` findings — you write code, you do not apply
it, and a human reads the diff before it lands. But say plainly which is which: a `likely` finding
from a reviewer and a `confirmed` one from a rule warrant different urgency, and the `assumption`
field is what the user checks before pasting.

## Coverage rows are guard targets too

`coverage.<set>.undeterminable` rows are **not findings** — no rule could establish anything about
them — and that is exactly what makes them good places to harden. A route whose auth could not be
verified is the ideal spot for an explicit, checked guard: adding one converts "we could not tell"
into "it is enforced here, in one readable line". Same for a `SECURITY DEFINER` function whose auth
check could not be shown to gate the body, and for an LLM call site whose limits could not be
confirmed.

Treat them honestly. The header is not "N more problems" — it is "N places nothing could be
proved". Manufacturing severity for an undeterminable row is grading, and grading belongs to
`grader.mjs`.

Two rows deserve special handling:

- **`coverage.tables.undeterminable`** with a non-null `verifyQuery`: the guard is to run that
  query against their own database first. Writing an RLS policy for a table whose RLS state nobody
  knows can just as easily break a working app as protect an open one.
- **`coverage.dynamicTableRefs`**: `.from(x)` computed at runtime. No per-table guard can be
  written, so the guard is structural — pin the set of allowed table names, or replace the generic
  helper with explicit calls.

## Steps

1. Resolve the target findings and coverage rows. If nothing is in context, run the `/cg-scan`
   workflow first.
2. For each finding, open its `guard:` recipe anchor and **adapt** the snippet to the user's real
   files at `evidence.at[]`: their table/column names, route paths, framework, env var names. Read
   the relevant source with Read/Grep so the guard drops in cleanly.
3. Output per finding:
   - a one-line HE + EN summary of the fix, plus `evidence.why` so the user sees the mechanism,
   - the exact code to paste and **where** it goes (`file:line` / new file path),
   - any follow-up steps that aren't code (rotate a key, run a migration, set a server env var),
   - a verification line ("re-run `/cg-scan`; for RLS also `/cg-live`").
4. Order findings by severity (P0 first), then confidence (`confirmed` first). Group multi-file
   fixes clearly.
5. Then a separate, clearly labelled section for the coverage-derived guards: subject, the note
   saying why the rule stopped, and the guard that would settle it. These are hardening
   suggestions, not findings — label them that way.

Prefer reusing the project's existing utilities (its Supabase client, its validation lib, its
middleware) over introducing new dependencies. If a fix needs a new package, say so explicitly.
