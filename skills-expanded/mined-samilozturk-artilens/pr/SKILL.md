---
name: pr
description: >-
  Build an annotated pull-request or branch walkthrough artifact from real git data. Use before review, when explaining a branch, preparing a PR, summarizing commits, or showing changed files and risks.
allowed-tools: [Bash, Read, Agent]
---

# PR Walkthrough

1. Run `node "${CLAUDE_PLUGIN_ROOT}/scripts/run-artilens.mjs" git pr --base <branch> --data .claude/artilens/pr.data.json`.
2. Relay the CLI's summary line to the user verbatim.
3. Start a background subagent with the Agent tool: `subagent_type: general-purpose`, `model: sonnet`, `run_in_background: true`. Prompt template:
   "Read `<absolute path to pr.data.json>` and `${CLAUDE_PLUGIN_ROOT}/references/artifact-authoring.md`. Load the artifact-design skill, then author and publish an artifact with the Artifact tool.
   Page plan: branch summary; commit list; file-by-file narrated walkthrough using the JSON's truncated hunks; risky areas; copy-as-prompt.
   All visual design decisions are yours."
4. Continue your own task. When the subagent finishes, relay the artifact URL to the user.
5. If the user pastes back copy-as-prompt JSON, apply `changes` and republish to the same URL (include the prior artifact URL in the subagent prompt).

Do not dump the full diff into the model context.
