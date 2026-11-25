---
name: code-agnostic
description: Work on code-agnostic, the CLI that centralizes MCP servers, rules, skills, agents, and workspace config, then compiles and syncs them into Codex, Cursor, and OpenCode. Use when editing this repo, explaining how code-agnostic works, or changing its config compiler, import, plan, apply, status, workspace, rule, skill, agent, or MCP behavior.
---

# Code Agnostic

`code-agnostic` is a config compiler for AI coding tools. It keeps one source of truth in `~/.config/code-agnostic/` and syncs MCP servers, rules, skills, agents, and workspace instructions into each app's native layout for Codex, Cursor, and OpenCode.

Do not treat it as an AI agent, prompt runner, editor plugin, or MCP server. It is the tool that manages and compiles config for those things.

## Mental Model

- Source config lives under `~/.config/code-agnostic/`.
- Target app files under `~/.codex/`, `~/.cursor/`, and `~/.config/opencode/` are generated or managed outputs.
- To change app config, edit the code-agnostic source of truth, run `code-agnostic plan`, then run `code-agnostic apply`.
- Do not manually update generated target app directories when the same change can be represented in code-agnostic source.
- The CLI workflow is `plan` first, then `apply`.
- `status` checks drift between source and targets.
- `import plan` and `import apply` migrate existing app config into the central source.
- `validate` checks canonical source files.
- `explain-lossiness` reports fields a target app cannot preserve.

## Main Commands

```bash
code-agnostic plan
code-agnostic apply
code-agnostic status
code-agnostic validate
code-agnostic explain-lossiness
```

Use `-a codex`, `-a cursor`, or `-a opencode` when a change is target-specific.

```bash
code-agnostic import plan -a codex
code-agnostic import apply -a codex
code-agnostic apps enable -a cursor
code-agnostic workspaces add --name myproject --path ~/code/myproject
```

## Installing This Skill

Preferred: place this directory at `~/.config/code-agnostic/skills/code-agnostic/`, then run `code-agnostic plan` and `code-agnostic apply` so supported apps receive their generated copies.

Direct app install is also valid when needed, for example `~/.codex/skills/code-agnostic/SKILL.md`.

## Source Formats

Prefer canonical bundle directories for new rules, skills, and agents:

```text
rules/<name>/meta.yaml
rules/<name>/prompt.md
skills/<name>/meta.yaml
skills/<name>/prompt.md
agents/<name>/meta.yaml
agents/<name>/prompt.md
```

`meta.yaml` is schema-validated metadata. `prompt.md` is instruction text only. App-specific fields belong under `x-codex`, `x-cursor`, or `x-opencode`; unknown top-level keys should fail validation.

Legacy single-file rules, `skills/<name>/SKILL.md`, and markdown agents still exist in the codebase. Preserve support unless the task is explicitly about removing legacy paths.

## Development Rules

- Read `README.md` and `docs/compiler/*.md` before changing compiler behavior.
- Keep changes surgical. This repo is about deterministic config translation, not broad refactors.
- Add or update tests before changing behavior.
- Reuse parser, repository, planner, and app service code instead of manually transforming strings.
- Treat generated target files as outputs. Fix the source model, compiler, planner, or executor instead.
- If a correct source change plus `apply` would generate the target file, do not edit `.codex/`, `.cursor/`, `.config/opencode/`, or repo-local generated app directories by hand.
- Run tests with `uv run pytest`; for narrow changes, run the smallest relevant test first.

## Common Mistakes

- Editing target app config and expecting it to be the canonical source.
- Skipping `plan` and guessing what `apply` will do.
- Assuming every target supports the same fields natively.
- Dropping unsupported fields silently instead of validating or reporting lossiness.
- Adding new metadata fields without a schema update, target mapping, and tests.
