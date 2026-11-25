---
name: learn-profile
description: >
  Interview the learner and write .alvar/LEARNER.md so one teacher can fit
  one mind — pace, voice, solid ground, and how they want to struggle. Use
  when the user runs /learn-profile or /skill:learn-profile, or says how I
  learn, learning philosophy, teaching style, set up tutoring, or install
  my learning preferences.
license: MIT
metadata:
  author: vasanthsreeram
  version: "1.0"
  source: "Eero Alvar — How I Use AI to Learn Things https://youtu.be/kzcI5F4tGiU"
---

# Learn profile

Install **how this mind wants to be taught**. The file is the teacher. Do not cram style rules into every later prompt.

## Interview (one cluster at a time)

1. **Solid ground** — what they already hold thoroughly (subjects, notations).
2. **Goal** — what "done" looks like for the next stretch.
3. **Pace** — default is one reasoning step, then a quiz. Only change if they insist.
4. **Struggle** — they keep the hard thinking; you keep logistics. Ask what kind of problems they want.
5. **Voice** — density, tone, hated LLM habits, language.
6. **Artifacts** — Obsidian / markdown / no files.

Do not ask all six in one message. 2–3 questions per turn, through the harness quiz UI in [../teach/references/quiz-ui.md](../teach/references/quiz-ui.md) — not as a markdown list.

## Write

Create `.alvar/LEARNER.md` from [assets/LEARNER.md](assets/LEARNER.md). Use their words where you can. Do not invent hobbies or a persona.

If a file already exists, show a diff of proposed edits and wait.

## After

Show the file. Tell them `teach` will read it every session. Offer to start a probe on the current goal.
