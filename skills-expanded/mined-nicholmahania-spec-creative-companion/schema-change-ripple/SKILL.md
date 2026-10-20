---
name: schema-change-ripple
description: Ripple-check habit for any change to a field id, a field's shape (string vs array), the detective brief schema, or the Zustand store shape. Use whenever adding, removing, renaming, or retyping a field — before considering the change done, not as a separate later audit.
---

# Schema-Change Ripple Check

The sharpest recurring bug class in this codebase is a schema change that isn't propagated everywhere the old shape was assumed. A field silently going from string to array, or a const referenced before its own declaration, has shipped to `main` before — once as a real TDZ crash that a passing `npm run build` did not catch (Vite bundling doesn't execute the module graph; only `npm test`'s actual counts did).

Whenever a field id, type, or shape changes:

1. **`grep` the field id across `src/`** before editing anything else. List every hit. A field renamed or retyped without checking every consumer is not done, no matter how clean the one file you meant to change looks.
2. **Check declaration order.** Anything referencing a const/import must be declared after it in the same module — no TDZ. A passing build is not proof of this.
3. **Check every `.trim()` / string-shaped call site** if a field is changing to an array (or vice versa) — these fail loudly (`undefined.trim is not a function`) but only at the moment that code path runs, not at build time.
4. **Check progress/completion counters** (`getDetectiveProgress`, `getRequiredEmpty`, or equivalent) still count the field once, with the right emptiness check for its new type. A field double-counted or dropped shifts every existing project's completion percentage — which reads to the user as their own progress silently regressing.
5. **Check contract tests** (`clientBriefContract.test.js` and siblings) — these encode real constraints (word caps, hidden-field lists). Run them, don't just add the field and assume CI will catch it later in this same session.
6. **Run the full suite and read the actual pass/fail counts**, not just tail output. "1 failed" can mean one assertion or an entire test file that failed to load — the difference matters and is easy to miss by skimming.
