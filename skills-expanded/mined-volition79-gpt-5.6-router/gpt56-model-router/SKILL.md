---
name: gpt56-model-router
description: Route explicitly requested work across GPT-5.6 Sol, Terra, and Luna using a user-selected performance, balanced, or token-saving profile, with Sol-owned but creatively open product, UX/UI, visual, interaction, motion, and art-direction work. Includes read-only discovery, parent-model-aware delegation, explicit approval before execution, and outcome-based design acceptance that preserves exploration and implementation creativity. Use only when the user explicitly invokes $gpt56-model-router or directly asks for the GPT-5.6 model router. Do not invoke implicitly for ordinary tasks.
---

# GPT-5.6 Model Router

Exploit each GPT-5.6 model's strengths without forcing users to design a team. The parent agent remains orchestrator and integrator; subagents perform only capability-matched stages that justify their overhead.

## Activation

Activate only after explicit invocation or a direct request to use this router. Do not change the parent model or Codex collaboration mode. Do not activate implicitly for ordinary tasks.

Before the first user selection, use only the request and existing conversation context. Do not read files, browse, run commands, invoke MCP, start tests, edit, or spawn agents.

## Gate 1: Choose An Objective

Present these profiles with a task-specific one-line tradeoff:

1. **PERFORMANCE** - maximize correctness, depth, and independent validation; may use more tokens or time.
2. **BALANCED** - preserve required quality while minimizing duplicate context and unnecessary agents. Recommend by default.
3. **TOKEN_SAVER** - minimize non-required Sol use, calls, and context while preserving Sol-owned design, explicit acceptance, and safety thresholds.

Use `request_user_input` only when the tool is explicitly available and the active collaboration mode permits it. In Default mode, use numbered text choices immediately instead of attempting the tool. Wait for a clear selection and do not infer one from silence or an unrelated message.

Alongside the choices, propose the minimum read-only discovery needed to route accurately. The user's profile selection authorizes only that displayed read-only discovery. If the task is already fully specified and discovery is unnecessary, say so.

## Read-Only Discovery

After Gate 1, inspect only the approved evidence needed to identify:

- independent versus tightly coupled work stages;
- ambiguity, consequence of error, repetition, and verification burden;
- available deterministic validators;
- likely context duplication and orchestration overhead;
- the parent model identity when reliably surfaced by the current session.

Do not write, deploy, publish, change accounts, access unstated sensitive surfaces, or spawn implementation agents during discovery. If the parent model is not reliably known, label it `unknown`; do not guess.

## Build The Adaptive Route

1. Express the task as a small dependency graph: analysis, research, design, implementation, deterministic transformation, verification, and final judgment as applicable.
2. For every program, product, app, game, website, or user-facing tool, explicitly decide whether a design stage exists. When it does, assign its design direction and subjective design acceptance to Sol.
3. Assign the lowest-cost model that satisfies each remaining stage's capability and risk floor.
4. Count the known parent model as an active capability. Do not duplicate its planning or integration role unless independent review has explicit value.
5. Prefer one agent. Add agents only for independent evidence, disjoint parallel work, deterministic volume, specialization, required Sol design ownership, or consequential independent review.
6. Keep context packets narrow. Send each subagent only its contract and necessary evidence.
7. Escalate Luna -> Terra -> Sol when ambiguity, failed validation, conflicting evidence, or higher consequence appears.
8. Compare the route with Sol direct. If delegation lacks a credible advantage for the selected profile or creates an unacceptable regression, recommend Sol direct.

When executing, prefer the installed custom role if the active subagent tool exposes it. If the runtime does not expose custom role names, use a built-in `default`, `worker`, or `explorer` agent with the approved GPT-5.6 model and reasoning override, and include the same role contract in its prompt. This is a role-adapter fallback, not permission to substitute the approved model.

If `spawn_agent` omits `agent_type`, `model`, or `reasoning_effort`, or Codex start/resume fails after enabling Multi-Agent V2, do not immediately classify the runtime as permanently incapable. During approved read-only discovery, read `references/runtime-troubleshooting.md` and check the active CLI/app versions, effective V2 settings, and exposed tool schema. Never print the whole config because it may contain secrets, and never edit global config without separate user approval. If a supported remediation plus restart/new thread still leaves model pinning unavailable, stop and report the capability gap instead of spawning.

Classify runtime support before approved execution:

- **A - full support**: `spawn_agent` exposes `agent_type`, `model`, `reasoning_effort`, and `fork_turns`. Continue only after a minimal explicit-model probe confirms the requested child model and reasoning effort when child metadata is observable.
- **B - limited support**: spawning works but model or role pinning is unavailable or cannot be verified. Stop routing, report that model pinning is not trustworthy, and request approval for a configuration remediation. Never inherit Sol silently.
- **C - request-wide failure**: the request is rejected before inference with the reserved `collaboration.spawn_agent` schema error. The skill cannot self-repair because it was not loaded. Use the install/recovery guidance in `references/runtime-troubleshooting.md`, then fully restart Codex and open a fresh thread.

Use `fork_turns: "none"` by default for routed children. Send a narrow packet containing role, objective, required evidence, allowed write surface, non-goals, requested model, reasoning effort, validation, and output shape. Do not claim successful routing from a successful spawn alone; when observable metadata reports a different model, reasoning effort, role, or sandbox, stop and report the mismatch.

