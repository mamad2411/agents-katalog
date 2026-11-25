---
name: audience-discovery
description: Use when deciding who to target, which segment or list to send to, or whether an audience should be split into separate segments. Determines whether the answer is one audience or several, ranks them by expected value, defines who must be excluded, and confirms each segment actually exists and is large enough to be worth sending to. Answers "who should we target?", "which list?" and "should we segment this?". Other skills delegate targeting here, so segment definitions stay in one place.
license: MIT
metadata:
  targetbay.display_name: Audience Discovery
  targetbay.version: "2.1.0"
  targetbay.category: audience
  targetbay.requires: email_sms.customer_intelligence, email_sms.order_intelligence, email_sms.product_intelligence, email_sms.segmentation, email_sms.suppression_and_consent, email_sms.campaign_analytics
  targetbay.risk_level: recommendation
  targetbay.execution_mode: recommend_only
  targetbay.status: foundation
---

# Audience Discovery

## Purpose

Answer "who should we target?" with a ranked, sized, exclusion-aware set of audiences — and say when the
correct answer is one audience, or none.

This is the most frequently composed skill in the package. Campaign, automation, holiday and planning
skills all delegate targeting here rather than reinventing it.

## When to Use

- A campaign, promotion or product push needs a target audience
- A skill needs candidate audiences ranked before planning
- The question is whether an audience should be split
- An existing segment's suitability for a specific send needs checking
- Someone needs to know who to exclude

## When Not to Use

- The audience is already agreed and only the message is in question. Use
  [campaign-optimization](../campaign-optimization/SKILL.md).
- The question is journey topology rather than targeting. Use
  [automation-architect](../automation-architect/SKILL.md).
- The store wants a full customer-base analysis rather than targeting for a specific action — that is
  analysis, not audience discovery.

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| The objective the audience serves | Targeting without an objective is arbitrary | Blocked |
| Lifecycle distribution | The strongest single targeting dimension | Blocked |
| Purchase history and intervals | Recency, frequency, affinity | Partial |
| Value distribution: AOV, LTV | Value-band audiences and offer depth | Partial |
| Product and category affinity | Product-relevant targeting | Product audiences unavailable |
| Engagement recency per channel | Cadence tolerance and channel selection | Partial |
| Consent and suppression state | Hard eligibility constraint | Blocked for SMS; email degraded |
| Existing segments and sizes | Reuse before creating; A1 | Blocked |
| Recent sends to candidate audiences | Prevents fatigue and collision | Partial; warn |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `email_sms.customer_intelligence` | Lifecycle, RFM, value, engagement, propensity signals |
| `email_sms.order_intelligence` | Purchase history, intervals, discount behaviour |
| `email_sms.product_intelligence` | Affinity, category and price-band relationships |
| `email_sms.segmentation` | Resolving and sizing audiences; reusing existing segments |
| `email_sms.suppression_and_consent` | Channel eligibility and suppression |
| `email_sms.campaign_analytics` | Which audiences have responded before |

## Decision Process

```
1. Restate the objective in targeting terms
      ↓  who plausibly acts on this, and why
2. Generate candidate dimensions
      ↓  lifecycle, RFM, affinity, value, engagement, propensity, channel, price sensitivity
3. Resolve and size each candidate                ← A1; reuse existing segments first
      ↓
4. Drop candidates that fail on size or relevance
      ↓
5. Test each surviving split                      ← A3: does treatment actually differ?
      ↓
6. Define exclusions                              ← A4
      ↓
7. Check consent per channel                      ← A10
      ↓
8. Check recent contact and collisions            ← F2, F8
      ↓
9. Rank by expected value                         ← A11
      ↓
10. Return ranked audiences with evidence
```

## Decision Rules

Binding: [../../rules/audience-rules.md](../../rules/audience-rules.md),
[../../rules/frequency-rules.md](../../rules/frequency-rules.md),
[../../rules/global-rules.md](../../rules/global-rules.md).

- Never return an audience that has not been resolved and sized (A1, G4).
- Reuse an existing segment when one fits. Creating a near-duplicate segment is segment sprawl.
- A split is returned only if the two groups would be treated differently (A3).
- Every returned audience carries its exclusions (A4). Exclusion candidates: recent purchasers of the
  promoted product, contacts in a competing journey, contacts contacted within the fatigue window,
  suppressed contacts, non-consented contacts on the chosen channel.
