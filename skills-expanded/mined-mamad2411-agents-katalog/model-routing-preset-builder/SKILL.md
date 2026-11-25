---
name: model-routing-preset-builder
description: Use when someone wants to create, clone, explain, or customize a portable Codex model-routing preset based on their available models, preferred quality, speed, usage budget, agent roles, capabilities, fallbacks, and human gates.
---

# Model Routing Preset Builder

Build a compact, reviewable routing preset instead of scattering topology,
model, effort, and lifecycle choices across prompts and agent files. Start from
an example, then make every deviation explicit.

## Build

1. Inventory models and efforts per `current_task`, `spawn_agent`, and
   `create_thread` channel. Inventory roles, skills, controls, and compute modes.
   Mark unverified entries unavailable.
2. Ask for preferences on speed, quality, cost/usage, master coordination,
   planning, Fleet work, field coordination, delegated subtasks, independent
   parallel tasks, review, memory work, and exceptional compute.
3. Copy either `assets/vitor-opinionated.toml` or
   `assets/neutral-balanced.toml`. Never edit the bundled example in place.
4. Adjust profiles and role defaults without duplicating the route algorithm.
   Keep reader-facing `Light` mapped to TOML `low`. Keep custom role TOML free
   of model/effort pins unless the operator intentionally wants an immutable binding.
5. Record capability requirements by stable names, not local filesystem paths.
6. Validate with the sibling `model-capability-router` script:

```bash
python3 <model-capability-router>/scripts/route.py validate --preset <preset.toml>
```

7. Show the topology matrix, role defaults, Fleet fan-out and ceiling, logical
   task relationships, and operator-only gates. Ask the operator to approve the
   preset before it becomes a default.

## Required Topologies

Cover `single`, `direct_subagent`, `direct_fleet`, `field_coordinator`,
`field_fleet`, `delegated_subtask`, `parallel_task`, `max_single`, and
`ultra_auto`. A delegated subtask is a user-owned platform peer with a logical
parent. A parallel task is user-owned and independent. Start Fleets with two or
three workers and set a ceiling no higher than eight.
Treat that ceiling as policy only: runtime routing must also account for the
live capacity and already-active children. Define `field_fleet` as a second
stage over an existing verified field coordinator, not as simultaneous creation
and delegation.

## Gates

`max` and `ultra` remain operator-authorized modes. A preset may describe when
they help, but must not select them automatically. Capabilities that mutate the
host, access secrets, deploy, publish, spend money, or cross accounts require an
explicit gate independent of model choice.

## Completion Contract

Return the preset path, its base example, every changed topology/profile/role,
unavailable channel selections, capability gaps, validation result, and
approval status.
