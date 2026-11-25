---
name: ai-content-governance
description: Use when deciding how much of a store's customer-facing writing a model may produce unattended — which automated message types may ship generated wording with no human sign-off, which must always be approved by a person before they reach a recipient, what that reviewer checks and in what order, whether a model may pick an incentive and from which pre-approved set, and what an unattended send does when the generator is unavailable or returns something unusable. Answers "can we let it write our newsletter?", "do we have to approve every generated email?" and "what stops an unattended send saying something untrue about our products?". Use content-optimization when one specific message underperforms and its wording needs rewriting rather than governing.
license: MIT
metadata:
  targetbay.display_name: AI Content Governance
  targetbay.version: "1.0.0"
  targetbay.category: content
  targetbay.requires: email_sms.template_management, email_sms.campaign_analytics, email_sms.product_intelligence, email_sms.customer_intelligence, email_sms.store_profile
  targetbay.composes: content-optimization
  targetbay.risk_level: plan
  targetbay.execution_mode: plan_then_execute
  targetbay.status: foundation
---

# AI Content Governance

## Purpose

Decide where the human sign-off sits in a pipeline that writes customer-facing copy automatically:
which message classes may ship unreviewed, which never may, what the reviewer checks and in what
order, and what the pipeline does when the generator fails.

Generated copy is fluent, which is what lets an invented price or an unsupportable claim ship
unnoticed. The opposite failure is a gate so heavy that reviewing costs more than writing, at which
point it becomes a rubber stamp. Decide both before anything is wired.

Where the gate sits is a policy decision; how it is wired is
[the recipe library](https://github.com/targetbay360/targetbay-agent-skills/blob/main/targetbay-marketing-automation-recipes/SKILL.md).

## When to Use

- Deciding whether a model may write copy that reaches customers, and for which message types
- Setting the review requirement for an automated pipeline before it is built
- Deciding what a reviewer checks, and in what order, so review is bounded rather than open-ended
- Defining what an automated send does when generation fails or returns something unusable
- Deciding whether a model may choose an offer, and from what
- Review has become a formality and the store wants to know which gates actually earn their cost

## When Not to Use

- One specific message underperforms and the copy needs rewriting. Use
  [content-optimization](../content-optimization/SKILL.md).
- The question is which variant wins. Use [ab-testing](../ab-testing/SKILL.md).
- The question is which offer depth a segment deserves. Use
  [aov-growth](../aov-growth/SKILL.md) or [cross-sell](../cross-sell/SKILL.md); this skill decides only
  whether a model may pick from the resulting set.
- The question is where a pipeline step should run rather than who signs it off. Use
  [automation-orchestration](../automation-orchestration/SKILL.md).

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| Which message types the store sends, and which carry a price, claim or offer | Message class decides the gate | Blocked |
| What product and offer data the generator can be given, and whether it is verified | A generator without verified source data will invent one | Blocked |
| Who can review, and how much time they actually have | A gate nobody can staff is not a gate | Blocked |
| Existing brand and claim constraints | What the reviewer is checking against | Partial; review becomes subjective |
| Current send volume by message type | Whether the proposed review load is survivable | Partial |
| Prior incidents where copy was wrong | Sharpens what the reviewer checks first | Partial |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `email_sms.template_management` | Which templates and blocks exist, and which are approved fixed assets |
| `email_sms.campaign_analytics` | Send volume by message type, which sizes the review load |
| `email_sms.product_intelligence` | The verified product and price data a generator may be given, and its limits |
| `email_sms.customer_intelligence` | The verified contact data personalisation may draw on |
| `email_sms.store_profile` | Store identity, brand constraints and the claim environment it operates in |

## Decision Process

```
1. Enumerate the message types the store sends
2. Classify each by what it asserts
     price or offer · product fact · brand claim · framing only · internal only
3. Set the gate per class                       ← assertion level decides it, not convenience
4. Decide what the generator may be given       ← verified data only; no data means no assertion
5. Decide whether a model may select an offer   ← selection from an approved set, never generation
6. Define the reviewer's ordered checklist      ← so review is bounded and repeatable
7. Define the failure path                      ← generation fails means send nothing
8. Size the review load against available time  ← an unstaffable gate is a rubber stamp
9. Define the rejection path                    ← a reason captured, and a bounded number of retries
```

## Decision Rules

Binding: [../../rules/content-rules.md](../../rules/content-rules.md),
[../../rules/global-rules.md](../../rules/global-rules.md),
[../../rules/safety-rules.md](../../rules/safety-rules.md),
[../../rules/personalization-rules.md](../../rules/personalization-rules.md).

- A message that asserts a price, an offer, a product fact or a brand claim is reviewed before it
  reaches a recipient. There is no volume at which this becomes uneconomic — the incident costs more
  (N3, N7, G3).
- A generator may only assert what it was given as verified data. It may not fill a gap, and a missing
  value means the element is omitted, not invented (G3, G12, P1, P5).
- A model **selects** an offer from a pre-approved set within agreed bounds. It never generates one.
  An unbounded per-person offer is price discrimination, and it is also how a ruinous discount ships
  unattended (C4, C5).
- A generation step that fails sends nothing (N13). This skill decides which classes are generated at
  all; it does not get to soften what happens when generation fails.
- An approval gate that expires into a send is not a gate, and a standing instruction is not per-send
  approval (S13, S3, S9).
- Approval of content is not approval to bypass suppression, consent or the frequency budget. The
  send path runs its own checks regardless (G13).
- The reviewer's checklist is ordered and finite, and the first item is factual accuracy. An
  open-ended "does this look right" is not reviewable and will decay into a glance.
- Personalisation inside generated copy is bound by the same verified-data rule as anywhere else, and
  sensitive or inferred-sensitive attributes are excluded before generation rather than filtered after
  (P7).
- Size the gate against the reviewer's real capacity. Where the load exceeds it, narrow what is
  generated rather than loosening what is reviewed (G7).

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read message types, volumes, available verified data, reviewer capacity, brand constraints | `read_only` |
| ANALYZE | Classify each message type by what it asserts; size the review load | `analysis` |
| PLAN | Gate per class, generator input bounds, reviewer checklist, failure and rejection paths | `plan` |
| PREVIEW | Present the policy with the review load it implies | `recommendation` |
| VALIDATE | Run the checks below | — |
| APPROVE | Human approves the policy | — |
| EXECUTE | Record the policy against the templates and pipelines it binds | `mutation` |
| — | **Sending any generated message** | `high_impact`, explicit approval per send where the class requires it |
| MEASURE | First-pass approval rate and review time together; incidents caught at the gate | — |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) containing: each message type with its
assertion class and its gate; what the generator may and may not be given; whether offer selection is
permitted and from what set; the reviewer's ordered checklist; the failure path; the rejection path
and its bound; the review load the policy implies against stated capacity; and the risks, including
what remains exposed under the chosen gates.

