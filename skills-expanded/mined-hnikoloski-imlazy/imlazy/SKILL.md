---
name: imlazy
description: Use when you want tier-aware agent routing — detects task complexity, routes to Quick/Standard/Heavy/Vault workflows, and auto-dispatches the right agent. Trigger with /imlazy or "i am lazy" prefix.
---

# imlazy — Tier-Routed Agent Workflow

A token-efficient workflow system that classifies tasks by complexity and routes them to the right set of skills automatically.

## How It Works

Trigger with `/imlazy <task>` or `i am lazy, <task>` — the router classifies the task into a tier and loads only what's needed:

| Tier | When | Skills loaded |
|------|------|---------------|
| **Quick** | Simple, single-file, obvious solution | Minimal — just execute |
| **Standard** | Moderate complexity, clear scope | imlazy-planning (light) + imlazy-tdd + imlazy-code-review |
| **Heavy** | Multi-file, ambiguous, architectural | imlazy-brainstorm + imlazy-planning (full) + imlazy-tdd + imlazy-code-review |
| **Vault** | Knowledge persistence — "vault init", "vault save", "vault search", "create vault" | imlazy-vault |
| **Learn** | Router misclassification feedback | imlazy-learn |

## Included Skills

**Core workflow:** imlazy-router, imlazy-bootstrap, imlazy-brainstorm, imlazy-planning, imlazy-tdd, imlazy-code-review, imlazy-debug, imlazy-parallel, imlazy-worktrees, imlazy-learn, imlazy-vault, imlazy-verify, imlazy-subagents, imlazy-write-plans, imlazy-write-skills, imlazy-receive-review, imlazy-request-review, imlazy-strategic-save, imlazy-eval, imlazy-finish-branch

**Domain:** imlazy-wordpress, imlazy-security, imlazy-api-design, imlazy-frontend, imlazy-backend, imlazy-standards

**Obsidian vault:** obsidian-markdown, obsidian-bases, json-canvas, obsidian-cli, defuddle, imlazy-vault

## Installation

```bash
bash install.sh          # Unix / WSL
.\install.ps1            # Windows PowerShell
```

## Usage

```
/imlazy add a tag filter to the image library
i am lazy, fix the broken upload button
```
