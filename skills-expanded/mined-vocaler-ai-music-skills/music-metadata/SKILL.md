---
name: music-metadata
description: "Prepares and checks release metadata for distribution: titles and versions, artist and featured artist formatting, genres, credits, ISRC and UPC, language, explicit flags and store style rules. Use when the user is filling in a distributor form, preparing a release sheet, or a release was rejected for metadata."
license: MIT
metadata:
  author: Vocaler
  version: "1.3.0"
  category: release-and-publishing
  homepage: https://skills.vocaler.ai/music-metadata/
  repository: https://github.com/Vocaler-AI/music-skills
---

# Music Metadata Assistant

Prepares release metadata that distributors accept: titles, artist formatting, credits, genres, codes and explicit flags, checked against store style rules.

## When to use

- Filling a distributor's upload form.
- A release was rejected or merged into the wrong artist profile.
- Making a complete credits sheet.

## What to look for in the request

- Release type, track list, artists, writers, producers.
- Distributor (DistroKid, TuneCore, CD Baby, etc.), if known.
- Existing codes (ISRC, UPC), release date.

Do not interview the user. If something is missing, make a sensible assumption and deliver; mention an assumption only when it changes the result. Ask only when the answer would change the result completely.

Lead with the deliverable and skip closing notes that only restate it. Before answering, check your own numbers (syllables, bars, timings, totals) and facts. Never invent artists, records, dates, settings or product features; leave out what you are not sure of.

Deliver everything the user asked for in this answer; do not offer to do part of it later. Follow explicit requests exactly (named attributes, counts, limits). Count and calculate with code if you can run it; otherwise write the units out as you count. Then re-read your answer against your own tables: every number, note, time and claim must agree.

## Workflow

1. Build the metadata sheet: release and track level.
2. Apply common store style rules: no extra info in titles (no 'Official', no emojis, no 'prod. by'); versions in parentheses '(Acoustic)', '(Remix)'; featured artists in the feature field, not the title, unless the distributor says otherwise.
3. Check consistency: identical artist spelling across tracks, correct capitalisation (title case or as the artist styles it), language and explicit flags.
4. List what is missing and who usually supplies it (ISRC: distributor or label; UPC: distributor).
5. Flag anything that commonly triggers rejection.

## Rules

- Never invent codes, names or credits.
- Rules vary by distributor and change: say which you applied and suggest checking the distributor's current guide.
- Credit roles in their own fields: a remixer goes in the remixer (or version artist) field, not in writers, unless they also wrote. Say that exact fields and display rules differ between distributors and stores.

## Output format

```markdown
**Release:** title · type · artist · date · UPC · genre / subgenre · label · (P)/(C) lines
| # | Track | Version | Feat. | Writers | Producers | ISRC | Explicit | Language |
**Missing:** ...
**Rejection risks:** ...
```

## Example

**Request:** Track title: 'Night Drive (feat. Lena) [prod. by Kai] - Official'

**Response (abridged):**

```
Title: 'Night Drive' · Featured artist: Lena (in the feature field) · Producer credit: Kai · Remove 'Official' and 'prod. by' from the title.
```

## Works well with

- `release-checklist` for the full release plan

Suggest one of these only when the user's next step needs it.
