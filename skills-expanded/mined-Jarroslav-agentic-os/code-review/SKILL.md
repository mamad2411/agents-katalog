---
name: code-review
description: >-
  Standalone, on-demand multi-lens code review of local git changes, outside any
  managed SDLC pipeline. Invoke when the user says "code review", "review my
  changes", "review my code", "review my branch", "review staged changes",
  "review this diff", or "run a code review" — and no pipeline is already
  driving the review. Resolves a review scope, materializes a diff, hands it to
  the review orchestrator, and renders the machine verdict. Read-only (R0):
  reports findings, never edits source, never applies fixes, never commits.
  Not for: pipeline-managed review gates (code-review-orchestrator via gate-arbiter), editing code, or applying the fixes it recommends.

---

# code-review

On-demand, git-native code review for a working copy. You resolve a scope, write
the diff to a file, invoke the downstream orchestrator inline, then read back and
render its verdict. You do three things and nothing more:

> **Prepare context → Invoke orchestrator → Present verdict.**

When invoked inside a managed run, persist review evidence and the gate decision
through the runtime authority described in
`../../references/runtime-authority.md`. The review artifact is a human-readable
output; it does not itself advance lifecycle state.
Use `legacy.export` when older ledger readers need a refreshed compatibility
view; do not append a review verdict directly to JSONL.

All the actual review reasoning — the `blind`, `edge-case`, and `acceptance`
lenses, standards/security adjudication, finding triage, and the machine verdict —
lives in the `code-review-orchestrator` skill. You do not reason about the code
yourself and you do not duplicate lens logic. Reuse the orchestrator's folded
lens definitions at `../code-review-orchestrator/references/review-lenses.md`;
do not restate or diverge from them.

## Blast radius

`R0` — read-only. You compute diffs and write run artifacts under a run directory.
You never modify tracked source and never apply a fix the orchestrator recommends.

## Relationship to the pipeline

Managed SDLC entry flows (`sdlc-guided`, `sdlc-auto`, `sdlc-brief`,
`sdlc-engine`) route the review gate through `gate-arbiter`, which records the
verdict to a gate ledger and may escalate. This skill is the standalone
front-door: it calls `code-review-orchestrator` **directly**, bypassing
`gate-arbiter` entirely — no gate ledger, no escalation.

Two shared gate-arbiter gate ids exist for this review; keep both verbatim:

| Gate id | Round | Used by this skill? |
|---|---|---|
| `code-review.final` | First/final review of the complete change | Yes — this is the gate you invoke under |
| `code-review.check` | Follow-up check round re-scoring prior findings | No — pipeline check-rounds only |

Because you only ever run `code-review.final`, the verdict carries no
`finding_status` field, and you never pass `prior_verdict` or `memory_brief`.

## Inputs

| Input | Required | Meaning |
|---|---|---|
| `target` | optional | Scope in the user's words: a range, a named scope, and/or paths |
| `spec` | optional | Path to an acceptance-criteria / story doc for business review |

- **Absent `target` → ask, never guess.** Present the four git-native scopes.
- **Absent `spec` → no-spec mode.** Valid. It forces verdict `confidence` to `low`
  by design and leaves `business_review` empty. Not an error.
- **Paths are a filter, never a scope.** A bare path still requires resolving one
  of the four scopes first, then applying the paths as a `-- <paths>` filter.

## Step 1 — Prepare context

### 1a. Confirm git

Run:

```
git rev-parse --is-inside-work-tree
```

Not inside a work tree → tell the user this skill is git-native and stop.

### 1b. Resolve scope

| Target shape | Action |
|---|---|
| Explicit range (`a..b`) or named scope | Use it; skip the scope question |
| Paths only | Resolve a scope (ask/confirm), then apply paths as `-- <paths>` |
| Ambiguous (not clearly range / named scope / existing path) | Ask to disambiguate |
| Absent | Present the four scopes via a user-question prompt |

When you must ask, compute a **per-scope one-line diffstat preview first** so each
choice shows its size:

```
git diff --stat <range> -- . ':(exclude)package-lock.json'
```

The four git-native scopes:

| Scope | Reviews | Range command |
|---|---|---|
| Branch vs base | Everything the branch added since divergence | `git diff <merge_base>...HEAD` |
| Staged | Changes staged for commit | `git diff --cached` |
| Working tree | All uncommitted changes vs HEAD | `git diff HEAD` |
| Explicit range | A user-named commit range | `git diff <from>..<to>` |

**Base resolution order** (for the branch-vs-base scope):

1. Configured base in the git-workflow guide (`.agentic/guides/standards/git-workflow.md`)
2. Repo default branch
3. `main`

Then: `git merge-base <base> HEAD`.

- Base branch missing, or `git merge-base` fails (unrelated / shallow history) →
  do **not** build `<unresolved>...HEAD`. Ask for a base/range, or offer the
  working-tree scope.

### 1c. Materialize the diff

Follow the canonical recipe in `../../references/diff-materialization.md`. Do not
invent a divergent recipe.

- Create the run directory, e.g. `docs/superpowers/reviews/<UTC-date>-<short-slug>/`.
- Write the diff to `<run_dir>/code-review.diff`.
- The mandatory exclusion filter applies to every diff command:
  `':(exclude)package-lock.json'`.
