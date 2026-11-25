---
name: prd-ready
description: "Write a PRD that engineering, design, QA, and downstream planning skills can consume without a clarification meeting. Owns problem framing, target-user specificity, success metrics, functional and non-functional requirements, scope and no-gos, appetite and rabbit holes, open-question log, downstream handoff block, and the iterate-vs-freeze lifecycle. Refuses hollow PRDs (sections filled, no decisions), invisible PRDs (reads the same across any product), feature laundry lists (un-prioritized feature dumps), solution-first PRDs (problem box names the solution), assumption-soup PRDs (we-assume-users-will-love-it claims), and moving-target PRDs (silent edits, engineer whiplash). Triggers on 'write a PRD,' 'product spec,' 'requirements doc,' 'one-pager,' 'product brief,' 'pitch for this feature,' 'problem statement.' Does not design the architecture (architecture-ready), sequence the roadmap (roadmap-ready), pick the stack (stack-ready), build the app (production-ready), or write launch copy (launch-ready). Top of the planning tier; no upstream siblings. Full trigger list in README."
version: 3.1.0
updated: 2026-11-23
changelog: CHANGELOG.md
suite: ready-suite
tier: planning
upstream: []
downstream:
  - architecture-ready
  - roadmap-ready
  - stack-ready
  - production-ready
pairs_with:
  - architecture-ready
  - roadmap-ready
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

# PRD Ready

This skill exists to solve one specific failure mode. A founder or PM opens a new Notion page, types "Write a PRD for X" into ChatGPT or Claude or ChatPRD or Gemini, and pastes the output back. What ships is a document that has an Executive Summary, a Problem Statement, five Personas, a Functional Requirements list, a Technical Requirements list, a Success Metrics table, a Risks table, and a Timeline. Every section is filled. The target user is "users who need productivity tools." The success metric is "increased engagement and retention." The problem statement reads "users currently struggle with inefficient workflows and need a better solution." The functional requirements are twelve bullets of the form "the system must allow users to..." and the non-functional requirements include "the system must be fast" and "the system must be secure." The out-of-scope section says "features beyond v1 scope." The risks table lists "adoption risk" with mitigation "strong go-to-market." The PRD is twelve pages long. The engineer reads it, asks the PM eight questions, and does not start building.

The job here is the opposite. Produce a PRD whose problem sentence names the specific friction a specific person hits on a specific workday and could not be pasted into a different product's PRD without sounding absurd. Whose target user is a named role in a named context with a named constraint, not "small business owners." Whose success metrics are measurable, time-bound, and outcome-framed (not feature-shipped-yes-or-no). Whose requirements are concrete enough that QA can write acceptance tests from them directly. Whose non-goals list is longer and more opinionated than the goals list, because out-of-scope is harder and more load-bearing than in-scope. Whose appetite is stated before the estimate is requested, so engineering can respond with a different scope rather than a different date. Whose open-question log is dated, owned, and visible at the top of the document. Whose handoff block pre-fills the next three planning-tier skills (architecture-ready, roadmap-ready, stack-ready) and the building-tier skill (production-ready) so the same decisions are not re-litigated three more times.

This is harder than it sounds because PRDs fail in a narrow but lethal band. The industry has converged on the failure modes (Marty Cagan, Ben Horowitz, Adam Fishman, Aakash Gupta, Reforge, Shape Up, Intercom, Amazon Working Backwards all describe the same ten patterns in slightly different vocabulary; see [references/RESEARCH-2026-04.md](references/RESEARCH-2026-04.md)). Tooling does not catch them. Google Docs, Notion, Confluence, and Coda will render any PRD you type; none of them will tell you the problem section names the solution, or that the four personas read like the same person, or that the MoSCoW ranks are all M. The skill is the layer above the tool that catches the document shape before it ships.

## Core principle: every sentence is a decision, a hypothesis, or a named open question

> **Every sentence in the PRD is one of three things: a decision with rationale, a flagged hypothesis with a validation plan, or a named open question with an owner and a due date. Nothing in between.**

This principle is non-negotiable. The whole taxonomy of PRD failure reduces to "sentences that pretend to be decisions but are not." The hollow PRD is sentences without decisions. The invisible PRD is sentences that could describe any product, which means they decide nothing specific. The feature laundry list is features listed without a priority call, which means the prioritization was never decided. The solution-first PRD is a solution presented as if it were a problem, which disguises an unchosen decision. The assumption-soup PRD states beliefs ("users will love this") as if they were facts, collapsing hypothesis into decision. The moving-target PRD is decisions edited silently, which means they were never decided, only written down.

The three-label test is auditable sentence by sentence. Read every sentence of the PRD. For each one, answer: is this a decision (we have chosen X, and here is the rationale), a hypothesis (we believe X, and here is how we will test it), or an open question (we do not yet know X, and [owner] will answer by [date]). If a sentence is none of the three, it is theater and must be rewritten or deleted. The skill enforces this test as a sentence-by-sentence discipline at every tier gate; see [references/prd-antipatterns.md](references/prd-antipatterns.md) section 1 for the exact procedure.

The substitution corollary. For any user-facing sentence in the problem, target-user, success-metric, and non-goals sections, substitute a competitor or adjacent product. If the sentence still reads plausibly, the sentence decides nothing specific and fails the test. "Users want a faster way to manage their inbox" substitutes into any email product ever shipped; "Fed-up Gmail users who archive more than 200 messages per week and have at least three filters they rewrite monthly" does not. Specificity is the discipline. See [references/problem-framing.md](references/problem-framing.md) section 2 for the substitution-test procedure applied to PRDs.

## When this skill does NOT apply

Route elsewhere if the request is:

