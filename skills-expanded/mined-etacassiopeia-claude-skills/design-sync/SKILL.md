---
name: design-sync
description: Keep a repository's design docs and code in sync with ONE source of truth — a decision register (`D-n`), citation grammar, amendment callouts, a deterministic coherence check (`design-check.py`), a verification index, and the three moments (before / during / after a change) where drift is born. TRIGGER when bootstrapping the practice in a repo ("set up design sync", "decision register", "keep docs and code in sync"), when a repo declares `design-check:` in its CLAUDE.md/AGENTS.md, when asked whether design docs still describe the code, or when a decision is reached mid-task that has no home. Usage — /design-sync [bootstrap|check|diff|verify <doc>|record]
---

# design-sync — one source of truth for design and code

The failure this skill targets: a decision that lived in a context that no longer exists — a
chat, a memory file, a vault note, an issue comment — being re-derived differently next session.
The cure is not spec-first development and not doc generation; it is **one home for decisions,
citations from the code that embodies them, and a mechanical check that the two still agree**.

Reference implementation and rationale: `rift-cluster`'s `docs/process/design-code-sync.md`
(this skill's `templates/PROCESS.md` is the project-agnostic copy). Evaluated and not adopted:
[lid](https://github.com/jszmajda/lid) — spec-authoritative and unidirectional; its three good
mechanisms (grep-able IDs, a coherence check, a status index) are what this skill installs, plus
the code→design direction lid lacks.

## Detecting a repo that has the practice

Any of: `scripts/design-check.py` exists · CLAUDE.md/AGENTS.md carries a line
`design-check: <path>` · `docs/decisions/DECISIONS.md` exists. Other skills (`/fix-issue`,
`/ship-issues`) key off this and add their design steps **only** when it is detected.

## Modes

### `check` — is the repo coherent right now?

```sh
python3 scripts/design-check.py            # full report
python3 scripts/design-check.py --strict   # what CI runs: errors fail, warnings print
```

Errors are structural (a citation that resolves to nothing, an amended section with no callout,
a malformed register entry). Warnings are the backlog (an active decision no code cites, a doc
whose code changed after it was last verified). Read the coverage table at the end: a decision
with `0 / 0` is one nothing enforces.

### `diff` — the change-time question, both directions

```sh
python3 scripts/design-check.py --diff                     # uncommitted vs HEAD
python3 scripts/design-check.py --diff <ref-or-worktree>   # a branch's changes vs its merge-base
```

- **CODE → DESIGN**: every decision/section the changed code cites, and whether that document
  was touched in the same change. `[NOT changed]` means: confirm it still holds, or amend it.
- **DESIGN → CODE**: for each changed document, the code that cites the *changed sections*, so
  those citations get re-read.

Run it **before** writing code (read what the design says about the area) and **before** the
PR (answer the question explicitly in the PR body — see `record`).

### `verify <doc>` — record that a document was re-read against the code

```sh
python3 scripts/design-check.py --mark-verified docs/architecture/06-flow-state.md
```

Only after actually re-reading it. The index (`docs/design-index.toml`) records the sha; the
tool records the claim, it does not make it true. Never bulk-mark.

### `record` — a decision reached mid-task

A decision is *not made* until it is a `D-n` in the register. When, during any task, you:

- chose between real alternatives another engineer could reasonably choose otherwise,
- made the code do something a doc says it does not,
- received a ruling from the user or a reviewer on a should-question,
- found the design wrong and built the right thing,

then in the **same PR**: add the entry (status, decided-where, `Amends:` if it changes a spec
section, `Code:` anchors), put the `> **Amended by D-n**` callout at every amended section, cite
the `D-n` from the embodying code, and pin it with a test whose doc comment states the claim
(`/// Pins D-n: …`). The PR body then carries `Design: amended — D-n (<one line>)`.

The PR body line is mandatory in one of three forms — silence is not an option:
`Design: unchanged — <docs>, confirmed` · `Design: amended — D-n` · `Design: n/a — <why>`.

**Memory vs. intent.** Before saving anything to agent memory: would a fresh agent, in any
tool, next session, need this to build the system *right*? Then it is intent → register. Memory
keeps at most a pointer. Memory is for how the *work* goes, not what the *system* is.

### `bootstrap` — install the practice in a repo that lacks it

Read `templates/PROCESS.md` first; it is the contract. Then, in order — each step leaves the repo
consistent, so stop anywhere:

1. **Inventory where intent lives today.** RFCs/ADRs/design docs in the repo; any existing
   decision log (an ADR "decisions" list, an RFC appendix — these are the seed); the issue
   tracker (closed-as-not-planned, "we chose X", "by design", "instead of" — an agent sweep over
   all issues is worth it: rift-cluster had ~25 decisions living *only* in issues); external
   notes/vault; agent memory files that state design facts. Write the inventory down before
   changing anything — it is the drift report the user never had.
2. **Create the register** from `templates/DECISIONS.md` (keep its "How to read an entry" and
   "Citation grammar" — they are the contract the check parses). *Move* every existing decision
   log into it; leave pointers behind, never a second copy. Add the issue-only decisions. Number
   continues from the highest existing id.
3. **Install the check**: copy `templates/design-check.py` to `scripts/`, adjust the constants at
   the top (`CODE_ROOTS`, `RFC_DIR`, `ADR_DIR`, `SEAMS_DOC`, heading regexes) to the repo's
   layout, and copy `templates/test_design_check.py` beside it. Run it. **The first run's error
   list is the drift inventory** — fix the real ones (missing callouts, ids nobody defined),
   tune the resolver for the false positives (upstream numbering spaces, vendored docs,
   fixture files → `design-check: ignore-file`).
4. **Create the index** from `templates/design-index.toml`: one table per design doc, `code`
   globs for what it describes, `verified_sha = ""` everywhere. Verify docs as they are actually
   re-read.
5. **CI**: a job running `python3 scripts/design-check.py --strict` (stdlib only; needs
   `fetch-depth: 0` for the staleness check).
6. **Instruction file**: a short block in CLAUDE.md/AGENTS.md — authority order, the
   `design-check: <path>` line, the three moments, the memory-vs-intent rule. If CLAUDE.md is
   gitignored in that repo (a global ignore is common), the tracked contract is the process doc
   under `docs/process/`; the CLAUDE.md block just points at it.
7. **External copies**: any vault/notes file that mirrors a repo doc becomes a pointer; analyses
   get a "derived — not normative" banner naming what they fed. Memory files that state design
   facts become pointers at the `D-n`.
8. **Citations and pins** (the long tail): for each active decision with `0 / 0` coverage, cite
   it from the embodying code and pin it with a test. Area-by-area, by agents if large; each
   agent also re-reads the chapter for its area against the code and either fixes the doc or
   reports the drift, then marks it verified.

## What this is not

- **Not spec-first.** Code corrects the design routinely; the requirement is that the
  correction is recorded as a decision, not that the spec is rewritten before code exists.
- **Not doc generation.** Prose generated from code is a third source of truth.
- **Not a gate on prose accuracy.** The check gates structure; whether a chapter is *true* is
  a reading, recorded honestly in the index (and the index says when nobody has done it).
