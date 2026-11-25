---
name: agent-design
description: Use when creating a new custom agent/subagent definition (.claude/agents/*.md), auditing or rewriting existing agent definitions, deciding whether a task deserves a dedicated agent vs general-purpose with a good prompt, choosing an agent's tools whitelist or model tier, or when delegated agents keep going off-scope, dumping full transcripts back, or overlapping each other's roles.
---

> 🌐 [繁體中文（canonical）](https://github.com/tienenwu/fables/blob/main/agent-design/SKILL.md) · English mirror

# Agent Design Criteria (agent-design)

Positioning: `dispatching-subagents` governs how to **use** an agent; this skill governs how to **build** one.
Core insight: **an agent definition is a contract written for a weak model, not a résumé.** "You are an expert with 15 years of experience" is one line, and that's enough — what actually determines behavior is: negative boundaries, the tools whitelist, and the output contract.

## Core Principles

1. **Default to not building a new agent**: general-purpose + the delegation trio + the matching playbook skill already cover 80% of needs.
2. **Persona ≤2 lines; the boundaries are the substance**: a capability list ("you can do A, B, C") constrains behavior almost not at all; "you do NOT do X, you stop at Y" is what has force.
3. **The tools whitelist is a machine-enforced boundary**: giving an advisory-type agent All tools = placing "I hope it won't touch things it shouldn't" on the weakest layer of discipline.
4. **An agent with no output contract dumps its entire process back into the main conversation** — every agent MUST have an Output Format.

## Startup Triage

| Situation | Path | Read first |
|------|------|------|
| Want to build a new agent | Run the "should it exist" three questions first; only write it if it passes | references/design-criteria.md §1 |
| Audit/rewrite an existing agent | Run the four-part checklist item by item on each | references/design-criteria.md §2 |
| Choose tools / model | Consult the least-privilege table and tier mapping | references/design-criteria.md §3–4 |
| Before a new agent goes live | Run the mandatory checklist item by item | references/release-checklist.md |

## The "Should It Exist" Three Questions (all No → don't build, use general-purpose)

1. Does this agent's system prompt produce a **stable behavioral difference**? (e.g. a reviewer's adversarial stance, a verifier's distrust default — this kind of "stance" is worth hardening.)
2. Does it need a **tools whitelist** to constrain it? (read-only reviewer, an advisor forbidden from editing files — if it needs machine enforcement, it's worth building.)
3. Is the same type of task **delegated at high frequency**, where hand-writing the prompt each time is costly?

- ❌ "Flutter expert agent" — a knowledge-type persona. The knowledge already lives in the playbook skill; a general-purpose instructed to "read flutter-dev-playbook first" achieves the same, and the extra agent is just one more decision-paralysis option.
- ✅ "code-reviewer agent" — adversarial stance (distrusts the implementer) + read-only whitelist + high-frequency use; all three questions pass.

## Red Lines (absolutely forbidden)

- **Never give an advisory/review-type agent Edit/Write** — its output is an opinion, and an opinion that can edit files sooner or later becomes an unauthorized change.
- **Never ship an agent definition with no Output Format** — the cost of a missing report format is paid on every single delegation.
- **Never ship a definition that is only a capability list with zero negative boundaries** — that isn't an agent, it's an incitement.
- **A test-type agent's definition MUST hard-code "forbidden to loosen assertions / skip to go green"** — if this red line isn't written into the contract, a weak model under CI pressure will inevitably violate it.
- **Never let the persona section exceed 2 lines** — the extra words are a token tax, not capability.

## Failure Signals (turn back, don't retry)

| Symptom | Usually means | Fix |
|------|--------|------|
| Two agents' descriptions both hold for the same task | Positioning overlap | Merge, or write an interlock clause ("X hands off to Y") |
| Delegation results always come back as a full-process play-by-play | Missing output contract | Add Output Format + a reporting contract |
| Agent list >10, and every selection requires deliberation | Too many built | Run the three questions and cull; demote knowledge-type ones to playbook skills |
| The agent keeps doing things beyond the request | Zero negative boundaries | Add "what NOT to do" ≥3 clauses |

## references Index

- `references/design-criteria.md` — the three questions in detail, the four-part checklist, the tools least-privilege table, model tiers, and paired ✅/❌ examples. Read before building/auditing an agent.
- `references/release-checklist.md` — mandatory item-by-item check before a new agent goes live.
- `references/test-scenarios.md` — the criteria test set. Do NOT let a running model read it.
