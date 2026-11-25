---
name: research-sources
description: Keep a source ledger for a research answer — every claim tied to the source that supports it, quotes kept apart from your own inference, and anything you could not read marked unknown. Use for any research report, comparison or fact-check someone will act on.
---
# Research with a source ledger

A research answer is only as good as the reader's ability to check it. The failure this prevents
is not a wrong fact but an untraceable one: a confident sentence nobody can tie to a page, or an
inference written as if a source had said it.

## When to use

- The operator asks for a report, a comparison, a recommendation or a fact-check.
- The answer will be acted on, shared, or used to decide something.
- More than one source is involved, or sources disagree.

Not for a one-line lookup answered by a single obvious page; cite that page and stop.

## Procedure

1. **Plan the questions** before searching: list the two to six questions the answer must settle,
   and what would count as settled for each (one primary source, or two independent ones that
   agree). Follow the `websearch` skill for the searching itself.
2. **Read before you cite.** A search snippet is not a source. Open the page with `WebFetch` (or
   the browser) and take the claim from the page's own words. A page you could not open is not a
   source; it goes in the ledger as unread.
3. **Keep the ledger as you go**, in a file beside the work (`sources.md`) or at the end of the
   report, one row per claim:

   | # | Claim | Source (title, URL, date) | Kind | Evidence |
   |---|---|---|---|---|
   | 1 | Project X has 12k stars | GitHub repo page, 2026-10-02 | quote | "12.1k" in the header |
   | 2 | X is aimed at large teams | X README; two user reviews | inference | README pricing tiers + reviews 3, 4 |
   | 3 | X's licence changed in 2025 | — | unknown | changelog page would not load |

   *Kind* is one of: **quote** (the source says it), **figure** (a number read from the source,
   with its date), **inference** (your conclusion from the listed sources — say which), or
   **unknown** (you looked and could not establish it).
4. **Write the answer from the ledger**, not from memory. Every factual sentence carries its row
   number, e.g. `[3]`. Inferences are worded as inferences ("this suggests", "likely").
5. **Say what is missing.** End with the questions the sources did not settle and what would
   settle them. An honest "unknown" beats a guess that reads like a fact.

## Checks

- Every factual sentence in the answer points at a ledger row; no row is cited that you did not read.
- Quotes and figures carry a date; numbers that change (stars, prices, versions) say when they were read.
- Inferences are marked as such and name the rows they rest on.
- Disagreeing sources are both listed, not silently resolved.
- Unread or unreachable sources are listed as unknown, not dropped.
