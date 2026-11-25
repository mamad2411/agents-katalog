---
name: deliverability-qa
description: Use when the question is whether the sending programme itself is fit to send — whether the sending domain authenticates and aligns, what the domain and IP reputation posture is, whether a new domain or a long silence means volume has to be ramped rather than resumed, and which mailbox providers are turning against this sender. Answers "are we authenticated?", "is our sender reputation getting worse?" and "can we safely increase volume?". Use list-hygiene when the remedy is which contacts to suppress, and email-quality-auditor when one specific campaign needs clearing before it goes out.
license: MIT
metadata:
  targetbay.display_name: Deliverability QA
  targetbay.version: "1.0.0"
  targetbay.category: optimization
  targetbay.requires: email_sms.sending_infrastructure, email_sms.campaign_analytics, email_sms.suppression_and_consent, email_sms.store_profile, email_sms.event_stream
  targetbay.composes: list-hygiene
  targetbay.risk_level: recommendation
  targetbay.execution_mode: recommend_only
  targetbay.status: foundation
---

# Deliverability QA

## Purpose

Establish whether this store's sending programme is in a condition to send, by diagnosing the three
layers in order — identity, reputation, then content — and decide what has to change before volume
does.

The failure this skill exists to prevent: diagnosing the wrong layer. A store whose authentication
does not align rewrites its subject lines; a store with a reputation problem redesigns its template.
Each remedy is real work aimed at a layer that was not broken, and while it happens the actual cause
compounds. The second failure is quieter: asserting inbox placement from data that cannot show it.

The layer model, and why each layer responds on a different timescale, is
[../../knowledge/deliverability-principles.md](../../knowledge/deliverability-principles.md).

## When to Use

- Establishing whether the sending setup is sound, before or independent of any campaign
- Engagement is falling across every send rather than in one campaign
- A mailbox provider appears to be treating this sender differently from the others
- Volume is about to increase materially, or a new sending domain or IP is being introduced
- Sending is resuming after a long silence
- Someone asks whether the store is "landing in spam" and the evidence has not been examined

## When Not to Use

- The remedy is which contacts to suppress, sunset or leave alone. Use
  [list-hygiene](../list-hygiene/SKILL.md), which this skill composes for that half of the answer.
- One specific campaign needs clearing before it is sent. Use
  [email-quality-auditor](../email-quality-auditor/SKILL.md).
- The question is whether a list may lawfully be mailed at all. Use
  [consent-verification](../consent-verification/SKILL.md).
- One campaign underperformed while the rest of the programme is healthy. Use
  [campaign-optimization](../campaign-optimization/SKILL.md).
- The message arrives but renders badly. Use [email-render-qa](../email-render-qa/SKILL.md).
- Nobody has named the problem yet. Use
  [opportunity-discovery](../opportunity-discovery/SKILL.md), which routes here when the scan points
  at deliverability.

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| Sending domains and their authentication state | The identity layer, which gates everything below it | Partial; identity reported as unverified |
| Whether the verified identity aligns with the visible sender | Alignment is the part that fails while each record looks present | Partial |
| Dedicated or shared IP, and warm-up state | Bounds how much may be sent and to whom | Partial; no ramp can be derived |
| Bounce and complaint rates over time, with their variance | The store's own threshold rather than a borrowed one | Blocked |
| Engagement movement segmented by receiving domain | The closest available proxy for placement | Partial; diagnosis stays programme-wide |
| Send volume and audience composition history | Whether a pattern change caused the signal | Partial |
| Suppression state and consent posture | Whether the population being mailed is legitimate | Blocked |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `email_sms.sending_infrastructure` | Sending domains, authentication records and alignment, IP posture, warm-up state and sending limits. **Flagged UNVERIFIED in the registry** |
| `email_sms.campaign_analytics` | Bounce, complaint and engagement rates, their movement, and their split by receiving domain |
| `email_sms.suppression_and_consent` | The population currently eligible to receive mail |
| `email_sms.store_profile` | Sending history, plan limits and the store's current volume band |
| `email_sms.event_stream` | Individual bounce and complaint events, for concentration analysis at contact level |

## Decision Process

```
1. Identity first        <- do the records exist, and does the verified identity align?
2. Stop here if identity fails         <- nothing below it is diagnosable until it is fixed
3. Reputation next       <- bounce and complaint trajectory against this store's own variance
4. Segment by receiving domain         <- one provider or all of them is a different problem
5. Check for a pattern change          <- volume, frequency, audience composition, a resumed silence
6. Derive the ramp if one is needed    <- from the store's current level, never a fixed schedule
7. Name what could not be observed     <- placement is inferred, and labelled as inference
8. Split the remedy: infrastructure, population, cadence   <- delegate the population half
```

## Decision Rules

Binding: [../../rules/deliverability-rules.md](../../rules/deliverability-rules.md),
[../../rules/global-rules.md](../../rules/global-rules.md),
[../../rules/safety-rules.md](../../rules/safety-rules.md),
[../../rules/frequency-rules.md](../../rules/frequency-rules.md),
[../../knowledge/deliverability-principles.md](../../knowledge/deliverability-principles.md).

- Diagnose in layer order and stop at the first failing layer (D1). A content recommendation issued
  over a broken identity layer is wasted work.
- Authentication records live in the store's DNS, outside the platform. Recommend the change, name
  who must make it, and never report it as executed (D1, S12).
- Thresholds come from this store's own recent variance, never from a published benchmark (D3, G2).
  This package ships no benchmarks.
