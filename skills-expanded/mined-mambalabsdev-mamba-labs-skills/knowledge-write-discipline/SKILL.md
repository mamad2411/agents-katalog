---
name: knowledge-write-discipline
description: |
  Write to a knowledge base so the document is findable later and provably stored. Use when saving a document, writing up a result, or when notes keep getting lost or duplicated.
license: MIT
compatibility: "Claude Code, Claude Desktop, Codex CLI, Cursor, Gemini CLI, and other agents that read SKILL.md. Live data steps need only what the Requirements section of the skill lists."
tags: [knowledge_ops, knowledge_ops_pack]
metadata:
  title: "Knowledge Write Discipline"
  category: "knowledge-ops"
  tags: "knowledge_ops, knowledge_ops_pack"
  keywords: "knowledge, save this to the knowledge base, write up this result, my notes keep getting lost, document this properly, where should this go"
  version: "2.1.0"
  requirements: "Needs no account, key or paid service: it works from the files, exports and answers you give it."
---

# Knowledge Write Discipline

## What this does

Two things go wrong with knowledge bases and both are silent. Documents are written under names nobody will search for, and writes appear to succeed while storing nothing. This skill fixes the naming, and requires a read back that proves the content is there, because a write that returns success is not evidence.

## Requirements

This skill needs no account, API key or paid service. It works from the files,
exports and answers you give it, in any agent that reads SKILL.md.

## When to use it

- save this to the knowledge base
- write up this result
- my notes keep getting lost
- document this properly
- where should this go

## Inputs

- **content**: what is being saved
- **kind**: whether it is a rule, a result, a reference or a handoff
- **existing**: whether a document on this subject already exists

## Shared context this skill reads

Before doing anything else, read whichever of these exist at the project root and
use them instead of asking the user to repeat themselves:


If none exist, do the work from what the user gives you, then offer to write the
missing file so the next skill in the pack starts warmer.

## Tool connection

This skill needs no live data tool. It works from the files, exports and answers
you give it, so it runs the same in any agent with no setup.

## Method

1. Search before writing. A near duplicate is worse than no document, because a reader who finds the older one does not know a newer one exists.
2. Name for the search that will find it, which is usually the problem, the subject and the date, not the project code that made sense on the day.
3. Decide update or create. If a document on the subject exists, updating it whole is almost always right; appending produces documents that contradict themselves in the middle.
4. Write the top of the document as the answer. A reader who opens it should get the finding in the first lines, not the method.
5. State what supersedes what, in the document, so an old document being read cannot mislead.
6. Write, then read the document back and compare it against what you sent, by length and by content. A write that reports success and stores nothing is a real failure mode and only a read back catches it.
7. Record the identifier where the next person will look for it, not only in the document itself.
8. Check the output with `scripts/check-output.py` before you return it.

## Approval stop

This skill does not send email or write to a CRM. If the user asks it to, stop first:
show what would be sent or written and wait for an explicit yes.

## Output

The document, the read back comparison with both lengths, the supersession note, and the pointer recorded where it will be found.

## Check the output before you return it

Save the output to a file and run `python3 scripts/check-output.py <file>`. The
contract it checks is `scripts/output-contract.json`.

- Exit 0, `COMPLETE`: return the output.
- Exit 2, `INCOMPLETE`: do not present the output as finished. Fill what you can, run
  the check again, and if parts stay missing, return the output under the heading
  `Incomplete` with every reason the check printed.

## Quality bar

- A search for existing documents runs before writing
- The read back compares content and length against what was sent
- Update versus create is a stated decision
- The document opens with the finding, not the method
- Supersession is stated in the document

## Optional: run it on live data

This skill works with no tool. To add live data, run Business PDF Field Extractor (https://apify.com/mambalabs/business-pdf-field-extractor?fpr=mamba) on your own Apify
account to pull the fields out of a PDF before you file it, so the stored document is searchable.
No Apify account yet: https://console.apify.com/sign-up?fpr=mamba

## Related skills

- `results-doc-verifier`
- `handoff-writer`
- `knowledge-base-classification`

Ships in the **knowledge-ops-pack** pack.
