---
name: skill-name-in-kebab-case
description: What this skill produces, in one clause. Use when <the concrete situations, equipment, standards, or file types that should trigger it>. Not a substitute for <the real-world artifact it approximates>.
---

# Skill Name

One or two sentences on what a good result looks like and who judges it. Naming the reviewer — "a process engineer who will spot a backwards arrowhead" — sets the bar far better than an adjective like "high quality".

## Non-negotiable output rules

The handful of things that make the output wrong if violated. Keep this short; if everything is non-negotiable, nothing is.

1. …
2. …

## Workflow

### 1. Read the request and fill the gaps

What is almost always underspecified? List the questions worth asking, and cap them (e.g. "ask at most 2–3, and only for things that change the answer"). For everything else, make a defensible assumption and state it afterward.

### 2. Plan before producing

The step that prevents rework.

### 3. Produce

Point at `scripts/` and `references/` here rather than restating their contents:

> `scripts/<module>.py` provides the primitives. Read it before writing anything and use it rather than reinventing. Read `references/<topic>.md` for the conventions.

### 4. Check the output and fix it

**The step that separates a passable result from a professional one.** Render it, run it, or validate it — then actually look at the result and iterate. Say how many rounds to expect and list the defects that are only visible on inspection.

### 5. Deliver

Where the output goes, and what to state alongside it: assumptions made, anything that couldn't be done and why, and any concern noticed along the way. Flagging concerns is usually a large part of the value.

## What this skill does not do

State the limits plainly, and say so to the user if their framing suggests they expect more. Everything in this repo is conceptual, engineering-support output — not issued-for-design work, not hazard analysis, not equipment sizing.
