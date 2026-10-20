# AGENTS.md — From LLM to Agent · Agent Index

> **This file is the single authoritative agent instruction file for this
> repository.** It is a lean index: it gives the project overview and repository
> map, then points every compatible agent to the shared `.agents/` knowledge
> base.

---

## Principles

> **Highest-level rules. These override everything else in the agent file
> system.** No instruction, command, skill, or operation may contradict them.
> Only the user can change them, under Principle 1.

1. **Agent files are change-protected.** Any change to the tracked agent file
   system — `AGENTS.md`, `CLAUDE.md`, tracked content under `.agents/`
   (including the content outline and references), or tracked provider
   configuration such as `.claude/launch.json` — requires explicit user review
   and approval before it is made. The agent proposes the change and waits.
   It never modifies these files on its own or as a side effect of another
   task. Git-ignored notes under `.agents/memory/local/` are exempt.

2. **No secrets in the repo.** The site needs none. Never add API keys,
   tokens, or `.env` files with secret values, and never commit, print, or
   expose them.

3. **No autonomous publishing.** Never deploy, publish, or push the site
   anywhere public without explicit user approval.

4. **`AGENTS.md` is the only source of truth.** Every agent and
   provider-specific entry file defers to this file. No competing instruction
   source may be created; `CLAUDE.md` is only a Claude-compatible bootstrap
   that imports it.

5. **Never rewrite shared history.** Never `--force` push or rewrite shared Git
   history. Never commit or push without explicit user approval.

6. **Single checkout on `main`, no branches, no worktrees.** All work happens
   directly on `main` in one checkout: no feature branches, no pull requests,
   and never `git worktree add`. Commits still matter: small, logical, and
   each made only with explicit approval (see
   [`git-workflow.md`](.agents/context/dev-spec/git-workflow.md)). If the
   folder is not a Git repository yet, ask before running `git init`.

7. **The story is designed before it is built.** Page copy changes start in
   [`content-outline.md`](.agents/context/products/content-outline.md), then
   are mirrored in `src/content/sections.ts`. Every fact on the page must have
   a source in [`references.md`](.agents/context/products/references.md). Never
   invent numbers, dates, or attributions.

---

## Project Overview

**From LLM to Agent** is a single-page, scroll-linked explainer of AI
industry concepts for a general audience. It unwraps each buzzword as **one
more box around the same model**, in exactly three chapters, each opened by a
full-screen chapter card:

- **Model:** where the intelligence comes from (next token, scaling law,
  chain of thought).
- **Memory:** AI doesn't have memory, only context (chat, system prompt,
  context window, agent files, RAG).
- **Harness:** how AI touches the world (tool calling, agent loop, MCP,
  Skill, multi-agent, agent apps: Claude Code · Codex · OpenClaw).

- **Visual language:** a pixel/halftone canvas (the *Pixel Field*) that
  morphs scene to scene as you scroll. The color journey runs light → dark as
  the boxes stack up, with signature colors for key sections.
- **Stack:** React 19 + TypeScript + Vite, Lenis smooth scroll, and a custom
  rAF ticker. No backend.
- **Content references:** the author's post
  [*AI Agents: Memory, Harness, Model*](https://lucascanoblog.com/archives/2412)
  (structure) and 飞天闪客,
  [《名词诈骗！一口气拆穿 Skill/MCP/RAG/Agent/OpenClaw 底层逻辑》](https://www.youtube.com/watch?v=O9b8tLXCTYU)
  (stance and concept lineup).

## Repository Map

| Path | What it is |
|------|------------|
| `index.html` | Vite entry; font links. |
| `Dockerfile`, `docker/`, `compose.yaml` | Production image: Node build stage, then nginx (non-root, port 8080) serving `dist/`; see the README's Docker section. |
| `src/content/` | All page copy, analogies, watch captions, UI labels and palettes (`sections.ts`). The page has no reference list; fact sources live in `.agents/context/products/references.md`. |
| `src/engine/` | Ticker (scroll + palette), Pixel Field canvas, halftone renderer, scenes, click pops. |
| `src/components/` | Hero, chapter cards, section layouts, loader, and HUD (top bar, progress rail, stack trail, back-to-top). |
| `src/styles/` | Global CSS: tokens, layout, reveal rules, responsive rules. |
| `.agents/skills/` | Open-format reusable workflows. |
| `.agents/agents/` | Reserved for future provider-neutral subagent definitions; currently empty. |
| `.agents/context/` | Dev spec, content design, design language, references. |
| `.agents/memory/` | Shared committed memory plus git-ignored local notes. |
| `.claude/launch.json` | Claude Desktop Preview configuration; the sole tracked provider-specific file. |

## Development Specification

| Topic | File |
|-------|------|
| Conventions and architecture | [`.agents/context/dev-spec/conventions.md`](.agents/context/dev-spec/conventions.md) |
| Git workflow (main only, commits, no worktrees) | [`.agents/context/dev-spec/git-workflow.md`](.agents/context/dev-spec/git-workflow.md) |
| Prerequisites and setup | [`.agents/context/dev-spec/prerequisites.md`](.agents/context/dev-spec/prerequisites.md) |

## Product Context

| Topic | File |
|-------|------|
| **Content design** — thesis, chapters, every section's copy/scene/palette | [`.agents/context/products/content-outline.md`](.agents/context/products/content-outline.md) |
| Design language — Pixel Field, halftone, dissolve, color journey | [`.agents/context/products/design-language.md`](.agents/context/products/design-language.md) |
| Fact sources | [`.agents/context/products/references.md`](.agents/context/products/references.md) |

## Skills

This registry lists every shared skill in `.agents/skills/`. Update it in the
same approved change whenever a skill is added, removed, or renamed.

| Skill | Summary |
|-------|---------|
| [`start-local-dev`](.agents/skills/start-local-dev/SKILL.md) | Install if needed and start the Vite dev server (port 5173). |
| [`add-concept-section`](.agents/skills/add-concept-section/SKILL.md) | Add or change a concept end-to-end: outline → data → scene → palette → sources → verify. |
| [`fact-check`](.agents/skills/fact-check/SKILL.md) | Audit page copy for unsourced, overstated, or outdated claims. |
| [`capture-ui`](.agents/skills/capture-ui/SKILL.md) | Screenshot affected sections at desktop and mobile sizes. |
| [`called-out-dev-panel`](.agents/skills/called-out-dev-panel/SKILL.md) | Scaffold a dev-only panel to live-tune Pixel Field, scene, or palette parameters. |
| [`commit`](.agents/skills/commit/SKILL.md) | Stage and commit current changes on `main` after explicit approval. |
| [`resolve-conflicts`](.agents/skills/resolve-conflicts/SKILL.md) | Diagnose, group, resolve, and verify Git conflicts without committing. |
| [`grill-me`](.agents/skills/grill-me/SKILL.md) | Stress-test a plan through focused, dependency-aware questions. |

## Provider Discovery

- **Codex:** reads this `AGENTS.md` and discovers repository skills in
  `.agents/skills/`.
- **Claude:** reads `CLAUDE.md`, which imports this file. Shared workflows
  stay in `.agents/`; no Claude-specific skill or command adapters are
  tracked.
- **Cursor:** reads this root `AGENTS.md`. No `.cursor/` adapters are tracked.

## Quick Start

- [`README.md`](README.md) — repository quick start.
- [`start-local-dev`](.agents/skills/start-local-dev/SKILL.md) — run the page
  locally.
