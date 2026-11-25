---
name: continual-learning
description: "Auto-mine session for durable memory: user preferences and workspace facts. Trigger: 'learn from this', 'update memory', 'save what we learned', or at session end."
when_to_use: "Activate at session end, when the user asks to save learnings, or periodically in long sessions. Do NOT use during active coding."
argument-hint: "[optional: specific area to learn from]"
disable-model-invocation: true
license: Apache-2.0
compatibility:
  - opencode-native
  - claude-standalone
  - cursor-native
  - codex
metadata:
  author: controlkeel
  version: "1.1"
  category: memory
  ck_mcp_tools: [ck_memory_search, ck_memory_record, ck_memory_archive]
  related_skills: [proof-memory]
---

# Continual Learning

Auto-mine session activity for durable memory updates. CK's `ck_memory_record` is manual — this skill automates extraction.

## Do NOT use when
- During active coding (distracts from the task)
- When no meaningful session activity has occurred
- To record secrets, tokens, or transient debugging state

## What gets learned (only two categories)

1. **User Preferences**: Recurring corrections, preferred patterns, naming, tools, workflows
2. **Workspace Facts**: Stable codebase facts, architecture decisions, module ownership, constraints

## What does NOT get learned

Secrets, one-off instructions, transient state, process meta-guidance

## Workflow

1. Search `ck_memory_search` for existing memories to avoid duplication.
2. Scan session recent events (reviews, findings, decisions) for:
   - User corrections recurring more than once
   - Architecture decisions approved and not reversed
   - Workspace facts discovered and not contradicted
   - Preferences stated explicitly or demonstrated consistently
3. For each candidate: Is it durable? Reusable? Specific? If no to any, skip.
4. Record via `ck_memory_record`:
   - Preferences → type `decision`, tags `["user-preference"]`
   - Facts → type `brief`, tags `["workspace-fact"]`
5. Archive superseded items via `ck_memory_archive`.
6. If no high-signal items found: "No high-signal memory updates."

## Rules

- Plain bullet points only — no metadata blocks, confidence scores
- Cap at 12 items per section
- Deduplicate semantically — "prefer Req" and "always use Req" are the same item
- Update in place, do not create duplicates alongside old items
- Never record secrets

## Output

- `ck_memory_record` entries for new preferences/facts
- `ck_memory_archive` for superseded items
- Summary: "Recorded N preferences, M facts, archived K items."
