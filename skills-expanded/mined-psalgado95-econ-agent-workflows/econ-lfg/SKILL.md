---
name: econ-lfg
description: "Complete a bounded economics research task end to end when the user requests autonomous execution."
---

# Econ LFG

Run an autonomous economics workflow without losing the research object, evidence trail, or review discipline.

`econ-lfg` is not a replacement for `econ-plan`, `econ-work`, or `econ-review`. It orchestrates them under a goal-backed contract, then owns the review-resolution loop before final delivery.

Read `references/review_resolution_reference.md` before classifying review findings, deciding whether to fix directly, writing a researcher-level decision memo, or choosing the targeted re-review surface.

## Direct invocation contract

Use this workflow only when the user explicitly asks for hands-off or one-prompt execution of a bounded economics or hybrid research task. Do not auto-route ordinary planning, work, review, or brainstorming requests here.

The required order is:

1. attach to a goal-backed run;
2. invoke `econ-plan`;
3. invoke `econ-work`;
4. invoke `econ-review`;
5. resolve review findings through a revision pass;
6. run targeted re-review when revisions or new evidence require it;
7. deliver only when the result is resolved, consciously deferred, or genuinely blocked.

Do not skip the saved-plan gate. For non-trivial tasks, `econ-plan` must produce or refresh a saved plan before `econ-work` begins.

Route pure software work to the current Compound Engineering workflow instead of forcing it through economics skills.

## Input

Treat the arguments passed with this invocation, or the user's current request, as the autonomous task to run end to end. Inspect any named files and the available project context before asking questions. Use the request, prior decisions, and that evidence to define the bounded task. Ask only for an unresolved choice that materially changes the economics, authority, or feasible deliverable. State reversible assumptions and proceed; do not repeat an intake interview when the user has already supplied the task. If the prompt would require deciding the research question itself, use `econ-brainstorm` or `econ-plan` to build the task first.

Once the bounded task is agreed and the run begins, work autonomously. Return with a question only when newly discovered evidence would materially change the agreed task, a researcher-level decision is required, required access is missing, or new external or destructive authority is needed.

## Goal-backed run

Use the host platform's goal or persistence primitive when available. If the run is already inside a goal, continue under that goal. If no active goal exists and a goal primitive is available, create one whose objective names the requested research output and the required `econ-plan -> econ-work -> econ-review -> revision -> re-review` loop.

If no goal primitive is available, execute the loop in the current foreground session using the available task list or saved progress record. Lack of a goal primitive is not itself a research blocker. State session-local persistence in the execution record and mention it to the user only when it limits completion or resumption. Do not claim a goal was created or promise work after the session ends.

Mark the goal complete only when the final deliverable is produced and review-resolution is handled. Mark the affected branch blocked when a genuine unresolved economics decision or access limit prevents progress. Continue independent authorised work; do not repeat an identical failed action or question without new evidence.

## Authority hierarchy

Keep these decision sources separate:

1. **Researcher-anchored choices**: constraints stated in the initial prompt, such as baseline, estimand, sample boundary, benchmark treatment, target output, note scope, or fixed comparison. Do not override these silently.
2. **Plan-backed choices**: decisions written into the saved `econ-plan`. These govern execution unless review or realised outputs show the plan's own assumptions need revision.
3. **Agent-owned choices**: defaults the agent inferred during planning or work, such as diagnostic order, figure priority, note framing, or an implementation route. These may be revised by best judgment when review evidence supports a better path.
4. **Execution-discovered facts**: realised outputs, missing inputs, failed checks, stale artefacts, or unexpected findings. These can force revision or a pause.

When a review finding conflicts with a researcher-anchored choice, pause and ask. When it challenges an agent-owned choice, revise without asking if the better path remains inside the initial prompt's intent.

## Pipeline

### Stage 0: Intake and routing

- Restate the task compactly.
- Classify whether it belongs in the economics workflow:
  - empirical or hybrid economics research: continue;
  - source collection, data construction, model computation, analysis, writing from defended evidence: continue;
  - pure app, API, UI, infrastructure, general tooling, or non-research refactor/debug task: route away.
- Identify likely researcher-anchored choices from the initial prompt.
- Before beginning the autonomous loop, resolve material ambiguity about the objective, baseline, estimand, sample boundary, benchmark treatment, output surface, note scope, destructive overwrite, or rerun authority. During the loop, stop only under the autonomous boundary above.

### Stage 1: Plan

Invoke `econ-plan` with the autonomous task.

After it returns:
- verify that a saved plan path exists, unless `econ-plan` stopped with a blocking question;
- if a blocking question was asked, pause the goal and return the question to the user;
- if the saved plan classifies the task as pure `software-handoff`, route away and stop the economics loop;
- capture the planned review route and artefacts `econ-work` must leave ready.

