---
name: generate-cfp
description: Generate a complete conference proposal through a structured brainstorming Q&A. Produces abstract, extended abstract, title variants, and learning outcomes — calibrated to the session format and grounded in your DevRel context.
---

Before doing anything else:
1. Check if `~/.devadvokit.md` exists.
2. If it does, read it silently and use it throughout this skill.
3. If it does not, stop and tell the user: "I need your DevRel context before I can run this skill. Please run /setup-devadvokit first."

---

## Brainstorming Q&A

Ask these questions one at a time. Wait for each answer before asking the next. Do not batch questions.

1. What session format are you submitting for, and how long is the slot? (e.g. talk / 30 min, workshop / 90 min, panel / 45 min — or unknown if the CFP is open) This determines structure, depth, and pacing of everything that follows.
2. What problem does this talk address? (What situation is the audience in that makes this relevant?)
3. In this talk, you will learn... (What are the 2–3 concrete things attendees will take away?)
4. You will leave with... (What can they do immediately after? Tools, frameworks, checklists, mental models?)
5. This talk is for... (Who specifically? Be as precise as possible about job role, situation, and what they're trying to do.)
6. Why are you the best person to deliver this? (What experience, data, or access do you have that others don't?)
7. Do you have a working title, or should we generate one?
8. Is there a specific event or CFP you're writing this for? (If yes, any known word limits or format requirements?)

Consult `reference/cfp-evaluation-criteria.md` and `reference/cfp-anti-patterns.md` throughout to assess answer quality. If an answer is vague or likely to produce weak output (e.g. a thin problem statement, a generic audience description), ask one focused follow-up question before moving on.

---

## Output

Produce all of the following once the Q&A is complete.

### 1. Abstract
100–150 words. Written for the attendee, not the programme committee. Answers: what's the problem, who's it for, what will they get. Calibrate length and structure to the session format given in question 1. No headers.

### 2. Extended abstract
200–300 words. Same voice as the abstract, more detail on the session structure and specific takeaways. Can use light structure (short paragraphs or a brief outline) if the format warrants it.

### 3. Title variants
3 options. Range from descriptive to punchy. No colon-with-subtitle constructions unless they genuinely improve clarity. No question marks.

### 4. Learning outcomes
3–5 bullet points. Concrete and specific. Each starts with a strong verb. "Understand how to..." is weak; "Run a competitor pricing audit using publicly available data" is strong.

### 5. Content library check
Scan the content library in `~/.devadvokit.md`. If any existing content covers similar ground, note it at the end:

> "This overlaps with [title] ([year]) — you may want to position this as an update or take a different angle."

If nothing overlaps, omit this section entirely.

---

Before presenting any output, read `../../shared/ai-antipatterns.md` and silently rewrite any flagged patterns. Do not mention this step to the user.
