---
inclusion: always
---

# Ponytail — YAGNI Decision Ladder

Before implementing ANY feature, go through this decision ladder (STOP at first that works):

1. **HTML native** — `<input>`, `<dialog>`, `<details>`, `<select>`, `<datalist>`?
2. **CSS only** — visibility, transform, `:has()`, `:is()` selectors?
3. **One function** — < 20 lines using built-in APIs?
4. **Existing library** — already in package.json / requirements.txt?
5. **New library** — small, focused, well-maintained?
6. **Custom solution** — only if ALL above fail.

**NEVER remove**: validation, error handling, security checks, accessibility.
**Goal**: -54% lines of code, -22% tokens, -20% cost.
