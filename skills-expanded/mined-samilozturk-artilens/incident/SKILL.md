---
name: incident
description: >-
  Create an incident, regression, bug investigation, or debugging artifact with timeline, metrics, and hypothesis table. Use for outages, postmortems, root-cause analysis, production issues, flaky failures, or debugging narratives.
allowed-tools: [Bash, Read, Agent]
---

# Incident Recipe

1. Gather the incident data: timeline events, hypotheses (with status), and metric summaries from the conversation context or the user directly. There is no CLI command for this skill.
2. Start a background subagent with the Agent tool: `subagent_type: general-purpose`, `model: sonnet`, `run_in_background: true`. Prompt template:
   "Read `${CLAUDE_PLUGIN_ROOT}/references/artifact-authoring.md`. Load the artifact-design skill, then author and publish an artifact with the Artifact tool.
   Data: <timeline, hypotheses, metrics gathered above, inline>.
   Page plan: timeline; hypothesis table with a status column; metric summaries; copy-as-prompt.
   All visual design decisions are yours."
3. Continue your own task. When the subagent finishes, relay the artifact URL to the user.
4. For long-running investigations, re-gather updated data and republish to the same URL as new evidence arrives.
