---
name: stack-ready
description: "Choose the right stack for a project before building it. Triggers on 'what stack should I use,' 'Next.js vs. Remix,' 'pick a database,' 'Postgres or Mongo,' 'which auth provider,' 'should I use Convex,' 'hosting recommendation,' 'move from Firebase to Supabase,' or any request to evaluate tech choices for a specific job. Outputs a ranked, scored shortlist with tradeoffs, pairing compatibility checks, and bundle recommendations tailored to domain, team size, budget, and time-to-ship. Stops at the recommendation: does not build the app (that's production-ready) or configure the repo (that's repo-ready). Not for purely abstract language debates with no project attached. Full trigger list in README."
version: 3.1.0
updated: 2026-11-23
changelog: CHANGELOG.md
suite: ready-suite
tier: planning
upstream: []
downstream:
  - repo-ready
  - production-ready
pairs_with:
  - production-ready
  - repo-ready
compatible_with:
  - claude-code
  - codex
  - cursor
  - windsurf
  - antigravity
  - pi
  - openclaw
  - any-agentskills-compatible-harness
---

# Stack Ready

This skill exists to solve one specific failure mode. Stack recommendations that *feel* authoritative but are generic, undated, and unaccountable. "Use Next.js, Postgres, and Prisma" for a healthcare app that needs a BAA and row-level audit. "Try Convex" for a reporting-heavy B2B tool that will hit its query model in month three. "Supabase is great" recommended to a team whose compliance office already rejected it last quarter. The team builds for six weeks, hits the failure mode that was predictable from day one, and rips out the stack.

The job here is the opposite. Produce a stack recommendation that names the assumptions it rests on, the failure mode that would flip it, the scale ceiling, and the switching cost. If a dimension is scored, the score explains its weighting. If a bundle is proposed, the pairings have been compatibility-checked. If a decision is made, it is written down in a form the next agent, the next engineer, and `production-ready` can consume without re-litigating.

This is harder than it sounds because stack selection is a 12-dimension decision with interaction effects. Pick Convex and you don't pick an ORM. Pick WorkOS and you don't pick Clerk. Pick Vercel and most self-hosting questions vanish, along with the option to self-host. A good recommendation is not a menu; it is a coherent bundle.

## Core principle: score for this job, not this year

Do not hand the user a neutral survey of options. Do not say "it depends" and stop. And do not pretend scores are objective. Every score in this skill is opinionated under stated weights. Change the weights, the score changes. The user's job is to confirm or override the weights; the skill's job is to make the weights visible.

> **Every output states the weighting assumptions the user can override, and names the failure mode that would flip the recommendation.**

This principle is non-negotiable. An unweighted recommendation is a horoscope. A flip-point-free recommendation is a guess. Both fail the user at month three.

## When this skill does NOT apply

Route elsewhere if the request is:

- **Purely abstract language or framework debate** with no project attached ("is Rust better than Go," "I hate TypeScript"). This skill requires a job to score against.
- **Learning roadmap** ("what should I learn next"). Pick a learning-roadmap skill instead; stack choices for learning are different from stack choices for shipping.
- **Implementation work** ("now build the app with Next.js"). That's `production-ready`.
- **Repo hygiene** ("set up CI for my Next.js app"). That's `repo-ready`.
- **Single-library evaluation** ("is zod or valibot faster"). Answer inline; the full workflow is overkill for a single-dimension choice unless the user explicitly wants the full scoring pass.
- **Vendor-specific sales questions** ("is Vercel worth the price for my company"). Answer factually; do not run the full comparison workflow unless the user is genuinely choosing between options.
- **The team already knows and is confident.** If the user explicitly states "we've shipped three apps on Rails; we're picking Rails again; confirm it still fits," run a compact pre-flight and constraint check only; do not run the full scoring pass. See `references/scoring-framework.md` § "When to skip the scoring pass entirely." Formal scoring applied to reversible, experience-backed, low-stakes decisions by a small team is itself a failure mode (paralysis by analysis); recognize when the skill's rigor is more cost than value.

## Workflow

Follow this sequence. Skipping steps produces the exact failure this skill exists to prevent: a stack recommendation that collapses under its unstated assumptions.