## Validation

- [ ] Every message type classified by what it asserts, not by how it is produced
- [ ] Anything asserting a price, offer, product fact or brand claim gated before send (N3, N7)
- [ ] Generator input limited to verified data, with omission rather than invention as the gap rule (G3, P1)
- [ ] Offer handling specified as selection from an approved set, never generation (C4)
- [ ] Failure path stated as "send nothing", with no fallback to a prior version (N13)
- [ ] No timeout, expiry or standing instruction that results in an approval (S13, S9)
- [ ] Content approval confirmed not to bypass suppression, consent or frequency (G13)
- [ ] Reviewer checklist ordered and finite, with factual accuracy first
- [ ] Sensitive and inferred-sensitive attributes excluded before generation (P7)
- [ ] Review load sized against stated reviewer capacity

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read and classify message types | `read_only` / `analysis` | None |
| Recommend the policy | `plan` / `recommendation` | None |
| Record the policy against templates and pipelines | `mutation` | Preview, then confirm |
| **Send a generated message in a gated class** | `high_impact` | **Explicit, per send** (S9) |
| **Relax a gate on a class that asserts a price, offer or product fact** | `high_impact` | **Explicit**, with the exposure stated |
| **Any pipeline that sends generated copy with no human gate at all** | — | **Refused.** Not planned by this skill (S2) |

## Examples

**"Can we have it write the weekly newsletter for us?"**
Splits the newsletter by what it asserts rather than treating it as one thing. The editorial framing
and section intros are framing only and can ship with a light check; the product blocks carry prices
and stock positions and are gated per send. Recommends narrowing generation to the framing and
keeping product blocks as approved fixed assets, which cuts the review to something the one available
reviewer can actually do weekly. Rejected: gating the whole newsletter, which the store would have
abandoned within a month, and gating none of it, which puts prices in front of customers unchecked.

**"Let it write and send the weekly newsletter on its own from now on."**
Refuses the no-gate version. A standing instruction is not per-send approval, and the newsletter
asserts prices and product facts. Notes that the constraint is partly structural anyway — the
platform surface has no campaign-create operation, so a human is in the loop by construction. Offers
the version that works: generate the draft, gate it, and use the rejection path so the reviewer's
objections improve the next draft rather than being discarded. Rejected: a review timeout that
auto-approves, which the store suggested as a compromise and which is simply the no-gate version with
extra steps.

## Failure Handling

| Situation | Response |
|---|---|
| Message types or their assertion content unknown | **Blocked.** Gates cannot be set without knowing what each message asserts |
| No verified product or offer data available to the generator | **Blocked.** A generator with no source data will invent one; there is no safe gate for that (G3) |
| No reviewer capacity available | **Blocked.** Recommend narrowing what is generated to classes that need no gate, rather than a gate nobody staffs |
| Send volume unavailable | **Partial.** Set gates by class and state that the review load could not be sized |
| Brand and claim constraints undocumented | **Partial.** Reviewer checklist covers factual accuracy and offer correctness only; brand consistency is stated as unreviewable until documented |
| Store wants a gate removed on a price-bearing class | Restate the exposure plainly, record the decision and who made it, and keep the failure path and scoped-approval rules intact |
| Store wants an unreviewed generated send | **Refused.** State why, record the refusal, and offer the narrowed-generation alternative (S2, S8) |

Degraded outcomes set `status` and populate `unmet_requirements`.
