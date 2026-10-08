---
name: fresh-eyes-loop
description: Implement a task through an automatic implement → fresh-eyes review → fix loop where the implementer/fixer runs on Opus 4.8 1M Max and every review runs as a fresh GPT 5.5 1M Extra High subagent. Two inline hooks (stop, subagentStop) keep the loop alive and capture each verdict verbatim. Use when the user asks for a fresh-eyes loop, review loop, auto-reviewed implementation, or to iterate until a reviewer approves. Requires the bundled hooks and the fresh-eyes-reviewer subagent to be installed (see README.md next to this skill). Arm the loop by creating .fresh-eyes/, implement, then follow PROTOCOL.md until approval or budget exhaustion.
disable-model-invocation: true
---

# Fresh-Eyes Loop (Cursor)

You are the **implementer and fixer** — keep doing that on **Opus 4.8 1M Max**. Each review runs as a **fresh `fresh-eyes-reviewer` subagent on GPT 5.5 1M Extra High**, so nobody approves their own context and the deciding judgment comes from a different model. The loop's state machine lives in `PROTOCOL.md`; your job here is to arm it correctly, implement, and then follow the protocol.

## Model split (the point of this variant)

- **Implement & fix** → **Opus 4.8 1M Max** (`claude-opus-4-8-thinking-max`). Run the loop in that session; if you're on another model, switch before arming.
- **Review** → the `fresh-eyes-reviewer` subagent, pinned to **GPT 5.5 1M Extra High** (`gpt-5.5-extra-high`) in its frontmatter.

You do not pick the reviewer's model per round — it is pinned in the subagent definition. Just keep the session on Opus 4.8 1M Max and let every review go to GPT 5.5 1M Extra High. (The 1M context comes from Max Mode; if a model isn't available on your plan, Cursor falls back to a compatible one.)

## 1. Arm the loop (before touching any code)

From the repo root (resolve `<skill_dir>` to the directory containing this SKILL.md):

```bash
mkdir -p .fresh-eyes
cp "<skill_dir>/assets/PROTOCOL.md" "<skill_dir>/assets/reviewer-instructions.md" "<skill_dir>/assets/continue.json" .fresh-eyes/
echo ".fresh-eyes/" >> .git/info/exclude
touch .fresh-eyes/active
```

Then create two files:

- `.fresh-eyes/task.md` — exactly:

  ```
  ## Task

  <the user's task, verbatim>
  ```

- `.fresh-eyes/state.md` — exactly (use the user's budgets if they gave any; defaults shown):

  ```
  outer=1
  inner=0
  max_outer=10
  max_inner=10
  next=review
  ```

Leave `.fresh-eyes/history.md` uncreated; it fills in automatically. If the skill assets, the hooks, or the `fresh-eyes-reviewer` subagent are missing, stop and tell the user to install them per the README — do not improvise a loop yourself.

## 2. Implement the task

Implement the task completely on Opus 4.8 1M Max, then **end your turn**. Do not review your own diff and do not spawn any subagents on your own initiative. While `.fresh-eyes/active` exists, ending a completed turn automatically continues the loop (the `stop` hook submits the next step).

## 3. Follow the protocol

Every continuation tells you to read `.fresh-eyes/PROTOCOL.md` and perform exactly the next step (`state.md` says which). Review steps spawn the `fresh-eyes-reviewer` (GPT 5.5 1M Extra High); fix steps happen on Opus 4.8 1M Max. Continue until the protocol declares the run finished — approved, or budgets exhausted — then delete `.fresh-eyes/active`, write the final report the protocol prescribes (outcome, what was achieved, next steps), and stop.

## Operator notes (if the user asks)

- Progress: `cat .fresh-eyes/state.md` and `.fresh-eyes/history.md`.
- Cancel: `rm .fresh-eyes/active` (only on explicit user request). Aborting a turn (Esc) also pauses the loop — the `stop` hook continues only after a *completed* turn, never after an abort or error.
- Cleanup after a finished run: `rm -rf .fresh-eyes` (it is git-excluded, never part of the diff).
