---
name: using-xskill
description: Use when installing, configuring, or operating xskill (the `xskill` CLI / `pip install xskill`) — starting the daemon, registering trajectory dirs, joining a team server, understanding how trajectories become Skills, or rebuilding/re-distilling the skill library after a model change.
---

# Using xskill

## Overview

xskill distills reusable **Skills** (`SKILL.md` folders) out of the real execution
trajectories of coding agents (Claude Code, Codex, OpenCode, Cursor, …). A background
daemon watches each agent's session logs, slices them into single-intent **atoms**,
clusters atoms into skills, and writes/versions each skill in its own git folder. New
skill versions only replace old ones when real traffic shows they serve users better
(canary A/B by UX score) — not by an LLM grading itself.

**Core mental model:** raw trajectory → atoms → candidate routing → SKILL.md → canary
A/B → installed into every agent's skill dir. You operate the daemon; the daemon does
the distilling.

## When to Use

- Installing xskill or filling in `~/.xskill/config.yaml` (LLM + embedding endpoints)
- Starting/keeping the daemon running (`xskill serve`), or backfilling old trajectories
- Joining or hosting a team server (`xskill serve --server` / `xskill connect`)
- Understanding the agent pipeline, atoms, canary/UX scoring, or deployment modes
- **Re-distilling the whole skill library** (e.g. after switching to a stronger model)

## Quick Reference

| Command | What it does |
|---------|--------------|
| `pip install xskill` | Install (Python 3.9+) |
| `xskill serve` | Standalone daemon: FastAPI + watcher; first run writes `~/.xskill/config.yaml` then exits |
| `xskill serve --server` | Team server: owns all LLM calls + git; prints a join token |
| `xskill connect <host:port> --token <t>` | Join a team server as a thin client |
| `xskill registry add <path>` | Backfill / watch an extra trajectory directory |
| `xskill traj search <query>` / `xskill search <query>` | Search trajectories or skills |
| `xskill read <path> --eco <eco>` | Batch-ingest db trajectories (ngagent/opencode) |
| `xskill rebuild [--force]` | Re-distill from existing raw trajectories (see reference) |
| `xskill stats` | Token usage & estimated cost |

The daemon is the engine: most commands only change state in the DB; nothing is
distilled unless `xskill serve` (or the team server) is running.

## Progressive Disclosure — read on demand

- **Install & configure** (config.yaml fields, per-agent collect/install paths, team
  client setup): `references/installation.md`
- **How it works** (TaskAgent → TaskClusterAgent → SkillEditAgent, atoms, canary/UX
  scoring, standalone vs team mode): `references/mechanisms.md`
- **Rebuild the skill library** (a ready-to-run prompt that walks a model through
  re-distilling correctly): `references/rebuilding-skill-library.md`

## Common Mistakes

- **Running `rebuild` with no daemon up.** `rebuild` only resets DB state; the watcher
  in `serve` does the actual re-split/re-cluster every 30s. No daemon = nothing happens.
- **Deleting raw `~/.xskill/*_sessions/*.md`.** Those are the *input* to distillation —
  delete them and you can no longer rebuild.
- **Expecting DeepSeek to do embeddings.** DeepSeek has no embedding endpoint; point the
  `embedding:` block at DashScope / OpenAI / Ollama.
- **Putting tokens in public places.** Team join tokens must never land in a public repo
  or chat log.
