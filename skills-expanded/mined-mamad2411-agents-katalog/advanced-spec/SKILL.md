---
name: advanced-spec
description: Turn Adam's compressed, high-intent ideas into execution-grade briefs with explicit constraints, defaults, risks, output contracts, and stop conditions. Use when the user has a strong vision but underspecified scope; before /plan, /ironman, delegation, project design, agent builds, apps, automations, workflows, offers, or system changes. Especially useful when the request sounds directionally right but could drift into vague planning, overbuilding, or weak delivery contracts.
---

# Advanced Spec

Convert intent into planning-grade specification.
Do not brainstorm past the user's mission.
Do not pretend missing details are facts.

## Mission

Take a compressed or visionary request and produce an execution-grade pre-planning brief that is strong enough to hand into `/plan`, `/ironman`, delegation, or build work.

## Core law

The user often knows:
- what they want to become true
- roughly why it matters
- the vibe or shape of the solution

The user often does **not** fully specify:
- scope boundaries
- output format
- defaults
- acceptance bar
- failure conditions
- what must be decided now vs later

Your job is to close that gap.

## Output contract

Use this structure unless the task is trivial:

### ADVANCED SPEC BRIEF
- **How I understand it**
- **Confirmed**
- **Inferred**
- **Critical gaps**
- **Constraints to lock**
- **Proposed defaults**
- **Output contract**
- **Acceptance bar**
- **Failure modes**
- **Blocking questions**
- **Planning readiness**

Keep it tight.
The goal is not elegance.
The goal is a buildable contract.

## Workflow

### 1. Reconstruct intent
State the likely mission in one sentence.
Use direct language.
Do not expand scope.

Preferred starters:
- `Rozumiem tomu tak, že...`
- `Cieľ je pravdepodobne...`

### 2. Separate reality from interpolation
Split into:
- **Confirmed** — directly stated
- **Inferred** — likely implied
- **Critical gaps** — missing dimensions that would distort planning

Never blur inferred with confirmed.

### 3. Lock the execution-critical dimensions
Surface only the dimensions that change execution quality.
Prefer these dimensions when relevant:
- objective
- scope in / out
- user / audience
- output form
- cadence / timing
- channels / systems involved
- dependencies
- approval boundaries
- quality bar
- stop condition
- risks

### 4. Propose defaults aggressively but safely
If the task can move forward without asking everything, propose reversible defaults.
Label them clearly.

Preferred language:
- `Ak nepovieš inak, default je...`
- `Safe default pre v1 je...`

### 5. Build the output contract
Always specify:
- what should be delivered
- in what form
- for whom
- by what standard
- what counts as failure

If that is missing, the task is not ready for planning.

### 6. Ask only the minimum blocking questions
Ask questions only if the answer changes:
- architecture
- scope
- risk
- delivery sequence
- external behavior

Maximum:
- 1 question for light tasks
- 3 questions for normal planning
- more only for truly critical work

### 7. Decide readiness
End with one of:
- **Ready for planning**
- **Ready for planning with defaults**
- **Not ready for planning until X is clarified**

## Adam-grade heuristics

Bias toward this skill when the request has:
- strong energy
- clear ambition
- weak boundaries
- mixed layers of vision + execution
- hidden assumptions
- too many things bundled into one sentence

Typical examples:
- `Sprav z toho projekt.`
- `Chcem z toho Natural20-like produkt.`
- `Potrebujem AI skill na toto.`
- `Postavme ongoing intel vrstvu.`
- `Chcem systém, čo mi toto celé bude riešiť.`

## Hard rules

- Do not drift into solution theater.
- Do not inflate the mission.
- Do not ask a soft list of generic product questions.
- Do not produce a plan disguised as clarification.
- Do not skip acceptance bar and failure bar.
- Do not let the user move into execution with a weak contract.

## Escalation pattern

If the user is visionary but structurally vague:
- tighten scope
- split layers
- define defaults
- force one primary output

If the user is overloaded:
- reduce fronts
- pick one dominant objective
- kill side branches early

If the user is already precise:
- say so
- do not create discovery theater

## Routing law

After producing the brief:
- route to `/plan` when a structured plan is needed
- route to `/ironman` when the project is non-trivial and needs design + verification gates
- route directly to execution only for tiny low-risk work

## References

If needed, read:
- `references/contract-patterns.md` for reusable contract dimensions and prompt shapes
