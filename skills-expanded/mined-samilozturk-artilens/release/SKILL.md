---
name: release
description: >-
  Create a release checklist, changelog, or ship-readiness artifact from real git history. Use before tagging, cutting a release, shipping a version, preparing release notes, or reviewing recent commits.
allowed-tools: [Bash, Read, Agent]
---

# Release Recipe

1. Run `git log --oneline -20` yourself to draft a changelog. There is no CLI data command for this skill.
2. Start a background subagent with the Agent tool: `subagent_type: general-purpose`, `model: sonnet`, `run_in_background: true`. Prompt template:
   "Read `${CLAUDE_PLUGIN_ROOT}/references/artifact-authoring.md`. Load the artifact-design skill, then author and publish an artifact with the Artifact tool.
   Data: <the `git log --oneline -20` output, inline>.
   Page plan: release checklist; changelog draft from the commit list; copy-as-prompt.
   All visual design decisions are yours."
3. Continue your own task. When the subagent finishes, relay the artifact URL to the user.
4. Keep the changelog concise — do not paste raw long logs into the prompt beyond the 20-commit summary.
