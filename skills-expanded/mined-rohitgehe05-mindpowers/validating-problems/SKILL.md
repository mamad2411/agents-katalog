---
name: validating-problems
description: Use when a user wants to test, sharpen, frame, or gather evidence for a customer or business problem before pitching a direction, prioritising work, or writing a PRD.
---

# Validating problems

## Overview

Determine what can defensibly be said about a customer or business problem before a team pitches a direction, prioritises work, or writes a PRD. Produce a scoped, solution-free problem definition whose claims remain traceable to evidence.

Keep problem validation separate from prioritisation and solution validation. Remain useful when evidence is incomplete without lowering the standard for calling a claim supported.

## Explain the conclusion plainly

Think precisely and respond in common words. Keep the detailed assessment in
the claim and evidence ledgers; do not dump that machinery into the
conversation or present it as a scorecard.

For a material user-facing conclusion, give a compact reasoning receipt:

1. lead with the conclusion or recommendation;
2. say what evidence you checked and the main reasons;
3. state the important uncertainty; and
4. give one next step, ending with one concrete question when a response is
   needed.

Use internal status and schema terms only when they help the user act. Explain
an unavoidable technical term on first use. When a rule could be misunderstood,
give one short example. If the user says the explanation is unclear, explain
again from scratch rather than defining the same jargon with more jargon.

## Bound the decision

Establish or infer these boundaries before evaluating the problem:

- `decision_to_inform`: Name the decision this work will support.
- `desired_outcome`: Name the customer or business condition that should improve.
- `scope`: Bound the exact users, workflow, context, and time period covered.
- `out_of_scope`: Exclude prioritisation, solution selection, and any other adjacent decision not being tested.

Do not force the user to restate a boundary already present in the conversation or available evidence. Narrow the claim when the evidence covers less than the proposed scope.

## Inspect before asking

Inspect relevant conversation context, linked workspace files, research, analytics summaries, support material, and previous problem briefs before asking a question. Cite each inspected source or path in the evidence ledger. Never ask the user to transcribe evidence that can be accessed safely.

When no evidence is available, mark the claims unsupported and identify the smallest useful evidence assignment. Do not manufacture a verdict.

When a current problem brief exists, preserve its settled boundaries, evidence, claim statuses, and original `as_of` values. Before relying on a settled claim, check for materially new evidence, changed scope, expired relevance, or contradiction. Reopen only an affected claim and date its new assessment to the relevant new evidence. Do not advance an unaffected claim's `as_of` merely because the freshness check happened later. Otherwise resume only the unresolved or newly disputed claim, and do not restart the whole brief unless the user explicitly reopens it.

## Evaluate four claims

Evaluate these claims independently:

| Claim | Evaluate |
|---|---|
| Existence | Determine whether the problem demonstrably happens. |
| Audience | Determine for whom, where, and when it happens. |
| Materiality | Determine what customer or business consequence it creates. |
| Mechanism / context | Determine what conditions, behaviours, or constraints appear to produce or sustain it. |

Use `mechanism / context`, not `cause`. Keep causal explanations as hypotheses unless the evidence supports them. Do not require causal proof to socialise a well-supported problem.

Assign one status to every claim:

- `supported`: Use only when the scoped claim has relevant evidence strong enough for the current decision.
- `partially-supported`: Use when some parts are supported but important scope, coverage, or mechanism gaps remain.
- `unsupported`: Use when available material does not substantiate the claim.
- `contradicted`: Use when relevant evidence materially conflicts with the claim.

Make every status scope- and time-bound. Record `as_of`. Never generalise beyond the users, workflow, context, or period represented by the evidence.

## Assess evidence

Classify evidence as a starting point, not as a mechanical score:

- **Anchor evidence:** Prefer observed workflow behaviour, product telemetry, transactions, churn or funnel data, support cases, direct interviews about recent past behaviour, workarounds and artefacts, and workflow observation.
- **Corroborating evidence:** Use stakeholder input, prior internal documents and research, sales or operations reports, customer-success patterns, and relevant external benchmarks to reinforce or qualify anchor evidence.
- **Hypothesis-only inputs:** Treat PM or executive judgement, isolated feature requests, AI reasoning, trend narratives, survey intent, and proposed solutions as hypotheses rather than proof.

Assess each evidence item across six dimensions:

- **Directness:** Distinguish observed, reported, and inferred evidence.
- **Relevance:** Check whether it covers the exact workflow or only an adjacent context.
- **Recency:** Record when the evidence was observed or collected.
- **Coverage:** Check representation across relevant users and situations.
- **Reliability and provenance:** Record the source, collection method, and material limitations.
- **Direction:** State whether the item supports, weakens, or is ambiguous about the claim.

Separate raw observation from interpretation. Do not treat direct evidence as automatically decisive. Weigh relevance, recency, coverage, reliability, provenance, and conflicting evidence together.

## Route by product stage

Select evidence appropriate to the product stage without weakening the meaning of `supported`:

- **Pre-product:** Seek direct accounts of recent pain, observed current workflows, workarounds, artefacts, and evidence that users already spend effort coping.
- **Existing product:** Seek behavioural and operational data showing the pattern, paired with research or support evidence explaining its context.
- **Mature or paid product:** Seek quantified customer and business impact, segmented behavioural evidence, churn or revenue consequences, and direct evidence explaining the pattern.

Match coverage to the decision and relevant user variation. Never apply a universal sample size. Seek stable patterns across the user types and contexts inside the scope, and narrow the claim when coverage remains narrow.

