---
name: codesplain
description: Use when working in a coding project owned by a non-coder - when the project root contains CODESPLAIN.md, when the user invokes /codesplain (to bootstrap a project or ask a question), when a consequential technical decision comes up during building, or when explaining a bug or fix to the owner in plain language.
---

# Codesplain

## Overview

Maintain `CODESPLAIN.md`: a living plain-language map plus decision log that lets a non-coder owner understand their own project, check the AI's work, and learn over time. The doc is a witness, not documentation. It only works if it stays short, current, and honest.

## The file (structure contract)

`CODESPLAIN.md` lives in the project root and has exactly three sections:

1. **Map** - 5 to 10 functional areas, each one something the owner would name when describing the product to a friend ("Turn resolution", "Saving games"), never a file or folder name. Each area gets one plain-language paragraph: what it does, why it exists, which files it lives in (as pointers), what it talks to. Hard cap: the whole Map fits in about 2 screens of text. Never go per-file; that produces an unreadable monument. If an area is genuinely huge, its paragraph ends with: "This is the biggest part - ask me to codesplain it if you need the layer below." Content inferred from existing code (not from a live decision) is marked *(inferred)*.
2. **Decision Log** - append-only, newest last. Each entry: date, area tag in bold, then **3 to 5 sentences maximum**: what was decided, why, the main alternative, what could break or bite later. At 6 sentences, cut the weakest one.
3. **Glossary** - every technical term the doc uses, defined once in plain language. Add a term the first time an entry needs it.

## Modes

- **`/codesplain` (no args, no file yet)** - bootstrap. Existing code: scan the project, write the Map (inferences flagged), plus empty Decision Log and Glossary sections. New or empty project: write the skeleton only; capture is live from the first decision, so the doc never needs archaeology.
- **`/codesplain <question or area>`** - answer ELI5, grounded in the Map and the code. If answering reveals the Map is wrong or stale, fix it.
- **Ambient capture** - in any session in a project containing `CODESPLAIN.md`, apply the capture tiers below.
- **Bug and fix explanations** - anchor every explanation to a Map area by name: "This is in **Turn resolution** - the part that decides what order player actions happen in." If what the code actually does contradicts the Map, say so out loud and correct the Map. Never silently paper over a contradiction.

## Capture tiers

**Tier 2 - STOP AND ASK BEFORE ACTING.** Explain the tradeoff ELI5, give a recommendation, wait for the owner's call. Triggers:
- The choice costs money or adds a paid service.
- Lock-in: switching later means a rewrite.
- Scope or time tradeoffs the owner should weigh (robust version = days more work).
- **Data safety: existing saves, files, or user data would become unreadable or could be lost.** Changing a data format so old data stops loading is Tier 2, not Tier 1. Doing it first and confessing after is a violation - the owner decides, before.

**Tier 1 - do it, then log.** Triggers:
- New dependency (a library added).
- New moving part other code will depend on (a new module, service, engine).
- Data-shape change that does NOT orphan existing data.
- Irreversible or expensive-to-undo choice that misses every Tier 2 trigger.
- Deliberate hack or workaround. Label the entry "TEMPORARY WORKAROUND" and state the symptom the owner would notice ("if the game feels laggy, this is the first place to look").

**Every Tier 1 capture has three jobs, not one:**
1. Append the log entry.
2. **Update the affected Map paragraph.** This is the most-skipped step and the one that keeps the doc alive. A capture that only appends to the log is incomplete.
3. One-line chat mention: "Logged to CODESPLAIN.md: chose zod to validate move orders - one clause why." Never stop work to ask permission for a Tier 1 item.

**Never capture:** bug fixes, behavior-neutral refactors, tests, styling, copy changes, renames, new functions inside an existing module.

## Voice

Write for a smart adult who has never coded - not a five-year-old. Plain phrase first, real term second: "the part that remembers the game between sessions (the *persistence layer*)". The term then goes to the Glossary. Analogies only when they pay rent (board-game analogies land well in game projects). Honest tradeoffs stated plainly; no baby talk, no hype, no em dashes.

## Hygiene

When the Decision Log passes roughly 2,000 words, move the oldest entries to `CODESPLAIN-archive.md` and leave one pointer line. The Map is never archived; it is always whole and current.

## Common mistakes (all observed in testing)

| Mistake | Fix |
|---|---|
| Bootstrap writes a per-file essay | Map = 5-10 owner-recognizable areas, 2-screen cap, files as pointers only |
| Capture appends a log entry but skips the Map update | Both, every time - the Map update is what keeps the doc alive |
| 6-8 sentence log entries | 5 sentences max, cut the weakest |
| Breaking existing data, then confessing afterward | Data-destructive = Tier 2: ask FIRST, act after the owner decides |
| Logging refactors, tests, renames | Silent. Logging noise trains the owner to stop reading |
