---
name: artifacts
description: >-
  List, find, inspect, diff, resume, or update this project's locally registered artifacts. Use when the user references a previous artifact, asks what artifacts exist, wants artifact history, or wants to continue from an artifact.
allowed-tools: [Bash, Read, Artifact]
---

# Artifact Registry

Use the local ArtiLens registry before reading individual artifact snapshots.

Steps:

1. Run `node "${CLAUDE_PLUGIN_ROOT}/scripts/run-artilens.mjs" artifacts list`.
2. Read `.claude/artifacts/index.md` for low-token discovery.
3. If the user wants details, run `node "${CLAUDE_PLUGIN_ROOT}/scripts/run-artilens.mjs" artifacts show <slug>`.
4. If the user wants a version comparison, run `node "${CLAUDE_PLUGIN_ROOT}/scripts/run-artilens.mjs" artifacts diff <slug> <vA> <vB> --as-artifact --out .claude/artilens/<slug>-diff.html`.
5. For updates, include the stored artifact URL in the publish prompt so Claude Code updates the same artifact.

The PostToolUse hook records new versions after publish.