### Step 0. Detect project state and mode

Read `references/stack-research.md` and run the mode detection protocol.

- **Mode A (Greenfield)**: no code yet, picking from scratch. Proceed to Step 1.
- **Mode B (Assessment)**: existing codebase, user is evaluating whether the stack still fits. Run the stack inventory scan. Its output replaces guesswork.
- **Mode C (Audit)**: user asks "did we pick right," "should we move off X," "is our stack still appropriate." Assessment plus scoring against current needs, producing a keep/adjust/replace verdict per dimension.
- **Mode D (Migration)**: user has already decided to move from X to Y (or is considering it) and wants the sequenced path, blast radius, and rollback plan. Skip to Step 7 after a short pre-flight.

**Passes when:** a mode is declared, and the corresponding research output block from `stack-research.md` is produced.

### Step 1. Pre-flight

Read `references/preflight-and-constraints.md`. Answer the 6 pre-flight questions in writing:

1. **Domain.** What real-world job does this stack serve? Map to one of the 12 domain profiles in `domain-stacks.md` (or explicitly the closest match plus overrides).
2. **Team.** How many engineers, what's their existing language depth, who is on call when it breaks?
3. **Budget posture.** Free-tier scrappy, cash-efficient growth, or enterprise-indifferent-to-cost? Named posture, not a dollar figure.
4. **Time-to-ship.** Days, weeks, months, or no hard deadline?
5. **Scale ceiling.** What's the 12-month honest traffic and data estimate? Do not pick for Google-scale when the answer is 10k users.
6. **Regulatory and data-residency constraints.** HIPAA, PCI-DSS, SOC 2, GDPR, EU data residency, FedRAMP, state-specific privacy laws (CCPA, etc.). List the ones that apply; silence is not an answer.

If the request is vague ("what stack should I use for a SaaS"), do not interrogate the user. Pick the most plausible defaults (team of 2-5, cash-efficient growth, ship in weeks, US market, no explicit compliance needs stated), state them in one paragraph as assumptions, and proceed. The user will redirect if the defaults are wrong.

**Passes when:** all 6 pre-flight questions are answered in writing, and explicit assumption statements replace any missing answers.

### Step 2. Constraint map

Convert the pre-flight answers into hard constraints the stack must satisfy. Not preferences, constraints. A constraint rules out candidates; a preference weights them.

| Constraint type | Source | Example rule |
|---|---|---|
| Compliance | Regulated domain | "HIPAA PHI in the data layer" rules out managed services without a BAA |
| Data residency | EU / APAC / public sector | "Must keep data in EU" rules out US-only regions, some Convex/Firebase tiers |
| Self-host | Ops/security posture | "Must be self-hostable" rules out fully managed-only platforms |
| Offline | Field work, maritime, remote sites | "Must work offline" rules out network-always BaaS |
| Cost ceiling | Free-tier scrappy | "Zero paid services month 1" rules out Vercel Pro, WorkOS, Datadog |
| Team language | Incumbent skill | "Team is Python-only, no JS headcount" rules out Node-centric bundles unless the team is willing to learn |
| SLA / uptime | Enterprise customers | "99.95% contractual uptime" rules out single-region hobby tiers |
| Vendor independence | Exit strategy, acquisition risk | "Must be portable in 30 days" rules out platforms with no equivalent migration path |

**Passes when:** every pre-flight answer has been translated into either a hard constraint (rules out candidates) or a weighted preference (scores candidates). Constraints are listed explicitly.

### Step 3. Candidate generation

Read `references/domain-stacks.md` and pull the top 3 picks per dimension for the identified domain. Also read `references/stack-bundles.md` and pull the 3 pre-combined bundles for the domain (typically: Safe Default, Fast-to-Ship, Enterprise).

For each dimension, produce a shortlist of 2-4 candidates that pass the Step 2 constraints. Candidates that violate a hard constraint are dropped here, not scored.

Dimensions to cover (12):

