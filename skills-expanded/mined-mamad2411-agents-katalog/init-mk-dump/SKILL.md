---
name: init-mk-dump
version: 1.0.0
description: One-time setup for the monkey-brain dump system. Creates directory structure, MONKEY_BRAIN_TEMPLATE.md, and empty dump-index.md. Use when user runs /init-mk-dump or needs to set up the system for the first time. Does not create sessions.
---

# init-mk-dump

One-time setup. Safe to re-run — always refreshes the template, skips dump-index.md if it already exists (user data).

## Flow

1. **Detect the active AI tool** — check which files/folders exist to identify the tool:
   - `.cursor/` exists → **Cursor** → instructions file: `.cursor/rules/monkey-brain.mdc`
   - `.windsurf/` exists → **Windsurf** → instructions file: `AGENTS.md`
   - `.github/` exists → **GitHub Copilot** → instructions file: `.github/copilot-instructions.md`
   - `GEMINI.md` exists → **Gemini CLI** → instructions file: `GEMINI.md`
   - `CLAUDE.md` exists → **Claude Code** → instructions file: `CLAUDE.md`
   - None of the above → default to **AGENTS.md** (universal standard)
   - If multiple signals conflict: ask the user which tool they are using.

2. **Install karpathy-guidelines (Claude Code only)** — skip this step for all other tools.
   - Run `claude plugins list` and check if `andrej-karpathy-skills` appears.
   - If missing: run in order:
     ```
     claude plugins marketplace add karpathy-skills github:forrestchang/andrej-karpathy-skills
     claude plugins install andrej-karpathy-skills@karpathy-skills
     ```
     Then tell user: "karpathy-skills installed — **restart Claude Code** before continuing."
   - If already installed: continue silently.

3. Create `docs/monkey-brain/`, `docs/monkey-brain/dump-sessions/`, and `docs/monkey-brain/specs/` if they don't exist
4. Always overwrite `docs/monkey-brain/MONKEY_BRAIN_TEMPLATE.md` — use content below (template is skill-owned, not user data)
5. Create `docs/monkey-brain/dump-index.md` if it doesn't exist — use format below
6. Create `docs/monkey-brain/spec-index.md` if it doesn't exist — use format below
7. **Write Core Philosophy to the detected instructions file** — check if it contains a `## Core Philosophy` section. If not, append the section below. If the file doesn't exist, create it with only the Core Philosophy section (create parent folders if needed).
8. Tell user: setup complete, which tool was detected, which file was written, then run `/add-mk-dump` to start first session

## Templates

**`docs/monkey-brain/MONKEY_BRAIN_TEMPLATE.md`** — write content from `MONKEY_BRAIN_TEMPLATE.md` exactly as-is.

**`docs/monkey-brain/dump-index.md`** — write content from `DUMP_INDEX_TEMPLATE.md` exactly as-is.

Notes:
- `latest:` is filled by `/add-mk-dump` on first session
- File paths in the Sessions table are relative to `docs/monkey-brain/dump-sessions/`
- Status: `dumped` = raw session created, `cleaned` = summary written, `kicked` = spec created

**`docs/monkey-brain/spec-index.md`** — write exactly if the file doesn't exist:

```
# Spec Index

| File | Status | Date done | Note |
|------|--------|-----------|------|
```

**`## Core Philosophy` section** — append exactly to the detected instructions file if the section is missing:

```
## Core Philosophy

Always active in every session. Skills must honor these principles.

**Layer 1 — Universal (always active):**

1. **Think before acting** — state assumptions, ask if unclear, present multiple interpretations
2. **Simplicity first** — minimum output that solves the problem — applies to code, docs, .md files equally
3. **Surgical** — touch only what the task requires, nothing adjacent
4. **Goal-driven** — define success criteria upfront, verify completion
5. **Low friction** — choose the path that keeps momentum in the right direction; start small
6. **Don't assume 100%** — hold conclusions loosely, leave room for bias — both user and Claude
7. **Multi-lens re-examination** — consider multiple perspectives before deciding

**Layer 2 — Thinking phase only (kick/grill/planning):** also consider emotional state, time, money, motivation, environment. Do NOT apply these in execution — too heavy.

For coding tasks: invoke `andrej-karpathy-skills:karpathy-guidelines` skill — full coding detail lives there, not here.
```