- Prefer behaviour over attributes (A5), and state the lookback window (A6).
- Stop adding conditions when the next one costs more reach than it adds relevance (A7).
- Resolve overlap between returned audiences explicitly (A8).
- Rank, always — an unordered list defers the decision back to the user (A11).
- Below the size where a send is worth building, recommend a different instrument (A12).
- Never target on unverified inference (A9).
- A machine-proposed cluster is a hypothesis, not an audience. It passes the same tests as any other
  candidate before it is materialised — it exists and is sized (A1, A2), it changes the treatment
  (A3, G8), and it can be described in a sentence a person understands. Check it for sensitive and
  inferred-sensitive attributes reconstructed from proxies
  ([../../rules/personalization-rules.md#P7](../../rules/personalization-rules.md)) before, not after,
  it becomes a segment.

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read customer, order, product, segment, consent data | `read_only` |
| ANALYZE | Generate, resolve, size and test candidates | `analysis` |
| PLAN | Rank, define exclusions, resolve overlap | `recommendation` |
| PREVIEW | Present ranked audiences with sizes and evidence | `recommendation` |
| VALIDATE | Run the checks below | — |

This skill does not mutate. Creating the segments it recommends is done by the calling skill, as a
`mutation` requiring preview and confirmation.

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) whose recommendations conform to
[../../schemas/recommendation.schema.json](../../schemas/recommendation.schema.json). Per audience:

- Definition in business terms, and the existing segment it maps to if any
- Size, and the lookback window used
- Exclusions, each with a reason
- Channel eligibility with consented counts
- Rank and what drives it
- Evidence: prior response, value concentration, affinity strength — with period and sample size
- Risks: fatigue, overlap, small sample, stale definition

Also: audiences considered and rejected, with reasons.

## Validation

- [ ] Every audience resolved and sized (A1)
- [ ] Every split changes the treatment (A3)
- [ ] Exclusions stated per audience (A4)
- [ ] Lookback windows stated (A6)
- [ ] Consent checked per channel (A10)
- [ ] Overlap between returned audiences resolved (A8)
- [ ] Recent contact checked against the send window (F2)
- [ ] Audiences ranked with stated criteria (A11)
- [ ] Existing segments reused where they fit
- [ ] No audience below usable size returned without a note (A12)
- [ ] No inferred sensitive attributes used (A9, P7)

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read customer and segment data | `read_only` | None |
| Return ranked audiences | `recommendation` | None |
| Create a recommended segment | `mutation` | Handled by the calling skill; preview then confirm |

## Examples

**"Who should we target for the new premium line?"**
Generates candidates across affinity, value band, lifecycle and engagement. Returns three ranked
audiences: prior premium-category buyers, high-AOV repeat buyers with adjacent affinity, and engaged
VIPs. Excludes anyone who bought the line in the pre-launch window. Rejects a "high income" audience
because the attribute is inferred, not verified (A9).

**"Who for the Tuesday clearance email?"**
Finds one audience is correct: engaged buyers with affinity to the clearing categories, excluding recent
full-price purchasers of the same items. Explicitly rejects splitting by value band because the offer is
identical for everyone (A3).

**"Should we split our win-back list?"**
Sizes at-risk and dormant separately. At-risk is large enough and warrants a lighter touch; dormant needs
a stronger reason to return. Returns two audiences, ranked, with different cadence expectations.

## Failure Handling

| Situation | Response |
|---|---|
| `email_sms.segmentation` unavailable | **Blocked.** Audiences cannot be confirmed to exist (G4) |
| Customer intelligence unavailable | **Blocked.** Targeting would be guesswork |
| An audience resolves to zero | Report it as zero. Never substitute a broader audience silently |
| All candidates below usable size | Recommend a different instrument (A12) and say why |
| Consent data unavailable | **Partial.** Return email audiences only; never assume SMS consent |
| No prior campaign history | Rank on structural evidence, lower confidence, say so |
| Objective too vague to target | Ask once with candidate interpretations |
| Heavy overlap between all candidates | Return the union with priority order rather than pretending they are distinct |

Degraded outcomes set `status` and populate `unmet_requirements`. Never return an unverified audience.
