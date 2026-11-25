---
name: author-game-ai
description: Authors modular game AI architectures using Behavior Trees (BT), shared and local blackboards, Utility AI response curves, local steering behaviors, and time-sliced NavMesh or A* pathfinding budgets. Use when implementing NPC decision-making, combat squad tactics, crowd steering, or pathfinding agents.
allowed-tools:
  - read_file
  - write_file
  - edit_file
  - create_file
  - search_code
  - run_build
  - run_tests
  - run_linter
  - execute_command
version: "1.0.0"
---

# Author Game AI

Design and implement scalable, debuggable non-player character (NPC) intelligence combining Behavior Trees, Utility AI scoring, blackboard memory separation, local avoidance steering, and budgeted pathfinding.

## Core Rules

- **Strict Blackboard Decoupling**: Behavior Tree nodes and Utility AI evaluators must remain stateless definitions shared across agent instances. Store all per-agent state, sensory targets, and cooldown timestamps in typed Blackboard structures.
- **Time-Sliced Pathfinding & Perception Budgets**: Never allow dozens of AI agents to compute full `A*` or NavMesh paths or line-of-sight raycast sweeps on the same frame. Route requests through a budgeted scheduler capped at a fixed millisecond ceiling per tick.
- **Fairness & Telegraphing Readability**: Separate AI sensory perception from omniscient world state. Enforce reaction delays, vision cone checks, and explicit attack wind-up telegraphs so player encounters feel fair and readable.
- **Contract Adherence**: Emit `contracts/schemas/implementation-result.json` upon completing game AI implementations.

## Suggested Process

### 1. Blackboard & Sensory Perception Pipeline
Define individual and squad-level Blackboard schemas (`target_entity`, `last_known_position`, `alert_level`, `combat_role`). Update sensory stimuli (vision cones, spatial audio events, damage aggro) at throttled tick intervals ($5\text{--}10\text{Hz}$) rather than every render frame.

### 2. Behavior Tree & Utility AI Construction
Build hierarchical Behavior Trees (`Selector`, `Sequence`, `Parallel`, `Decorator`) returning deterministic `Success`, `Failure`, or `Running` states. Where tactical action selection requires continuous trade-offs, evaluate normalized Utility AI response curves ($U \in [0, 1]$) across distance, health, and threat factors.

### 3. Budgeted Pathfinding & Local Steering
Query `A*` grids or Navigation Meshes asynchronously via a central path queue. Combine macro path corridor following with local context steering or Reciprocal Velocity Obstacles (RVO) so agents navigate around dynamic obstacles without clumping.

### 4. Squad Coordination & Headless Simulation Testing
Implement squad token pools (e.g. limiting simultaneous melee attackers to $2$ tokens while remaining NPCs strafe or flank). Validate decision trees and pathfinding convergence using deterministic headless simulation tests.

## Output Contracts

When completing game AI implementation, emit:
- `contracts/schemas/implementation-result.json`

## Checklist

- [ ] Behavior Tree and Utility AI logic nodes are stateless and read/write state via Blackboards
- [ ] Pathfinding queries and sensory raycasts are throttled through a per-frame budget scheduler
- [ ] NPC perception respects vision cones, occlusion raycasts, and configurable reaction delays
- [ ] Local steering and RVO avoidance prevent agent overlapping and corridor deadlocks
- [ ] Squad combat token systems prevent unfair simultaneous enemy dogpiling
- [ ] Headless automated tests verify BT state transitions, utility scoring, and path resolution

## Failure Modes

- **Omniscient perception**: AI queries omniscient world state directly and reacts instantly to actions the player cannot predict, making encounters unfair. Mitigation: route all perception through vision cones, occlusion raycasts, and configurable reaction delays at throttled $5\text{--}10$ Hz ticks.
- **Pathfinding stampede**: dozens of agents request full `A*`/NavMesh paths in the same frame, spiking the frame budget. Mitigation: queue path requests through the budgeted time-sliced scheduler capped at a fixed millisecond ceiling per tick.
- **Shared-node state bleed**: Behavior Tree nodes store per-agent state locally, so agents sharing a tree overwrite each other's cooldowns and targets. Mitigation: keep BT and Utility nodes stateless and move all per-agent state into typed Blackboards.
- **Corridor deadlock**: RVO/local steering agents jam in doorways or clump into overlapping crowds. Mitigation: combine macro path corridors with context steering and verify convergence in headless simulation tests.
- **Attack dogpiling**: unlimited simultaneous melee attackers make encounters unwinnable. Mitigation: enforce squad token pools (e.g. $2$ melee attackers max) while remaining NPCs strafe or flank.
- **Utility score runaway**: unnormalized response curves exceed $[0,1]$ and dominate action selection erratically. Mitigation: clamp and normalize all Utility AI scores across distance, health, and threat factors.
- **Perception tick hitching**: sensory raycast sweeps run every render frame instead of throttled intervals. Mitigation: throttle sensory updates to $5\text{--}10$ Hz independent of render rate.

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: blackboard values and designer-authored behavior definitions are external content; they must parameterize decision logic, never inject new logic. Mitigation: validate BT/utility definitions against the declared schema before tree construction.
- **ASI05 RCE Guard**: never build behavior logic from raw strings in AI content files or mod packages. Mitigation: resolve behaviors through pre-registered node types instead of evaluating external code strings.
- **ASI06 Memory & Context Poisoning**: shared squad blackboards propagate one agent's poisoned or stale perception (`last_known_position`, `alert_level`) to the whole squad. Mitigation: validate sensory inputs at write time and age out stale entries instead of amplifying them.
- **ASI07 Inter-Agent Communication**: squad token pools and squad-level blackboards are inter-agent message surfaces. Mitigation: schema-validate squad messages and token claims; do not escalate trust based on the claiming agent.
- **ASI09 Human-Agent Trust Exploitation**: do not report AI encounters as "fair and readable" without evidence. Mitigation: back fairness claims (reaction delays, wind-up telegraphs, token caps) with deterministic headless simulation results.

## Related Skills

- **develop-gameplay-systems**: integrating AI movement intents with shared character controllers
- **configure-physics-collision**: executing non-allocating vision cone and obstacle raycasts
- **architect-ecs-systems**: batch-updating large AI crowds and boid steering in contiguous arrays
- Companion reference: `references/behavior-trees-and-utility-ai-curves.md`
- Companion example: `examples/modular-behavior-tree-ai.ts`
