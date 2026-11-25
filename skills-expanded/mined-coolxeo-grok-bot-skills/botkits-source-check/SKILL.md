---
name: botkits-source-check
description: >-
  Use this after drafting an article, before publish, to verify every factual
  claim and statistic against a named source.
---
# Source check

Check every factual claim in a draft before it goes out. Report only, except for adding or updating a Sources section at the end.

## 1. List the claims

Go through the draft and log each checkable statement with its line: numbers, dates, quotes, "X said", "X caused Y", rankings, comparisons, and anything about a named person or company. Skip the writer's clearly marked opinions and their own first-hand experience.

## 2. Check each one

Look in this order: a source named in the draft, the writer's notes and files, then the open web.

On the web, check the source before trusting it. Who published it, what do they gain, and what do others say about them? If the page is weak, look for better coverage of the same claim rather than digging into the weak page. Follow every quote and number back to where it first appeared; cite that, not the article repeating it.

Give each claim one status:

- **OK.** A good source says exactly this.
- **Stretched.** The source says something narrower ("up to 40%" became "40%", one study became "research shows").
- **Open.** Plausible, but nothing found yet.
- **Wrong.** The evidence contradicts it, or it cannot be supported.

When two good sources give different numbers, use the primary one and tell the writer about the conflict.

## 3. Look at the whole

- More than half the claims resting on one source.
- Old numbers in a fast-moving field.
- A number without the context that changes its meaning.
- Vague attribution ("studies show", "experts agree") still in the text.
- Social posts or press releases standing in for evidence, beyond what the account itself announced.

## 4. Sources section

Add or update `## Sources` at the end: numbered, grouped by section, each with author or outlet, title, date, URL, and the date you checked it. Add an archive link when the page looks likely to change. Remove entries for claims that were cut. Never duplicate.

## Report

Counts per status, then each non-OK claim with its line, what the source actually says, and a fix (source to find, softer wording, mark as opinion, or cut). Verdict: **Ready**, **Small fixes**, **Needs sourcing**, or **Not reliable**, plus one sentence.

Never rewrite the prose. Never paper over an open claim with a source that doesn't say it.

## Inspired by

- [Nadiem Mahmoud, source-check](https://github.com/nadiem99/claude-writing-skills/blob/5b52111e1bd30e93643929f17155e82aa26f771f/skills/pipeline/source-check/SKILL.md) (MIT). Does well: four passes, clear claim statuses, the original-source rule, and a maintained Sources section. Missing: judges reputation by a fixed list of outlets, says nothing about two good sources that disagree, and records no access dates or archive links.
- [Mike Caulfield, SIFT](https://hapgood.us/2019/06/19/sift-the-four-moves/). Does well: stop, check who is behind a source, find better coverage, trace claims to their origin. Missing: built for readers judging what they see, not writers producing a cited draft.
- [Wikipedia, Verifiability](https://en.wikipedia.org/wiki/Wikipedia:Verifiability) (CC BY-SA 4.0). Does well: the person adding a claim owns the burden of sourcing it, and quotes and challengeable claims need inline citations. Missing: rules for an encyclopedia, with no claim triage or report format.

## What this version adds

- Checking who is behind a source and finding better coverage, instead of trusting a fixed outlet list.
- A rule for conflicting numbers, taken from Dani's own LinkedIn workflow.
- Access dates and archive links in the Sources section.