- Inbox placement is not observable from sending data. Where no placement signal exists, say
  placement is unknown and present engagement, bounce and complaint movement by receiving domain as
  proxies, labelled as proxies (D7, G15).
- Separate receiving domains before drawing a programme-wide conclusion (D6, A8).
- A remedy that does not change who is mailed or how often is not a deliverability remedy (D8).
  Where the diagnosis is reputation, hand the population half to
  [list-hygiene](../list-hygiene/SKILL.md) rather than proposing suppression here.
- A ramp is derived from the store's current sending level and stated as a dependency every plan in
  that window inherits (D9). Never a fixed schedule.
- A pattern change is itself an event (D5). Check volume, frequency and audience composition before
  concluding the programme has degraded.
- Never recommend a send whose expected complaint level risks a block, regardless of its expected
  revenue (D10, G1).
- Consent and suppression are never weakened to improve a number (S7).

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read authentication and IP state, rates and variance, engagement by receiving domain, volume history | `read_only` |
| ANALYZE | Layer diagnosis; locate concentration; test for a pattern change | `analysis` |
| PLAN | Layer verdicts, the ramp if needed, the remedy split across infrastructure, population and cadence | `recommendation` |
| PREVIEW | Present each verdict with its evidence and each unobservable signal by name | `recommendation` |
| VALIDATE | Run the checks below | — |
| APPROVE | Human decides on any pause, ramp or infrastructure change | — |
| — | **Pausing or resuming sending** | `high_impact`, explicit approval |
| MEASURE | Rate and engagement movement against the pre-change baseline, by receiving domain | — |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) containing: a verdict per layer with the
evidence behind it; the failing layer, if any, and what must change before the next one is
diagnosable; concentration by receiving domain; whether a pattern change explains the signal; the
derived ramp and its dependency on the store's current level; the remedy split, with the population
half delegated; and an explicit list of signals that could not be read, placement among them.

## Validation

- [ ] Identity checked first, and the diagnosis stopped there if it failed (D1)
- [ ] Alignment checked, not merely the presence of each record
- [ ] Authentication remedies named with the owner outside the platform (D1, S12)
- [ ] Thresholds derived from this store's own variance, no published benchmark used (D3, G2)
- [ ] Rates segmented by receiving domain before any programme-wide conclusion (D6)
- [ ] Placement stated as unknown where no placement signal exists; proxies labelled as proxies (D7)
- [ ] Pattern change tested before concluding degradation (D5)
- [ ] Any ramp derived from the store's current level, not a fixed schedule (D9)
- [ ] Population remedy delegated to list-hygiene rather than duplicated here (G7)
- [ ] No content recommendation issued as a deliverability remedy (D8)
- [ ] Every unreadable signal named (G15)

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read infrastructure state, rates and engagement | `read_only` / `analysis` | None |
| Report layer verdicts and remedies | `recommendation` | None |
| Change an authentication record | — | Outside the platform; recommended with a named owner, never executed here |
| **Pause or resume sending** | `high_impact` | **Explicit** |
| **Increase volume beyond the derived ramp** | `high_impact` | **Explicit**, with the reputation cost stated (D2, D10) |

## Examples

**"Our open rates have been sliding for two months across everything we send."**
Checks identity first and finds the records present but the visible sender on a subdomain that does
not align with the verified one — which is the whole finding, because nothing below that layer is
diagnosable until it is fixed. Names the DNS change and its owner outside the marketing team.
Reports that engagement decline is consistent with the alignment failure but that placement itself
cannot be observed, so the causal claim is an inference. Rejected: the subject-line testing
programme the store had already scheduled, which addresses the content layer while the identity
layer is failing.

**"We want to send our Black Friday campaign to the whole list — we usually only mail the last
90 days."**
Establishes that the proposed send is several times the store's usual volume to a population whose
engagement is largely unmeasured, which is a pattern change rather than a bigger version of a normal
send. Derives a ramp from the current level and shows what fraction of the list it reaches inside
the campaign window. Delegates the question of which dormant contacts are worth including to
list-hygiene. Recommends the ramped send plus the engaged remainder, and states plainly what the
unramped version risks for every send afterwards. Rejected: the full-list send, and also the
do-nothing option, which forgoes recoverable revenue the ramp can reach.

## Failure Handling

| Situation | Response |
|---|---|
| `email_sms.sending_infrastructure` unavailable | **Partial.** Report the identity layer as unverified rather than assumed sound, diagnose reputation with that caveat carried into every conclusion, and record the capability as a dependency (S12) |
| Bounce and complaint history unavailable | **Blocked.** Reputation cannot be diagnosed from a single point, and a guess here directs the whole remedy |
| Rate history too short to establish variance | **Partial.** Report levels rather than movement, state that no threshold can be derived yet, and recommend the measurement before the intervention |
| Engagement cannot be segmented by receiving domain | **Partial.** Diagnosis stays programme-wide; state that a single-provider cause cannot be ruled out (D6) |
| No placement signal of any kind | Expected, not an error. State that placement is unknown and present the proxies as proxies (D7) |
| Suppression and consent state unavailable | **Blocked.** The legitimacy of the sending population is a precondition for every other conclusion |
| Warm-up state unreadable | **Partial.** Derive the ramp from observed volume history instead, and say the platform's own warm-up state was not read |
| Identity failing and the store wants to send anyway | Present the blast radius and the cost to every later send (D2, D10). The decision is the store's; the risk is recorded as accepted |
| Volume history unavailable | **Partial.** A pattern change cannot be ruled in or out; say so rather than concluding degradation |

Degraded outcomes set `status` and populate `unmet_requirements`.
