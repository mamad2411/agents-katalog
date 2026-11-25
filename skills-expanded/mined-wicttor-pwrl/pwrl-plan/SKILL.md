---
name: pwrl-plan
description: "Create structured implementation plans with three tiers (Fast/Standard/Deep). Pure skill pipeline orchestrator—no agent routing."
argument-hint: "[task description, requirements doc, or goal to plan]"
---

# PWRL Plan — Pure Skill Orchestrator

Create durable implementation plans that can be handed off for execution. Orchestrates a deterministic pipeline of micro-skills: scope → research → design → generate. No agent dependency, no fallback paths.

## Purpose

Plans capture decisions, structure, and approach before execution. They enable:

- Clear scope and success criteria
- Identified risks and dependencies
- Concrete implementation units with acceptance criteria
- Knowledge reuse through related learnings
- Confidence that work won't go off the rails

## Core Workflow: Four-Phase Pipeline

```
INPUT (task description)
  ↓
PHASE 1: Scope (pwrl-plan-scope)
  → Gather context, validate domain, bootstrap requirements
  → Output: Scoped context artifact
  ↓
PHASE 2: Research (pwrl-plan-research)
  → Discover patterns, identify risks, recommend external research
  → Output: Research findings artifact
  ↓
PHASE 3: Design (pwrl-plan-design)
  → Decompose into units, map dependencies, assess complexity
  → Output: Design artifact with unit decomposition
  ↓
PHASE 4: Generate (pwrl-plan-generate)
  → Select tier, render plan, embed learnings, save to docs/plans/
  → Output: Final plan document saved to file
  ↓
OUTPUT (plan file ready for execution)
```

## Phase Summary

Each phase is orchestrated sequentially: the orchestrator calls the micro-skill, receives the output artifact, validates it with a quality gate, and passes it to the next phase.

**Phase 1: Scope** ([pwrl-plan-scope](../pwrl-plan-scope/SKILL.md)) — Gather context, validate domain, set interaction mode. Output: Scoped context artifact.

**Phase 2: Research** ([pwrl-plan-research](../pwrl-plan-research/SKILL.md)) — Discover tech stack, local patterns, and risk areas. Output: Research findings artifact.

**Phase 3: Design** ([pwrl-plan-design](../pwrl-plan-design/SKILL.md)) — Decompose into units, map dependencies, assess complexity. Output: Design artifact with unit decomposition.

**Phase 4: Generate** ([pwrl-plan-generate](../pwrl-plan-generate/SKILL.md)) — Select tier, render plan, embed learnings, save to `docs/plans/`. Output: Final plan document.

**Quality Gates:** Run `/pwrl-phase-checkpoint plan N [artifact-path]` to validate each phase. See [pwrl-phase-checkpoint](../pwrl-phase-checkpoint/SKILL.md) for validation rules.

### Interaction Mode Propagation

Interaction mode (`detailed | smart | yolo`) is set in Phase 1 (via `pwrl-plan-scope` Step 1.5) and read at the start of each subsequent phase. Determines whether confirmation steps execute or are skipped. The three modes behave as follows:

- **`detailed`** — Pause at every phase transition; show generated artifacts; require explicit approval to proceed.
- **`smart`** — Phases run automatically; pause only when the next phase produces a HIGH-risk operation. v1 simplification: behaves like Yolo with a single confirmation prompt at workflow start.
- **`yolo`** — Every phase runs automatically; only the final outcome is reported.

**Exception:** Error recovery steps always pause the pipeline, regardless of mode. See the canonical pattern in `docs/learnings/pattern/interaction-mode-three-mode-propagation-2026-06-29.md`.

## Planning Tiers

| Tier         | Best For                           | Files | Risk | Time      |
| ------------ | ---------------------------------- | ----- | ---- | --------- |
| **FAST**     | Bug fixes, small tweaks            | 1-3   | LOW  | 5-15 min  |
| **STANDARD** | Most features                      | 4-8   | MED  | 30-45 min |
| **DEEP**     | Architecture, security, migrations | 9+    | HIGH | 1-2 hours |

**See** [references/planning-tiers.md](references/planning-tiers.md) for full tier decision criteria and template examples.

