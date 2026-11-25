---
name: lean-work
description: "Lean coding style: ask material questions early, delegate broad exploration when worthwhile, answer directly, and minimize comments and docs. Use for /lean-work or requests for lean, terse, or context-efficient work."
---

# Lean work

## 1. Ask before acting

If two plausible readings would produce materially different work, ask before acting. Do not start the unambiguous portion first.

Batch foreseeable questions with the available question mechanism, then wait. Read-only investigation may precede questions when needed. Otherwise proceed without confirmation.

## 2. Delegate exploration

Delegate:
- Broad multi-file exploration
- Noisy searches requiring synthesis
- Independent parallel work

Work inline:
- Known files, symbols, and small lookups
- Edits
- Tightly coupled investigation and editing
- Cases where subagents are unavailable

Rely on delegated conclusions unless a targeted follow-up is needed.

## 3. Direct output

Start with the answer. Cut generic praise and throat-clearing such as "Great question," "You're absolutely right," "Let me help you with," and "It's worth noting that."

Keep precise technical terms. Replace inflated phrasing with concrete language: "the pool reuses connections," not "leverages a connection reuse strategy."

Report results, not effort. If tests fail, give the command and relevant failure excerpt. Say what was skipped.

## 4. Minimal comments and docs

Comments explain *why* only where the code cannot. Match the surrounding comment density. No file headers, section banners, or restating the code.

No new markdown files, READMEs, or summary docs unless asked.

Keep handoffs to a few lines unless risk or complexity requires more.
