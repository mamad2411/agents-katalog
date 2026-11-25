---
name: opportunity-solution-tree
description: "Guides the PM through Teresa Torres' Opportunity Solution Tree (OST) framework for continuous product discovery. Maps a desired outcome to customer opportunities, then to potential solutions, and finally to assumption tests and experiments."
category: discovery
default_depth: standard
---

# Opportunity Solution Tree

Read `docs/workflow-contract.md` once per session before applying this skill. Resolve it from the nearest ancestor of this file containing `manifest.json`; all Shipwright paths are relative to that root.

## Description

Guides the PM through Teresa Torres' Opportunity Solution Tree (OST) framework for continuous product discovery. Maps a desired outcome to customer opportunities, then to potential solutions, and finally to assumption tests and experiments.

## When to Use

- Starting a new discovery cycle for a product area
- Connecting customer pain points to strategic outcomes
- Deciding which solutions to test next
- Aligning a team around a shared discovery map

## Depth

| Scope | Use When | Sections to Include |
|---|---|---|
| **Light** | Quick alignment on which opportunity to pursue next | Steps 1-2 (Desired Outcome + Opportunity Map) only |
| **Standard** | Discovery sprint planning or quarterly roadmap input | All steps |
| **Deep** | Multi-team discovery with shared outcome or bet-level investment | All steps + cross-team opportunity deduplication, assumption interdependency mapping, experiment sequencing timeline |

**Omit rules:** At Light depth, skip Steps 3-5 (Solution Ideas, Assumptions, Assumption Tests). Produce only the outcome and prioritized opportunity map with evidence.

## Framework

### Step 1: Define the Desired Outcome

Ask the PM to state a single, measurable business or product outcome.

**Good outcomes are:**
- Measurable (has a metric attached)
- Time-bound (has a target date or cadence)
- Within the team's influence (not purely external)

**Anti-pattern:** "Increase revenue" is too vague. "Increase trial-to-paid conversion from 8% to 12% by Q3" is actionable.

### Step 2: Map Customer Opportunities

Opportunities are unmet customer needs, pain points, or desires discovered through research. They are NOT features or solutions.

**Format each opportunity as:**
```
[Opportunity ID]: [Description of the customer need/pain]
Evidence: [Source, interview, survey, data, observation]
Frequency: [How often users encounter this]
Severity: [How painful it is when they do]
```

**Rules:**
- Phrase opportunities from the customer's perspective, not the business's
- Prefer specific over general ("can't find the right plan" > "confused by pricing")
- Cluster related opportunities under a parent opportunity when they share a root cause

### Step 3: Generate Solution Ideas

For each prioritized opportunity, brainstorm 3+ distinct solution approaches. Diversity of solutions is critical, avoid anchoring on the first idea.

**Format each solution as:**
```
[Solution ID]: [Brief description]
Opportunity addressed: [Opportunity ID]
Approach: [How this solves the problem]
Effort estimate: [T-shirt size: S/M/L/XL]
Reversibility: [Easy to undo / Hard to undo]
```

### Step 4: Identify Underlying Assumptions

Every solution carries assumptions. Surface them explicitly.

**Assumption categories:**
- **Desirability:** Will customers want this?
- **Viability:** Will this work for the business?
- **Feasibility:** Can we build this?
- **Usability:** Can customers figure this out?

**Format each assumption as:**
```
[Assumption ID]: [Statement that must be true for the solution to work]
Category: [Desirability / Viability / Feasibility / Usability]
Confidence: [High / Medium / Low]
Evidence: [What we know so far, if anything]
```

### Step 5: Design Assumption Tests

Prioritize testing the riskiest assumptions first (low confidence + high impact if wrong).

**For each test:**
```
[Test ID]: [What we're testing]
Assumption: [Assumption ID]
Method: [Prototype test / Survey / Data analysis / Concierge / Wizard of Oz / etc.]
Success criteria: [What result would validate the assumption]
Failure criteria: [What result would invalidate it]
Timeline: [How long to run]
Cost: [Effort required]
```

## Minimum Evidence Bar

**Required inputs:** A measurable desired outcome and at least one customer opportunity with an evidence source. Comparing priorities requires multiple supported opportunities; do not invent alternatives to fill the tree.

**Acceptable evidence:** Customer interview insights, user research synthesis themes, support ticket patterns, behavioral analytics, JTBD opportunity scores, or direct observation of user workarounds.

**Insufficient evidence:** With no evidenced opportunities, return the outcome and evidence gaps, then recommend targeted discovery. With one opportunity, build a scoped branch and label comparative prioritization unavailable.

**Hypotheses vs. findings:**
- **Findings:** Opportunities (Step 2) must cite specific evidence sources. Assumptions flagged as "High confidence" must have supporting data.
- **Hypotheses:** Solutions (Step 3) and assumptions (Step 4) are inherently speculative, label confidence levels honestly and ensure every low-confidence assumption has a test designed in Step 5.

## Output Format

Produce a structured markdown document with:

1. **Desired Outcome**, the single measurable target
2. **Opportunity Map**, hierarchical list of customer opportunities with evidence
3. **Solution Space**, solutions mapped to opportunities
4. **Assumption Register**, all assumptions with risk ratings
5. **Experiment Backlog**, prioritized list of assumption tests

**Shipwright Signature (required closing):**
6. **Decision Frame**, Which opportunity-solution pair to test first, trade-off between assumption risk vs. experiment cost, confidence in opportunity prioritization with evidence quality, owner, decision date, revisit trigger
7. **Unknowns & Evidence Gaps**, Opportunities with single-source evidence, assumption categories (desirability/viability/feasibility/usability) with no tests designed
8. **Pass/Fail Readiness**, PASS if the outcome is measurable, each opportunity is evidenced, and each prioritized solution has a riskiest assumption and test. Light depth may omit solutions and tests. FAIL if the tree invents opportunities or implies unsupported prioritization.
9. **Recommended Next Artifact**, Which Shipwright skill to run next and why

Include a visual tree summary at the top using indented markdown:

```
Outcome: [Desired outcome]
├── Opportunity A
│   ├── Solution A1
│   │   ├── Assumption: [riskiest]
│   │   │   └── Test: [experiment]
│   │   └── Assumption: [next riskiest]
│   └── Solution A2
├── Opportunity B
│   └── Solution B1
```

## Common Mistakes to Avoid

- **Jumping to solutions**, Always start with outcomes and opportunities
- **Single-solution thinking**, Generate at least 3 solutions per opportunity
- **Untested assumptions**, Every solution should have its riskiest assumption identified
- **Confusing outputs with outcomes**, "Ship feature X" is an output; "Reduce churn by 15%" is an outcome
- **Skipping evidence**, Every opportunity needs a source; gut feelings aren't opportunities

## Weak vs. Strong Output

**Weak:**
> Opportunity: "Users find onboarding confusing"
> Evidence: Team discussion

Vague pain description with no customer source, could mean anything and drives no specific solution.

**Strong:**
> Opportunity O3: "New users cannot locate their first workflow within 2 minutes of signup"
> Evidence: 6/8 interview participants (P01, P02, P04, P05, P07, P08) abandoned onboarding at step 3; avg. time-to-first-action = 4.2 min (Mixpanel, Jan 2026)

Specific, measurable, multi-source evidence with participant IDs, directly testable and prioritizable.
