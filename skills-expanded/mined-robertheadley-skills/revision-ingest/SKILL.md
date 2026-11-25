---
name: revision-ingest
description: Use when a human edits a generated document (Markdown, export, report) and the change must be merged back into the authoritative source that produced it. Diffs the two renderings as data, converts the delta into source records, keeps ids stable, and proves the result with independent gates.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [generated-documents, ingest, reconciliation, stable-ids, idempotency, verification]
    related_skills: [hermes-agent-skill-authoring, requesting-code-review, incremental-code-indexing]
---

# Revision Ingest

## Overview

A generated document — a catalog, a report, a spec, an index — is a **delivery format**, not a
source of truth. When a human edits that rendering and hands it back, the edit is real work that
must land in the data, and the temptation is to read the diff by eye and hand-transcribe.

That fails in a specific, expensive way: a revision that changed 31 of 448 records does not look
different from one that changed all 448. Edited prose is uniform. Only a programmatic diff tells
you which records moved, and a programmatic ingest makes the change reproducible, reviewable and
re-runnable.

This skill is that discipline: **parse both renderings into records, diff them as data, write the
delta back into the source, and let an independent gate prove the result.**

## When to Use

- A human returns an edited copy of a document your pipeline generates ("here's the updated
  version", an attachment, a reviewed export).
- An upstream revision arrives authored against a *different* numbering than yours.
- A record's identity must survive a rename, a re-rank, or a re-categorisation.
- You are tempted to hand-edit a generated file to fix one line. (Don't — fix the source.)

Don't use it for: prose documents with no per-record structure (merge those normally), or for
edits to the source files themselves (that is just editing).

## Core rules

These are the ones that cost real damage when skipped.

1. **Id stability beats positional ids.** If an id is assigned by sort position, then renaming or
   re-ranking *one* record renumbers its neighbours and silently repoints every reference to
   them — including references the revision itself makes. Pin ids to a stable key
   (`file:source_id`, a slug, a UUID) in a committed lock file, and only mint new ids for records
   the lock does not know. See [Id stability](#id-stability) below.
2. **Compare against the artifact the human actually edited** — the rendering, not the raw source.
   Renderings normalise things: they sort list fields, they union fields that merges folded
   together, they strip entries equal to the title. Comparing a rendering against raw source
   reports every record as modified and buries the real 31 changes in 400 phantoms.
3. **List fields compare as sets, case-insensitively.** A reordering is not an edit. Declaring
   one is how you end up rewriting 324 files and calling it an ingest.
4. **Ingest regenerates; it never appends a delta.** Writing "only the new records" means a second
   run writes nothing — an empty file that silently deletes everything the first run imported.
   Regenerate the imported section from the revision every time, and refuse to write when the
   parse yields nothing. Then *prove* idempotency by running it twice.
5. **The gate must re-derive, not compare.** An audit that checks stored values against stored
   values agrees with itself. Re-compute the classification from the evidence and fail on drift.
6. **A freshness check compares to the exact current set, never a floor.** `>= 460 urls checked`
   passed happily while 26 newly added citations had never been requested. Assert equality against
   the set that exists now.
7. **Read column positions from headers.** `row.split("\t")[2]` breaks silently the moment a column
   is inserted, and the break looks like a data error.
8. **Import the human's governing prose verbatim** as its own document. Do not paraphrase their
   policy into an existing file; the wording is the deliverable.
9. **Do not classify what the revision did not.** Record `unclassified` and hand the decision to
   the host. Inventing classes is inventing policy.
10. **Encode the revision's rulings as data, name-checked.** If the revision says "these seven are
    preferences", put them in a config file with their names and have the build assert the id
    *still* carries that name — so a future renumber cannot silently move a preference onto an
    unrelated record.

## Workflow

Each step ends with a completion criterion. Do not advance on a partial result.

### 1. Preserve the incoming artifact

Copy it into the project (`incoming/<name>.<rev>.md`) and work from that copy.

**Done when:** the artifact is inside the repo, byte-identical, and every later step reads the copy.

### 2. Parse both revisions into records

Write a small parser (it becomes a reusable tool, not a throwaway): split on the per-record
heading, capture the id, the title, and every `**Bold field.**` / `*Italic field:*` label.

Record the **field labels each side carries**: labels present only in the new revision *are the
schema change*, and finding them this way is how you learn the revision added seven fields.

**Done when:** a diff run prints added ids, removed ids, and per-id changed fields — and the
counts are plausible against the file size (a 15k-line file with 40 new records and 31 edits, not
448).

### 3. Measure before you write

Run the diff with no `--apply`. Check the numbers against an independent signal (heading counts,
the revision's own revision-notes section).

Then **audit your own comparison** for the traps in rule 2. If ~every record reports as changed,
your comparison is wrong, not the file. Fix the comparison before ingesting anything.

**Done when:** you can explain the changed count, and independently reproduced it a second way.

### 4. Write the delta into the source

- New records → their own source file, in the revision's document order, carrying a `doc_order`.
- Edited records → patch each mapped field into the existing source record, comparing against the
  *rendering* as in rule 2.
- Log every change to a report: id, source file, which fields, and the before/after text.

**Done when:** the report lists each change, an `--apply` run writes them, and a second `--apply`
run reports zero changes (rule 4).

### 5. Pin the ids

If the revision was authored against a different numbering, bootstrap a lock from its own
(id, title) pairs: resolve each title to a source key, write `config/id-lock.json`. Then have the
id assignment prefer the lock and only mint for unknowns.

**Done when:** re-deriving every id from the rebuilt data reproduces the revision's numbering
exactly — zero id→title mismatches.

### 6. Rebuild and re-verify

Fix the failures the gate reports, in this order: your comparison (step 3), the id map (step 5),
then the artifacts. Every failure is one of those three; there are no others.

**Done when:** the independent gate passes, and every count in the docs matches the data.

## Id stability

The subtle one, and the one that silently corrupts documents.

```
positional:  id = f"AP-{sort_index:04d}"     # rename one record → neighbours renumber
pinned:      id = lock.get("file:source_id") or mint_next_free()
```

Adopt this whenever two conditions hold:

- Records have short human-facing ids that documents and humans cite (`AP-0177`, `RFC-0009`).
- Record content can change (titles, severities, categories, tags) in ways that alter sort order.

Assign ids **after** merging but **from** the lock first; write the lock back only when it changed.
Report newly minted ids on every build — a surprise mint is how you notice the lock has a hole.

Re-pinning to a revision's numbering is a **one-time** operation (`bootstrap_id_lock`) run when
adopting that revision, not part of the normal build.

## Verification gates

Run all four; each catches a different class of error.

| gate | what it proves | catches |
|---|---|---|
| second `--apply` run | ingest is idempotent | a diff-writing tool that empties the import |
| independent validator | source files conform to the declared taxonomy | a new category the validator doesn't know |
| rebuild + audit | artifacts agree with the data, re-derived | stale docs, drifted classifications, hardcoded columns |
| exact-set freshness | every citation/asset was actually checked | new records arriving with unverified references |

The audit should re-derive the things it checks — classifications, eras, counts — rather than
reading back what the build wrote. A gate that trusts the build is a mirror, not a gate.

## Common Pitfalls

1. **Diffing by eye.** A uniform document hides its own delta. Parse both sides and diff records.
2. **Comparing rendering to raw source.** Sorted lists and merged unions report as thousands of
   phantom edits. Compare like with like.
3. **Case-sensitive list comparison.** `['A','b']` vs `['b','A']` is a reorder, not an edit.
4. **Writing only the new records.** Destroys the import on the second run. Regenerate; refuse empty.
5. **Positional ids.** Renames renumber neighbours and repoint every reference. Pin them.
6. **Hand-editing a generated file.** It is regenerated on the next build and the edit vanishes.
   Edit the source; if the source cannot express the change, the schema is wrong.
7. **Paraphrasing the human's policy prose.** Import it verbatim as its own document.
8. **Inventing classifications** the revision did not make. Record `unclassified`.
9. **A freshness floor instead of an exact set.** New content passes unnoticed.
10. **Declaring success from the writer's output.** "writes: 40" is not evidence the 40 are
    correct — rebuild and re-read the artifact.

## Verification Checklist

- [ ] Incoming artifact preserved in-repo; every step read the copy
- [ ] Both revisions parsed; field-label delta identified (= the schema change)
- [ ] Diff reports added / removed / modified counts that reconcile with independent counts
- [ ] Comparison verified against the *rendering*, not raw source, for list and merged fields
- [ ] Every source write logged with before/after in a report
- [ ] Second `--apply` run reports zero changes (idempotent)
- [ ] Ids pinned in a committed lock; zero id→title mismatches against the revision
- [ ] Every cross-reference inside the revision resolves to the *intended* record
- [ ] Schema version bumped; new fields added explicitly; renderers updated for all of them
- [ ] Independent validator passes on the new taxonomy
- [ ] Freshness check compares to the exact current set; every new citation verified
- [ ] Audit re-derives classifications and passes
- [ ] Docs (counts, tables, headline numbers) regenerated, not hand-edited
- [ ] The human's governance prose imported verbatim

## One-Shot Recipe

Reference implementation: `D:\AI\AIProjects\agent-anti-patterns` (448-record catalog,
`tools/` holds all of these).

```bash
# 1. Keep the incoming revision
cp "<attachment>" incoming/ANTI-PATTERNS.rev2.md

# 2. What changed, as data (added / removed / modified / field-label delta)
python tools/diff_revision.py ANTI-PATTERNS.md incoming/ANTI-PATTERNS.rev2.md

# 3. Report the ingest without writing, then write it
python tools/ingest_revision.py incoming/ANTI-PATTERNS.rev2.md
python tools/ingest_revision.py incoming/ANTI-PATTERNS.rev2.md --apply

# 4. Pin ids to the revision's numbering (only when adopting its ids)
python tools/bootstrap_id_lock.py incoming/ANTI-PATTERNS.rev2.md

# 5. Rebuild and gate
python tools/build_catalog.py
python tools/validate_research.py
python tools/check_sources.py        # network: re-verify every cited URL
python tools/audit.py

# 6. Prove idempotency
python tools/ingest_revision.py incoming/ANTI-PATTERNS.rev2.md --apply   # must report 0 changes
python tools/build_catalog.py && python tools/audit.py                   # must still pass
```

Expected on a clean second pass: `new entries: <N> legacy edited: 0` (regeneration, not a diff)
with identical artifacts and a passing audit.
