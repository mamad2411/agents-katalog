---
name: no-doubts
description: >
  Interview the user relentlessly about a plan, design, or topic, checkpointing every answer to a
  brainstorm file so nothing is lost. Use when the user wants to stress-test a plan, get grilled on
  a design, run a brainstorm or discovery session, extract what's in their head into a doc, or says
  "grill me", "no doubts", "any doubts", "stress test this", "what am I missing", "poke holes",
  "challenge this", "steel man this", "red team this plan".
domain: process
composable: true
yields_to: []
---

# No Doubts

Relentlessly interview the user about every aspect of their topic until you reach shared understanding. Walk down each branch of the decision tree, resolving dependencies one by one. The real goal is to **extract what's in their head into a durable, organized markdown file** so nothing is lost as context fills up.

## The capture file is the whole point

Long interviews fill up context. If you hold answers only in your head, you will eventually misremember, conflate, or drop something. So you **checkpoint to disk after every single answer**. The file, not your context, is the source of truth. Never make the user ask you to save progress.

## Setup (do this BEFORE the first question)

1. **Create the capture file** at `brainstorms/{YYYY-MM-DD}-{topic-slug}.md` (create the `brainstorms/` folder if it doesn't exist). Every brainstorm capture lives here. One predictable home, regardless of topic. Do NOT scatter captures into project folders. If a session later produces a polished deliverable (a plan, a map, a spec), that artifact can move into the relevant `projects/` folder, but the raw capture always stays in `brainstorms/`.
   - Get today's date with `date +%F` (Bash) if you don't already know it.
2. **Create the file immediately** with a header: title, date, the goal of the session, and an empty "Open flags" section.
3. **Tell the user where you're saving**, in one line. Then ask Q1.

## The checkpoint rule (non-negotiable)

After EVERY user answer, BEFORE you ask the next question:
- Append a structured entry to the capture file: the question topic, the key facts and decisions from their answer (in their words where the wording matters), and any flags (things they couldn't answer plus who should).
- Update or correct earlier entries if a later answer changes them.
- Only then ask the next question.

Never batch multiple answers into one write. Checkpoint one answer at a time. The point is that if context is lost at any moment, the file already holds everything said so far.

## Interview method

- Ask **one question at a time**. For each, provide your **recommended answer** (your best inference from context) so the user can simply confirm, correct, or redirect.
- Resolve dependencies in order: settle the upstream decision before the ones that depend on it.
- If a question can be answered by **exploring the codebase or reading a file/doc**, do that instead of asking. If the user hands you a doc (e.g. a Google Doc), read it and only surface what's net-new.
- When the user **can't answer** something, capture it as a flag with the right owner and move on. Don't stall.
- Keep going until the user says you're done, or you've covered every branch. Offer a completeness backstop near the end ("anything we haven't touched?").

## Question types — probe from multiple angles

Don't just ask "what do you want?" Rotate through these lenses:

| Lens | What it reveals | Example |
|------|----------------|---------|
| **Constraints** | Hard limits (time, budget, tech) | "What's non-negotiable here?" |
| **Tradeoffs** | What they're willing to sacrifice | "If X or Y had to give, which stays?" |
| **Success** | What "done" looks like | "How will you know this worked?" |
| **Failure** | What they're afraid of | "What would make this a waste of time?" |
| **Scope** | Where the edges are | "What's explicitly NOT part of this?" |
| **Priority** | What matters most | "If you could only ship one piece..." |
| **History** | What they've already tried | "What have you attempted before?" |
| **Audience** | Who this is for | "Who's the first person that'll use this?" |

## Capture file structure

```
# {Topic}: Brainstorm / Discovery Notes
Date: {date} · Goal: {one line}

## Summary / key decisions
(running synthesis, updated as you go)

## Q&A log
### Q1 — {topic}
- Asked: {question}
- Captured: {facts, decisions, in their words where it matters}
- Flags: {open item -> owner}
...

## Open flags (pending input)
- {item} -> {who can answer}
```

## At the end

- Do a final read of the capture file for contradictions or gaps and reconcile them.
- Give the user a short recap: what's captured, what's still flagged, and the suggested next step.

## Composability — Working With Other Skills

> **See `PROTOCOL.md` (SIP) at skills root for full interop contract.**

### Domain Declaration

```yaml
domain: process
composable: true
yields_to: []
```

No-doubts owns **process** — the structured interview workflow for extracting and capturing user intent.

### When No-Doubts Leads

- User wants to stress-test a plan or design
- User says "grill me", "no doubts", "any doubts", "challenge this"
- User wants a brainstorm or discovery session
- User has a fuzzy idea and needs to crystallize it
- User says "what am I missing" or "poke holes in this"

### When No-Doubts Defers

| Other Skill's Domain | What No-Doubts Does |
|---------------------|---------------------|
| **Voice** (e.g. blogger) | No-doubts structures the interview. Voice handles tone of the capture file prose if needed. |
| **Craft** (e.g. painter) | No-doubts captures design intent. Craft handles visual design decisions. |
| **Content** (e.g. researcher) | No-doubts captures the question. Researcher does the deep dive. |

### Conflict Signal

> `⚠️ Process conflict: [what's conflicting]. [What was chosen, what was preserved].`
