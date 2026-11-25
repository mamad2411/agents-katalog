---
name: idea-to-done
description: Carry clarified work across planning entry, delivery, review, readiness, publication, merge-aware closeout, optional release routing, and durable completion without replacing the specialist workflows.
---

> References to plugin documentation files (e.g. `docs/workflow-artifact-templates.md`) refer to the plugin-level `docs/` directory (`../../docs/` relative to this file). Other `docs/` paths (such as artifact output destinations) refer to the target project.

## Purpose

Use this skill as the opt-in top-level conductor when a developer wants one
workflow to carry clarified work across planning, delivery, review, readiness,
publication, and post-publish merge-aware closeout.

This skill is a thin coordinator: it owns sequencing, progression mode, durable
workflow-state updates, post-publish closeout decisions, and stop boundaries. It
does **not** replace ideation, planning, delivery, review, readiness,
publication, release, or knowledge workflows.

Persistent team, squad, or fleet-style long-lived orchestration is out of scope
for this skill; use a separate orchestration layer if persistent coordination is
needed.

## When to Use It

Activate when the developer asks for things like:

- "carry this clarified request through the whole loop"
- "take this from idea to done"
- "run the whole workflow with explicit stop points"
- "sequence planning, delivery, review, and publish for me"
- "resume this lifecycle from the last trusted workflow state"
- "continue from review comments / failed readiness / publish waiting on me"
- "continue closeout after the PR was published or merged"

Use this skill only when the work is already clarified enough to choose an entry
path safely. If the request is still exploratory and no bounded direction
exists, start with `/flow:brainstorm` or stop for clarification.

Do **not** use this skill when:

- the developer only wants one specialist phase;
- the request is release-shaped rather than PR/publication-shaped;
- the workflow should resume a stale or ambiguous prior lifecycle without
  re-establishing trusted durable state first.

## Project-Specific Inputs

Before you start, identify:

- the clarified work request, accepted task list, or plan reference;
- whether this invocation is a fresh lifecycle start or a continuation request;
- the active branch and intended review target;
- the repository's validation commands and quality gates;
- the latest factual brief, shared context facts, or discovery artifact;
- whether planning already produced a durable artifact worth trusting;
- whether shared workflow defaults exist at `.flow/defaults.json`
  (see `docs/workflow-defaults-contract.md`);
- whether durable workflow state exists at `.flow/state.json`
  (see `docs/workflow-state-contract.md`), and the trusted durable artifacts it
  references;
- whether the recorded workflow owner, workspace branch/target, and current
  tree still match the lifecycle being resumed;
- whether any downstream publish, merge, release-approval, or deployment step
  must stop for human confirmation under `automation.stop-for-human` or local
  policy;
- whether trusted readiness, publish, merge, and release evidence still
  describes the exact tree or lifecycle now being continued or closed out;
- whether the repository should be treated as release-aware or
  non-release-aware for this lifecycle;
- whether a durable knowledge sink is available if optional
  `knowledge-save` capture is recommended.

When shared workflow defaults are present, consume only the keys relevant to the
conductor:

- `automation.progression` for the baseline progression mode;
- `automation.stop-for-human` for hard human-stop boundaries;
- `review.mode` for the default downstream diff-review mode suggestion;
- publish and artifact-sink preferences only when the downstream specialist
  workflow already supports them.

If any required input is missing, stop and get it first. Do not guess.

## Workflow

### 1. Build the conductor brief and verify the upstream contracts

Before sequencing work, confirm the run still sits on the expected foundation:
the `1.6.0` shared defaults and durable workflow-state contracts, and the
`1.7.0` direct-execution handoff/report contract that `deliver` produces. Then
create or reuse one factual brief covering the task summary, ready entry
artifacts, validation commands, scope boundaries, known dependencies, and the
current branch or comparison baseline.

#### Continuation entry contract

Continuation stays inside this conductor. Do **not** create a separate
mega-skill for resume behavior. The conductor remains coordinator-shaped and
routes only to the existing specialist workflows after it re-establishes trust.

Accepted continuation inputs are:

1. an explicit developer request to continue or resume the lifecycle;
2. `.flow/state.json` from the same repository; and
3. at least one trusted durable artifact referenced by that state, such as a
   planning artifact, direct-execution report, review report, readiness report,
   publish summary, merged PR or merge-policy evidence, release summary, prior
   completion summary, or prior conductor summary.

Reject unsafe continuation when any of the following is true:

- the durable state file is missing and no equivalent trusted artifact bundle is
  available;
