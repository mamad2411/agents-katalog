---
name: review-strategy
description: Diagnose what actual results and changed conditions mean for the current direction: check whether each bet ran with enough exposure, compare expected with observed, weigh competing explanations, recommend continue, increase, change, hold or close, and name the decisions to change at their owners. Use at a planned decision point, when a threshold is crossed, or when a consequential new observation arrives.
---

# review-strategy

Writes [`strategy-review`](../../../../.group/contracts/strategy-review.md) under the shared [document rules](../../../../.group/contracts/document-rules.md).

## When and what it decides

The question: **what does this result actually tell us, about which choice, and what should change?** A review diagnoses and recommends. The skills that own targets, offers, prices and focus revise their own documents.

## Inputs and authority

- `venture-definition`, `objectives`, `bet-portfolio`, `focus-plan`: what was intended and why.
- Observations: `readout`, `experiment-result`, `financial-report`, customer or market observations, capability changes. Each carries its source. A plan, scenario or earlier proposal is never a result.
- Execution facts: did the action happen, when, to whom, how often.

## Method

Record sources, exact owner quotes and calculation premises in the relevant table’s basis or source cells. Carry decision status in its status column and the document’s role; prose states choices and ambition directly.

1. **Establish exposure first.** For each bet: did the intervention run as designed, to the intended customers, for long enough to be read? If not, the disposition concerns execution, not strategy.
2. **Compare expected and observed.** Use `python3 workers/strategy/venture-strategist/tools/focus.py compare --expected "…" --observed "…"` for quantities; it refuses incompatible units and unknown values. An `unknown` observation yields no conclusion, only a next observation.
3. **Generate competing explanations** across the chain: target, offer, access, buying friction, delivery, execution, mechanism ([objective trade-offs](../../../knowledge/objective-tradeoffs-and-outcome-mechanisms.md) §5). For each material issue, name the observation that discriminates between explanations, and whether it exists.
4. **Locate the cause.** Decide whether the result indicts one choice or a link of the venture's value chain itself ([venture coherence](../../../knowledge/venture-coherence-and-value-mechanisms.md) §5). Only the latter calls for revising the venture-definition.
5. **Choose a disposition** among continue, increase, change, hold, close, considering the remaining opportunity and the cost of the next commitment. Effort already spent is no reason to continue. A pivot is a change to core choices, justified only by a supported diagnosis.
6. **Name required changes** by artifact and owning skill, with ordering and the next observation or decision condition. When evidence is insufficient, name the next observation and a bounded decision point instead of a verdict.

## Evaluate and correct

| Defect | Detect by | Correct by |
| --- | --- | --- |
| Verdict without exposure | Disposition on a bet that barely ran | Change to an execution finding; set the decision point |
| Single explanation | Diagnosis lists one cause | Add the competing explanations and the discriminating observation |
| Plan counted as result | Observed column cites a projection or the bet's own expectation | Replace with an observation or `unknown` |
| Review as authority | The review states new prices, targets or focus itself | Move the change to Required changes for the owning skill |
| Sunk-cost continuation | Reason cites effort spent | Reason from remaining opportunity and next commitment |

Run the group check; observation cells need basis.

## Recovery

- **NeedData:** the needed observation does not exist. Write the disposition `hold`, the observation needed, who produces it (Evidence) and the date of the decision point.
- **Conflict:** two observations disagree. Name both sources and the check that would reconcile them; no disposition depends on either until reconciled.

## Example

Illustrative fixture: fictional venture and observation records.

The paid-use result calls for completing the commercial intervention. It leaves the value and price questions available for a properly exposed test.

```markdown
## Bet dispositions
| Bet | Objective | Expected | Observed | Execution and exposure | Disposition | Reason | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BET-1 | OBJ-2 | Paid use after the offer | No offer responses | Offer prepared but not sent | change | Complete delivery before interpreting buyer response | [observed: readout/2027-01#offer-delivery] |

## Diagnosis
| Observation | Explanations | Discriminating basis | Conclusion |
| --- | --- | --- | --- |
| Paid adoption has not begun | Offer did not reach users; price or value was rejected; payment route prevented purchase | [observed: readout/2027-01#offer-delivery] records that sending has not occurred | The evidence identifies an execution gap; buyer response requires delivery |

## Required changes
| Artifact | Owner | Change | Ordering | Next condition |
| --- | --- | --- | --- | --- |
| focus-plan | set-focus | Prepare ACT-2 for owner execution using an available payment route | After payment-route confirmation | Record actual delivery and responses |
```

The review supplies a correction to the focus owner and a concrete observation for the commercial choice.

## Final readable delivery

After this change's native documents and checks are final, follow the group's Human-readable result delivery: run `python3 {product-root}/.group/tools/result_html.py {state-directory} --open` once for the combined result and return `result.html` with the native files. The product root is this installed strategy group; the state directory is the current documents, with no automatic candidate overlay. Intermediate exports omit `--open`. Keep the complete file and report the exact path if the host cannot open it. This derived view changes no native record, decision, status or delivery contract.

For a final delivery that combines current documents and proposed revisions, pass `--candidate` explicitly to overlay matching files from `STATE_DIRECTORY/candidate/`. The HTML records those exact candidate source paths and statuses; generation grants no acceptance. Without this flag the current source set is exported. Point `STATE_DIRECTORY` directly at a standalone final/candidate document directory when that is the complete delivered result. Never substitute older current documents for the version actually delivered.
