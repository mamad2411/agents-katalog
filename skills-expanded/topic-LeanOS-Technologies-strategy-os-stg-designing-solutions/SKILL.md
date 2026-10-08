---
name: stg-designing-solutions
description: Designs solution architecture, selects growth model, assembles positioning, maps features to problems, and defines MVP scope. Use when constructing Solution Design section during BUILD phase 2.
serves: strategist
domain: solution-design
affects: solution-design-section
depends-on: none
produces: Solution Design section in register format
---

# Solution Design

Design solution architecture: select growth model, assemble positioning, map features to problems, define MVP scope, design growth loops. Output is the Solution Design section of the register -- a derived design artifact constrained by all three hypotheses, not a hypothesis itself.

## Procedure

### Step 1: Load Hypothesis Context [S]

Read: problem, segment, unit economics hypotheses. Also read competitive analysis (gaps, alternatives) for positioning assembly.

Extract constraints each hypothesis places on the solution:
- **Problem** -> what must be solved (top problems by severity)
- **Segment** -> buyer type (user=buyer or committee), ACV range, time-to-value expectations
- **Unit Economics** -> cost constraints (gross margin target, COGS limits)

Extract positioning inputs:
- **Problem claim** -> the problem statement for the positioning template
- **Segment claim** -> the target for the positioning template
- **Competitive analysis** -> alternatives and gaps for the "unlike" clause
- **Aha moment** (assembled in Step 5) -> unique capability clause

Produce: hypothesis constraints table + positioning inputs.

**Gate:** `constraints_extracted: bool` -- at least one constraint from each hypothesis documented, positioning inputs identified.
- Pass: Step 2.
- Fail: If a hypothesis is missing, note the gap. Proceed with available constraints, flagging reduced confidence.

### Step 2: Select Growth Architecture [R]

Score buyer characteristics against decision matrix:

| Factor | PLG | Network | Traditional | Source |
|--------|-----|---------|-------------|--------|
| ACV | < $5K | < $5K | > $25K | Segment hypothesis |
| Buyer type | User = buyer | User = buyer | Committee | Segment hypothesis |
| Time-to-value | < 1 day | < 1 day | Weeks+ | Product nature |
| Collaboration | Optional | Inherent | Either | Product nature |
| Shareability | Medium | High | Low | Product nature |

For ACV between $5K-$25K: Hybrid. Document which factors pulled in which direction.

Selection is T1/T2 (derivable from segment characteristics).

Produce: growth architecture selection with rationale [T1/T2].

**Gate:** `architecture_selected: bool` -- selection justified by segment characteristics, not asserted.
- Pass: Step 3.
- Fail: If factors conflict (e.g., low ACV but committee buyer), flag the tension and select with documented reasoning.

### Step 3: Assemble Positioning [K-grounded]

**Grounded in:** Problem claim, Segment claim, competitive analysis gaps, growth architecture selection.

Assemble the positioning statement from hypothesis outputs -- this is composition, not hypothesis construction. Every clause traces to an existing hypothesis or research output:

- **Target:** from Segment hypothesis claim
- **Problem:** from Problem hypothesis claim
- **Category:** determine the category the product occupies in the buyer's mind. If category is ambiguous or contested, mark as [GOVERNOR_DECISION] for escalation.
- **Differentiator:** from competitive analysis gaps -- what the product does that alternatives do not
- **Unlike [alternative]:** from competitive analysis -- the primary alternative the target currently uses
- **Unique capability:** from aha moment (forward reference -- finalize after Step 5 defines aha moment, revise positioning if needed)

Produce: assembled positioning statement + category framing decision.

Note: the "unique capability" clause depends on the aha moment defined in Step 5. Write a draft here using competitive gaps. Revise after Step 5 if the aha moment provides a stronger unique capability clause.

**Gate:** `positioning_assembled: bool` -- positioning statement has all six clauses filled (unique capability may be draft), category framing documented.
- Pass: Step 4.
- Fail: Identify which clause cannot be filled. If target or problem clause is empty, the upstream hypothesis is missing -- halt and report.

### Step 4: Map Features to Problems [K-grounded]

**Grounded in:** problem hypothesis (top problems), segment characteristics (jobs addressed).

For each top problem, identify features that solve it. For each feature, classify:

| Job Dimension | What It Means | Example |
|--------------|---------------|---------|
| Functional | What they need accomplished | "Generate reports in 2 minutes" |
| Emotional | How they want to feel | "Feel confident in data accuracy" |
| Social | How they want to be perceived | "Be seen as data-driven leader" |

Flag if all features are functional-only: "Technical founders design for the functional job and ignore emotional and social jobs."

Prioritize each feature:
- **MVP** -- minimum for aha moment
- **POST_MVP** -- important but not for first value
- **FUTURE** -- nice to have or expansion

Produce: feature map with job dimensions and priorities [T2].

**Gate:** `features_mapped: bool` -- every feature traces to a stated problem, at least one non-functional job dimension addressed, priorities assigned.
- Pass: Step 4.
- Fail: Features that do not trace to any stated problem must be removed or the problem must be added to the hypothesis. Every feature must trace.

### Step 5: Define MVP Scope [K-grounded]

**Grounded in:** feature map, growth architecture.

MVP = minimum set that delivers the aha moment.

**Aha moment definition:** the specific experience where the user says "this solves my problem." Must be concrete and experiential:
- Good: "Generate a complete design system from 3 inputs in 90 seconds"
- Bad: "See value in the product", "experience efficiency"

