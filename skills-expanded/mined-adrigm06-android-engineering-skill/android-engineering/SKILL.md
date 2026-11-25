---
name: android-engineering-skill
description: Use when working on Android/Kotlin projects — architecture decisions, Compose UI, build/Gradle, testing strategy, performance, security, code review, debugging, or release engineering. Also use when Android tasks span multiple domains and a unified decision is needed.
---

# Android Engineering Master Skill

Use this as the single Android entrypoint. It orchestrates the domain skills in `skills/` and returns one integrated decision.

Global policy, non-negotiables, authority model, quantitative gates, and output contracts are defined in `AGENTS.md`.

<HARD-GATE>
Do NOT produce a final recommendation until you have:
1. Classified the mode (Design | Review | Generation | Debug)
2. Selected a lead skill from the routing matrix
3. Run the validation stage (Plan → Validate → Execute)
If evidence is insufficient, return a measurement-first plan — not a final answer.
</HARD-GATE>

## Primary objective

- Provide one complete Android skill for end-to-end engineering work.
- Keep modular depth by delegating domain-heavy reasoning to `skills/*/SKILL.md`.
- Avoid conflicting advice by using the authority protocol from `AGENTS.md`.

## When not to use this orchestrator directly

- When the task is purely within one domain with no cross-domain tension → invoke the domain skill directly.
- When the task is about backend services with no Android-specific implications → out of scope.
- When the task requires deep domain specialization and no synthesis → use the domain skill as lead with no orchestrator overhead.

## Mode classification

| Signal | Mode |
|---|---|
| "design", "architect", "how should I structure", "which pattern" | Design |
| "review this", "what's wrong with", "PR", "tech debt audit" | Review |
| "implement", "generate", "write code for", "scaffold" | Generation |
| "debug", "crash", "ANR", "why is X happening", "root cause" | Debug |

When signals conflict (e.g., "review and then fix"), choose the highest-risk mode.

- Design → recommend architecture/implementation direction + alternatives + decision triggers.
- Review → findings by severity with evidence, risk, fix, and verification.
- Generation → implementation plan/code strategy aligned to constraints and rollback-safe sequencing.
- Debug → ranked hypotheses, reproduction plan, instrumentation, and confidence updates.

## Operating workflow (mandatory)

1. Assess project context and constraints using `assets/project-context-assessment.md`.
2. Classify mode using the table above.
3. Select lead domain skill and supporting skills with `assets/routing-matrix.md`.
4. Execute lead-skill decision flow; pull only required supporting constraints.
5. Resolve conflicts with authority protocol and quantitative gates from `AGENTS.md`.
6. Run Validation stage: Plan → Validate → Execute.
7. Return one integrated output using the global output contract.

## Validation stage (mandatory before final output)

- **Plan**: define proposed path, risk class, expected impact, and verification gates.
- **Validate**: confirm minimum required evidence exists; if not, downgrade confidence and define minimum extra evidence.
- **Execute**: deliver final recommendation with explicit `pass | at-risk | fail` gate status and rollback-safe next steps.

If required evidence is missing, do not present a false-final answer. Return a measurement-first plan.

## Routing matrix (quick map)

- Architecture, modularization, dependency direction → `skills/android-architecture/SKILL.md` (lead)
- Compose UI state/recomposition/navigation → `skills/android-compose/SKILL.md` (lead)
- Build times, Gradle architecture, dependency governance → `skills/android-gradle-build/SKILL.md` (lead)
- Test strategy, flaky suites, confidence depth → `skills/android-testing/SKILL.md` (lead)
- Startup/jank/memory/ANR/battery optimization → `skills/android-performance/SKILL.md` (lead)
- Secrets, trust boundaries, sensitive data controls → `skills/android-security/SKILL.md` (lead, critical override)
- PR/technical debt quality synthesis → `skills/android-code-review/SKILL.md` (lead)
- Root-cause investigation and narrowing → `skills/android-debugging/SKILL.md` (lead)
- Go/no-go, rollout, rollback, release guardrails → `skills/android-release-engineering/SKILL.md` (lead)
- Coroutine scope, Flow/StateFlow, dispatcher, cancellation safety → `skills/android-kotlin-concurrency/SKILL.md` (lead)

For multi-domain tasks, set exactly one lead skill and add only materially relevant supporting skills.

## Project context adaptation

### Greenfield
- Start with modular monolith unless ownership/build pain justifies deeper split.
- Prefer Kotlin + Compose + coroutines + Room + Hilt + KSP + version catalogs.
- Establish CI, test strategy, and release gates from day one.

### Legacy modernization
- Prioritize pain-first increments; avoid big-bang rewrites.
- Stabilize boundaries before style purity.
- Use rollback-safe migration slices with explicit temporary compromises.

### Enterprise / multi-team
- Enforce strict ownership boundaries and module contracts.
- Increase release and security rigor; require stronger evidence gates.
- Optimize for long-term maintainability and team scalability.

### Startup / MVP
- Optimize for delivery speed with explicit debt labeling.
- Protect critical flows with focused testing and release guardrails.
- Keep upgrade paths documented for every pragmatic shortcut.

## Common rationalization anti-patterns

| Agent excuse | Correct behavior |
|---|---|
| "This is a simple task, I don't need to classify mode" | Mode classification is always required. Even simple tasks have an output contract. |
| "Performance and architecture conflict, I'll just pick performance" | Use the conflict resolution protocol. Architecture wins unless measured runtime evidence is critical. |
| "Security override feels excessive for this feature" | Security override is not about feeling — it applies to any exploitability or sensitive data pathway. |
| "I have partial context, I'll make reasonable assumptions" | Downgrade confidence, list assumptions explicitly, request minimum missing data. Do not produce a false-final answer. |
| "The user wants code, so I'll skip to Generation mode" | Classification is required. If code is requested without sufficient context, enter Design mode first. |

## Required behavior

- Do not bypass non-negotiable constraints.
- Do not produce independent checklists per domain; synthesize one plan.
- Do not present temporary compromises as permanent architecture.
- Always include confidence and assumptions for non-trivial recommendations.

## Mandatory output block (non-trivial responses)

Include this compact block in all non-trivial outputs:

- `Lead domain`: selected lead skill.
- `Supporting domains`: only materially relevant supporting skills.
- `Top gates`: 2-4 key gates labeled `pass | at-risk | fail`.
- `Minimum extra evidence`: smallest missing inputs that could change the decision.

## Key assets

- Global runtime policy: `AGENTS.md`
- Project context worksheet: `assets/project-context-assessment.md`
- Routing matrix: `assets/routing-matrix.md`
- Domain catalog: `skills/README.md`
