---
name: using-elyra-skills
description: Navigate the elyra-skills registry - pick the right skill for the task, chain skills across the development lifecycle, and combine them without conflicts. Use when unsure which skill applies, when a task spans multiple skills, when the user asks what skills exist or how they fit together, or at the start of a large multi-phase task.
license: MIT
compatibility: elyra >=0.1, claude-code
allowed-tools: read, bash, grep
metadata:
  author: elyra-skills
  version: 1.0.0
  tags: [meta, skills, workflow, lifecycle]
---

# Using Elyra Skills

A map of the registry: which skill to load **when**, how they **chain**, and how to combine them without tripping over each other.

## When to use

- Unsure which skill fits the current task
- A task spans multiple phases (idea → ship) and needs a sequence
- The user asks "what skills do you have?" or "how do these fit together?"
- Kicking off a large feature where the right opening move matters

## Selection rules

1. **Match the task's phase, not its noun.** "Fix the payment API" might be `debugging` (it's broken), `resilience-patterns` (it's flaky), or `deprecation-migration` (it's being replaced). Ask what's actually happening before loading.
2. **One primary skill at a time.** A primary skill drives the process and the output format; others are consulted for their checklists, not their workflow.
3. **Vague input → discovery skill first.** When the request can't be restated as a verifiable outcome, start with `idea-refine` (new ideas) or `codebase-exploration` (unfamiliar code) — never with implementation.
4. **No skill fits → no skill.** Skills encode workflows; trivial tasks don't need one. Loading a skill for a one-line fix is overhead.

## The lifecycle map

```
DEFINE            PLAN             BUILD              VERIFY           SHIP             OPERATE          MAINTAIN
idea-refine   →   task-breakdown → incremental-     → debugging      → ci-cd-pipeline → observability  → tech-debt-triage
spec-writing                       implementation     test-writing     release-         incident-        refactoring
threat-modeling                    codebase-          code-review      checklist        response         dependency-update
api-design                         exploration        security-audit   feature-flag-    runbook-author   deprecation-migration
architecture-                      error-handling     accessibility-   rollout          cost-            
review                             caching-strategy   review           changelog        optimization     
adr-author                         resilience-        i18n-review      conventional-                     
                                   patterns           performance-     commits                           
                                   database-          budget           pr-description                    
                                   migration          data-privacy-    git-workflow                      
                                   llm-feature-       review                                             
                                   design             code-style-guide                                   
```

Cross-cutting (any phase): `context-engineering`, `onboarding-doc`, `git-workflow`.

## Stack-specific skills

Stack skills are selected **in addition to** the phase skill, never instead of it. The phase skill drives the workflow; the stack skill supplies the framework-specific rules and checklists for the steps.

| Project signal | Stack skills |
|---|---|
| Laravel (`composer.json` has `laravel/framework`) | `laravel-eloquent-performance`, `laravel-queue-design`, `laravel-testing` |
| Laravel + `laravel/ai` | `laravel-ai-features` (layered on `llm-feature-design`) |
| TALL (Livewire, Flux) | `livewire-component-design`, `flux-ui-patterns` |
| VILT (Vue, Inertia) | `vue-component-patterns`, `inertia-patterns` |
| PrimeVue in `package.json` | `primevue-patterns` |
| Filament panels | `filament-resource-design` |

Examples of the pairing:

- Slow Laravel page → `debugging` (primary, owns the loop) + `laravel-eloquent-performance` (the stack checklist inside steps 2–4)
- New TALL feature → `task-breakdown` → `incremental-implementation` (primary) + `livewire-component-design` / `flux-ui-patterns` consulted per task
- Testing phase in a Laravel app → `test-writing` for *what* to test, `laravel-testing` for *how* to test it here

Detect the stack from manifests (`composer.json`, `package.json`) before assuming — don't load Laravel skills into a Django repo because the user said "backend".

## Standard chains

**New feature, end to end:**
`idea-refine` → `spec-writing` → `task-breakdown` → `incremental-implementation` → `code-review` → `release-checklist`
Skip `idea-refine` when the problem is already crisp; skip `spec-writing` for tasks under ~1 hour.

**Sensitive feature (auth, money, PII):** insert `threat-modeling` during spec — its mitigations become acceptance criteria — and `security-audit` + `data-privacy-review` at review.

**Bug in production:** `incident-response` (if users are hurting now) → `debugging` (root cause) → `test-writing` (regression test). Postmortem actions may spawn `resilience-patterns` or `observability` work.

**Inherited/unfamiliar codebase:** `codebase-exploration` → `tech-debt-triage` → then the normal feature chain, with `context-engineering` to write down what you learned.

**Replacing something old:** `codebase-exploration` (blast radius) → `deprecation-migration` (the plan) → `database-migration` / `dependency-update` for the mechanics.

## Combining without conflict

- The **primary** skill owns the output format. If `incremental-implementation` is driving and a step needs a migration, apply `database-migration`'s rules *inside* that step's boundaries — don't switch report formats mid-task.
- Review skills (`code-review`, `security-audit`, `accessibility-review`, `i18n-review`) stack cleanly: run as separate passes, merge findings into one severity-ranked list.
- When two skills disagree (e.g. `refactoring` says "small steps", deadline says "big bang"), surface the trade-off to the user — don't silently pick.

## Output format

When recommending skills for a task:

```markdown
**Task as I understand it:** …
**Primary skill:** `<name>` — why.
**Supporting:** `<name>` (used for: …)
**Chain (if multi-phase):** `a` → `b` → `c`, with handoff points.
**Not loading:** `<name>` — why not (e.g. overlap, overkill).
```

## Anti-patterns

- ❌ Loading three skills and blending their workflows into mush — one primary, others consult
- ❌ Skipping discovery (`idea-refine`/`codebase-exploration`) because the user sounded confident
- ❌ Forcing a skill onto a trivial task for ceremony's sake
- ❌ Following a skill's letter against the project's reality — skills encode defaults, the codebase wins
- ❌ Running the full lifecycle chain on a bugfix — match weight to the task