- **Designing the architecture** ("draw the system diagram," "what components do we need," "how do the services talk to each other," "entity-relationship model"). That is `architecture-ready` (not yet released). prd-ready stops at "these are the entities and flows at a black-box level"; architecture-ready starts at "here is how those entities and flows decompose into services, modules, queues, and storage."
- **Sequencing a roadmap** ("build a quarterly plan," "milestone schedule," "what ships first," "when does the beta happen"). That is `roadmap-ready` (not yet released). prd-ready defines WHAT; roadmap-ready defines WHEN. prd-ready supplies priority signals (MoSCoW, release-gating criteria, dependencies); roadmap-ready consumes them to produce the calendar.
- **Picking the stack** ("what framework should I use," "Next.js vs. Remix," "pick an ORM," "should we use Supabase"). That is [`stack-ready`](https://github.com/hannsxpeter/ready-suite/tree/main/skills/stack-ready). prd-ready's output is a primary input to stack-ready via `.prd-ready/HANDOFF.md`; it is not a substitute. A PRD that recommends a stack has violated the scope fence.
- **Building the app** ("wire the dashboard," "implement the checkout flow," "add RBAC"). That is [`production-ready`](https://github.com/hannsxpeter/ready-suite/tree/main/skills/production-ready). prd-ready writes the requirement ("users must be able to cancel their subscription in a single click and receive a confirmation email within 5 minutes"); production-ready builds it and proves it works end-to-end.
- **Setting up the repo** ("CI config," "CONTRIBUTING.md," "CODEOWNERS"). That is [`repo-ready`](https://github.com/hannsxpeter/ready-suite/tree/main/skills/repo-ready). prd-ready never touches the repo scaffold.
- **Deploying the app** ("pipeline," "canary," "rollback plan"). That is [`deploy-ready`](https://github.com/hannsxpeter/ready-suite/tree/main/skills/deploy-ready). prd-ready may specify deployability requirements ("must deploy without downtime to existing users") but does not design the deployment.
- **Monitoring the app** ("SLO," "alerts," "runbook"). That is [`observe-ready`](https://github.com/hannsxpeter/ready-suite/tree/main/skills/observe-ready). prd-ready may specify observability requirements ("billing failures must be visible to support within 60 seconds") but does not design the dashboards.
- **Writing the launch** ("landing page copy," "Product Hunt post," "OG card"). That is [`launch-ready`](https://github.com/hannsxpeter/ready-suite/tree/main/skills/launch-ready). prd-ready's language is internal; launch-ready translates for external.
- **Pricing strategy.** ("Should we charge $29 or $49," "freemium vs. paid," "per-seat vs. per-usage"). prd-ready may reference pricing tiers in functional requirements ("free tier is capped at 100 actions/month") but does not decide what to charge. That is a business decision with its own research practice.
- **Competitive analysis as a discipline.** prd-ready references competitors when framing the problem ("today, users solve this with a Notion page and a Slack channel") and when running the substitution test. It does not run a full competitive review (feature matrix, pricing comparison, market share). That is a separate product-research practice.
- **Go-to-market planning.** (launch venues, press outreach, positioning). That is `launch-ready`'s territory. prd-ready's positioning is internal ("who this is for and what it replaces"); launch-ready's positioning is external ("the hero sentence on the landing page").
- **Marketing positioning and copy.** prd-ready produces a problem-first, internal-audience document. Any "marketing copy" output is a scope violation; route to launch-ready.
- **Technical spike or proof-of-concept code.** That is production-ready in research mode, or a separate discovery skill. prd-ready does not write code.
- **Acceptance tests and test plans.** prd-ready writes acceptance *criteria* (what must be true for a feature to count as done); production-ready's Tier 1 and Tier 4 proof tests and the QA org turn those into executable test plans. prd-ready states the outcome; production-ready proves the system meets it.
- **User research methodology.** Interview scripts, survey instruments, usability-test protocols, recruiting plans. prd-ready *consumes* the output of user research (citations, quotes, evidence) and does not run the research. If research has not been done, prd-ready flags the evidence gap as an open question; it does not invent evidence.
- **Design mockups and wireframes.** prd-ready names the visual-identity direction in prose ("modern clinical," "fintech-serious," "playful SaaS") for production-ready Step 3 to pick up. It does not generate pixel-level mockups or wireframes. AI-generated wireframes have an obvious AI-generated sheen and collapse credibility; refuse.

This section is the scope fence. Every plausible trigger overlap with a sibling gets a route-elsewhere line.

## Workflow

Follow this sequence. Skipping steps produces the exact class of failure this skill exists to prevent: a PRD that passes visual review, fills every section, and decides nothing.

### Step 0. Detect PRD state and mode

Read [references/prd-research.md](references/prd-research.md) and run the mode detection protocol.

- **Mode A (Greenfield product).** Net-new product, no prior PRD. Start from problem framing. Often paired with a PR-FAQ or Working Backwards pass (see [references/prd-anatomy.md](references/prd-anatomy.md) section 6).
- **Mode B (Greenfield feature).** Existing product, new feature. PRD exists for the product; this PRD adds one feature. Inherits the product's target user and success framing; does not re-litigate them.
- **Mode C (AI-slop PRD exists).** A PRD has already been generated by Claude / ChatPRD / Gemini / Notion AI and it fails the three-label test. The ask is "fix this before sign-off." Run the audit first (Step 1.5); rewrite sections that fail.
- **Mode D (Iteration / refresh).** Existing PRD is stale. Team shipped v1; scope has shifted; requirements drifted. Update the existing PRD with a dated changelog entry rather than writing a new one.
- **Mode E (Pivot).** New target user, new problem, materially different success metric, or >50% timeline delta. Fork a new PRD; cross-link to the prior one. Do not overwrite. Research (RESEARCH-2026-04.md section 7.2) confirms this is the threshold where teams write a new document.
- **Mode F (Rescue).** The PRD was approved, engineering started building, and the build stalled because the PRD is underspecified. Diagnose which sections engineering cannot build from (problem ambiguity, non-estimable requirements, missing non-functionals, scope creep mid-build) and remediate the dominant cause.

**Passes when:** a mode is declared in writing, and the corresponding research block from `prd-research.md` is produced. For Mode C, at least one failed sentence is quoted. For Mode F, the dominant underspecification cause is named.

### Step 1. Pre-flight

Read [references/problem-framing.md](references/problem-framing.md). Answer the 7 pre-flight questions in writing:

1. **What is the problem.** One paragraph, naming the specific friction a specific person hits on a specific workday. The paragraph survives the substitution test against two competitors.
2. **Who has it.** A named role, a named context, a named constraint. Not "small business owners," not "enterprise users," not "modern teams."
3. **How they solve it today.** The existing workaround. Usually not another product; usually a Notion page, a Slack channel, a spreadsheet, a cron job, a habit (April Dunford, competitive-alternative framing).
4. **Why now.** The forcing function. What changed in the world, the technology, the regulation, the user's job that makes this the right moment.
5. **What it costs them.** The current friction translated into time, money, morale, or risk. Concrete numbers beat adjectives.
6. **What success looks like in 90 days.** The outcome, not the ship. "100 teams have replaced their Notion page with this tool and have not opened the Notion page in 30 days" beats "v1 is launched."
7. **Appetite.** How much time are we willing to spend before we stop. Stated as a duration (4 weeks, 8 weeks, 1 quarter), not as an estimate. Shape Up's rule: appetite before estimate. If the work cannot fit the appetite, scope is cut, not time extended.

If any answer is "I don't know yet," flag it as an open question with an owner and a due date; do not fabricate. If the user's input is one sentence ("write a PRD for a habit tracker"), do not invent seven answers. Ask the user the minimum set that the default assumptions cannot cover, state explicit assumptions for the rest, and proceed.

**Passes when:** all 7 pre-flight questions are answered in writing, explicit assumption statements replace any missing answers, and the problem paragraph has been run through the substitution test against two named competitors or alternatives.

### Step 1.5. Mode C audit (only if a prior AI-slop PRD exists)

Skip if not Mode C. Otherwise, read [references/prd-antipatterns.md](references/prd-antipatterns.md) and run the audit:

- Quote every sentence from the Problem section. For each, apply the three-label test. Sentences that are not a decision, a flagged hypothesis, or a named open question are marked for rewrite.
- Quote the target-user paragraph. Apply the substitution test against two competitors. Rewrite if it passes (meaning the sentence describes the category, not the user).
- Quote every success metric. A success metric that does not name a number, a deadline, and a measurement source is not a success metric; mark for rewrite.
- List every requirement. A requirement without a MoSCoW rank is a laundry-list entry; either rank it or cut it.
- Scan the Out-of-Scope section. If it is shorter than three bullets or contains "features beyond v1 scope," it is a missing section.

Output the audit as a list of specific defects with the failing quote and the required remediation. Do not rewrite yet; decide first what fails, then proceed to the regular workflow.

**Passes when:** every failing section has a specific defect quote, the dominant failure mode is named (invisible / laundry list / solution-first / assumption-soup / moving-target / hollow), and the Mode C remediation plan is listed in writing.

### Step 2. Problem framing (the problem-first discipline)

Read [references/problem-framing.md](references/problem-framing.md). The Problem section does three things and only three:

1. **Names the friction.** In the target user's vocabulary, not the product's.
2. **Names who has it.** Not a persona archetype; a concrete role with a concrete constraint.
3. **Names the existing workaround.** The competitive alternative, per April Dunford's framing. The replacement frame (a Notion page, a cron job) beats the feature frame (a competitor product).

The Problem section does not:

- Name the solution. Intercom's rule: "Do not add the solution here." If the Problem section says "users need a tool that automatically..." it has already named the solution. Rewrite in the form "users today do X manually, which takes Y time and costs Z."
- List features. Features live in the Requirements section.
- Describe the product's benefits. Benefits are downstream of the problem; they live in the Success section.

**Passes when:** the Problem section contains three paragraphs (friction, who, workaround) and zero sentences that begin with "Our product," "The system," "The tool," "Users need a solution that," or any other phrasing that names the product's solution before the problem is fully framed.

### Step 3. Target user (specificity is the discipline)

Read [references/user-personas.md](references/user-personas.md). The Target User section names one primary user and optionally one or two secondary users. Each named user has:

1. **A role.** "Engineering manager at a Series B startup with 8-15 engineers." Not "tech leader."
2. **A context.** What they are doing when they hit the problem. Not their life story; the specific workday moment.
3. **A constraint.** Budget, time, tooling, org politics, compliance. The thing that shapes the solution space.
4. **A current workaround.** The specific alternative they use today. Consistent with the Problem section.
5. **A named quote or citation.** If user research has happened, a real quote. If not, a citation to the research gap as an open question; do not fabricate quotes.

The section is not a persona paragraph. Persona paragraphs have three problems:

- They are abstract ("Sarah is a 35-year-old marketing manager who values efficiency") and survive the substitution test against every product in the category.
- They are fictional, which makes engineers skeptical and leadership quote the fiction back as if it were evidence.
- They accrete fake demographics that do not drive decisions ("Sarah drinks coffee and listens to podcasts").

The section is instead a **tight, concrete, cited** description of who this is for. Five bullets, not five paragraphs.

**Passes when:** the primary user is named with a specific role, context, and constraint; the target-user paragraph survives the substitution test against two competitor products; and every claim about the user either cites real research or is flagged as a hypothesis with a validation plan.

### Step 4. Success criteria

Read [references/success-criteria.md](references/success-criteria.md). Every success metric has four required properties:

1. **Measurable.** A number, not an adjective. "80%" or "under 3 seconds" or "400 weekly active teams," not "high" or "fast" or "widely adopted."
2. **Time-bound.** A deadline or a measurement window. "At 90 days post-launch," not "eventually."
3. **Outcome-framed.** A user or business outcome, not a feature-shipped indicator. "Median time-to-first-value is under 10 minutes" is an outcome. "The onboarding flow is live" is a feature-shipped indicator; it does not belong in success metrics.
4. **Source-attributed.** Where the number comes from. "Measured in Amplitude via the `first_value_moment` event" beats "tracked in analytics."

Separate leading from lagging indicators:

- **Leading indicators** show movement before the outcome lands. "% of new teams completing onboarding in the first session," "median time from signup to first action," "activation rate at day 7."
- **Lagging indicators** confirm the outcome. "Weekly active teams at 90 days," "paid conversion at day 30," "net revenue retention at month 6."

A PRD that cites only lagging indicators has no way to steer during build. A PRD that cites only leading indicators has no anchor. Every tier above Tier 1 requires at least one of each.

Anti-patterns to refuse:

- **Vanity metrics.** Total signups, total pageviews, total downloads without engagement qualifier. These are not success metrics.
- **Feature-shipped checkboxes dressed as metrics.** "The payment flow is integrated" is not a metric.
- **Engagement without activation.** "Weekly active users" without a definition of "active" is meaningless.

**Passes when:** at least one leading and one lagging success metric, each with a number, a deadline, an outcome frame, and a source. Vanity metrics and feature-shipped-checkbox metrics are rejected.

### Step 5. Functional requirements

Read [references/requirements.md](references/requirements.md). Functional requirements describe what the system must do from the user's point of view. Each requirement has:

1. **A user-observable behavior.** "The user can upload a CSV of up to 10,000 rows and receive a preview in under 5 seconds." Not "the system supports CSV import."
2. **A MoSCoW rank.** Must, Should, Could, Won't (this release). Ranks are scarce: a list where every item is a Must is not ranked; force distribution.
3. **Acceptance criteria.** What QA or production-ready's Tier 1 proof test checks. "Given 10,000 rows, when the user uploads, then a preview of the first 100 rows renders within 5 seconds on a 4G connection."
4. **A dependency list.** Other requirements this one depends on, if any. Consumed by roadmap-ready for sequencing.

Requirements are not:

- Features in the product-marketing sense ("AI-powered insights").
- Screens or wireframes ("the dashboard has three tabs").
- Implementation details ("uses a Kafka queue").
- Nested lists of sub-requirements four levels deep.

Granularity rule: a requirement is user-observable and testable. If a line is not both, it is too small (a task) or too big (an epic). Split or merge until it is.

MoSCoW discipline:

- **Must.** Fails the release if missing. Usually 30-50% of the list.
- **Should.** Important but the release can go without it. Usually 20-30%.
- **Could.** Nice to have; shipped if time-box allows (Shape Up appetite logic). Usually 20-30%.
- **Won't (this release).** Explicitly not shipping in this cycle. Cross-linked to the Out-of-Scope section.

A PRD where everything is Must has not been prioritized. A PRD where everything is Should has not been decided.

**Passes when:** every functional requirement has a user-observable behavior, a MoSCoW rank, acceptance criteria, and a dependency list; no more than 50% of requirements are Musts; and no requirement is an implementation detail or a feature-marketing phrase.

### Step 6. Non-functional requirements

Read [references/requirements.md](references/requirements.md) section 4. Non-functional requirements (NFRs) describe how the system must behave, not what it must do. Each NFR names a dimension and a threshold:

| Dimension | Example threshold |
|---|---|
| Performance | "p95 response time under 300ms for primary user actions on a 4G connection" |
| Scale | "Supports 10,000 concurrent users and 1M events/day at v1" |
| Availability | "99.9% uptime monthly; at most 43 minutes of downtime per month" |
| Security | "All data in transit encrypted (TLS 1.3+); data at rest encrypted with customer-managed keys for Enterprise tier" |
| Privacy | "No PII in logs; Sentry PII scrubbing enabled; GDPR subject access requests fulfilled within 30 days" |
| Compliance | "SOC 2 Type II controls apply to production; HIPAA BAA required for Healthcare tier" |
| Accessibility | "WCAG 2.2 AA compliance verified by automated axe-core scan plus manual screen-reader pass" |
| Internationalization | "English only at v1; string externalization scaffold in place; no hardcoded strings in UI components" |
| Observability | "Every user-facing error is logged with user ID, trace ID, and a support-reproducible payload" |
| Data retention | "Active user data: indefinite. Inactive accounts: 24 months. Audit logs: 7 years for Finance tier." |

Non-functional requirements are the most commonly skipped section in AI-generated PRDs. The downstream cost is enormous: architecture-ready cannot size the system without scale and latency targets; stack-ready cannot rule out candidates without compliance constraints; production-ready cannot pass Tier 3 without security and a11y targets; observe-ready cannot write SLOs without availability targets.

If the team does not yet know a threshold, flag it as an open question with an owner and a due date. Do not fabricate numbers. A flagged "unknown" is a valid PRD entry; an invented "99.99%" is a decision masquerading as a fact.

**Passes when:** every applicable NFR dimension has either a stated threshold or a flagged open question with an owner; compliance and security dimensions are never silent (at minimum, a statement of what regulations do and do not apply); and no threshold is an invented number presented as a requirement.

### Step 7. Scope and no-gos

Read [references/scope-and-out-of-scope.md](references/scope-and-out-of-scope.md). The Out-of-Scope section is the single hardest and most load-bearing section of a PRD. Every modern guide (Shape Up "no-gos," Kevin Yien Square template, Reforge, Intercom) foregrounds it; every AI-generated PRD minimizes it.

The section has three parts:

1. **Explicit no-gos.** Things the team has considered and decided not to build. Each entry names what was considered and why it was cut. Example: "Slack integration: cut for v1 because 78% of survey respondents use Teams, not Slack. Reconsidered at v1.5 if Teams integration lands and users ask for parity."
2. **Deferrals.** Things that are in the product plan but not this release. Cross-linked to the Won't (this release) MoSCoW tier. Example: "Multi-tenant admin panel: deferred to v2; single-tenant admin ships in v1."
3. **Explicit non-ownership.** Things this PRD's team is not responsible for, to prevent downstream confusion. Example: "Email deliverability: owned by platform team; this PRD assumes Postmark is already configured for the domain."

The section length rule: the Out-of-Scope section is expected to be **longer than the Won't (this release) MoSCoW tier** because it catches things nobody thought to rank. A three-line Out-of-Scope section is a red flag.

Scope-creep prevention depends on this section being read before every scope change. The change-control protocol (Step 11) requires that any proposed scope addition be first checked against this section: if it is an explicit no-go, the change is escalated; if it is a deferral, the team confirms whether the deferral still holds; if it is non-ownership, the change is rerouted.

**Rabbit holes** (Shape Up term). A separate subsection: anticipated risks that could blow up the scope if not addressed. Each rabbit hole names:
- What could go wrong.
- Why it is tempting to over-build.
- The smallest version that avoids the rabbit hole.

Example: "Real-time collaboration: rabbit hole. Tempting to build full CRDT-based sync; v1 uses optimistic locking with last-writer-wins and a 'refresh to see latest' banner. Full real-time is a v2 scoping question."

**Passes when:** the Out-of-Scope section has at least three explicit no-go entries with a reason each, at least one deferral entry, at least one non-ownership entry, and at least one rabbit hole named with its smallest-version alternative. A three-bullet Out-of-Scope passes only for the tiniest Tier 1 briefs; Tier 2+ requires meaningful length.

### Step 8. Risks, assumptions, and open questions

Read [references/risks-and-assumptions.md](references/risks-and-assumptions.md). Three separate lists; do not merge.

**Risks.** Named risks with:
- A specific failure mode (not "adoption risk"; "if the top 3 beta teams do not convert to paid in 60 days, the revenue model is unvalidated").
- An owner (the person accountable for watching the risk).
- A mitigation (concrete action, not "strong go-to-market").
- A trigger (what we will see if the risk materializes).

**Assumptions.** Claims we are proceeding as if true but have not proven. Each assumption has:
- The claim.
- The evidence supporting it (or "no evidence yet; hypothesis").
- The validation plan (how we will prove or disprove it, and when).

An assumption of the form "we assume users will love it" is the canonical assumption-soup failure. Rewrite as "we assume that ~70% of beta teams will reach first-value in their first session; validation plan is to measure the activation rate via Amplitude and check at day 14 post-launch."

**Open questions.** Things we do not know, distinct from risks (which we know but accept) and assumptions (which we believe but have not proven). Each open question has:
- The question.
- An owner (accountable for the answer).
- A due date.
- A blocking flag (does this block Tier 2 sign-off? Tier 3? Ship?).

The Open Questions log is visible at the top of the PRD (not buried at the bottom) and is the first thing an engineer or designer reads when deciding whether the PRD is build-ready.

**Passes when:** every risk has a failure mode, owner, mitigation, and trigger; every assumption has a claim, evidence, and validation plan; every open question has an owner, a due date, and a blocking flag; and no item is a lazy catch-all ("adoption risk," "we assume product-market fit").

### Step 9. Downstream handoff block

Read [references/prd-anatomy.md](references/prd-anatomy.md) section 8. Write `.prd-ready/HANDOFF.md` in the user's project directory. This artifact is the contract with the next three planning-tier skills and the building-tier app skill.

The handoff block has four sub-sections, one per downstream consumer:

#### To stack-ready (live, v1.1.5)

Populates all six of stack-ready's pre-flight questions so stack-ready skips interrogation:

```markdown
## Stack-ready pre-flight inputs
- Domain: [one of stack-ready's 12 domain profiles, or closest match + overrides]
- Team: [size, language depth, on-call coverage]
- Budget posture: [free-tier scrappy / cash-efficient growth / enterprise]
- Time-to-ship: [days / weeks / months / no deadline]
- Scale ceiling (12 months): [honest users and data estimate]
- Regulatory constraints: [HIPAA / PCI / SOC 2 / GDPR / FedRAMP / none]
```

#### To architecture-ready (not yet released)

```markdown
## Architecture-ready inputs
- Entities: [the nouns, with key attributes]
- Flows: [the verbs, happy path + at least 2 error paths per primary feature]
- Non-functional requirements: [copied from Step 6]
- Integration points: [named third-parties and internal services]
- Trust boundaries: [who sees what, who mutates what]
- Scale ceiling: [same as stack-ready]
- Compliance constraints: [same as stack-ready]
- Explicitly deferred to architecture: [what the PRD intentionally does not decide]
```

#### To roadmap-ready (not yet released)

```markdown
## Roadmap-ready inputs
- Priority ordering: [MoSCoW ranks, aggregated]
- Release-gating criteria: [per feature, what must be true to ship]
- Dependencies: [feature X blocks feature Y]
- Must-haves vs. nice-to-haves: [the cut line]
- Rabbit holes: [from Step 7]
- Dates or ranges: [contractual deadlines, marketing windows, regulatory dates]
```

#### To production-ready (live, v2.5.6)

```markdown
## Production-ready inputs
- Entities and CRUD surface: [what can be created / read / updated / deleted]
- Roles and permissions: [who can do what]
- Audit trail requirements: [what gets logged, retention, visibility]
- Acceptance criteria per feature: [from Step 5]
- Error and edge states: [named, not implied]
- Visual identity direction: [modern clinical / fintech-serious / playful SaaS / etc.]
- Domain landmines: [regulated-domain callouts]
```

**Passes when:** `.prd-ready/HANDOFF.md` exists and every sub-section is either filled or has explicit "deferred to downstream" with a reason. Empty sub-sections block Tier 2 sign-off.

### Step 10. Alignment and sign-off protocol

Read [references/stakeholder-alignment.md](references/stakeholder-alignment.md). The PRD is not done when the PM declares it done; it is done when the named stakeholders have signed off in writing.

Sign-off roster by tier:

| Tier | Required signers |
|---|---|
| Tier 1 (Brief) | Product manager, one engineering lead, one design lead |
| Tier 2 (Spec) | Tier 1 signers + QA lead or equivalent |
| Tier 3 (Full PRD) | Tier 2 signers + data/analytics, legal/compliance (if regulated), customer support |
| Tier 4 (Launch-Ready PRD) | Tier 3 signers + marketing/product marketing + executive sponsor |

Each signer attests to a specific thing, not a blanket "approved":

- **PM** attests to: problem framing, target user, success metrics, scope and no-gos, appetite.
- **Engineering lead** attests to: functional requirements are estimable, non-functional requirements are achievable, acceptance criteria are testable, rabbit holes are identified.
- **Design lead** attests to: user flows are coherent, target user is recognizable, non-goals do not strand the user.
- **QA lead** attests to: acceptance criteria are testable, edge states are named.
- **Data/analytics** attests to: success metrics are measurable with named instrumentation.
- **Legal/compliance** attests to: compliance constraints are named and accurate for the domain.
- **Customer support** attests to: failure modes and edge states are documented well enough to triage.
- **Marketing** attests to: launch criteria and rollout plan are coordinated.
- **Executive sponsor** attests to: strategic alignment and investment authorization.

The sign-off section records each signer's name, date, and the specific attestation. No anonymous "approved" entries.

**Passes when:** every required signer for the current tier has attested in writing, with name, date, and specific attestation. Missing signatures block the tier.

### Step 11. Iterate-vs-freeze lifecycle

Read [references/iterate-vs-freeze.md](references/iterate-vs-freeze.md). The PRD is a living document with change-control discipline. Four states:

1. **Draft.** Pre-Tier 1 sign-off. Anyone can edit; changes do not require changelog entries.
2. **Living.** Tier 1 or Tier 2 signed; Tier 2+ in flight. Edits allowed; every edit requires a changelog entry (date, author, section, one-line summary of the change). Horowitz's rule: "update the PRD and tell people."
3. **Soft-frozen.** Tier 3 signed; build in progress. Changes require PM approval and broadcast; they are additions or clarifications, not reversals. Reversals require escalation to the executive sponsor and a new Tier 3 sign-off.
4. **Archived.** Post-launch; PRD is no longer actively edited. A post-launch retrospective is added as a final section; the PRD is linked to the next PRD (if any) and moved to a historical location.

Change classification (the "in-scope change vs. new PRD" question):

- **In-scope change.** Clarification, acceptance-criteria tweak, wording change. Stays in current PRD, logged.
- **Scope adjustment.** Adding a sub-requirement to an existing feature, tightening an NFR threshold, narrowing a no-go. Stays in current PRD, PM sign-off, broadcast.
- **New PRD required.** New feature, new target user, new success metric, or >50% appetite delta. Fork; cross-link the prior.

Broadcast discipline:
- Every change in Living or Soft-frozen state is announced in the team's async channel (Slack, Linear, Discord) with a link to the changelog entry.
- Engineering cannot discover changes by re-reading the PRD; the broadcast is mandatory.
- Silent edits are the moving-target-PRD failure mode and are the primary reason engineering stops trusting PRDs.

**Passes when:** the PRD has a current state declared, a changelog section with every edit dated and attributed, a change classification for every proposed edit since Tier 1 sign-off, and a broadcast record showing changes were announced.

### Step 12. Staleness check

PRD practices shift slowly but measurably. At the end of every run, print:

```
Skill version: prd-ready [current skill version]
Last updated: [frontmatter updated date]
Current date: [today]
```

If the skill version is older than 6 months relative to today, warn the user. Call out dimensions most likely to have shifted: AI-slop vocabulary (the banned-phrase list drifts as model outputs shift), downstream-skill interfaces (if a sibling skill changed its handoff contract, the PRD's handoff block may need re-templating), and compliance baselines (regulations tighten, new jurisdictions matter).

**Passes when:** the skill version and date are printed, and a staleness warning is surfaced if the skill is >6 months old.

## Completion tiers

Four tiers. Each independently shippable, each declarable at a boundary, each audit-able.

### Tier 1: Brief (mandatory, always the default)

A one-page Product Brief. Problem + who + appetite + top-line success criteria + no-gos + open questions. Fits on a single page or single Google Doc screen; readable in 2-3 minutes.

| # | Requirement |
|---|---|
| 1 | **Mode declared.** A through F, with the research block from `prd-research.md`. |
| 2 | **Pre-flight answered.** All 7 questions from Step 1 in writing, or explicit assumptions for any gaps. |
| 3 | **Problem framed.** Step 2 three-paragraph Problem section passes substitution test and problem-first discipline. |
| 4 | **Target user specified.** Step 3 named role, context, constraint. |
| 5 | **Success criteria drafted.** At least one leading and one lagging metric, each with number, deadline, outcome frame, source. |
| 6 | **Appetite stated.** A duration, not an estimate. |
| 7 | **No-gos listed.** At least three explicit no-gos with reasons. |
| 8 | **Open questions logged.** Every unknown has an owner and a due date. |

**Proof test:** a reader unfamiliar with the project can state, after 3 minutes of reading, the problem, the target user, the top-line success metric, and the appetite. If they cannot, Tier 1 is not complete.

### Tier 2: Spec (lean PRD for solution-space alignment)

Tier 1 plus the requirement set, rabbit holes, a downstream handoff block, and engineering/design alignment.

| # | Requirement |
|---|---|
| 9 | **Functional requirements written.** Step 5: every requirement has behavior, MoSCoW rank, acceptance criteria, dependencies. |
| 10 | **MoSCoW distribution valid.** No more than 50% Musts; Should / Could tiers populated. |
| 11 | **Non-functional requirements written.** Step 6: every applicable dimension has a threshold or a flagged open question. |
| 12 | **Out-of-Scope section meaningful.** More than three bullets; includes deferrals and non-ownership. |
| 13 | **Rabbit holes named.** At least one, with a smallest-version alternative. |
| 14 | **Risks listed.** Each with failure mode, owner, mitigation, trigger. |
| 15 | **Assumptions listed.** Each with evidence or flagged as hypothesis with validation plan. |
| 16 | **Handoff block written.** `.prd-ready/HANDOFF.md` has all four sub-sections filled or explicitly deferred. |
| 17 | **Tier 1 signers have attested.** PM, engineering lead, design lead. |

**Proof test:** an engineer can read the PRD and start writing tickets without scheduling a clarification meeting. QA can begin drafting test plans from the acceptance criteria. Design can begin flow work without guessing the target user.

### Tier 3: Full PRD (build-ready, signed off)

Tier 2 plus full stakeholder sign-off, full NFR coverage, and a change-control protocol in effect.

| # | Requirement |
|---|---|
| 18 | **Every NFR dimension addressed.** Step 6: no silent dimension. |
| 19 | **Compliance and security are explicit.** Regulated-domain callouts are present or "not applicable" is stated with reason. |
| 20 | **Visual identity direction named.** One phrase, consumable by production-ready Step 3. |
| 21 | **All Tier 2 open questions resolved or explicitly deferred.** A deferred open question has a named next-review date. |
| 22 | **Tier 2 signers plus QA lead have attested.** For regulated domains, legal/compliance also signed. |
| 23 | **Change-control protocol in effect.** The PRD is Living or Soft-frozen; the changelog is being maintained; broadcasts are happening. |
| 24 | **Prior-art section.** Three comparable products or internal projects referenced with status, borrowed from stack-ready's pattern. "We looked at three real deployments" is the strongest defense against horoscope-shaped decisions. |

**Proof test:** a new engineer reads the PRD six months later and understands what was built, why, for whom, what was cut, and which decisions are still outstanding. They can tell whether the scope has shifted and by how much.

### Tier 4: Launch-Ready PRD

Tier 3 plus launch coordination, measurement instrumentation verified, support runbook drafted, and a post-launch retrospective scheduled.

| # | Requirement |
|---|---|
| 25 | **Launch plan cross-linked.** Pointer to `.launch-ready/` artifacts if launch-ready has been invoked, or a concise internal launch plan for low-visibility releases. |
| 26 | **Measurement instrumentation verified.** Every success metric from Step 4 has a live event, dashboard, or query ready to read. No metric is "we'll set this up later." |
| 27 | **Support runbook drafted.** Customer support has playbook-level coverage of the top 5 failure modes and edge states. |
| 28 | **Rollback plan named.** If the release fails, what reverts. Consistent with deploy-ready's rollback discipline. |
| 29 | **Post-launch retrospective scheduled.** 30 days post-launch, a review against Tier 1 success criteria. |
| 30 | **Tier 3 signers plus marketing plus executive sponsor have attested.** |
| 31 | **No have-not remains.** Every item on the disqualifier list below passes. |

**Proof test:** the day-1 launch telemetry can answer, for each Tier 1 success metric, "where are we." If any metric has no live measurement on day 1, Tier 4 is not complete.

## The "have-nots": things that disqualify the PRD at any tier

If any of these appear, the PRD fails its contract and must be fixed before declaring done:

- **Invisible PRD.** The Problem or Target User section survives the substitution test against two competitors. Rewrite with specificity before proceeding.
- **Feature laundry list.** More than seven functional requirements are Must-ranked, or more than twelve requirements are un-ranked. Force prioritization or cut.
- **Solution-first PRD.** The Problem section names the product's solution. Rewrite in the form "users today do X manually, which takes Y and costs Z."
- **Assumption-soup PRD.** "Users will love this," "customers want," "the market demands" without cited evidence or an explicit hypothesis-with-validation plan. Relabel or cut.
- **Moving-target PRD.** An edit has been made to a Tier 2+ document without a changelog entry, or a changelog entry exists but the team was not broadcast to.
- **Hollow PRD.** Any section contains "TBD," "TODO," "coming soon," "we'll figure this out later," "to be determined by the team," without an owner and a due date. Either name an owner and a date, or cut the section.
- **Laundry-list success metrics.** More than five success metrics, or any metric that is a vanity count (total signups, total pageviews, total downloads without engagement qualifier).
- **Fabricated personas.** A target-user paragraph with demographics that do not drive decisions (hobbies, beverage preferences, age range) and no named research citation.
- **Silent NFR dimensions.** A Tier 3 PRD with no security statement, no compliance statement, or no performance threshold. Silence is not an answer.
- **Missing or trivial Out-of-Scope.** An Out-of-Scope section of three bullets or fewer on a Tier 2+ PRD, or a section that says "features beyond v1 scope" without enumeration.
- **Unowned open questions.** Any open question without an owner and a due date. Every unknown is somebody's to answer.
- **Unsigned tier.** A tier declared complete without the tier's required signers attested in writing.
- **Invented NFR thresholds.** "99.99% uptime" or "under 100ms p99" without a stated basis. Either cite the requirement source (SLA contract, industry baseline, customer commitment) or flag as open question.
- **PRD written from a single-sentence prompt.** If the user input was "write a PRD for X" and the skill produced a full PRD without at least a Mode declaration and the seven pre-flight questions answered or explicitly flagged, it is AI-slop PRD output. Refuse.
- **Banned phrases in user-facing sections.** "Industry-leading," "enterprise-grade" (without definition), "seamlessly," "AI-powered" (for non-AI products), "best-in-class," "world-class," "cutting-edge," "game-changing," "revolutionary." These are launch-ready's concern in external copy; in an internal PRD they signal that the writer reached for an adjective instead of a claim. Replace with the specific claim the adjective was covering for, or cut.
- **PRD longer than Tier 1 but shorter than Tier 2's requirements.** A document that is two pages with no MoSCoW ranks is not a Brief and is not a Spec; it is a halfway house. Either commit to Tier 1 and cut, or commit to Tier 2 and write the requirements.
- **No prior-art section at Tier 3.** Three comparable products or projects with status, honestly cited. If prior art cannot be named honestly, the product is more novel than claimed; reconsider. Borrowed from stack-ready and Rust's RFC process.
- **Persona paragraphs written as fiction.** "Sarah is a 35-year-old marketing manager who values efficiency and drinks coffee." Rewrite as concrete role + context + constraint + cited research or flagged research gap.

When you catch yourself about to write any of these, fix it before proceeding. A PRD that ships with any of these is worse than no PRD; the team will act on it and the first thing they cannot build is the first thing to rewrite.

## Reference files: load on demand

The body above is enough to start. Load each reference *before* the step that uses it, not after.

| Reference file | When to load | ~Tokens |
|---|---|---|
| `prd-research.md` | **Always.** Start of every session (Step 0). | ~4K |
| `problem-framing.md` | **Always.** Step 1 pre-flight and Step 2 problem framing. | ~7K |
| `user-personas.md` | **Tier 1.** Step 3 target user. | ~6K |
| `success-criteria.md` | **Tier 1.** Step 4 success metrics. | ~7K |
| `requirements.md` | **Tier 2.** Step 5 functional and Step 6 non-functional. | ~10K |
| `scope-and-out-of-scope.md` | **Tier 2.** Step 7 no-gos and rabbit holes. | ~7K |
| `risks-and-assumptions.md` | **Tier 2.** Step 8 risks, assumptions, open questions. | ~6K |
| `prd-anatomy.md` | **Tier 2.** Step 9 handoff block; also full-template annotated reference. | ~9K |
| `prd-antipatterns.md` | **On demand.** Mode C audits and tier-gate checks against the have-nots. | ~8K |
| `stakeholder-alignment.md` | **Tier 3.** Step 10 sign-off protocol. | ~6K |
| `iterate-vs-freeze.md` | **Tier 3 and Tier 4.** Step 11 lifecycle and change-control. | ~6K |
| `RESEARCH-2026-04.md` | **On demand.** When the user asks "why this rule" or "what is the evidence"; source citations for the initial release. | ~36K |
| `EXAMPLE-PRD.md` | **On demand.** A complete worked example PRD for a fictional B2B SaaS product (Pulse, a Customer Success ops platform). Demonstrates problem framing, MoSCoW ranking, named no-gos, sign-off block, downstream handoff. Useful when the user asks "what should the output look like" or when the agent needs a concrete template; passes the skill's own grep tests for hollow / invisible / feature-laundry / solution-first / assumption-soup / moving-target failure modes. Cross-references to the worked architecture, roadmap, and stack-decision examples in their respective sibling repos. | ~14K |

Skill version and change history live in `CHANGELOG.md`. When resuming a PRD across sessions, confirm the skill version matches the version recorded in the PRD's front matter if one exists. A skill update between sessions can shift have-nots (banned-phrase list evolves as AI outputs shift), add sections (downstream-skill interfaces tighten), or change tier gates. If versions differ, re-run the Tier audit on any Tier 2+ artifact before continuing.

## Session state and handoff

PRDs span sessions; maintain `.prd-ready/STATE.md` when the work is ongoing.

**Template:**

```markdown
# PRD-Ready State

## Skill version
prd-ready [current skill version], [frontmatter updated date].

## Current tier
Working toward Tier [N]. Last completed tier: [N-1].

## Mode
A / B / C / D / E / F.

## Pre-flight answers
(copied from Step 1)

## Active sections
Problem: [status]
Target user: [status]
Success criteria: [status]
Functional requirements: [status]
Non-functional requirements: [status]
Out-of-scope: [status]
Risks / Assumptions / Open questions: [status]
Handoff block: [status]

## Sign-off ledger
- PM: [name, date, attestation]
- Eng lead: [name, date, attestation]
- Design lead: [name, date, attestation]
- [etc.]

## Open questions blocking next tier
- [Q]: [owner], [due date]

## Last session note
[ISO date] [what happened, what's next]
```

**Rules:**
- STATE.md is the contract with the next session. Update at every tier boundary and every context compaction.
- Never delete STATE.md.
- If `PRD.md` and `HANDOFF.md` exist and Tier 3 is reached, STATE.md can be collapsed into the PRD changelog; the PRD becomes the source of truth.

## Suite membership

This skill is part of the **ready-suite**. See [`SUITE.md`](SUITE.md) for the full map.

- **Planning tier:** `prd-ready` (what, this skill), `architecture-ready` (how), `roadmap-ready` (when), `stack-ready` (with what tools).
- **Building tier:** `production-ready` (the app), `repo-ready` (the repo scaffolding).
- **Shipping tier:** `deploy-ready` (ship it), `observe-ready` (keep it healthy), `launch-ready` (tell the world), `harden-ready` (survive adversarial attention).

prd-ready sits at the top of the planning tier. Nothing upstream feeds into it; four downstream siblings consume its output. The harness is the router; this skill tells the user which sibling to invoke next and why.

## Consumes from upstream

This skill sits at the top of its tier and has no upstream consumers. It starts from the user's request directly, with the Step 0 mode detection and the Step 1 pre-flight as the first shape the user gives it.

That said, if the user has prior artifacts the PRD should incorporate (a pitch deck, a board memo, a user-research transcript, an earlier PRD from a pivoted project), the skill reads them at Step 1 as inputs to the pre-flight answers. They are inputs, not upstream skill artifacts.

## Produces for downstream

Four downstream siblings consume this skill's output. Writing these is part of the skill's definition of done.

| Artifact | Path | Consumed by |
|---|---|---|
| **Product Brief / Spec / Full PRD / Launch-Ready PRD** | `.prd-ready/PRD.md` | architecture-ready (entities, flows, NFRs), roadmap-ready (priorities, dependencies), stack-ready (constraints, scale), production-ready (requirements, acceptance criteria) |
| **Downstream handoff block** | `.prd-ready/HANDOFF.md` | Each downstream skill reads its sub-section directly |
| **Session state** | `.prd-ready/STATE.md` | Next prd-ready session resumes here |
| **Open questions log** | `.prd-ready/OPEN-QUESTIONS.md` (optional; may live inline in PRD.md) | All downstream; the log is a live inventory of what the PRD does not yet know |

## Handoff: architecture, roadmap, stack, and build are not this skill's jobs

prd-ready stops at "this is what we are building and for whom, here is what counts as done, here is what we are not building." What comes next:

- To **`architecture-ready`** (not yet released): the PRD's entities, flows, NFRs, integration points, and trust boundaries are read from `.prd-ready/HANDOFF.md` and become the starting point for system design. prd-ready does not draw component diagrams; architecture-ready does.
- To **`roadmap-ready`** (not yet released): the PRD's priorities, dependencies, rabbit holes, and appetite are read from `.prd-ready/HANDOFF.md` and become the inputs to sequencing. prd-ready does not produce a quarter-by-quarter plan; roadmap-ready does.
- To **`stack-ready`** (live, v1.1.5): the PRD's six pre-flight answers are read from `.prd-ready/HANDOFF.md` and become the pre-fill for stack-ready's Step 1 pre-flight. stack-ready skips interrogation and goes to constraint mapping. prd-ready does not pick a framework; stack-ready does.
- To **`production-ready`** (live, v2.5.6): the PRD's entities, CRUD surface, roles, acceptance criteria, and visual-identity direction are read and become the Step 2 architecture-note inputs. prd-ready does not build any feature; production-ready does.

**If your harness exposes a skill-invocation tool** (e.g., Claude Code's Skill tool), invoke the next sibling directly when the handoff trigger fires ("OK, the PRD is Tier 2-signed, which stack should we pick?"). **Otherwise**, surface the handoff to the user: "This step needs `stack-ready`. Install it or handle the sibling layer separately." Do not attempt to generate the sibling's output inline from prd-ready.

## Keep going until every sentence is a decision, a hypothesis, or a question

The problem framing is roughly 25% of the work. The requirement set is another 25%. The Out-of-Scope section, rabbit holes, risks, assumptions, open questions, and the handoff block are the remaining 50%. A user who walks away with "we think we'll build X for Y" but no appetite, no no-gos, no measurable success, and no handoff block does not have a PRD; they have an opinion that will be re-litigated at every tier gate and re-invented at every downstream skill.

When in doubt, ask whether an engineer on the team could read the document tomorrow morning and begin building without scheduling a meeting to ask you questions. The first question they would have to ask you is the next thing to write down.
