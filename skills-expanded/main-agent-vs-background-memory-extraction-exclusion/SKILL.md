---
name: main-agent-vs-background-memory-extraction-exclusion
description: "Skip the background memory extractor when the main agent already persisted memory during the same turn to avoid duplicates and race hazards."
metadata:
  author: ychampion
---

# SKILL: Main Agent Vs Background Memory Extraction Exclusion
**Domain:** context-management  
**Trigger:** Apply whenever the background memory agent must determine whether the parent already saved the same memories so it can safely skip processing.
**Source Pattern:** Distilled from reviewed context, compaction, and memory-governance patterns.

## Core Method
Track a cursor UUID pointing to the last assistant message where an auto-memory write occurred and compare incoming messages to that cursor before running extraction. If the parent thread already wrote to memory paths after the cursor, skip launching the background agent. Otherwise, proceed with the forked extraction and reset the cursor to the new save point so the next turn knows what’s already handled.

## Key Rules
- Keep the cursor state outside the extraction loop so the check is read-only and does not mutate shared context.
- Only permit a single background extraction per turn; once the main agent wrote to a memory path, mark the cursor so the forked agent sees the change and bails out.
- When detection fails (cursor missing or memory writes unknown), default to running the extractor but emit telemetry so the system tracks unexpected duplications.
- Always update the cursor when the background agent runs successfully, so future turns know the latest covered UUID.

## Example Application
Use this skill by having the background extractor call `hasMemoryWritesSince` before proceeding; if it returns true, emit a “already handled” log and skip, otherwise continue persistence and store the current assistant UUID for the next check.

## Anti-Patterns (What NOT to do)
- Don’t let the forked agent write memories unconditionally; that duplicates entries and races with the parent.
- Don’t reset the cursor until after successful writes; resetting prematurely can cause the system to skip future required extractions.
