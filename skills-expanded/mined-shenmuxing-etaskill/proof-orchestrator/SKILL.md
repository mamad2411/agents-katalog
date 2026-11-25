---
name: proof-orchestrator
description: "Coordinate proof runs across three interfaces: exhaust actionable local proof work first, package exact unresolved obligations for a provider-neutral external solver only when justified, and keep the user informed and in control of consequential choices."
---

# Proof Orchestrator

## Role

Run proof work across three interfaces:

1. **Internal:** Codex owns the local search, falsification, correctness audit,
   notation audit, exposition, and run record. Complete every concrete local next
   action that remains justified and feasible.
2. **External:** When the internal search is operationally exhausted, package
   the verified setting, attempted routes, strongest partial results, and
   smallest unresolved blocker for an external solver. No provider is the
   default.
3. **User:** Keep the user informed at meaningful decision points and preserve
   their authority over theorem changes, source disclosure, provider choice,
   uploads, browser operation, and paid calls.

External help follows the Internal Exhaustion Gate below, unless the user
explicitly requests earlier consultation. In either case, first prepare an
audit-ready local account of what is known and what remains unresolved.

For GPT Pro, Claude/Fable, or any other external solver, use an available authorized adapter or give the user a manual handoff. If the user selects GPT Pro and asks Codex to perform the call, load `call-gpt-pro`.

## Run Directory And Canonical Record

Keep each run under:

```text
mindflows/<YYMMDDHH-num>/
```

Use only the files needed by the run:

```text
task.md              # precise theorem or proof obligation
materials.md         # definitions, givens, notation, and source excerpts
local-proof.md       # Codex's proof attempt or isolated blocker
approach-registry.md # optional route portfolio for difficult proof searches
sources/             # stable local source snapshots
source-manifest.md   # source role, disclosure status, and external filename
external-brief.md    # provider-neutral problem and evidence package
provider-prompt.md   # optional provider/interface-specific rendering
handoff.md           # chosen route, authority, transfer order, and status
external-output.md   # returned answer, kept as raw evidence
audit.md             # correctness and source-alignment audit
final.md             # verified, simplified, user-facing proof
codex-ledger.md      # run state and provenance, optional
next.md              # next narrow obligation, optional
```

Use only the files the run needs. `external-brief.md` is the canonical,
provider-neutral handoff. Create `provider-prompt.md` only when a selected
provider or interface requires a distinct rendering.

Do not create provider-specific prompts, `handoff.md`, or remote project state
before the local attempt unless the user explicitly requests an external
handoff. Preparing a local `external-brief.md` after the Internal Exhaustion
Gate passes does not itself authorize external contact.

## Continuing a Project

Treat an existing run, `next*.md`, `redo*.md`, or continuation artifact as a project continuation. First read any prior next/redo/continuation files that exist. Treat completed run artifacts and prior external conversations as append-only evidence; do not overwrite them.

Always create a new run directory for new proof work. Record the prior run ID, the exact files read, inherited proved/conjectural/rejected claims, preserved sources, and the single current obligation.

When inheriting an approach registry, preserve family identities and blocker-strength classifications. Keep a blocked route blocked unless the new run records a valid novelty key under `references/portfolio-search.md`.

If a continuation reaches external consultation, prepare a new
`external-brief.md` for the current obligation. Reuse prior sources only after
checking that they still match the frozen target. Prefer a fresh external
conversation unless `handoff.md` explains why prior context is required.

## Status Labels

Use these labels in `codex-ledger.md`, `audit.md`, or `handoff.md`:

- `INTERNAL_ATTEMPT`
- `INTERNAL_PROVED`
- `INTERNAL_EXHAUSTED`
- `INTERNAL_STOPPED_WITH_ACTIONS_REMAINING`
- `ASK_USER`
- `READY_FOR_EXTERNAL_BRIEF`
- `READY_FOR_MANUAL_HANDOFF`
- `READY_FOR_AUTHORIZED_DISPATCH`
- `WAITING_FOR_EXTERNAL_OUTPUT`
- `EXTERNAL_OUTPUT_RECEIVED`
- `NEEDS_EXTERNAL_FOLLOWUP`
- `AUDIT_FAILED`
- `READY_FOR_USER`


## Notation Gate

When the user asks about notation or symbols, when the proof is theorem-heavy, or when one proof step contains at least five nonstandard symbols, read `references/notation-audit.md` and include this exact scorecard in `audit.md` or the user-facing audit:

