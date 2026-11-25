---
name: standup-summary
description: "Summarize work completed over a time period using git commits + CK session data. Trigger: 'what did I get done', 'standup', 'weekly summary', 'status update'."
when_to_use: "Activate ONLY when the user asks for a work summary over a time range. Do NOT auto-trigger during coding or review tasks."
argument-hint: "[time period: yesterday, last 3 days, last week]"
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
  category: reporting
  ck_mcp_tools: [ck_session_digest, ck_outcome_tracker, ck_memory_search]
  related_skills: [proof-memory]
---

# Standup Summary

Summarize work over a time period. Enriches git log with CK session data for richer context than git alone.

## Do NOT use when
- During coding, review, or planning tasks
- The user wants code changes (not a summary)

## Workflow

1. Resolve time window from user input. Default: yesterday.
2. Read git commits by current user in range:
   ```
   git log --author="$(git config user.email)" --since="<start>" --until="<end>" --no-merges --format="%h %s"
   ```
3. Enrich with CK data:
   - `ck_session_digest` (mode: `generate`) for session tasks, findings, budget
   - `ck_outcome_tracker` (mode: `get_session`) for session outcomes and approval patterns
   - `ck_memory_search` for active decisions in the time window
4. Synthesize: prioritize substantial changes, omit cosmetic-only.
5. Output format:
   ```
   ## Standup: <start> – <end>
   <one sentence summary>
   ### Shipped
   - <2-5 bullets, major changes only>
   ### In progress / Blocked
   - <if any>
   ```

## Guardrails

- Every bullet traces to a commit or CK record — no fabrication
- Do not infer intent — describe changes functionally
- If no activity in range, say so clearly

## Output

- Concise status update with real date range
- 2-5 major bullets for substantial changes