- the state file is malformed or uses an unsupported schema version;
- a referenced durable artifact is missing;
- the recorded workspace does not match the current branch/target;
- the recorded owner does not match the lifecycle being resumed;
- the latest readiness or publish evidence does not describe the exact tree now
  under continuation;
- trusted merge evidence is stale, missing, or no longer matches the published
  lifecycle being resumed;
- trusted release evidence is stale, missing, or no longer matches the merged
  lifecycle being closed out;
- the next-ready outcome cannot be determined from trusted evidence.

If the direct-execution handoff or durable-state contract is absent, stale,
ambiguous, or contradicted by newer local work, rescue before continuation:
narrow the scope to the trusted surfaces, regenerate the needed factual brief
or artifact reference, and if trust still cannot be re-established, stop and
surface the exact gap.

### 2. Resolve progression mode

The conductor supports exactly three progression modes:

| Mode | Meaning | Default behavior |
| --- | --- | --- |
| `manual` | phase-by-phase control | stop before every major next phase and wait for explicit developer confirmation |
| `guided` | bounded automation with explicit stop points | continue through safe phase boundaries, but stop at documented human gates |
| `auto` | highest automation allowed by current guardrails | continue through all safe boundaries until a documented hard stop or completion |

Resolve the active mode using this precedence order:

1. explicit developer input for the current invocation;
2. active workflow-state continuity for the same owned lifecycle, when safe;
3. `.flow/defaults.json`;
4. local fallback to `manual`.

Record the resolved mode in the durable state and in the conductor summary.

### 3. Resolve fresh entry vs. continuation

Fresh entry and continuation use the same conductor but start from different
trust boundaries. **Fresh entry** — no trusted conductor-owned lifecycle state
exists yet, so the conductor chooses the best specialist entry path from the
clarified request and available planning artifacts. **Continuation** — trusted
lifecycle state already exists, so the conductor must first identify the
next-ready outcome from durable evidence, using the matrix below, before
routing anywhere else.

#### Next-ready decision matrix

Use the latest trusted lifecycle evidence to pick exactly one primary outcome:

| Trusted evidence | Primary outcome | Route |
| --- | --- | --- |
| No trusted state, no accepted plan, or scope ambiguity remains | clarification | stop for clarification or route to `brainstorm` |
| No trusted task breakdown or planning artifact exists yet | planning | `/flow:plan` |
| State is `planned`, `entry-confirmed`, `planning-skipped`, or `delivery-blocked` with actionable implementation work remaining | delivery | `/flow:deliver` |
| Delivery artifact exists for a non-empty diff and no trusted diff review has accepted it yet | diff review | `/flow:diff-review` |
| Review report shows unresolved findings or `current-phase=review-needs-resolution` | review resolution | `/flow:pr-resolve` |
| Review accepted the diff but no trusted readiness verdict exists yet | readiness | `/flow:pr-ready` |
| Readiness is `ready` or `ready-with-follow-ups`, publish is allowed, and the exact tree still matches the readiness artifact | publication | `/flow:pr-publish` |
| Publication is complete, the PR is still open, and merge has not happened yet | merge monitoring | stop with the `merge-monitoring` boundary and exact monitoring action |
| Publication is complete, but merge is blocked by policy or waiting on explicit human action | merge waiting on human action | stop with the `merge-waiting-human` boundary |
| Merge is confirmed in a release-aware repository and trusted release handoff context says release-closeout is next | release-closeout | `/flow:release` |
| Merge is confirmed, release is still required, but approval, deployment, or policy gates block it | release blocked | stop with the `release-blocked` boundary |
| Merge is confirmed, and the repository explicitly allows release-skipped closeout | release skipped | stop with the `release-skipped` boundary |
| Merge is confirmed, release is not required or already complete, and a reusable lesson is worth preserving | knowledge capture | `/flow:knowledge-save` |
| Merge or release is complete, and stale, duplicate, or conflicting knowledge is the next-ready specialist concern | knowledge refresh recommendation | `/flow:knowledge-refresh` when the mode and trust boundary allow it; otherwise recommend it explicitly |
| Trusted merge, release, and knowledge evidence shows no further specialist work remains | completion summary | write a durable completion summary |
| A completion summary already exists for the current lifecycle | lifecycle completion | stop with the final lifecycle outcome recorded |

When multiple rows appear plausible, choose the earliest incomplete specialist
phase that still has trusted evidence. Do not skip forward past a missing or
stale gate.

