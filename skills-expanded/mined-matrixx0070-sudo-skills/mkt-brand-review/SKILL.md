---
name: mkt-brand-review
version: 1.0.0
description: Audit marketing content against a brand voice and style guide, flagging every deviation by severity with a concrete fix for each.
author: matrixx0070
tags: [marketing, brand, review, copyediting, voice, quality]
capabilities: []
---

## When to use

Use this when you have a finished or near-finished piece of content (blog, email, ad, landing page, social post) plus a brand voice or style guide, and you need an objective, ship/no-ship audit before it goes live.

**Not for:** writing content from scratch (use mkt-draft-content), high-level positioning debates (use mkt-competitive-brief), or copy where no brand reference exists and none can be inferred — get a guide or sample set first.

## Method

1. Load the reference. Extract voice attributes (tone, personality), style rules (grammar, casing, punctuation, terminology, banned words), and formatting conventions. Decision point: if no guide exists, either infer a baseline from 2-3 on-brand samples or stop and request one — state which you did.
2. Read the target once, top to bottom, for overall impression before any line-level work.
3. Check voice: does tone match the guide (confident not arrogant, warm not flippant)? Capture mismatches as direct quotes.
4. Check style mechanics: terminology, product names, capitalization, Oxford comma, numerals, banned/discouraged words.
5. Check structure: headline conventions, CTA phrasing, length norms, accessibility (alt text, reading level).
6. Assign severity to each finding: CRITICAL (off-brand, factual, or legal risk), MAJOR (noticeable voice/style break), MINOR (polish).
7. Decision point: if any CRITICAL exists, verdict is block/revise regardless of score. Attach a fix to every flag.

## Example

Guide says "friendly, never salesy; never use 'revolutionary'." Content reads: "Our revolutionary platform will transform your business overnight."
- CRITICAL — "revolutionary" — banned word + unsubstantiated claim. Fix: "Our platform helps teams work faster."
- MAJOR — "transform... overnight" — salesy hype, breaks friendly tone. Fix: "so you see results in your first week."
Score: 62/100. Verdict: revise.

## Pitfalls

- Complaining without a fix — every flag must carry a concrete replacement.
- Nitpicking MINOR items while missing a CRITICAL claim or legal risk.
- Applying personal taste instead of the documented guide; cite the rule you are enforcing.
- Scoring high because prose is "good" when it is good but off-brand — conformance, not quality, is the test.

## Output format

```
Score: <0-100> — <one-line verdict>
Verdict: ship | revise | block

Findings:
| Severity | Location / quote | Issue | Suggested fix |
|----------|------------------|-------|---------------|
(grouped CRITICAL, then MAJOR, then MINOR)

Quick wins: <top 3 highest-impact edits>
```
