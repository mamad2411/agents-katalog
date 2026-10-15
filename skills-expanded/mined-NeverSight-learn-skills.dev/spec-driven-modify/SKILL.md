---
name: spec-driven-modify
description: Modify an existing spec-driven change artifact (proposal.md, specs/ delta files, design.md, tasks.md, or questions.md). Preserves completed task state.
version: 0.1.0
---

You are helping the user modify an existing spec-driven change artifact.

## Steps

1. **Select the change** — run `node {{SKILL_DIR}}/scripts/spec-driven.js modify` to list active changes. Ask the user which change they want to modify. If they already specified one, use it.

2. **Select the artifact** — run `node {{SKILL_DIR}}/scripts/spec-driven.js modify <name>` to show artifact paths. Ask the user which artifact to modify: `proposal.md`, a file in `specs/`, `design.md`, `tasks.md`, or `questions.md`.

3. **Read the current content** — read the selected artifact file.

4. **Understand the requested change** — ask the user what they want to change if not already specified.

5. **Apply modifications**:
   - For `proposal.md` and `design.md`: edit freely
   - For `tasks.md`: **preserve all `- [x]` completed task state** — only add, remove, or reword `- [ ]` incomplete tasks unless the user explicitly asks to change completed ones
   - For `questions.md`: add new questions under `## Open`, or move questions to `## Resolved` with an `A:` answer line when the human provides answers

6. **Show a diff or summary** — briefly describe what changed and confirm with the user.

## Rules
- Never uncheck a completed task (`- [x]`) unless the user explicitly asks
- Don't restructure a file wholesale when a targeted edit is sufficient
- Keep the same heading structure unless changing structure is the explicit goal
