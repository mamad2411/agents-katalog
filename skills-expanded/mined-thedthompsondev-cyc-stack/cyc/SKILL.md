---
name: cyc
description: "Run a software task through CYC: a fast scout, a build, and a verify loop that repeats until the project's real checks pass, then a concise handoff. Use when the user says \"cyc\", \"run this through cyc\", or, in a project with CYC installed, asks for a feature, bug fix, refactor, performance improvement, review, or verification, or asks to explain how code works, plan or compare approaches, resume interrupted work, prepare a handoff, or set up CYC."
---

# CYC

You own the outcome. Keep normal work short without dropping context reuse, review, or retained learning. Follow Scout and the compact [work assessment contract](../../docs/work-assessments.md) when `run next` requires it; load deeper methods only for the relevant question. A short route still owes every required outcome.

**One entry point.** Users invoke only `/cyc` and describe their outcome. Select the playbook and supporting methods yourself; never ask the user to choose a skill or present the internal catalog as a menu. Ask only about consequential missing requirements. For `/cyc` without a task, ask what they want to accomplish. For setup requests, use the linked Setup method. Supporting methods are internal instructions loaded by file path, not public slash commands; load only what the current step needs.

## Frontend work

“Make my homepage look better” is enough to start a visual redesign. Use the [frontend design method](../../methods/cyc-design/frontend-design/SKILL.md) for new sites and composed redesigns, including fast routes. The assistant owns art direction, accessible interaction and rendered comparison. Check the main action before extending a design, then verify the finished journey on desktop and phone. Apply the same sheet to host/platform requirements and the original criteria. Narrow repairs preserve identity. A request for critique or concepts stays within that scope.

## The flow

Select the playbook by the requested outcome and permissions using the table below; the keyword route is advisory. Review/explanation does not authorize product edits. Read the chosen playbook. The controller's next action owns stage order; supporting methods are internal paths, not additional public commands.

scout → build → finish/proof judgment → verify → deliver

Read the project's context index first, `docs/context/INDEX.md`, and then only the component docs whose Covers match affected paths. Plan canonical feature context before Build and retain it before final verification; the controller publishes the run's change record at completion. See [Context](../../methods/cyc-context/SKILL.md).

