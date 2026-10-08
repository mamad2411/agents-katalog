---
name: understand-anything
description: LeeWay-governed binding to Egonex-AI Understand Anything for turning a codebase, knowledge base, or documentation set into an explorable knowledge graph and guided understanding workflow.
license: Upstream license applies
metadata:
  authority: LeeWay Standards
  source: Egonex-AI/Understand-Anything
  canonical-skill: understand-anything-plugin/skills/understand/SKILL.md
  mode: syncable-remote-canonical
---

# Understand Anything — LeeWay Binding

Canonical package: `Egonex-AI/Understand-Anything` → `understand-anything-plugin/` on `main`.
Canonical skill entry: `understand-anything-plugin/skills/understand/SKILL.md`.

Use synchronized `upstream/skills/understand/SKILL.md` plus only the plugin agents/scripts it requires. If upstream is absent, fetch the canonical files through authorized GitHub/network access.

## Route here when

- onboarding to a large or unfamiliar codebase;
- the user wants an interactive knowledge graph or visual architecture explorer;
- the task requires guided multi-agent analysis of files, functions, classes, dependencies, or documentation;
- a project should become easier to search and explain rather than repeatedly reread raw files.

Graph output is evidence, not authority. Keep extracted facts separate from inferred relationships. Do not claim the graph/dashboard exists until its plugin/runtime actually ran and generated artifacts.

State while `upstream/` is absent: `REMOTE_CANONICAL`.
