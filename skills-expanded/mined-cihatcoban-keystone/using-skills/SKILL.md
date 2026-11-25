---
name: using-skills
description: Routes the current work to the right Keystone skills and chains them in order. Use at session start or when unsure which process applies. Triggers - which skill should I use, where do I start with this task, what is the process here, hangi skill, nereden başlayayım.
---

# Using Skills

Keystone is a process library. Each skill encodes how one kind of engineering
work is done properly. This meta-skill decides which one applies and in what
order — picking wrong is worse than picking none, because a half-matching
process produces confident, wrong-shaped work.

## Read first, every session

1. `CLAUDE.md` — the invariants. They outrank every skill.
2. The project's `CONSTRAINTS.md` — the numbers. If absent, run `/constraints`.
3. Existing ADRs (`docs/adr/`) — decisions already made are not re-litigated
   mid-task.

## Router

| Situation | Skill |
|---|---|
| Request is vague, or you are about to guess what someone wants | `requirements-interrogation` |
| Intent is clear, nothing is written down | `spec-driven-development` |
| Spec exists, work needs sequencing | `planning-and-task-breakdown` |
| A choice will be expensive to reverse | `architecture-decisions` |
| The words in the code don't match the words in the business | `domain-modeling` |
| Modules are tangled, a change touches everything | `boundaries-and-dependencies` |
| Designing anything another system calls | `api-and-contract-design` |
| Choosing or shaping storage, indexes, schema | `data-modeling-and-storage` |
| Network calls, queues, partial failure, retries | `distributed-systems-and-resilience` |
| Shared mutable state, locks, transactions, races | `concurrency-and-consistency` |
| Building user interface | `frontend-architecture` |
| Writing the code for a planned task | `incremental-delivery` |
| Any logic or bug fix | `test-driven-development` |
| Deciding what to test and at which level | `testing-strategy` |
| Code works but is hard to read or change | `refactoring-and-simplification` |
| Commits, branches, history, PR hygiene | `git-workflow` |
| Before merge | `code-review` |
| Something broke or behaves unexpectedly | `debugging-and-root-cause` |
| Something is slow, or a budget is at risk | `performance-engineering` |
| Untrusted input, auth, secrets, sensitive data | `security-and-threat-modeling` |
| You cannot tell what production is doing | `observability-and-slos` |
| Cutting a version, shipping, rolling back | `release-engineering` |
| Removing or replacing something in use | `deprecation-and-migration` |
| Production is on fire, or just stopped being | `incident-response` |
| Adding a library, model, dataset or copied snippet | `dependency-and-license-policy` |
| A config value, API key, `.env` file or leaked secret | `configuration-and-secrets` |
| Adding or trusting an MCP server, plugin, hook or agent permission | `agent-and-toolchain-security` |
| Writing docs a future person will rely on | `documentation-and-knowledge` |
| Putting a model in the product | `ai-integration-guardrails` |
| Setting or enforcing the quality bar | `constraint-driven-development` |
| Configuring what the agent knows about this repo | `context-engineering` |
| Several agents on one task, parallel work, or a loop that will not stop | `agent-orchestration` |
| Adding to Keystone itself | `skill-authoring` |

## Chains

Chains matter more than individual skills — most real failures happen between
stages, not inside them.

**New capability**
`requirements-interrogation` → `spec-driven-development` → `architecture-decisions`
(only if a choice is costly to reverse) → `planning-and-task-breakdown` →
per task: `incremental-delivery` + `test-driven-development` → `code-review` →
`release-engineering` → `observability-and-slos`

**Integrating an external system**
`api-and-contract-design` (their contract, your adapter) →
`distributed-systems-and-resilience` (timeouts, retries, idempotency) →
`testing-strategy` (contract tests, recorded fixtures) → `observability-and-slos`

**"It's slow"**
`performance-engineering` (measure, find the real bottleneck) → then whichever
of `data-modeling-and-storage`, `concurrency-and-consistency`,
`frontend-architecture` the measurement points at — never the reverse order

**Inherited code you must change**
`boundaries-and-dependencies` (map what depends on what) →
`testing-strategy` (characterization tests as a safety net) →
`refactoring-and-simplification` → then the actual change

**Replacing something live**
`deprecation-and-migration` → `incremental-delivery` (expand/contract) →
`observability-and-slos` (shadow comparison) → `release-engineering`

## Rules

- Multiple skills apply more often than one. Apply all of them; do not pick a
  favorite and drop the rest.
- Reading a skill costs little; applying the wrong process costs a rewrite.
- No skill fits? Fall back to `CLAUDE.md` invariants and say so. A gap felt
  three times is a skill worth writing (`skill-authoring`).
- A skill never overrides `CLAUDE.md`, `CONSTRAINTS.md`, or an accepted ADR.

## Exit checklist

- [ ] `CLAUDE.md` and the project's `CONSTRAINTS.md` were read this session
- [ ] Every skill that applies to the current work has been identified, not just one
- [ ] The chain, not only the individual step, has been considered
- [ ] Any gap where no skill fits has been stated rather than improvised over