### 4. Choose the entry path or resumed specialist

The conductor owns lifecycle sequencing, but a fresh entry still routes into
exactly one specialist workflow: `/flow:brainstorm`
when the request is still exploratory or trade-off shaped; `/flow:plan`
when there is no accepted plan, durable planning artifact, or trusted task
breakdown yet; otherwise `/flow:deliver` once the
work is clarified, planned enough, and execution-ready.

Manual entry into any specialist workflow remains valid. The conductor is an
opt-in convenience layer, not a replacement for those entry points.

### 5. Own lifecycle state and update it at major phase boundaries

While the conductor is the active lifecycle owner, it writes
`.flow/state.json` at meaningful phase boundaries only. It
must not rewrite the state on every minor action, and downstream specialist
workflows must not silently overwrite conductor-owned state.

#### State update matrix

| Boundary | Status | Current phase | Minimum artifact references | Next-action rule |
| --- | --- | --- | --- | --- |
| Conductor accepts ownership | `planned` or `active` | `entry-confirmed` | planning artifact if already known, else none | choose ideation, planning, or delivery entry |
| Continuation trust assessment begins | `active` | `resume-assessment` | state file plus latest trusted artifact for the current phase | resolve one next-ready outcome from trusted evidence |
| Continuation is stale or unsupported | `stale` | `resume-stale` | state file plus artifact or mismatch evidence that triggered the stop | stop unsafe progression and request human confirmation or regeneration |
| Ideation or planning selected | `active` | `planning-entry` | ideation note or planning reference when produced | complete planning or stop for clarification |
| Planning intentionally skipped | `active` | `planning-skipped` | trusted accepted task or prior plan reference | enter delivery |
| Delivery delegated | `active` | `delivery-in-progress` | planning artifact or accepted task reference | wait for delivery result and handoff |
| Delivery completes with non-empty diff | `active` | `delivery-complete` | direct-execution report, track report, or equivalent delivery artifact | enter diff review |
| Delivery completes with no-change or blocked result | `blocked` or `complete` | `delivery-no-change` or `delivery-blocked` | delivery artifact with explicit reason | stop or request narrower follow-up |
| Diff review accepts the delivered surface | `active` | `review-complete` | delivery artifact plus review report | enter readiness gate |
| Diff review requires fixes | `active` or `blocked` | `review-needs-resolution` | review report | route to `/flow:pr-resolve` |
| Readiness passes | `active` | `readiness-passed` | readiness report | publish if policy allows, else stop for human |
| Readiness fails or remains partial | `blocked` | `readiness-blocked` | readiness report | stop with required remediation |
| Publication completes | `active` | `published` | publish summary or PR reference | enter `closeout-assessing` instead of inferring merge or release from publish alone |
| Publication is deferred by policy | `blocked` | `publish-waiting-human` | readiness artifact | wait for explicit human action |
| Closeout trust assessment begins | `active` | `closeout-assessing` | latest trusted publish summary, merge evidence, or prior conductor summary | verify merge, release, and knowledge obligations before routing |
| Merge is still pending and safe to monitor | `active` | `merge-monitoring` | publish summary plus open PR reference | monitor merge and re-run closeout when new merge evidence exists |
| Merge is pending but blocked by human or policy gate | `blocked` | `merge-waiting-human` | publish summary plus merge-policy note | wait for the exact human action required before closeout continues |
| Merge is confirmed | `active` | `merge-complete` | merged PR reference or equivalent merge evidence | determine whether release-closeout is required next |
| Release-closeout is next-ready | `active` | `release-entry` | merge evidence plus release handoff context, versioning note, or changelog pointer | invoke `/flow:release` or stop if the mode or policy requires human confirmation first |
| Release-closeout is blocked or intentionally skipped | `blocked` or `complete` | `release-blocked` or `release-skipped` | release handoff artifact or explicit policy note | surface the exact follow-up or continue to knowledge or summary only when the skip is trusted |
| Knowledge capture is next-ready | `active` | `closeout-knowledge-capture` | merge or release evidence plus latest publish or release summary | invoke `/flow:knowledge-save` or stop if the current mode requires confirmation |
| Knowledge refresh is next-ready | `active` or `complete` | `closeout-knowledge-refresh` | knowledge artifact or closeout note plus refresh trigger | invoke or recommend `/flow:knowledge-refresh` without replacing the current lifecycle owner |
| Completion summary is finalizing | `active` | `closeout-summarizing` | latest merge, release, and knowledge artifacts | write the durable completion summary |
| Lifecycle closes | `complete` | `closeout-complete` or `closeout-partial` | completion summary plus latest specialist artifact | stop with the final lifecycle outcome recorded |
| Closeout trust fails after publication or merge | `stale` or `blocked` | `closeout-stale` | stale-state reason plus last trusted references | stop unsafe progression and require human confirmation or state regeneration |

