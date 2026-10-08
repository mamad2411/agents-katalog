---
name: ccgs-game-studio
description: "Use when a user invokes CCGS Game Studio workflows or slash-command style procedures for game project onboarding, design, architecture, implementation stories, reviews, QA, release, engine setup, or studio process guidance."
---

# CCGS Game Studio

This project-local skill is a Codex conversion of the portable parts of Claude Code Game Studios installed in `.claude/`.

## Start Here

1. Identify the user's requested workflow. If they use an original slash command such as `/start` or `/design-system`, map it through `references/slash-commands.md`.
2. Read only the matching file in `references/workflows/` plus the role, rule, template, or engine references it explicitly needs.
3. Treat workflow names such as `start`, `brainstorm`, `design-system`, `dev-story`, `vertical-slice`, and `gate-check` as named Codex procedures. Use `references/slash-commands.md` for the full list.
4. Use `assets/templates/` when a workflow asks for a source template.
5. Use `references/engine-reference/` for version-pinned Godot, Unity, and Unreal notes.

## Claude-to-Codex Adaptation Rules

- Preserve original `/name` slash commands as aliases. Codex users can invoke the generated wrapper skill for that command or invoke this main skill with the slash command in the prompt.
- Ignore Claude frontmatter fields such as `allowed-tools`, `argument-hint`, `user-invocable`, `agent`, and `model` except as preserved metadata.
- Map Claude tools to Codex behavior: `Read`/`Glob`/`Grep` mean inspect files, `Write`/`Edit` mean make scoped edits under normal Codex editing rules, `Bash` means shell commands with normal approval and sandbox handling, and `WebSearch`/`WebFetch` mean browse current sources when required.
- Map `AskUserQuestion` to a concise chat question, or `request_user_input` when that tool is available.
- Map `TodoWrite` to Codex planning only when a task list materially helps.
- Treat `Task`, `subagent_type`, and named Claude agents as role-review guidance. Do not claim that persistent Claude subagents exist. Only delegate to Codex subagents when the user explicitly asks for delegated or parallel agent work and the active Codex tools permit it.
- When a workflow says to read `CLAUDE.md`, read `AGENTS.md` first if present, then `CLAUDE.md` if the project still has Claude-era guidance.
- When a workflow references `.claude` runtime settings, hooks, status lines, or agent memory, skip that runtime behavior unless an equivalent Codex plugin or hook exists in the current environment.
- Keep the source workflow's collaborative approval intent, but follow current Codex editing instructions and sandbox rules over legacy Claude tool wording.

## Reference Map

- `references/workflows/`: converted slash-command workflows.
- `references/slash-commands.md`: original `/command` to Codex wrapper mapping.
- `references/agents/`: converted role references from Claude subagents.
- `references/rules/`: converted path and domain rules.
- `references/docs/`: studio process, coordination, context, and workflow catalog references.
- `references/engine-reference/`: Godot, Unity, and Unreal reference notes.
- `references/testing-framework/`: source skill test specs and rubric.
- `assets/templates/`: document templates used by authoring workflows.

## Common Routing

- New project or unsure where to begin: load `references/workflows/start.md`.
- Existing game project adoption: load `project-stage-detect.md` and `adopt.md`.
- Game concept exploration: load `brainstorm.md`.
- Small design change: load `quick-design.md`.
- Full system design: load `design-system.md`.
- Engine setup: load `setup-engine.md` and the matching engine reference.
- Architecture work: load `create-architecture.md`, `architecture-decision.md`, `create-control-manifest.md`, or `architecture-review.md`.
- Implementation stories: load `create-epics.md`, `create-stories.md`, `story-readiness.md`, `dev-story.md`, or `story-done.md`.
- Vertical slice work: load `vertical-slice.md` before committing to production.
- Reviews and gates: load `design-review.md`, `code-review.md`, `gate-check.md`, `scope-check.md`, or the relevant audit workflow.
- Release work: load `release-checklist.md`, `launch-checklist.md`, `changelog.md`, `patch-notes.md`, `hotfix.md`, or `day-one-patch.md`.

## Omitted Source Parts

The converter intentionally omits active Claude runtime registration:

- `.claude/settings.json`
- `.claude/hooks/` as executable hooks
- `.claude/statusline.sh`
- `.claude/agent-memory/`
- Claude local settings templates and hook reference docs as runtime behavior
