---
name: capture-transcript
description: Use when the user asks to save, upload, capture, or persist the current Claude Code or Codex session transcript (conversation log) to Artifacta. Verifies and snapshots the live transcript, then stores it through the supported Artifacta connection; Codex also supports one-shot next-Stop capture with an explicit --automatic flag.
---

# Capture a supported agent transcript

Store the current conversation log in Artifacta. This skill is only for the
session transcript; use `persisting-outputs` for reports, datasets, generated
files, or other run outputs.

## Select the provider workflow

Determine the current host from the active runtime and session context:

- In Claude Code, read
  [references/claude-code.md](references/claude-code.md) completely and follow
  it.
- In Codex, read [references/codex.md](references/codex.md) completely and
  follow it.
- If the host cannot be identified, stop and ask the user which supported host
  is running. Never guess a transcript format or location.

## Shared safety rules

- Verify, never guess. Recency alone does not identify the current transcript.
- Never push an unverified file.
- Copy the actively written transcript and upload only the private snapshot.
- No redaction on push: Artifacta does not automatically scan or remove
  credentials or other secrets from transcript bytes.
- Never print transcript bytes, base64 content, credentials, or environment
  dumps in diagnostics or the final response.
- Report the artifact ID, filename, decoded size, capture kind, and the
  retrieval method used by the selected provider workflow.
- Model metadata is a captured producer claim, not a cryptographic attestation.
  Describe `models_used` as models observed, not an exhaustive list.
