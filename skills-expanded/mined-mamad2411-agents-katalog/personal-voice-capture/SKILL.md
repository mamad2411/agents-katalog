---
name: personal-voice-capture
description: "Use when a user wants an agent to learn, encode, or improve their personal writing voice as a reusable skill through source-text ingestion and iterative calibration edits."
---

# Personal Voice Capture

## Overview

Use this meta-skill to create or improve a personalized voice skill for a specific person. The output is not a one-off prompt. The output is a durable `SKILL.md` that future agents can load to draft or rewrite text in that person's voice.

This skill is a calibration process: corpus evidence plus user edits become executable voice rules, context modes, phrase preferences, examples, and quality checks.

## Non-Negotiable Principle

Capture expression, not identity.

The generated skill may describe how the person tends to write. It must not invent their beliefs, commitments, emotions, facts, approvals, or positions. When future agents use the generated voice skill, they rewrite the supplied intent in the person's voice; they do not decide what the person thinks.

## When to Use

Use when the user says things like:

- "capture my voice"
- "learn how I write"
- "build my voice skill"
- "make future agents write like me"
- "that doesn't sound like me; update the voice skill"
- "calibrate on my edits"
- "turn these samples into my writing style"

Do not use for:

- impersonating someone without their consent
- inventing views, promises, or commitments
- forensic authorship attribution
- making text deceptively appear authored by someone in a context where disclosure is required
- replacing current task intent with generic personality mimicry

## Operating Modes

### 1. Capture Mode

Use this when no mature personal voice skill exists yet. The goal is to create a first usable `SKILL.md`.

### 2. Maintenance Mode

Use this when a voice skill already exists and the user corrects, edits, or rejects generated text. The goal is to patch the existing skill with new rules, weakened rules, deleted rules, or better examples.

## Phase 0 — Scope and Consent

Before ingesting or storing source material, establish the scope. If the user already specified the scope, proceed without re-asking.

Capture:

1. **Person** — whose voice is being captured.
2. **Primary languages** — English, Hebrew, mixed, or other.
3. **Contexts** — DM, email, internal memo, investor note, customer note, public post, technical doc, etc.
4. **Source policy** — pasted samples, local files, email/docs/chat exports if authorized.
5. **Storage policy** — default: do not retain raw corpus; retain derived rules and user-approved examples only.
6. **Output target** — local profile skill, repo skill, or both.

Default if unspecified:

- Store only derived voice rules and approved examples.
- Create a private, user-local skill named `<person-slug>-voice`.
- Keep source-text notes session-local unless explicitly asked to save them.

## Phase 1 — Ingest Past Writing

Accept sources from pasted examples, files, docs, emails, chat exports, social posts, or prior agent outputs edited by the user.

For each source, classify:

| Dimension | Values |
|---|---|
| Authorship confidence | authored, edited, transcript, uncertain |
| Medium | DM, email, memo, post, comment, deck, doc |
| Audience | self, friend, team, investor, customer, public |
| Formality | casual, crisp, polished, technical, strategic |
| Language | English, Hebrew, mixed, other |
| Recency | current, older, unknown |

Extract observations across these categories:

- sentence length and rhythm
- paragraph shape
- openers and closers
- transitions and framing devices
- directness vs. hedging
- compression level
- warmth and humor
- punctuation habits
- bullets/tables/numbered-list usage
- rhetorical patterns such as "not X, but Y"
- vocabulary and recurring phrases
- words or phrases the person avoids
- multilingual switching patterns
- context-specific differences

Keep evidence labels. Distinguish strong recurring patterns from weak one-off clues.

## Phase 2 — Draft the Initial Voice Model

Create `Voice Spec v0.1` with these sections:

```md
# <Person> Voice Spec

## Confidence
What evidence exists and where it is weak.

## High-Level Signature
A compressed description of the person's recognizable writing voice.

## Invariants
Rules that apply across most contexts.

## Context Modes
### DM / Chat
### Email
### Internal Memo
### Public Post
Add/remove modes as needed.

## Cadence
Sentence length, rhythm, paragraph shape.

## Diction
Preferred words, avoided words, recurring phrases.

## Structure
How the person organizes arguments and asks.

## Warmth / Humor / Edge
How much personality appears and when.

## Do / Don't
Concrete rewrite rules.

## Examples
Generic -> Person voice pairs.
```

Do not treat v0.1 as truth. It is a hypothesis to test against user edits.

## Phase 3 — Calibration Loop

Run short rounds. Each round should include 3–5 calibration items unless the user asks for a different pace.

### Delivery: editable file (default)

Do not paste calibration items into chat as blockquotes — they are painful to copy and edit. Instead, write the round to a single plain-text markdown file the user edits inline in their editor, then hand back. This scales to large rounds and keeps the user in one place.

Conventions for the file:

- Write to a session-local, gitignored location (e.g. `.scratch/calibration-round-<n>.md`). Never store raw corpus or edits in a committed path unless storage policy allows it.
- One block per item. Label the context/language. Show the generic version and the assistant's attempt as **plain text, not blockquotes** (no `>` and no leading indentation), so the user can copy or overwrite freely.
- Give each item a clearly delimited edit zone with an explicit sentinel the user types into, e.g.:

