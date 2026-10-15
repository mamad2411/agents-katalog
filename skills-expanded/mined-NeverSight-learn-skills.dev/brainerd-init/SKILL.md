---
name: brainerd-init
description: Initialize a repo-local Brainerd brain. Use when setting up Brainerd in the current repo; auto-route to Pi, Codex, or Claude based on the active harness.
---

# Brainerd Init

Initialize Brainerd in the current repo and route to the correct harness-specific setup path.

## Detect the harness first

1. If the active session exposes Pi Brainerd tools, or you are in Pi, use the guarded `/brainerd-init` command surface. Do not use the shell wrappers in that branch.
2. If `CODEX_THREAD_ID` is present, use the Codex wrapper:

```bash
./scripts/brainerd-codex.sh init
```

3. If `BRAINERD_CLAUDE_SESSION_ID` or `BRAINERD_CLAUDE_TRANSCRIPT_PATH` is present, use the Claude wrapper:

```bash
./scripts/brainerd-claude.sh init
```

4. If none of those signals match, stop and report that harness detection failed. Do not guess.

## Workflow

1. Run the matching init path for the detected harness.
2. Review the bootstrap preview before writing it.
3. Apply the optional bootstrap note only when the user explicitly wants it.
4. Keep edits limited to `brain/` and the managed Brainerd block in `AGENTS.md`.
5. On the Claude branch, keep `CLAUDE.md` as a thin shim and preserve Claude imports under `brain/imports/claude/`.

## Guardrails

- Do not edit arbitrary repo files outside `brain/` and the managed Brainerd block in `AGENTS.md`.
- Stop if the managed Brainerd block is duplicated or malformed.
- End with a short summary of what was created and whether bootstrap was previewed or applied.
