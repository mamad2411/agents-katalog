---
name: hermes-insight
description: Use when debugging, planning, or a pattern may recur.
version: 0.9.3
author: Pablo Navarro (PabloTheThinker), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [cognition, pattern-recognition, experience, planning, learning, memory]
    category: cognition
    related_skills: []
    requires_toolsets: [hermes_insight]
---

# Hermes Insight

You are a Hermes agent. Insight is your **local retrieve-and-recognize organ**.
It is not a `MemoryProvider`, not MEMORY.md, not a chat dump, and not proof that
a rhyme is causal.

The lattice stores **structures** (rules, events, tasks, facts) and **links**.
Query it before inventing a root cause. Write back only what you actually learned.

## When to Use

- Hard debugging, architecture, operations, or tool-routing.
- A failure, correction, or workflow looks familiar.
- Multi-step work should teach the next session.
- Workspace, tools, or service state just changed.
- At least three distinct tasks may hide a reusable workflow.

Do not use for trivia, one-step deterministic actions, bulk chat logging, or as
evidence that a weak analogy is true.

## Prerequisites

- The `hermes-insight` plugin is enabled; `insight_*` tools exist.
- `insight_stats` shows the intended agent id, database path, and version.
- One database per profile or client. Never share a writable lattice.
- Never pass credentials, private keys, or unrestricted transcripts.

If the tools are missing, tell the user to install the plugin and restart Hermes.
Do not invent results or fall back to another memory store.

## How to Run

```text
skill_view(name="hermes-insight")
insight_stats()
insight_perceive(situation="<what you see>", observations=["<error or fact>"])
```

Mental model and pack keys:
`skill_view(name="hermes-insight", file_path="references/HOW-IT-WORKS.md")`

Ontology, install, examples:
`skill_view(name="hermes-insight", file_path="references/AGENT-GUIDE.md")`

## How It Works

```text
observe → recall → perceive → plan → task / events → credited close → learn
  state    memory    shape     route     evidence         credit       recurrence
```

For you, that means:

1. **`insight_recall(query=...)`** returns a **budgeted working set** — rules,
   facts, echoes, hops, contradictions — plus `usable`. It does not dump MEMORY.md
   or the lattice.
2. **`insight_perceive(situation=...)`** names the shape: `lever`, top rule,
   `action_hint`, `usable`. Recognized rules harvest bound events as **`dots`**.
   Repeated dots grow local Hebbian **`pathways`**. Those are `sequence`
   candidates, never published Hermes skills (`automatic_skill_write=false`).
3. **`insight_plan(situation=...)`** ranks routes by relevance plus **explicit**
   applied outcomes. Similarity is not credit.
4. **`insight_task(action="close", used_pattern_ids=[...])`** is the only write
   of `applied` credit. Recalling or recommending a pattern does not count.

If `usable=false`, gather two or three concrete observations and perceive again.

## Quick Reference

| Tool | You use it to |
|---|---|
| `insight_perceive` | Name the shape — lever, rule, echoes, `dots`, `pathways` |
| `insight_recall` | Retrieve a working set before acting |
| `insight_attune` | Set the trait plate (not a diagnosis) |
| `insight_remember` | Store one compact fact / pointer |
| `insight_plan` | Rank a route with reliability + environment |
| `insight_observe` | Snapshot the workspace or log a typed event |
| `insight_task` | Open/close a task; credit only applied ids |
| `insight_experience` | Catalogue a decision, failure, or fix |
| `insight_learn` | Mine recurrence across distinct tasks |
| `insight_feedback` | Strengthen or weaken a known pattern |
| `insight_hygiene` | Decay noise; densify structural links |
| `insight_cycle` | Deeper pass on a novel, substantive scene |

## Procedure

1. **Ground.** After a material workspace change:
   `insight_observe(mode="environment", root="<workspace>")`.
2. **Recall, then perceive.**
   `insight_recall(query="...", observations=[...])` when you need priors.
   Then `insight_perceive(situation="...", observations=[...], log=true)` with
   component names, exact errors, and an optional `domain`. Read `usable`,
   `lever`, top score, top rule, `dots`, and `pathways` before acting.
   `insight_remember(claim="...", pointer="user.md#heading")` for one durable
   fact — never a chat log.
3. **Refuse thin structure.** `usable=false` means gather observations, not a
   root-cause story.
4. **Plan consequential work.**
   `insight_plan(situation="...", observations=[...])`. Read primary route,
   explicit success/failure counts, environment fingerprint, verify, rollback.
5. **Open a task.**
   `insight_task(action="open", name="...", goal="...")` — keep `task_id`.
6. **Leave evidence.** Typed tool/skill transitions:
   `insight_observe(mode="event", event_type="...", task_id=..., tool=... or skill_id=..., status=..., outcome=...)`.
   Human-readable beats: `insight_experience(title="...", body="...", task_id=...)`.
7. **Execute and verify.** Follow the route. Completion needs an observable
   result, not a missing exception.
8. **Close with honest credit.**
   `insight_task(action="close", task_id=..., outcome="...", summary="...", used_pattern_ids=[...])`.
   Only ids you actually applied.
9. **Induce after enough tasks.**
   `insight_learn(materialize=false)` after ≥3 comparable tasks. Inspect support,
   outcomes, counterexamples, Wilson bound, lifecycle.
10. **Materialize cautiously.** `insight_learn(materialize=true)` writes a local
    `sequence` for review. It never writes or executes a Hermes skill.

Promote to a Hermes skill only when lifecycle is `verified_local`, the user
reviews it, and you respect the skill write-approval gate. Then start a new
session so the skill index can see it.

## Pitfalls

- **Similarity is not causality.** A high score still needs observation.
- **Selection is not application.** Do not put untried ids in `used_pattern_ids`.
- **One task is not recurrence.** Repeats inside one `task_id` count once.
- **Success-only memory overfits.** Keep failures and counterexamples.
- **A pathway is not a skill.** Grown sequences stay local candidates.
- **Environment drift invalidates precedent.** Snapshot after material change.
- **Shared databases cross trust boundaries.** One DB per profile/client.
- **Raw telemetry is a liability.** Store structure and artifact pointers.

## Verification

- `insight_stats` reports this profile and a writable local database.
- A concrete perceive/recall is usable; a vague query returns `usable=false`.
- `insight_remember` stores one fact that `insight_recall` can retrieve.
- `insight_plan` shows the current snapshot and separates relevance from reliability.
- Closing with real `used_pattern_ids` changes explicit outcome evidence.
- Three identical traces in one task produce no workflow candidate.
- Three or more distinct tasks can produce a `candidate`; only the evidence gate
  can produce `verified_local`.
- `insight_learn` always reports `automatic_skill_write=false` and
  `automatic_execution=false`.
