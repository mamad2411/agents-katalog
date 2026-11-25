---
name: grimoire-refine
description: Discuss with the user to update project knowledge and refine requirements.
disable-model-invocation: true
---

# Purpose

Discuss with the user to update project knowledge and refine requirements.

# Workflow

## 1. Load

Read the two skill files:

- `skills/grimoire-clarify/SKILL.md`
- `skills/grimoire-record/SKILL.md`

Completion: Both files are read into context. Their rules are active.

## 2. Discuss

Start discussing with the user. Follow grimoire-clarify's loop.

While discussing, follow grimoire-record's trigger detection. Do not wait until all questions are answered.

Completion: User confirms discussion is complete. Frontier is empty. Every qualifying item is recorded.

---

## 3. Recommend approach

Assess the refined requirements against these signals:

| Signal     | Spec-first                   | Plan-first             |
| ---------- | ---------------------------- | ---------------------- |
| Domains    | Multiple domains or systems  | Single domain          |
| Ambiguity  | Unresolved unknowns remain   | Well-understood        |
| Components | Multiple interacting parts   | Few isolated changes   |
| Decisions  | Many open design choices     | Decisions are obvious  |
| Slicing    | Likely needs vertical slices | Fits one batch of work |

- **Spec-first**: `grimoire-spec` → `grimoire-slice` → `grimoire-plan` → `grimoire-implement`
- **Plan-first**: `grimoire-plan` → `grimoire-implement`

State the recommendation with at least one concrete reason tied to the discussion.

Completion: User receives a recommendation with reasoning grounded in the discussion.

---

# Rules

- Load both skills before starting the discussion.
- Record as you go. Never defer documentation to a separate pass.
- Never execute the user's objective. Discussion and documentation only.
- Never ask the user for verifiable facts (sub-agents handle that).
- Always give a development approach recommendation before exiting.
