---
name: harness-creator
description: Use when creating or adapting a coding-agent harness for either an existing repository or a new project, especially when you need to preserve working flows such as spec-driven development, verification paths, or session continuity.
license: MIT
---

# Harness Creator

Build or adapt a repo-local harness without breaking the repo's current working model.

**Language rule:** Unless the user explicitly asks otherwise, follow this logic to choose the scaffold language:

1. **Existing repo mode** — detect the harness language by scanning `AGENTS.md`, `CLAUDE.md`, `README.md`, `docs/AGENTS.md`, `specs/AGENTS.md`, or other top-level prose files. If the majority of these files are written in Chinese, recommend Chinese templates and confirm with the user. Otherwise default to English.
2. **Greenfield mode** — ask the user which language they prefer before generating any scaffold. Offer English and Chinese as choices.

Templates are organized under `templates/en/` (English) and `templates/zh/` (Chinese). When scaffolding, pick the subdirectory that matches the chosen language.

## When to use

Use this skill when:

- A user wants `AGENTS.md`, `CLAUDE.md`, progress tracking, verification rules, or session continuity.
- A repository already has some harness structure, and you need to improve it without replacing its source of truth.
- A new or early-stage project needs an initial harness, but the workflow and architecture still need to be clarified.

Do not use this skill for prompt engineering, model choice, or generic software architecture.

## Core rule

**Do not force one harness shape onto every repository.**

## High-fidelity templates

Treat these bundled templates as the highest-fidelity scaffold sources:

- `templates/{en,zh}/architecture.md`
- `templates/{en,zh}/specs-agents.md`
- `templates/{en,zh}/docs-agents.md`

Use them when generating:

- `ARCHITECTURE.md`
- `specs/AGENTS.md`
- `docs/AGENTS.md`

Do not collapse them into short summaries. Match their level of specificity, section granularity, and formatting discipline, then adapt the content to the target repository.

For `specs/AGENTS.md`, preserve the detailed rules for:

- directory responsibilities
- file naming
- plan template structure
- phase and task formatting
- lifecycle transitions
- writing guidance

For `docs/AGENTS.md`, preserve the detailed rules for:

- writing principles
- numbering rules
- frontmatter requirements
- section templates

Then extend the docs model to cover:

- `docs/lessons/`
- `docs/features/`
- `docs/decisions/`

Use `docs/decisions/` as the long-term home for durable design decisions instead of a separate specs constitution folder.

Choose one of two modes:

1. **Existing repo mode**
   - Inspect the current harness first.
   - Preserve the existing source of truth if it works.
   - If the repo is already spec-driven, extend that path instead of adding parallel `feature_list.json`, `progress.md`, or handoff files by default.

2. **Greenfield mode**
   - If the repo is empty or very early, gather enough product and workflow context first.
   - If the user has not defined architecture, lifecycle, or execution style, ask for that context before generating files.
   - Only scaffold after the working model is clear enough.

## Workflow

### 1. Detect the repo mode

Look for:

- `AGENTS.md`, `CLAUDE.md`
- `specs/AGENTS.md`, `specs/active/`, `specs/draft/`, `specs/archive/`
- `docs/AGENTS.md`, `docs/lessons/`, `docs/features/`, `docs/decisions/`
- `feature_list.json`, `progress.md`, `session-handoff.md`
- `init.sh`, `bootstrap`, `check`, or other readiness entrypoints

If the repo already has a coherent harness, improve it in place. Do not create duplicate truth sources.

Use [Repo Adaptation Pattern](references/repo-adaptation-pattern.md) for this pass.
Use [Specs Directory Pattern](references/specs-directory-pattern.md) and [Docs Directory Pattern](references/docs-directory-pattern.md) when the repo already separates planning from knowledge capture.

### 2. Pick the state source on purpose

The agent needs one primary control plane for scope and status. Common options:

- **Spec-driven**: active spec + docs decisions + status checkboxes
- **Feature-list-driven**: `feature_list.json` + `progress.md`
- **Minimal**: `AGENTS.md` + readiness path + short progress log

If the repo already has a good state source, keep it.

Use [Spec-Driven Harness Pattern](references/spec-driven-harness-pattern.md) when long-running work is phase-based.

### 3. Define readiness instead of blindly adding `init.sh`

The harness must define how the agent proves the repo is ready to work on. That can be:

- `init.sh`
- a smaller verification script
- a startup checklist inside `AGENTS.md`
- a phase-0 section in an active spec

Use readiness gates that match the repo, not a fixed bootstrap ritual.

### 4. Encode end-of-session continuity

The repo must answer:

- What is the current focus?
- What is done?
- What is blocked?
- What proof exists?
- Where does the next session resume?

That continuity can live in `progress.md`, `session-handoff.md`, or an actively maintained spec.

## Specs and docs are complementary

Treat `specs` and `docs` as two different but related systems:

- **`specs/`** pushes active development forward.
- **`docs/`** captures stable explanations, lessons, feature behavior, and durable decisions.

When the repository uses structured planning, prefer this split:

- `specs/active/NN-topic-plan.md` for execution
- `docs/features/NN-topic.md` for user-facing or system-facing capability docs
- `docs/lessons/NN-topic.md` for experience summaries and non-obvious implementation lessons
- `docs/decisions/NN-topic.md` for durable cross-spec decisions

Do not bury durable decisions inside stale specs if they need to outlive one implementation plan.

### 5. Keep governance separate from planning

Spec-driven development can replace some progress and state files, but it does **not** replace:

- clean-state discipline
- verification discipline
- repository hygiene
- periodic governance reviews

Use [Gotchas](references/gotchas.md) before finalizing a design.

## Templates and scripts

Use these bundled assets selectively. Prose templates live under language-specific subdirectories:

```
templates/
├── en/                     # English templates
│   ├── agents.md
│   ├── architecture.md
│   ├── specs-agents.md
│   ├── docs-agents.md
│   ├── docs-decision.md
│   ├── docs-feature.md
│   ├── docs-lesson.md
│   ├── active-spec.md
│   ├── progress.md
│   ├── session-handoff.md
│   └── readiness-check.md
├── zh/                     # Chinese templates
│   ├── agents.md
│   ├── architecture.md
│   ├── specs-agents.md
│   ├── docs-agents.md
│   ├── docs-decision.md
│   ├── docs-feature.md
│   ├── docs-lesson.md
│   ├── active-spec.md
│   ├── progress.md
│   ├── session-handoff.md
│   └── readiness-check.md
├── feature-list.json       # language-neutral
├── feature-list.schema.json
└── init.sh                 # language-neutral
```

Scripts:

- `scripts/detect-harness.sh`
- `scripts/scaffold-greenfield.sh`

Never copy every template by default. Pick the smallest set that fits the repo mode.

When generating `specs/AGENTS.md` or `docs/AGENTS.md`, prefer the detailed templates over a minimal directory guide. Only emit a minimal version if the user explicitly asks for one.

## Common mistakes

- Replacing a spec-driven workflow with `feature_list.json` just because the course used it.
- Adding `init.sh` when the repo only needs a lightweight readiness check.
- Creating `progress.md` and `session-handoff.md` even though the active spec already tracks phase state well.
- Letting planning files and governance files drift apart.
- Creating multiple status sources that disagree.
