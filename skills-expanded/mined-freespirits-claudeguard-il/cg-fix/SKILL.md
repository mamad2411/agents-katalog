---
name: cg-fix
description: Apply ClaudeGuardIL guards to the codebase (opt-in auto-fix) for findings the grader marked confirmed and autofixable, dry-run diff first and review before writing. Use when the user types /cg-fix or asks to automatically fix, patch, or apply the security fixes. Only touches the codebase, never a live target.
argument-hint: "[finding-id | all] [--apply]"
allowed-tools: [Read, Glob, Grep, Edit, Write, Bash]
user-invocable: true
---

# /cg-fix — apply guards (opt-in, dry-run first)

Apply the hardening code to the codebase. **Safety-first and non-destructive by default:** show a
diff, get confirmation, then write. Never touches a live target — only source files.

Argument: `$ARGUMENTS` — a finding id or `all` (default: every eligible finding from the latest
grader run), plus optional `--apply` to write after review.

## Eligibility — both conditions, no exceptions

A finding may be auto-fixed only if:

```
finding.confidence === 'confirmed'   AND   finding.autofixable === true
```

Neither field is yours to set. `confirmed` comes only from `evidence.strength === 'definitive'` —
the bundler inlines the prefix, the migration never enables RLS, the header was absent on the wire.
Everything else caps lower: `strong` → `likely`, `weak` → `needs-review`, and a reviewer's
`judgement` → `likely` and can never reach `confirmed`. So a reviewer finding is never eligible
here, however well argued. Editing someone's source on the strength of a guess is how a security
tool becomes the thing that broke production.

Skip everything else and say why in one line — "needs a human: the check may live in a helper this
pass does not follow" — with the finding's `assumption`, so the user knows what to check rather
than just that it was skipped.

## The finding schema you are reading

`grader.mjs` emits, per finding:

- **`guard`** — `guard-recipes/<name>.md#<anchor>`, resolved against
  `${CLAUDE_PLUGIN_ROOT}/skills/claudeguard/references/`. This is the fix. Open that anchor; do not
  invent a patch from the title.
- **`evidence`** — **an object**, not an array: `{ strength, nameOnly, why, at: [...] }`.
  - `evidence.at[]` is the location list: `{ file, line, snippet }` per entry. This is where the
    patch goes.
  - `evidence.why` is the mechanism in one sentence — use it in the diff summary so the user reads
    *why* before approving a write.
  - Schema change from v1: evidence used to be the bare array that is now `evidence.at`. Code or
    habits that reach for `finding.evidence[0].file` now get `undefined` and will patch nothing, or
    the wrong file, without complaining.
- **`severity`**, **`confidence`**, **`provenance`**, **`tier`**, **`assumption`**, **`id`**,
  **`subject`** — for grouping and for the summary. Never recompute any of them.

If `evidence.at` is empty there is nowhere to patch — coverage-shaped findings such as
`CG-DB-COVERAGE` are like this. Skip them and route them to `/cg-harden`.

## Rules

- **Never auto-do the irreversible-but-not-code parts.** Rotating a leaked key, running a
  production migration, or changing hosting env vars are listed as manual steps, not performed.
- **Dry-run by default.** Without `--apply`, produce the full diff and stop.
- A live target is never touched. Fixes land in source.

## Steps

1. Resolve eligible findings from the latest grader output. If none is in context, run the
   `/cg-scan` workflow first — do not re-derive findings by reading code, because a fix applied to
   a finding that was never graded is a fix nobody can reproduce.
2. For each, open the `guard:` recipe anchor and adapt it to the real files at `evidence.at[]`:
   their table/column names, route paths, framework, env var names. Read the surrounding code so
   the guard drops in cleanly.
3. **Present a unified diff** per file, grouped by finding, headed with the id, severity,
   confidence and `evidence.why`. Summarize in Hebrew + English.
4. If the user did not pass `--apply`, stop here and ask them to review. If they confirm (or passed
   `--apply`), write the changes with Edit/Write.
5. After applying: list the remaining **manual** steps (key rotation, migrations, env changes), then
   re-run the grader:

   ```bash
   node ${CLAUDE_PLUGIN_ROOT}/scripts/grader.mjs <path>
   ```

   Report the before/after `verdict` and `counts` — both `bySeverity` and `byConfidence`. A P0 that
   moved from `confirmed` to gone is a fix; a P0 that merely stopped being detectable is a
   regression in evidence, and the two look identical if you only compare P-counts.

Prefer minimal, idiomatic diffs that match the surrounding code. If a fix is risky or ambiguous,
downgrade it to a `/cg-harden` suggestion rather than writing it.
