---
name: git
description: >-
  Visualize real git status, changed files, a commit, or a remote diff as an artifact. Use when the user asks what changed, wants a repo/change overview, needs git status explained, or asks to inspect a commit or diff.
allowed-tools: [Bash, Read, Agent]
---

# Git Views

1. Run the deterministic view matching what the user asked for:
   - Working tree: `node "${CLAUDE_PLUGIN_ROOT}/scripts/run-artilens.mjs" git status --data .claude/artilens/git-status.data.json`
   - Commit: `node "${CLAUDE_PLUGIN_ROOT}/scripts/run-artilens.mjs" git commit <ref> --data .claude/artilens/git-commit.data.json`
   - Remote diff: `node "${CLAUDE_PLUGIN_ROOT}/scripts/run-artilens.mjs" git remote-diff --base <base> --data .claude/artilens/remote-diff.data.json`
2. Relay the CLI's summary line to the user verbatim.
3. Start a background subagent with the Agent tool: `subagent_type: general-purpose`, `model: sonnet`, `run_in_background: true`. Prompt template:
   "Read `<absolute path to the data JSON>` and `${CLAUDE_PLUGIN_ROOT}/references/artifact-authoring.md`. Load the artifact-design skill, then author and publish an artifact with the Artifact tool.
   Page plan: summary line up top; changed-files table (status, +/-); notable risk points; copy-as-prompt.
   All visual design decisions are yours."
4. Continue your own task. When the subagent finishes, relay the artifact URL to the user.
5. If the user pastes back copy-as-prompt JSON, apply `changes` and republish to the same URL (include the prior artifact URL in the subagent prompt).
