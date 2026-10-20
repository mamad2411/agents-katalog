---
description: Scaffold a host tool the agent can call, following the l4-tools.ts defineTool pattern
argument-hint: <tool-name> <what the tool does>
allowed-tools: Read, Edit, Write, Bash
---
Arguments: `$ARGUMENTS`
Treat the **first token** as the tool name and **the rest** as what it does. If no
arguments were given, ask me for them.

Add a new server-side tool the agent can call, following the existing pattern exactly.

Steps:
1. Read `src/lessons/l4-tools.ts` (the `defineTool({ name, description, parameters, execute })`
   pattern; note it uses relative imports and `execute` returns a plain object) and
   `server.ts` (how tools are passed to `makeAgentWithTools`).
2. Add a `defineTool(...)` export to `src/lessons/l4-tools.ts`: a zod `parameters`
   schema and an `execute` that returns a plain JSON-serializable object (data, or
   `{ a2ui_operations: [...] }` for an A2UI surface).
3. In `server.ts`, import the new tool and add it to the `l4` agent's tool array in
   `makeAgentWithTools(...)`, and add a one-line hint to that agent's prompt so the
   model knows when to call it.
4. Run `npm run typecheck` and `npx vitest run`; fix anything red.
5. Summarize what you added and a chat prompt I can use to trigger it (on the L4 tab).

Do not add new dependencies. Do not commit unless I ask.
