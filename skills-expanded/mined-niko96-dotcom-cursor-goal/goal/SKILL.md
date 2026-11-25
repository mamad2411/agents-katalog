---
name: goal
description: Run or manage a Codex-style persistent goal loop in Cursor Agent chat using cursor-goal checkpoint helpers. Use for /goal, /goal pause, /goal resume, /goal clear, /goal edit, durable objectives, verification loops, and evidence-based completion.
disable-model-invocation: true
---

# Goal Skill

Install: `cursor-goal-install-skill --global` after `npm install -g cursor-goal` (see repo `docs/install.md`).

Use this skill when the user invokes `/goal` or asks for a Codex-style persistent goal loop.

**Run the loop in this Cursor chat session.** You are the agent. Do not start a separate agent process or move the loop outside this chat.

Use the local `cursor-goal` CLI only for durable state, verification, and checkpoint accounting.

## Command mapping

- `/goal` → `cursor-goal` (status).
- `/goal <objective>` → set state, then work the goal in this chat.
- `/goal pause` → `cursor-goal pause`.
- `/goal resume` → `cursor-goal resume`, then continue in this chat.
- `/goal clear` → `cursor-goal clear`.
- `/goal edit <objective>` → `cursor-goal edit "<objective>"`, then continue.

When setting a goal from the CLI surface:

```bash
cursor-goal "<objective>" --verify "npm test"
```

If the objective names verification ("verify with …", "verified by …"), pass `--verify`. Otherwise infer a safe command from the repo when obvious (`npm test`, `pnpm test`, `pytest`, etc.).

## Checkpoint loop (each turn)

1. Load active goal with `cursor-goal`. If missing on `/goal <objective>`, set it with `cursor-goal`.
2. If status is not `active`, report status and stop unless the user asked to resume.
3. Optionally run `cursor-goal prompt` when you need the formatted continuation contract.
4. Make **one bounded checkpoint** of concrete progress with normal Cursor tools.
5. End your assistant message with exactly:

```text
GOAL_STATUS: COMPLETE | CONTINUE | BLOCKED
GOAL_REASON: <one short evidence-based sentence>
```

6. Record the checkpoint:

```bash
cursor-goal checkpoint --tool-calls <n>
```

Pipe your final assistant text on stdin when needed:

```bash
cursor-goal checkpoint --tool-calls 3 <<'EOF'
<summary of work>
GOAL_STATUS: CONTINUE
GOAL_REASON: tests still failing on auth module
EOF
```

7. Read the printed status. If still `active`, continue in follow-up turns until `complete`, `blocked`, `budget_limited`, or the user pauses.

Optional: pass `--once` on checkpoint to pause after one checkpoint when still active (useful for single-step handoffs). This does not reduce `maxTurns`.

## Operating contract

For the full continuation contract (same text `cursor-goal prompt` prints), run `cursor-goal prompt` when you need the canonical wording.

- Treat the goal text as both the starting prompt and the completion criteria.
- Prefer small, auditable changes over sweeping rewrites.
- Use repository evidence: files, diffs, tests, command output, artifacts.
- Do not declare complete unless verification passed or you justify why it no longer applies.
- If blocked by missing credentials, destructive ambiguity, or unavailable verification, use `GOAL_STATUS: BLOCKED`.
- Do not pause, resume, clear, or edit unless the user asked for that lifecycle action.
- Default to at most 8 checkpoints unless the user set a different budget in state.
- `--once` on `cursor-goal checkpoint` pauses after that checkpoint if the goal is still `active`; it does **not** change the turn budget.
- `--tier` is recorded for audit only; the model you pick in Cursor chat is what runs.
- Default state is stored outside the workspace for native Codex parity. Use `--state-dir .goal` or `CURSOR_GOAL_STATE_SCOPE=workspace` only when the user explicitly wants legacy workspace-local state.

## Goal quality

A strong goal includes: end state, verification surface, constraints, boundaries, iteration policy, and blocked stop condition.

When the objective is too vague, draft a better goal in one short paragraph, then proceed unless a destructive/ambiguous choice needs user input.

## Safety

- Do not run destructive verification unless the user explicitly requested it and state allows it.
- Do not expose secrets.
- If blocked, stop and report what input is needed.