#### Optional refresh routing

After knowledge capture completes, or when the conductor observes stale,
duplicate, or conflicting knowledge during closeout, it may recommend or route
into `/flow:knowledge-refresh` as the next-ready
specialist step. Refresh remains optional: it never replaces the current
lifecycle owner and never prevents the conductor from recording
`closeout-partial` when the developer intentionally defers it.

When recommending refresh: note the triggering signal (e.g., duplicate prior
learnings, stale knowledge found during review, or a significant completion
event); suggest `manual` or `guided` mode unless the developer already expressed
a progression preference; route directly into `knowledge-refresh` only when the
active mode is `guided` or `auto` and no human-stop boundary applies, otherwise
recommend it explicitly; and never transfer lifecycle ownership to
refresh — the conductor closes the current lifecycle, and refresh starts a new
one if invoked.

Every write must include the required workflow-state fields from
`docs/workflow-state-contract.md`: schema-version, workflow, updated-at, status,
current-phase, automation-mode, next-action, and durable artifact references.

### 6. Sequence the specialist workflows without absorbing their jobs

Use the following lifecycle path when the work remains healthy:

```text
brainstorm (only if needed)
  -> plan (only if needed)
  -> deliver
  -> diff-review
  -> pr-resolve (only if needed)
  -> pr-ready
  -> pr-publish
  -> merge monitoring / merge waiting-human (conductor-owned closeout)
  -> release (only for a release-aware repository after merge)
  -> knowledge-save (optional)
  -> knowledge-refresh (optional, advisory or routed when next-ready)
  -> completion summary (conductor-owned)
```

Coordinator rules:

1. After `deliver`, auto-enter
   `/flow:diff-review` only when the delivered
   result produced a non-empty diff and the active mode allows safe progression.
2. After diff review, route to
   `/flow:pr-resolve` only when findings or
   unresolved review items actually exist.
3. Do not invoke `/flow:pr-publish` until
   `/flow:pr-ready` returns `ready` or
   `ready-with-follow-ups` for the exact tree being published.
4. After `pr-publish`, do not infer merge or release from publish
   alone; re-enter closeout through `closeout-assessing` and pick exactly one
   next-ready closeout outcome from trusted evidence.
5. Route to `/flow:release` only after merge is
   confirmed in a release-aware repository; skip straight to knowledge or
   completion steps in a non-release-aware repository. Release approval,
   deployment, or policy gates remain hard stop-for-human boundaries.
6. Treat `/flow:knowledge-save` as conditional and
   advisory, never mandatory.
7. Treat `/flow:knowledge-refresh` as optional. Recommend it
   when stale, duplicate, or conflicting knowledge is observed, and route into
   it only when the active mode and trust boundary allow it.

### 7. Produce durable completion and conductor summaries

At completion, or at any hard stop that leaves a durable handoff, emit one
durable conductor summary using the `Conductor lifecycle summary` template in
`docs/workflow-artifact-templates.md`. When closeout reaches
`closeout-summarizing`, also emit one durable completion summary using the
`Completion summary` template in the same file.

The shared defaults contract does not yet define dedicated conductor or
completion-summary sinks, so use repository-appropriate durable sinks —
prefer `.flow/artifacts/conductor-summary-<topic>.md` and
`.flow/artifacts/completion-summary-<topic>.md` locally, or an equivalent
structure elsewhere with the same field shape. Point the conductor summary at
the final `.flow/state.json` snapshot and any completion summary rather than
duplicating the state contract inline.

## Required Gates

A conductor run is not complete until:

- the upstream defaults/state and direct-execution contracts were verified or an
  explicit stop reason was recorded;
- one factual brief or trusted context summary exists for the lifecycle;
- the progression mode was resolved and recorded;
- continuation requests resolved to exactly one next-ready outcome before any
  downstream specialist workflow was invoked;
- post-publish or post-merge closeout resolved to exactly one trusted primary
  outcome before any downstream closeout workflow was invoked;
- the conductor updated `.flow/state.json` at every meaningful
  phase boundary it owned;
