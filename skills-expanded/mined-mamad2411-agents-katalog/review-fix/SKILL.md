---
name: review-fix
description: >-
  Run configurable review-and-fix rounds on a working change until clean.
  Use for review-fix requests on uncommitted work, a branch, PR, or MR; use the
  Default Review Policy when no brief is supplied, accept an optional target or
  custom review brief, and leave supported fixes uncommitted.
---

# Review fix

Run Review Rounds until clean from a resolved Review Policy:

```text
/review-fix [target] [free-form review brief]
```

Examples:

```text
/review-fix
/review-fix #123
/review-fix over-engineering
/review-fix #123 specification compliance and authorization boundaries
/review-fix ponytail-review and writing-code
```

An explicit brief chooses the Review Policy; no brief uses the Default Review
Policy. This skill owns reviewer orchestration, evidence verification, repairs,
and checks.

## Resolve the request

Treat the leading argument as the target only when it unambiguously resolves as
an existing Git ref, a PR or MR number in the current repository, or a PR or MR
URL. Otherwise use the current branch and working tree as the target and treat
the whole argument as the Review Brief.

Resolve an explicit target into an editable local checkout without disturbing
uncommitted work. A target that cannot be checked out safely makes the outcome
`incomplete`. Determine the target's base from forge metadata, its upstream, or
the repository's default branch, in that order.

When the request contains no brief, use the Default Review Policy below. This
includes a target-only request such as `/review-fix #123`.

## Resolve the review policy

A Review Request runs in a fresh, report-only Reviewer Tree. A Leaf Review Skill
reports through one Reviewer; a Composite Review Skill may delegate the review
work it requires. Every agent in the tree inherits the same report-only boundary.

- Each explicitly named review skill creates one Review Request.
- Explicitly named skills replace the Default Review Policy rather than adding
  to it.
- Read each named skill during preflight. Accept leaf and composite Review Skills
  that can complete the request without writes or external mutations. Reject
  cycles and skills whose required descendants cannot be resolved or kept
  report-only.
- When no skill is named, match the brief against installed Review Skills.
  One unambiguous match uses that skill; no match creates one ad-hoc Reviewer
  from the brief; several plausible matches require native structured input to
  select one. Start no Reviewer and leave the target unchanged until selection.
  Offer a multi-skill panel only when the caller explicitly asks for multiple
  Review Requests.
- Several concerns in one skill-free brief remain one ad-hoc Review Request.
  Never split prose into an implicit panel.
- Text around explicit skill names refines those requests. If it clearly adds a
  separate, unassigned concern, ask whether it belongs to a named Reviewer or a
  separate ad-hoc Reviewer.

Preflight the complete Reviewer Tree before starting any Reviewer. Resolve named
skills and their required review skills to absolute directories so every agent
can read its skill directly even when model invocation is disabled. Reserve
enough agent slots for Composite Review Skills; serialize top-level requests
when concurrent dispatch would starve their descendants. The runtime chooses
models and reasoning effort; this skill carries no model matrix. Record each
resolved Reviewer Tree and its slot reservation for the final report.

### Default Review Policy

Use one Review Request per row when the caller supplies no Review Brief. The
mode narrows write-capable skills to report-only evaluation.

| Review skill | Mode |
| --- | --- |
| `code-review` | Standards and Spec review |
| `brooks-review` | Maintainability review |
| `ask-exemplar` | Embedded Evaluation |
| `zero-tech-debt` | Analysis only |
| `writing-code` | Audit mode |

## Establish the scope contract

Before the first round, derive a compact Scope Contract from the user's brief,
the target's issue or PR, repository terminology, repository instructions, and
relevant durable docs. Record the intended behavior, canonical terms, owned
dependency or module boundary, explicit non-goals, and required verification.

A defect claim must protect a Scope Contract clause or a concrete repository
standard and name a consequence in the reviewed change. Record unsupported
observations as suggestions, not Verified Findings or repair work.

## Run until clean

Keep the resolved Review Policy authoritative across rounds. A Full Review
Round dispatches every Review Request; a Delta Review Round dispatches only the
Impacted Review Requests. The first round is Full. After a repair, a clean Delta
round may finish the run only when the Impacted set is demonstrably complete,
every accepted claim is verified-closed, the Repair Gate passes, and the repair
does not change a public interface, cross-module behavior, dependency boundary,
security boundary, or contract term. Ambiguity requires a later Full round.

Maintain two compact ledgers in orchestration state, never in the target:

- The Run Ledger records each round's scope, HEAD, status, diff hash, Reviewer
  Tree identities and slot reservations, reports, target-mutation result,
  repairs, checks, and CI classification.
- The Claim Ledger keys each claim by location and meaning, and records its
  Scope Contract or repository-standard basis, provenance, evidence, required
  validation, and one finding state: accepted-pending, accepted-repaired,
  rejected with reason, unverified with evidence gap, or verified-closed. Record
  each proposed remedy separately with its provenance and disposition: accepted,
  rejected with reason, or superseded with replacement. Merge repeated claims
  without erasing remedy decisions. Reconsider a rejected or superseded remedy
  only when new evidence answers its recorded reason.

After a repair, derive the Impacted Review Requests from the repair diff. Include
every request that reported an accepted claim and every request whose criteria
cover the changed files, interfaces, sibling paths, or behavior. Ambiguity widens
the set. When that set is the complete Review Policy, the next round is Full.

1. Record the target's HEAD, status, and complete diff. Do not edit while
   Reviewers run.