```md
## Example <n> — <context, language>

GENERIC:
<neutral, competent, non-personal version>

MY ATTEMPT:
<rewrite using current voice model>

YOUR EDIT (replace this line; write `good` if the attempt nails it):
‹edit here›
```

- Tell the user the file path and to save when done. Then read it back, parse each `YOUR EDIT` block, and proceed to Phase 4.
- Keep a brief top-of-file instruction line so the file is self-explanatory if reopened later.

### Delivery: one-by-one (alternative)

If the user prefers, show a single item at a time as plain text (no blockquotes), wait for their edit, then show the next. Use this for small or high-touch rounds.

Vary the examples across the scoped contexts. Include both easy and revealing cases:

- a strategic recommendation
- a casual DM
- a disagreement
- a concise ask
- a warm follow-up
- an apology or correction
- a public-facing thought
- a technical/product explanation

When the user edits, preserve their exact edited text as an approved example unless storage policy forbids it.

## Phase 4 — Diff Edits into Rules

After each edited example, compare:

1. generic version
2. assistant's attempted personalized version
3. user's edited version

Infer small, testable rules. Examples:

- User removed throat-clearing; strengthen compression rule.
- User changed "I believe" to "I think"; update subjective-claim phrasing.
- User replaced abstract nouns with concrete operational language.
- User kept the structure but changed diction; update phrasebank, not cadence.
- User rejected the whole framing; update intent/context interpretation.

Record the rule as one of:

- **add** — new pattern
- **strengthen** — observed again
- **weaken** — less universal than assumed
- **delete** — contradicted by user edits
- **split by context** — true in one medium, false in another

Do not overfit a global rule from one edit.

## Phase 5 — Periodic Consolidation

Every 5–10 calibration examples, rewrite the voice spec.

Produce:

```md
## Voice Spec v<X>

### Changes since v<previous>
- Added ...
- Weakened ...
- Deleted ...
- Split ... by context

### Current Voice Model
<updated spec>

### Open Questions
<contexts or patterns still uncertain>
```

Then re-apply the updated model to fresh calibration examples.

## Phase 6 — Stopping Criteria

Stop when either:

1. the user says "done", "ship it", "save it", "that's enough", or equivalent; or
2. the user accepts 5 consecutive examples with no substantive edits across at least 2 scoped contexts.

If only one context is in scope, 5 consecutive accepted examples in that context is enough.

If the user has no edits but has not explicitly asked to save, generate the final skill and say that the voice model appears stable. If the user says "save" or equivalent, create/update the skill.

## Final Output — Generated Voice Skill

The generated skill should be named `<person-slug>-voice`, for example `alex-voice`.

It should include:

- purpose and hard rule
- evidence/confidence note
- high-level voice signature
- context modes
- diction and cadence rules
- do/don't list
- phrasebank
- approved examples
- transformation workflow
- quality checklist
- maintenance instructions

Use `templates/generated-voice-skill.md` if available.

## Generated Voice Skill Hard Rule

Every generated voice skill must include this rule near the top:

> Preserve the supplied intent, facts, constraints, audience, and commitments. Do not invent what this person believes, feels, approves, promises, or knows. Voice changes expression only.

## Maintenance Mode Workflow

When the user says a generated draft does not sound like them:

1. Ask for or inspect their corrected version if available.
2. Diff the assistant draft against the correction.
3. Identify whether the correction affects diction, cadence, structure, warmth, context mode, or a hard prohibition.
4. Patch the existing voice skill with a minimal rule/example update.
5. Prefer weakening or context-splitting over adding broad rules from one example.

If a correction is important and repeatable, save it. If it is task-specific, do not encode it as voice.

## Output Style During Capture

Be concise. The user is doing high-attention editing work. Avoid long explanations during calibration rounds.

Good cadence:

1. Show 3–5 examples.
2. Ask for edits.
3. After edits, briefly state what changed in the model.
4. Continue.

Do not bury the user in analysis unless asked.

## Common Pitfalls

1. **Mimicking content instead of voice.** Do not infer the user's opinions from sample texts unless the opinion is supplied for the current task.
2. **Overfitting.** One edit rarely proves a universal rule.
3. **Flattening contexts.** Chat voice, email voice, memo voice, and public-post voice can differ sharply.
4. **Keeping stale rules.** Consolidation should delete and weaken rules, not only add them.
5. **Storing raw corpus by accident.** Default to derived rules and approved examples only.
6. **Using generic style labels.** "Direct" is not enough. Add concrete examples and transformation rules.
7. **Ignoring language switching.** If the person writes in Hebrew and English, capture when and how they switch.
8. **Stopping after easy acceptances.** Stability should span at least two contexts unless the user scoped the skill narrowly.

## Verification Checklist

Before creating or updating the generated voice skill:

- [ ] Scope, languages, and contexts are explicit.
- [ ] Raw source storage policy is respected.
- [ ] The skill preserves intent/facts and does not invent beliefs.
- [ ] At least 5 calibration examples were tested, or the user explicitly said to stop earlier.
- [ ] Accepted examples cover the requested contexts.
- [ ] Rules include confidence/context qualifiers where needed.
- [ ] The generated `SKILL.md` has valid frontmatter.
- [ ] The generated skill contains approved examples, not only abstract rules.
- [ ] The final answer tells the user where the skill was saved or what remains unsaved.
