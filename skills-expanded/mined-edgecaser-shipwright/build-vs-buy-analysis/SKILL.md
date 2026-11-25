---
name: build-vs-buy-analysis
description: "Evaluates whether to build a capability in-house, buy/license from a vendor, integrate via API, adopt open-source, or partner. Produces a total-cost-of-ownership comparison anchored to strategic fit, not just sticker price, with explicit kill criteria for revisiting the decision."
category: strategy
default_depth: standard
---

# Build-vs-Buy Analysis

Read `docs/workflow-contract.md` once per session before applying this skill. Resolve it from the nearest ancestor of this file containing `manifest.json`; all Shipwright paths are relative to that root.

## Description

Evaluates whether to build a capability in-house, buy/license from a vendor, integrate via API, adopt open-source, or partner. Produces a total-cost-of-ownership comparison anchored to strategic fit, not just sticker price, with explicit kill criteria for revisiting the decision.

## When to Use

- Engineering wants to build something that already exists as a product (e.g., billing, auth, search)
- A vendor contract is up for renewal and the team is questioning whether to keep paying or replace it
- A new capability is needed and it's unclear whether it's core to the product or commodity infrastructure
- Technical debt in a bought solution is mounting and the team is debating a rebuild
- An open-source tool is being evaluated against a commercial alternative

## Depth

| Scope | Use When | Sections to Include |
|---|---|---|
| **Light** | Quick sanity check on an obvious build or buy decision (e.g., "should we write our own email delivery?") | Step 1 (Capability Gap), Step 2 (Options, top 2-3), Step 4 (Strategic Fit, core vs. context only) |
| **Standard** | Genuine ambiguity between build and buy with real trade-offs | All sections |
| **Deep** | High-stakes decision with significant investment (e.g., $500K+ annual spend, 6+ eng-months build), multiple stakeholders, or irreversibility risk | All sections + vendor comparison matrix, reference customer calls, detailed year-over-year TCO model, migration/exit cost analysis per option |

**Omit rules:** At Light depth, skip Step 3 (Total Cost of Ownership), Step 5 (Decision and Kill Criteria), and the full Output Format. Produce only the capability gap definition, top options, and a core-vs-context verdict with one-line rationale. If the answer is obvious at Light depth (e.g., "don't build your own payment processor"), say so and stop.

## Framework

### Step 1: Define the Capability Gap

Name the specific capability you need, not the solution category. Be precise enough that you could write acceptance criteria for it.

```markdown
## Capability Gap

**What we need:** [Specific capability, e.g., "Recurring billing with usage-based metering, proration, and self-serve plan changes for 3 pricing tiers"]

**Why now:** [Trigger, e.g., "Current flat-rate pricing can't support the enterprise tier launching Q3"]

**Current state:** [How this is handled today, e.g., "Manual invoicing via spreadsheet + Stripe one-time charges, ~4 hrs/week finance overhead"]

**Must-have requirements:**
- [Requirement 1, e.g., "Support usage-based metering at 5-minute granularity"]
- [Requirement 2, e.g., "Self-serve plan upgrades/downgrades without CS involvement"]
- [Requirement 3, e.g., "SOC 2 Type II compliant"]

**Nice-to-have requirements:**
- [Requirement, e.g., "Revenue recognition reporting for ASC 606"]
```

### Step 2: Identify Options

List every realistic path. Do not pre-filter to build vs. buy, the actual option space is wider.

```markdown
## Options

| Option | Description | Example |
|---|---|---|
| **Build in-house** | Custom implementation owned by your engineering team | Build billing service on top of Stripe primitives |
| **Buy / License SaaS** | Commercial product, vendor-managed | Adopt Chargebee, Recurly, or Maxio |
| **Integrate via API** | Use a platform's API as building blocks, own the UX layer | Stripe Billing API with custom dashboard |
| **Open-source + Maintain** | Deploy and maintain an OSS project | Self-host Kill Bill or Lago |
| **Partner / Outsource** | Third party operates the capability on your behalf | Contract a billing-ops firm |

### Options Under Consideration

For each viable option, capture:
- **Vendor/project:** [Name]
- **Fits must-haves?** [Yes / Partial, which gaps / No]
- **Maturity:** [GA / Beta / Community-maintained]
- **Reference customers in our segment:** [Names or "none found"]
```

