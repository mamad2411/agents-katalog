---
name: package-authoring
description: >
  Use this skill whenever adding, revising, or publishing an AI Workflow Kits
  package, including Codex skills, Claude agents, Gemini prompts, Copilot
  instructions, hooks, commands, plugins, examples, manifests, and registry
  entries. This skill keeps contributions organized by workflow package first,
  runtime second, and artifact type third, and it requires the public safety
  scan before publishing.
---

# package-authoring

Use this skill before adding or changing anything intended for publication in AI Workflow Kits.

## Core Rule

Organize by workflow first, runtime second, artifact type third.

```text
packages/<package-id>/
├─ README.md
├─ manifest.yaml
├─ codex/
├─ claude/
├─ gemini/
├─ copilot/
├─ plugins/
└─ examples/
```

Do not create top-level `skills/`, `agents/`, or `plugins/` folders for one artifact type.

## Placement

| Artifact | Location |
| --- | --- |
| Codex skill | `packages/<package-id>/codex/skills/<skill-id>/SKILL.md` |
| Codex instructions | `packages/<package-id>/codex/AGENTS.md` |
| Claude Code agent | `packages/<package-id>/claude/agents/*.agent.md` |
| Claude Code hook | `packages/<package-id>/claude/hooks/` |
| Claude command | `packages/<package-id>/claude/commands/` |
| Gemini prompt | `packages/<package-id>/gemini/prompts/` |
| Gemini instructions | `packages/<package-id>/gemini/GEMINI.md` |
| Copilot instructions | `packages/<package-id>/copilot/github/copilot-instructions.md` |
| Copilot prompt | `packages/<package-id>/copilot/github/prompts/` |
| Optional plugin | `packages/<package-id>/plugins/<plugin-id>/` |
| Example workflow | `packages/<package-id>/examples/<example-id>/` |

## Workflow

1. Identify the workflow package.
2. If it is new, create it from `templates/package-template/`.
3. Add runtime-native files under the matching runtime folder.
4. Update package `manifest.yaml`.
5. Update root `REGISTRY.md`.
6. Update root `registry.yaml`.
7. Add or update a public-safe example.
8. Run `python tools/public-safety-scan.py --history`.
9. Commit only after the scan passes.

## Public Safety

Before publishing, verify that the package does not expose private workspace details, internal project labels, local paths, generated logs, local audit trails, large generated artifacts, or credential-like values.

Use `docs/publication-guard.md` as the detailed rule source.

## Output

When reporting completion, include:

- package path
- runtime folders changed
- registry files updated
- examples added or updated
- public safety scan result
