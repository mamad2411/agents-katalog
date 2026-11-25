---
name: litig-chronology
version: 1.0.0
description: Build a case chronology or timeline of events with a source and evidentiary support cited for every entry.
author: matrixx0070
tags: [litigation, chronology, case-analysis, evidence, fact-development]
capabilities: []
---

## When to use
Use this when you need a defensible timeline of what happened, when, and how you can prove it. It structures each event with a date, description, actors, source, and evidentiary support, and separates established facts from disputed or inferred ones. Useful for case assessment, motion practice, and witness prep.

**Not for:** drafting the brief that uses the timeline (see litig-brief-section-drafter) or preparing a witness (see litig-deposition-prep).

## Method
1. Collect every event from the record: pleadings, documents, emails, deposition testimony, and interrogatory answers.
2. For each entry, capture date, event description, actors, and the exact source (Bates number, deposition page:line, exhibit).
3. **Decision point:** If an event's date or occurrence is contested, tag it DISPUTED and record the competing versions and their sources; if uncontested, tag it ESTABLISHED.
4. **Decision point:** If a fact is inferred rather than directly evidenced, tag it INFERRED and note the inferential basis so it is not overstated as proven.
5. Sort chronologically and flag gaps where a needed fact lacks any evidentiary support (discovery targets).
6. Cross-reference each entry to the element or claim it supports.
7. ATTORNEY-ESCALATION gate: Where the chronology drives case strategy or is shared externally, route it to a supervising attorney for review before it is relied upon or produced.

## Example
> Building a breach-of-contract timeline, you log the signed agreement (Ex. 3), the missed delivery (Smith Dep. 42:5-18), and a disputed oral extension the parties recall differently, tagging the last DISPUTED with both sources. A gap on when notice was received becomes a discovery target, and you route the chronology to the supervising attorney.

## Pitfalls
- **Unsourced entries:** A timeline entry without a citation cannot be used to prove anything and erodes credibility.
- **Blending fact and inference:** Presenting an inference as an established fact invites impeachment.
- **Ignoring disputes:** Omitting the opponent's version leaves you unprepared for cross.
- **Stale as discovery evolves:** A chronology frozen at intake misses later-produced evidence; update it.

## Output format
```
CASE CHRONOLOGY — [Matter]
Date | Event | Actors | Source (Bates / Dep p:line / Ex.) | Status | Supports element
2024-01-05 | Contract signed | A, B | Ex. 3 | ESTABLISHED | formation
[...]
Evidentiary gaps / discovery targets: [...]
Attorney review: [name | date | status]
```

## Reference
A rigorous chronology distinguishes admissible, sourced facts from attorney inference and cites the record precisely: Bates ranges for documents, page:line for deposition testimony, and exhibit numbers for produced materials. Admissibility turns on foundation, authentication (FRE 901), relevance (FRE 401), and hearsay analysis (FRE 801-803); a dated email may need a business-records or party-admission basis to come in. Deposition testimony is cited by page and line and can be used for impeachment or, for a party, as an admission. Building the chronology early surfaces evidentiary gaps that become interrogatory, document-request, or deposition targets, and supports statute-of-limitations and element-by-element analysis. Evidentiary rules and citation conventions vary by jurisdiction; confirm the governing rules of evidence and local practice. General information, not legal advice.
