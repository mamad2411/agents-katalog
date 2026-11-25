---
name: explore-index
description: Consult a small persistent index of what was already learned about this repo before running broad searches, so exploration stops repeating itself. Use when you need to find where something lives, before grepping or globbing across a repo you have not fully navigated this session, when a symbol or concept does not appear to exist, or when deciding whether a subsystem has already been traced. Covers proven-absent facts, concept-to-region pointers, and repo conventions. Not for ordinary edits to a file you already have open.
license: MIT
metadata:
  version: "0.2.0"
  stage: "experimental"
---

# Explore Index

Find where something lives without paying for the same search twice.

## The rule

An exploration is wasted when it re-derives a fact this repo already settled. Before a
**broad** search — repo-wide grep, glob sweep, or opening files to see what is inside — check
`.explore/INDEX.md` if it exists.

**Do not check when** the code is already in front of you. If you just read a file, or the
target directory is already open, navigate directly. The index pays off at subsystem
boundaries, not on every tool call.

## A hit is binding, not advisory

This is the whole point of the index. A row that matches is a **ceiling**, not a suggestion.

- `ABSENT` → the answer is no. **Stop searching.** Do not run the synonym family. Do not
  glob for `withRetry`, `retryWith`, `sendWithRetry`. The absence was already proven.
- `REGION` → go straight to that directory. Do not sweep the repo first.
- `RULE` → follow it. It replaces a search, not one step of it.
- `REAL` → read that one file. You are done searching for this question.

After a row resolves your question, the search is over. Going back to grep anyway means you
paid for the index **and** the search.

Broad searches are the expensive part. Each one enlarges the context that every later step
must re-read, so three repo-wide greps cost far more than their own output suggests.
Budget **at most 3 broad searches per task**, and only when no row covers it.

## Read narrow, not whole

When no row covers the question you are still hunting. A single large read is
expensive in a compounding way: everything you pull in is re-read on every later
step. Opening a 70KB module to "see what's in it" can cost more than the entire
rest of the task.

- `grep` or `glob` to find the symbol or section first, then `read` with
  `offset`/`limit` around it.
- If you must confirm a file exists, read the top ~60 lines, not the whole file.
- Only widen when the narrow read actually failed to answer the question.

Narrow reads are the difference between a 60k run and a 260k one on the same task.

## The loop

1. **Cold subsystem, broad search coming?** Read `.explore/INDEX.md`.
2. **Matching row?** Follow it and stop, per the rules above.
3. **No row?** Search normally, then journal what you learned.
4. **Every search journals a line** — hit or miss. That is what makes the next one cheap.

## Rules that matter

- **Never let the index state a fact about code.** It routes; it does not answer. A wrong row
  must cost you one wasted hop, never a confident wrong answer.
- **Absent is an answer.** If the index says a symbol does not exist, that ends the search.
  Do not try `with_backoff`, then `backoff_retry`, then open three files hoping.
- **Anchor, never line numbers.** Line numbers rot the moment anything above them changes,
  including edits you make yourself.
- **Do not store symbols or signatures here.** A repo map already derives those
  deterministically. This index is only for what a parser cannot know.
- **Below ~20 files, ignore all of this.** Read the repo. It fits.

## Writing an entry

One line, four fields:

```
<label> :: <kind> :: <target> :: <note, max 12 words>
```

| Kind | Target | Meaning |
|---|---|---|
| `ABSENT` | search scope | proven not to exist in that scope |
| `REGION` | directory | a concept lives here |
| `RULE` | short text | a convention or gotcha |
| `REAL` | path | repomap missed it; here it is |

Examples:

```
shared retry helper :: ABSENT :: src/** :: searched backoff, retry, sleep; every service inlines it
auth entry point :: REGION :: src/auth :: middleware chain starts at index.ts
imports use @/ alias :: RULE :: tsconfig paths; never relative parent paths
billing totals :: REAL :: packages/billing/src/totals.ts :: not in repomap, small module
```

Journal with the bundled script so the format stays consistent:

```bash
bash scripts/journal.sh "shared retry helper" ABSENT "src/**" "searched backoff, retry, sleep"
```

Then rebuild the index (deterministic, no model judgment):

```bash
bash scripts/reindex.sh
```

## Validity

Entries can rot. Before trusting a row, confirm the anchor still exists:

```bash
bash scripts/verify.sh
```

Rows whose anchor is gone are dropped on rebuild. If you edit a file that several rows point
at, run `verify.sh` after — a touched file makes every row naming it suspect.

## Scope

Session-scoped by default. Promoting this index into the repo is a human decision, never
automatic — an index that outlives the code it describes is a lie with extra steps.

Full detail: `references/PROTOCOL.md` (lookup and journaling), `references/ENTRY-FORMATS.md`
(entry schemas and worked examples).
