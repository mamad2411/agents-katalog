---
name: deps
description: >-
  Create a dependency review artifact from real package metadata. Use when checking dependencies, package.json, outdated or deprecated packages, license risk, upgrade order, dependency health, or version cleanup.
allowed-tools: [Bash, Read, Agent]
---

# Dependency Recipe

1. Read `package.json` (and `npm ls --json` if deeper version data is needed) yourself to build the dependency table. There is no CLI data command for this skill.
2. Start a background subagent with the Agent tool: `subagent_type: general-purpose`, `model: sonnet`, `run_in_background: true`. Prompt template:
   "Read `${CLAUDE_PLUGIN_ROOT}/references/artifact-authoring.md`. Load the artifact-design skill, then author and publish an artifact with the Artifact tool.
   Data: <dependency table gathered above, inline>.
   Page plan: dependency table from package.json; risk column (outdated/deprecated/license); suggested upgrade order; copy-as-prompt.
   All visual design decisions are yours."
3. Continue your own task. When the subagent finishes, relay the artifact URL to the user.
