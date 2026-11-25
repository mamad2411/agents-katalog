---
name: list-skills
description: List all PAI skills. Use when user asks "list skills", "available skills", "what can you do", "exact output", or "show me the output" of org_skill.py --list.
---

# List Skills — Passthrough Only

When this skill triggers, the user wants the raw skill list.

## Required Behavior

1. Run `python3 _scripts/org_skill.py --list`
2. **Your response must be ONLY the command output** — copy it exactly, line for line
3. **Do NOT add:** Reflection, Next Steps, Key Insight, summaries, or any other text
4. **Do NOT suggest** `org_skill.py --run` — that flag does not exist

