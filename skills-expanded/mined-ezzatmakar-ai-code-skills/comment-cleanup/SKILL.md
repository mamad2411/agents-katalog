---
name: comment-cleanup
description: Sweeps a codebase and rewrites its code comments in place to one standard — short (1-line default, 3-line cap), sorted (canonical docblock tag order), correctly placed (attached to the declaration, no detached or trailing essays), and consistently marked (TODO with a tracked issue). Deletes comments that restate the code, banner art, commented-out blocks, changelog-in-comments, and assistant filler; adds a docblock only to non-obvious public API. Use when asked to clean up, shorten, sort, standardize, or fix code comments and docblocks — "my comments are too long", "sort the docblocks", "remove the useless comments", "normalize the JSDoc/PHPDoc/docstrings". Edits comments only, never executable code, and always previews the plan before touching a file. Do not use for rewording comments into plainer, more direct English (use rephrase-code-comments), writing prose documentation, README files, PR review comments, or commenting out code.
license: MIT
compatibility: Requires git and python3 (3.8+, standard library only). Stack-agnostic — handles C-style, hash, SQL, HTML, CSS, Lua, and Python comment syntax, and defers to the repository's own linter configuration when one exists. Designed for Codex and Claude Code using the Agent Skills open standard.
metadata:
  author: Ezzat Malak
  version: "1.0.1"
---

# Comment Cleanup

Sweep a codebase's **comments** and bring them to one standard: **short**, **sorted**, **placed**, **marked**.
This skill **edits by default** — it is not a report generator. Because it edits by default and sweeps the whole
repository by default, every run passes through a preview gate first, and it never touches a line of executable
code.

The standard and its sources are in [references/COMMENT_STANDARD.md](references/COMMENT_STANDARD.md). The
per-language docblock spellings are in
[references/LANGUAGE_CONVENTIONS.md](references/LANGUAGE_CONVENTIONS.md). The catalogue every finding maps to is
[references/ANTIPATTERNS.md](references/ANTIPATTERNS.md).

Two helpers do the mechanical work; resolve `<skill-directory>` from the loaded skill path:

- `<skill-directory>/scripts/scan-comments.py` — inventories every comment and flags candidates by rule ID.
- `<skill-directory>/scripts/detect-stack.sh` — summarizes the languages and tooling in play.

## Non-negotiable output

- **Comments only. Never executable code.** Not a rename, not a reorder, not a "while I was in there" fix. When a
  comment is only bad because the code is unclear, **report it and move on** — that is an `ESCALATE`, not an edit.
  Crossing this line turns a comment sweep into an unreviewed refactor. `git diff` at the end must contain no
  change to a non-comment line.
- **Refuse to start on a dirty working tree.** Run `git status --porcelain`. If it is not empty, stop and say so —
  the user must be able to `git diff` the whole result and `git checkout .` to undo it. Proceed only if they
  explicitly accept mixing the sweep into existing changes.
- **Preview before editing.** No file is modified before the user approves the plan (Phase 4). Never skip this,
  even when the scope is a single file.
- **Never delete information that is not recoverable from the code** — a licence header, a bug/spec link, a
  workaround rationale, or a **pragma** (`@ts-ignore`, `eslint-disable`, `# noqa`, `//nolint`, `//go:build`,
  `# frozen_string_literal`, …). Pragmas are code wearing a comment's syntax; deleting one changes behavior.
- **Never invent a tracking reference.** An un-owned `TODO` is reported, not rewritten into a fake issue number.
- **Never reproduce a suspected secret.** Report the file, line, and class of credential, redacted. Say plainly
  that deletion does not remediate it — the value must be rotated and the git history handled.
- **Preserve the repository's language.** Do not translate existing comments into English.
- **The repository's own configuration wins.** If a linter already encodes a comment rule, follow it over the house
  rule and say which one you deferred to.
- **Report faithfully.** State what was changed, what was deliberately left alone and why, and what was escalated.
  Never describe an edit you did not make.

## Phase 0: Resolve inputs

Determine these before doing anything else, then echo them back:

1. **Scope.** Default: **the whole repository**. Honor explicit paths, directories, or globs. Generated, vendored,
   minified, and lockfile paths are always excluded — `scan-comments.py` does this for you.
2. **Stance.** Default **minimalist**: assume most comments should not exist; keep the *why*; require a docblock
   only on non-obvious public API. The alternative, on request, is **conventional**: document every exported symbol.
3. **Line cap.** Default 3 for inline comments (`--cap N` to change).
4. **Apply or preview only.** Default: apply, after the Phase 4 gate. `preview only` stops after the plan.
5. **Clean tree.** Run `git status --porcelain` and apply the rule above.

## Phase 1: Detect the stack and the local rules

