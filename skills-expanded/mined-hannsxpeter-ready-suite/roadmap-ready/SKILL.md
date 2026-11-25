---
name: roadmap-ready
description: "Sequence software work over time with discipline. Ingests the PRD (from prd-ready) and the architecture dependency graph (from architecture-ready); requires a team-capacity input; produces a Markdown `ROADMAP.md` with Now-Next-Later horizons, named milestones with completion gates, topologically-sorted slice queues for production-ready, cutover cadence for deploy-ready, KPI handoffs for observe-ready, and explicit launch-milestone gate dates for launch-ready. Refuses fictional precision (Gantt-to-the-day with no capacity input), fictional parallelism (more concurrent tracks than engineers), quarter-stuffing (all four quarters equally full), speculative features (items absent from the PRD or architecture), feature-factory output (rows that are bare feature names with no outcome or commitment), shelf roadmaps (written once, never consulted), and roadmap theater (Gantt aesthetics with no commitments). Triggers on 'build a roadmap,' 'milestone plan,' 'quarterly plan,' 'sequence the work,' 'Now-Next-Later,' 'Shape Up cycle,' 'PI planning,' 'what ships first,' 'when does the beta happen,' 'roadmap for this quarter.' Does not redefine the product (prd-ready), design the architecture (architecture-ready), pick the stack (stack-ready), build the app (production-ready), scaffold the repo (repo-ready), deploy (deploy-ready), monitor (observe-ready), or launch (launch-ready). Planning tier; consumes `.prd-ready/PRD.md` and `.architecture-ready/ARCH.md`; produces `.roadmap-ready/ROADMAP.md` and `HANDOFF.md`. Full trigger list in README."
version: 3.1.0
updated: 2026-11-23
changelog: CHANGELOG.md
suite: ready-suite
tier: planning
upstream:
  - prd-ready
  - architecture-ready
downstream:
  - stack-ready
  - production-ready
  - deploy-ready
  - observe-ready
  - launch-ready
pairs_with:
  - prd-ready
  - architecture-ready
  - stack-ready
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

# Roadmap Ready

This skill exists to solve one specific failure mode. A founder, PM, or engineering lead opens a new Notion doc, types "build a roadmap for the next 6 months" into ChatGPT, Claude, or Productboard AI, and pastes the output. What ships is a grid with four columns labeled Q1, Q2, Q3, Q4, each stuffed with roughly the same number of feature titles, each with a date to the day, half of which name features that are not in the PRD and the other half lack any outcome framing. Three parallel tracks are assumed for a team of two engineers. Dependencies between features are visible to anyone who has read the architecture doc but are not encoded anywhere in the roadmap. The launch milestone exists but has no readiness gates underneath it (observability live, rollback tested, runbooks reviewed). The document is printed, signed off, filed. Six weeks later it is stale. Engineering works from the sprint backlog. The roadmap becomes a polite artifact for investor decks. Nobody cites it when a tradeoff call comes up.

The job here is the opposite. Produce a roadmap whose every item maps back to a specific PRD section and a specific architecture component. Whose sequencing respects the topological order of the architecture dependency graph. Whose horizon length is chosen from a named cadence model (Shape Up 6+2, quarterly themes, SAFe PI, milestone-based, continuous delivery with rollout calendar) with the rationale stated. Whose precision decreases across horizons: Now is specific and owned, Next is directional, Later is thematic and fuzzy by design. Whose parallel-track count never exceeds the team-size input. Whose launch milestone names explicit readiness gates (observability live, rollback tested, support runbooks reviewed) with dates, not feelings. Whose public-facing derivative is a separate redacted view, not the same file. Whose every feature row is either an outcome-framed direction or a high-integrity commitment with a named reason, and never a bare feature name with no rationale. If the roadmap cannot answer "why this next, not something else," it is not ready.

This is harder than it sounds because roadmaps fail in a narrow band that looks like success. Every LLM-generated roadmap fills every cell; precision is visually high; stakeholders nod. The industry converges on the same ten failure modes under slightly different names: John Cutler's feature factory (2016), Melissa Perri's build trap (2018), Marty Cagan's feature-roadmap critique (SVPG 2015), Janna Bastow's Now-Next-Later (ProdPad 2012), Ryan Singer's fixed-time-variable-scope (Shape Up 2019), and the emerging-but-unowned terms (roadmap theater, fictional parallelism, quarter-stuffing, speculative roadmap, shelf roadmap). Every source is cited in [`references/RESEARCH-2026-04.md`](references/RESEARCH-2026-04.md). Tooling does not catch any of them. Productboard, Aha!, Linear, Jira, and ChatPRD will render any roadmap you hand them; none of them will tell you that the parallelism you drew exceeds your team size, or that two items in Q2 depend on a Q3 item, or that the launch milestone has no observability-live date underneath it. The skill is the layer above the tool that catches the roadmap shape before it ships to engineering.

## Core principle: grounded commitment, outcome-framed direction, or named open question

> **Every item on the roadmap is exactly one of three things: a grounded commitment (fixed date and fixed scope, with a named reason and signed off), an outcome-framed direction (target outcome with appetite or confidence band), or a named open question (explicit "we do not yet know" with an owner and a due date). Nothing else. No bare feature names. No invented dates. No invisible parallelism. No work that is not in the PRD.**

This principle is non-negotiable. The entire taxonomy of roadmap failure reduces to items that pretend to be commitments but are not grounded, directions that pretend to be commitments, or commitments that pretend to be directions. The feature factory (Cutler) is items listed with no outcome; the build trap (Perri) is the institutional symptom; roadmap theater is dates asserted with no capacity; fictional parallelism is tracks that exceed team size; quarter-stuffing is everything asserted at the same precision regardless of horizon; speculative roadmap is items invented without upstream reference; shelf roadmap is commitments unrefreshed after cycle boundaries; polish-indefinitely is extensions without explicit decision. Every one of these is a misclassification: a thing that is not a grounded commitment is being treated as if it were.

The three-label test is auditable row by row. For every item on the roadmap, answer: is this a grounded commitment (a date, a scope, a named reason, and a sign-off), an outcome-framed direction (a target outcome and an appetite or a confidence band), or a named open question (an unknown with an owner and a review date)? If an item is none of the three, it is theater and must be rewritten or cut. The skill enforces this row-by-row at every tier gate; see [`references/roadmap-antipatterns.md`](references/roadmap-antipatterns.md) section 1 for the procedure.

The grounding corollary. Every grounded commitment and every outcome-framed direction must reference an upstream artifact: a PRD section from `.prd-ready/PRD.md`, an architecture component from `.architecture-ready/ARCH.md`, or a named external constraint (regulatory date, partner launch, contract clause). An item with no upstream reference is speculative and must be either cut or routed back to prd-ready for inclusion. This is the defense against AI-generated "reasonable-sounding" feature names that no one has actually specced. See [`references/sequencing-principles.md`](references/sequencing-principles.md) section 3.

