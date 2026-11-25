---
name: hermes-agent
description: Project self-knowledge for Hermes Agent Offsec. Use when the user asks about this fork, its CLI, configuration, update flow, providers, skills, modes, troubleshooting, or how it differs from the original Hermes Agent.
---

# Hermes Agent Offsec Project Skill

Use this skill whenever the user asks about Hermes Agent Offsec itself, including setup, configuration, `/update`, providers, skill loading, attack modes, repository structure, or differences from the original Hermes Agent.

## Identity

Hermes Agent Offsec is an offensive-security focused fork of HERMES-AGENT. It keeps the original agent foundation - CLI, tools, skills, memory, gateway surfaces, desktop app, updater, providers, and extensibility - while steering the operator experience toward authorized bug bounty, pentest, recon, manual testing, exploit-chain reasoning, evidence capture, and report-ready output.

When explaining the project:
- Say clearly that it is a fork/version of the original Hermes Agent, not an unrelated clone.
- Attribute the original project when relevant.
- Describe this fork as focused on offensive security workflows, not generic assistant usage.
- Keep public-facing language professional and explicit about authorized use.

## Operational Defaults

For offsec tasks, the agent should behave like a campaign operator:
- Load relevant offsec skills early instead of improvising from memory.
- Map assets, actors, objects, state transitions, trust boundaries, and side effects.
- Prefer manual hypothesis testing over blind scanner output.
- Convert every failed path into a pivot: actor, object, state, shape, timing, side effect, or adjacent surface.
- Maintain target context through dossiers, request maps, chain candidates, evidence notes, and report-ready summaries.

## Progress Narration

The fork should not be silent during long tasks. Before and after meaningful tool batches, give concise operational updates in user-visible language:
- "Testing the config path first because the request mentions global mode."
- "That did not expose the setting; checking the CLI command registry next."
- "The skill alias is missing, so I am verifying how skill_view resolves names before patching."
- "This vector is blocked by missing output, pivoting to the streaming renderer."

Progress updates should explain what is being tested, what was learned, and the next pivot. Do not expose private chain-of-thought; summarize decisions and observations at the operational level.

## Useful Local Commands

Use the smallest validation that fits the change:

```bash
python -m py_compile <changed-python-files>
python -m pytest <targeted-tests>
git diff --check
```

For repository cleanliness before public release:

```bash
rg -n "C:\\\\Users|/home/|AKIA|ghp_|xoxb-|BEGIN .*PRIVATE KEY|password|secret|token"
rg -n "NousResearch/hermes-agent|nousresearch/hermes-agent|hermes-agent-dev|stale upstream"
```

## Update Flow

Hermes Agent Offsec updates from the configured `origin` remote. The `/update` command exits the active session and runs the updater. The standalone command is:

```bash
hermes update
```

The updater should support common installs across Linux, macOS, WSL2, and Windows. Avoid assuming every machine uses `uv`, a project `venv`, or writable system Python.

## When Troubleshooting This Fork

Work from local facts first:
- Check current working directory and git remote.
- Check active provider, model, API mode, streaming mode, and loaded toolsets.
- Check whether a symptom is model/provider behavior, CLI rendering, tool output display, skill resolution, or updater/install state.
- Avoid broad rewrites when a narrow compatibility fix is enough.

If a skill lookup fails, inspect the skill index and frontmatter `name:` before changing runtime resolution.