Read `references/routing-policy.md` for capability floors and profile behavior. Read `references/execution-playbooks.md` for handoffs and integration.
Read `references/runtime-troubleshooting.md` only when model/role overrides are missing, spawning fails, start/resume reports a multi-agent configuration error, or version drift could invalidate a known workaround.

## Estimate Effects Honestly

Report Sol-direct-relative estimates for:

- output quality;
- elapsed time;
- total tokens/cost;
- regression risk;
- confidence in each estimate.

Use directional values such as `lower`, `similar`, or `higher` plus the evidence and uncertainty. Use numeric percentages or token/time ranges only when they come from comparable measured history or deterministic workload counts. Never invent savings or guarantee superiority.

If exact token usage is unavailable from the runtime, say `not observable` rather than estimating a number. A profile controls priorities, not outcomes.

## Gate 2: Approve Execution

Present one recommended route using `assets/routing-plan-template.md`. Include a compact alternative only when it has a genuinely different useful tradeoff.

The route must show:

- selected profile and parent-model assumption;
- stages, roles, models, reasoning effort, permissions, and order;
- expected deliverable and validation per stage;
- Sol-direct comparison and estimate confidence;
- external or destructive actions that remain separately approval-gated.

Wait for explicit approval of the displayed route. Selection of a profile is not execution approval. After approval, spawn only the approved roles.

Use `references/approval-protocol.md` for state transitions and material reapproval rules.

## Creativity And Flexibility

- Fix responsibilities and safety boundaries, not solutions.
- Let Sol compare unconventional approaches and challenge the user's framing.
- Let Terra adapt implementation tactics and improve expression inside the approved design intent; do not reduce Terra to mechanical transcription.
- Treat playbooks as defaults, not a closed list or keyword table.
- Permit tactical changes within approved scope, permissions, risk, and cost without reapproval.
- Stop for reapproval only when model, role, scope, permissions, order, risk, or cost changes materially.

## Creative Freedom Invariant

Protect creative breadth while keeping Sol accountable for design quality.

- Make Sol define intent, audience, emotional target, experience principles, constraints, and outcome-based acceptance. Do not require premature pixel-level, component-level, or stylistic lock-in unless the user explicitly requests exact fidelity or the domain requires it.
- For open-ended design work, have Sol explore at least two meaningfully different directions before convergence unless the user has already fixed the direction or the scope is too small to repay comparison. Compare concepts by their underlying idea, not cosmetic color swaps.
- Give Terra bounded creative license to refine composition, hierarchy, motion, microinteractions, technical expression, and responsive behavior when changes preserve the approved intent, safety, scope, and acceptance threshold.
- Require Terra to preserve and report promising emergent ideas. Apply reversible, in-contract improvements without reapproval; return material direction changes to Sol as proposals instead of discarding them or silently applying them.
- Make Sol judge the implemented result as new evidence. Sol may evolve the original contract when the implementation reveals a stronger solution; do not treat the first design draft as immutable truth.
- Judge design acceptance by clarity, coherence, usability, emotional fit, distinctiveness, and craft rather than literal conformity to the first proposal.
- Avoid premature convergence on generic templates, fashionable defaults, or reference imitation. Use references for principles and constraints, not as a ceiling on originality.
- Respect explicit user choices. Creative freedom may improve the route within the approved objective, not override the user's settled direction.

## Sol Design Ownership

Treat design as a Sol capability floor for program-building work. Design includes product and experience direction, information architecture, UX/UI, visual language, interaction and motion behavior, art direction, design-system decisions, and subjective visual-quality acceptance.

- Use the Sol parent when the parent is reliably Sol; otherwise assign a Sol design role.
- Let Terra implement the approved design intent, exercise the creative latitude defined above, and run deterministic UI checks, but return material design choices, tradeoffs, and visual acceptance to Sol.
- Require Sol to review implementation evidence when final quality depends on visual, interaction, or experiential judgment. A separate Sol reviewer is optional when the Sol parent already provides independent-enough final judgment.
- Do not assign Luna design direction or subjective design review.
- Preserve this ownership in PERFORMANCE, BALANCED, and TOKEN_SAVER. Profiles may reduce context or duplicate review, not the Sol design floor.
- If a task has no meaningful design surface, state that briefly and route normally.

## Model Boundaries

- **Sol**: product/UX/UI/visual/interaction/motion/art direction, subjective design acceptance, ambiguous planning, architecture, high-consequence execution, adversarial review, and final judgment.
- **Terra**: exploration, implementation of an approved design, general implementation, deterministic testing, and evidence synthesis.
- **Luna**: deterministic extraction, normalization, conversion, and repetitive transformation with objective checks.

Never assign Luna source-of-truth selection, design direction, subjective design review, architecture, ambiguity resolution, destructive decisions, safety judgment, or final sufficiency review.

## Safety Invariants

- Routing approval does not bypass normal permission or action approvals.
- Never weaken the parent's effective sandbox or approval policy.
- Never use `danger-full-access` as a role default.
- Keep delegation depth at one; subagents must not spawn descendants.
- Do not silently substitute an unavailable model. Pause and request reapproval.
- Do not expose secrets in plans, handoffs, logs, or evaluations.
- Do not automatically persist prompts, source content, or sensitive telemetry.

## Completion

The parent integrates all results and reports the actual route, validation, deviations, elapsed-time evidence when observable, token usage when observable, and residual risk. Subagent completion alone is not task completion.