```text
Core semantic objects retained: <retained>/<declared> (<percent>)
Undefined symbols: <count>
Symbol collisions: <count>
One-use definitions: <count>/<all new symbols> (<percent>)
Maximum parallel representations of one object: <count>
Maximum alias-chain depth: <count>
Maximum active nonstandard symbols in one proof step: <count>
```

Do not rename, merge, omit, or replace these lines with other useful findings. Report logical gaps, domain errors, and irrelevant notation after the fixed scorecard. Core-object retention must be 100%, and undefined symbols and collisions must both be zero before `READY_FOR_USER`.

Never improve the scorecard by inventing a definition, domain, assumption, identity, or relation that the source does not supply. If an undefined symbol or missing implication cannot be resolved from authoritative material, keep it in the audit, mark the proof `AUDIT_FAILED` or `ASK_USER`, and rewrite only the valid fragment or the diagnosis.

## Derivation Structure Gate

For every nontrivial derivation, organize the user-facing proof from the target downward, even if the proof was discovered bottom-up:

1. State the target and its role: "To prove A, it is enough to establish B, C, and D," together with the lemma, identity, or inference that makes those subgoals sufficient.
2. Derive each immediate subgoal and state where it comes from: an assumption, definition, prior lemma, or an explicitly shown calculation.
3. If a subgoal has its own dependencies, expand it in the same target-first form. Order dependent subgoals by their true dependency relation rather than presenting a misleading flat list.
4. Recombine the established subgoals and explicitly return to the original target.

This is an exposition rule, not a license to reverse an implication or hide a gap. Check that the dependency graph is acyclic, every reduction is justified, and no subgoal silently assumes the target. Do not force this scaffold onto a one-step argument where it would add more ceremony than clarity.

Record `Top-down derivation structure: PASS`, `FAIL`, or `NOT_APPLICABLE` in `audit.md`. A nontrivial derivation cannot be `READY_FOR_USER` while this gate is `FAIL`.

## Search Portfolio Gate

For a research-level, open-ended, or repeatedly stalled obligation, read
`references/portfolio-search.md` before committing to one proof route. Create
`approach-registry.md`, compare routes by their mathematical mechanism, classify
the strength of every central blocker, and run task-specific adversarial checks.
For a routine proof with a direct path, skip this gate and do not create the
registry.

An expected answer is a search direction, not a proof premise. Do not assume a
theorem is true merely because the user, benchmark, or prior model output says a
proof exists. Use independent workers only when they are explicitly authorized
and available; the gate must also work as a sequential local search.

## Three-Interface Contract

### Internal Interface

The local run is the canonical source of truth. Follow the Search Portfolio and
Internal Exhaustion Gates where applicable, record both positive and negative
evidence, and perform Codex's own correctness audit. A second model never
substitutes for that audit.

### External Interface

External interaction begins from the provider-neutral `external-brief.md`
specified in the External Handoff Contract. Choose a provider only after the
mathematical role is clear. The provider may
be GPT Pro, Claude/Fable, another model, a human expert, a theorem prover, or a
specialized service. Record the choice and reason in `handoff.md`. Provider-
specific connection instructions belong in the selected adapter or
`provider-prompt.md`; they must not determine the core proof workflow.

### User Interface

Report ambiguity, missing information, a genuine blocker, justified external
help, and the audited external result. Ask before changing the theorem,
disclosing non-approved material, choosing materially different external routes,
operating a browser, uploading files, sending messages, or spending credit. If
user information is the blocker, mark `ASK_USER`. Before external contact,
provide the decision record required in workflow step 6.

## Internal Exhaustion Gate

`INTERNAL_EXHAUSTED` means operationally exhausted under the frozen target,
available local tools and sources, and any explicit user budget. It does not
claim that no proof exists or that all mathematics has been searched.

The gate passes only when all of the following are recorded in `audit.md` or
`codex-ledger.md`:

1. The exact target, assumptions, quantifiers, conventions, and allowed sources
   are frozen; missing user choices or sources have been separated from proof
   difficulty.
2. Codex attempted the actual completion task and audited every claimed result,
   rather than stopping after a difficulty probe or delegating the original
   theorem unchanged.
3. For a routine task, the direct route and its natural repairs were completed,
   rejected, or reduced to an exact blocker. For a research-level, open-ended,
   or repeatedly stalled task, the Search Portfolio Gate was applied.
