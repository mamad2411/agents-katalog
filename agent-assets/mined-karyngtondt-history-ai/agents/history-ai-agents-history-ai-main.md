# AI Agent Instructions

Entry point for AI assistants. Stable implementation rules live in `.ai/system/`.

---

# Before implementing

1. Read `.ai/system/cursor-system-prompt.md`
2. Read `START_HERE.md`
3. Read **`docs/vision/LUMEN_VISION_2030.md`** — constitutional reference
4. Read the current Task in `planning/Shadow/Sprint-XX/TASK-00XX.md`
5. Read `.ai/context/` if relevant to the milestone
6. Read documentation referenced by the Task

---

# Standard Cursor prompt (Shadow sprints)

```text
Read:
.ai/system/cursor-system-prompt.md
docs/vision/LUMEN_VISION_2030.md

Implement:
planning/Shadow/Sprint-XX/TASK-00XX.md
```

---

# After implementing

Archive to `.ai/prompts/` and `.ai/reviews/` (see `planning/WORKFLOW.md`).

---

# Documentation precedence

```text
LUMEN_VISION_2030.md
  ↓
Product Manifesto
  ↓
Engineering Principles
  ↓
Shadow Roadmap / Architecture
  ↓
Task file
  ↓
Code
```

Current focus: **Sprint 68 — Shadow Everywhere Foundation** — see [planning/DELIVERY_ROADMAP.md](planning/DELIVERY_ROADMAP.md)
