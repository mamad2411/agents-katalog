---
description: Scaffold a tool for the 🔁 Agent Loop demo (the model decides when to call it)
---

Add a new tool the 🔁 Agent Loop can call. Arguments: `$ARGUMENTS` (a tool name and a short description of what it does).

Steps:

1. Open `src/agent-loop/loop-tools.ts`.
2. Add a `defineLoopTool({ ... })` block near the seed tools, following the existing pattern:
   - `name`: snake_case, unique.
   - `description`: write it for the MODEL — say clearly when to call it.
   - `parameters`: a `z.object({...})` with `.describe()` on each field.
   - `kind`: `"data"` (returns JSON) or `"ui"` (returns `{ component, props }`).
   - `execute(args)`: pure, no secrets, no shell, no filesystem.
3. Add it to the exported `loopTools` array (at the `🪁 EXTENSION POINT` marker).
4. If `kind: "ui"`, add a renderer:
   - pick a `component` key (e.g. `"flightCard"`),
   - in `src/agent-loop/loop-component-registry.tsx`, import the component and add it to the `registry` map (also at its `🪁 EXTENSION POINT`).
5. Add a unit test in `src/agent-loop/loop-tools.test.ts` asserting `execute` returns the expected shape.
6. Run `npx vitest run src/agent-loop/` — make sure it passes.
7. Run `npm run dev`, open the 🔁 Agent Loop tab, and confirm the new tool appears in "Available tools" and the model calls it for a fitting prompt.

Keep it the smallest tool that demonstrates the idea. Show the diff and the test result.
