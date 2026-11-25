---
name: value-spec-review
description: Review a product specification through a Chief Product Officer lens, focused on value specs (not feature specs). Produces a strategic, business-oriented critique structured in three sections — value definition of the problem space, gaps in capabilities, and second-order impact if delivered — with a CPO-style bottom-line approval/non-approval recommendation. Trigger on phrases like "review this spec", "review this value spec", "analyze this spec", "CPO review", "product spec review", "spec analysis", "review my PRD", "critique this spec", "pressure-test this spec", "give me a CPO perspective on this", "what would a CPO say about this", or any slash commands like "/specreview", "/valuespec", "/cporeview". Also trigger when the user shares a Notion link, Google Doc, file, or pasted spec content and asks for review, feedback, critique, or analysis from a product leadership angle. Use this skill whenever a user wants strategic spec critique even if they don't name the framework — but skip for narrow engineering-detail reviews where the user explicitly wants implementation feedback, not value-level critique.
---

# Value Spec Review

A Chief Product Officer's review of a product specification. The goal is to surface strategic issues — value framing, capability gaps, second-order consequences — that engineering-led specs typically under-address. The output is direct, decision-oriented, and ends in an approve / don't-approve / approve-with-changes recommendation.

## The lens

This is a **value spec** review, not a feature spec review. The reviewer reads the document as a CPO would: looking for whether the investment is defensible, whether the customer problem is real and quantified, whether the capability set is coherent, and whether the second-order effects (positive and negative) have been priced in. Engineering rigor in the document is noted but not the primary scoring axis.

Engineering-led specs tend to be strong on *what* and *how*, weak on *why for the customer* and *what happens next*. This skill leans into those weak spots deliberately.

## When this fires

- **Explicit invocation** — "review this spec", "give me a CPO review", "/specreview", "/valuespec", "/cporeview", "analyze this value spec".
- **Implicit invocation** — user shares a Notion link, Google Doc, file upload, or pasted spec text and asks for review, critique, feedback, pressure-test, or "what do you think". When the artifact is clearly a product spec and the ask is evaluative, run this skill.

If the user invokes the skill without a spec attached, ask for it before proceeding. Do not improvise a generic answer.

## Input gathering

If the user has not yet provided a spec, ask:

> Which spec would you like me to review? Paste the content, share a Notion or Google Doc URL, or upload a file. If it has companion docs (PRD, URD, related implementation packs), point me at those too — second-order analysis is sharper when the surrounding product context is visible.

If the user provides only a Notion link, fetch it via the Notion connector. If they provide a Google Doc, fetch via the Drive connector. If a file is uploaded, read it directly. If they paste content inline, work from that.

If the spec references companion documents (PRD, URD, implementation packs, reconciliation policies, etc.) and they are linked, scan their titles to understand context — but the review is of the spec the user named, not its companions.

## The three sections (required output structure)

The review must produce three labeled sections, in this order, with a closing bottom line. Each section is substantive — five to ten findings is typical, each one a punchy paragraph or tight bullet. Avoid nitpicks; aim at issues that change the investment decision.

### 1. Value definition of the problem space

Pressure-test whether the spec defends *why this matters to the customer*, not just why it matters to engineering. Look for:

- **Customer-pain framing vs. internal-dependency framing.** Specs often say "X is foundational to everything else we want to build." That's an engineering dependency, not a customer pain. Flag it.
- **Quantified problem.** Prevalence, severity, addressable market. If the spec says "customers struggle with X" without a number behind it, call it out.
- **Job-to-be-done clarity.** Who is the customer, what job are they hiring this capability to do, and what are they hiring today instead?
- **Competitive context.** Who else solves this problem and why does the company's wedge matter? If absent, name the competitors the spec should have addressed.
- **Standalone value of the deliverable.** Especially for previews / MVPs / phase-1 scopes — what does the customer *get* from this phase on its own? If the answer is "nothing operational until phase 2", surface that explicitly.
- **Urgency.** Why now and not in twelve months? Forcing functions (regulatory, competitive, market) should be named.
- **Customer success metric.** Distinct from technical success metrics. If graduation criteria are all throughput / accuracy / no-incidents, flag that no *customer outcome* is being measured.
- **Persona-to-value linkage.** Personas listed should map to a value they receive, not just a role they play.
- **For previews specifically — the design partner value exchange.** What does the DP get for their time? "Validate our inventory" is what the DP *does*, not what they *get*.

### 2. Gaps in capabilities

Identify what the spec says is in scope vs. what it must also do to deliver the value it claims. Look for:

- **Definitional gaps in the success criteria.** "95% accuracy" — accuracy of what, measured how? Unfalsifiable graduation gates are the most common failure mode.
- **Coverage gaps the spec admits but does not size.** If the deployment model creates structural blind spots (e.g., agent only runs on certain endpoints, scanner depends on network adjacency), the spec should estimate the expected coverage, not just acknowledge the limit.
- **Edge-case handling.** Unknown / unidentified items, false positives, conflicts between data sources, nomadic / mobile entities, multi-tenant ownership, items the system finds but cannot classify.
- **Customer-facing gaps.** RBAC, multi-tenancy, retention policy, audit trails, PII / PHI / regulated-data handling, localization, accessibility.
- **Feedback loop gaps.** Can the customer correct, override, tag, annotate? If not, how does the content / catalog / training pipeline get better over time?
- **Operational readiness gaps.** Onboarding playbook, pre-flight checklist, escalation path, support model, telemetry strategy.
- **Disambiguation gaps.** If the company has adjacent products that look similar, the spec should explain how this differs. Customers and sales reps will ask.
- **Resourcing and timeline gaps.** No dates, no FTE estimates, no test-fleet budget — common in technical specs and a CPO blocker.
- **Dependency gaps.** If a separate workstream (e.g., a platform capability, a content licensor agreement, a sensor framework) is required for the spec to ship its claimed value, that dependency should be first-class in the plan, not a footnote.

