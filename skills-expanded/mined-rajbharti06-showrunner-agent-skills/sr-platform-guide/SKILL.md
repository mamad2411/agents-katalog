---
name: sr-platform-guide
description: A sourced, dated field guide to YouTube, Instagram, TikTok, Facebook, LinkedIn, X and Threads. For each platform it gives formats and limits, how people find content, what it reports to creators, what the creator controls, and what nobody outside the company knows, with every fact labelled official, reported, inferred or study and dated. Use when someone asks how a platform works, what the algorithm rewards, which format to use there, or whether a rule they heard is true. Checks the facts database instead of repeating folklore.
license: MIT
compatibility: Any agent that loads Agent Skills. The facts lookup needs Python 3.9+; the reference files can be read without it.
metadata:
  author: Raj Bharti
  version: "0.1.2"
  family: showrunner
---

# Platform guide

Most algorithm advice is a guess repeated confidently. This guide keeps facts, reports and guesses apart.

## How to answer a platform question

1. Say the platform and what the person wants to do there.
2. Look the facts up: `facts_search platform=<name>`, or read `references/<platform>.md`. Each has a status and a date.
3. Answer in three parts: what is known (official), what is reported by others (say who), and what is inferred or unknown.
4. If a fact is more than 90 days old, say so and suggest the person check the live app (`facts_stale`).
5. End with what the creator controls: packaging, retention, consistency, topic fit.

## Status labels

| Status | Meaning |
|---|---|
| official | The platform states it in its own help or announcements |
| reported | Someone other than the platform reports it: a news outlet, a vendor blog, or a platform executive quoted second-hand. The source link and the confidence tell you how far to trust it |
| inferred | A reasonable reading of indirect evidence |
| study | One analysis of data; correlation, not proof |

Every entry also has a confidence level (high, medium, low), a source where there is one, and an as-of date. Many "reported" entries come from secondary sources, so treat low-confidence ones as leads to check, not as facts.

## Reference files

- `references/youtube.md`
- `references/instagram.md`
- `references/tiktok.md`
- `references/facebook.md`
- `references/linkedin.md`
- `references/x-threads.md`

They are generated from the facts database, so they never disagree with it. Platforms change quickly. Facts are checked by hand, not live.

## Things nobody outside the platforms knows

The exact ranking weights for any of them. YouTube has not published its ranking signals (`youtube.ranking.unpublished`). TikTok lists the kinds of signals but not their weights (`tiktok.signals.published`). LinkedIn has not published weights (`linkedin.signals.modelled`). X published code in August 2026, and secondary reports disagree on details, so check `x.ranking.open_source` and its confidence before quoting a number. Anyone selling "the algorithm" with exact percentages is guessing or selling.

## Fixing a wrong fact

If the person has a newer source, add or correct the entry in `engine/showrunner/data/facts.json` (or the generator) and open a "fact PR" with the source link (`CONTRIBUTING.md`). A fact needs an id, claim, status, confidence, source URL and as-of date.

## Gate

None. This skill informs the other skills.

## Do not

- State a limit or weight from memory.
- Treat a vendor blog or a secondary report as official.
- Present a correlation study as a rule.