- **Untracked files** are appended for the **working-tree scope only** — never for
  staged, branch-vs-base, or explicit-range. To list and append:

  ```
  git status --porcelain=v1 -z --untracked-files=all -- <paths>
  git diff --no-index /dev/null <file>
  ```

  Split `?? ` entries on NUL, honor the path filter, and exclude `<run_dir>`
  itself. `git diff --no-index` exits 1 when there is a diff — that is normal,
  not an error.
- Optional integrity signature: `sha256sum <run_dir>/code-review.diff`. Omit the
  `signature` field rather than pass a placeholder.

**Error handling in this step:**

- Any `git diff` errors (bad ref/revision/pathspec) → surface the error and
  re-ask. Never proceed with a partial diff file.
- **Empty diff** after materialization → tell the user "no changes in that scope",
  offer another scope, and do **not** invoke the orchestrator. An empty diff makes
  the orchestrator emit false-approve sentinels.

## Step 2 — Invoke the orchestrator

Call `code-review-orchestrator` via the **Skill tool, inline** — not as an Agent
subagent. Pass:

| Param | Value |
|---|---|
| `gate_id` | `"code-review.final"` |
| `original_task` | e.g. `"Standalone review of <scope> on branch <branch>"` |
| `run_dir` | the Step-1 run directory |
| `artifacts` | the ArtifactRefs map below |

Do **not** pass `prior_verdict` or `memory_brief` (those are check-round /
pipeline-only).

**ArtifactRefs schema** — `diff` is the only required entry; include the others
only when the file is discovered. `signature` is an optional sha-256.

```json
{
  "diff":         {"kind": "diff", "path": "<run_dir>/code-review.diff", "summary": "<diffstat>", "signature": "<sha-256>"},
  "spec":         {"path": "<spec path>", "summary": "...", "signature": "..."},
  "git_workflow": {"path": ".agentic/guides/standards/git-workflow.md", "summary": "..."},
  "code_quality": {"path": ".agentic/guides/standards/code-quality.md", "summary": "..."},
  "security":     {"path": ".agentic/guides/development/security-patterns.md", "summary": "..."}
}
```

Optional context files to look for and attach when present:

- `.agentic/guides/standards/git-workflow.md` (also the base-branch config source)
- `.agentic/guides/standards/code-quality.md`
- `.agentic/guides/development/security-patterns.md`
- the spec/story, e.g. under `docs/stories/**`

The orchestrator writes its verdict to `<run_dir>/code-review-final.json` and
returns control to you. (Its check-round sibling would write
`<run_dir>/code-review-check.json`; you never trigger that here.)

## Step 3 — Present the verdict

Read `<run_dir>/code-review-final.json`. The verdict shape is defined in
`../code-review-orchestrator/references/verdict-schema.md` — treat that as
authority.

Render-critical keys:

| Key | Type |
|---|---|
| `decision` | enum: `Approve` / `request-changes` |
| `confidence` | enum incl. `low` |
| `rationale` | string |
| `risk_flags` | array (present even when empty) |
| `business_review` | array (present even when empty) |
| `standards_review` | array (present even when empty) |
| `findings` | array (present even when empty) |

- `findings[]` fields: `id`, `title`, `file` (`:line` when present), `problem`,
  `impact`, `recommendation`, `severity`.
- `business_review[]`: criterion → status.
- `standards_review[]`: `commit-format` / `code-quality` / `security` → status.
- `risk_flags[]` examples: `security`, `breaking-change`, `public-api`.
- `finding_status` is a check-round field and is correctly **absent** at
  `code-review.final`.

**If the verdict file is missing, unparseable, missing a render-critical key, or a
key has the wrong type** → tell the user the review did not complete and why, then
stop. Do not improvise a verdict.

**Safe-fail sentinel (verbatim rule).** If the verdict is
`decision: "request-changes"` **and** `confidence: "low"` **and** `risk_flags`,
`business_review`, `standards_review`, **and** `findings` are all empty → the
review could **not** run. Do **not** present this as genuine changes-requested.
Report the non-run and its likely reason (commonly an empty or unreadable diff),
then stop.

Otherwise, present the decision, confidence, rationale, risk flags, the standards
and business review rows, and each finding. You present only — you do not patch
findings, apply fixes, edit source, or commit review artifacts.

## References

| Path | Use |
|---|---|
| `../../references/diff-materialization.md` | Canonical diff recipe (Step 1c) |
| `../code-review-orchestrator/references/review-lenses.md` | Folded `blind` / `edge-case` / `acceptance` lens defs — reuse, don't restate |
| `../code-review-orchestrator/references/verdict-schema.md` | Verdict shape for rendering (Step 3) |

## Non-goals

- PR/MR review by number (`gh pr diff <n>`) — a future cascade; git-native only for v1.
- Applying fixes or present-and-act — this skill is present-only.
- Editing source, patching findings, or auto-committing review artifacts.
- Routing through `gate-arbiter` — only the SDLC entry flows do that.
- Modifying `code-review-orchestrator` or inventing a competing review method.