### Step 3: Total Cost of Ownership

Compare costs over a 3-year horizon. Include all cost categories, sticker price is the least interesting number.

```markdown
## TCO Comparison (3-Year Horizon)

| Cost Category | Build In-House | Buy/License [Vendor] | API Integration | Open-Source + Maintain |
|---|---|---|---|---|
| **Upfront build/integration** | [eng-months × loaded cost] | [implementation fee + eng integration] | [eng-months × loaded cost] | [eng-months × loaded cost] |
| **Annual licensing/SaaS fees** | $0 | [$X/yr, note pricing model] | [API usage fees] | $0 |
| **Ongoing maintenance** | [eng-months/yr × loaded cost] | [admin overhead] | [eng-months/yr × loaded cost] | [eng-months/yr, patches, upgrades, security] |
| **Scaling costs** | [How cost grows with usage] | [Per-seat, per-transaction, or tier pricing] | [API call pricing at 10x volume] | [Infrastructure costs at scale] |
| **Opportunity cost** | [What those engineers won't build] | [Vendor roadmap doesn't match yours] | [Partial lock-in to platform] | [Community abandonment risk] |
| **Migration/exit cost** | N/A (you own it) | [Data export difficulty, re-integration] | [API swap difficulty] | [If project dies, fork + maintain cost] |
| **3-Year Total** | [$X] | [$X] | [$X] | [$X] |

**Key assumptions:**
- Loaded engineering cost: [$X/month per engineer]
- Expected scale: [current → projected over 3 years]
- Discount rate applied: [yes/no]
```

### Step 4: Strategic Fit Evaluation

Cost is one input. Strategic fit determines whether cheap is actually good.

```markdown
## Strategic Fit

| Criterion | Build | Buy | API | Open-Source |
|---|---|---|---|---|
| **Core vs. Context** | [Is this capability a competitive differentiator or commodity infrastructure?] | | | |
| **Differentiation potential** | [Can custom implementation create a better user experience than off-the-shelf?] | | | |
| **Control requirements** | [Do you need to own the data model, release cadence, or UX?] | | | |
| **Time-to-value** | [How fast does each option get you to production?] | | | |
| **Vendor lock-in risk** | N/A | [Switching cost if vendor raises prices or degrades] | [API portability, is there a standard?] | [Community health, contributors, commits, funding] |
| **Team capability** | [Do you have the expertise to build and maintain this?] | [Do you have the expertise to evaluate and manage the vendor?] | | |
| **Compliance/security** | [Internal audit implications] | [Vendor's compliance posture] | [Data residency, shared responsibility] | [Self-managed security burden] |
```

**Core vs. Context test (Geoffrey Moore):**
- **Core:** Activities that directly increase competitive advantage. You should own these.
- **Context:** Everything else. You should outsource or buy these to free up resources for core work.

Rule of thumb: If two competitors could swap this component and neither would gain an advantage, it's context. Buy it.

### Step 5: Decision and Kill Criteria

Commit to one path. Avoid "let's build a prototype and see" unless you define what "see" means with a deadline.

```markdown
## Decision

**Chosen path:** [Build / Buy / API / Open-Source / Partner]
**Rationale (1-2 sentences):** [Why this path wins given the TCO and strategic fit analysis]

**What we're explicitly giving up:**
- [Trade-off 1, e.g., "We lose billing UX customization but save 4 eng-months"]
- [Trade-off 2, e.g., "We accept vendor lock-in risk in exchange for 6-week time-to-value"]

## Kill Criteria (Conditions to Revisit This Decision)

| Trigger | Threshold | Action |
|---|---|---|
| Vendor price increase | [e.g., ">25% YoY or >$X/yr"] | Re-run TCO with updated pricing |
| Build timeline overrun | [e.g., ">150% of estimated eng-months"] | Stop build, evaluate buy fallback |
| Scaling cost surprise | [e.g., "API costs exceed $X/month at current growth"] | Evaluate self-hosted alternative |
| Capability gap emerges | [e.g., "Vendor can't support requirement X by Q date"] | Scope custom build for the gap |
| Team attrition | [e.g., "Maintainer leaves and no one else understands the system"] | Assess buy/partner option |
```

## Minimum Evidence Bar

