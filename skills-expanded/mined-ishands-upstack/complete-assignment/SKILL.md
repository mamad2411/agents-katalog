---
name: complete-assignment
description: >
  Run the reasoning review gate for a completed assignment. Asks 2-3
  Reasoning Review Prompts from COURSE.md, verifies genuine understanding,
  and only marks the assignment complete if the learner demonstrates
  conceptual grasp. Use when a learner finishes an assignment and is
  ready for verification.
metadata:
  version: '1.0'
---

## Purpose

This skill is the gate between "the work is done" and "the assignment
is complete." A correct result is necessary but not sufficient — the
learner must demonstrate they understand what they built and why.

The reasoning review serves two functions:

- **Verification** — confirm the learner has genuine conceptual grasp,
  not just a working output.
- **Final teaching moment** — surface latent gotchas, edge cases, and
  failure modes the learner hasn't encountered yet. The review is not
  an interrogation; it is the last opportunity to deepen understanding
  before moving on.

---

## Before You Start

Read these files — they must be in your context before continuing:

1. The active `COURSE.md` — specifically the Reasoning Review Prompts
   for the assignment being completed
2. `progress/<slug>/learner-context.md` — the learner's Dreyfus level
   and background in this subject
3. `core/meta/TUTOR-CONTRACT.md` §7 — the reasoning review protocol

---

## Procedure

### Step 1 — Identify the assignment

Read `progress/<slug>/journal.md`. Find the **Progress Tracker**
section. Look for the first unchecked assignment (`- [ ]`).

- **If the learner named a specific assignment** — confirm it matches
  the next unchecked item. If it doesn't, ask: "Your next unchecked
  assignment is [X]. Did you mean that one, or are you completing [Y]
  out of order?"
- **If the learner didn't specify** — assume the first unchecked
  assignment. Confirm: "It looks like you've finished [title]. Ready
  for the reasoning review?"
- **If all assignments are already checked** — tell the learner the
  course is fully complete. There is nothing to mark.

### Step 2 — Load context

Read the following to calibrate the review:

1. **COURSE.md** — find the Reasoning Review Prompts for this
   assignment. These are the questions you will ask.
2. **`progress/<slug>/learner-context.md`** — note the learner's
   self-declared Dreyfus level in this subject and their prior skills.
   This determines probe depth:
   - **Novice/Beginner** — probe for rules and heuristics. "When
     would you use this pattern?" "What's the rule of thumb here?"
   - **Competent+** — probe for nuance and trade-offs. "Where does
     this break down?" "What would you change if the constraints
     shifted?"
3. **`profile/PROFILE.md`** (if it exists) — cross-reference the
   learner's broader background. Their mental models from other
   domains may inform better probing questions.

### Step 3 — Run the reasoning review

Ask 2–3 Reasoning Review Prompts from COURSE.md. One prompt at a
time — wait for the learner's response before asking the next.

For each prompt:

- Require explanation in the learner's own words. Not recitation
  from documentation, not code snippets, not rote recall.
- Push for edge cases: "Where does this pattern break down?"
- Push for trade-offs: "Why this approach instead of the alternative?"
- Calibrate depth to the learner's Dreyfus level (Step 2).

Do not rush through the prompts. Each answer deserves a response —
acknowledge what's correct, probe what's vague, correct what's wrong.

### Step 4 — Evaluate understanding

**If understanding is shallow:**

- Do not mark the assignment complete.
- Identify the specific gap: "Your explanation of [X] suggests you
  might be thinking of it as [Y]. That's a common mental model but
  it breaks when [Z]."
- Tell the learner what to work on: "Spend some time with [concept].
  Try [specific exercise or re-reading]. When you're ready, invoke
  this skill again."
- **Exit.** Do not loop or re-ask. The learner needs time to work
  through the gap, not another question in the same sitting.

**If understanding is strong:**

- Use the review as a final teaching moment (Tutor Contract §7.3).
  Surface one latent gotcha or failure mode the learner hasn't
  encountered: "You've explained this correctly. What happens
  when [edge case]? Does your approach still hold?"
- This is a gift, not a trap. If the learner doesn't know, briefly
  explain — they've earned it. Don't turn the teaching moment into
  another gate.
- Proceed to Step 5.

### Step 5 — Update the journal

Make two changes to `progress/<slug>/journal.md`:

**1. Progress Tracker** — change the assignment's checkbox:

```
- [x] **Assignment N: Title** — completed YYYY-MM-DD
```

Use today's date.

**2. Completion Marker** — add a section at the end of the
assignment's journal content (after What Clicked, or after the last
populated section):

```markdown
## Assignment N: Title — Completed YYYY-MM-DD

**Key takeaway:** {the learner's answer — see below}
```

Ask the learner: "What was the single most important thing you
learned from this assignment?" Use their answer as the key takeaway.
Write it in the learner's voice, not yours.

### Step 6 — Commit

Present the commit message to the learner:

```
progress: complete <assignment-title>
```

Wait for the learner to commit.

---

## Notes

- **This is a conversation, not an exam.** The reasoning review
  should feel like a discussion between a mentor and a learner who
  just finished something meaningful. Acknowledge effort. Be
  genuinely curious about their reasoning.
- **Don't rubber-stamp.** "I understand" is not evidence of
  understanding. Neither is restating the documentation. Push for
  the learner's own mental model — how they think about it, not
  how the textbook describes it. **[Anti-pattern 5]**
- **Don't interrogate.** If the learner gives a correct but brief
  answer, a light follow-up probe is fine. Demanding exhaustive
  explanations for every concept turns the review into a chore.
  Two or three well-chosen prompts are enough.
- **Calibration matters.** A novice who can articulate the basic
  rule correctly has demonstrated understanding at their level. Don't
  demand expert-level nuance from a beginner. Conversely, don't let
  an experienced learner pass with surface-level answers.
- **The key takeaway is the learner's, not the tutor's.** Resist
  the urge to rewrite or "improve" their answer. If it's vague,
  ask them to sharpen it. But the words should be theirs.

---

## Reference

- Reasoning review protocol: `core/meta/TUTOR-CONTRACT.md` §7
- Learning principles (P8 — Verify Understanding, Not Output):
  `core/meta/PRINCIPLES.md`
- Journal template and completion marker format:
  `.agents/skills/core/start-course/references/JOURNAL-TEMPLATE.md`
- Tech spec §6.3.2: full skill specification
