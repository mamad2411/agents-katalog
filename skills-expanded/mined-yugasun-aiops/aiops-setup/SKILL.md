---
name: aiops-setup
description: Configure a target project for the aiops bundle — issue tracker, triage labels, domain doc layout. Silent defaults on inline bootstrap; full prompts on explicit /aiops-setup.
disable-model-invocation: true
---

# aiops-setup

Scaffold per-repo config: **issue tracker**, **triage labels**, **domain docs**.

## Modes

### Silent bootstrap (from `/aiops` conductor)

When `docs/agents/` is missing:

1. Read repo-root `aiops.yaml` if present — see [aiops-yaml.md](aiops-yaml.md).
2. **No yaml** → `issue_tracker.kind: local`, triage labels 1:1, `domain.layout: single`. Write `docs/agents/*` **without asking**.
3. **Yaml with `github` or `gitlab`** → seed matching `issue-tracker-*.md`; apply yaml `prs_as_triage` and label overrides. No A/B/C questionnaire unless yaml is incomplete.
4. Update `CLAUDE.md` or `AGENTS.md` `## Agent skills` block (create section if missing; ask only if neither file exists).

### Full setup (explicit `/aiops-setup`)

Interactive — explore, confirm one section at a time, then write. Use when switching tracker or restarting config.

## Full setup process

### 1. Explore

Check: `aiops.yaml`, `git remote`, `AGENTS.md` / `CLAUDE.md`, `CONTEXT.md`, `CONTEXT-MAP.md`, `docs/adr/`, `docs/agents/`, `.scratch/`.

### 2. Ask (one section at a time)

Skip sections already satisfied by `aiops.yaml` — show yaml values and offer edit only.

**A — Issue tracker:** Only offer GitHub/GitLab in the questionnaire if user has no `aiops.yaml` **and** explicitly asks for remote tracker. Otherwise default local markdown.

**B — Triage labels:** Map five roles to tracker strings. Default 1:1.

**C — Domain docs:** Single-context (`CONTEXT.md` + `docs/adr/`) or multi-context (`CONTEXT-MAP.md`).

**D — Constitution:** If `CONSTITUTION.md` does not exist at repo root, offer to generate one from [constitution-template.md](constitution-template.md). Walk through each section (Testing, Code quality, Architecture, Performance, Security, Process) and ask the user to fill in project-specific principles. These are **non-negotiable** — referenced by every agent at every phase.

### 3. Confirm draft

Show `## Agent skills` block + `docs/agents/issue-tracker.md`, `triage-labels.md`, `domain.md` for user edit.

### 4. Write

Seed templates: `issue-tracker-*.md`, `triage-labels.md`, `domain.md`. If constitution was configured, write `CONSTITUTION.md` from template with user's answers.

### 5. Done

Point user to `docs/agents/*.md`. Optional: add `aiops.yaml` from [aiops.yaml.example](aiops.yaml.example) for reproducible team defaults.
