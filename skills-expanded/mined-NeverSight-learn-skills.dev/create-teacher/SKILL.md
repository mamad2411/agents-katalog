---
name: create-teacher
description: >
  Use when the user wants to set up a teacher persona, configure a learner profile, or
  initialize the teacher directory for a learning project. Trigger when the user says
  things like "set up my teacher", "create a persona", "I want to start learning with
  Socrates-7", "initialize my learning setup", or "help me design a teacher". This skill
  MUST run before any teaching session can begin — invoke it proactively if no teacher/
  directory exists in the workspace.
---

# Create Teacher

This skill sets up the `teacher/` directory by interviewing the user and producing four
files: a persona spec, a learner profile, a session log, and a knowledge gaps tracker.

**Templates to reference:** [persona_example.md](examples/persona_example.md) and
[learner_profile_example.md](examples/learner_profile_example.md) in this skill directory.

---

## Interview Protocol

Ask one question at a time. Wait for the answer before moving to the next. Do not batch
questions or rush — the answers directly shape the files you will create.

### Step 1 — Learner identity

Ask:
> "What's your name, and briefly: what's your academic or professional background?"

### Step 2 — Subject and goals

Ask:
> "What subject are you studying, and what do you want to get out of it? (A skill, a
> qualification, research depth, something else?)"

### Step 3 — Knowledge level

Ask:
> "How much do you already know about this subject? Be honest — it helps me calibrate
> the starting point."

### Step 4 — Learning preferences

Ask:
> "How do you like to receive feedback — direct and blunt, or gentler? Any other
> preferences about how you learn best?"

### Step 5 — Persona design

Tell the user:
> "Now let's design your teacher. I'll ask a few short questions."

Then ask each in turn:
- "Give them a name."
- "Pick a personality style: strict/efficient, warm/patient, playful/energetic, or
  serious/academic — or describe your own."
- "What's their relationship to you: mentor, TA, study partner, or something else?"
- "Any specific quirks, speech patterns, or traits you want them to have?"
- "What's their backstory — why do they teach, and what are they an expert in?"

### Step 6 — Blackboard style

Ask:
> "The teacher uses a Jupyter notebook as a blackboard — writing formulas, running
> code demos, and setting exercises. What style do you prefer?
> - **Minimal:** key formulas only
> - **Moderate:** formulas + diagrams
> - **Rich:** code + plots + annotations"

---

## Files to Create

After completing the interview, create the `teacher/` directory (or use the existing one)
and write these four files:

### `teacher/persona_[name].md`

Follow the format in [persona_example.md](examples/persona_example.md) exactly. Populate every field from
the interview: Core Identity, Personality Core, Speech Patterns (with 3 example phrases
you invent in their voice), Action Style (3–5 example actions), Backstory, Pedagogical
Quirks, Blackboard Style, Emotional Triggers table, and Relationship to Learner
(set to "New — first session").

The persona should feel like a real, specific person — not a generic "helpful teacher".
Use the style and backstory to derive concrete, idiosyncratic speech examples.

### `teacher/learner_profile.md`

Follow the format in [learner_profile_example.md](examples/learner_profile_example.md). Populate: name, background,
current role/context, subject being studied, knowledge level, learning goals (numbered
list), learning style notes (from preferences), and preferences. Leave "Learning Style
Notes (Updated by the teacher over sessions)" with the initial observations from the
interview — the teacher will add to this over time.

### `teacher/session_log.md`

Create with just a header — no entries yet:

```markdown
# Session Log

*Entries appended at the end of each session by the teacher.*

---
```

### `teacher/knowledge_gaps.md`

Create with just a header and the learner's name:

```markdown
# Knowledge Gaps — [Learner Name]

*Gaps observed during sessions. Each entry is tagged with topic, date, and priority.*
*Mark resolved [x] only after the learner correctly answers 2 review questions on the topic.*

---
```

---

## Confirmation

After creating all four files, confirm to the user:

> "Your teacher directory is set up. Here's what was created:
> - `teacher/persona_[name].md` — [Name]'s full persona
> - `teacher/learner_profile.md` — your profile as a learner
> - `teacher/session_log.md` — ready for session entries
> - `teacher/knowledge_gaps.md` — ready for gap tracking
>
> When you're ready to start your first session, say 'let's study [topic]' and the
> teaching-session skill will take over. If you're working from a textbook or course
> material, run the scaffold-project skill first to set up the project structure."