1. **Framework** (fullstack meta-choice: Next.js, Remix, SvelteKit, Nuxt, Astro, Rails, Django, Laravel, Phoenix, FastAPI, etc.)
2. **Language / runtime** (TypeScript, Python, Ruby, Elixir, Go, Kotlin, Rust, etc.)
3. **Database** (Postgres, MySQL, SQLite, MongoDB, DynamoDB, Convex, Firebase Firestore)
4. **ORM / query layer** (Prisma, Drizzle, Kysely, SQLAlchemy, Ecto, ActiveRecord, raw SQL)
5. **Auth / identity** (Better Auth, Auth.js, Clerk, WorkOS, Supabase Auth, Firebase Auth, Devise, django-allauth, Keycloak)
6. **UI library / component layer** (shadcn/ui, Radix, Mantine, MUI, Chakra, Ant, headless + custom, Tailwind UI)
7. **Client state / data fetching** (TanStack Query, SWR, RTK Query, Apollo, Convex hooks, Server Components, Hotwire/Turbo, HTMX)
8. **Hosting / deploy** (Vercel, Netlify, Railway, Fly, Render, AWS, GCP, Azure, self-hosted VPS, Cloudflare)
9. **Observability** (Sentry, Datadog, New Relic, Honeycomb, Axiom, Grafana Cloud, OpenTelemetry self-host)
10. **Payments** (Stripe, Paddle, Lemon Squeezy, Braintree, Adyen, Stripe Connect for marketplaces)
11. **Email / notifications** (Resend, Postmark, SendGrid, AWS SES, Loops, Knock for in-app)
12. **Background jobs / queues** (Inngest, Trigger.dev, BullMQ, SQS, Sidekiq, Celery, Oban, Temporal)

**Passes when:** each dimension has 2-4 candidates listed with hard-constraint violations already filtered.

### Step 4. Pairing compatibility check

Read `references/pairing-rules.md`. Walk the anti-pairings table against every candidate pair. A bundle where two dimensions conflict is not a bundle; it is a future rewrite.

Common conflicts to reject here:

- **Convex + Prisma** (Convex is the data layer; stacking Prisma is fighting the platform).
- **Supabase + Firebase** (two competing BaaS is rarely the right call).
- **Clerk + Better Auth + WorkOS** (pick one identity provider; mixing creates user-record split-brain).
- **Vercel + AWS Lambda in the same app** (Vercel already runs on AWS Lambda; stacking adds a hop for no benefit).
- **Prisma + Drizzle in the same service** (one ORM per service; mixing creates two sources of schema truth).
- **shadcn/ui + MUI in the same app** (two design systems, one app, no survivors).
- **TanStack Query + SWR in the same app** (pick one cache layer).
- **Sidekiq + BullMQ** (two job queues is the wrong kind of polyglot).

If a conflict is intentional (e.g., migrating and running both temporarily), name it explicitly in Step 7.

**Passes when:** the surviving candidates form at least one viable bundle per domain profile (Safe Default, Fast-to-Ship, Enterprise) with no anti-pairings.

### Step 5. Scoring pass

Read `references/scoring-framework.md`. Apply the 12-dimension scoring under the user's weights (or the stated defaults if the user has not overridden).

Each candidate in each dimension gets a score 1-10 plus a one-line rationale. The aggregate bundle score is the weighted sum. Surface the top 3 bundles.

**Score rationale discipline:**
- Every score names what it scored on (DX, scale ceiling, ecosystem, cost, ops burden, compliance fit).
- No score above 9/10 unless the candidate is the consensus domain winner for the past 12+ months. 10/10 is reserved for "no rational alternative exists."
- No score below 3/10 unless the candidate has a documented failure mode in this domain. A 2/10 is "ship and regret"; a 1/10 is "do not ship."
- Scores are stack-dependent. Prisma is 8/10 for a small team on Next.js and 5/10 for a team with heavy SQL ops needs. Context shapes the number.

**Weighting discipline:**
- Default weights are published in `scoring-framework.md`. Users override by saying "weight DX high, cost low" or by providing a numeric vector.
- If a user has not overridden, state the default vector in the output.

**Passes when:** each shortlisted bundle has per-dimension scores with rationale, a weighted aggregate, and the weights used are stated.

### Step 6. Tradeoff narrative

