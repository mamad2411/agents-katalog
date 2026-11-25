---
name: ecosystem-compare
description: Compare OMC, OMX, and Copilot CLI concepts without implying parity.
---

# Ecosystem Compare Skill

This is an illustrative skill for the v1 research repo, not runtime parity machinery.

Use this skill when asked to explain how an OMC or OMX workflow maps to Copilot
CLI.

## Active routine

If shell access is available, run:

```bash
./.github/skills/ecosystem-compare/check-parity-claims.sh .
```

If the script reports parity-risk wording, fix the wording before answering.

## Steps

1. Identify the user need behind the OMC/OMX feature.
2. Look for an existing Copilot CLI primitive: instructions, custom agents,
   skills, hooks, MCP, plugins, plan mode, autopilot, review, or delegation.
3. State whether the mapping is direct, partial, or only a design inference.
4. Avoid claiming feature parity unless verified in Copilot CLI.
