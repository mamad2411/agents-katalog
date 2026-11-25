---
name: ingest-writing
description: "Paste any raw material and route extractions into the appropriate context pages (voice / about / vocabulary / preferences)"
risk_class: soft
---

# Ingest writing

The user pastes raw material — a draft, an email, an article they wrote,
meeting notes, anything. This skill classifies the content, extracts what's
useful, and routes the extractions into the right context pages. Append-only;
**never silently overwrite**.

## When to invoke

- The user explicitly says: "ingest this", "learn from this", "remember this
  about how I write", "this is what I sound like", or pastes a wall of text
  with a directive like "use this".
- `/onboard` hands off to this skill after its lightweight interview, if
  the user accepts the paste-raw invitation.
- `/wrap-up` invokes this skill when `settings.ingest.auto_on_wrap_up` is
  `true` and there is end-of-day material to ingest.

## Gating

Before extracting, read the active settings:

```bash
rubber-ducky settings get ingest.kinds
```

The returned list bounds the extraction surface. If the user has restricted
`ingest.kinds` to `["voice"]`, do not extract facts, vocabulary, or
preferences from the pasted material — even if they're obviously present.
Respect the user's stated scope.

## Behavior

### Step 1 — Classify the input

Read the pasted text. Tag what it contains:

| Tag           | Looks like                                                                | Routes to                |
| :------------ | :------------------------------------------------------------------------ | :----------------------- |
| `voice`       | First-person prose, the user's own words at length.                       | `wiki/voice.md`          |
| `facts`       | Statements of who-does-what, role descriptions, project descriptions.      | `wiki/about.md`          |
| `vocabulary`  | Acronyms, internal terms, codenames, jargon.                              | `wiki/vocabulary.md`     |
| `preferences` | Statements about style, tone preferences, things to avoid.                | `wiki/preferences.md`    |

A single paste can produce extractions in multiple tags. Don't force a
single classification.

### Step 2 — Read existing context pages

Before extracting, query each target page so duplicates aren't appended:

```bash
rubber-ducky context query <kind>
```

The CLI returns each `##` section's body. Skim the existing entries —
extractions that say substantively the same thing as an existing entry
should be skipped, not duplicated.

### Step 3 — Build the extraction summary

Don't write anything yet. Present the user with a structured summary:

```
EXTRACTION SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
voice (1 new sample)
  > "<first ~80 chars of the sample>…"
    Why kept: first-person, long-form — useful for tone calibration.

facts (2 new)
  - User leads the platform team at <employer>.
  - <Project codename> is the migration off the old auth stack.

vocabulary (1 new)
  - **HOOTL** — hands-off, out-of-the-loop.

preferences (skipped — no new patterns beyond what we already have)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Write all of these? (yes / no / pick)
```

If the user picks `pick`, walk them through each candidate one at a time
(one question per turn) and write only what they greenlight.

### Step 4 — Append to the pages

Hold to two invariants on every write:

1. **Append-only** — new content is added at the end of the matching
   section, never replacing or rewording existing lines.
2. **Source-attributed** — each new entry begins with a `### Source —
   YYYY-MM-DD` heading (date in ISO form) plus a one-line note describing
   what the source was (e.g., "Pasted draft of OKR update").

For `voice.md`, each appended sample lands under `## Samples`. For
`about.md`, route into `## Identity`, `## Projects`, or `## People`
depending on the fact's nature. For `vocabulary.md`, route into `## Terms`,
`## Acronyms`, or `## Internal system names`. For `preferences.md`,
route into `## Style`, `## Pet peeves`, or `## Decision-making`.

If a heading the extraction needs is missing (e.g. an `## Acronyms`
section in a brand-new vault), create it; do not invent additional
headings.

### Step 5 — Audit log

Once writes complete:

```bash
rubber-ducky log append "[ingest-writing] +<N> voice / +<N> facts / +<N> vocab / +<N> prefs from pasted material"
```

### Step 6 — Confirm and pivot

End with a one-line confirmation: *"Added N entries across `<pages>`. Anything
else?"* If the user pasted before answering an active task or working flow,
pivot back to that — don't strand them in the ingest path.

## What this skill does NOT do

- **No silent overwrites.** Existing content is never rewritten — even when
  the new material seems to supersede the old. Append a new
  source-attributed entry; let the reader interpret the timeline.
- **No extraction outside `ingest.kinds`.** Respect the user's stated scope
  even when the source material is rich in other categories.
- **No interpretation of what the user *meant*.** Quote what the source
  said; don't paraphrase facts into your own voice. Preserving the source
  is the whole point of source-attribution.
