---
name: corporate-launcher
description: Generates a secure, branded, organization-specific launcher that wraps Claude Code, Codex CLI, Gemini CLI, Cursor, or Cline onto a corporate AI gateway. Triggers on "wrap claude for my company", "white-label cline", "internal AI CLI", "bedrock gateway", "azure openai cli", "vertex cli".
---

# Corporate Launcher (Gemini skills surface)

Gemini CLI extensions can also expose **skills** under `skills/<name>/SKILL.md`. This file mirrors the canonical `SKILL.md` at the repo root.

For the complete workflow, templates, reference files, and quality bar, see the repo root `SKILL.md`:
https://github.com/Connected-Mate/corporate-launcher

## Quick workflow

1. Phase 0 — confirm CLI + backend
2. Phase 1 — interview (`references/interview-flow.md`)
3. Phase 2 — validate + confirm
4. Phase 3 — render via `scripts/render.py`
5. Phase 4 — distribution kit
6. Phase 5 — post-install summary