**Time-to-value target:**
- PLG: must be < 1 day from signup
- Network: must be < first interaction with other user
- Traditional: must be < first sales call follow-up

**Excluded features:** list each with why excluded and when to add.

**Mode overlay:**
- BOOTSTRAP -> smallest possible MVP for fastest revenue
- VENTURE -> MVP can be slightly larger if it enables growth loop

Produce: MVP scope with aha moment and time-to-value [T2 for scope, T3 for timing effectiveness].

**Gate:** `mvp_defined: bool` -- aha moment is specific and experiential, time-to-value target stated, excluded features have rationale.
- Pass: Step 6. After defining aha moment, revisit Step 3 positioning -- revise "unique capability" clause if aha moment provides a stronger formulation.
- Fail: If aha moment is vague, rewrite with specific experience, observable outcome, and timeframe. If MVP has >5 features, challenge: which single feature delivers the aha moment? Start there.

### Step 6: Design Growth Loops [K-grounded]

**Grounded in:** growth architecture, feature map, segment characteristics.

For selected architecture, define growth mechanisms:

| Architecture | Loop Pattern | Requires |
|-------------|-------------|----------|
| PLG | Product usage -> sharing -> new signups -> more usage | Shareable output, invite mechanism |
| Network | User joins -> invites others -> network value increases | Collaboration features, density threshold |
| Traditional | Sales close -> implementation success -> referral | Customer success process, case studies |

Each loop: mechanism, what it requires (features, scale), tier label.

Produce: growth loop definitions [T2].

**Gate:** `loops_designed: bool` -- at least 1 growth loop with mechanism, requirements, and tier label.
- Pass: Step 7.
- Fail: If no natural growth loop exists for the architecture, document: "Growth loop is weak -- customer acquisition will depend primarily on paid channels." This is a finding.

### Step 7: Write Solution Design Section [S]

Write complete Solution Design section in register format:

- **Growth Architecture:** {PLG | Network | Traditional | Hybrid} with rationale
- **Architecture Rationale:** ACV, buyer type, time-to-value, collaboration, selection reasoning
- **Positioning:** assembled statement with all six clauses, category framing, category rationale
- **Feature Map:** table with feature, solves problem, job dimension, priority, tier
- **MVP Scope:** included features, aha moment, time-to-value target, excluded features with rationale
- **Growth Loops:** loop name, mechanism, requirements, tier
- **Constraints from Hypotheses:** table with constraint from each hypothesis (Problem, Segment, Unit Economics) and what to re-evaluate if hypothesis changes
- **Adequacy Criteria:** specific, measurable criteria for solution adequacy (not kill conditions -- this is a design artifact, not a hypothesis)
- **Last Updated:** date

Produce: complete Solution Design section.

**Gate:** `section_written: bool` -- all fields populated, positioning statement complete, constraints reference all three hypotheses.
- Pass: Done.
- Fail: Fix missing fields. Ensure constraints table references all three hypotheses. Ensure positioning statement has all six clauses finalized (unique capability revised after aha moment).

## Quality Criteria

- Growth architecture selection justified by segment characteristics (not asserted)
- Positioning statement assembled from hypothesis outputs (not invented independently)
- Every positioning clause traces to a hypothesis claim or competitive analysis output
- Category framing decision documented (with governor escalation if ambiguous)
- Every MVP feature traces to a problem in the Problem hypothesis
- At least one feature addresses emotional or social job (not all functional)
- Aha moment is specific and experiential (not a vague benefit)
- Constraints from all three hypotheses documented
- Excluded features have rationale and "when to add" guidance
- Growth loops are mechanistically described (not just named)

## Failure Modes

| Mode | Signal | Recovery |
|------|--------|----------|
| Feature completeness before launch | MVP contains >5 features or includes "platform" / "ecosystem" language | Flag technical founder pattern. Ask: which single feature delivers the aha moment? Start there. Everything else is POST_MVP until customer evidence demands it |
| Aha moment is vague | "Users see value", "teams get results", "experience efficiency" | Rewrite as specific experience with observable outcome and timeframe. "Complete X task in Y minutes that previously took Z hours" |
| Growth architecture mismatch | PLG selected but ACV >$25K, or Traditional selected but ACV <$2K | Architecture-ACV misalignment. Either the pricing is wrong or the architecture is wrong. Flag for resolution in economics hypothesis |
| Positioning invented rather than assembled | Positioning statement contains claims not traceable to any hypothesis or competitive analysis | Every clause must trace to a source. Target = Segment claim. Problem = Problem claim. Alternative = competitive analysis. If a clause has no source, it is fabrication |
| Solution not constrained by hypotheses | Features that do not trace to any stated problem; growth loops that assume segment behaviors not in evidence | Every feature must trace to the Problem hypothesis. Every growth loop must be consistent with Segment characteristics. Remove untraced elements or add the tracing |

## Boundaries

**In scope:** Growth architecture selection, positioning assembly from hypothesis outputs, feature-to-problem mapping with JTBD dimensions, MVP scope definition with aha moment, growth loop design, hypothesis constraint documentation, adequacy criteria.

**Out of scope:** Pricing design (stg-designing-pricing), economics calculation (stg-calculating-economics), problem scoring (stg-scoring-problems), competitive analysis (stg-analyzing-competition).