- every downstream closeout step remained delegated to
  `/flow:release`,
  `/flow:knowledge-save`, or
  `/flow:knowledge-refresh` rather than being reimplemented
  inside the conductor;
- merge, release approval, deployment, and other hard human-stop boundaries
  were respected according to mode and policy;
- a durable completion summary or explicit blocked handoff summary was produced.

### Verification checklist

Before declaring the conductor pass complete, confirm ALL of the following:

- [ ] Upstream contracts verified — PASS / FAIL
- [ ] Progression mode resolved and recorded — PASS / FAIL
- [ ] Closeout decision resolved from trusted post-publish or merge evidence — PASS / FAIL
- [ ] State writes occurred only at owned phase boundaries — PASS / FAIL
- [ ] Merge and release human-stop boundaries respected — PASS / FAIL
- [ ] Manual specialist entry points remain valid — PASS / FAIL
- [ ] Durable completion summary or blocked handoff summary produced — PASS / FAIL

If any item is FAIL: surface the failing item, state the required next action,
and do not declare the lifecycle complete.

## Stop Conditions

- Requirements are still unclear or no safe entry path exists.
- A human decision is required by the current lifecycle boundary or
  `automation.stop-for-human`.
- Merge is still pending and no trusted closeout outcome beyond monitoring is
  safe.
- Readiness has not been achieved for the exact tree that would be published.
- Release or merge policy may demand a separate step outside the conductor's
  safe scope, including release approval or deployment gates.
- Durable workflow state is stale, malformed, unsupported, or owned by another
  workflow in a way that makes auto-progression unsafe.
- Referenced durable artifacts are missing, workspace mismatch is detected, or
  lifecycle-owner mismatch is detected.
- Readiness or publish evidence was invalidated by later tree changes.
- Merge or release evidence was invalidated by later lifecycle changes.
- Downstream rescue fails to re-establish a trusted handoff.
- The developer asks to stop.

Rescue policy: when the lifecycle stalls, narrow the scope, drop to a more
conservative progression mode, or return to the most recent trusted specialist
workflow. Do not silently skip gates or infer success-shaped state.

## Example

### Guided clarified-work entry

```text
Developer: /flow:idea-to-done carry this
feature to a publish-ready result in guided mode

Coordinator:
  Clarified request: yes
  Trusted plan artifact: docs/plan-add-pagination.md
  Active mode: guided
  Shared defaults: automation.progression=guided, stop-for-human=[publish, merge, release]
  Durable state path: .flow/state.json

  -> Skipping ideation and planning: requirements are bounded and an accepted
     plan artifact already exists.
  -> Delegating execution to /flow:deliver, then
     entering /flow:diff-review and
     /flow:pr-ready in turn
  -> Readiness verdict: ready
  -> Stopping before publish because stop-for-human includes publish.

  Durable state updated at: entry-confirmed -> planning-skipped ->
    delivery-complete -> review-complete -> readiness-passed ->
    publish-waiting-human

  Durable conductor summary:
    .flow/artifacts/conductor-summary-pagination.md

  Next action:
    Developer may now invoke /flow:pr-publish
    or re-run the conductor in a mode that still respects the same human-stop
    boundary.
```

### Manual continuation after failed readiness

```text
Developer: /flow:idea-to-done continue this
branch in manual mode after readiness failed

Coordinator:
  Trusted state: status=blocked, current-phase=readiness-blocked
  Trusted artifacts: readiness report with fix-now items
  Next-ready outcome: delivery

  -> Stopping at the delivery handoff because manual mode requires explicit
     developer confirmation before each major next phase
  -> Recommended next specialist: /flow:deliver
```

### Auto closeout after merge: release-aware vs. non-release-aware repository

```text
Coordinator (release-aware repository):
  Trusted state: status=active, current-phase=published, mode=auto
  Trusted artifacts: publish summary + merged PR + release handoff note

  -> Writing merge-complete, then release-entry
  -> Routing to /flow:release unless a release
     approval or deployment gate forces release-blocked first
  -> Auto mode continues through safe boundaries but halts at that
     hard human-stop boundary instead of proceeding silently

Coordinator (non-release-aware repository):
  Trusted state: status=active, current-phase=published, mode=auto
  Trusted artifacts: publish summary + merged PR reference

  -> Writing merge-complete, then skipping release-entry because this
     repository does not require release-closeout for done
  -> Routing to /flow:knowledge-save when a
     reusable lesson is worth preserving
  -> Writing closeout-summarizing and closeout-complete once the completion
     summary is emitted
```
