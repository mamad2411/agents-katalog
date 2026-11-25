---
name: deep-research-brief
description: Turns any research question into a decision-ready brief with question decomposition, multi-source triangulation (3+ independent sources per claim), confidence labels, and full citations. Use when the user asks to "research this", "deep dive on", "find out whether", "compare the options for", "build a research brief", or needs sourced facts before making a decision. Don't use for writing the final content piece (hand the brief to linkedin-content-pack or newsletter-assembler) or single-fact lookups.
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Content & Marketing, Research, Briefs, Web]
    related_skills: [linkedin-content-pack, newsletter-assembler, content-repurposer]
    requires_toolsets: [web]
---

# Deep Research Brief

Produces a brief a decision-maker can act on without re-checking your work: the question broken into sub-questions, every claim triangulated across at least 3 independent sources, every claim labeled with confidence, and a numbered citation list. No claim without a source; no source without a URL.

## When to Use

- The user needs facts, market data, or comparisons before deciding something.
- A downstream content skill (LinkedIn pack, newsletter) needs a sourced foundation.
- The user says "research", "deep dive", "what's the evidence for", "is it true that".
- **Not for:** writing the final content piece (hand the brief to `linkedin-content-pack` or `newsletter-assembler`), or single-fact lookups a quick search answers in one step.

## Quick Reference

| Action | Command / Call |
|---|---|
| Search a sub-question | `web` toolset search, 2–3 query phrasings per sub-question |
| Fetch a source | `web_extract` on the URL; save title, author, date |
| Check source independence | Compare domains AND original reporting origin |
| Count sources per claim | `python3 -c "..."` tally from your notes (step 5) |
| Label confidence | High = 3+ independent agree; Medium = 2, or 3 with 1 dissent; Low = 1, or sources conflict |

## Procedure

1. **Precheck** — confirm the `web` toolset is available (run one trivial search). If not, stop and tell the user this skill needs web access. Confirm the decision the brief serves: ask "What decision does this inform?" if not stated.
2. **Decompose** — split the main question into 3–6 sub-questions. Each must be answerable with evidence, not opinion. Write them down first; they become the brief's section headers.
3. **Search** — for each sub-question, run 2–3 differently-phrased searches. Collect candidate URLs. Prefer primary sources (official docs, filings, original studies, first-party announcements) over aggregators.
4. **Extract & log** — fetch each promising source. For every claim you keep, log: claim text, source URL, publish date, and whether the source is original reporting or citing someone else. Two outlets quoting the same press release count as ONE independent source.
5. **Triangulate** — every claim that will appear in the brief needs 3+ independent sources for a High label. Verify your tally with stdlib Python (write your claim→sources map as JSON to a temp file first):
   `python3 -c "import json;d=json.load(open('/tmp/claims.json'));[print(k,len(set(v))) for k,v in d.items()]"`
   Expected: each claim prints its independent-source count. Anything under 3 gets Medium or Low.
6. **Label** — attach a confidence label to every claim: **High / Medium / Low** per the Quick Reference rules. If sources actively conflict, say so and show both sides — never average a disagreement into a fake consensus.
7. **Deliver** — assemble the Output Template. Lead with the answer, not the journey. Citations are numbered and every in-text claim carries its bracketed numbers.

## Output Template

```
# Research Brief: [Question]
**Decision this informs:** [one line]
**Bottom line:** [2–3 sentence answer with confidence label]

## Findings
### [Sub-question 1]
- [Claim] — **High** [1][2][3]
- [Claim] — **Medium** [4][5]
(repeat per sub-question)

## What we couldn't verify
- [Open question + what evidence would settle it]

## Sources
1. [Title — Publisher, Date](URL)
2. ...
```

## Pitfalls

- **Echo-chamber sourcing** — five URLs, one press release. Recovery: trace each source to its origin; collapse duplicates to one, then search specifically for dissenting or independent coverage.
- **Stale data presented as current** — a 2023 stat answering a 2026 question. Recovery: log publish dates in step 4; flag anything older than 18 months in-text ("as of [date]") and search for a newer figure before labeling High.
- **Scope creep** — brief balloons past the decision it serves. Recovery: re-read the decision statement from step 1; cut any finding that doesn't change the decision into a one-line "Related but out of scope" note.
- **Confidence inflation** — labeling High because the claim "feels obvious". Recovery: the label is mechanical — rerun the step 5 count; if the tally says 2, it's Medium, full stop.

## Verification

- [ ] Every claim in Findings has ≥1 bracketed citation and a confidence label
- [ ] Every High-labeled claim traces to 3+ independent origins (step 5 tally re-run)
- [ ] Bottom line answers the stated decision in ≤3 sentences
- [ ] All citation URLs were actually fetched this session (no invented links)
- [ ] "What we couldn't verify" section exists, even if it says "Nothing material"
