---
name: goal-loop-builder
description: Create copy-ready, verifiable run contracts for long-horizon agent work. Use when the user asks to write, improve, or review Codex `/goal` prompts, Claude Code `/goal` conditions, Claude `/loop` prompts, `.claude/loop.md`, `goal.md`, loop engineering prompts, autonomous run instructions, stop/pause conditions, verification criteria, bounded iteration policy, or persistent Markdown instructions for agents.
---

# Goal Loop Builder

Create a runnable contract for agent loops: a copy-ready command plus a durable Markdown file when useful. For `/goal` work, default to a real Markdown contract file plus a short one-line `/goal` command that references that file. Default to Chinese-first output with an English-compatible mirror unless the user asks otherwise.

## Workflow

1. Classify the request.
   - Use a normal prompt for one-turn answers, small rewrites, or trivial shell output.
   - Use Codex `/goal` or Claude `/goal` when the task has one finish line and should keep advancing until evidence proves completion.
   - Use Claude `/loop` when the task should run on a timer, poll external state, babysit a PR/deploy, or produce recurring reports.
   - Use `.claude/loop.md` when the user wants a default prompt for bare `/loop`; it defines one default prompt, not a task list.
   - Use `goal.md` or `<task-slug>.goal.md` for `/goal` contracts; the Markdown file is the source of truth, and the `/goal` command only points to it.

2. Ask only for high-impact missing details.
   - Ask if runtime choice, target outcome, verification surface, write boundary, production access, credentials, or destructive authority is unclear.
   - Otherwise choose conservative defaults and state them briefly.

3. Build the contract.
   - Outcome: one concrete result, not an activity.
   - Verification: commands, logs, screenshots, API responses, generated files, PR state, or other evidence.
   - Constraints: behavior, public API, data, style, security, and branch rules that must not change.
   - Boundaries: allowed write paths, forbidden paths, tools, environments, and external systems.
   - Iteration policy: small steps, rerun checks, inspect logs before retrying, change evidence source after repeated failure.
   - Stop/Pause: evidence that proves completion; blockers that require a human decision.
   - For `/goal`, write the full contract to a real Markdown file before final output. Use `goal.md` when safe; if it already exists, use `<task-slug>.goal.md`. In projectless workspaces, write to the available output directory or current workspace.
   - Keep the `/goal` command one line and under 350 characters. It should reference the Markdown file with `@/absolute/path/to/file.md`; never paste the full contract into the command.

4. Output in this order.
   - `推荐运行方式`
   - `已生成 Markdown 文件` for `/goal` contracts
   - `可复制 /goal prompt` or `可复制命令`
   - `文件内容摘要` for `/goal` contracts
   - `默认选择理由`
   - `可选调整` only when choices remain useful
   - `English-compatible mirror`

## Reference Routing

- Read `references/runtime-playbook.md` when choosing between Codex `/goal`, Claude `/goal`, Claude `/loop`, `.claude/loop.md`, and `goal.md`.
- Read `references/output-templates.md` when drafting final commands or Markdown artifacts.
- Run `python3 scripts/lint_goal_loop.py <file>` for saved goal or loop artifacts before saying they are ready.

## Quality Bar

Reject or revise output that:

- Leaves placeholders such as `[goal]`, `<path>`, `TODO`, or `待补充`.
- Uses vague verification such as "make sure it works" or "看起来不错就行".
- Allows broad writes like "edit anything" or "随便改".
- Lacks a stop condition, pause condition, write boundary, or verification evidence.
- Puts a full `/goal` contract directly in the command instead of a referenced Markdown file.
- Produces a `/goal` command longer than 350 characters.
- Treats `/loop` as a completion-driven command. `/loop` is timer-driven; `/goal` is completion-driven.
- Treats `.claude/loop.md` as multiple scheduled tasks. It is one default prompt for bare `/loop`.

## Examples

User: "帮我做个 App"

Output: Recommend Codex or Claude `/goal`, create `goal.md` or `app-mvp.goal.md`, and return a short `/goal Read @/absolute/path/to/file.md ...` prompt.

User: "让它每 5 分钟检查部署是否完成"

Output: Recommend Claude `/loop 5m ...`, include observation signals, reporting format, stop/escalation conditions, and optional `.claude/loop.md`.

User: "修复现有仓库的 flaky test"

Output: Recommend `/goal`, create a file-backed goal contract, require discovery of test commands, isolated fix boundaries, regression evidence, and pause on missing repro or environment blockers.
