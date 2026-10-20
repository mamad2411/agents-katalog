---
alwaysApply: true
description: Core2 project identity and Cursor conventions
---

# Core2

This repo is **Core2**. Read identity from `.tapps-mcp.yaml` and the git remote, not from sibling workspaces.

## Identity

| Field | Value |
|-------|-------|
| Repo | `wtthornton/Core2` |
| Linear team | `TappsCodingAgents` (key `TAP`) |
| Linear project | `Core2` |
| Agent assignee | `Claude Agent` |

## Scope

- Engineering **code** for this repo only. Do not patch AgentForge or other siblings.
- Core2 Linear for Core2 implementation. Missing AF APIs → Linear **AgentForge Platform** (design only; do not build host middleware).
- Sibling repos under `C:\code` are reference-only unless the user names them.

## Vision (HARD)

Core2 device talks **directly** to AgentForge. No PC bridge.
Source of truth: `docs/firmware/VISION.md` (also `.cursor/rules/core2-af-direct.mdc`).

## Cursor layout

- Rules: `.cursor/rules/`
- Skills: `.cursor/skills/`
- MCP: `.cursor/mcp.json` (Linear + local NLT fleet)
- Agent instructions: `AGENTS.md`
