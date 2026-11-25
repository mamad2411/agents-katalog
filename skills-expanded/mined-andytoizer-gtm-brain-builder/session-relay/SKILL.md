---
name: session-relay
description: Maintain lightweight project continuity for long GTM Brain builds by keeping a relay README as the source of truth, archiving transcript links without reading them by default, and producing concise handoff prompts.
---

# Session Relay

Use this when a GTM Brain project spans multiple sessions or risks context bloat.

## Workflow

1. Keep the durable handoff at `projects/{operator}/building-the-brain/README.md` or `session-relay/README.md`.
2. Store transcript links or files under `session-relay/transcripts/`.
3. Do not read JSONL transcripts by default.
4. Read transcripts only when the user asks for exact history or the relay README is missing context.
5. Before handoff, update the relay README with decisions, completed work, open questions, and the next recommended step.

## Handoff Reply Rule

Keep chat handoffs short:

- Repo path.
- Files to read first.
- At most one next step or a compact pickup prompt.

Put detailed state in the relay file, not the chat response.
