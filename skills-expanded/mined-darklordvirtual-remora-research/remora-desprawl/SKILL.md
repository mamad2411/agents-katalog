---
name: remora-desprawl
description: Use when REMORA-research has too many documents, when asked to "reduce AI sprawl", "fjern unødvendig dokumentasjon", "rydd dokumenter", "slett duplikater", before adding a new overview, guide or summary document, or when the document register, docs/README index or archive keeps growing without new evidence behind it.
---

# remora-desprawl

Sprawl is documentation that costs a reader attention and gives nothing the
repository does not already hold elsewhere: copies, orphans nobody links to,
summaries of a canonical document, templates with invented content. Removing
it is a judgement per document. A file count is never the goal; one wrong
deletion of preserved history is worse than ten copies left in place.

## Start from the detector, not from a guess

```bash
python scripts/check_doc_sprawl.py          # worklist, most signals first
python scripts/check_doc_sprawl.py --json   # for scripting
```

It only reports. Protected documents never appear. These are frozen or
pre-registered files, NEGATIVE_RESULTS, the paper, history, and anything a
claim, test, script, workflow or module names by path. Do not delete outside
its worklist without stating why the detector missed the file.

## Decide per signal

| Signal | Action |
|---|---|
| `archive_twin:<live>` | Delete. Every prose line is in the live file and in git history. |
| `placeholder` | Delete. Template text or invented results breaks "claims resolve to committed evidence". If a number in it looks real, stop and check it first. |
| `near_dup:<other>` | Merge: move the lines only this file has into the canonical one, then delete. |
| `orphan` (live doc) | Nothing cites it. `indexed` means only `docs/README.md` lists it. Read it. Link it from the canonical document that should own it, merge it, or archive it with the notice banner. Delete only a stub or a copy. An ADR or review record stays and gets linked. |
| `stale` | Update it against the code, or archive it. Do not delete a stale record of a decision. |
| `superseded_by:<later>` | Keep. Versions are history; mark it superseded in the register if it is not already. |
| `unaudited`, `stub` | Not removal signals on their own. Combine them with another signal or leave them. |

Never delete an archived file that has a line of its own (no `archive_twin`).
The line may be the only record of a superseded finding.

## Each removal or merge changes these in the same commit

1. Delete the file with `git rm`, or merge it into the canonical document.
2. Remove the entry and its topic line from `docs/assurance/document_register_v1.yaml`.
3. Remove it from the `docs/README.md` index.
4. Fix every inbound link (`git grep -n "<path>"`), or point it at the canonical document.
5. Run `python scripts/check_prose_style.py --update-baseline` when a scanned file goes.

## Gates before the PR

```bash
python scripts/check_document_governance.py
python scripts/check_prose_style.py
python -m pytest -q -m docgate --no-cov
python scripts/check_doc_sprawl.py   # the removed files are gone, nothing new appears
```

One PR per kind of removal, titled `docs(desprawl): ...`. Its body lists each
path, its signal and its action. Do not touch the CHANGELOG unless a reader
outside the repository relied on the file.

## Do not add sprawl

Before writing a new document, find the canonical one for its topic in
`docs/README.md` and edit that instead (CLAUDE.md, CONTRIBUTING.md). A new
summary, overview, "status", "plan" or "report" file needs a register entry,
an index line and an owner, or it is sprawl on arrival.

## Red flags: stop and re-read

- Deleting to reach a number ("cut 30 %").
- "It's in the archive, so it's safe to delete." The archive is preserved history. Only `archive_twin` qualifies.
- "Nobody links to it, so it's useless." Orphans get linked or merged first.
- Merging two documents without moving the lines only one of them has.
- Removing a file and leaving its register entry or index line.