1. **Scout.** Read docs/context/INDEX.md, matched component docs and the relevant error ledger before code. Use investigate with affected paths to discover context/recipes; confirm freshness against actual files and the dirty diff. Reuse, extend, repair or create with a short reason. Trace authoritative state and affected consumers; for a new protected consumer execute the existing writer/status and new protected reads/writes together. Retain every original outcome and material clause. Ask only about consequential unknowns; do not manufacture approval.
2. **Start once.** Save START.json under .cyc/runtime with goal, playbook, explicit criteria/clauses, literal allowedPaths, evidenceVersion:1, original requirements text, reviewPolicy, plan and scout. Scout contains context, approach, alignment and named consumers; the [assessment contract](../../docs/work-assessments.md) defines fields. Include contextRetention: {version:1, disposition:"required", features:[{id,doc,paths}]} for each new/changed feature and affected shared owner. Use the target project’s focused canonical docs and index, creating them when missing; the controller includes these paths before scope freezes. Inspect the inferred plan if omitted. Generic handoffs, recipes and runtime logs do not satisfy feature retention. Explicit documentation restrictions remain pending without unauthorized writes. Pass it to run start --file START.json before edits. Scout supplied at start is already recorded; do not record it twice. Use the returned exact runId and generated template paths, never another conversation's sole run. Allowed paths are literal files/directory prefixes; translate brief globs without broadening authorization. Advisory wording-only work can use packet --advisory with the actual reason no run applies.
3. **Bind actual capability.** Set executionMode to native-codex, native-claude, cursor or explicitly authorized standalone. conversationId is the actual host conversation; session is a separate workflow label. Native modes need actual hook context; standalone neither creates hook state nor certifies activation and cannot downgrade a live native request. Unknown capability returns one setup action. Do not invent Cursor identity, tokens or host observations. Legacy callers retain their documented limits. The CLI is .cyc/engine/bin/cyc.mjs for copied installs or bin/cyc.mjs in this checkout.
4. **Build and record failures.** Follow the relevant [Build method](../../methods/cyc-build/SKILL.md). Write meaningful boundary tests, then the smallest coherent implementation. Feature/bug proof must fail on originals; refactor characterization must pass there. Preserve imported fields, references and access metadata when recreating records. Keep consumer policies coherent and server authorization separate from client response checks. Record failed fixes promptly in the selected ledger; run-local history is valid when shared history is outside scope. Finalize authorized source/context/ledger edits before final checks. Never clear proof ownership, overwrite unexpected edits or manually swap source to obtain proof.
5. **Review once, then affected changes.** Follow Rigor below. Capture before dispatch, fill recordTemplate with actual evidence and identity:null or observed text, then record it. Open findings block. Finish reuses current records; do not transcribe provenance. For bounded scopes inspect dependencies and declare contextPaths/contextEvidence; static imports/configuration bind coverage, unknown impact falls back to whole source. FollowupPath lists changes/contracts/findings; affected paths need new review. Matching provenance is not correctness.
6. **Finish with generated input.** Fill finishTemplate with summary, semantic judgments and one scenarioEvidence per original criterion/clause: named scenario, configured check, receipt:current-verification, result:passed, origin:agent-reported, actual evidence and consumers mapped to Scout IDs. Exact legacy views are derived; unavailable journeys stay unverified. Existing criterion/consumer evidence remains compatible.
   Run finish --run ID --file FINISH.json --wait-ms 30000. It prepares required canonical context before proof/final checks, completes stages and generates delivery evidence. Fill learning.context {id,currentView} or author planned docs; needs-context supplies remaining input until authored knowledge, index and source binding pass. Learning:none cannot waive a feature; restrictions remain pending. Later context edits need fresh checks, never only a new packet.
   Needs-proof-review supplies failure IDs, diagnostics and an exact bound continuation. Judge actual category/reason then invoke its command; module-load/setup is not a behavioral defect, unknown boundaries stay unknown. Bug fixes need decisive existing behavior; features may establish a missing interface. Do not inspect low-level files just to discover IDs or build a second packet. Truthful non-testable exemptions retain their limits. See [assessments](../../docs/work-assessments.md).
7. **Bound check work, preserve coverage.** Optional proofCommands at start freezes focused red/green execution. --tests chooses swapped files, not command scope. Final candidate checks remain broad. Pre-existing broad failures need compatible measured original broad evidence; finish measures it when an acceptance decision requires it, retaining focused results when valid. The existing baseline cache and candidate receipts reuse only compatible, explicitly local-deterministic checks; unknown inputs, external/freshness checks rerun. Never change config/tests to pass. A running operation returns phase/check/elapsed/latest available output, logs and an exact operation handle. Use run wait with that handle for 30–60 seconds when permitted; do not inspect lock files for ordinary progress. Silence, failure and interruption are distinct; honor user stop controls.
8. **Deliver.** Use the generated review and canonical run evidence; name decisive checks and disclose failures, unavailable services and unverified host activation. Native Codex/Claude finish writes its request-bound packet; standalone writes run-local delivery.json without a native claim. Cursor still needs its exact-response packet with explicit mode. Recheck the concise reply with check-reply; standalone uses --mode standalone instead of nonexistent hook-state reads. Follow the [response standard](../../docs/response-standard.md), including its visual and length rules. A stage, fingerprint or model-authored score never certifies product readiness. Retain pending proposals as pending; do not invent human acceptance.

Detailed/interrupted flows retain record/retry/recover. Failed checks require recovery/Build before edits; preserve evidence and shared budgets. Configure real checks before start; missing checks use [Setup](../../methods/cyc-setup/SKILL.md). Protected configuration and native gates cannot be weakened mid-run.

## Explain progress

