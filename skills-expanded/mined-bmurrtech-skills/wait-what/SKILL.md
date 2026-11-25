---
name: wait-what
description: >
  Stop and re-pitch the last explanation in plain ASD-STE100 Simplified Technical
  English; prefer CONTEXT.md ubiquitous language when present. Use when the user
  is lost, says wait-what, or the last message did not land.
disable-model-invocation: true
---

# wait-what

Stop. Re-pitch where things stand.

## Rules

1. Short context only — what we are doing and why it matters now
2. ASD-STE100 Simplified Technical English (short sentences, controlled vocabulary)
3. If `CONTEXT.md` (and linked knowledge concepts) exist, use those terms — do not invent synonyms; otherwise use the project’s established language
4. No new decisions, no implementation, no expanding scope

**Done when:** the user can restate the current position in one sentence.
