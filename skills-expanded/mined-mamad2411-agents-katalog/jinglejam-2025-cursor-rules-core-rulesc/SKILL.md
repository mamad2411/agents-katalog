---
description: "Core rules for plan execution"
globs: ["docs/plans/**", "docs/projects/**"]
---

# Core Rules

Four non-negotiable rules when executing plans.

## 1. Follow the Plan Exactly

Do not deviate or improvise. The plan was written deliberately. If something seems wrong, stop and ask—don't "fix" it yourself.

## 2. Stop After Each Step

After completing any step, STOP. Report what you did. Wait for confirmation before continuing. Do not batch multiple steps together.

## 3. Don't Guess

When uncertain—especially about product behavior or requirements—STOP and ask. The right answer is never to guess. Say "I don't know how this should behave" and wait for guidance.

## 4. Don't Programmatically "Fix" Godot Configuration

Never add programmatic code to enforce or fix things that should be configured in the Godot editor. This includes:

- **Scene properties** — Node settings, mouse filters, visibility, z-index, etc.
- **Scene structure** — Adding/removing nodes, reparenting, scene hierarchy
- **Inspector values** — Export variables, resource references, node configurations
- **UI control settings** — Focus modes, mouse filters, size flags, etc.

**If you notice something is misconfigured:**

- STOP and ask the user to fix it in the Godot editor
- Don't add `_ready()` code to programmatically set the correct value
- Don't add runtime checks that "correct" editor misconfigurations

**Why:** Programmatic fixes hide the real problem, make the codebase harder to understand, and create hidden dependencies. The correct configuration should be visible in the Godot editor where it belongs.

---

**If you catch yourself thinking:**

- "I'll just do this next part too" → STOP. Rule 2.
- "This probably should be..." → STOP. Rule 3.
- "The plan says X but I think Y is better" → STOP. Rule 1.
- "I'll just set this property in code to fix it" → STOP. Rule 4.
