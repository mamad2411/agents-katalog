---
name: chaos
description: "Claim-led multi-agent deliberation for high-stakes judgments that direct verification cannot settle. Use only when the user explicitly requests CHAOS, council/debate, structured disagreement, adversarial or claim audit, minority report, stress-test, or evidence-standard synthesis. Never launch unasked; propose it only when a decision is simultaneously hard to reverse, costly if wrong, and not directly verifiable. Work directly for document/diff review, lookup, calculation, routine edits, brainstorming, or anything one agent can verify."
---

# CHAOS

Use CHAOS to make a judgment that verification cannot settle survive
independent search and adversarial criticism. The parent remains judge and
final writer; advisers run as native subagents or fresh agent sessions.

## Gate

CHAOS is off by default, and loading this skill is not a decision to run it.
Launch adviser runs only when the user asked for a deliberation mode by name.
Unasked, even the strongest case — a judgment hard to reverse, costly if wrong,
and beyond direct verification, all three — warrants at most a one-sentence
proposal to the user, never a launch. Perceived importance is not enough: high
stakes alone do not justify deliberation. Reading, reviewing, or assessing a
document, diff, or answer is direct single-agent work, whatever its stakes,
unless the user asked for independent review. When in doubt, work directly;
when direct work exposes a genuinely contested claim, propose escalation —
cheap to offer, and the user decides. The gate also applies inside a run: any
claim a cheap direct check can settle is settled by the check; deliberation
handles only what verification cannot reach.

## Modes after the gate

Choose a deliberation mode only after the gate admits CHAOS.

| Mode | Use when |
|---|---|
| Skip/direct | Reading or assessing a document, diff, or answer; simple lookup; deterministic calculation; routine work; raw divergent ideation; or tightly coupled work better solved by direct verification. |
| Claim audit | An existing answer, plan, proposal, document, claim set, or diff needs claim-led stress testing or focused refutation before decision. |
| Council | Broad ambiguous decision or high-stakes research/design needs independent same-question first positions. |
| Review loop | An implementation or artifact needs parent-controlled writing plus fresh independent review. |

For full recipes, escalation, and stop rules, read
[references/protocols.md](references/protocols.md).

## Core workflow

1. **Frame.** Fill the task frame from
   [references/artifact-schemas.md](references/artifact-schemas.md): question,
   scope, evidence standard, success criterion, mode, stop rule, perspectives,
   model/provider trust boundary, and artifact destination. State the question
   neutrally — advisers never see the user's leaning or the parent's preferred
   answer.
2. **Separate.** Apply the expansion rule in `references/protocols.md`: explicit
   exhaustive CHAOS uses all suitable approved routes; every other activation
   starts with the smallest sufficient independent set and expands only for a
   missing decision-relevant axis. Discover the host's live execution and model
   capabilities (looking up specific models' strengths, style, and reported
   weaknesses when helpful for duty assignment), then launch each route as a
   native subagent when that backend satisfies the isolation contract, otherwise
   as a fresh agent session. Start first positions in parallel when possible; if
   the host can only serialize isolated sessions, keep prior outputs hidden and
   record `serial-isolated`. Collect every first position before any adviser
   sees peer answers. Every Council first-position adviser answers the same
   whole frame and names the strongest alternative it rejected; topic-sharded
   research is scouting only.
3. **Externalize.** Convert positions into claims, assumptions, evidence,
   confidence basis, uncertainty, and risks.
4. **Cross-examine.** The parent mediates: anonymize memos by diversity axis,
   forward only evidence-bearing critiques in `claim → evidence → consequence →
   requested change` form, drop rhetoric.
5. **Revise.** Defend, narrow, correct, merge, concede, withdraw, or preserve
   dissent. A reversal must cite the specific evidence, falsified premise, or
   corrected inference that changed the conclusion; an ungrounded reversal is
   conformity, not correction, and the parent discounts it.
6. **Synthesize.** The parent normalizes claims and writes the final answer
   against the frame. Agreement counts are never truth; unanimous first
   positions trigger a shared-blind-spot check, not a conclusion.
7. **Record.** Match record depth to the problem: for a single contested issue,
   keep the conclusion, supporting basis, surviving dissent, and its impact on
   the decision; use a full claim ledger and decision receipt for multi-claim,
   multi-round, or auditable runs. Save substantial outputs in the runtime's
   artifact directory or an OS temporary directory by default; write them into
   the project only when the user asks for durable artifacts. Verify files
   exist. For a failed perspective, inspect execution and authoritative output
   first; retry once only under the failure rules in
   `references/orchestration.md`, otherwise record the degraded perspective.
   Code claims require locatable evidence: `file:line`, diff hunk, test output,
   command output, or stable permalink.

## Output contract

Return: decision or answer; surviving claims with support;
changed/narrowed/rejected/merged/withdrawn claims; live objections or minority
report; uncertainty and validation still needed; failed/degraded perspectives;
and why the synthesis follows from the frame. If the evidence standard is unmet,
return `unresolved after exhaustive available review`, `needs direct test`,
`needs external expertise`, or `insufficient evidence`. Use
[references/artifact-schemas.md](references/artifact-schemas.md) for durable
artifact shapes.

## References and final check

Use references by need:
[references/orchestration.md](references/orchestration.md) before multi-agent
launch, artifact handling, failure handling, or review-loop coordination;
[references/adviser-prompts.md](references/adviser-prompts.md) when writing
agent prompts;
[references/evaluation-rubric.md](references/evaluation-rubric.md) before final
synthesis; [references/philosophy.md](references/philosophy.md) only when
modifying the skill or resolving protocol-design ambiguity.

Before finishing, confirm: neutral frame; every Council first position answered
the whole frame (no scouting shards); record depth matches the issue; critiques
anonymized, evidence-bearing, and keyed to claim IDs; reversals grounded in
specific evidence or corrected reasoning; synthesis based on evidence rather
than majority count; dissent and validation gaps preserved.
