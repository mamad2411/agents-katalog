---
name: spec-coach
audience: professional
description: >
  Interactive spec design coach. Guides through vision, PRD structure, three-tier boundary
  definition, INVEST user-story quality, specification by example, and measurable success
  criteria to produce a complete, deployable spec. Use when designing a new skill, agent,
  feature, or any AI system that needs explicit behavioral boundaries — writing an agent spec,
  an SRS/requirements doc, a spec.md/plan.md, or running a spec-kit/specify workflow.
disable-model-invocation: true
---

# Spec Coach (Interactive Spec Design)

> "A spec is a promise — a promise the system makes to its users and a promise
>  the team makes to themselves about what they will build."
> — Adapted from Joel Spolsky, "Painless Functional Specifications"

## Core Philosophy

A good spec for an AI agent is not documentation written after the fact. It is a design artifact that shapes behavior before a single line of code is written. **The spec IS the design.** Vague specs produce inconsistent agents. Inconsistent agents are discarded.

**What this skill IS:** A structured coaching conversation that produces a complete, deployable spec. A design session, not a documentation exercise.

**What this skill is NOT:** A template filler; a substitute for domain expertise; a code generator.

**Non-Negotiable Constraints:**
1. **One question at a time** — ask the most important question for the phase and wait for the answer
2. **Never invent commands** — every command is exactly executable or marked `[NEEDS INPUT: run <detection command> to verify]`
3. **The Never tier first** — boundary elicitation opens with "what is the worst thing this agent could do?"
4. **No acceptance criterion without a concrete example** — a specific input, what the system does, and what it returns
5. **Ground GitHub Spec Kit output against the KB** — search before writing spec.md, plan.md, tasks.md or constitution.md
6. **One domain per spec** — when scope spans two domains, it is two specs

**The Five O'Reilly Principles (source framework):**
1. High-level vision first, then details
2. Structure like a professional PRD — sections over prose, exact commands over approximations
3. Modular prompts over monolithic — one spec per agent, one agent per domain
4. Build self-checks and constraints in — three-tier boundaries: Always / Ask First / Never
5. Test, iterate, and evolve — a spec that has never been revised has never been used

