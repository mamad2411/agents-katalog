---
name: compare
description: >-
  Create an option comparison artifact with tradeoffs and a recommendation. Use when the user wants to compare approaches, architectures, libraries, plans, implementation choices, pros/cons, or decision options.
allowed-tools: [Bash, Read, Agent]
---

# Compare Recipe

1. Gather the options and tradeoffs: ask the user or infer the option set and pros/cons from the conversation context. There is no CLI command for this skill.
2. Start a background subagent with the Agent tool: `subagent_type: general-purpose`, `model: sonnet`, `run_in_background: true`. Prompt template:
   "Read `${CLAUDE_PLUGIN_ROOT}/references/artifact-authoring.md`. Load the artifact-design skill, then author and publish an artifact with the Artifact tool.
   Data: <options and tradeoffs gathered above, inline>.
   Page plan: option cards; pro/con lists per option; recommendation highlight; copy-as-prompt for the user's final choice.
   All visual design decisions are yours."
3. Continue your own task. When the subagent finishes, relay the artifact URL to the user.
4. If the user pastes back copy-as-prompt JSON, apply `changes` and republish to the same URL (include the prior artifact URL in the subagent prompt).
