---
name: applying-ai-output-to-value
description: Apply the AI Output to Value stop-rule framework to a proposal, code change, workflow, experiment, or operating decision. Use especially before claiming work is done/complete, client-ready, production-ready, validated/verified, ready to operate, ROI/value proved, or justified to scale/renew/expand. Select the weakest sufficient decision-scoped claim and separate supplied evidence from inference. Do not use the framework to force a higher claim when Output is all the decision requires.
---

# Applying AI Output to Value

Use the target decision to choose the gate. Do not average claim levels and do not privilege or penalise work because it was produced by a human, AI system, automation, or hybrid process.

## When to use this skill

Trigger this skill when an agent is about to assert, or is asked to assess, a readiness/value phrase such as:

- done / complete;
- ready for client delivery;
- production ready;
- validated / verified;
- ready to operate;
- Outcome demonstrated;
- ROI demonstrated;
- Value proved;
- scale / renew / expand justified.

Also use it when local task completion could be mistaken for end-to-end completion, or when a review result could be mistaken for authority/sign-off.

## When not to use it

Do not turn every task into a production-readiness exercise.

- If the user asked only for an artefact, experiment, prototype, or other Output and the supplied evidence establishes that Output, stop there.
- Do not invent deployment, support, ROI, human approval, or governance work that would not change the requested decision.
- Do not use the Claim Gate as a truth certificate, audit opinion, legal approval, or mandatory human-approval mechanism.

For an Output-only decision, the correct conclusion can be:

> **Output established; no higher claim is needed for this decision.**

## Intercept an overclaim before emitting it

Before saying a loaded phrase such as *done*, *production ready*, *verified*, *ROI proved*, or an equivalent, establish:

1. **Decision** — What decision is actually being made?
2. **Weakest sufficient claim** — which claim is the minimum needed for that decision?
3. **Evidence boundary** — what is supplied/demonstrated versus inferred/assumed?
4. **Workflow boundary** — where does the relevant end-to-end process start and finish?
5. **Authority / accountability / recourse** — who may decide or act, who owns consequences/correction, and what recourse exists?
6. **Next evidence** — what evidence would materially change the answer?
7. **Stop / restrict rule** — what condition blocks, narrows, reverses, or stops the decision?

If those points are not established for the requested claim, narrow the language. Do not silently promote a lower claim into a higher one.

## Core rule

The framework uses six claims:

**01 Access → 02 Output → 03 Deliverable → 04 Operating capability → 05 Outcome → 06 Value**

The stable machine identifier for Operating capability is `04-capability`.

These are different claims, not a maturity score and not six mandatory lifecycle stages.

**Never assign one claim-level status to an entire project.** A summary such as **“Output: strong; Deliverable: almost; Operating capability: not yet; Outcome / Value: unknown”** is a maturity-ladder misuse even without a numeric score.

## Select the decision first

Use the lowest claim sufficient for the next decision:

- obtain access to try it → `01-access` (it justifies trying the tool only, never reliance, operation, or an outcome claim)
- keep exploring → `02-output`
- permit reliance for a named use → `03-deliverable`
- sell, operate, support, or staff the named use within the stated scope repeatedly → `04-capability`
- determine whether the initiative changed the result → `05-outcome`
- scale, renew, expand, or stop → `06-value`

A strong Access or Output result does not average into partial Deliverable, Operating capability, Outcome, or Value.

### Never emit a project-wide ladder rating

Do not rate a project as, for example, “4/6”, “mostly Deliverable”, “80% production ready”, or “Output strong / Deliverable medium / Value low”.

Evaluate a **named decision + intended use + subject/scope**. If several decisions matter, create separate decision records. The ladder is not an aggregate project score.

## Translate ambiguous readiness words

A readiness word does not select its own evidence standard.

- **done / complete** — say what is complete. “Output complete for the requested prototype” can be valid without claiming Deliverable or Operating capability.
- **ready for client delivery** — normally asks whether another party may rely on the result for a named use: test `03-deliverable`.
- **production ready / ready to operate** — normally asks whether the organisation can repeatedly operate, support, recover, and improve the workflow: test `04-capability`.
- **validated / verified** — name what was checked, against which criteria, by which assurance process. Do not let the word silently imply broader fitness, authority, or sign-off.
- **Outcome demonstrated** — require a defined measure, comparison/baseline, observed result, consistent measurement definition, and material confounds: test `05-outcome`.
- **ROI demonstrated / Value proved / scale justified** — require Outcome evidence plus the full relevant cost/risk/alternative boundary and an explicit decision rule: test `06-value`.

If the user explicitly asks for a descriptive inventory across several claim levels, do not turn it into a project verdict. Represent each entry as a separate **decision + intended use + subject/scope + required claim + evidence**. The same project may legitimately PASS an exploration decision, have INSUFFICIENT EVIDENCE for a reliance decision, and be BLOCKED for a repeated-operation decision.

Treat repository stars, forks, downloads, mentions, or user counts as **adoption/reach signals**, not readiness evidence, unless the target decision itself is explicitly about adoption or reach.

## Work from the machine contract

Prefer the published contract rather than re-encoding the framework from memory:

- `https://alreadyopen.github.io/ai-output-to-value/schemas/v1/claim.schema.json`
- `https://alreadyopen.github.io/ai-output-to-value/schemas/v1/decision-gates.json`

