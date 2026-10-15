---
name: find-content-angles
description: Use when you have a single piece of content (blog post, talk, case study, docs PR) and want to extract multiple content angles from it — abstraction ladders, audience pivots, controversy checks, and hidden assumptions that could each become their own piece.
---

Before doing anything else:
1. Check if `~/.devadvokit.md` exists.
2. If it does, read it silently and use it throughout this skill.
3. If it does not, stop and tell the user: "I need your DevRel context before I can run this skill. Please run /setup-devadvokit first."

---

## What NOT to Do

This skill produces angles, frameworks, and directions — not finished content. Specifically:

- **No full drafts** — you're finding the seeds of future pieces, not writing them
- **No SEO keyword research** — that's a different skill for a different workflow
- **No social media posts** — use `/repurpose-talk` for that

The goal is content strategy discovery, not content production.

---

## Q&A

Ask these questions one at a time. Wait for each answer before asking the next.

1. What's the content piece? Paste or describe it — blog post, talk abstract, case study, docs PR, etc. This is your source material.

2. What was the core insight or lesson here, in one sentence? (What's the one thing you want people to take away?)

3. Who was the original audience for this piece? (The people you wrote it for the first time.)

4. What response did this get when you published it? (Comments, questions, "but what about X" — these are clues for angles you didn't explore.)

---

## Output

Produce all of the following once the Q&A is complete.

### 1. Abstraction Ladder

Start with the specific problem you solved, then climb up 3 levels of generalization:

- **Level 1 (specific):** [What you actually did]
- **Level 2 (pattern):** [What this is an instance of]
- **Level 3 (principle):** [What principle this demonstrates]
- **Level 4 (universal):** [What universal truth this points to]

Include one sentence on when each level is the right framing for a new piece.

### 2. Audience Pivots

The same insight reframed for different readers. Generate 3 pivots:

- **Pivot 1:** [Different job role perspective]
- **Pivot 2:** [Different experience level perspective]
- **Pivot 3:** [Different context/industry perspective]

For each pivot:
- Who they are (specific)
- What they care about that's different from the original audience
- How the same insight serves them differently
- A working title for this angle

Ground pivots in your actual audience knowledge from `~/.devadvokit.md`.

### 3. Controversy Check

Is there a defensible contrarian take buried in this piece? Most educational content has one. Surface it:

- **The conventional wisdom:** [What most people believe or do]
- **Your contrarian angle:** [Where you disagree or take a different path]
- **Why it's defensible:** [Evidence, experience, or reasoning]
- **The piece this could become:** [Title + premise]

If no genuine controversy exists (not all content has one), note: "No strong contrarian angle — this is consensus-building content" and move on.

### 4. "What This Assumes"

Surfaces hidden assumptions in your argument. Each could become its own piece:

List 3–5 assumptions your piece makes that readers might not share. For each:

- **Assumption:** [What you're taking for granted]
- **Who might not share it:** [Which audience segment]
- **The piece this assumption could become:** [Title + brief description]

---

## Content Library Check

Scan the content library in `~/.devadvokit.md`. If any existing content covers similar angles or themes:

> "This overlaps with [title] ([year]) — consider whether this angle adds something new or whether you're retreading ground."

If nothing overlaps, omit this section entirely.

---

Before presenting any output, read `../../shared/ai-antipatterns.md` and silently rewrite any flagged patterns. Do not mention this step to the user.