---
name: criminal-discovery-summarizer
description: Condense police reports, body camera transcripts, witness statements, and discovery packets into a case-relevant summary organized around defense-relevant issues. Use whenever the user uploads or pastes police reports, body cam transcripts, discovery documents, or witness statements and wants them summarized, organized, or reviewed for issues.
---

# Criminal Discovery Summarizer

Condenses raw discovery material into a summary organized around what actually matters for defense strategy, not a chronological restatement of every report.

## Workflow

1. **Summarize each document type separately**: police report(s), body cam/dash cam transcript, witness statements, forensic/lab reports, other evidence (video, photos referenced).
2. **Extract the narrative** each source tells, in 2-4 sentences per document — what happened according to that source.
3. **Flag internal inconsistencies** across documents (officer report vs. body cam, witness statements that conflict with each other or with the report).
4. **Flag potential legal issues** as neutral observations, not conclusions: search/seizure timing and basis, Miranda timing, identification procedure, chain of custody gaps, missing or referenced-but-not-provided evidence.
5. **Note anything favorable to the defense** explicitly (inconsistent ID, procedural irregularity, exculpatory statement) — don't bury it in a purely factual recap.
6. **Close with an open-questions list** — what's referenced in discovery but not yet provided (e.g., "video mentioned in report, not included in this packet").

## Output format

```
## Discovery Summary — [Case name]

### Police Report
[2-4 sentence summary]

### Body Cam / Dash Cam
[2-4 sentence summary]

### Witness Statements
- [Witness]: [summary]

### Inconsistencies flagged
- [specific conflict between sources]

### Potential issues (neutral, for attorney review)
- [search/seizure, Miranda, ID procedure, chain of custody, etc.]

### Favorable to defense
- [specific point]

### Missing/referenced but not provided
- [item]
```

## Document Output Format

If this summary is wanted as a standalone document for the case file or co-counsel, use the `docx` skill:

- **Header:** firm name/logo placeholder, case name/docket number, "Discovery Summary — Attorney Work Product" title, date.
- **Body:** real Word heading styles per document type (Police Report, Body Cam, etc.), not markdown headers; witness statement list as a proper Word list.
- **Flags sections** (inconsistencies, potential issues, favorable-to-defense, missing items): visually distinct from the neutral summaries — e.g., shaded callout boxes — so an attorney skimming the document can find them without rereading the whole thing.
- **Typography:** Calibri or Arial 11pt, 1" margins, page numbers.
- Mark the document clearly as attorney work product in the footer.

## Notes

- Flag legal issues neutrally ("timing of the search relative to the stop may be worth reviewing") rather than asserting a suppression motion will succeed — that's attorney judgment.
- Never omit an inconsistency because it seems minor; small inconsistencies are often the whole ballgame in these cases.
