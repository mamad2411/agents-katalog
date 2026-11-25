---
name: ponytail-yagni
description: "Ponytail YAGNI (You Aren't Gonna Need It) Decision Ladder. Forces radical architectural simplicity: native HTML/CSS/standard library first, minimal code, zero over-engineering, without compromising security, validation, error handling, or accessibility."
---

# Ponytail YAGNI — The Anti-Overengineering Decision Ladder

Always follow this decision ladder before writing, refactoring, or architecting any piece of software. Always prefer the lowest step that satisfies the requirements.

## The 6-Step Decision Ladder

```
[Level 1: Native HTML] (<input>, <dialog>, <details>, <select>, <form>)
        ↓ (fails?)
[Level 2: Pure CSS]    (visibility, transform, :has(), flex, grid, media queries)
        ↓ (fails?)
[Level 3: One Function] (<20 lines, built-in standard APIs, zero dependencies)
        ↓ (fails?)
[Level 4: Existing Lib] (already in package.json / requirements.txt)
        ↓ (fails?)
[Level 5: New Library]  (small, single-purpose, battle-tested, zero transitive bloat)
        ↓ (fails?)
[Level 6: Custom Code]  (only if all 5 levels above genuinely cannot solve it)
```

## Non-Negotiable Core Invariants
Regardless of how simple the solution is, **NEVER REMOVE OR COMPROMISE**:
1. **Validation:** Validate all input boundaries (client & server).
2. **Error Handling:** Graceful failures with actionable error messages.
3. **Security:** Sanitization, auth checks, parameterization, zero secret leakage.
4. **Accessibility (a11y):** Keyboard navigation, semantic ARIA roles, focus management.

## Heuristics for AI Agents
- Do NOT install state management libraries (Redux, MobX) for 2 simple UI toggles.
- Do NOT write custom modal backdrops when `<dialog>` natively handles `showModal()`, backdrop, and Esc-key closing.
- Do NOT build an accordion component in 100 lines of JavaScript when `<details><summary>` does it natively with zero JS.
- Do NOT create microservice abstractions or 5-layer inheritance hierarchies for simple CRUD endpoints.