2. Select a Full or Delta round and record why each request is included. Dispatch
   one fresh top-level Reviewer per included Review Request, concurrently where
   the preflighted nesting budget allows. Give each tree the same target, base,
   diff scope, Scope Contract, Claim Ledger, and repository instructions. Mark
   ledger conclusions as prior evidence, not authority: every fresh Reviewer
   independently inspects the current target and may challenge them. A
   named-skill Reviewer reads and follows that skill and its required references;
   an ad-hoc Reviewer uses the Review Brief as its review criteria.
3. Require every Reviewer Tree to inspect and report only. A Composite Review
   Skill delegates only where required and passes the target context and
   report-only boundary to every descendant. A Reviewer executing a Leaf Review
   Skill or ad-hoc focus does not delegate. No Reviewer may modify files, commit,
   comment on a forge, or push. Each finding includes its location, claim,
   evidence, and proposed remedy; a clean Reviewer says so.
4. Wait for every Reviewer Tree. If any agent fails or times out, or the target
   changed during review, apply no orchestrator edits and return `incomplete`
   with the failed request or changed state.
5. Route an observable claim that source inspection cannot decide to the
   smallest in-scope direct check. When that check is unavailable, retain one
   automation gap instead of redispatching the same claim as new. Claims that
   remain unverified are not findings and never receive fixes.
6. Pass the Synthesis Gate before editing. Merge claims by root cause while
   retaining every Reviewer's provenance; independently verify each hypothesis
   against the exact source, Scope Contract, repository standards, or observable
   behavior; and resolve conflicting remedies. Test each proposed remedy against
   the contract, likely regression paths, and sibling callers. Reject speculative
   hardening and scope expansion, then batch compatible smallest root-cause
   repairs. An unresolved remedy conflict makes the outcome `incomplete`.
7. Apply the synthesized repair batch as tight edits. Do not expand the target's
   scope or edit adjacent code without a Verified Finding.
8. Pass the Verification Gate before recording any outcome by running the Scope
   Contract's required verification and the smallest relevant tests, lint, and
   type checks. Exercise a changed output surface directly when existing tests do
   not observe it. After a repair, this is the Repair Gate: also independently
   confirm each repaired claim is absent and inspect sibling paths sharing its
   root cause. A code or test failure, unmet required verification, or unsafe
   repair makes the outcome `incomplete`.
   Treat remote CI as evidence for the reviewed snapshot only when the target has
   no uncommitted changes and the run's head SHA equals the round's recorded HEAD.
   Otherwise the run is prior context, not Verification Gate evidence. Observe
   matching CI when it already exists; do not wait for, trigger, or rerun it.
   Classify each non-successful remote CI result as a code or test failure,
   infrastructure or account failure, cancelled or superseded run, or unavailable
   evidence by inspecting executed steps and annotations. When no steps ran for
   an infrastructure reason, run the closest safe local equivalents and report
   remote CI as unavailable, never passed. Infrastructure-only CI does not block
   `clean` when those local equivalents satisfy the required verification.
9. Record the round's Review Outcome. A Full round with no Verified Findings is
   `clean`. A repaired round is `fixed` and starts the round selected from the
   Impacted Review Requests: Full when the set is the complete Review Policy,
   Delta otherwise. A Delta round with no Verified Findings is
   `clean` when it meets the narrow-repair closure conditions above; otherwise it
   is `ready-for-full-review` and starts a Full round. `incomplete` ends the run
   without further edits.

Continue only while each `fixed` round changes the target and passes the Repair
Gate. A repeated Verified Finding without new evidence, or any round that cannot
make a supported repair, makes the outcome `incomplete` instead of cycling.

## Return the outcome

Choose one output form:

- For a one-round `clean` run, return only the compact downstream handoff. Include
  the policy source, exact Review Request count, Scope Contract, round scope,
  Reviewer Tree provenance and slot reservation, target and base refs, final HEAD
  and diff hash, checks and CI classifications, and terminal outcome once. Do not
  narrate the workflow separately or include empty categories; omission means the
  category is absent, not rendered as `None`.
- Otherwise, report the policy source, resolved Review Requests, Scope Contract,
  each round's scope and Reviewer Tree provenance, non-empty Claim Ledger states,
  Verified Findings, rejected claims and remedies, unverified claims and evidence
  gaps, superseded remedies, automation gaps, repairs, Verification and Repair
  Gates, checks and CI classifications, and Review Outcome. Use compact tables or
  lists, omit empty categories, and state repeated clean provenance once. End with
  a compact downstream handoff containing the target and base refs, final HEAD and
  diff hash, terminal outcome, non-empty repair and claim summaries, checks and CI
  classifications, automation gaps, and Reviewer Tree provenance.

For each repaired round, explicitly name the Synthesis Gate, Repair Gate, and
`fixed` outcome. Give each repaired claim one ledger row containing its Reviewer
provenance and complete state progression. A preflight `incomplete` report states
that the target, repository history, and forge state remain unchanged. For each
Composite Review Skill, provenance names the top-level Reviewer and every
descendant role, and records that preflight accepted the tree with enough agent
capacity. State the exact Review Request count, identify the fresh top-level
Reviewer dispatched for each included request, and explain each Delta subset while
confirming that the authoritative Review Policy remained unchanged.

Finish with exactly one terminal outcome. The downstream handoff is the sole input
later history or publication skills need from this run.

- `clean`: a Full round on the complete current diff has no Verified Findings, or
  a later clean Delta round meets the narrow-repair closure conditions.
- `incomplete`: the requested policy could not finish safely.

Leave all repairs uncommitted. Do not commit, rebase, comment, or push. The
caller owns the repository's history and publication workflows.