**Required inputs:** A capability gap, must-have requirements and candidate options. A decision to spend or build requires real pricing and engineering estimates for at least two options; Light directional fit analysis may explicitly defer those numbers.

**Acceptable evidence:** Vendor pricing pages or quotes, engineering estimates from the team that would build it, reference customer case studies, open-source project health metrics (GitHub stars alone are insufficient, look at commit frequency, maintainer count, issue response time), prior experience with similar build/buy decisions at the company.

**Insufficient evidence:** If no engineering estimate exists for the build option, or no pricing exists for the buy option, the TCO comparison is fiction. Stop and gather real numbers before completing Step 3. Produce Steps 1-2 and Step 4 (strategic fit) as a draft to guide the data-gathering effort.

**Hypotheses vs. findings:**
- **Findings:** Vendor pricing confirmed by sales quote, engineering estimate reviewed by tech lead, reference customer validated the vendor's claims
- **Hypotheses:** Scaling cost projections, maintenance burden estimates, vendor roadmap promises, must be labeled with source and confidence level

## Output Format

Produce a Build-vs-Buy Decision Brief with:
1. **Capability Gap Summary**, what you need, why now, must-have requirements
2. **Options Evaluated**, all paths considered with quick fit assessment
3. **TCO Comparison**, 3-year cost table with key assumptions stated
4. **Strategic Fit Verdict**, core vs. context determination with supporting rationale
5. **Recommendation**, chosen path with explicit trade-offs acknowledged
6. **Kill Criteria**, table of triggers that would reopen the decision

**Shipwright Signature (required closing):**
7. **Decision Frame**, Recommended path with primary trade-off (cost vs. control, speed vs. flexibility), confidence level with evidence quality, decision owner, decision date, revisit trigger
8. **Unknowns & Evidence Gaps**, Missing vendor quotes, unvalidated engineering estimates, untested scaling assumptions, vendor roadmap items taken on faith
9. **Pass/Fail Readiness**, PASS for a spending/build decision if comparable TCO uses sourced prices and estimates for at least two options and strategic fit is justified. Light depth may PASS only as a directional fit assessment with cost gaps explicit; it cannot authorize procurement or engineering commitment.
10. **Recommended Next Artifact**, Which Shipwright skill to run next and why

## Common Mistakes to Avoid

- **Comparing sticker price to build cost**, A $50K/yr SaaS license looks expensive until you account for the 3 engineers spending 20% of their time maintaining the in-house alternative. Always compare total cost of ownership, including opportunity cost.
- **Treating "build" as free**, Engineering time has a loaded cost ($15-25K/month per engineer at most companies) and an opportunity cost (what those engineers won't build). If your build estimate is "a few sprints," you haven't estimated seriously.
- **Ignoring migration and exit costs**, The cheapest vendor is expensive if extracting your data later costs 6 eng-months. Ask "what happens if we need to leave?" before signing.
- **Letting sunk cost drive the decision**, "We already built half of it" is not a reason to keep building. Evaluate the remaining cost to finish and maintain vs. switching, not the cost already spent.
- **Conflating "not invented here" with strategic advantage**, Building your own auth system is almost never a competitive advantage. Reserve custom builds for capabilities where your implementation is visibly better to the customer, not just different.

## Weak vs. Strong Output

**Weak:**
> "We should buy because building would take too long and cost too much. Stripe is the industry standard so we should just use it."

No TCO numbers, no requirements check, no strategic fit analysis, no kill criteria. This is an opinion dressed as a recommendation.

**Strong:**
> "Capability: usage-based billing with metering at 5-minute granularity for 3 tiers. Build estimate: 4 eng-months upfront + 1 eng-month/yr maintenance (source: tech lead review, Mar 2026). Stripe Billing: $0 platform fee + 0.7% per invoice, est. $42K/yr at projected volume. 3-year TCO: Build $680K (loaded cost + opportunity cost of delayed analytics platform) vs. Stripe $186K. Strategic fit: Billing is context, not core, our differentiator is the analytics layer, not the payment flow. Recommendation: Stripe Billing API with custom dashboard. Kill criteria: revisit if Stripe pricing exceeds $75K/yr or metering granularity requirement drops below 1-minute intervals."

Real numbers, stated sources, explicit trade-offs, and conditions under which the decision changes.
