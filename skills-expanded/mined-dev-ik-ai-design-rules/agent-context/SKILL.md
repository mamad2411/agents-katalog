---
name: agent-context
description: Retrieve concise, graph-backed design context from AI Design Context with the local CLI. Use before implementing or reviewing a user-facing flow, reference fixture, prompt output, or known knowledge object when an agent needs relevant research, rules, patterns, checklists, and evidence limits without reading every index.
---

# Agent Context

Run this skill before a user-facing implementation or review when the applicable knowledge is not already explicit.

## Workflow

1. In a product repository with the npm package installed, verify `npx --no-install ai-design-context context --help`. In the knowledge-source checkout, use `npm run context -- --help`.
2. Resolve the task, review target, or stable object:

   ```bash
   npm run context -- --task quick-capture --platform mobile --intent implement --format json
   npm run context -- --review examples/todo-reference --intent qa
   npm run context -- --object PAT-00002 --format json
   ```

   For the installed npm package, replace `npm run context --` with `npx --no-install ai-design-context context` in these examples. Markdown provides absolute reading paths; JSON adds `absolutePath` while retaining relative graph `path`.

3. Read the selected files before proposing product guidance or code.
4. Apply only the returned rules and patterns that fit the task.
5. Preserve every returned evidence boundary; `draft` and `seed` do not justify broad product claims.
6. If the resolver returns no match, create an observation or research need rather than inventing a rule.
7. Inspect each object's selection reason. Required dependencies are complete, while optional links in broad review gates must be followed explicitly when the review needs them.

## Boundaries

- The CLI is read-only and does not replace `npm run check`.
- `--platform` adds relevant context; it does not prove that a pattern applies.
- Use `--format json` for another agent or script; errors are machine-readable on stderr.
- Task matching is lexical. Simple English task wrappers are supported; arbitrary paraphrases and translation are not. Prefer an exact known slug or ID when available.
