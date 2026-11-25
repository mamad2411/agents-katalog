---
name: education-category-pointer
description: "Pointer to a library of 5 specialized Education skills. Use when working on education-related tasks."
risk: none
---

# Education Capability Library 🎯

This is a **pointer skill**. The 5 specialized Education skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **examprep-ai** — Exam preparation assistant that converts syllabi, past papers, or notes into a ranked High Score Roadmap. Covers theory, numericals, MCQs, coding, and lab prep, ordered Easy → Medium → Hard. Use for last-minute revision, important topics, and question prediction.
- **learn** — Help a user learn a topic through adaptive tutoring, lesson planning, practice, retrieval checks, explanations, study guides, or exercises. Use when the user asks to learn, understand, practice, drill, review, study, or be tutored on something.
- **lesson-generator** — Build compact, standalone multi-lesson course artifacts with lesson navigation, objectives, flashcards, quizzes, and source links.
- **puzzle-activity-planner** — Plan puzzle-based activities for classrooms, parties, and events with pre-configured generator links
- **teach** — Teach the user a new skill or concept, within this workspace.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `view_file` to read its `SKILL.md` from the vault:
   `<CONFIG_ROOT>/.config/opencode/skill-libraries/education/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `<CONFIG_ROOT>/.config/opencode/skill-libraries/education`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
