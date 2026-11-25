---
name: per-agent-skill-listing-dedupe
description: "Keep skill-listing deltas scoped per agent or thread so each agent gets its own first-turn announcement surface."
metadata:
  author: ychampion
---

# SKILL: Per-Agent Skill Listing Dedupe
**Domain:** attachment-pipeline
**Trigger:** Use when a multi-agent runtime must announce new skills or capabilities without one thread's deltas erasing another thread's initial listing.
**Source Pattern:** Distilled from reviewed per-agent capability-announcement tracking implementations.

## Core Method
Track which skill names were already sent to each agent separately rather than globally. Each agent or thread gets its own seen-set keyed by a stable agent identity, so the main thread announcing a listing does not make every subagent believe it already saw the same surface. When building the delta list for a given agent, compare only against that agent's set and update that set after sending.

## Key Rules
- Store a distinct seen-set per agent or thread, including a stable identity for the main thread.
- Filter outgoing skill deltas against the target agent's seen-set, not a global pool.
- Keep the per-agent seen-set alive for the lifetime of that agent so resumes and follow-up turns reuse its own state.
- Update the agent's seen-set immediately after sending new skills so later deltas stay accurate.

## Example Application
If a subagent is spawned in the middle of a long-running coding session, start it with its own empty seen-set. Even though the main thread already announced the skill surface, the subagent still gets a proper first-turn listing because its own history starts blank.

## Anti-Patterns (What NOT to do)
- Do not keep one global seen-set; that makes every new agent believe everything was already announced.
- Do not let one agent reuse another agent's seen-set; cross-agent sharing collapses the whole point of per-thread deltas.