1. Run `<skill-directory>/scripts/detect-stack.sh` for the languages and tooling.
2. Read repository guidance when present: `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `README.md`.
3. **Find any comment rule the project already enforces**, and defer to it:
   - JS/TS — `eslint` `jsdoc/*`, `require-jsdoc`, `valid-jsdoc`, `spaced-comment`, `no-inline-comments`;
     `.prettierrc` print width.
   - PHP — `phpcs.xml` / `.php-cs-fixer.php` (`Squiz.Commenting.*`, `phpdoc_*` fixers).
   - Python — `ruff` `D` rules, `pydocstyle` convention (`google` / `numpy` / `pep257`), `flake8-docstrings`.
   - Go — `golangci-lint` `godot`, `revive` `exported`, `godoclint`.
   - Rust — `#![warn(missing_docs)]`, `clippy::missing_docs_in_private_items`.
   Never fight a configured rule. If the house standard and the project's config disagree, the config wins and you
   say so in the summary.
4. Note the **dominant existing convention** so rewritten comments do not look foreign beside their neighbours.

## Phase 2: Inventory

```bash
python3 <skill-directory>/scripts/scan-comments.py [paths...] [--cap N] [--json]
```

The scan reports, it never gates — it always exits 0. Every line is a **candidate, not a verdict**: the heuristics
cannot read intent. Useful flags: `--rules DUP,DEAD` to focus a pass, `--summary-only` for a baseline,
`--json` for structured input, `--max-per-file N` to bound output.

Rule IDs and their default dispositions:

| ID | Means | Default |
|---|---|---|
| `DUP` | restates the code beside it | `DELETE` |
| `LEN` | inline comment over the cap | `SHORTEN` |
| `ORD` | docblock tags out of canonical order | `REORDER` |
| `POS` | detached from its declaration, or a trailing essay | `REPOSITION` |
| `TODO` | marker with no tracked issue | `ESCALATE` |
| `DEAD` | commented-out code | `DELETE` |
| `BANNER` | divider or section art | `DELETE` (labelled dividers: `SHORTEN`) |
| `CHANGELOG` | version history that belongs in git | `DELETE` |
| `GENERATED` | assistant attribution or filler | `DELETE` |
| `EMPTY` | docblock adding nothing beyond the signature | `DELETE` |
| `SECRET` | possible credential in a comment | `ESCALATE`, redacted |

Three antipatterns are **not** scanner-detectable and are found only by reading: `STALE` (the comment contradicts
the code), `CONTAMINATE` (implementation detail in an interface comment), and `MISSING` (undocumented non-obvious
public API). Look for these in the files you open — a large scan result is not a substitute for reading.

## Phase 3: Classify

Open each flagged file and assign a disposition per candidate, using
[references/ANTIPATTERNS.md](references/ANTIPATTERNS.md):

`DELETE` · `SHORTEN` · `REORDER` · `REPOSITION` · `ADD` · `KEEP` · `ESCALATE`

Confirm the scanner's guess against the actual code — it does not know that a "duplicate" comment carries a *why*
clause, that a long comment encodes an algorithm's invariants, or that a commented-out block is a documented
example. Downgrade to `KEEP` freely and record the reason so the next run does not re-litigate it.

Bias hard toward `KEEP` for: config-file comments (often the only documentation of an option), test files (a
comment naming the scenario earns its place), and anything referencing an external system you cannot verify.

## Phase 4: Preview gate

**No file is modified before this passes.** Present:

1. Files to be touched and the count per rule ID.
2. The net effect — comments deleted, shortened, reordered, repositioned, added.
3. Two or three representative **before/after** pairs, including the most aggressive edit planned.
4. Everything being escalated rather than fixed (`TODO`, `STALE`, `SECRET`, unclear code).
5. Anything skipped and why (generated, vendored, linter-governed).

For a scope over ~20 files, write this to `COMMENT_CLEANUP_PLAN.md` at the repository root and give the path
instead of flooding the chat. Then get explicit confirmation. The user may narrow the scope, drop a rule, or
change the stance — re-plan rather than proceeding partially.

## Phase 5: Apply

Work in **batches of related files**, not one sweeping pass, so a bad batch can be reverted without losing the good
ones. After each batch:

1. Re-read what you changed and confirm every hunk is comment-only.
2. Keep the file's existing docblock dialect and alignment — you are normalizing order and length, not converting
   JSDoc to TSDoc or reflowing aligned PHPDoc columns.
3. Never leave a file mid-standard. If a docblock cannot be fixed without touching the signature, `ESCALATE` it and
   leave it untouched.

Then verify the batch (Phase 6) before starting the next.

## Phase 6: Verify

After each batch, and again at the end:

```bash
git diff --stat                      # scope check
git diff -U0 | grep -E '^[+-]' | grep -vE '^(\+\+\+|---)'   # every changed line
python3 <skill-directory>/scripts/scan-comments.py [paths...] --summary-only
```

1. **Read every changed line.** Each one must be either (a) wholly a comment or a blank line, or (b) a line whose
   **code portion is byte-identical** to its counterpart, differing only in a trailing comment that was removed or
   rewritten. Anything else — a renamed variable, a moved statement, a reformatted expression — violates the first
   non-negotiable rule. Revert it immediately.
2. Re-scan and confirm the counts moved in the expected direction, and that no new rule fired.
3. Run whatever the project already provides and is cheap: the linter, the type checker, and the focused tests for
   the touched files. A docblock edit can break a build — malformed C# XML docs, an unparseable rustdoc fence, a
   Go build constraint that lost its exact spacing. Do not claim a check passed if you did not run it.
4. If the project generates documentation (`typedoc`, `phpDocumentor`, `sphinx`, `cargo doc`, `godoc`), build it
   when that is cheap and confirm it still succeeds.

## Phase 7: Summarize

In chat, report concisely:

- Files changed and the counts by disposition.
- What was **escalated** and needs a human: un-owned `TODO`s, comments that contradict their code, suspected
  secrets (redacted), and any place where the comment was only bad because the code is unclear.
- What was deliberately kept, and which project linter configuration you deferred to.
- The verification commands you ran and their results.

Remind the user the whole sweep is one reviewable diff: `git diff` to inspect, `git checkout .` to undo.