Read `references/tradeoff-narratives.md`. For each shortlisted bundle, write:

1. **What flips it.** The failure mode that would make this bundle the wrong call. One paragraph, concrete.
2. **The scale ceiling.** The point where the stack starts fighting the team instead of helping. Often a user count, a data volume, a query-pattern shift, or a feature (e.g., "Convex hits its ceiling when you need SQL aggregations across tenants for reporting").
3. **The switching cost.** If they pick this and later want off, what is the rebuild bill? Weeks, months, full rewrite?

A recommendation without a flip point is a horoscope. A recommendation without a scale ceiling is a promise you can't keep. A recommendation without a switching cost is a trap.

**Passes when:** each shortlisted bundle has all three tradeoff narrative bullets. No narrative may be "none" or "unknown."

### Step 7. Migration path (Mode D only)

Read `references/migration-paths.md`. Produce a sequenced migration from X to Y covering:

1. **Blast radius.** What stops working temporarily, what risks permanent data loss, what integrations break.
2. **Sequence.** The order of steps, with parallel runs where possible (dual-write, dual-read) and cutover points.
3. **Rollback plan.** At each checkpoint, what reverts the system if a step fails.
4. **Data migration strategy.** Schema transforms, backfills, reconciliation queries, validation plan.
5. **Timeline and team cost.** Engineer-weeks honest estimate, not aspirational.

If the migration has a preferred staging environment (blue-green, canary tenants, read-only mode), call it out.

**Passes when:** the migration plan has all five components, identifies at least one rollback checkpoint per phase, and states the honest engineer-week cost.

### Step 8. Decision handoff

Produce `.stack-ready/DECISION.md` in the user's project directory. This artifact is the contract with future sessions, future teammates, and with `production-ready` if the user moves to implementation.

Contents:

```markdown
# Stack Decision

## Skill version
stack-ready 1.1.1, 2026-04-22. If a newer version runs this artifact through again, re-run the staleness check (Step 9) before making stack changes.

## Project
[one-line description]

## Pre-flight answers
- Domain: [...]
- Team: [...]
- Budget posture: [...]
- Time-to-ship: [...]
- Scale ceiling (12 months): [...]
- Regulatory constraints: [...]

## Hard constraints
- [...]

## Weighting
[default vector] OR [user-overridden vector, with reason]

## Chosen bundle

| Dimension | Choice | Score | Rationale |
|---|---|---|---|
| Framework | ... | ... | ... |
| ... | ... | ... | ... |

Aggregate score: X.X / 10

## Runner-up bundle
[one table, abbreviated]

## What flips this decision
[concrete failure mode paragraph]

## Scale ceiling
[where the stack starts fighting the team]

## Switching cost
[rebuild bill estimate]

## Rejected bundles and why
- [bundle]: [reason it lost]

## Prior art and analogous picks
Three real deployments with a comparable stack at comparable scale, each in one line:
- [Project / company]: [stack summary]. [Status / how it's held up, with a date if known.]
- [Project / company]: [stack summary]. [Status.]
- [Project / company]: [stack summary]. [Status.]

(Borrowed from Rust's RFC process. "We looked at three real deployments" is the strongest defense against horoscope-shaped recommendations. If prior art can't be named honestly, the pick is more novel than claimed; reconsider.)

## Open questions left to the user
- [question] (owner: [name], due: [date])

## Handoff
- To `production-ready`: this decision is the Step 2 architecture-note stack bullet.
- To `repo-ready`: stack detected; generate CI/lint/test for [language / runtime].
```

**Passes when:** `.stack-ready/DECISION.md` exists and is complete per the template. Missing sections block the handoff.

### Step 9. Staleness check

Stack recommendations rot. At the end of every run, print:

```
Skill version: stack-ready 1.1.1
Last updated: 2026-04-22
Current date: [today]
```

If the skill version is older than 6 months relative to today, warn the user before relying on the output. Call out dimensions most likely to have shifted (frameworks, pricing tiers, new entrants): auth providers, AI/ML tooling, and hosting pricing have historically churned fastest. Point the user at the project repo for the latest CHANGELOG and matrix updates.

