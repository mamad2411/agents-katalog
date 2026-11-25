---
name: auto-learn
description: "Auto-captures corrections and confirmations from every conversation → writes to ~/.claude/session-queue.jsonl → processed by Stop hook into memory files."
allowed-tools: Bash, Write
---

# Auto-Learn — Session Learning Capture

## What It Does
Every session: captures corrections ("no, don't do that") and confirmations ("yes, exactly")
→ writes learnings to `~/.claude/session-queue.jsonl`
→ Stop hook processes into `~/.claude/projects/-Users-mc/memory/` as feedback/user memories

## Always Active
Runs on every prompt. Cannot be disabled. Feeds the memory system.

## Queue File
`~/.claude/session-queue.jsonl` — processed after each session by Stop hook
