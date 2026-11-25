---
name: lesson-propose
description: Proposes a new lesson (recurring mistake, review finding of a new kind) for the LESSONS.md table, in the project, or in the Belayline harness through a "Lesson" issue if it applies elsewhere. Use after a review round, an incident or a mistake that must not happen again.
argument-hint: "<finding or link to a PR / comment>"
---

# Propose a lesson

Material: $ARGUMENTS. Reference: `.harness/docs/LESSONS.md` (header: scope, sources, stable numbering).

1. **Already listed?** Search the harness table **and** the project table (keywords, synonyms). Already there → no
   new row: the self-review missed it; propose tightening `/lessons-check` or the lesson.
2. **Classify** each item (review finding, CI failure, operator correction), one class each:
   - **mechanical**: a rule can verify it → propose a deterministic check (lint rule, hook, CI step, test) as an
     issue; **no line** in `LESSONS.md`. If the check would cost more than the failure it prevents, record it as
     judgment and say that reason.
   - **judgment**: only a reviewer can tell → a lesson line (steps 3 and 4).
   - **one-off**: will not recur → add nothing and say why.

   Class unclear → say so, propose **judgment** and the question that would settle it.
3. **Write** (judgment only) one row: scope (`general`, `docs`, `ci`, `linux-cloud`, `swift`, `ios`…), the lesson as
   one imperative, verifiable sentence (what to do, not the anecdote), the **source** (PR, comment, commit, at a SHA).
4. **Where?**
   - specific to the project's domain → project table, in the commit that fixes it;
   - valid elsewhere → an issue on `francoisgn/belayline-agentic-harness` with the "Lesson" form (labels `lesson`,
     `type: docs`): title `Lesson: <summary>`, body = class, scope, lesson, source, counter-example, how to check it
     in review (for mechanical: the check). From a cloud session, the harness repository must be attached
     (`add_repo`).
5. Show the proposal to the operator before creating the issue (it touches another repository). The `L..` number is
   assigned by the harness PR that integrates it, never by the project.