**Passes when:** the skill version and date are printed, and a staleness warning is surfaced if the skill is >6 months old.

## Completion tiers

Four tiers. Each is independently shippable, each declarable at a boundary, each audit-able.

### Tier 1: Shortlist (mandatory, always)

The user has a viable list of candidate bundles that pass their hard constraints.

| # | Requirement |
|---|---|
| 1 | **Mode declared.** A, B, C, or D, with the research block from `stack-research.md`. |
| 2 | **Pre-flight answered.** All 6 questions in writing, or explicit assumptions for any gaps. |
| 3 | **Constraints mapped.** Every pre-flight answer converted into a hard constraint or weighted preference. |
| 4 | **Candidates generated.** 2-4 viable options per dimension, hard-constraint violators removed. |
| 5 | **At least one bundle proposed.** Safe Default or domain-matched, with no obvious anti-pairings. |

**Proof test:** the user can point at a named stack and say "why did this survive." Every surviving candidate must have a one-line answer.

### Tier 2: Scored (recommended for most users)

The shortlist is ranked with stated weights and no pairing conflicts.

| # | Requirement |
|---|---|
| 6 | **Pairing check complete.** Every proposed bundle passed the anti-pairings table. |
| 7 | **Every dimension scored.** 1-10 with one-line rationale per candidate. |
| 8 | **Weights stated.** Default vector or user override, either way made explicit. |
| 9 | **Aggregate ranked.** Top 3 bundles with weighted aggregate scores. |

**Proof test:** the user can see *why* bundle A beat bundle B. The answer is in the numbers and the rationales, not in the skill's say-so.

### Tier 3: Justified (ship-ready recommendation)

The recommendation has failure modes, scale ceilings, and switching costs named. A reader six months from now can understand why this was picked and when to reconsider.

| # | Requirement |
|---|---|
| 10 | **Flip point documented.** Each shortlisted bundle names the failure mode that would reverse the choice. |
| 11 | **Scale ceiling named.** Concrete metric: user count, data volume, query pattern, feature boundary. |
| 12 | **Switching cost honest.** Weeks or months to move off, stated in engineer-weeks, not wishful. |
| 13 | **Rejected bundles explained.** Why the losers lost, not just that they lost. |

**Proof test:** a new engineer reads `DECISION.md` six months later and understands not just the pick but the reasoning. They can tell whether the flip point has been hit.

### Tier 4: Decided (handoff complete)

The decision is written down, handed off, and composable with the rest of the ready-suite.

| # | Requirement |
|---|---|
| 14 | **`.stack-ready/DECISION.md` written** with every section of the template filled. |
| 15 | **Handoff declared.** Either "no implementation planned" or an explicit `production-ready` handoff with the stack bullet pre-filled. |
| 16 | **Staleness check printed.** Skill version, last-updated date, current date. |
| 17 | **Open questions listed.** Anything the user still needs to decide, with owner and deadline. |
| 18 | **No anti-pattern remains.** Every item in the have-nots list passes. |

**Proof test:** a separate agent with no memory of the conversation reads `DECISION.md` and can start `production-ready` from Step 1 without asking the user another stack question. If they have to ask, Tier 4 is not complete.

## The "have-nots": things that disqualify the recommendation at any tier

If any of these appear, the recommendation fails and must be fixed:

