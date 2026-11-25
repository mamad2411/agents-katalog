---
name: provenance-and-escalation
description: "Keeps agent output traceable to its sources and escalates to a human only on legitimate triggers, with a self-contained handoff. Use when output needs citations, sources disagree, deciding what to automate versus review, confidence is being used for routing, or an agent escalates too often or too rarely. Not for output schemas (use output-contracts); not for enforcing an approval gate in code (use deterministic-enforcement)."
when_to_use: "citations lost in synthesis, sources disagree, agent escalates too much, when to hand off to a human, handoff payload, automate or review extractions, confidence threshold"
license: MIT
---

# Provenance and escalation

Two failures sit at opposite ends of one axis. An agent that cannot say where a claim came from
cannot be trusted. An agent that escalates whenever a user sounds upset is useless. Both are design
failures, not model failures.

The governing rule: when a human or a downstream consumer is the legitimate decider, the agent
annotates the conflict or gap and passes it on, and leaves the resolution to them.

## 1. Attach provenance at retrieval, to every finding

Each finding carries:

- the claim
- the source URL or identifier
- the document name
- the relevant excerpt
- the publication or collection date
- who retrieved it

Attach these when the finding is retrieved. Provenance you plan to reattach later is already lost.

Synthesis is where most provenance is lost, because paraphrasing drops the claim-to-source links.
Tell the synthesis agent to preserve and merge those links, and to end with inline citations or a
reference section. If the synthesis output still has no citations, the defect is upstream: the
sources never reached the synthesis agent (see agentic-loop-control for passing partial results as
structured data).

## 2. Annotate conflicts with full attribution; leave the choice to the consumer

When sources disagree, keep both values with their context and let the consumer decide. Picking
the newer value, the more official source, or an average each destroys information and hides the
disagreement from the one party entitled to judge it.

Keep the dates and qualifiers. Audited versus preliminary, fiscal versus calendar, and restated
versus original usually explain the gap, so what looks like a contradiction is often a trend.

An analysis agent that finds a conflict finishes its work with the conflict included and annotated.
The worst available outcome is silently dropping one value: the output looks clean and is wrong.

## 3. Make coverage gaps visible

Any synthesis built from partial inputs gets a coverage section, for example: "Geothermal is
limited: the two primary journals were unreachable during collection." A reader can act on a stated
gap. A silent gap turns a thin evidence base into a confident claim. This only works if upstream
failures are reported as structured partial results rather than suppressed.

## 4. Measure before automating: segment, calibrate, sample

- **Segment accuracy.** A high aggregate hides segments that fail badly: 97% overall can be 99% on
  digital PDFs and 60% on photographed receipts. Break accuracy down by document type, source,
  locale and field, and automate only the segments that pass on their own.
- **Calibrate confidence.** Raw model self-assessment is poorly calibrated; a 0.9 does not mean
  90%. Calibrate against labelled data before routing on confidence.
- **Sample the confident path too.** Stratified sampling that includes high-confidence items is
  the only way to catch new error patterns in the path with no human in it.
- **Review the most uncertain item first.** Order the review queue by uncertainty and recompute
  the order as items are reviewed. Arrival order spends reviewer time on records that were already
  right.

Worked examples of each step are in
[references/automation-validation.md](references/automation-validation.md).

## 5. Escalate on exactly three triggers

1. **The person explicitly asks for a human.** Escalate immediately, without investigating first.
2. **A policy gap.** The policy is silent on this situation. A policy violation is different: the
   policy has a documented no, and that is an answer to give, not a gap.
3. **Inability to progress** after a genuine attempt to resolve the issue.

Keep sentiment and self-reported confidence out of the trigger list:

- Frustration is not complexity. A frustrated person with a problem you can solve gets
  acknowledgement and a solution, and is escalated only if they then ask for a person.
- Confidence is poorly calibrated, so a confidence trigger escalates by phrasing, not by
  difficulty.

When a lookup matches several records, ask for a disambiguating identifier such as email, phone
or order number. Picking by "most recent" or "most active" risks acting on the wrong account and
exposing one person's data to another.

<example>
User: "This is the third time I've called and I'm furious." (The issue is a replacement you can
process.)
Decision: resolve. Acknowledge, reference the earlier tickets, and process the replacement now.
Sentiment is not a trigger.
</example>

<example>
User: "I'm relocating mid-contract to a country you don't ship to. What happens to my
subscription?"
Decision: escalate, reason `policy_gap`. The handbook covers cancellation and address changes but
not cross-border relocation mid-term, and silence is not a no.
</example>

<example>
User: "Can I get a refund 9 months after purchase?"
Decision: answer without escalating. The policy documents a 90-day limit, which is a documented no.
</example>

<example>
Lookup: two accounts match the email address.
Decision: ask for the order number or phone, and take no action until one account is identified.
</example>

## 6. Make every handoff self-contained

The human who picks up an escalation does not see the transcript. "Escalating, see above" is not a
handoff. Every handoff follows this shape:

```json
{
  "customer_id": "string",
  "issue_summary": "string: what happened, with dates and amounts",
  "root_cause": "string or null: what the investigation established",
  "already_attempted": ["string: each step taken and its result"],
  "amount_at_stake": "string or null",
  "recommended_action": "string: the decision the reviewer is asked to make",
  "escalation_reason": "human_requested | policy_gap | cannot_progress | amount_over_auto_approval_limit"
}
```

`escalation_reason` is a closed enum. The first three values are the triggers from section 5. The
fourth covers a request routed by a code gate from deterministic-enforcement. Because the reason is
machine-readable, you can audit how often each trigger fires.

<example>
```json
{
  "customer_id": "C-4421",
  "issue_summary": "Charged 3x for order #8891; two duplicate charges of 247.83 GBP.",
  "root_cause": "Payment retry loop fired on a processor 504; idempotency key absent (confirmed in logs).",
  "already_attempted": ["Verified identity via get_customer", "Confirmed 3 charges in lookup_order",
                        "Refund blocked by the 500 GBP auto-approval gate"],
  "amount_at_stake": "495.66 GBP",
  "recommended_action": "Approve the 495.66 GBP refund and file a processor-retry bug.",
  "escalation_reason": "amount_over_auto_approval_limit"
}
```
</example>

## Failure modes

- **Citations demanded from an agent that was never given sources.** It can only satisfy the
  instruction by inventing plausible citations, which survive casual review.
- **Conflicts resolved by a heuristic.** Averaging an audited fiscal-year figure with a preliminary
  calendar-year figure produces a number that appears in no source and describes no real period.
- **An empty section marked as success.** Readers take it to mean "nothing notable" when it means
  "we could not look".
- **Escalation wired to sentiment or confidence scores.** The queue fills with problems the agent
  could have solved, and resolution gets slower for everyone.

Notes on applying this outside Claude-based agents are in
[references/porting.md](references/porting.md).

## Verify

1. Pick three claims from a recent output. Each one should trace to a source, a document and an
   excerpt without re-running anything.
2. Spot-check five citation URLs and confirm that each resolves and supports its claim.
3. Grep the escalation code. Every trigger should map to one of the three in section 5, and no
   branch should read a sentiment or confidence score.
4. Check a recent handoff against the section 6 shape. Every field should be filled, or null where
   null is allowed.

If there is no code or output to inspect, say so and return the checklist for the user to run.
Without a checkout: work from the outputs, prompts and code excerpts the user pastes.

These are engineering practices distilled from production agent deployments, not API
requirements. Present them to a team as house rules with a rationale.
