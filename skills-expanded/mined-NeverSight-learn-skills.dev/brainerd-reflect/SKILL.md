---
name: brainerd-reflect
description: Persist durable learnings from the current conversation into the repo-local brain. Auto-route to Pi, Codex, or Claude based on the active harness.
---

# Brainerd Reflect

Persist durable repo memory from the current session and route to the correct harness-specific flow.

## Detect the harness first

1. If the run exposes `brainerd_current_session` and `brainerd_apply_changes`, you are in the Pi branch. Stay inside the Pi tool flow.
2. If `CODEX_THREAD_ID` is present, you are in the Codex branch. Use the Codex wrapper.
3. If `BRAINERD_CLAUDE_SESSION_ID` or `BRAINERD_CLAUDE_TRANSCRIPT_PATH` is present, you are in the Claude branch. Use the Claude wrapper.
4. If none of those signals match, stop and report that harness detection failed. Do not guess.

## Pi branch

1. Read the ambient brain context already injected into the run.
2. Open additional `brain/` files only when needed.
3. Call `brainerd_current_session`.
4. Distill the smallest durable change that helps future sessions.
5. Prefer updating an existing principle; otherwise create one focused note.
6. Apply changes only through `brainerd_apply_changes`.
7. End with a visible section that starts exactly with `Brainerd summary:`.

## Codex and Claude branches

1. Read `brain/index.md` and `brain/principles.md`.
2. Run the matching wrapper:

```bash
./scripts/brainerd-codex.sh current-session
./scripts/brainerd-claude.sh current-session
```

3. Distill the smallest durable change that helps future sessions.
4. Prefer updating an existing principle; otherwise create one focused note.
5. Write a small JSON payload to `/tmp/brainerd-reflect.json` with a `changes` array.
6. Apply changes only through the matching wrapper:

```bash
./scripts/brainerd-codex.sh apply-changes --input /tmp/brainerd-reflect.json
./scripts/brainerd-claude.sh apply-changes --input /tmp/brainerd-reflect.json
```

## Guardrails

- Do not store secrets, one-off task state, or generic skill instructions.
- Do not hand-edit generated entrypoints like `brain/index.md` or `brain/principles.md`.
- If nothing durable happened, say so and stop.
- End with a short summary of what changed and why.
