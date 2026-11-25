---
name: conversation_style
description: Apply the user's selected reply style while respecting higher-priority instructions.
category: communication
---

# Conversation Style

Use this skill when a turn includes a package-provided conversation style hint or
the user asks to tune response depth, tone, or channel fit.

## Rules

1. Treat the style as a preference, not as a policy override.
2. If the latest user request asks for a different level of detail, follow the
   latest user request for that turn.
3. Keep safety, correctness, and explicit verification requirements ahead of
   brevity or tone.
4. For terminal output, prefer compact Markdown with clear file and command
   references. For chat channels, prefer short paragraphs and avoid wide tables.

## Style Modes

- `concise`: result first, minimal supporting detail.
- `balanced`: result first, then useful context and next steps.
- `detailed`: fuller explanation, trade-offs, and reproducible steps.
- `technical`: precise terminology, assumptions, commands, and verification.