4. Every approach family is `CANDIDATE`, `BLOCKED`, or `REJECTED`; each blocked
   family has a smallest blocker, blocker-strength classification, and attempted
   falsification. No family remains merely `EXPLORING`.
5. No concrete local next action remains that is both relevant and feasible.
   Unused actionable ideas, unchecked hypotheses, or unrun decisive checks mean
   the gate fails.
6. The strongest locally proved result, the exact residual obligation, and
   `Equivalent-strength blocker: <YES|NO|UNKNOWN>` are recorded.
7. The reason for stopping is epistemic rather than cosmetic: additional local
   work would require a new mechanism, a missing authoritative source, a user
   decision, unavailable capability, or effort beyond an explicit budget.

If work stops because of a user or environment budget while concrete actions
remain, use `INTERNAL_STOPPED_WITH_ACTIONS_REMAINING`, list those actions, and
do not claim exhaustion. External consultation may still be offered if the user
requests it, but the handoff must disclose that local search was truncated.

If the user explicitly requests external consultation before this gate passes,
honor the request within its authorization boundary, but mark the exception in
`handoff.md` and include the untried local actions in `external-brief.md`.

## Workflow

Default route: freeze target -> maintain evidence -> exhaust actionable internal
work -> local correctness audit -> exposition edit -> final. When the Internal
Exhaustion Gate passes: prepare a provider-neutral external brief -> report the
decision record to the user -> use the user-selected manual or authorized route
-> ingest raw output -> return to internal proof and audit -> final.

1. Freeze the target.
   - Decide whether the request is new or a continuation.
   - State the exact theorem, assumptions, quantifiers, and allowed sources.
   - Do not broaden or repair the theorem silently.
2. Maintain local evidence.
   - Read only the files needed to understand the target.
   - Copy stable, directly relevant snapshots into `sources/` when the original may change or cannot be referred to reliably.
   - Keep private run materials in the run directory, never in the skill package.
3. Run the internal proof search.
   - Try to complete the actual proof, disproof, counterexample, or diagnosis; do not stop at a difficulty probe.
   - Check definitions, boundary cases, domains, support, topology, quantifiers, and imported theorem hypotheses.
   - Write `local-proof.md` with the conclusion, proof attempt, dependencies, and any unresolved gap.
   - Apply the Search Portfolio Gate when it applies, and continue while a relevant, feasible concrete next action remains.
4. Audit and classify the internal result.
   - Verify every theorem, lemma, reduction, equality, bound, constant, and quantifier against the stated assumptions and local sources.
   - Distinguish proved, imported, conjectural, repaired, and unsupported statements.
   - For an unresolved run, record `Equivalent-strength blocker: YES`, `NO`, or `UNKNOWN` in `audit.md` or `codex-ledger.md` and justify the classification.
   - If the exact target passes audit, mark `INTERNAL_PROVED` and continue to exposition.
   - If information or a theorem choice is missing, mark `ASK_USER` and present the smallest question that changes the proof state.
   - Otherwise apply the Internal Exhaustion Gate and use its status rules. If it does not pass, return to step 3. Optional external review remains additional evidence, not a substitute for Codex's audit.
5. Edit the proof for exposition.
   - Apply the Notation and Derivation Structure Gates when they apply.
   - Lead with the conclusion, preserve each core semantic object, and retain every non-obvious logical dependency.
   - Prefer a short direct argument to decorative formalism; do not polish an unresolved gap into an apparently complete proof.
6. Prepare the external brief only when justified.
   - Proceed only under the condition and exception rules in the Internal Exhaustion Gate.
   - Complete the External Handoff Contract below and mark `READY_FOR_EXTERNAL_BRIEF`.
   - Before contact, present what is proved locally, what was tried, what remains, why further local work is not actionable, what would be shared, and the available manual or authorized-dispatch routes. If a consequential choice remains open, mark `ASK_USER` while retaining the readiness event.
7. Select and authorize the external route.
   - Record the route and authority in `handoff.md` as required by the External Handoff Contract.
   - For a manual route, provide transfer instructions and mark `READY_FOR_MANUAL_HANDOFF`; after transfer, mark `WAITING_FOR_EXTERNAL_OUTPUT`.
   - For Codex-operated dispatch, require explicit current authority, mark `READY_FOR_AUTHORIZED_DISPATCH`, and load the relevant adapter skill. After sending, mark `WAITING_FOR_EXTERNAL_OUTPUT`.
