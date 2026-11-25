---
name: brainerd-ruminate
description: Mine older repo-scoped session history for repeated corrections, preferences, missed durable knowledge, and recurring failure patterns. Auto-route to Pi, Codex, or Claude based on the active harness.
---

# Brainerd Ruminate

Mine older repo-scoped session history for durable memory gaps and route to the correct harness-specific flow.

## Detect the harness first

1. If the run exposes Brainerd staged-ruminate tools, you are in the Pi branch. Stay inside the Pi tool flow.
2. If `CODEX_THREAD_ID` is present, you are in the Codex branch. Use the Codex wrapper.
3. If `BRAINERD_CLAUDE_SESSION_ID` or `BRAINERD_CLAUDE_TRANSCRIPT_PATH` is present, you are in the Claude branch. Use the Claude wrapper.
4. If none of those signals match, stop and report that harness detection failed. Do not guess.

## Pi branch

1. Read the ambient brain context already injected into the run.
2. Determine whether the run is preview or apply from the hidden Brainerd context.
3. In preview mode, call `brainerd_repo_sessions`, derive findings, and stage them through `brainerd_stage_ruminate`.
4. In apply mode, call `brainerd_get_staged_ruminate` first and apply only that staged proposal through `brainerd_apply_changes`.
5. End with a visible section that starts exactly with `Brainerd summary:`.

## Codex and Claude branches

1. Read `brain/index.md` and `brain/principles.md`.
2. Check for a staged preview with the matching wrapper:

```bash
./scripts/brainerd-codex.sh staged-ruminate
./scripts/brainerd-claude.sh staged-ruminate
```

3. If the user clearly wants to apply or discard that preview, do so through the matching wrapper.
4. Otherwise run the matching repo-sessions command, derive a new preview, and write a small JSON payload to `/tmp/brainerd-ruminate.json`.
5. Stage the preview only through the matching wrapper:

```bash
./scripts/brainerd-codex.sh stage-ruminate --input /tmp/brainerd-ruminate.json
./scripts/brainerd-claude.sh stage-ruminate --input /tmp/brainerd-ruminate.json
```

## Guardrails

- Preview is not permission to write.
- Use only repo-scoped session history.
- Do not dump raw transcript excerpts into the brain.
- If no durable finding exists, say so and stop.
- End with a short summary of what was staged, applied, discarded, or left unchanged.
