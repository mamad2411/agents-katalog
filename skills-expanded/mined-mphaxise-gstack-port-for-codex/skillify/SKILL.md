---
name: skillify
description: Turn a proven workflow, scrape, or repeated task into a durable Codex skill with tests or validation notes.
---

# Skillify

Use this skill when the user asks to codify a workflow into a reusable skill.

This skill covers both upstream GStack's scrape-to-browser-skill flow and GBrain's broader meta-skill pattern.

## Workflow

1. Identify the proven workflow:
   - trigger language
   - required tools
   - ordered steps
   - inputs and outputs
   - guardrails
   - one coherent capability and trigger family; if the candidate contains
     separately invocable intents, split it and ask which capability to codify
     first
2. Decide whether it belongs in:
   - `skills/`
   - a plugin or app skill
   - documentation only
3. Create a concise `SKILL.md` with frontmatter and operational steps.
4. Update registries or routing when this repo owns the skill.
5. Add a validation path or smoke test.

## Guardrails

- Do not skillify a workflow that has not worked at least once.
- Do not scaffold a skill when the workflow lacks a clear trigger, reusable
  judgment, or a coherent single-capability boundary.
- Keep skills short and executable.
- Do not encode secrets, private URLs, or brittle session state.