- A score with no stated weighting (reads as "objective" when it is not).
- A bundle with an unresolved anti-pairing from `pairing-rules.md`.
- A recommendation with no flip-point paragraph (horoscope territory).
- "It depends" as a final answer. Depends on *what*. State the variable, then decide under stated assumptions.
- A library recommendation that hasn't been checked for current maintenance (archived repo, last commit >18 months, no active releases). Dead-library suggestions are ghost recommendations.
- A managed service recommended into a compliance-constrained domain without BAA, SOC 2, or equivalent documented (HIPAA apps on services with no BAA, PCI-DSS apps on providers that don't support SAQ-A).
- A self-host recommendation without naming the ops cost (if the team is 2 engineers, "self-host Postgres on Kubernetes" is a scale-ceiling trap, not a stack choice).
- A recommendation based on a trend ("because it's popular," "because it's new") rather than a domain fit.
- Any undisclosed commercial tie. If you have a relationship with a vendor being scored, disclose it in the output or recuse that score.
- A stack recommendation without a date stamp. An undated rec is a dated rec with the date hidden.
- A migration plan (Mode D) without a rollback checkpoint for every phase.
- Cost ceilings that ignore egress, seat pricing, or the free-tier cliff. "Free until you need auth" is not free.
- Recommending "microservices" to a team of 2 with no scale forcing function. The complexity floor is higher than the complexity they are trying to avoid.
- Recommending a framework version that does not exist yet (Next.js 20 when Next.js 15 is current, Rails 9 when Rails 8.1 ships). Pin to released versions, note upcoming versions separately.

When you catch yourself about to write any of these, fix it before proceeding. A broken recommendation is worse than no recommendation; the user will act on it.

## Reference files: load on demand

The body above is enough to start. Load each reference *before* the step that uses it, not after.

| Reference file | When to load | ~Tokens |
|---|---|---|
| `stack-research.md` | **Always.** Start of every session (Step 0). | ~8K |
| `preflight-and-constraints.md` | **Always.** Step 1 and Step 2. | ~7K |
| `domain-stacks.md` | **Tier 1.** Step 3 candidate generation; the domain matrix. | ~22K |
| `stack-bundles.md` | **Tier 1.** Step 3, to pull pre-combined bundles per domain. | ~12K |
| `pairing-rules.md` | **Tier 2.** Step 4 compatibility check. | ~6K |
| `scoring-framework.md` | **Tier 2.** Step 5 scoring pass; weighting defaults. | ~9K |
| `dimension-deep-dives.md` | **On demand.** Open per dimension when a candidate is close-call. | ~16K |
| `tradeoff-narratives.md` | **Tier 3.** Step 6; flip points, scale ceilings, switching costs. | ~11K |
| `migration-paths.md` | **Mode D only.** Step 7; X-to-Y migration sequences. | ~13K |
| `RESEARCH-2026-04.md` | **On demand.** When the user asks "why this score" or "what's the evidence"; source citations for 1.1.0's refresh. | ~30K |
| `stack-antipatterns.md` | **Tier 2 + Mode C audits.** Named-failure-mode catalog with grep tests, severity, and per-skill guards. Loaded at every tier-gate check. | ~5K |
| `EXAMPLE-STACK.md` | **On demand.** A complete worked example stack decision for a fictional B2B SaaS pilot (Pulse, a Customer Success ops platform). Demonstrates a constraint map sourced from upstream PRD and architecture, nine ranked-shortlist categories with scoring rationale per candidate, pairing compatibility checks, an itemized bundle summary against the cost ceiling ($50/mo of a $400/mo cap), and eight stack-level ADRs naming alternatives and migration paths. Passes the skill's grep tests for vibe-stack / resume-driven / premature-scale / decoupled-from-architecture / cost-blind failure modes. Consumes the worked PRD, architecture, and roadmap from their respective sibling repos. | ~14K |

Skill version and change history live in `CHANGELOG.md`. When resuming a project, confirm the skill version your session loaded matches the version recorded in `.stack-ready/STATE.md` if one exists. A skill update between sessions can move scores, add candidates (Convex released a new tier, Cloudflare acquired a vendor, Prisma published a major version), or change anti-pairings. If versions differ, re-run the scoring pass on the shortlisted bundles before continuing.

## Suite membership

stack-ready is the planning-tier skill that picks the technology bundle. See `SUITE.md` at the repo root for the full map. The relevant siblings at a glance:

- **Planning tier:** `prd-ready` (what), `architecture-ready` (how), `roadmap-ready` (when), `stack-ready` (this skill, with what tools).
- **Building tier:** `production-ready` (the app), `repo-ready` (the repo scaffolding).
- **Shipping tier:** `deploy-ready` (ship it), `observe-ready` (keep it healthy), `launch-ready` (tell the world), `harden-ready` (survive adversarial attention).

Skills are loosely coupled: each stands alone, each composes with the others via well-defined artifacts. No skill routes through another; the harness is the router. Install what you need.

## Consumes from upstream

When the agent starts, it checks for upstream artifacts and pre-fills the pre-flight from them rather than asking the user to repeat decisions already made. Absence is fine; the skill runs standalone on its own defaults.

| If present | stack-ready reads it during | To pre-fill |
|---|---|---|
| `.prd-ready/PRD.md` | Step 1 (pre-flight) and Step 2 (constraint map) | Domain, target users, non-functional requirements, budget posture, team size, time-to-ship, and any compliance or data-residency constraints that rule out candidates. |
| `.architecture-ready/ARCH.md` | Step 1 and Step 2 | System shape (monolith vs. services, sync vs. async), the component breakdown, and the non-functional targets the stack must satisfy (a relational store with tenant scope, a worker entry point, structured logging). |

If neither is present, the skill states its assumptions in one paragraph and proceeds. If an upstream artifact *contradicts* the running code (Mode B or C), trust the code and note the drift. Upstream artifacts are historical records, not current-state overrides.

## Produces for downstream

stack-ready emits the stack decision for downstream skills and future sessions to consume. Writing it is the skill's definition of done.

| Artifact | Path | Consumed by |
|---|---|---|
| **Stack decision** | `.stack-ready/DECISION.md` | `production-ready` reads the locked-in technology set to build slices against without re-litigating the choice. `repo-ready` reads it to scaffold the matching CI matrix, linter, and platform configs. `deploy-ready` reads the hosting and database picks for the topology note. |
| **Session state** | `.stack-ready/STATE.md` | The next stack session (Mode C audit or Mode D migration) reads to resume scoring without re-deriving the shortlist. |

If a downstream skill is not installed, stack-ready still produces these artifacts. They cost nothing to emit and make the suite extensible.

## Session state and handoff

Stack decisions can span sessions, especially in Mode C (audit) or Mode D (migration). Maintain `.stack-ready/STATE.md` when the work is ongoing.

**Template:**

```markdown
# Stack-Ready State

## Skill version
stack-ready 1.1.1, 2026-04-22.

## Current tier
Working toward Tier [N]. Last completed tier: [N-1].

## Mode
A / B / C / D.

## Pre-flight answers
(copied from the run)

## Hard constraints
(copied from the run)

## Shortlisted bundles
- Bundle A: [name] - scored [X.X]
- Bundle B: [name] - scored [X.X]
- Bundle C: [name] - scored [X.X]

## Leaning toward
[Bundle name] because [one line]. Not yet decided.

## Open questions blocking decision
- [Q]: [who owns the answer]

## Last session note
[ISO date] [what happened, what's next]
```

**Rules:**
- STATE.md is the contract with the next session. Update at every tier boundary and every context compaction.
- Never delete STATE.md. If an entry is wrong, correct it in place with a dated note.
- If `DECISION.md` exists (Tier 4 reached), STATE.md can be archived; DECISION.md is now the source of truth.

## Handoff: implementation is not this skill's job

Once the decision is made, hand off.

- To **`production-ready`**: the chosen bundle becomes the Step 2 architecture-note stack bullet and the Step 1 pre-flight answer to question 3. Invoke `production-ready` directly on harnesses that support skill invocation; otherwise, instruct the user to run it.
- To **`repo-ready`**: pass the language, framework, and platform so it can generate stack-appropriate CI, lint, and test configs. On skill-invocation harnesses, invoke directly. Otherwise surface as a recommendation.

Do **not** begin building the app or configuring the repo from this skill. Scope fence is strict: stack-ready stops at the decision.

## Keep going until it's actually decided

The shortlist existing is roughly 30% of the work. The scoring is another 30%. The remaining 40% is the tradeoff narrative, the flip points, the scale ceiling, the switching cost, the rejected-bundle explanations, and the `DECISION.md` artifact that makes the decision portable. A user who walks away with "I think we should use Next.js, Postgres, and Prisma" but no flip-point paragraph does not have a decision; they have an opinion they will relitigate in three months.

When in doubt, imagine the user in month three, standing in front of their team, justifying the stack pick to a new hire or a skeptical lead. The first question they can't answer is the next thing to write down.
