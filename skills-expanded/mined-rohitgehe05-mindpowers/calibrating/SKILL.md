---
name: calibrating
description: Use after a knowledge-work deliverable ships or gets human edits. Triggers on "that draft worked", "they rewrote half of it", "remember this for next time", or when the user returns with feedback on a shipped doc. Not for code retrospectives.
---

# Calibrating

## Overview

mindpowers does one loop: shape, draft, review, fact-check, and remember what you like. This skill is the "remember" step, and the only one that writes `docs/mindpowers/preferences.md`. `mindstorming` step 1 reads that file before it starts a new session, so what gets recorded here shapes every future spec of that template type.

This is a light skill. Don't turn it into an interrogation: most of the time there are 1-3 short questions and one write.

## User-Facing Language

Think precisely; respond plainly. Use common words and short sentences. Explain
an unavoidable technical term the first time it appears, and give one short
example when a rule could be misunderstood. For a material conclusion about a
preference or proposed write, give a compact explanation: the recommendation or
conclusion, what you checked, the main reasons, uncertainty, and the next step.
Do not dump internal machinery. If the user says the explanation is unclear,
explain it again from scratch.

## Process

1. **Identify what this is about.** Figure out which spec/draft the feedback concerns. Scan `docs/mindpowers/specs/` and `docs/mindpowers/drafts/` for a matching topic or recent file; if it's genuinely ambiguous, ask which one. Note its template `type`: preferences are filed under that type.
2. **Compare supplied versions first.** When the user supplies or points to both the Mindpowers draft and the final human-edited artifact, compare them before asking questions. Identify meaningful changes and infer their likely intent from context. Ask only about meaningful changes whose intent cannot be inferred.
3. **Ask at most 3 questions**, skipping any already answered by what the user said or by the comparison:
   - What landed: what worked and should happen again?
   - What got cut or rewritten by a human: where did the draft miss?
   - What should change next time?
4. **Distill into 1-3 one-line preference entries.** Record only stable preferences, not a general evaluation of the product, field, or artifact. Keep entries short, concrete, reusable, and distinct from a summary of the conversation.
5. **Show the entries and get approval before writing.** Let the user edit the wording.
6. **Append to `docs/mindpowers/preferences.md`** under the matching template's section.

## preferences.md format

Markdown, sectioned by template type, each section a flat bullet list of dated one-liners:

```markdown
<!-- Read by mindstorming step 1. Written only by calibrating. -->

## business-review
- 2026-07-07: audience is CPO not VP, default audience field accordingly
- 2026-03-12: prefers UK spelling

## decision-doc
...

## general
- 2026-01-20: keep recommendations to one sentence, always up front
```

Sections match the 9 template types (`business-review`, `decision-doc`, `one-pager`, `prd`, `briefing-doc`, `comms-draft`, `framework`, `talking-points`, `post-mortem`) plus `general` for anything cross-cutting. If the file doesn't exist, create it with the header comment above and only the section(s) you're writing to, no need to pre-populate all 10.

## Rules

- **Never record sensitive content.** If feedback is political ("X didn't like the framing"), generalize it to a role ("the exec sponsor preferred a shorter framing"), not a name.
- **Prune on write.** If a new entry contradicts an older one in the same section, replace the old line rather than appending a second one that disagrees with it.
- **Cap each section at ~10 bullets.** If a write would push a section over that, merge overlapping entries or drop the stalest one. If it's unclear which to drop, ask the user rather than guessing.
- Keep entries short, one line each. This file gets read at the start of every mindstorming session; it should stay skimmable.
- Never ingest the Mindpowers draft or final human-edited artifact into a corpus.

## Cowork / no-filesystem fallback

Paths above are relative to the working folder; in Cowork that's the user's shared folder. If no writable folder exists, show the proposed entries in chat and say plainly they weren't saved, since there's nowhere for the next session to read them from either.