Do not perform implementation work until the saved-plan gate is satisfied.

### Stage 2: Work

Invoke `econ-work` on the saved plan with the private `caller_contract: econ-lfg/v1` return contract.

After it returns:
- validate that the response uses `econ-work-for-caller/v1` and contains every required field; retry a malformed or wrong-version child response once, then stop with the child-contract failure rather than guessing;
- verify that work reached a valid closeout or named blocker;
- capture what was inspected, changed, run, and regenerated; code role; outputs refreshed versus inherited or inspected-only; interpretation or note-brief status; review-bundle status; and residual risks;
- if work paused for a user-level decision, pause the goal and return that decision;
- if work completed with a recommended `econ-review` route, continue.

Do not treat a script run, generated output, or partial closeout as enough to proceed.

### Stage 3: Review

Invoke `econ-review` with one complete `econ-review-request/v1` object and the
review route from the plan or work closeout. Set `invocation` to `nested`,
`caller` to `econ-lfg/v1`, and `resolution_context` to `null` for this first
review. Populate every other required request field, including the bounded
scope, evidence manifest, triggers, timeout policy, and supplemental assessment
declarations. Do not pass a persona choice or a private caller/report contract.
Consume the returned `econ-review-report/v3` inline. This nested review creates no files
and performs no fixes; this parent owns revision and re-review.

Select review depth and scope from the actual research risks and `econ-review` triggers, not from a general preference for stricter review. When the triggers leave two depths equally defensible and the result is promotion-bound or will leave the workspace (a paper draft, a coauthor, a referee, a replication package), take the stricter one. Record the chosen depth, whether promotion was requested, and the reason in the execution record. The selected lenses define coverage, not mandatory child agents. Apply the shared delegation policy and preserve the broader research question. This explicitly requested end-to-end workflow authorises its nested formal review stage.

Capture:
- retained findings;
- fix classes;
- trust effects;
- affected labels;
- residual work;
- missing diagnostic surfaces; and
- whether the panel was degraded.

Validate the response against `econ-review-report/v3` and require every selected
role lifecycle, canonical finding field, diagnostic gap, assessment lifecycle,
coverage field, verdict, safety record, canary, and promotion gate. Preserve and
stop on an unknown report version. For missing or malformed worker returns, reassess whether a local check or a
targeted follow-up can finish coverage; replacement starts count toward the
delegation budget. Retry a malformed same-version parent envelope once. If a promotion-tier panel remains
degraded, pause and ask whether to proceed with the named missing coverage; do
not enter revision or delivery as though the review were complete. At quick or
standard tier, carry degraded status and missing roles as explicit diagnostic
gaps, and do not deliver while any resulting trust-affecting gap remains
unresolved.

### Stage 4: Review-resolution pass

Do not deliver immediately after review. Use
`references/review_resolution_reference.md` to classify every retained finding
and diagnostic gap. Review outputs are evidence for the loop, not orders to
change the research object.

For every retained finding, inspect its finding ID, fix class, trust or
promotion effect, issue origin, affected labels, evidence locations, issue
follow-up type, user-judgement flag, confidence, missing diagnostic surfaces,
and authority source. Then assign exactly one route token:

- `fix-now`: `safe-automatic`, mechanical, or plan-required work that should be handled before delivery;
- `revise-plan-choice`: review evidence shows an agent-owned planning default should change;
- `ask-user`: the fix would override a researcher-anchored choice or touch the researcher-level trigger list;
- `defer-with-rationale`: legitimate follow-up outside the prompt or not needed for the requested output;
- `advisory-only`: useful note that does not affect trust, promotion, or the requested output.

For every diagnostic gap, inspect its gap ID, trust effect, issue origin,
affected labels, prior evidence, recommended action, and authority source. Use
the same route tokens: produce already-required evidence under `fix-now`, route
researcher choices to `ask-user`, and retain deferred or advisory gaps with
their `G<n>` IDs. Never treat a gap as resolved merely because no ordinary
finding was returned.

Apply this policy. Every revision-stage `econ-work` invocation includes
`caller_contract: econ-lfg/v1` and consumes `econ-work-for-caller/v1`. Every
targeted `econ-review` invocation instead uses a complete
`econ-review-request/v1` and consumes `econ-review-report/v3`; there is no
review-specific private caller contract.
- Fix `fix-now` findings and gaps through `econ-work` or a bounded local revision pass.
- Revise `revise-plan-choice` findings or gaps when the new path remains inside the initial prompt's intent.
- Pause for `ask-user` findings or gaps and write a decision memo when the decision is non-trivial.
- Record `defer-with-rationale` and `advisory-only` findings and gaps in the final closeout; do not hide them. Items that affect trust must also land on a durable residual sink before delivery — the review bundle's residual section, a GitHub issue (with approval), or a dated `docs/residual-findings/<slug>.md` — with `F<n>` or `G<n>` IDs preserved. Never deliver with trust-affecting residuals recorded only in chat.