### 3. Second-order impact if delivered

This is the section where a CPO earns their salary — the consequences (positive and negative) of shipping what the spec describes. Two sub-buckets:

**Positive second-order impacts (the leverage to underwrite).** These are the strategic reasons to fund the work even if the first-order deliverable looks narrow. Look for:

- Platform / data-model multipliers (does this new asset class or capability compound across existing products?)
- Adjacent-market wedges (does this protocol stack, data shape, or persona generalize to other domains?)
- Channel / GTM enablement (does this strengthen positioning against a specific competitor, or open a new buyer persona?)
- Regulatory / compliance lift (does this enable a specific named compliance requirement that unblocks a market?)
- Customer-relationship deepening (does this make the company the system-of-record for something new?)

**Risks to price in (the part most specs miss).** These are the failure modes a CPO must consider before approval:

- **Expectation overhang.** If the spec lists downstream use cases as motivation, customers will demand them the moment phase 1 ships. Is the pacing and messaging discipline in place?
- **Reputation and trust risk.** Does the new capability change the product's posture in a way that long-time customers will notice (e.g., a low-impact agent now doing active network scanning, a read-only system now holding credentials)?
- **Credential / data / security blast radius.** Every new integration expands attack surface. Is rotation, scoping, and incident-response addressed?
- **Legal / IP posture.** Customer-contributed data, content-licensor agreements, third-party IP — any unresolved contractual question that could ship-block.
- **Segment / pricing / packaging conflict.** If the capability is "included" in an existing product, where's the incremental revenue? If it's a separate SKU, what's the cannibalization risk?
- **Engineering coordination overhead.** Parallel claimable workstreams that pivot on a single integration point create refactor risk.
- **Data-model lock-in.** Schemas committed in phase 1 persist into phase N. Pressure-test that the model generalizes.
- **Competitive socialization.** Design partners and external content licensors increase information leakage.
- **Sales / marketing / CSM readiness.** Who owns DP relationships, who positions the GA, who supports it in field?
- **Sequencing dependencies that gate value delivery.** If shipping phase 1 doesn't unlock customer value until phase 2 ships, and phase 2 has its own dependencies, the value-delivery timeline is longer than the spec implies.

## Output format

The review is delivered as prose with light structure: a brief intro, three clearly-labeled sections, and a closing bottom line.

### Intro

One short paragraph: state what the spec is, characterize its overall posture (e.g., "engineering-ready but value-thin", "tightly scoped but missing competitive context", "strategically defended but operationally vague"), and name the verdict that the rest of the review will defend.

### The three sections

Use H2 headers: `## 1. Value definition of the problem space`, `## 2. Gaps in capabilities`, `## 3. Second-order impact if delivered`. Inside each section, prefer bolded lead-ins followed by a sentence or two of explanation. Long enough to be substantive, short enough to be scannable.

For section 3 specifically, use two clearly-separated sub-buckets: positive impacts and risks to price in.

### Bottom line

Close with a `## Bottom line` section that delivers the CPO verdict in 2–4 sentences. Pattern:

> The spec is [strong somewhere] but [weak somewhere else]. As written I would [approve / approve with conditions / not approve] [reason]. The conditions for approval are: (1) ..., (2) ..., (3) .... The strategic logic ([leverage point]) is sound — the spec just doesn't yet defend it the way the investment requires.

End with a concrete offer of next steps tied to what the review surfaced — typically one of:

- "Want me to draft a one-page value brief that closes the gaps in section 1?"
- "Want me to annotate the [Notion / Google] doc directly with comments tied to specific sections?"
- "Want me to produce a redlined version of the spec with the changes inline?"
- "Want me to draft the missing [open-questions resolution / DP value brief / competitive-positioning section]?"

## Style

- **Direct.** This is a peer review between product leaders, not a customer email. Don't soften, don't equivocate, don't bury the verdict.
- **Strategic, not nitpicky.** Skip typos, formatting issues, broken links. Surface issues that change the investment decision.
- **Specific.** Quote section numbers and specific phrases from the spec when calling something out. Vague critiques ("the value section is weak") are unhelpful; specific critiques ("§1.0 frames identification as a dependency on downstream capabilities rather than as a customer pain — the seven use cases listed are aspirational, not committed") are actionable.
- **Constructive.** Every gap identified should imply a fix the author could make. The closing bottom line should give the author a path forward, not a verdict-with-no-recourse.
- **Honest about strengths.** Good specs have parts worth preserving. Name them — both for accuracy and to signal that the critique is calibrated.

## What good looks like

A spec that would pass this review without major changes typically has:

- A customer-pain hypothesis with at least one quantified baseline
- A clear job-to-be-done and a named alternative the customer is hiring today
- A wedge thesis vs. named competitors
- A standalone value claim for the phase being scoped (not just "foundation for phase 2")
- At least one customer-outcome metric in the success criteria, distinct from technical metrics
- A timeline, an FTE estimate, and a named engineering lead
- A list of dependencies with their own owners and timelines
- An explicit risk register including credential / data / contractual / competitive risks
- A pricing / packaging posture (even if "TBD, decision by date X")
- A design-partner or early-adopter value exchange (for previews)

Use this list as the implicit rubric — gaps against it become findings in sections 1 and 2.

## Reminder

The user invoked this skill because they want a CPO's pressure-test, not a cheerleader. Be the toughest reasonable reader of the document. If after honest review the spec is genuinely good, say so — but the default posture is skeptical-but-fair, and most specs will not pass without changes.
