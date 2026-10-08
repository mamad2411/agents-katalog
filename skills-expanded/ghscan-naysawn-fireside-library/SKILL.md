---
name: bahai-module
description: Create structured Baha'i educational modules for seeker deepening. Use this skill whenever Naysawn asks to write, draft, create, or build a module, lesson, or educational session — even if he doesn't use the word "module". Also trigger when he asks to turn source material into a discussion format, or wants to create something for a group exploring the Baha'i Faith.
---

# Bahai Module Skill

Creates structured two-section educational modules in markdown format for seeker deepening. The audience is always a mixed group of 2 Baha'is and 2 people learning about the Baha'i Faith — assume no prior Baha'i knowledge from half the room.

Each section follows this structure: opening exploration questions → reading passage → discussion questions.

---

## Spelling Conventions

- Write **Baha'i** with its apostrophe (e.g. "the Baha'i Faith", "a Baha'i community")
- Write names like **Baha'u'llah**, **Abdu'l-Baha**, **Shoghi Effendi** with standard apostrophes and hyphens, but **without diacritical marks** (no dots under letters, no macrons, no special characters)
- Apply this consistently throughout all output — reading passages, questions, and headers

---

## Fixed Assumptions (do not ask Naysawn about these)

- **Audience**: Mixed group of 2 Baha'is and 2 seekers (non-Baha'i)
- **Format**: Group discussion setting
- **Sections**: 2 by default (Naysawn can override)
- **Reading length**: 500–750 words per section (reading passages only, not counting questions)
- **Questions per section**: 3 opening reflection questions + 3 closing discussion questions
- **Source material**: Always provided by Naysawn — never generate, invent, or substitute your own

---

## Interview Phase (Always Run First)

Ask only these questions before starting. Wait for answers before proceeding.

1. **What is the topic or theme of this module?**
2. **Please paste in the source material.** (All reading passages must be grounded in what Naysawn provides.)
3. **Are there specific quotations from the Writings you want included?** (If not specified, draw from the source material provided.)
4. **How many sections?** (Default is 2 — confirm or ask if he wants to override.)

---

## Workflow (follow this exactly, step by step)

### Step 1: Analyze & Propose Section Divisions

Read the source material carefully. Then propose to Naysawn how to divide it into 2 sections — what each section would focus on and why that arc makes sense given the material. Wait for his confirmation or adjustment before proceeding.

### Step 2: Propose 3 Arcs Per Section

For each section, propose **3 different narrative arcs** — each a distinct way to frame or build the argument of that section using the source material. Present them as short 2–3 sentence summaries. Example arc format:

> **Arc A — [Short title]**: This section would open with [angle], build through [key idea], and land on [conclusion or tension].

Wait for Naysawn to choose or tweak an arc for each section before drafting anything.

### Step 3: Draft Section 1

Draft Section 1 reading passage only (no questions yet) based on the chosen arc. Present it for review. Iterate until Naysawn approves it.

### Step 4: Draft Section 2

Draft Section 2 reading passage only. Present it for review. Iterate until Naysawn approves it.

### Step 5: Propose Questions

Once both reading passages are approved, propose **10 opening reflection questions and 10 closing discussion questions** for the module as a whole. Present all 20 as a numbered list and let Naysawn select and tweak. The final module will use 3 opening + 3 closing questions per section (6 total opening, 6 total closing drawn from the pool of 20).

### Step 6: Collate and Output

Once questions are finalized, assemble the complete module in the output format below and present it as the finished product.

---

## Writing Guidelines

### Opening Reflection Questions
- Draw on universal human experience — answerable by anyone regardless of faith background
- Do not introduce Baha'i concepts; let the reader arrive from their own life first
- Questions should feel genuinely curious, not leading
- Strong example: *"Have you ever had a moment where you felt certain of God's presence? What was happening?"*
- Avoid questions that telegraph the "right" answer

### Reading Passages
- Write in clear, warm, accessible prose — readable aloud in a group conversation
- Weave quotations into the prose naturally; never drop them in as standalone block quotes
- Stay strictly grounded in Naysawn's source material
- Each passage should build a coherent argument or narrative arc, not just list ideas
- Attribute quotes clearly: *Baha'u'llah writes... / Abdu'l-Baha explains... / Shoghi Effendi notes...*
- Write for a non-Baha'i reader — avoid assumed familiarity with Baha'i terminology; briefly gloss any technical terms

### Closing Discussion Questions
- Require genuine reflection — no obvious answers
- Push into implications, tensions, and personal application
- At least one question per section should connect the spiritual principle to lived experience
- Avoid leading questions (e.g. "Don't you think...?" or "Wouldn't it be true that...?")
- Strong questions hold a tension: *"If God is truly unknowable, what does it mean to grow closer to Him?"*

### Common Failure Modes to Avoid
- **Too long**: Stay within 500–750 words per reading passage. Cut ruthlessly.
- **Weak sourcing**: Every claim in the reading must trace back to the provided source material
- **Leading questions**: Questions should open exploration, not confirm conclusions
- **Surface-level questions**: If a question can be answered in one sentence without real reflection, go deeper
- **Dropped quotes**: Quotations must be integrated into prose, never floated on their own
- **Assumed Baha'i knowledge**: Write as if half the room has never heard of the Faith

---

## Output Format

```
# [Module Title]

## Section 1: [Section Title]

### Questions for Reflection

1. ...
2. ...
3. ...

### Reading

[Prose passage with integrated quotations]

### Questions for Discussion

1. ...
2. ...
3. ...

---

## Section 2: [Section Title]

### Questions for Reflection

1. ...
2. ...
3. ...

### Reading

[Prose passage with integrated quotations]

### Questions for Discussion

1. ...
2. ...
3. ...
```

---

## Common Module Topics (for context only — do not substitute for provided source material)

- Baha'i administrative order
- Importance of service in the Baha'i Faith
- Life of Baha'u'llah
- Why suffering exists
- The Nine Year Plan
- Why the world is chaotic
- Baha'i spiritual principles
- The nature of God and developing a relationship with God
- Progressive revelation
- The soul
- Prayer and devotion
- The harmony of science and religion

---

## Reference Files

- `references/example-module.md` — A completed module showing the target quality level. Read before drafting to calibrate tone, depth, question style, and how quotations are integrated into prose.
