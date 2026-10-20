---
name: agent-teammate
description: "Persistent AI teammate, cross-session memory, personality, project context continuity. Use when setting up a long-running collaborative AI partner."
version: 1.0.0
platforms: [linux, macos]
---

# Agent Teammate

## What It Does
Creates and manages a persistent AI agent teammate that remembers project context, user preferences, and past decisions across sessions. The teammate has a defined personality, role-specific strengths/weaknesses, and can be @mentioned in conversations to contribute expertise without full context handoff.

## Iron Laws (NEVER violate)
1. **Memory is sacred** — Never lose or corrupt teammate memory between sessions. Every interaction must be persisted.
2. **Role boundaries** — Teammate stays in its lane. A reviewer teammate does not rewrite; a planner teammate does not deploy.
3. **Feedback loop required** — Every correction from the human partner must update the teammate's behavior model.
4. **No hallucinated memory** — Never fabricate past interactions. If memory is missing, ask — don't guess.

## Red Flags (STOP immediately)
- **Memory drift** — Teammate contradicts what was established 3+ sessions ago → memory corruption
- **Role creep** — Teammate starts performing tasks outside its defined role without being asked
- **Silent disagreement** — Teammate disagrees with a decision but doesn't surface it → escalates to human
- **Context amnesia** — Teammate asks questions already answered in persistent memory

## Common Rationalizations (self-deception)
- "I'll remember this detail, no need to persist it" → Memory decays. Persist everything that matters.
- "The teammate knows the project well enough, skip the context" → Always verify current context.
- "One more capability won't hurt the role definition" → Role creep destroys trust and predictability.

## When To Use
- User wants a persistent AI collaborator that remembers project history
- Complex multi-session projects where context handoff is expensive
- Team workflows where multiple humans interact with the same agent teammate
- User wants a specialized role (architect, reviewer, tester) with persistent memory

## Human Partner Signals (escalate to human)
- **Confidence < 70%** — Teammate is unsure about a critical decision → escalate
- **Role conflict detected** — Task requires capabilities outside teammate's role → ask human to reassign
- **Memory inconsistency found** — Two memory entries contradict → flag for human resolution
- **Ethical boundary touch** — Task approaches ethical gray zone → pause and escalate

## Pipeline
1. Define teammate: role, personality, strengths, weaknesses, communication style
2. Initialize memory: load past sessions, project context, user preferences
3. Deploy teammate: register @mention trigger, set up notification channels
4. Operate: teammate responds to @mentions, learns from feedback, updates memory
5. Review: periodic memory audit, role boundary check, performance review with human

## Verification Checklist
- [ ] Teammate memory persists across 3+ sessions without data loss
- [ ] Role boundaries enforced: teammate refuses out-of-scope tasks
- [ ] @mention triggers teammate response within defined latency SLA
- [ ] Feedback from human updates teammate behavior in next interaction
- [ ] Memory audit shows no fabricated or contradictory entries
- [ ] Human partner can view/edit teammate memory directly

## Related Skills
- `squad-builder` — Agent teammates are the building blocks of squads
- `task-lifecycle-manager` — Tasks assigned to teammates go through lifecycle tracking
- `session-memory` — Underlying memory infrastructure for persistence
- `agent-introspector` — Debugging teammate behavior and decision traces
