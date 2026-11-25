---
name: evolution-guide
description: Explains how Evolving Lite works when the user asks about the system, its features, or how to use it. Triggers on questions like "how does this work", "what is evolving lite", "what hooks are running", "explain the system".
---

# Evolution Guide

When the user asks about Evolving Lite, explain based on their question:

## What is Evolving Lite?

A Claude Code plugin that learns from your corrections, manages your context budget, and improves every session - automatically. You install it once and it works in the background while you code normally.

## The 4 Feedback Loops

### LEARN Loop (active from Tier 2, session 3+)
You correct Claude -> correction-detector recognizes it -> creates an Experience file -> next time a similar problem comes up, thinking-recall injects that experience mid-conversation. Claude doesn't make the same mistake twice.

### HEAL Loop (active from Tier 1)
health-sentinel checks at every session start whether all hooks ran correctly last session. If a hook silently failed (no sentinel output), you get a warning immediately. The system also has integrity-checker/fixer agents for deeper repairs.

### EVOLVE Loop (active from Tier 1)
usage-tracker counts what tools and commands you use. auto-archival removes stale experiences (>90 days unused). The system gets leaner and more focused over time without you doing anything.

### CONTEXT Loop (active from Tier 1)
context-warning monitors your context budget. At 70% it warns you. At 93% it suggests creating a handoff. precompact-extract saves important knowledge before compaction wipes it. You never lose context silently.

## Tiered Activation

All hooks are installed from day one but activate progressively:

| Tier | Active from | What activates | Purpose |
|------|------------|----------------|---------|
| 1 | Session 1 | context-warning, security-tier-check, health-sentinel, usage-tracker | Safety & monitoring |
| 2 | Session 3 | correction-detector, delegation-enforcer, session-summary | Learning & delegation |
| 3 | Session 10 | thinking-recall, auto-archival, precompact-extract | Deep memory & maintenance |

## Available Commands

All commands are optional. The system works fully automatically without using any of them.

| Command | What it does |
|---------|-------------|
| `/debug` | Start a structured 4-phase debugging workflow |
| `/plan-new` | Plan a complex project with discovery and kill criteria |
| `/remember` | Explicitly save something to memory |
| `/whats-next` | See current status and next steps |
| `/context-stats` | Check context window usage |
| `/sparring` | Adversarial brainstorming |
| `/think` | Apply structured thinking frameworks |
| `/evolution` | See what the system learned/changed recently |
| `/evolving-update` | Check for and install updates |
| `/create-command` | Create your own custom command |
| `/create-hook` | Create your own automation hook |
| `/review` | Structured code review |
| `/haiku` `/sonnet` `/opus` | Switch Claude model |

## Where Data Lives

All data is local in the plugin directory:
- `_memory/experiences/` - Learned patterns and solutions (JSON files)
- `_memory/sessions/` - Session summaries (Markdown files)
- `_memory/projects/` - Project state and progress
- `_memory/analytics/` - Usage counts and evolution log
- `_graph/cache/` - Context routing and delegation config

## Enhancing with Kairn (optional)

Install `kairn-ai` (pip install kairn-ai) for semantic memory search across sessions. Without Kairn, memory search is keyword-based. With Kairn, you can ask "how did I solve the auth problem?" and get results even if you used different words.

## Uninstalling

Remove the plugin path from `pluginDirectories` in `~/.claude/settings.json`. Your memory data stays in the plugin directory - delete it if you want a clean removal, or keep it if you might reinstall later.
