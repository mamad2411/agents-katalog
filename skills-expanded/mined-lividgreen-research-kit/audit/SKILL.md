---
name: audit
description: A consistency audit across the project's documents — the mechanical checks first, then what no script sees, every import read at its exporting statement, a regime condition stated with the same constants, a status labelled alike, definitional drift and every negative-coverage sentence held to the artifact; reported as a table of discrepancies with the audit editing nothing, after which each sentence found false of the artifact is corrected. Use as `/research:audit`, optionally with a scope (`/research:audit the two companion documents`), after a statement or a definition other documents cite has changed, and before a document goes out. The project's instructions file names its corpus and what it holds the documents to; this skill names none of it. When the person says 'audit', 'do documents agree' or 'check for consistency', they mean this skill — call it every time, even if it ran earlier in the session, and take every step.
license: Apache-2.0
compatibility: No script of its own; runs the project's checks, and `library check` and `formal cite` where those are bound.
metadata:
  version: "0.12.1"
---

# A consistency audit

A statement one document imports is the one the exporting document proves, with the same strength, the same conditions and the same scope, cited as a result and never re-derived or quietly strengthened.
The audit reads what no script reads; the scripts run first, so its effort goes there.

## The project's part

The setup (`/research:research-init`) forms with the person what the project's reviews hold its documents to and writes it under a `### Reviews` heading of the instructions file, inside its `## Records and method` section; the audit reads it there, each item a check of its own in step 2:

- the documents that form the corpus, the draft and deferred ones among them, which no gate reads and which therefore go stale first;
- which document imports which;
- the regime conditions, each with its explicit constants;
- the claims whose status is written in more than one document;
- the objects whose definitions are compared, and any two that share a name on purpose;
- any rule of the project's own a document is held to, such as a result each document must own;
- which documents a review may correct in the session, and which it reports and asks the person about first (an ADR, a contract, a history held as written at its date);
- the gates this audit runs first, by name, where they are more than the hooks.

Where the instructions file has no such part, or it does not say what this review needs, the review says so and advises `/research:research-init`, which forms it with the person in a project set up before as well; where only this review's part is missing and a full setup is not needed, it asks the person for that part in place and, on their word, writes it where the setup would.
The scope of a run is what the person gives with the command, and otherwise the corpus; the report says which it took.

## The steps

1. **The mechanical checks first.**
   Run the project's gates by their exit codes: by default the hooks of `.pre-commit-config.yaml`, as `prek run --all-files` or `pre-commit run --all-files`, and those the project's part names, `library check` and `formal cite` where they are bound among them, so citations, declaration names and figures are settled before the reading starts; a failing gate is reported with the audit and not fixed inside it.
2. **What no script sees.**
   Open every exporting statement and read its hypotheses before judging the sentence that cites it.
   - Every import, read at the exporting statement for its strength, its conditions and its scope; a document that claims more from another than that one establishes is a discrepancy, and a dropped condition is the gravest.
   - A regime condition stated with the same explicit constants everywhere it is load-bearing, not as an asymptotic shorthand in one place and constants in another.
   - A status labelled identically everywhere the claim appears — proved, machine-checked, conditional on a named hypothesis, open; a "machine-checked in X" is checked at X's own record of what is checked, not at the existence of some declaration.
   - Definitional drift: each named object defined alike, and each later use matching the definition; two objects sharing a name on purpose are never conflated in one sentence.
   - Every negative-coverage sentence ("nothing here does X", "none of these results", "stays open") is a claim about every document and every row of the artifact at once, held to the artifact at its committed state, and no gate reads it: for each, name the row, the statement or the declaration that would falsify it, or confirm that none does.
   - Each rule the instructions add.
3. **The report, the audit editing nothing.**
   A table: the discrepancy, the files and lines involved, which statement is correct, the severity.
   Where the artifact settles it, the correct statement is the artifact's; "the person decides" is written only where it does not, and a sentence found false of the artifact is never put to the person as a choice.
4. **Then the corrections.**
   After the report, each sentence found false of the artifact is corrected in this session at its own size, and reaches every summary site that restates it; a document the project's part names as one a review reports and asks about first gets the sentence, its evidence and the correction put to the person instead.
   What is the person's to decide goes to them as a question with a recommendation; a discrepancy not corrected now is captured on the person's word (`flow idea` where the project runs the flow), so the report does not live in the conversation alone.
   The gates run again after the edits.

**Output.** The gates by exit code, the table, the corrections made with their files, and what was asked or captured.
