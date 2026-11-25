---
name: yc
description: >-
  Draft or refresh a Y Combinator application from a founder hub's real evidence. Confirms the current
  batch, deadline and application questions on the web, answers only from logged evidence, marks
  unsupported claims, and lists the evidence to get before submitting. Use when preparing a YC
  application, a founder video script, or any accelerator or investor form.
argument-hint: "[batch] [refresh | gaps | video]"
---

# /yc: an application built on evidence

## The founder hub

This skill reads and writes a **founder hub**: one folder holding the startup's truth.

- **Location:** the `FOUNDER_HUB` environment variable, default `~/founder`. Below, `<hub>` means that
  folder.
- **Files this skill uses:**

| File | What it holds |
|---|---|
| `<hub>/bottleneck.md` | The current bet, this week's single bottleneck, the goal and its deadline. This skill writes the application deadline here |
| `<hub>/ideas.md` | Candidate ideas and their status; the `committed` one is what the application is about |
| `<hub>/evidence/<idea>.md` (+ `-prospects.md`, `-pipeline.md`) | Conversations, pilots, users, payments, metrics, with dates |
| `<hub>/founder.md` (optional) | The founders' background and proof of shipping and selling, in their own words |
| `<hub>/yc/<batch>-draft.md` | The application drafts this skill writes |

**If the hub or a file is missing,** say so and offer to create the minimal structure: the folder, an
empty `bottleneck.md` (current bet, bottleneck, goal, deadline), `ideas.md` with a table header (idea,
one line, who pays, evidence so far, status), an empty `evidence/` and `yc/`. With no evidence yet,
still draft, but most answers will be `[NEEDS EVIDENCE]`, and say plainly that the application isn't
ready. Never fail silently.

Read `bottleneck.md`, `ideas.md`, the committed idea's evidence files and `founder.md` if present. If no
idea is committed, say so and draft for the strongest candidate, clearly labelled as such.

## Steps

1. **Confirm the facts on the web** (web search and fetch, starting at ycombinator.com/apply): the
   current or next open batch, its application deadline, and the current application questions. Never
   assume a batch, a date or a question list from memory; they change every cycle. If the user named a
   batch, check it is still open. Record the source URL and the date you checked, and write the
   deadline into `bottleneck.md`.
2. **Draft `yc/<batch>-draft.md`,** answering every current question in plain, specific, short
   sentences. YC readers value clarity and concrete numbers.
   - The one-liner: what it is, for whom, the outcome.
   - Progress and traction: only what `evidence/` supports (conversations held, pilots, users, revenue,
     growth), with dates. **Never invent or round up a number.** If there's nothing yet, say what's
     being done this week to get some.
   - Why now, the insight, competitors: be specific. Name real competitors and say what you know that
     they don't.
   - The founders: the real story, including concrete proof of shipping and selling (from `founder.md`
     or what the user tells you). Ask rather than embellish.
3. **`gaps`:** the 3 to 5 pieces of evidence that would most strengthen the application before the
   deadline, each with the action that gets it (usually through the `discover` or `sell` skills, if
   installed).
4. **`video`:** a 60-second founder video script: who you are, what you're building, the evidence, why
   you.
5. **`refresh`:** re-check step 1, then update the existing draft from evidence logged since, and list
   what changed.

## Rules

- Evidence over adjectives; no hype words.
- Every claim traces to a file in the hub. Mark anything unsupported as `[NEEDS EVIDENCE]`.
- Draft only. The founders review and submit the application themselves; never submit a form or send
  anything on their behalf.