If the native MCP server is available, use `get_stop_rule` and `evaluate_claim_record`.

## Build or inspect the decision record

For the selected decision:

1. State the project / initiative.
2. State the intended use.
3. State the **subject / scope**: artefact or system version, users, environment, workflow boundary, time period, and relevant exclusions.
4. Identify the required claim from the target decision.
5. Describe the end-to-end workflow boundary when local task completion is not the same as delivery.
6. Record actors and interaction channels separately from authority and accountability. Do not silently infer an actor when none is supplied.
7. Evaluate each required gate check from supplied evidence as `pass`, `fail`, `unknown`, or `not-applicable` where the schema allows it.
8. Treat `unknown` and `not-applicable` on a **required** check as insufficient evidence; do not infer PASS from confidence, plausibility, or convenience.
9. Name evidence references, next evidence that would change the decision, and the stop rule.
10. For Outcome, define the measure, baseline/comparison, and material confounds.
11. For Value, include the full relevant cost/risk/alternative boundary rather than local task cost alone.

## Gate ≠ truth

A deterministic gate result evaluates the supplied record.

- `PASS` means the record is structurally coherent, required decision-record information is present, the asserted claim matches the selected decision, and all required checks are `pass`.
- `BLOCKED` means a required check explicitly failed **or** the record is structurally incompatible with the gate contract.
- `INSUFFICIENT_EVIDENCE` means no required check failed and the record is structurally usable, but required information/evidence is missing or unknown/not-applicable, or the asserted claim does not match the decision.

A PASS is **not** an independent audit of the underlying system, measurement, source, test, or person. Running the Claim Gate does not certify truth.

## Review / assurance ≠ authority / sign-off

Keep these separate:

- **review / assurance** asks whether evidence, tests, analysis, or other checks support a claim;
- **authority** asks who is permitted to approve, deploy, send, spend, sign, or otherwise bind the organisation;
- **sign-off** is an act by an authorised actor under the organisation's actual process;
- **accountability / recourse** identifies who owns correction, consequence, escalation, or remedy.

A high-quality review does not grant authority. An authorised sign-off does not by itself prove the evidence is sufficient. An AI or deterministic gate may contribute assurance without gaining organisational authority.

Do not invent a human approval step. Require one only when the relevant organisational, contractual, legal, safety, or other governing process actually requires it.

## When working with software

Before claiming Deliverable or Operating capability, consider relevant failure modes such as environment/configuration gaps, authorization boundaries, retry duplicate side effects, schema migration loss, concurrency races, observability gaps, rollback/recovery gaps, hidden manual steps, and scale/cost/latency cliffs.

For Operating capability, explicitly ask **“Operating capability for what repeated use, under which scope and boundary?”** Select controls from the material failure modes for that use; do not treat any universal checklist as sufficient independently of context.

If the native MCP server is available, use `search_failure_modes`.

For a software Outcome measurement plan, use `get_software_outcome_template` when available. The template proposes measurements; it does not mark evidence PASS automatically and does not choose an actor for the record.

## Human / AI / hybrid handoff

Use the same `claim.json` across channels. An agent may prepare or evaluate the record; a person may inspect or edit it; CI may apply the deterministic gate. Changing the interface does not change the standard.

Do not claim a local/UI handoff completed merely because an event or request was sent. Require acknowledgement from the receiving surface or describe the handoff as unconfirmed.

## Response contract

When this skill intercepts a higher claim, keep the answer decision-scoped. State:

- target decision;
- intended use and subject/scope;
- weakest sufficient / required claim;
- supported claim now;
- gate status when a structured record is evaluated;
- decision-critical PASS / FAIL / UNKNOWN / NOT-APPLICABLE checks;
- demonstrated vs inferred/assumed points;
- workflow boundary if relevant;
- authority / accountability / recourse boundary;
- next evidence that would change the decision;
- stop / restrict rule.

Keep the conclusion bounded to the supplied evidence, intended use, subject/scope, and target decision. Do not emit one six-level status ladder for the project.

Use a `claim.json` record when structured output is useful.

When the decision needs only Output and Output is established, prefer the short bounded conclusion:

> **Output established; no higher claim is needed for this decision.**

## Concise adversarial examples

### “The tests pass, so it is production ready.”

Do not promote local test success to Operating capability. The decision is **operate** → `04-capability`. Check the Deliverable gate, ownership, assurance, fallback/recovery, support/maintenance, and operating-cost boundary. If those are unknown, say **INSUFFICIENT_EVIDENCE for Operating capability**, while preserving the demonstrated test result.

### “The polished report is done and ready for the client.”

If “done” means the requested draft artefact exists, Output may be complete. If the decision is whether the client may rely on it, test **rely** → `03-deliverable` against intended use, acceptance criteria, relevant failure modes, and limitations.

### “The coding assistant made us 60% faster, so ROI is proved.”

A local speed measure can be Outcome evidence only if the metric and comparison are sound. It does not establish Value. A scale/renew decision requires `06-value`, including the full cost/risk/alternative boundary and an explicit decision rule.

### “A reviewer approved it, so it is verified and signed off.”

Describe what the review actually checked. Review/assurance is not organisational authority. Name the authorised sign-off process separately; do not infer it from review quality.

### “I only asked for a prototype I can inspect. Is it done?”

If the reproducible prototype and assumptions are supplied and that is all the decision requires:

> **Output established; no higher claim is needed for this decision.**