The direct-fix boundary, the researcher-level trigger list, and the decision-memo contract are defined in `references/review_resolution_reference.md`; apply them exactly.

When a researcher-level decision needs evidence synthesis, write an economist-facing decision memo before asking, using HTML unless another format was requested. A clear single decision can be asked directly with its evidence and consequences; follow the proportional memo contract in the reference. When the installed runtime provides them, prefer the `econ-html-memo` skill for the memo shape and validation, and the `econ-writing` skill for prose discipline. If those skills are unavailable in the runtime, use the fallback memo contract in `references/review_resolution_reference.md` rather than failing on a dangling dependency. The memo must say what decision arose, what the outputs or review findings show, what the agent recommends and why, what changes under each choice, what stays unchanged, and what the agent will do next after the researcher decides.

Write runtime decision memos to the active research workspace. If the saved plan names a memo, note, or output directory, use it. Otherwise write to `docs/decision-memos/<YYYY-MM-DD>-<slug>.html` under the current task workspace. Do not write runtime decision memos into this package/source repo unless the task is explicitly about this repo.

If revisions materially change the plan's assumptions, record that divergence in the work closeout or a follow-up plan recommendation. Do not rewrite the saved plan as a progress log.

### Stage 5: Targeted re-review

If the initial review is complete and no revision, new evidence, or unresolved coverage issue requires another pass, proceed to delivery. Do not manufacture a revision or repeat an unchanged review.

After `fix-now` or `revise-plan-choice` revisions to findings or diagnostic
gaps, run targeted `econ-review` on changed or previously problematic surfaces.
Build another complete
`econ-review-request/v1` with `invocation: nested`, `caller: econ-lfg/v1`, and a
non-null `resolution_context`. That context names the prior run and carries
`finding_outcomes` and `gap_outcomes` maps keyed by each resolved finding ID and
diagnostic-gap ID. Each trace records the outcome (`fixed`,
`researcher-rejected`, or `deferred`), affected labels, and prior evidence
references; `fixed` also requires a changed path.
The new request's normal surfaces, scope, manifest, and triggers still define
what is reviewed; resolution context never suppresses new evidence or reuses
the old roster blindly.

Escalate to broader review only when revisions changed the baseline, sample, estimand, specification, inference, benchmark treatment, note argument, or primary output family.

Repeat the review-resolution pass until:
- no blocking or worth-fixing findings or diagnostic gaps remain;
- remaining findings and gaps are consciously deferred with rationale;
- a researcher-level decision prevents further meaningful work on the affected branch; or
- external access or missing data prevents meaningful progress.

### Stage 6: Deliver

Lead the final closeout with the research outcome and usable deliverable. Explain what the evidence supports, what changed, and the limitations that matter for interpretation or reuse. Then give the saved plan and main output paths, what was actually regenerated versus only inspected, the validation result, and the review conclusion. Translate internal terms when explaining them to the researcher; do not lead with schemas, stages, or agent status.

Keep detailed stage and code-role bookkeeping in the execution record, including the review depth chosen and any delegated worker's model, effort, and reason. Preserve finding and gap IDs for fixes and residuals, their targeted re-review outcomes, and durable residual paths. Disclose degraded coverage or a blocked promotion plainly; neither can be hidden by a shorter closeout. Include a decision memo or resume instruction only when one is needed. Do not create a follow-up merely to fill a final field.

If the autonomous run explicitly included compounding and produced a durable reusable lesson, invoke `econ-compound` after review-resolution. If compounding was in scope but no durable lesson emerged, report `Reusable lesson: none` and write nothing. When compounding was not in scope, keep any candidate in the closeout without interrupting the run or writing a learning note.

## Hard stops

- Do not skip `econ-plan` for non-trivial tasks.
- Do not proceed from `econ-work` to delivery without `econ-review`, unless the saved plan or work closeout explicitly says no later review is needed.
- Do not deliver with unprocessed review findings.
- Do not deliver a promotion-tier result while its reviewer panel remains degraded without the researcher's explicit decision.
- Do not stage, commit, or push unless the user explicitly requests that Git action.
- Do not silently override researcher-anchored choices.
- Do not make cross-language validation default-on.
- Do not auto-create GitHub issues unless the user requested issue creation or update.
- Do not add Compound Engineering PR, CI, browser-test, or deploy behavior to this workflow.
- Do not write durable learning notes unless the user explicitly asked for learning capture or the autonomous run explicitly includes compounding.

## Output

When complete, return the final closeout. When blocked, return:
- blocker type;
- decision or missing access needed;
- evidence path or review finding that caused the pause;
- options for the user;
- recommended conservative path; and
- exact command or prompt to resume the goal-backed run.
