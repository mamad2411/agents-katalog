---
name: design-review
description: "Runs a multi-stakeholder design review by evaluating a product proposal through 7 parallel perspectives: Engineering, Design, Executive, Legal/Compliance, Customer Voice, Devil's Advocate, and Sales/GTM. Produces a synthesized review with consensus points, tensions, blockers, and open questions."
category: technical
default_depth: standard
---

# Design Review Facilitator

Read `docs/workflow-contract.md` once per session before applying this skill. Resolve it from the nearest ancestor of this file containing `manifest.json`; all Shipwright paths are relative to that root.

## Description

Runs a multi-stakeholder design review by evaluating a product proposal through 7 parallel perspectives: Engineering, Design, Executive, Legal/Compliance, Customer Voice, Devil's Advocate, and Sales/GTM. Produces a synthesized review with consensus points, tensions, blockers, and open questions.

## When to Use

- Before finalizing a PRD or technical spec
- Reviewing a major feature design before committing engineering resources
- When a proposal needs sign-off from multiple stakeholders
- Stress-testing a design before presenting to leadership
- Any time you want to catch blind spots before they become expensive mistakes

## Depth

| Scope | Use When | Sections to Include |
|---|---|---|
| **Light** | Small feature or low-risk change | Review Setup + 3 perspectives (Engineering, Customer Voice, Devil's Advocate) + Synthesis |
| **Standard** | Typical feature or cross-team project | All 7 perspectives + full Synthesis |
| **Deep** | Major platform bet or irreversible architecture decision | All 7 perspectives + external benchmarking, red team scenario modeling, written stakeholder sign-off |

**Omit rules:** At Light depth, skip Design/UX, Executive, Legal, and Sales/GTM perspectives. Produce only Review Setup, the 3 core perspectives, and a condensed Synthesis.

## Framework

### Step 1: Set Up the Review

```markdown
## Design Review: [Feature / Proposal Name]

### Document Under Review
- **Type:** [PRD / Tech Spec / Design Mockup / Business Case]
- **Author:** [name]
- **Version:** [v1.0]
- **Link:** [document link]

### Review Scope
- **What to evaluate:** [Specific questions or areas to focus on]
- **What's already decided:** [Constraints or decisions that are non-negotiable]
- **Timeline:** [When the review needs to be complete]
```

### Step 2: Run the Selected Perspectives

Evaluate the document from each stakeholder perspective. Two rules apply to every perspective:

- **Cite what you checked.** Every verdict, Green included, lists the sections of the document and the evidence it was checked against. A Green with no cited checks is an unassessed perspective, not a clean one.
- **Do not simulate input you do not have.** If a perspective has no real input (no legal team or compliance documentation, no sales data, no customer research), mark its verdict `Not assessed` and state what input would be needed. Do not invent concerns, findings or requirements to fill the slot.

At Light depth, use only Engineering, Customer Voice, and Devil's Advocate. At Standard and
Deep depth, use all seven perspectives. When one model runs several perspectives, they are one
reviewer's views organized under headings, not independent opinions. Say so in the Synthesis and
treat the output as preparation for human review.

```markdown
## Perspective Reviews

### 1. Engineering Perspective
**Evaluator mindset:** "Can we build this reliably, performantly, and maintainably?"

**Feasibility Assessment:**
- [ ] Is the scope technically feasible within the proposed timeline?
- [ ] Are there hidden complexities not addressed in the spec?
- [ ] Does this create technical debt? How much?

**Architecture Concerns:**
- [Concern 1]: [Description and severity]
- [Concern 2]: [Description and severity]

**Missing Technical Details:**
- [Gap 1]: [What needs clarification]

**Effort Estimate Validation:**
- Proposed: [estimate from spec]
- Engineering assessment: [revised estimate if different]
- Delta rationale: [why the difference]

**Checked against:** [Sections of the document reviewed, and the evidence used: estimates, architecture docs, prior incidents]

**Verdict:** [Green: Feasible as-is / Yellow: Feasible with changes / Red: Needs rethink / Not assessed: no engineering input, needs (what)]

---

### 2. Design / UX Perspective
**Evaluator mindset:** "Will this be intuitive, accessible, and delightful for our users?"

**Usability Assessment:**
- [ ] Does the flow match established user mental models?
- [ ] Are error states and edge cases designed?
- [ ] Is the information hierarchy clear?

**Accessibility Review:**
- [ ] Keyboard navigation considered?
- [ ] Screen reader compatibility addressed?
- [ ] Color contrast and visual accessibility checked?

**Consistency Check:**
- [ ] Follows existing design system patterns?
- [ ] New patterns needed? If so, are they justified?

**Concerns:**
- [Concern 1]: [Description, UX risk]

**Checked against:** [Sections reviewed and evidence used]

**Verdict:** [Green / Yellow / Red / Not assessed: no input for this perspective, needs (what)]

---

### 3. Executive / Strategy Perspective
**Evaluator mindset:** "Does this align with our strategy and move the right metrics?"

**Strategic Alignment:**
- [ ] Supports which strategic bet? [Bet name]
- [ ] Moves which key metric? [Metric and expected impact]
- [ ] Opportunity cost: What are we NOT doing to do this?

**Business Case Validation:**
- Expected impact: [projected outcome]
- Confidence level: [High / Medium / Low]
- Time to value: [how long until we see results]

**Concerns:**
- [Concern 1]: [Strategic risk]

**Checked against:** [Sections reviewed and evidence used]

**Verdict:** [Green / Yellow / Red / Not assessed: no input for this perspective, needs (what)]

---

### 4. Legal / Compliance Perspective
**Evaluator mindset:** "Does this create legal, regulatory, or compliance risk?"

**Data & Privacy:**
- [ ] What PII is collected, processed, or stored?
- [ ] GDPR/CCPA compliance implications?
- [ ] Data retention and deletion requirements?

**Regulatory:**
- [ ] Industry-specific regulations affected?
- [ ] Accessibility regulations (ADA, WCAG)?

**Contractual:**
- [ ] Affects existing customer contracts or SLAs?
- [ ] New terms of service needed?

**Concerns:**
- [Concern 1]: [Legal/compliance risk]

**Checked against:** [Privacy policy, DPA, contract terms, or regulatory guidance actually consulted. If none, this perspective is Not assessed.]

**Verdict:** [Green / Yellow / Red / Not assessed: no legal or compliance input, needs (what)]

---

### 5. Customer Voice Perspective
**Evaluator mindset:** "Would our target customer actually want this, and would they understand it?"

**Demand Validation:**
- [ ] What evidence supports customer demand? [Source]
- [ ] Which persona benefits most?
- [ ] What job-to-be-done does this address?

**Adoption Concerns:**
- [ ] Will customers discover this feature?
- [ ] Is the learning curve acceptable?
- [ ] Does this solve the problem as customers frame it (not just how we frame it)?

**Voice of Customer Data:**
- [N] customers have requested this
- NPS/feedback mentions: [relevant data]
- Competitive pressure: [are customers asking because competitors have it?]

**Concerns:**
- [Concern 1]: [Adoption or demand risk]

**Checked against:** [Sections reviewed and evidence used]

**Verdict:** [Green / Yellow / Red / Not assessed: no input for this perspective, needs (what)]

---

### 6. Devil's Advocate Perspective
**Evaluator mindset:** "What are we wrong about? What could go catastrophically wrong?"

**Assumption Challenges:**
| Assumption in the Proposal | Why It Might Be Wrong | Evidence |
|---|---|---|
| [Assumption 1] | [Counter-argument] | [Data or reasoning] |
| [Assumption 2] | [Counter-argument] | [Data or reasoning] |

**Worst-Case Scenarios:**
1. [Scenario]: [What happens and how bad is it]
2. [Scenario]: [What happens and how bad is it]

**What's Missing:**
- [Blind spot 1]: [Something the proposal doesn't address]

**Kill Case:** Under what conditions should we NOT build this?
- [Condition 1]

**Checked against:** [Sections reviewed and evidence used]

**Verdict:** [Green / Yellow / Red / Not assessed: no input for this perspective, needs (what)]

---

### 7. Sales / GTM Perspective
**Evaluator mindset:** "Can we sell this? Does it help us win deals?"

**Sales Impact:**
- [ ] Does this address a common objection or lost-deal reason?
- [ ] New selling points created?
- [ ] Competitive positioning impact?

**Enablement Needs:**
- [ ] Sales training required?
- [ ] Updated battlecards needed?
- [ ] New demo scenarios?

**Pricing Impact:**
- [ ] Affects pricing or packaging?
- [ ] Upsell/expansion opportunity?

**Concerns:**
- [Concern 1]: [GTM risk]

**Checked against:** [Sections reviewed and evidence used]

**Verdict:** [Green / Yellow / Red / Not assessed: no input for this perspective, needs (what)]
```

### Step 3: Synthesize the Review

```markdown
## Review Synthesis

### Consensus Points (all perspectives agree)
1. [Point of agreement]
2. [Point of agreement]

### Tensions (perspectives disagree)
| Tension | Perspective A Says | Perspective B Says | Resolution Needed |
|---|---|---|---|
| [Topic] | [View] | [Conflicting view] | [Who decides, by when] |

### Blockers (must resolve before proceeding)
| Blocker | Raised By | Severity | Proposed Resolution |
|---|---|---|---|
| [Blocker 1] | [Perspective] | Critical | [Suggested fix] |

### Recommendations (should address but not blocking)
| Recommendation | Raised By | Priority |
|---|---|---|
| [Rec 1] | [Perspective] | High / Medium / Low |

### Open Questions (need more information)
| Question | Owner | Due Date |
|---|---|---|
| [Question] | [Name] | [Date] |

### Coverage
- **Reviewed by:** [Named stakeholders who contributed, or "one model, all perspectives"]
- **Not assessed:** [Perspectives with no real input, and the input each needs before it can be]
- **Correlation note:** [If one model produced every perspective, say so here; consensus between them is not independent agreement]

### Overall Verdict (Standard and Deep)
| Perspective | Verdict | Checked against |
|---|---|---|
| Engineering | [Green/Yellow/Red/Not assessed] | [what was checked] |
| Design | [Green/Yellow/Red/Not assessed] | [what was checked] |
| Executive | [Green/Yellow/Red/Not assessed] | [what was checked] |
| Legal | [Green/Yellow/Red/Not assessed] | [what was checked] |
| Customer | [Green/Yellow/Red/Not assessed] | [what was checked] |
| Devil's Advocate | [Green/Yellow/Red/Not assessed] | [what was checked] |
| Sales | [Green/Yellow/Red/Not assessed] | [what was checked] |

**Recommendation:** [Approve / Approve with changes / Revise and re-review / Reject]
```

At Light depth, replace the seven-row overall-verdict table with this three-row table:

```markdown
### Overall Verdict (Light)
| Perspective | Verdict | Checked against |
|---|---|---|
| Engineering | [Green/Yellow/Red/Not assessed] | [what was checked] |
| Customer | [Green/Yellow/Red/Not assessed] | [what was checked] |
| Devil's Advocate | [Green/Yellow/Red/Not assessed] | [what was checked] |

**Recommendation:** [Approve / Approve with changes / Revise and re-review / Reject]
```

## Minimum Evidence Bar

**Required inputs:** A written proposal document (PRD, tech spec, or design mockup) with enough detail to evaluate feasibility, user impact, and business alignment.

**Acceptable evidence:** The proposal itself, supporting user research, analytics data, competitive analysis, engineering estimates, or prior review feedback.

**Insufficient evidence:** If the proposal lacks defined scope or success metrics, stop and recommend running the PRD skill before attempting this skill.

**Hypotheses vs. findings:**
- **Findings:** Blockers, consensus points, and effort estimate deltas (must be grounded in the reviewed document or cited data)
- **Hypotheses:** Worst-case scenarios, assumption challenges, and adoption projections (must be labeled as Devil's Advocate or speculative)

## Output Format

Produce a Design Review Report with:
1. **Review Setup**, document under review, scope, constraints
2. **Perspective Reviews**, with Engineering, Customer Voice, and Devil's Advocate at Light depth; all seven perspectives at Standard and Deep depth
3. **Synthesis**, consensus, tensions, blockers, recommendations, open questions
4. **Overall Verdict**, go/no-go recommendation

**Shipwright Signature (required closing):**
5. **Decision Frame**, approve/revise/reject recommendation, trade-off, confidence with evidence quality, owner, decision date, revisit trigger
6. **Unknowns & Evidence Gaps**, unresolved tensions, missing stakeholder input, every `Not assessed` perspective with the input it needs, untested assumptions surfaced by Devil's Advocate
7. **Pass/Fail Readiness**, PASS for the review report if findings cite checks, tensions have owners or explicit ownership gaps, and the recommendation reflects blockers. Report proposal approval separately: any unresolved Critical blocker prevents approval. Not assessed perspectives remain evidence gaps; Light covers the three core perspectives only.
8. **Recommended Next Artifact**, Which Shipwright skill to run next and why

## Common Mistakes to Avoid

- **Skipping the Devil's Advocate**, This is the most valuable perspective; don't cut it for time
- **Green verdicts that cite nothing**, An all-Green review is a legitimate outcome when each perspective shows what it checked and against what evidence. A Green with no cited checks is a perspective that was skipped, not one that passed. Do not manufacture Yellows to look rigorous
- **No resolution owners for tensions**, Identified tensions without owners become permanent ambiguity
- **Review too late**, Run design reviews before significant engineering investment, not after
- **Simulating a perspective with no input**, If there is no legal team, no compliance documentation and no regulatory context, mark Legal `Not assessed` and name the input needed. Invented compliance findings are worse than an honest gap, because they get acted on
- **Presenting seven headings as seven opinions**, One model writing all perspectives produces correlated views; state this in Coverage so consensus is not mistaken for independent stakeholder agreement

## Weak vs. Strong Output

**Weak:**
> "Engineering says the timeline is aggressive."

No specifics on which parts are under-scoped, no revised estimate, no path to resolution.

**Strong:**
> "Engineering rates the timeline Yellow: the auth integration is scoped at 2 days but requires OAuth 2.0 PKCE flow plus token refresh handling, estimated at 5 days by the backend lead. Proposed resolution: split auth into a separate sprint or adopt API-key-only auth for V1. Owner: Tech Lead, decision by 2026-04-01."

Identifies the specific gap, quantifies the delta, proposes alternatives, and assigns ownership.
