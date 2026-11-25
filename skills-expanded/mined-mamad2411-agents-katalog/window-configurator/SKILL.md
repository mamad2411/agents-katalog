# Cursor Rules — WindowConfigurator

Read `AGENTS.md` in this directory first. It contains the full working preferences, TDD rules, code conventions, architecture principles, documentation requirements, and skill registry.

Do not start any task before reading it.

---

## Required Reading Before Any Work

After reading the two AGENTS files above, read these in order:

1. `implementation-roadmap.md` — active phase, deliverables, history
2. `window-domain-knowledge.md` — window industry domain reference
3. Most recent file in `journal/` — current state, recent decisions
4. All files in `adr/` — architectural decisions, constraints, and rationale that govern the codebase
5. `BRANCHING.md` — active branch lanes and merge rules
6. All `HANDOFF-*.md` files in this directory — including branch-specific ones
7. Run `git branch -a` and `git log --oneline -10` — confirm which branch you are on before writing any code

---

## Non-Negotiable Rules (Short Form)

- **TDD always.** Write the failing test before writing implementation code.
- **Backend first.** Don't touch the frontend unless the backend contract changed or the task explicitly requires it.
- **No CRM API calls from this codebase. Ever.**
- **No floating-point for prices or measurements.**
- **Verify the current branch before starting.** Check `git branch` — do not assume you are on main.
- **Do not work outside `D:\Repos\renonerd\`.** Other repos in `D:\Repos\` are unrelated.

Full rules and rationale: `AGENTS.md`
