---
name: auto-pr
description: Use when the user invokes `/auto-pr <repo-url>` or asks to "open N PRs against <repo>", "auto-contribute to <repo>", or "raise mergeable PRs automatically". Wraps the `vouch auto-pr` CLI: points at any github repo, learns its contribution norms (from shipped guidance, else synthesized from merged PRs), sources work items (open issues first, then agent-discovered improvements), and drives claude/codex to fix each one — alternating fixer and reviewer — opening a PR only when the repo's own test gate is green and the reviewing engine signs off.
---

# auto-pr

**Goal:** point at any github repo and open N *mergeable* PRs — not N PRs.
each one resolves a real issue (or a genuine discovered improvement), passes
the repo's own test gate locally, and is signed off by a second engine before
it ever reaches a maintainer.

this is a thin orchestration layer over the `vouch auto-pr` CLI. it is a
sibling tool to the knowledge base: it never writes to storage / proposals /
the audit log, and the review gate is untouched.

## invocation

```
vouch auto-pr <repo-url> \
  --workspace <dir> --count <N> \
  --claude-effort <low|medium|high|max> \
  --codex-effort  <low|medium|high|max> \
  [--issue-label good-first-issue] \
  [--fork-owner <login>] \
  [--max-revise 2] [--autonomy edit|full] \
  [--dry-run] [--json]
```

`<repo-url>` may be `https://github.com/<owner>/<name>`,
`git@github.com:<owner>/<name>.git`, or the `<owner>/<name>` shorthand.

output: the URLs of the PRs that were actually opened (one per line, or a JSON
array under `--json`). attempts that fail verification are reported on stderr
as *skipped* with a reason — they are never opened. **M genuine PRs beats N
shaky ones**; partial success is the intended behaviour, not an error.

## prerequisites

- **`gh` CLI** authenticated for the target repo (`gh auth status` returns a
  session). used for fork/clone, issue listing, dedup search, and PR creation.
- **`claude`** (Claude Code) and **`codex`** on `PATH` — both engines are used;
  one fixes while the other reviews, alternating per PR.
- **`vouch` CLI** on `PATH` (`pip install vouch-kb`).

if `claude` or `codex` is missing, **stop and tell the user** — cross-verify is
the whole point; don't silently fall back to a single engine.

## how it works (the pipeline)

1. **resolve workspace** — if `--workspace` is already a clone, use it; else
   `gh repo fork --clone` (or a plain clone when you have push access). sync the
   default branch.
2. **detect-or-bootstrap guidance** — scan the repo for `CONTRIBUTING.md`,
   `AGENTS.md`, `CLAUDE.md`, `.claude/skills/**/SKILL.md`, `.codex/`,
   `.github/PULL_REQUEST_TEMPLATE.md`. if any exist, they become fixer/reviewer
   context. **if none exist, fetch the repo's merged PRs and synthesize a
   contribution `SKILL.md`**, written into the clone's `.claude/skills/` (and a
   `.codex/` mirror) so it's reused next run.
3. **source N work items** — open *unassigned* issues first (filterable by
   `--issue-label`); if fewer than N survive dedup, let the engines discover
   genuine bugs/improvements to fill the remainder. every candidate is
   dedup-checked against the repo's existing PRs.
4. **per item** (isolated `auto-pr/<slug>` branch): the fixer engine edits +
   commits; the repo's own gate runs (`make check` / `pytest` / `npm test` /
   `cargo test` / `go test`); the *other* engine reviews the diff. a red gate or
   a rejection feeds back to the fixer for up to `--max-revise` rounds. still
   failing ⇒ skip with a reason. passing ⇒ push to the fork and `gh pr create`.

## house rules it enforces

- conventional-commit titles; lowercase prose bodies.
- **no `Co-Authored-By` / AI-attribution trailer** in generated commits.
- dedup before opening — no Nth duplicate of a tried/rejected fix.
- the repo's own CI-equivalent gate must be green locally before a PR opens.
- one logical change per PR; link/close the issue it addresses.

## effort levels

`--claude-effort` / `--codex-effort` tune each engine independently:

| level | claude model | codex reasoning |
|---|---|---|
| low | haiku | low |
| medium | sonnet | medium |
| high | opus | high |
| max | opus | high (codex cap) |

(claude models are passed as aliases — `opus`/`sonnet`/`haiku` — so the tool
tracks the latest model in each tier. `high` and `max` both select opus; codex
caps reasoning effort at `high`.)

use `high` for real contributions; drop to `low`/`medium` only for cheap
exploratory runs. start with `--dry-run` against a new repo to see what it
*would* open before spending an engine on the real thing.

## autonomy & safety

the fixer drives the engines headlessly against a clone of an *untrusted*
third-party repo, so the default is constrained:

- `--autonomy edit` (default) — claude `acceptEdits` (auto-accepts file edits,
  no arbitrary command execution) and codex `--sandbox workspace-write`
  (writes confined to the clone, no network). sufficient for most fixes, since
  the test gate runs through vouch's own runner, not the engine.
- `--autonomy full` — escalates claude to `bypassPermissions` (the engine may
  run arbitrary commands with no permission prompt). only use this for repos
  whose fix genuinely needs to run commands, and only on repos you trust enough
  to execute. it is an explicit, per-run operator choice — never the default.

reviewing is always read-only (claude `plan` / codex `read-only`).

## failure semantics

- workspace resolution fails ⇒ the whole run aborts; nothing was opened.
- no work items ⇒ exit cleanly with "nothing to do".
- a single item fails (no diff, red gate, rejected past the cap, push/`gh`
  error) ⇒ that item is skipped with a reason; the batch continues.
- a missing engine binary ⇒ fail fast naming the binary.
