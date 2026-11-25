---
name: brainstorming
description: "Turning a rough idea into a structured design/brainstorm document before planning. Apply when the user is shaping a new feature or project and has no design doc yet."
---

# Brainstorming Ideas Into Designs

> Adapted from [obra/superpowers](https://github.com/obra/superpowers)

## Overview

Help turn ideas into fully formed designs and specs through natural collaborative dialogue.

Start by understanding the current project context, then ask questions one at a time to refine the idea. Once you understand what you're building, present the design in small sections (200-300 words), checking after each section whether it looks right so far.

## The Process

**Understanding the context:**

- Read CLAUDE.md (project-level, then global) to identify the stack(s) in use
- If stack skills are referenced (e.g., `django-patterns.md`, `nextjs-patterns.md`, `flutter-patterns.md`), read them to understand tech constraints and conventions
- Review any existing project files, docs, or recent commits
- Treat the stack as a given — don't ask which framework or language to use when CLAUDE.md already specifies it

**Refining the idea:**

- Ask questions one at a time to refine the idea
- Prefer multiple choice questions when possible, but open-ended is fine too
- Only one question per message — if a topic needs more exploration, break it into multiple questions
- Focus on understanding: purpose, constraints, success criteria

**Exploring approaches:**

- Propose 2-3 different approaches with trade-offs
- Present options conversationally with your recommendation and reasoning
- Lead with your recommended option and explain why

**Presenting the design:**

- Once you believe you understand what you're building, present the design
- Break it into sections of 200-300 words
- Ask after each section whether it looks right so far
- Cover: architecture, components, data flow, error handling, testing
- Be ready to go back and clarify if something doesn't make sense

## After the Design

**Documentation:**

- Write the validated design to `docs/plans/YYYY-MM-DD-<topic>-brainstorm.md`
- If in a git repo, commit the design document

**Next step:**

After committing the design doc, suggest:

> "Design is saved. Next steps depend on what you're building:
> - **Product/UX-heavy feature:** Run `/prd` to formalize requirements, then `/ux-spec` for UX foundations before planning.
> - **Technical/backend feature:** Start a new session with the planner agent to break this into implementation phases."

## Key Principles

- **One question at a time** — Don't overwhelm with multiple questions
- **Multiple choice preferred** — Easier to answer than open-ended when possible
- **YAGNI ruthlessly** — Remove unnecessary features from all designs
- **Explore alternatives** — Always propose 2-3 approaches before settling
- **Incremental validation** — Present design in sections, validate each
- **Be flexible** — Go back and clarify when something doesn't make sense