## Core Principles

- **Deterministic Pipeline:** Phases always execute in sequence: scope → research → design → generate (no agent switching, no fallback paths). Conditional pauses for error recovery (e.g., circular dependencies, ambiguous tier selection) are expected error handling, not branching.
- **Focus on Decisions:** Capture approach, structure, risks, and sequencing (not code simulation)
- **Right-Size:** Small tasks → short plans; complex work → more structure
- **Separate Planning from Execution:** Don't simulate implementation during planning
- **Be Concrete:** Use specific files, components, and dependencies
- **Stay Portable:** Use repository-relative paths only
- **Transparent Artifacts:** Each phase produces explicit output artifact for next phase
- **Interaction Mode Propagation:** Once set in Phase 1, interaction_mode (detailed, smart, or yolo) is read at the start of each subsequent phase and determines whether confirmation steps execute. See `docs/learnings/pattern/interaction-mode-three-mode-propagation-2026-06-29.md` for the full contract.

## Error Handling & Recovery

**Philosophy:** Fail explicitly, not silently. Each phase has clear error handling with recovery suggestions.

**See:** [references/error-handling.md](references/error-handling.md) for comprehensive error recovery workflows across all phases, including circular dependencies, tier ambiguity, missing directories, filename collisions, and resume operations.

## Key Outputs

Each plan includes (tier-dependent):

- **Problem & Scope:** Clear problem frame and intended behavior
- **Success Criteria:** 1-3 specific conditions for completion
- **Implementation Units:** Named U-IDs with dependencies, files, approach, and acceptance criteria
- **Related Learnings:** Linked learning files with applicability notes (STANDARD/DEEP)
- **Learning Gaps:** Areas needing post-implementation documentation (DEEP)
- **Tier-Specific Sections:** Risk analysis, alternatives, rollout notes (STANDARD/DEEP)

## Interaction Method

- Use platform's `ask_user_question`, `ask_user`, `ask_user_input`, `vscode/askQuestions` or any available extension/tool for user interaction for all decisions
- Ask one question at a time
- Use multiple-choice questions when possible
- If input is empty, ask: "What would you like to plan? Describe the task or project."
- Provide clear recovery suggestions when errors occur

## Architecture

```
pwrl-plan orchestrator
├── 1. Call pwrl-plan-scope → get scope artifact
├── 2. Call pwrl-plan-research → get research artifact
├── 3. Call pwrl-plan-design → get design artifact
└── 4. Call pwrl-plan-generate → save plan file
```

**Benefits:**

- ✅ Simpler to understand (single code path)
- ✅ Easier to test (no branching logic)
- ✅ More maintainable (micro-skills independently testable)
- ✅ More composable (micro-skills reusable in other workflows)
- ✅ Better error handling (explicit at each phase)

## Micro-Skill References

- [pwrl-plan-scope](../pwrl-plan-scope/SKILL.md) — Context & scope gathering
- [pwrl-plan-research](../pwrl-plan-research/SKILL.md) — Pattern discovery & risk identification
- [pwrl-plan-design](../pwrl-plan-design/SKILL.md) — Unit decomposition & dependency mapping
- [pwrl-plan-generate](../pwrl-plan-generate/SKILL.md) — Plan rendering & file generation

## Related Documentation

- [references/planning-tiers.md](references/planning-tiers.md) — Tier definitions and decision criteria
- [docs/guides/micro-skill-patterns.md](../docs/guides/micro-skill-patterns.md) — How to extend with new micro-skills
- [docs/guides/architecture-refactoring.md](../docs/guides/architecture-refactoring.md) — Rationale for refactoring

## Frequently Asked Questions

**Q: What if a phase fails? Can I skip it or retry?**

A: Yes. Each phase has explicit error handling with recovery suggestions. You can retry, provide clarification, modify scope, or abort. No silent failures.

**Q: Can I use just one micro-skill (e.g., only generate from design)?**

A: The orchestrator expects to call all four phases in sequence. If you want to use a single micro-skill, call it directly by name: `/pwrl-plan-scope`, `/pwrl-plan-design`, etc.