8. Ingest the returned material as evidence.
   - Save user-pasted or Codex-retrieved text as `external-output.md` or the provider-specific filename recorded in `handoff.md`.
   - Mark `EXTERNAL_OUTPUT_RECEIVED` and apply only the formatting repairs allowed below before mathematical auditing.
   - Record the provider, conversation or task identifier when available, files actually disclosed, prompt actually sent, and whether the response is complete.
9. Re-enter the internal loop.
   - Audit every external claim against the frozen target and authoritative sources; use only valid ideas as new local proof actions.
   - If the target passes, return to step 5; `final.md` may be clearer than the raw answer but must preserve necessary logic and epistemic labels. If a gap remains, first pursue the new local actions it creates; mark `NEEDS_EXTERNAL_FOLLOWUP` only after isolating the residual blocker and recording the applicable exhaustion or early-consultation exception.

## External Handoff Contract

1. Keep authoritative copies under `sources/` with stable generic filenames.
2. Write `source-manifest.md` with, for each source:
   - local relative path;
   - external-visible filename;
   - why it is needed and whether it is authoritative or contextual;
   - whether it must be transferred separately or is faithfully summarized in `materials.md`;
   - disclosure status: `approved`, `not-approved`, `needs-user-approval`, or `not-needed`;
   - readiness status: `ready`, `missing`, `optional`, or `returned-by-user`.
3. Make `external-brief.md` self-contained and provider-neutral. Include, in this order:
   - exact target, assumptions, quantifiers, object conventions, and allowed sources;
   - definitions and source filenames the solver will see;
   - locally verified results and their dependencies;
   - attempted approach families, concrete failures, counterexamples, and blocker strengths;
   - the smallest unresolved blocker and its relation to the original target;
   - any concrete local actions left untried because the user requested early consultation or a budget stopped the run;
   - exact requested output, permitted theorem imports, verification expectations, and a completion marker such as `END_EXTERNAL_OUTPUT`.
4. If a provider or interface needs special formatting, derive `provider-prompt.md` from `external-brief.md`. Do not weaken assumptions, omit failed routes that prevent repetition, or promote conjectures to facts. Keep connection mechanics out of the canonical brief.
5. Make `handoff.md` record the selected solver and rationale, authority granted, approved disclosures, files and prompt actually sent, transfer order, return path, status, and any deviation from the canonical brief.

If a required source or disclosure decision is missing, mark `ASK_USER` or the
handoff blocked rather than silently replacing it with memory. A narrow blocker
is the default request. Ask for the full theorem only when independent search or
whole-proof verification is the explicit external role, and say why that wider
scope is useful.

## External Output Preservation And Repair

Keep `external-output.md` or the recorded provider-specific output file
recognizable as raw external evidence. Formatting repair may fix copy corruption
but must not change claims, constants, assumptions, theorem status, or proof
order.

Required checks:

- Confirm the requested completion marker is present.
- Balance display-math delimiters and inspect suspicious blank lines.
- Repair obvious escaped-brace corruption such as `\left{` to `\left\{` and `\right}` to `\right\}` only when the intended delimiter is unambiguous.
- Remove residual interface or copy separators only when their intended role is clear; otherwise flag them in `audit.md`.
- Scan for malformed operators, stray Markdown markers, and broken right delimiters.

Record nontrivial repairs in `audit.md` or `codex-ledger.md`. Perform substantive clarity and notation editing in `final.md`, after the correctness audit, rather than rewriting the raw output.

## Guardrails

- Never invent missing citations, source statements, assumptions, or proof steps to avoid a blocker or make a handoff look complete.
- Never treat invoking this skill as authority for browser control, uploads, remote messages, API spending, provider selection, or another external turn.
- Never disclose a source marked `not-approved` or `needs-user-approval`.
- Do not reuse prior authorization, silently switch providers, or infer a paid/API fallback after another route fails.
- Do not present a comparable, equivalent, or stronger missing lemma as routine progress. Reopen a blocked route only when `references/portfolio-search.md` supplies a valid novelty key.
- Audit before simplifying. Preserve any step whose removal would make a non-obvious inference unverifiable.
- Treat an external answer as raw evidence. Re-enter local search and audit before accepting it, pursue any new local actions before requesting a follow-up, and obtain new authorization before every dispatch.
- If correctness and elegance conflict, preserve correctness and state the remaining exposition issue explicitly.
