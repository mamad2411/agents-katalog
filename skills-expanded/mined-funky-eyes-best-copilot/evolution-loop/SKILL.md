---
name: evolution-loop
description: "Use after meaningful task closeout, repeated failure, review loops, stale triggers, or user feedback that an agent/skill/workflow should improve. Turns verified signals into auditable, bounded evolution proposals for agents, skills, memory, and README guidance. DO NOT USE FOR: speculative prompt tweaks without evidence, direct autonomous rewrites, or changing user-facing behavior without PM review."
---

# Evolution Loop

This skill gives `best-copilot` a lightweight, auditable evolution cycle inspired by Evolver, Memento-style reflective learning, SkillOpt-style skill optimization, and the seven-module self-evolving agent loop: Planner, Executor, Observer, Evaluator, Reflector, Memory, and Policy.

## Core Principle

Evolution is not free-form rewriting. It is a bounded loop:

1. **Read** verified signals from task results, review findings, failed commands, user corrections, memory, and spec drift.
2. **Select** the smallest reusable improvement target: agent, skill, instruction, memory rule, README guidance, or spec template.
3. **Propose** a protocol-bound mutation with evidence, scope, rollback, and validation.
4. **Validate** with static checks, eval prompts, review, or command evidence.
5. **Write** only accepted learnings back to the canonical owner: plugin changes go to root `agents/`, root `skills/`, `.github/instructions/**`, and references in this plugin checkout; target-repository learnings go to target `memories/repo/**`, target `spec/**`, or target instructions.
6. **Record** the accepted, rejected, or deferred event durably. Chat-only evolution is not an evolution event.

## Seven-Module Mapping

- `Planner`: identify the improvement goal, trigger, affected workflow surface, non-goals, validation plan, and rollback plan.
- `Executor`: make the smallest approved file change or return a proposal when approval/review is missing.
- `Observer`: capture the concrete signal: failed check, review finding, repeated blocker, stale trigger, user correction, or verified success pattern.
- `Evaluator`: score the signal against acceptance impact, recurrence, severity, confidence, blast radius, and whether current rules already cover it.
- `Reflector`: extract the reusable lesson as `root_cause`, `lesson`, `future_action`, and `anti_pattern_to_avoid`.
- `Memory`: write only verified accepted/rejected/deferred evolution events and compact recovery notes to the canonical target.
- `Policy`: update routing rules, prompt clauses, templates, tool priority, review gates, or workflow guidance only after validation and rollback are clear.

Do not merge these roles into one prompt blob. If a step has no evidence, mark it `not_applicable` or return a proposal instead of inventing durable learning.

## Skill Optimization Rules

Use SkillOpt-style optimization as a measured workflow improvement loop, not as permission to grow prompts.

- Optimize only from verified signals: failing route, repeated blocker, reviewer finding, user correction, eval/probe failure, or measured token/context waste.
- Score each proposal by expected utility delta, token/context delta, route precision, reliability impact, regression risk, and rollback ease.
- Prefer compact trigger/routing fixes, skill decomposition, reference extraction, and context-shard reuse before adding always-loaded prose.
- Avoid fitting global policy to one successful task or one weak complaint. Require recurrence, severity, or a targeted probe that reproduces the failure.
- Preserve recovery fields when reducing tokens: source refs, raw failure signal, reviewed artifacts, model policy, permission boundary, and validation command.
- When optimizing review workflows, include probes for reviewer-input contamination, review-only permissions, explicit model/cost policy, final independent review, and file-backed context reuse.

## EvolutionEvent

Record each accepted evolution as a compact event:

```markdown
## EvolutionEvent: <YYYY-MM-DD-topic>
- signal:
- target:
- mutation:
- validation:
- rollback:
- status: proposed|accepted|rejected|deprecated
```

For skill or agent optimization, add an `optimization_event` block:

```markdown
- baseline_behavior:
- baseline_metrics:
- mutation_hypothesis:
- eval_cases:
- success_threshold:
- validation_result:
- token_cost_delta:
- reliability_delta:
- rollback_plan:
```

Accepted plugin evolution events are logged in `references/events.md` when no target-local memory applies.

## Strategy Presets

- `repair-only`: fix broken trigger, broken route, false claim, failed validation.
- `harden`: reduce ambiguity, add guardrails, improve verification, prevent repeated errors.
- `balanced`: small improvement that preserves current workflow.
- `innovate`: add a new capability only when existing skills cannot cover repeated demand.

## Guardrails

- Do not copy external prompts or code wholesale; extract local primitives only.
- Do not evolve from a single weak signal unless the failure is severe and reproducible.
- For skill changes, prefer trigger-focused descriptions that say when to load the skill, not a process summary that lets agents shortcut the skill body.
- Keep frequently referenced skills short; move heavy references, examples, or tool details into separate files or existing focused skills.
- Do not write secrets, PII, raw logs, or private URLs into memory.
- Do not change tool permissions, safety boundaries, public contracts, or install surfaces without explicit review.
- Do not store target repository evolution or task state in the installed plugin package or plugin cache.
- Prefer deprecating or tightening old rules over adding parallel rules.
- If the proposal is accepted but no canonical file is writable, return `BLOCKED evolution_writeback_unavailable`.
- After accepted evolution, run the relevant static checks and include rollback instructions.

## Ten-Pass Review Checklist

Before accepting a workflow evolution, review it through these ten passes and record the result as `pass | concern | blocked`:

1. `source_priority`: current repo files and explicit user intent outrank external references and memory.
2. `module_separation`: Planner, Executor, Observer, Evaluator, Reflector, Memory, and Policy stay separable.
3. `scope_minimality`: the mutation is the smallest reusable change, not a broad rewrite.
4. `no_capability_loss`: existing init gates, native ask gates, review lanes, permission boundaries, model/cost policies, final independent review, and verification requirements are not weakened.
5. `evidence_quality`: the signal is verified or explicitly marked as proposal-only.
6. `memory_hygiene`: no secrets, PII, raw logs, chat transcripts, or unverified guesses are stored.
7. `policy_reversibility`: rollback is clear and does not depend on hidden state.
8. `runtime_compatibility`: Codex, Copilot, and Claude packaging boundaries are not broken.
9. `verification_fit`: static checks, schema checks, eval/probe prompts, or command evidence match the change type; review-boundary changes include contamination, permission, model/cost, final-review, and token-reuse probes.
10. `future_reuse`: the lesson helps future tasks without forcing unrelated tasks through heavier workflow.

## Output

```markdown
## Evolution Proposal
- strategy:
- signals:
- target:
- proposed_mutation:
- expected_delta:
- validation_plan:
- rollback_plan:
- writeback_files:
- state_sync:
- seven_module_trace:
- ten_pass_review:
```
