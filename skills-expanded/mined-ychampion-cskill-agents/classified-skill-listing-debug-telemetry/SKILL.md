---
name: classified-skill-listing-debug-telemetry
description: "Emit low-cost debug telemetry for skill-listing batches that records batch size, initial-vs-dynamic mode, and cumulative sent count without logging the payload body."
metadata:
  author: ychampion
---

# SKILL: Classified Skill Listing Debug Telemetry
**Domain:** command-surfaces  
**Trigger:** Apply when a listing or announcement pipeline needs debuggable operational signals, but logging the full payload would be noisy, expensive, or sensitive.
**Source Pattern:** Distilled from reviewed command-surface and listing-control patterns.

## Core Method
Emit one compact debug log per listing batch that classifies the batch and summarizes its size. Record the current batch count, whether it is the initial or a dynamic update, and the cumulative sent total after state mutation, but omit the actual payload content. This gives operators enough information to trace listing behavior, verify delta logic, and spot regressions without leaking or duplicating the rendered skill list in logs.

## Key Rules
- Log derived counts and batch class, not the rendered listing body or full command set.
- Use the same post-filter batch that will actually be emitted so telemetry matches runtime behavior.
- Include both per-batch and cumulative counts; one without the other makes delta behavior harder to debug.
- Keep the telemetry call close to payload construction so classification and counts cannot drift from what is sent.

## Example Application
If a REPL session emits a first skill-listing attachment with seven items, log a line such as "sending 7 skills, initial, 7 total sent" before formatting the payload. When two more skills appear after a plugin reload, emit a second line classified as dynamic with the updated cumulative total, without logging the actual skill names.

## Anti-Patterns (What NOT to do)
- Do not log the full listing payload just to debug batch behavior; it bloats logs and may expose irrelevant content.
- Do not emit debug telemetry from the pre-filter command pool; the logged counts must reflect the exact emitted delta.
