---
name: deck-grilling
description: Use when a medical presentation is about to be planned or built and the deck type, audience, purpose, duration, language, output format (HTML or PPTX), template or sources have not all been stated by the user, or when someone wants their talk idea stress-tested.
---

# Deck grilling

## Overview

Interview the presenter until you share one picture of the talk. Map it as a **design
tree**: each decision branches into the decisions that depend on it (a journal club opens
questions about appraisal depth; a clinical case opens questions about consent).

Finding **facts** is your job. Making **decisions** is theirs. A decision you fill in
yourself is an assumption, and assumptions are what this skill exists to remove.

## How to run it

Work in **rounds**. The **frontier** is every open decision whose prerequisites are
settled. Ask the whole frontier in one message, numbered, each with your recommended answer,
worded so "yes" accepts it:

```
❓ **Q1 · Output format**: HTML (one offline file; animation; laser pointer and pen while
presenting) or PowerPoint (.pptx; editable by you and your department)? Or both?

➡️ Recommended: HTML, because <reason from what they told you>.

---

❓ **Q2 · Template**: Do you have a template to follow: a hospital/university .pptx or
.potx, a conference template, or slides whose look you want? If yes, attach it.

➡️ Recommended: <…>
```

**Each round ends your turn.** Send the questions and stop: no files, folders, searches for
the talk's content, or drafts until the user replies.

After each answer, recompute the frontier and ask the next round. A question whose answer
depends on another question still open belongs to a later round.

The first round almost always contains these, unless the user already stated them:
deck type and purpose, audience, duration, language, **output format**, **template**,
sources, presenter and event. The full tree is in `question-tree.md`.

**Facts are yours:** paper metadata, trial registration, guideline version, what a
template file contains. Look these up (tools, files, a subagent) and do not ask the user.
Ask the questions that don't depend on the lookup while it runs.

**Hurried users get one round, not zero.** Put every frontier question in a single message
and say "reply 'yes' to accept all recommendations". That costs them ten seconds.

Never ask about colours, fonts or layout when a template answers them. Never ask the user
for a fact you can find.

## Done means

The frontier is empty and the user has confirmed this summary. Write it to
`<talk>/brief.md`:

```markdown
# Brief: <working title>
- Deck type / purpose:
- Audience (level, specialty, size):
- Event, date, venue, projector (16:9 / 4:3), offline?:
- Duration (talk / Q&A) → slide budget:
- Language (+ terminology convention):
- Output format: HTML | PPTX | both
- Template: <file path> | none (palette chosen: …)
- Presenter (exact name and title as printed):
- Sources supplied: <files> | to be researched (databases allowed: …)
- Core message (one sentence the audience should remember):
- Must include / must avoid:
- Figures: reuse originals? motion graphics? (level) · AI image account: ChatGPT | Gemini | both | none
- Patient data: none | de-identified, consent: …
- Open items:
```

Do not plan or build before the user confirms the brief.

## Red flags

| Thought | Reality |
|---------|---------|
| "PPTX is the safe default" | Format changes the whole build. It is their decision. |
| "No template mentioned, so none exists" | Ask. Hospitals and congresses usually have one. |
| "I'll ask, and start on the plan while they read" | Asking means waiting. End the turn after the questions. |
| "I'll list my assumptions and proceed" | Listing assumptions after deciding is not asking. |
| "Too many questions will annoy them" | One numbered round with recommendations is fast. Zero rounds leads to rework. |
| "I'll ask which trial they mean" | If the paper is identifiable, look it up yourself. |
