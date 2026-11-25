---
name: engagement-setup
description: |
  This skill should be used when the user mentions "new engagement", "setup engagement",
  "initialize workspace", "start operation", "new pentest", "setup project",
  "create workspace", "engagement setup", "initialize engagement", "new investigation",
  "start campaign", "new operation", "workspace init", "set up a new operation",
  "begin engagement", or discusses setting up a new offensive security engagement
  from scratch with target definition, plugin selection, and workspace creation.
---

# Engagement Setup

Initialize a new engagement workspace with target configuration, plugin selection, tool verification, and tailored project files.

## Quick Start

Run `/setup` to start the interactive wizard, or `/setup <engagement-name>` to skip the name prompt.

## What Gets Created

| File              | Purpose                                                                       |
| ----------------- | ----------------------------------------------------------------------------- |
| `engagement.json` | Central engagement config — name, targets, plugins, opsec profile, timestamps |
| `CLAUDE.md`       | Tailored guidance for this engagement — active plugins, commands, workflows   |
| `README.md`       | Human-readable engagement overview and status tracker                         |
| `scope.md`        | Formal scope definition — in-scope, out-of-scope, rules of engagement         |
| `targets.jsonl`   | Structured target list with types (domain, ip, cidr, org, individual)         |
| `.gitignore`      | Runtime data file ignore patterns for all active plugins                      |

## Plugin-Aware Setup

The setup process knows about all fsociety plugins and will:

1. **Check tool dependencies** — Runs each plugin's tool-checker (Tier 1/2/3)
2. **Tailor CLAUDE.md** — Only includes commands and skills for active plugins
3. **Configure OPSEC profiles** — Maps unified profile (surface/standard/paranoid) to each plugin's native profiles
4. **Detect cross-plugin pipelines** — Documents tyrell→elliot data flows when both are active
5. **Generate goal-specific workflows** — Suggests first commands based on engagement goals

## Available Plugins

| Plugin      | Domain                     | Agents         |
| ----------- | -------------------------- | -------------- |
| **elliot**  | Web & Application Security | scout, darlene |
| **romero**  | Reverse Engineering        | cipher         |
| **trenton** | Operational Security       | ghost, cleaner |
| **tyrell**  | Leak Database Hunting      | joanna, scott  |

## OPSEC Profiles

| Profile    | Description                       | Timing        |
| ---------- | --------------------------------- | ------------- |
| `surface`  | No anonymity, max speed — lab/CTF | Immediate     |
| `standard` | Basic precautions, moderate speed | 1-5s delays   |
| `paranoid` | Full anonymity, Tor/VPN required  | 10-60s delays |

## Re-Running Setup

Running `/setup` in a directory with an existing `engagement.json` will offer to:

- Update targets, plugins, or scope (non-destructive)
- Re-check tools for newly added plugins
- Regenerate CLAUDE.md and README.md with updated configuration
- Append new targets to targets.jsonl (SHA256 deduplication prevents duplicates)

## Additional Resources

- **`references/engagement-guide.md`** — Target taxonomy, scope best practices, plugin selection matrix, cross-plugin pipelines