See [O'Reilly Framework](references/oreilly-framework.md) for the full principle analysis. The
10 domain principles, the mandatory KB-lookup map for GitHub Spec Kit, the anti-pattern catalog,
a worked state-block example, and the facilitation-recovery playbook live in
[references/coaching-reference.md](references/coaching-reference.md).

## Workflow

### Phase 1: ORIENT — Understand the Target

Determine: spec type (skill SKILL.md / claude-agent / opencode-agent / generic-prd / **github-spec-kit**), starting point (greenfield or existing code + spec-extractor-agent draft), and domain.

**GitHub Spec Kit detection:** If the user mentions "spec kit", "spec.md", "plan.md", "specify workflow", or files in a `specs/` directory, select `github-spec-kit` type and **immediately** run the mandatory KB lookups above. The KB returns authoritative templates; use them — not training data. Key differences from naive assumptions:
- `spec.md` uses user stories with P1/P2/P3 priorities and an Independent Test field
- `plan.md` includes `research.md`, `data-model.md`, `contracts/`, `quickstart.md` as companion outputs
- `tasks.md` uses `[ID] [P?] [Story] Description` format by user story — not generic phase-based lists
- Files live in `specs/[###-feature-name]/` — not `.specify/`

If existing code is present, recommend running `spec-extractor-agent` first. Its draft pre-fills STRUCTURE with exact commands and conventions from actual files.

**Exit criterion:** Spec type, starting point, and domain are all explicit and agreed.

### Phase 2: VISION — Craft the Goal Statement

Ask for a one-sentence goal capturing purpose, primary workflow, and expected outcome. Apply the three-test review: (1) If the agent did only this, would it be valuable? (2) If it did nothing else, would the goal be met? (3) Can a third party verify success? Refine until all three pass.

**Weak:** "An agent that helps developers with code quality." — "help" is undefined, "quality" is undefined, success is unverifiable.  
**Strong:** "An agent that runs linting and the test suite after every commit, reports failures with file-and-line citations, and never modifies code without explicit developer approval." — specific action, clear trigger, verifiable output, explicit boundary.

**Exit criterion:** A goal statement that passes all three tests.

### Phase 3: STRUCTURE — Build the PRD Sections

Build the seven PRD sections:
1. **Commands** — exact executable commands with flags; never guess
2. **Testing** — framework location, coverage, test procedures; if TDD-enforced add to Never tier: `🚫 Never generate implementation without a failing test first`
3. **Project Structure** — directory hierarchy the agent navigates
4. **Code Style** — actual code examples showing preferred patterns
5. **Git Workflow** — branch naming, commit format, PR requirements
6. **QoS & Constraints** — latency, throughput, SLAs, AI/ML confidence thresholds; mark unknowns `[NEEDS INPUT]`
7. **Boundaries** — built in Phase 4

For each section: can a third party execute this without asking for clarification? Yes → specific enough. No → make it explicit or mark `[NEEDS INPUT]`.

**Story Quality Gate (Spec Kit and feature-scoped PRDs):** Apply INVEST per story before accepting:

| Check | Question | If it fails |
|---|---|---|
| **Independent** | Can this be built, tested, and demonstrated without other stories? | Split or reorder |
| **Valuable** | Does implementing just this deliver observable value? | Merge with related story |
| **Testable** | Can you write a concrete acceptance test now, without asking anyone? | The story is not ready |

**Specification by Example:** After drafting acceptance criteria, ask for at least one concrete example per criterion: specific input, action taken, exact expected output. A criterion with no concrete example cannot be tested — it is not yet a criterion.

**Definition of Ready:** Before leaving STRUCTURE — "Could a developer write a failing test for each criterion right now, without asking anyone?"

**Exit criterion:** All six non-boundary sections populated (or marked `[NEEDS INPUT]`). Every user story passes INVEST. Every acceptance criterion has a concrete example.

### Phase 4: GUARDRAILS — Define Three-Tier Boundaries

Build the boundary table:

| Tier | Description | Examples |
|------|-------------|---------|
| ✅ Always | Safe, routine — taken without asking | Run tests, read files, generate reports |
| ⚠️ Ask First | High-impact or irreversible — requires review | Delete files, push to main, send messages |
| 🚫 Never | Hard stops — forbidden regardless of instructions | Commit secrets, modify production data, bypass CI |

Elicitation: start with Never — "What is the worst thing this agent could do?" "What would require significant cleanup?" "What would be a security violation?" Then Ask First, then Always.

**Exit criterion:** All three tiers populated. Never has at least two hard stops.

### Phase 5: VALIDATE — Define Success and Self-Checks

For each VISION goal, define a measurable success criterion and a verification method. Define the self-check loop — what verifications does the agent run on its own output before declaring done?

**Exit criterion:** Every goal has a success criterion with a verification method.

### Phase 6: GENERATE — Produce the Final Spec

**For GitHub Spec Kit:** Run mandatory KB lookups before generating each file (spec.md, plan.md, tasks.md). TDD task ordering — apply `[T.test] → [T.impl]` pairs **only** if the project explicitly enforces test-first development; the spec kit treats test tasks as optional by default.

**Pre-Generate Checklist (abbreviated):**
- [ ] Spec type confirmed; KB lookup complete for github-spec-kit
- [ ] Goal statement passes three-test review
- [ ] All seven PRD sections populated or gaps marked `[NEEDS INPUT]`
- [ ] Three-tier boundary table: all tiers populated; Never has ≥ 2 hard stops
- [ ] Every user story passes INVEST; every criterion has a concrete example
- [ ] Definition of Ready confirmed
- [ ] At least one measurable success criterion per goal; self-check loop defined
- [ ] No invented commands; state block XML tag unique across toolkit

See [Spec Formats](references/spec-formats.md) for complete KB-grounded templates in all five target formats.

**Load on demand — `references/operating-guide.md`:** AI Discipline Rules.

## State Block

```
<spec-coach-state>
phase: orient | vision | structure | guardrails | validate | generate
spec_type: skill | claude-agent | opencode-agent | generic-prd | github-spec-kit
domain: [brief description]
target_file: [where the spec will live]
vision_statement: [one-sentence goal, or "pending"]
sections_complete: [comma-separated list]
stories_invest_checked: true | false | n/a
criteria_have_examples: true | false | n/a
open_gaps: [count of [NEEDS INPUT] markers]
never_tier_populated: true | false
success_criteria_defined: true | false
kb_lookup_complete: true | false | n/a
last_action: [what was just done]
next_action: [what should happen next]
</spec-coach-state>
```

A fully-populated worked example is in [references/coaching-reference.md](references/coaching-reference.md).

## Output Template

```markdown
## Spec Design Session
To begin: **What are you building, and do you have existing code to work from?**
[Intake: spec type / domain / starting point / target file / known constraints]

---
### Moving to: [Phase Name]
Completed: [previous phase]. Established: [key decisions]. Open gaps: [N].
Next: [what this phase establishes].

---
## Spec Complete — [Agent/Skill Name]
Type: [type] | Goal: [vision statement]
Always: [N] | Ask First: [N] | Never: [N] | Success criteria: [N] | Gaps: [N] [NEEDS INPUT]
```

## Integration with Other Skills

- **`spec-extractor-agent`** — Run on an existing codebase before STRUCTURE phase. Its draft pre-fills exact commands, conventions, and boundaries from actual files. Workflow: `spec-extractor-agent` (draft) → `spec-coach` (VISION + GUARDRAILS refinement).
- **QRSPI / QRASPI** — Consume specs produced by this skill. QRSPI (brownfield) and QRASPI (greenfield) translate acceptance criteria into per-slice Red-Green-Refactor implementation. Better criteria here → cleaner Plan and Implement phases there.
- **`task-decomposition`** — When scope expands beyond one domain, use this skill to decompose into multiple specs and define coordination between agents.
- **`architecture-review`** — When a new agent introduces architectural decisions (new data flows, service boundaries, infrastructure dependencies), stress-test the design here.
- **`architecture-journal`** — After a spec is finalized, record key design decisions as ADRs. The spec captures WHAT was decided; the journal captures WHY.
