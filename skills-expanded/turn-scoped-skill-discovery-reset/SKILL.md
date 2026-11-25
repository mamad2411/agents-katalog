---
name: turn-scoped-skill-discovery-reset
description: "Reset per-turn skill discovery tracking so long-lived sessions don\u2019t leak outdated discovery flags while still honoring already-known skills."
metadata:
  author: ychampion
---

# SKILL: Turn Scoped Skill Discovery Reset
**Domain:** command-surfaces  
**Trigger:** Use when the conversation engine needs to clear the list of discovered skills at the start of each new turn so repeated invocations stay accurate.
**Source Pattern:** Distilled from reviewed command-surface and listing-control patterns.

## Core Method
Tie skill discovery tracking to the turn boundary: clear `discoveredSkillNames` right before each `submitMessage` turn, and feed the cleared set into `ask()` so the next turn can rediscover only what emerges afresh despite previously cached suggestions. Persist the cleared set long enough for telemetry but don’t let it grow across turns, ensuring each new user turn begins with an empty discovery set.

## Key Rules
- Maintain a Set of discovered skill names per turn inside QueryEngine, clearing it at the earliest point the new turn begins.
- When a skill is rerun via a forked agent, note that separately but do not carry it over to the global set; the turn-level set should reset regardless of agent-internal events.
- Emit telemetry about the cleared set proactively so analytics can compare discovery counts; do not reuse the old set except for logging.
- Keep the discovery reset outside of compaction retries so the next turn still respects the trimmed context.

## Example Application
In a long-running Claude Code session, apply this skill when you implement a subagent and need the parent conversation to treat each user message as if it's discovering skills anew, avoiding stale recommendations or double-counted discovery telemetry.

## Anti-Patterns (What NOT to do)
- Do not let `discoveredSkillNames` accumulate over turns; that dilutes new discovery signals and leads to misleading telemetry.
- Do not clear the set mid-turn; it must stay stable until the next `submitMessage` call ends so the current turn can honor discovery gating.
