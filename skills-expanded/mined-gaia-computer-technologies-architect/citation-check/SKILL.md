---
name: citation-check
description: Verify every reference in a document — planning appeal decisions, planning policies, code clauses, standards, research papers, precedents, product and performance claims, statistics — by checking that each one exists, says what it is cited for, and is current, then return a verified / not found / misquoted / outdated / unverifiable table with sources. Use when the architect wants to "check the references", "verify these citations", "is this appeal decision real", "fact-check this report", "check an AI-written draft", or to test an incoming objection letter or consultant report. Used by objection-response and any skill whose output cites sources.
license: MIT
metadata:
  author: Gaia Computer Technologies, Inc.
  version: "1.0.0"
---

# Citation Check

Check that what a document cites is real, says what it is cited for, and still applies. AI-generated text invents references that look right. In planning, AI-written objection letters have been found citing appeal decisions that did not exist when a lawyer checked (Pinsent Masons reported this). A fabricated reference in a submission damages credibility at best, and at worst becomes a professional problem.

## When to use

- Before issuing any document that cites policy, case law, appeal decisions, codes, standards, research or products. This applies especially if AI helped write it.
- When an objection letter, consultee response, or third-party report cites decisions or policies in support of its case.
- When a precedent, statistic, or performance claim "sounds right" but nobody remembers where it came from.

## Input

- The document (text, PDF, or pasted extract).
- Optional: the jurisdiction, and access to sources (web search, the planning portal, code libraries the practice subscribes to).

## Process

1. **Extract every reference.** Include explicit citations (case numbers, policy references, clause numbers, DOIs, URLs) and implicit claims that need a source ("studies show", "the council has consistently refused", "this material achieves X"). Number them.
2. **Classify each.** Appeal or court decision, planning policy, code clause or standard, academic or industry source, precedent project, product or performance claim, statistic.
3. **Check existence.** Search for the reference in an authoritative source: the official appeals or court database, the authority's plan documents, the publisher, the manufacturer's datasheet, the project architect's own published material. Record exactly where you looked.
4. **Check content.** Does the source actually say what the document claims? Compare the claim with the source text. A real decision cited for the opposite point is a misquote.
5. **Check currency.** Is the policy still adopted? Has the code edition been superseded? Was the decision quashed or overturned? Is the product still made with that specification?
6. **Grade it.**
   - **Verified:** exists, supports the claim, current.
   - **Misquoted:** exists, but doesn't say what's claimed.
   - **Outdated:** exists, but superseded, withdrawn or quashed.
   - **Not found:** no trace in the sources checked. This is not proof of fabrication; state where you looked.
   - **Unverifiable:** behind a paywall or needs access you don't have. Say what access is needed.
7. **Summarise the risk.** How much of the document's argument depends on references that failed?

## Domain knowledge

- **Appeal decisions have formal references.** In England, the Planning Inspectorate appeal references follow a set format and are searchable. Other jurisdictions have their own registers. A reference in the wrong format is a red flag, not proof.
- **Fabrications cluster.** A document with one invented reference often has more. If one fails, check the rest more carefully.
- **"Not found" needs the search log.** List the databases and queries used so a person can repeat or extend the search.
- **Secondary sources are pointers.** A news article about a decision isn't the decision. Go to the primary record where possible.

## Output format

```
## Citation Check — [document], checked [date]

**Summary:** [n] references: [v] verified, [m] misquoted, [o] outdated, [x] not found, [u] unverifiable.
**Risk:** [which parts of the argument rest on failed references]

| # | Reference as cited | Type | Status | What the source actually says | Where checked (link) |
|---|---|---|---|---|---|

### Claims needing a source
- [unsupported claim] → [suggested source to look for, or "remove"]

### Search log
- [database / site] — [query] — [result]
```

## What you don't do

- Don't mark a reference "verified" because it looks plausible or matches a pattern. Verified means you saw the source.
- Don't call a "not found" reference fabricated. Report the search; let the person draw the conclusion.
- Don't silently fix a reference. Report it, and suggest the correct one only if you found it.
- Don't judge the merits of the argument. Check the references; leave the planning case to objection-response or the planner.