The capacity corollary. The roadmap refuses to commit dates without a team-capacity input. Team size in engineers, available engineer-weeks per cycle, and serial-fraction estimate (Amdahl's law applied to coordination overhead) are required before any dated commitment is emitted. Without them, the skill produces direction without dates, explicitly labeled as such. See [`references/dependency-graph.md`](references/dependency-graph.md) section 4 for the capacity-matching procedure.

## When this skill does NOT apply

Route elsewhere if the request is:

- **Defining the product or writing the PRD** ("write a PRD," "product spec," "requirements doc," "what should we build"). That is [`prd-ready`](https://github.com/hannsxpeter/ready-suite/tree/main/skills/prd-ready). roadmap-ready consumes the PRD's priorities, dependencies, appetite, and no-gos from `.prd-ready/HANDOFF.md`; it does not decide what the product is or what belongs in it. A roadmap that adds a feature not in the PRD has violated the scope fence; route the feature back to prd-ready.
- **Designing the architecture or drawing the dependency graph** ("draw the system diagram," "what components do we need," "how do services talk," "where is the trust boundary"). That is [`architecture-ready`](https://github.com/hannsxpeter/ready-suite/tree/main/skills/architecture-ready). roadmap-ready reads `.architecture-ready/HANDOFF.md` for the component DAG and uses it for topological sequencing; it does not decide the DAG. If an item has no architecture-component reference, route the decomposition to architecture-ready.
- **Picking the stack** ("what framework," "Next.js vs. Remix," "pick an ORM," "should we use Supabase"). That is [`stack-ready`](https://github.com/hannsxpeter/ready-suite/tree/main/skills/stack-ready). roadmap-ready may reference stack decisions ("the Postgres migration ships in M3") but does not decide what Postgres replaces or what ORM wraps it. Stack decisions are their own planning-tier skill.
- **Building the app or writing code** ("wire the dashboard," "implement the checkout," "add RBAC"). That is [`production-ready`](https://github.com/hannsxpeter/ready-suite/tree/main/skills/production-ready). roadmap-ready emits a slice queue for production-ready to drain; it does not drain it. A roadmap item with implementation detail ("uses Bull queue for background jobs") has overreached; cut the detail.
- **CI/CD pipeline design, zero-downtime migrations, rollback protocol** ("set up the pipeline," "expand/contract migration," "blue/green"). That is [`deploy-ready`](https://github.com/hannsxpeter/ready-suite/tree/main/skills/deploy-ready). roadmap-ready names the cutover cadence ("milestone 3 ships to production on 2026-06-12"); deploy-ready wires the pipeline. Do not draft pipeline YAML in the roadmap.
- **Observability setup, SLO authorship, alerting, runbooks** ("add Datadog," "define an SLO," "write a runbook"). That is [`observe-ready`](https://github.com/hannsxpeter/ready-suite/tree/main/skills/observe-ready). roadmap-ready may include "observability wiring" as a slice with a target cycle and the KPIs the launch should move; observe-ready owns the dashboard content and alert thresholds.
- **Launch marketing, landing page, waitlist, OG cards, Product Hunt coordination** ("launch my product," "build a landing page," "Show HN," "waitlist"). That is [`launch-ready`](https://github.com/hannsxpeter/ready-suite/tree/main/skills/launch-ready). roadmap-ready identifies the launch milestone, names the launch mode (hard, soft, beta, GA, Product Hunt, etc.), and lists the pre-launch dependencies; launch-ready runs the launch.
- **Repo scaffolding and CI hygiene** ("CONTRIBUTING.md," "CODEOWNERS," "release automation"). That is [`repo-ready`](https://github.com/hannsxpeter/ready-suite/tree/main/skills/repo-ready). roadmap-ready may include "repo hardening" as a slice, not as implementation detail.
- **Team hiring, capacity planning, head-count modeling, who does what**. roadmap-ready takes team size as an input constraint; it does not decide the team. Hiring plans live in HR-land.
- **Financial forecasting, burndown charts, velocity modeling, story-point estimation**. roadmap-ready uses rough size labels (S / M / L / XL, or days / weeks) or Shape Up appetites (small batch / big batch). Detailed estimation is the team's local process, not this skill's output.
- **Agile ceremony design** (standups, retros, sprint planning, grooming, refinement). roadmap-ready owns the cadence choice ("quarterly themes with monthly check-ins," "Shape Up 6+2"); it does not design the daily or weekly rituals.
- **Project management tool choice** (Linear vs. Jira vs. Productboard vs. Aha!). roadmap-ready outputs a canonical Markdown `ROADMAP.md` that any tool can import; it does not pick the tool.
- **OKR authorship and business goal-setting**. Objectives come from the business. roadmap-ready consumes them from the PRD's success criteria and organizes work to move them; it does not set them.
- **Deadlines imposed from outside the team** (investor pressure, conference demos, competitor launches). roadmap-ready helps model what is feasible given a deadline; it does not validate or negotiate the deadline. "Can this ship by July?" is answered with scope-that-fits, not scope-we-wish-for.
- **Discovery, user research, opportunity identification**. That is upstream of the PRD; Teresa Torres's opportunity-solution-tree practice lives in discovery. roadmap-ready consumes resolved opportunities (through the PRD), not open ones.

This section is the scope fence. Every plausible trigger overlap with a sibling has a route-elsewhere line.

## Workflow

Follow this sequence. Skipping steps produces the exact class of failure this skill exists to prevent: a roadmap that fills every cell, looks balanced, decides nothing specific, and is stale at the next cycle boundary.

### Step 0. Detect roadmap state and mode

Read [`references/roadmap-research.md`](references/roadmap-research.md) and run the mode detection protocol. One of six modes must be declared in writing before any other step.

- **Mode A (Greenfield).** No prior roadmap. Start from cadence selection (Step 2) and the PRD ingestion (Step 3). Paired with `prd-ready` Tier 2+ and `architecture-ready` Tier 1+ as upstream.
- **Mode B (AI-slop roadmap exists).** A roadmap has already been generated by an LLM, a PM tool's AI feature, or a ChatPRD pass. The ask is "fix this before sign-off." Run the Mode B audit (Step 1.5); rewrite items that fail the three-label test; cut items without upstream references.
- **Mode C (Iteration / refresh).** Prior roadmap exists; one cycle (or one quarter) has passed; actuals are in. The ask is "re-plan the next horizon." Retain the grounded commitments, re-sequence the directions, update the open questions. This is the default healthy mode. See [`references/review-cadence.md`](references/review-cadence.md) section 2.
- **Mode D (Pivot).** New target user, new problem, materially different success metric. Upstream PRD has forked. Fork a new ROADMAP.md; cross-link to the prior one; do not overwrite. A pivot at the PRD level always forks the roadmap.
- **Mode E (Rescue / stall).** Roadmap was committed, build started, work stalled, commitments slipping. Diagnose the dominant cause: scope exceeded appetite (Shape Up circuit-breaker applies), dependency missed in sequencing (return to Step 4 with DAG), capacity over-committed (re-run Step 1), or discovery gap (route to prd-ready). See [`references/review-cadence.md`](references/review-cadence.md) section 4.
- **Mode F (Freeze).** Launch milestone is approaching; the pre-launch cut line is active. No new items accepted; every proposed addition is routed to the post-launch backlog. See [`references/launch-sequencing.md`](references/launch-sequencing.md) section 5.

**Passes when:** a mode is declared in writing and the corresponding research block from `roadmap-research.md` is produced. For Mode B, at least one failing item is quoted with its failure label. For Mode E, the dominant stall cause is named before any re-sequence is attempted.

### Step 1. Pre-flight inputs

Read [`references/sequencing-principles.md`](references/sequencing-principles.md). Answer the 8 pre-flight questions in writing. Missing answers become explicit assumptions or flagged open questions; do not fabricate.

1. **Team capacity.** Number of engineers (and designers, if the roadmap includes design work); engineer-weeks available per cycle; on-call or support rotation share that is not roadmap work. Without this, no dated commitment is emitted.
2. **Cadence choice.** Continuous delivery, milestone-based, Shape Up 6+2, quarterly themes, SAFe PI, or a declared hybrid. Selected via [`references/cadence-models.md`](references/cadence-models.md) selection matrix, not defaulted.
3. **Horizon length.** The farthest time the roadmap commits to explicitly. Shape Up: 6 weeks for a bet, plus a shape for the next. Quarterly: 3 months. SAFe: 10-12 weeks per PI. Linear / continuous: 4-6 weeks of Now, plus 3 months of Next, plus direction for Later.
4. **Hard external dates.** Regulatory deadlines, partner launches, contract clauses, conference demos. Each one is a commitment input; each feeds a potential launch milestone.
5. **Audience of the roadmap.** Internal only, internal plus execs, internal plus customers (public roadmap), mixed (internal canonical plus a public derivative). Drives Step 10.
6. **Risk tolerance.** Continuous-delivery tolerance is highest (can roll back fast). PI-planning tolerance is lowest (commitments last 10-12 weeks). Affects cadence choice and scope-cut discipline.
7. **Existing commitments.** Promises that predate this roadmap (contracts, past-investor commitments). Each is grounded-commitment-labeled in the output or explicitly renegotiated.
8. **Upstream artifact state.** Is `.prd-ready/PRD.md` at Tier 2 or above? Is `.architecture-ready/ARCH.md` at Tier 1 or above? If either is missing, the roadmap degrades (Step 3 fallback); if either is at Tier 1 Brief or lower, the roadmap's precision ceiling is lower.

If the user's input is one sentence ("build a roadmap for the next quarter"), do not invent eight answers. Ask the minimum set that defaults cannot cover, state explicit assumptions for the rest, and proceed with a Tier 1 Sketch. No dated commitment is emitted until the capacity answer is real.

**Passes when:** all 8 pre-flight questions are answered in writing; explicit assumptions replace any missing answers; if team capacity is null, no dated commitment is emitted at any tier until it is filled.

### Step 1.5. Mode B audit (only if a prior AI-slop roadmap exists)

Skip if not Mode B. Otherwise, read [`references/roadmap-antipatterns.md`](references/roadmap-antipatterns.md) and run the audit:

- Quote every item on the existing roadmap. For each, apply the three-label test: grounded commitment, outcome-framed direction, or named open question? Unlabeled items are marked for rewrite or cut.
- Quote every date. Apply the capacity check: with the stated team size and cadence, is this date feasible? Gantt-to-the-day precision without capacity input is fictional precision; mark for confidence-band relabel or cut.
- Count parallel tracks in each period. If the count exceeds team capacity, mark the excess tracks for re-sequencing (fictional parallelism).
- Cross-reference every feature against `.prd-ready/PRD.md`. Items absent from the PRD are speculative; route back to prd-ready or cut.
- Scan for quarter-stuffing: are Q1, Q2, Q3, Q4 filled to visual balance at identical precision? Flag and re-shape using Now-Next-Later precision gradients.
- Scan for launch milestones: does each launch name observability-live, rollback-tested, and runbook-reviewed sub-items? If not, the launch is unsequenced; re-plan via [`references/launch-sequencing.md`](references/launch-sequencing.md).

Output the audit as a list of specific defects with the failing quote and the required remediation. Name the dominant failure mode(s) before any rewrite. Proceed to the regular workflow.

**Passes when:** every failing item has a specific defect quote; the dominant failure mode is named (fictional precision / fictional parallelism / quarter-stuffing / speculative / feature-factory / shelf / roadmap-theater); a Mode B remediation plan is written down.

### Step 2. Cadence selection

Read [`references/cadence-models.md`](references/cadence-models.md). Run the selection matrix. The cadence is not a preference; it is a decision with a rationale tied to team size, risk tolerance, customer expectations, and existing organizational process.

Match the team profile to one of seven candidate cadences:

- **Shape Up 6+2** (6-week cycles, 2-week cool-down, betting table at cycle boundary). Good fit: 5-40 engineers, product-led, autonomy, no fixed-scope obligations. Bad fit: regulated rollouts, PI-dependent coordination.
- **Quarterly themes with monthly check-ins** (themes per quarter, monthly review cadence, weekly sprints underneath). Good fit: 30-300 people, OKRs in use, board cadence aligned to quarters.
- **SAFe PI planning** (8-12 week Program Increments, PI planning event, Scrum underneath). Good fit: 100+ engineers, multiple ARTs, regulated or safety-critical.
- **Continuous delivery with rollout calendar** (no release cadence, feature-flag rollout from N% to 100%, risk calendar). Good fit: consumer SaaS at scale, strong DevOps, feature-flag infra.
- **Milestone-based** (named releases 1.0 / 1.1 / 2.0 tied to public or contractual events). Good fit: mobile, enterprise with GA gates, hardware-adjacent.
- **Hybrid: quarterly themes plus Shape Up bets underneath**. Good fit: 40-150 engineers, growth-stage SaaS, product-led but with exec-reporting cadence.
- **Hybrid: milestone release calendar plus continuous-delivery within**. Good fit: B2B SaaS with named customer GAs and internal continuous deploy.

The cadence decision is a one-paragraph ADR-shaped statement: "We choose [cadence] because [team-size-and-risk reasoning]. Alternatives considered: [at least two]. Trigger for re-evaluation: [when we'd revisit]." A roadmap without a declared cadence is a roadmap that will drift toward whatever cadence the PM tool defaults to, which is usually Gantt.

**Passes when:** one cadence is declared with a written rationale; at least two alternatives are named and rejected; the cadence is consistent with the team-size and risk-tolerance pre-flight answers.

### Step 3. Ingest upstream artifacts

Read `.prd-ready/HANDOFF.md` (for priorities, dependencies, appetite, no-gos, rabbit holes) and `.architecture-ready/HANDOFF.md` (for the component dependency graph, load-bearing-first ordering, risk-ordered architecture items). If either artifact is at a lower tier or absent, degrade as follows:

| Upstream state | Roadmap precision ceiling |
|---|---|
| PRD at Tier 2 (Spec) or higher AND ARCH at Tier 1 (Sketch) or higher | Tier 3 Committed or Tier 4 Public-ready permitted |
| PRD at Tier 1 (Brief) only OR ARCH absent | Tier 2 Plan max; directional only, no grounded commitments beyond this cycle |
| PRD absent | Tier 1 Sketch max; flag that the roadmap is a feature wishlist until the PRD lands |
| ARCH absent but PRD present | Tier 2 Plan max; flag that sequencing risks missing dependencies until ARCH lands |

Every item on the roadmap references at least one upstream anchor: a PRD section, an architecture component, or a named external constraint. Items with no anchor are either speculative (route back to prd-ready) or external (tagged with the constraint).

Build the working dependency graph. From `.architecture-ready/HANDOFF.md`, extract the component DAG. Topologically sort. Items whose architecture components have no dependencies go first; items with prerequisites go after them. If the roadmap schedules A before B when A depends on B, the roadmap is incoherent; re-sequence.

**Passes when:** every roadmap item has at least one upstream anchor reference; the precision ceiling from the degradation table is applied; the topological order of architecture dependencies is reflected in the Now and Next columns.

### Step 4. Sequencing pass

Read [`references/sequencing-principles.md`](references/sequencing-principles.md) sections 2 and 4, plus [`references/risk-driven-prioritization.md`](references/risk-driven-prioritization.md). Sequence the items within the chosen cadence.

The sequencing is a layered decision:

1. **Topological order first.** If A depends on B, B goes first. Non-negotiable.
2. **Risk-driven layering.** Among items that could be sequenced in either order, items that resolve the highest-risk unknowns (Eric Ries's "leap-of-faith assumptions") go earlier. The cheapest time to discover "this won't work" is before the cheap things have been built on top of it.
3. **Appetite fitting (Shape Up).** If the cadence is Shape Up, every item gets an appetite (small batch 2 weeks, big batch 6 weeks). Items that do not fit are shaped smaller or deferred; they are not carried forward at full scope.
4. **Capacity check.** At no point does the count of concurrent tracks in one period exceed the team-capacity input. This is the fictional-parallelism guard.
5. **Prioritization framework overlay (optional).** RICE, ICE, WSJF, MoSCoW, Kano, Opportunity Scoring, or appetite-first may be applied for ranking within a horizon; the choice is declared. See [`references/risk-driven-prioritization.md`](references/risk-driven-prioritization.md) sections 1-8 for the compatibility matrix.
6. **Amdahl's law sanity check.** Doubling team size does not double throughput; the serial fraction (reviews, coordination, cross-team dependencies) caps the achievable parallelism. Flag Now-column items whose apparent parallelism assumes zero serial overhead.

**Passes when:** the Now column respects topological order; no period has more concurrent tracks than team capacity; highest-risk items are in the earliest position they can be scheduled to; a prioritization framework (or "appetite-first") is declared; and the Amdahl-check note is recorded.

### Step 5. Milestone anatomy

Read [`references/roadmap-anatomy.md`](references/roadmap-anatomy.md) section 2 on milestones. At least one milestone must exist for any roadmap at Tier 2 or higher.

A milestone is a named set of slices with a completion gate. Every milestone has:

1. **Name.** Concrete. "M2: Onboarding redesign" not "Q2 Objectives."
2. **Target date or date range.** A single date with a confidence band ("2026-06-30, 70%"), a range ("end of June 2026"), or an appetite ("6 weeks from start"). Not a single-point date with no uncertainty.
3. **Completion gate.** A yes-or-no condition. "New signups reach first-value in under 10 minutes at p75" is a gate. "Onboarding is improved" is not.
4. **In-scope items.** Enumerated. Each references a PRD section and an architecture component.
5. **Out-of-scope items.** Enumerated, with reasons. Longer than the "deferred" list; this is the no-gos list, not the backlog.
6. **Rabbit holes.** Shape Up term: anticipated risks that could blow up the scope. Each rabbit hole names what could go wrong and the smallest version that avoids it. See [`references/scope-vs-time.md`](references/scope-vs-time.md) section 4.
7. **Dependencies.** Upstream milestones that must complete first (from the architecture DAG).
8. **Cutover cadence.** When this milestone ships to production (every milestone, every N milestones, continuous with a flag-rollout date). Feeds deploy-ready.

A milestone without a completion gate is not a milestone; it is a wishlist heading. A milestone without an out-of-scope list is a milestone that will grow until the cycle runs out. A milestone without a cutover cadence is a milestone that will confuse deploy-ready.

**Passes when:** every milestone has all 8 fields populated or explicitly flagged; no milestone has an empty out-of-scope list; no milestone has "improve X" as its completion gate.

### Step 6. Horizon-appropriate precision (Now-Next-Later)

Read [`references/roadmap-anatomy.md`](references/roadmap-anatomy.md) section 3. The canonical roadmap output organizes work by horizon, not by date-to-the-day:

- **Now.** Current cycle (current 6 weeks, current month, current PI). Specific, owned, dated or appetite-bounded, fully decomposed into slices. Items here are grounded commitments; each slice has an owner; done-definition is explicit.
- **Next.** Directly after the current cycle (next 6 weeks, next month, next PI). Directional. Items are themes or outcomes, not yet decomposed into slices. Confidence bands ("70%") are appropriate here; day-level dates are not.
- **Later.** Longer-term direction. Thematic. Names outcomes and intent, not features. Items here are hypotheses about where the product goes, not commitments.

Precision gradient is the rule: equal precision across all three horizons is the quarter-stuffing failure. If Later has day-level dates or fully-decomposed slices, rewrite; if Now has only thematic labels with no slices, rewrite. A Now item with a confidence band of 30% belongs in Next, not Now. A Later item with a sign-off date is overclaiming; it belongs in Next.

For cadences other than Now-Next-Later (Shape Up, quarterly, PI), the analog is: current cycle is specific; next cycle is shaped not bet; future is sketched not shaped. The precision gradient applies regardless of vocabulary.

**Passes when:** the Now column is specific and owned; the Next column is directional with confidence bands or themes; the Later column is thematic; no row in Now has precision lower than a named owner and a slice decomposition; no row in Later has precision higher than a theme and an outcome.

### Step 7. Launch milestone identification

Read [`references/launch-sequencing.md`](references/launch-sequencing.md). If the roadmap includes a launch (any external announcement that takes one-time amplification: GA, Product Hunt, Show HN, press day, beta open-to-public), declare it explicitly and name the mode.

For each launch milestone, produce:

1. **Launch mode.** Hard, soft, beta, GA, waitlist-to-GA, Product Hunt, TechCrunch-day, or other named mode. Determines the D-calendar shape.
2. **Target date.** With a confidence band. "2026-07-15, 60% by this date, 90% by 2026-08-15" is legitimate. A single date with 100% implied is a commitment and requires Tier 3 sign-off.
3. **Launch readiness gates.** At minimum: observability-live date (feeds observe-ready), rollback-tested date (feeds deploy-ready), runbooks-reviewed date (feeds launch-ready), support-team-briefed date. Each gate is a sub-milestone with its own target.
4. **Pre-launch dependencies.** Items in earlier milestones that must ship before the launch is even sequenced. Drawn from the architecture DAG and from external commitments.
5. **D-calendar.** D-30, D-14, D-7, D-1, D-0, D+7 milestones at minimum. launch-ready's D-7 runbook starts against the D-7 gate; if the gate is missing, launch-ready cannot start.
6. **Slip protocol.** The rule for "launch has slipped." Default is Shape Up's circuit-breaker: re-shape, do not extend. Named exceptions (regulatory, partner-committed launches) that must hold the date despite scope pressure are explicitly tagged.
7. **External commitments.** Press briefings, partner announcements, platform coordination (Product Hunt hunter confirmed, Hacker News submitter identified). Each is a hard dependency on the launch date.

A launch milestone without observability-live, rollback-tested, and runbooks-reviewed sub-items is not a launch milestone; it is a crisis waiting to be scheduled. See [`references/launch-sequencing.md`](references/launch-sequencing.md) sections 2-4 for the gate-composition rules.

**Passes when:** every launch milestone has all 7 fields populated; observability-live, rollback-tested, runbooks-reviewed dates are present; the D-calendar has at least D-7, D-0, D+7 markers.

### Step 8. Downstream handoff block

Read [`references/handoff-to-execution.md`](references/handoff-to-execution.md). Write `.roadmap-ready/HANDOFF.md` in the user's project directory. This artifact is the contract with the five downstream consumers.

The handoff block has five sub-sections, one per downstream consumer:

#### To `stack-ready` (live)

If stack-ready has not yet run, the roadmap's cadence choice, milestone horizon, and first-milestone scope shape the stack-ready constraint map. Supply:

```markdown
## Stack-ready inputs (from roadmap)
- Cadence: [Shape Up 6+2 / quarterly / PI / continuous / milestone / hybrid]
- First milestone horizon: [4-6 weeks / 3 months / 10-12 weeks]
- First milestone scope shape: [monolith v1 / service split / etc.]
- Time-to-first-ship target: [weeks / months]
- Any stack-level commitments baked into milestones: [managed Postgres by M2, etc.]
```

#### To `production-ready` (live)

The slice queue production-ready drains in its Step 5 slice ordering. Every slice has:

```markdown
## Production-ready slice queue
| Slice | Owner | Appetite or size | PRD ref | Architecture ref | Depends on | Milestone |
|---|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... | ... |
```

Slices are ordered (the queue is a sequence). production-ready's Step 5 reads the queue top-to-bottom and drains it, respecting the dependency column. A queue with cycles is rejected (A depends on B depends on A) and must be re-sequenced.

#### To `deploy-ready` (live)

The cutover cadence and per-milestone deploy posture:

```markdown
## Deploy-ready cutover cadence
- Cadence style: [per-milestone / every N milestones / continuous with feature flags / hybrid]
- Milestone 1 cutover: [date or condition]
- Milestone 2 cutover: [date or condition]
- ...
- Launch milestone cutover: [date, mode]
- Migration posture: [expand/contract multi-milestone calendar if any]
- Rollback policy: [same-artifact promotion / forward-only / versioned]
```

deploy-ready reads this to compute the pipeline cadence and the promotion gates.

#### To `observe-ready` (live)

The KPIs each milestone is expected to move, and the readiness gates for any launch:

```markdown
## Observe-ready inputs
- Milestone 1 KPIs: [activation, error rate, p95 latency, custom]
- Milestone 2 KPIs: [...]
- Launch readiness: observability-live by [date], SLOs finalized by [date], alert routes confirmed by [date]
- On-call coverage window: [hours / days surrounding launch]
```

#### To `launch-ready` (live)

The launch milestone summary (full details are in Step 7):

```markdown
## Launch-ready inputs
- Launch mode: [hard / soft / beta / GA / PH / etc.]
- Target date: [YYYY-MM-DD, confidence band]
- D-calendar: [D-30 / D-14 / D-7 / D-1 / D-0 / D+7 gate dates]
- Pre-launch dependencies: [milestones that must complete first]
- External commitments: [press, partners, platforms]
- Slip protocol: [hold / re-shape / exceptions]
- Public-roadmap derivative location: [file path]
```

**Passes when:** `.roadmap-ready/HANDOFF.md` exists and every sub-section is populated or explicitly "not applicable" with a reason. Empty sub-sections block Tier 3 sign-off.

### Step 9. Review cadence and freshness

Read [`references/review-cadence.md`](references/review-cadence.md). A roadmap without a review cadence becomes a shelf roadmap within one cycle.

Declare, in writing:

1. **Review cadence.** How often the roadmap is revisited. Shape Up: every betting table (every 8 weeks). Quarterly: monthly check-in, quarterly re-plan. SAFe: every PI planning event. Continuous: monthly.
2. **Who has authority to change what.** The Now column changes with standing authority (PM or team lead). The Next column changes at review cadence with broadcast. The Later column changes at cadence with explicit sign-off (it's a direction change, not an edit). Launch-milestone dates change only with escalation.
3. **What triggers an unplanned re-plan.** Scope discovery during a cycle (rabbit hole expanded), capacity loss (team member departure), external shift (regulatory change, partner slip), PRD change (pivot or material delta). See [`references/review-cadence.md`](references/review-cadence.md) section 4.
4. **What freezes a milestone.** Launch cut-line (Mode F), contractual lock-in, regulatory window. Frozen milestones reject new items; proposals are routed to the next-milestone backlog.
5. **Freshness indicator.** Every item carries a last-reviewed date. Items with a last-reviewed date older than one cadence cycle are flagged stale. This is the shelf-roadmap guard.
6. **Archive rule.** Completed milestones are archived, not overwritten. The roadmap file grows by one section per cycle.

**Passes when:** the review cadence is declared; authority map is written down; re-plan triggers and freeze conditions are named; freshness indicators are present on every Now and Next item.

### Step 10. Public-facing derivative (if applicable)

If the roadmap audience includes customers (public roadmap), produce a derivative. The canonical internal ROADMAP.md is never the public file. Read [`references/roadmap-anatomy.md`](references/roadmap-anatomy.md) section 6 for the redaction rules.

Redactions for public view:
- Strip capacity math, team assignments, engineer-weeks.
- Replace "Won't have" phrasing with "Not planned."
- Remove commercially-sensitive context (contract clauses, partner names under NDA).
- Remove internal owners; replace with "team" or nothing.
- Soften confidence bands (internal "70%" becomes external "targeting").
- Remove rabbit-hole details (the existence is visible; the specifics are not).

Additions for public view:
- Customer-value framing on each row ("Why this matters to you").
- Cross-links to changelog entries on shipped items.
- Clear "feedback welcome" channel if applicable.

A single file serving both audiences is the leak failure mode; a public file that does not exist is the opaque-vendor failure mode. Pick one derivative model explicitly.

**Passes when:** if audience is mixed, the public derivative exists at a separate path; the redaction checklist is applied; the internal canonical file is not visible externally.

### Step 11. Staleness check

Roadmap-building practices shift meaningfully. At the end of every run, print:

```
Skill version: roadmap-ready [current skill version]
Last updated: [frontmatter updated date]
Current date: [today]
```

If the skill version is older than 6 months relative to today, warn the user. Call out dimensions most likely to have shifted: cadence-tool landscape (Productboard AI, Aha! AI, Linear, Jira Rovo all ship features on quarterly cadences); downstream-skill interfaces (if deploy-ready or launch-ready changed their handoff contract, the HANDOFF.md may need re-templating); named-failure-mode vocabulary (new LLM-output tells emerge).

**Passes when:** the skill version and date are printed; a staleness warning is surfaced if the skill is >6 months old.

## Completion tiers

Four tiers. Each independently shippable, each declarable at a boundary, each audit-able.

### Tier 1: Sketch (mandatory, default for low-input sessions)

A one-page outline: cadence declared, team capacity stated, Now column populated with 2-5 slices, at least one milestone with a name and a completion gate, out-of-scope at least three bullets, upstream-artifact state noted.

| # | Requirement |
|---|---|
| 1 | **Mode declared.** A through F, with the research block from `roadmap-research.md`. |
| 2 | **Pre-flight answered.** 8 questions (Step 1) in writing or flagged as open. |
| 3 | **Cadence declared.** One cadence with rationale and two rejected alternatives. |
| 4 | **Upstream state noted.** PRD tier, ARCH tier, degradation ceiling applied. |
| 5 | **Now column populated.** 2-5 slices; each references a PRD section and an architecture component. |
| 6 | **One milestone named.** Name, completion gate, at least three in-scope items, at least three out-of-scope items. |
| 7 | **Capacity guard active.** No concurrent track count exceeds team size. |
| 8 | **No speculative items.** Every row has at least one upstream anchor. |

**Proof test:** a reader unfamiliar with the project can state, after 3 minutes, the cadence, the team size, the current focus, and the completion gate for the first milestone. If they cannot, Tier 1 is not complete.

### Tier 2: Plan (lean roadmap for alignment)

Tier 1 plus the Next and Later columns, full dependency graph reflected, at least two milestones, rabbit holes, review cadence declared.

| # | Requirement |
|---|---|
| 9 | **Next column populated.** Directional items; confidence bands or themes, not day-level dates. |
| 10 | **Later column populated.** Thematic outcomes; no slice decomposition, no dates. |
| 11 | **Topological order reflected.** Architecture DAG is respected across Now and Next. |
| 12 | **At least two milestones named.** Each with 8 anatomy fields from Step 5. |
| 13 | **Rabbit holes enumerated.** At least one per active milestone with a smallest-version alternative. |
| 14 | **Prioritization framework declared.** RICE / ICE / WSJF / MoSCoW / Kano / Opportunity / Appetite, chosen for this roadmap with rationale. |
| 15 | **Review cadence declared.** Frequency, authority map, re-plan triggers, freeze conditions. |
| 16 | **Downstream handoff drafted.** `.roadmap-ready/HANDOFF.md` has all 5 sub-sections filled (even "not applicable" counts, with a reason). |

**Proof test:** production-ready can read the slice queue and start Step 5; deploy-ready can read the cutover cadence and start pipeline design; each downstream consumer finds enough to start without asking follow-up questions.

### Tier 3: Committed (signed-off, launch-aware)

Tier 2 plus a named launch milestone (if the project has one), full readiness gates, stakeholder sign-off, change-control protocol active.

| # | Requirement |
|---|---|
| 17 | **Launch milestone named (if applicable).** Mode, target date with confidence band, full D-calendar, external commitments. |
| 18 | **Launch readiness gates dated.** Observability-live, rollback-tested, runbooks-reviewed, support-briefed. |
| 19 | **Capacity math signed off.** Engineer-weeks match planned slices with Amdahl allowance. |
| 20 | **Commitments explicitly labeled.** Items with fixed date and fixed scope carry the "high-integrity commitment" label and a named reason. |
| 21 | **Stakeholder sign-off.** PM, engineering lead, design lead (if design work in scope), exec sponsor (if launch milestone), legal (if regulated), support (if SLA impact). Every signer attests to a specific thing. |
| 22 | **Change-control active.** The roadmap is Living; the changelog is being maintained; broadcasts are happening. See [`references/review-cadence.md`](references/review-cadence.md) section 3. |

**Proof test:** an engineer new to the project six months from now can read the roadmap, understand what shipped, what is next, what was cut, what is committed vs. directional, and where the launch milestone lives. If anything requires a clarification meeting, Tier 3 is not complete.

### Tier 4: Public-ready (mixed-audience roadmap)

Tier 3 plus a public derivative, a declared retrospective schedule, and launch-ready has the pre-launch runbook start date.

| # | Requirement |
|---|---|
| 23 | **Public derivative produced.** Separate file; redaction checklist applied; no internal capacity math, no contractual names, no rabbit-hole specifics visible. |
| 24 | **Retrospective scheduled.** Date and attendee list for the post-cycle or post-launch review. |
| 25 | **launch-ready D-7 starts against a real gate.** The D-7 date in the roadmap matches the D-7 in launch-ready's runbook if launch-ready is installed. |
| 26 | **No have-not remains.** Every item on the disqualifier list below passes. |

**Proof test:** customers reading the public derivative cannot see internal capacity; engineering reading the internal file has every decision and rationale; launch-ready's runbook starts cleanly against the roadmap's D-7 gate.

## The "have-nots": things that disqualify the roadmap at any tier

If any of these appear, the roadmap fails its contract and must be fixed before declaring done:

- **Fictional precision.** A date in day-level resolution (YYYY-MM-DD) outside the Now column, or any date without either a confidence band or a "high-integrity commitment" label with a named reason.
- **Fictional parallelism.** More concurrent tracks in any period than the team-capacity pre-flight answer allows.
- **Quarter-stuffing.** Q1, Q2, Q3, Q4 (or equivalent horizon columns) filled to identical density of items, with identical precision. The precision gradient (Now greater than Next greater than Later) is absent.
- **Speculative items.** A row with no PRD section reference AND no architecture component reference AND no named external constraint. It was invented somewhere, and nowhere is not a source.
- **Feature-factory output.** A row with no outcome framing, no appetite, no commitment reason. Item has no reason to be on the roadmap.
- **Bare feature name in place of an item.** "SSO," "Dark mode," "AI integration" without an outcome, an appetite, or a commitment label. The three-label test is not optional.
- **Shelf roadmap.** The roadmap's last-reviewed date is older than one cadence cycle and no review is scheduled. Mode C refresh has not run when it should have.
- **Missing launch readiness gates.** A launch milestone without observability-live, rollback-tested, and runbooks-reviewed sub-items.
- **Missing out-of-scope.** A milestone with an empty or placeholder out-of-scope list ("things beyond this scope," "to be determined"). See [`references/roadmap-anatomy.md`](references/roadmap-anatomy.md) section 2.
- **Dependency cycle.** A -> B -> A in the slice queue. Topological order is impossible; re-sequence.
- **Dates without capacity.** Any dated commitment emitted when the team-capacity pre-flight answer was null or incomplete.
- **Launch milestone without D-7 runbook target.** launch-ready cannot start its D-7 runbook; the launch is unsequenced.
- **Polish-indefinitely.** A cycle or milestone extended past its appetite or deadline with no explicit decision and no scope cut; default-extension is the failure mode. See [`references/scope-vs-time.md`](references/scope-vs-time.md) section 3.
- **Linear (single-track) roadmap.** All items in one column when team size is greater than one; no parallelism acknowledged even where architecture DAG supports it. Flag.
- **Perpetual-now.** All items are in Now; Next and Later are empty. There is no forward view. Also flag the inverse: items only in Later with nothing in Now.
- **Public file is the internal file.** A single roadmap file published to customers that includes internal owners, capacity math, rabbit-hole specifics, or contractual detail. Immediate fix before any external share.
- **Roadmap without a cadence.** A document titled "Roadmap" with no declared cadence defaults to whatever the tool assumes, which is usually Gantt. Reject.
- **Roadmap without a review cadence.** Step 9 skipped. Shelf roadmap in one cycle.
- **Invisible parallelism.** Parallel tracks drawn with shared-service bottlenecks that are not acknowledged in the Amdahl check. See [`references/dependency-graph.md`](references/dependency-graph.md) section 5.
- **Banned grid-generation output.** An AI-produced quarterly grid with even fill, no upstream references, invented dates, and no cadence declaration. Reject wholesale; re-run from Step 0.

When you catch yourself about to ship any of these, fix it before proceeding. A roadmap that ships with any of these is worse than no roadmap; the team will act on it, and the first misaligned slice is the first wasted cycle.

## Reference files: load on demand

The body above is enough to start. Load each reference *before* the step that uses it, not after.

| Reference file | When to load | ~Tokens |
|---|---|---|
| `roadmap-research.md` | **Always.** Start of every session (Step 0). Mode detection protocol. | ~6K |
| `sequencing-principles.md` | **Always.** Step 1 pre-flight and Step 4 sequencing. Decision framework for topological-vs-risk-vs-appetite layering. | ~7K |
| `roadmap-anatomy.md` | **Tier 1.** Step 5, Step 6, Step 10. Full ROADMAP.md template with annotations; milestone anatomy; horizon structure; public-derivative rules. | ~9K |
| `cadence-models.md` | **Tier 1.** Step 2 cadence selection. Seven cadences, selection matrix, rationale templates. | ~7K |
| `dependency-graph.md` | **Tier 1.** Step 3 and Step 4. Reading architecture DAGs, topological sort, capacity matching, Amdahl check. | ~6K |
| `risk-driven-prioritization.md` | **Tier 2.** Step 4 sequencing. RICE, ICE, WSJF, MoSCoW, Kano, Opportunity Scoring, appetite-first; compatibility matrix. | ~8K |
| `scope-vs-time.md` | **Tier 2.** Step 5 and Step 9. Appetite xor estimate; MoSCoW at milestone; when to cut scope vs. move the date; rabbit-hole anatomy. | ~6K |
| `handoff-to-execution.md` | **Tier 2.** Step 8 downstream handoff. Slice queue for production-ready; cutover cadence for deploy-ready; KPIs for observe-ready; launch summary for launch-ready. | ~7K |
| `launch-sequencing.md` | **Tier 3 (if launch in scope).** Step 7 launch milestone. Launch modes, readiness gates, D-calendar, slip protocol, external commitments. | ~7K |
| `review-cadence.md` | **Tier 2 and Tier 3.** Step 9. Review frequency, authority map, re-plan triggers, freeze conditions, freshness indicators, archive rule. | ~6K |
| `roadmap-antipatterns.md` | **On demand.** Mode B audits and tier-gate checks against the have-nots. Named-failure-mode catalog with shapes, examples, fixes. | ~8K |
| `RESEARCH-2026-04.md` | **On demand.** When the user asks "why this rule" or "what is the evidence." Source citations for the initial release; 267 URLs, 10 sections. | ~36K |
| `EXAMPLE-ROADMAP.md` | **On demand.** A complete worked example roadmap for a fictional B2B SaaS pilot (Pulse, a Customer Success ops platform). Demonstrates a 14-week appetite with named capacity input (140 eng-days, 42 design-days, 14 AE-days), Now-Next-Later horizons, three milestones with binary completion gates, a topologically-sorted slice queue feeding production-ready, a cutover cadence feeding deploy-ready, a KPI handoff feeding observe-ready, and a risk register with named owners. Passes the skill's grep tests for fictional-precision / fictional-parallelism / quarter-stuffing / speculative-features / feature-factory / shelf-roadmap / roadmap-theater failure modes. Consumes the worked PRD and the worked architecture; feeds the worked stack-decision example in its sibling repo. | ~16K |

Skill version and change history live in `CHANGELOG.md`. When resuming a roadmap across sessions, confirm the skill version matches the version recorded in `.roadmap-ready/STATE.md`. A skill update between sessions can shift have-nots (AI-slop tells evolve), downstream-skill interfaces (if deploy-ready or launch-ready changed their handoff contract, HANDOFF.md may need re-templating), and cadence-tool landscape (Productboard AI, Aha! AI, Jira Rovo feature sets shift quarterly). If versions differ, re-run the Tier audit on any Tier 2+ artifact before continuing.

## Session state and handoff

Roadmaps span sessions; maintain `.roadmap-ready/STATE.md` when the work is ongoing.

**Template:**

```markdown
# Roadmap-Ready State

## Skill version
roadmap-ready [current skill version], [frontmatter updated date].

## Current tier
Working toward Tier [N]. Last completed tier: [N-1].

## Mode
A / B / C / D / E / F.

## Pre-flight answers
- Team capacity: [N engineers; M engineer-weeks per cycle]
- Cadence: [declared cadence]
- Horizon: [length]
- Hard external dates: [list, or "none"]
- Audience: [internal / mixed / public]
- Risk tolerance: [continuous / milestone / PI]
- Existing commitments: [list, or "none"]
- Upstream state: [PRD tier, ARCH tier]

## Milestones
- M1: [name, gate, target, status]
- M2: [name, gate, target, status]
- ...
- Launch: [mode, date, confidence, gates]

## Now / Next / Later
- Now (current cycle): [5 slices]
- Next: [4 themes]
- Later: [3 directions]

## Downstream handoff status
- Stack-ready inputs: [drafted / signed off / not applicable]
- Production-ready slice queue: [N slices / ordered]
- Deploy-ready cutover cadence: [declared]
- Observe-ready KPIs: [per milestone]
- Launch-ready inputs: [drafted / committed / not applicable]

## Sign-off ledger
- PM: [name, date, attestation]
- Eng lead: [name, date, attestation]
- ...

## Open questions blocking next tier
- [Q]: [owner], [due date]

## Last reviewed
[ISO date]. Next review due: [ISO date].

## Last session note
[ISO date] [what happened, what's next]
```

**Rules:**
- STATE.md is the contract with the next session. Update at every tier boundary and every context compaction.
- Never delete STATE.md. If an entry is wrong, correct it in place with a dated note.
- If `ROADMAP.md` and `HANDOFF.md` exist and Tier 3 is reached, STATE.md can be collapsed into the ROADMAP's changelog; ROADMAP becomes the source of truth.

## Suite membership

This skill is part of the **ready-suite**. See [`SUITE.md`](SUITE.md) for the full map.

- **Planning tier:** `prd-ready` (what), `architecture-ready` (how), `roadmap-ready` (when, this skill), `stack-ready` (with what tools).
- **Building tier:** `production-ready` (the app), `repo-ready` (the repo scaffolding).
- **Shipping tier:** `deploy-ready` (ship it), `observe-ready` (keep it healthy), `launch-ready` (tell the world), `harden-ready` (survive adversarial attention).

roadmap-ready sits in the planning tier alongside prd-ready, architecture-ready, and stack-ready. Upstream of roadmap-ready: prd-ready (WHAT) and architecture-ready (HOW). Downstream: stack-ready, production-ready, deploy-ready, observe-ready, launch-ready. The skill's output is the bridge between planning and execution: engineering reads the slice queue, deploy reads the cutover cadence, observe reads the KPIs, launch reads the milestone. The harness is the router; this skill tells the user which sibling to invoke next and why.

## Consumes from upstream

When the agent starts, it checks for upstream artifacts and pre-fills from them rather than asking the user to repeat decisions already made. Absence is fine; the skill degrades gracefully per the Step 3 degradation table.

| If present | roadmap-ready reads it during | To pre-fill |
|---|---|---|
| `.prd-ready/PRD.md` | Step 3 (upstream ingestion); Step 5 (milestone in-scope references); Step 6 (Now / Next / Later items) | Priority ordering from MoSCoW, release-gating criteria per feature, rabbit holes, appetite, existing commitments, target-user and success criteria that anchor outcome framing. |
| `.prd-ready/HANDOFF.md` | Step 3 | Pre-filled "Roadmap-ready inputs" sub-section: priority ordering, release-gating criteria, dependencies, must-haves vs. nice-to-haves, rabbit holes, dates or ranges. |
| `.architecture-ready/ARCH.md` | Step 3 (component DAG extraction); Step 4 (topological sequencing); Step 5 (milestone architecture references); Step 7 (launch-milestone architecture impact) | System shape (monolith vs. services), component breakdown, dependency graph edges, integration architecture, trust boundaries, non-functional targets that shape milestone scope. |
| `.architecture-ready/HANDOFF.md` | Step 3; Step 4 | Pre-filled "Roadmap-ready inputs" sub-section: component dependency graph, load-bearing-first ordering, risk-ordered architecture items, evolution plan (if Mode E). |
| `.stack-ready/DECISION.md` | Step 2 (cadence alignment); Step 5 (stack-level milestone content) | Any stack decisions whose implementation lands in a particular milestone (migration from one DB to another; framework upgrade). Stack decisions are not re-made here; they are sequenced. |

If `.prd-ready/` is absent entirely, the skill emits a Tier 1 Sketch at most, flags that the roadmap is effectively a feature wishlist until a PRD lands, and pauses dated commitments. If `.architecture-ready/` is absent, the skill emits at most Tier 2 Plan, flags that sequencing risks missing dependencies, and re-runs Step 4 against ARCH when it arrives. Upstream absence is handled gracefully; upstream falsehood is not (if `.prd-ready/PRD.md` contradicts the running code, trust the code and route back to prd-ready for reconciliation before building on top of a stale PRD).

## Produces for downstream

Five downstream siblings consume this skill's output. Writing these is part of the skill's definition of done.

| Artifact | Path | Consumed by |
|---|---|---|
| **Roadmap** | `.roadmap-ready/ROADMAP.md` | All downstream; canonical internal artifact. |
| **Downstream handoff block** | `.roadmap-ready/HANDOFF.md` | Each downstream skill reads its sub-section directly. |
| **Public derivative (if mixed audience)** | `.roadmap-ready/ROADMAP-PUBLIC.md` (or project-specific path) | Customers, partners, external stakeholders. |
| **Session state** | `.roadmap-ready/STATE.md` | Next roadmap-ready session resumes here. |
| **Retrospective log** | `.roadmap-ready/retrospectives/YYYY-MM-slug.md` | Post-cycle or post-launch retrospective; read by the Mode C refresh and the Mode E rescue. |

Specific downstream consumers and what they read:

- **`stack-ready`** reads the "Stack-ready inputs" sub-section of HANDOFF.md (cadence, first-milestone horizon, time-to-ship target) during its Step 1 pre-flight.
- **`production-ready`** reads the "Production-ready slice queue" in HANDOFF.md and the ordered slice list in ROADMAP.md's Now column during its Step 1 and Step 5 (slice ordering). Already wired: production-ready v2.5.6 upstream frontmatter lists roadmap-ready.
- **`deploy-ready`** reads the "Deploy-ready cutover cadence" sub-section during its Step 2 topology note and Step 4 pipeline design. At v1.0.5 deploy-ready consumes the cutover block when present.
- **`observe-ready`** reads the "Observe-ready inputs" sub-section during its SLO authorship and monitoring setup to align KPIs with milestone outcomes.
- **`launch-ready`** reads the "Launch-ready inputs" sub-section plus the launch-milestone block in ROADMAP.md during its Step 0 (mode detection) and Step 11 (D-7 runbook). The D-7 gate date is read directly.

## Handoff: architecture, stack, repo, production, deploy, observe, and launch are not this skill's jobs

roadmap-ready stops at "this is the sequence, these are the milestones, here are the handoffs." What comes next:

- To **`stack-ready`** (live): cadence, first-milestone horizon, and time-to-ship become inputs to stack-ready's constraint map. roadmap-ready does not pick a framework; stack-ready does.
- To **`production-ready`** (live): the slice queue becomes production-ready's work list. roadmap-ready does not write code; production-ready does.
- To **`repo-ready`** (live): if repo scaffolding is a milestone slice, repo-ready receives it. roadmap-ready does not author CI configs; repo-ready does.
- To **`deploy-ready`** (live): the cutover cadence becomes deploy-ready's pipeline-cadence input. roadmap-ready does not design expand/contract migrations; deploy-ready does.
- To **`observe-ready`** (live): KPI handoffs become observe-ready's SLO authorship inputs. roadmap-ready does not write SLOs; observe-ready does.
- To **`launch-ready`** (live): the launch milestone, mode, D-calendar, and pre-launch dependencies become launch-ready's Step 0 and Step 11 inputs. roadmap-ready does not write landing copy or launch-day runbooks; launch-ready does.

**If your harness exposes a skill-invocation tool** (e.g., Claude Code's Skill tool), invoke the next sibling directly when the handoff trigger fires ("OK, the roadmap is Tier 2-signed, which stack should we pick?"). **Otherwise**, surface the handoff to the user: "This step needs `stack-ready`. Install it or handle the sibling layer separately." Do not attempt to generate the sibling's output inline from this skill.

## The roadmap refuses to lie

Sequencing is roughly 25% of the work. The milestone anatomy is another 25%. The handoff block, the review cadence, the public derivative, and the staleness guard are the remaining 50%. A user who walks away with "we'll build these features over the next quarter" and no cadence, no capacity check, no upstream-anchor per item, no launch-readiness gates, and no review schedule does not have a roadmap; they have a feature wishlist that will be re-litigated at the first cycle boundary and re-invented at every downstream skill.

The AI-tooling landscape is full of generators. The gap is a refuser. When a date is asserted without a capacity input behind it, refuse. When a track is drawn beyond team size, refuse. When a feature is on the roadmap but not in the PRD, refuse. When a launch milestone has no readiness gates, refuse. The roadmap is worth more when it commits less and grounds more than when it fills every cell.

When in doubt, ask whether an engineer on the team could read the document tomorrow morning and begin the next slice without scheduling a meeting to ask which slice is next. The first question they would have to ask is the next thing to write down.
