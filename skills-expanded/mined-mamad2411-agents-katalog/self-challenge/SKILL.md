---
name: self-challenge
description: Use when a blocker, failing evidence, review finding, user correction, workaround, unplanned work, semantic-boundary change, or repeated candidate change may prompt a direction-changing edit. Run a short self-challenge before that edit to keep the candidate action traceable to confirmed intent; do not use for routine typos, ordinary within-intent debugging, an authorized fallback, initial exploration without a confirmed baseline, or final artifact review.
license: MIT
metadata:
  author: sevenflankse
  version: 0.1.0
---

# Self-Challenge

Use this candidate to question an imminent direction transition before acting on it. It starts with a short stage-one reflection, not an approval gate, final review, debugging workflow, or a reason to defend the current plan blindly.

## Scope

Run stage one when an observable pivot cue appears: a blocker, failing evidence, review finding, user correction, tempting workaround, unplanned work, semantic-boundary change, or repeated change of candidate action. Complete it before the first direction-changing edit.

Failing evidence that motivates replacing an implementation mechanism or semantic boundary is a stage-one cue; run stage one before continuing quietly within intent.

Do not escalate routine typo correction, ordinary within-intent debugging, a fallback already authorized by confirmed intent, initial exploration without a confirmed baseline, directly verifiable review feedback, or final artifact review. Continue these cases quietly.

## Stage-One Check

Before the edit, identify the following from decision-relevant evidence:

1. The candidate action and the exact confirmed-intent source that supports it or conflicts with it.
2. The commitment it could affect, including scope, acceptance, domain, data, ownership, security, compatibility, or a confirmed non-goal.
3. One observable falsifier that would show the candidate action is wrong.
4. One lower-commitment alternative that can address the immediate problem while changing fewer commitments.

Distinguish an implementation, test, or environment defect from evidence that invalidates a confirmed plan assumption. A defect normally calls for repairing the implementation within intent; an invalidated assumption calls for preserving evidence and returning to the existing decision process.

Apply a rebuttable conservative presumption: confirmed intent is the current best baseline, so a deviation needs evidence. Treat evidence that invalidates the baseline as a reason to revise course rather than a reason to preserve it by default.

Choose among confirmed-intent sources only when recency and clarity form one unique, evidence-backed ordering. Unresolved precedence is missing decision-relevant evidence: block the direction-changing edit and return to the existing decision process.

## Stage-Two Successful Path

After stage one, deepen only when an imminent candidate action may affect confirmed intent or decision-relevant directional uncertainty remains. Repeated candidate changes are supporting evidence for that judgment, not an automatic escalation rule.

Open exactly one fresh challenger that did not participate in forming the candidate. Use runtime-enforced read-only permissions when the runtime supplies capability evidence; otherwise claim only observed-no-write. The challenger may retrieve sources, but must not edit, revise a plan, authorize a scope change, create another challenger, or invoke `self-challenge`.

Use the same challenger handle for two sequential prompts:

1. Round one gives ordered authoritative source IDs and content or retrieval instructions, problem evidence, constraints, and non-goals. Do not disclose the candidate. Require a source-first reconstruction of the baseline, invariants, source conflicts and precedence, alternative hypotheses, and falsification conditions.
2. Round two discloses the candidate only after reconstruction. Require a bilateral steelman of preserving and changing direction, the main agent's likely error risk, the protected or invalidated invariant, evidence source IDs, the condition that would change the conclusion, one evidence-backed verdict, its reason, and one allowed next action.

Apply evidence-first precedence before selecting a verdict. Insufficient decision-relevant evidence or unresolved source precedence requires `MORE_EVIDENCE` and blocks the direction-changing action. With sufficient evidence, use `REPLAN_REQUIRED` when confirmed intent needs revision, `ADAPT_WITHIN_INTENT` when commitments stay stable, or `KEEP_COURSE` when the deviation lacks support. A verdict does not edit or revise the plan, authorize scope, or create a new approval gate.

## Bounded Evidence And Safe Reentry

`MORE_EVIDENCE` is bounded, not an invitation to continue investigating. It must name exactly one `decision_relevant_question`, one `minimal_read_only_investigation`, one `completion_signal`, and one `non_expansion_scope`. Do not make a direction-changing edit while that gap remains. After the stated read-only investigation completes, apply all four verdicts again; if materially changed evidence still returns `MORE_EVIDENCE`, emit a `USER_OWNED` handoff and stop rather than widening the investigation.

Keep confirmed-intent baseline material separate from decision-relevant evidence material. The baseline consists only of confirmed-intent sources, constraints, and non-goals; do not derive it from a mixed bag of sources. For a session, the same normalized baseline, candidate, and evidence tuple gets one stage-two attempt only. Normalization may use NFC, line-ending normalization, trimming, and repeated-whitespace collapse only. Do not case-fold, remove punctuation, reorder material, hash fuzzily, or infer semantic equivalence.

Before any prompt, emit, or awaited operation, synchronously validate the tuple and consume it. A timeout, source failure, malformed output, missing verdict, missing read-only proof, observed write, recursion, or exception does not change the tuple and never permits a retry. A changed candidate or changed evidence can start one later attempt; a candidate-only change does not satisfy an earlier evidence gap. A changed baseline preserves the old baseline and requires a user-owned handoff and a newly confirmed session.

Open at most one challenger per attempt. Every attempt ends in either one verdict or one typed safe failure, never both. A safe failure preserves the baseline and can only lead to `PRESERVE_BASELINE` or a separately validated bounded `MORE_EVIDENCE`; it never authorizes a deviation or treats a tool failure as evidence against confirmed intent.

## Continue Or Disclose

When the candidate remains traceable to confirmed intent and no commitment changes, continue without announcing the check. Clear within-intent adaptation is also quiet.

Use bounded disclosure only when the check changes the next action, reveals missing decision-relevant evidence, or reaches a direction that already requires a user-owned decision. State the affected commitment, the evidence gap or falsifier, and the smallest next action. Do not expose a ceremonial checklist or ask for approval that confirmed intent does not require.