## Run the conversation

Make each conversational turn contain:

1. Give the concise plain-language conclusion or current assessment.
2. Internally identify the claim most likely to change the decision and its
   status; name the status label only when it helps the user act.
3. Summarise in common words the evidence that supports, weakens, or limits
   that claim.
4. Ask exactly one highest-value question, adding one concrete example only when helpful.

When the user asks what can be said now or whether to proceed, state the current
workflow decision in common words; name its stable label only when that helps
the user act. Before presenting a current statement as safe to pitch or
socialise, surface at least one plausible alternative framing or one route
that could weaken or disconfirm it. Do not require alternatives in an early
elicitation turn that offers no conclusion.

Choose the question most likely to change the decision, narrow the scope, or distinguish between competing explanations. Do not march through a fixed questionnaire or batch questions.

Keep the evidence status separate from the decision to socialise, gather evidence, or stop. Treat leadership urgency, sales pressure, and engineering readiness as decision context, not as problem evidence.

## Challenge the premise

Test the premise whenever doing so could change the decision:

- Translate a solution disguised as a problem or an isolated feature request into the underlying job, friction, or consequence.
- Identify who does not experience the problem, who has been excluded from the evidence, and who benefits from the current state.
- Examine incentives, policy, process, training, data access, and organisational constraints as possible non-product explanations.
- Examine whether the team's assumptions or process contribute to the symptom.
- State what evidence would make the proposed framing false.

Generate at least two plausible alternative framings or mechanisms before settling on the final problem statement. Include non-product explanations when plausible. Preserve conflicting observations and seek evidence that can distinguish the alternatives rather than averaging the conflict away.

## Stop for real-world evidence

Stop speculative elicitation when the remaining decision-critical gap requires research, observation, or data. Do not simulate missing evidence through more conversation.

Issue one specific evidence assignment containing:

- claim to test;
- evidence needed;
- source or participant profile;
- method;
- observation or measure;
- what would strengthen the claim;
- what would weaken or contradict it; and
- which decision the result will affect.

End the evidence-assignment turn with exactly one decision-relevant next-step question asking whether the user can supply or collect the named evidence. Do not add an arbitrary coordination questionnaire.

After the user confirms the evidence can be supplied or collected, ask in a later one-question turn for the user to provide or explicitly accept any useful threshold before the test. Never invent sample sizes, durations, confidence scores, or success thresholds and present them as standards.

## Decide and write the brief

Choose one workflow decision independently from the claim statuses:

- `ready-to-socialize`: Use when the decision-critical claims are sufficiently supported for the stated scope and all limitations are explicit.
- `gather-evidence`: Use when a named evidence gap could materially change the framing or decision.
- `stop`: Use when the problem is contradicted, immaterial for the stated decision, or no longer the problem that should be investigated.

Allow a partially supported problem to be socialised only as an explicitly labelled hypothesis with unresolved claims visible. Never treat `ready-to-socialize` as prioritised, approved, or ready to build.

Read [references/problem-brief.md](references/problem-brief.md) before writing the result. Write the brief relative to the invoking workspace at `docs/mindpowers/problems/YYYY-MM-DD-<slug>.md` using the exact schema and body contract in that reference.

Before writing customer-sensitive evidence in a shared or public workspace, warn the user and offer a private or ignored location. If no writable workspace exists, present the complete brief in chat and state that it was not saved.

## Hand off

Recommend the next action in plain language and explain why. Name the internal
skill when useful, but wait for explicit user confirmation before switching.
Completing the brief is not permission to invoke another skill.

Carry a completed brief into the confirmed next workflow without changing its
evidence status:

- For a one-pager or other direction-setting conversation, recommend `mindstorming` and require downstream claims to preserve scope, status, limitations, and the `as_of` date.
- For prioritisation, hand the brief to an external prioritisation workflow. Do not prioritise inside this skill.
- For solution selection or solution validation, recommend `mindstorming`. Do not design a pilot, prototype, feature, or solution here.

Keep this skill and `mindstorming` independently usable. Do not require a one-pager or any other downstream artifact to complete problem validation.

## Visual companion (optional)

When the claim discussion has enough moving parts that a table beats prose
(usually once two or more claims have different statuses), offer the visual
companion in its own message, naming the mode per the fallback ladder in
`skills/_shared/companion/COMPANION.md`:

> "Want a live claim ledger alongside our chat? It shows each claim's status
> and as-of date, updating as we go."

If accepted, follow COMPANION.md. Push the `claim-ledger` screen there and
re-push it (versioned filename) whenever a claim's status or as_of changes.
Everything else — questions, evidence discussion, the brief — stays in chat.
Never offer during the first bound-the-decision exchange.

## Hard rules

- Inspect available evidence before asking for information.
- Evaluate existence, audience, materiality, and mechanism / context separately.
- Ask exactly one decision-relevant question per conversational turn.
- Scope every conclusion to the evidence and its recency.
- Prefer direct and behavioural evidence without applying the hierarchy mechanically.
- Separate raw observations from interpretations.
- Surface plausible alternative framings and a route to disconfirm the premise.
- Preserve contradictions and unsupported claims visibly.
- Never invent thresholds, sample sizes, durations, or confidence scores.
- Never move into prioritisation, solution design, pilot design, or PRD hardening.
- Never turn urgency, executive belief, feature requests, or engineering readiness into evidence.
- Never present an unsupported or contradicted claim as fact.