For setup or a requested first-task walkthrough, explain the benefit once: the request says what changes; project rules and earlier decisions say what must keep working. Before work name the outcome and preserved behavior; during work connect an actual rule/discovery to a decision and check; after work link actual evidence, limits and saved target context. Introduce capabilities when useful, not as a catalog. Reuse onboard.experience, investigate match/freshness and route/workflowAdvice as leads. They do not certify semantics, authorize new work or waive checks. Unknown first-use history stays unknown; create no personal tracking store.

Use the [shared progress/engineering-understanding standard](../../docs/response-standard.md#progress-updates): readable behavior → mechanism → decision/check, usually one or two paragraphs at meaningful developments and about each minute of long work. Disclose uncertainty; command counts and explanation supplied do not prove understanding. Pass this to an authorized reviewer and consolidate findings.

## The senior bar

Apply the [engineering principles](../../docs/principles.md): smallest coherent change, root cause, observable tests that can fail, existing patterns/helpers, explicit domain state, boundary validation, migrated callers, tested assumptions after repeated failure, observed claims and readable code. Read the relevant trigger/skip signal when judging a consequential boundary.

## Rigor

The high-risk reviewer brief starts with the named authoritative state transition and conflicting legacy/canonical representations: execute the existing state-changing entrypoint followed by existing status and the new protected read/write consumer. Then test asynchronous actor/resource identity on reads and sends while cached identity remains unchanged. Preserve history continuity and focus findings; prioritize demonstrated privacy/identity failures before cosmetic issues. Reuse one authoritative resolver or require explicit reconciliation. Development examples are known data, not evidence of effectiveness on unseen tasks.

Scale process by risk, keeping the quality bar. Normal work uses the flow above. High risk (auth, permissions, payments, migrations, deletes, public APIs) adds one focused [Challenge](../../methods/cyc-challenge/SKILL.md) before Build and a fresh-context review before finish when subagents are available. Give that reviewer diff, original criteria, [principles](../../docs/principles.md), data contracts and producer/consumer paths; omit implementation rationale and require demonstrated findings. Resolve/dismiss with evidence. If unavailable record self and disclose it; extra agents require a specific independent question.

Capture before dispatch with run review-capture --run ID --file CAPTURE.json ({reviewer:"fresh-context",scope:["affected/path"]}; omit scope for whole source). Use returned template/command for review-record with reviewId,evidence,findings and actual identity/null; semanticReview.receipts references it. Self/peer scopes use the same record. These are agent-reported provenance, not identity attestation. Later edits need affected-delta review or explicit self/unverified coverage; mixed review is not a fresh review of every final byte. Source fingerprints establish bytes, not correctness.

## When things go wrong

Use run recover --run ID after a failure/interruption. It diagnoses existing records without resuming, resetting budgets or authorizing new scope. Preserve source, locks and proof backups; follow [recovery guidance](../../docs/onboarding-recovery.md). Tool-not-found and timeout errors are setup observations, not application diagnoses. After two failed fixes, check their shared assumption before another attempt.

Accept an unrelated pre-existing check only with a real reason and compatible measured original broad evidence. Candidate verification must retain the same failure: exit/error, named failing tests/errors and non-test lines, with no new failure or changed-source stack. Timings may differ. New regressions stay blocking; report accepted failures in the reply. Never repeatedly run unchanged failing checks, weaken tests/configuration, reset a budget or hide a stopped run behind a replacement. Focused proof is not a broad baseline.

If a missed consumer changes the plan, map it and repair within authorization. If the user says the result is wrong, use [Correct](../../methods/cyc-correct/SKILL.md). An external blocker gets an honest blocked handoff with the smallest needed action. Existing permission persists; do not ask again for an already authorized repair. Learning is proportionate: preserve verified facts and failed approaches, keep unverified hypotheses/proposals labeled, and follow the [context lifecycle](../../docs/work-assessments.md#learning-lifecycle-and-final-file-order).

## Playbooks

Use the [project tools](../../docs/project-tools.md) automatically when relevant: Scout/Understand discover matching context and recipes with `investigate`; Build uses a narrow recipe for feedback; Verify runs applicable authorized supplementary recipes and the controller's required checks. `run next` supplies stage-specific tool hints. Missing or inapplicable recipes fall back to project evidence; matched paths do not authorize side effects, and old receipts do not replace current verification.

| Intent | Playbook |
| --- | --- |
| Explain current behavior or reasons | [Investigation](references/playbooks/investigation.md) |
| Compare possible directions | [Explore](references/playbooks/explore.md) |
| Organize a multi-stage change | [Plan](references/playbooks/plan.md) |
| Add or change behavior | [Feature](references/playbooks/feature.md) |
| Repair broken behavior | [Bug fix](references/playbooks/bug-fix.md) |
| Preserve behavior while changing structure | [Refactor](references/playbooks/refactor.md) |
| Improve measured speed or cost | [Performance](references/playbooks/performance.md) |
| Assess existing work | [Review](references/playbooks/review.md) |
| Establish whether criteria hold | [Verify](references/playbooks/verify.md) |
| Improve an end-to-end user experience | [Experience](references/playbooks/experience.md) |
| Explain and support learning | [Teach](references/playbooks/teach.md) |
| Prepare a reviewable result | [Handoff](references/playbooks/handoff.md) |
| Recover an interrupted task | [Resume](references/playbooks/resume.md) |
| Extract supported lessons | [Reflect](references/playbooks/reflect.md) |
| Compare skill or workflow effectiveness | [Evaluate](references/playbooks/evaluate.md) |

## Work queue

A plan with several ordered units can run as a [work queue](../../docs/work-queue.md). When the user says "next" or "continue the queue", or `run next`/`run finish` shows a `queue` entry, call `queue next`. For a ready unit: read the listed dependency change records, recheck any drifted file, and tell the user about files under `drift.outsideUnit` before building on them. Follow the returned instruction: a Scout playbook adds scout and plan to the start file, another playbook starts it as written. Then `run start --file` it; keep its criteria, playbook and queue field as written. Work one unit per run, and after it completes tell the user which unit is next. A halted line needs the user: report the unit, its recorded reason and the files under `drift`, and record retry, skip or cancel with `queue decide` only after they choose. Never start a queue's work as an unbound run to get around a refusal.

The queue's [board](../../docs/work-queue.md#the-board) carries messages between agents and the user. When a `run` result starts with `board`, read it first. Read the code before asking; ask with `queue post --run ID` only what another unit or `person` owns. Wait with `queue wait`, or close your own question with disposition `assumed`; an answer given later still reaches you, so act on it or tell the user. `run finish` returning `needs-answer` lists what holds the unit: answer each finding `fixed` or `declined`. Never post as the person: show the user what waits for them and post only their answer. To review a unit another session builds: `queue next --seat review --session ID`, change no file, post findings, end with `review-done`. Under review: settle context records, post `ready-for-review`, wait, then `run review-record --from-board`. What holds a unit shows the message to post. When several sessions share a folder, draft your reply in a file of your own under `.cyc/runtime` and give that file to `check-reply`.

A person cannot see any of this from a chat. When you start working a queue, run `cyc hub` in the background and give the user the address it prints: the page shows the line, what the agents say to each other and what waits on the user, as it happens. Say that it is there; do not assume they are watching it.

## Autonomy

Just do: read, search, run tests, edit files in scope, build prototypes. Always ask first: commits and pushes (unless asked), publishing, deleting user data, global installs, sending messages. The delivery gate won't let you finish while your run is still open; a run that ends blocked is reported as blocked, never as done.

## Unified task context and bounded delegation

For available Codex dispatch, freeze delegation {version:1,mode:"auto"} at Start unless the user/project chooses off/recommend or a different host. Follow swarmAction: delegate swarm plans from task/source inventory, decides, runs independent workers concurrently and reviews/merges one task document. Default concurrency is two; preserve explicit limits. Unknown economics favors solo; time routing claims no savings. Inspect conflicts and terminal recovery before dependent work. Manual execute/reconcile remains available. Required review, proof, retention and checks remain mandatory. Usage is reporting only; never stop/refuse work for token counts. See [task context](../../docs/task-context.md); model judgments prove no activation/savings.
