---
name: diagnose
description: Use when debugging bugs, failures, regressions, stale proof, recurring whack-a-mole fixes, unclear ownership, poor seams, missing domain boundaries, write/leak risks, or behavior needing coordinated root-cause investigation.
---

# Diagnose

A discipline for hard bugs. `$diagnose` is an orchestrator skill: it builds the feedback loop, launches bounded investigators when work can be split, integrates evidence, proves root cause, reaches bounded cohort agreement on the issue and resolution when the work is substantive, emits a build-ready JSON packet with fix evals and a pasteable `/goal` handoff, and prints a human-readable diagnosis rundown to the screen. Skip phases only when explicitly justified.

Default boundary: `$diagnose` sets up the whole fix; it does not implement the fix unless the user explicitly asks this same run to implement after diagnosis and the active route permits edits. A normal `$diagnose` run stops at the JSON packet.

When exploring the codebase, use the project's domain glossary to get a clear mental model of the relevant modules, and check ADRs in the area you're touching.

## Operating standard

Diagnose uses the Toyota Way adapted for software debugging:

- **Genchi genbutsu**: go to the real code, runtime, schema, logs, payloads, and users' workflow. Do not debug from vibes.
- **Five whys**: keep asking why until the cause explains the defect class, not only the visible symptom.
- **Jidoka**: stop the line when the feedback loop, ownership, seam, live schema, tenant boundary, or write/leak radius is unknown.
- **Kaizen / clean as you go**: if the bug exposes local SRP, ownership, seam, missing-domain, or coupling debt in code you must touch, classify it and clean the `fix-now` part as part of the diagnosis/fix. Do not leave the next whack-a-mole bug for someone else.
- **Standardised work**: finish with a regression loop, cleanup, and a causal note future agents can reuse.
- **Ratchets**: every root-cause fix should add a permanent guard where practical: a regression test, domain boundary, invariant check, lint/contract/gate, ownership doc, or deleted duplicate path that makes the old failure mode harder to reintroduce.
- **Fresh evidence**: diagnosis evidence must belong to the current head, branch, PR, runtime, schema, proof subject, and original user symptom. Stale proof is not proof.
- **PRs are evidence, not boundaries**: when the prompt names a PR, treat that PR as one artifact in the causal chain. Do not stop at "what the PR changed" until you have tested whether a lower writer, integration, retry, formatter, or side-effect path still creates the same symptom.

## Orchestrator mode

The lead agent owns the final causal chain and fix decision. Subagents provide bounded evidence only.

Launch specialised subagents whenever there are two or more independent investigation tracks, the codebase area is unfamiliar, or one agent would otherwise mix reproduction, ownership tracing, data proof, and fix design in the same pass.

Use narrow roles. No subagent gets more than one job:

- **Repro loop investigator**: builds or sharpens the deterministic failure signal.
- **Ownership/SRP investigator**: maps the owning module, overloaded files, duplicate responsibilities, and refactor classification.
- **Domain-boundary investigator**: decides whether the behavior belongs in an existing domain, needs extraction into a domain service/model, or is correctly local to the current layer.
- **Seam investigator**: finds the correct regression-test seam and flags false-confidence seams.
- **Write/leak radius investigator**: enumerates direct and transitive writes, side effects, tenant/auth/data leaks, cache/event/job retries, and the affected records/users/tenants/processes.
- **Recent-trap investigator**: reviews recent PR/review/proof failures for the touched domain and extracts trap classes that could recur here.
- **Evidence-freshness investigator**: verifies that commands, proof artifacts, schema checks, PR numbers, branch names, SHAs, and runtime subjects match the current diagnosis.
- **Runtime/source-truth investigator**: verifies live schema, config, queue, external integration, log, or payload facts.

Prefeed subagents with exact files, symbols, commands, source snippets, and stop rules. Ask for concise evidence: facts, paths, commands, failed assumptions, and unanswered questions. Do not delegate implementation until the root cause and fix-now cleanup are known.

## Cohort agreement loop

For substantive, repeated, unclear, high-risk, or build-ready diagnoses, `$diagnose`
must run a bounded agreement loop before handing off implementation. Use
`/Users/ben/.codex/skills/diagnostic-cohort/SKILL.md` as the reusable contract
when a formal artifact is needed.

Agreement means the required reviewers approve the same:

- user-visible issue
- confirmed root cause
- owning-boundary resolution
- fix evals
- pasteable `/goal` prompt for the build lane

Minimum reviewer lenses:

- `issue-root-cause-reviewer`: confirms symptom, causal chain, and owner.
- `adversarial-but-why-reviewer`: challenges assumptions, contradictions,
  shallow causality, and rejected alternatives.
- `proof-eval-reviewer`: checks fix evals, proof freshness, and stop rules.

Add `blast-radius-reviewer`, `patch-or-fix-reviewer`, domain, runtime, schema,
or UI reviewers when the bug class requires them.

Finite loop rules:

- Run one initial reviewer round.
- If reviewers materially disagree, update the evidence or packet and run one
  focused recheck round.
- Do not run more than two rounds by default, or more than three with explicit
  user approval.
- Do not rerun the same reviewer on unchanged evidence.
- If the same blocker repeats, if a required reviewer cannot run, or if evidence
  cannot resolve disagreement, stop with `diagnosis_status: "blocked"` or
  `root_cause_ready`, not `build_ready`.

Tiny, deterministic, low-risk bugs may use a documented solo-low-risk rationale
instead of spawning a cohort, but `build_ready` for substantive work requires
cohort agreement.

## Root-cause confirmation gate

Do not produce a way-forward as `build_ready` until root cause has been
confirmed. Confirmation requires:

- the symptom, immediate cause, deeper cause, and root cause are linked by
  evidence in `root_cause_chain`
- the owning boundary is named and source-proven
- plausible alternate hypotheses are rejected or recorded as remaining
  uncertainty
- the cohort, or documented solo-low-risk review, agrees the proposed resolution
  changes the source of the defect rather than a consumer-layer symptom

If the feedback loop proves the symptom but root cause is not confirmed, use
`repro_ready`. If root cause is confirmed but the resolution/evals/goal handoff
are not agreed, use `root_cause_ready` or `blocked`.

## Fix evals and pasteable goal handoff

Every `build_ready` diagnosis must include fix evals and a pasteable `/goal`
prompt. Fix evals are stronger than a generic verification list: they state what
must fail before the fix or prove the old failure cannot recur after the fix.

Each fix eval must name:

- purpose
- command or proof action
- proof type
- expected failure before the fix
- expected pass after the fix
- freshness subject
- required-before gate

The `/goal` prompt must be safe to paste into a fresh build thread. It must name
the diagnosis packet path, allowed scope, required eval IDs, verification plan,
and follow-up gates such as `patch-or-fix`, `blast-radius`, PR checks, or live
proof when applicable. It must also tell the build agent what not to do.

## Mandatory structural diagnosis

Every run must answer these before Phase 5 starts:

- **Ownership**: Which module/service/table/route/job owns the behavior? Which callers only consume or display it? Is ownership duplicated, missing, or leaking across boundaries?
- **SRP/refactor**: Is any touched file doing three or more jobs, hiding domain logic in transport/UI/glue code, or mixing read/write/orchestration concerns? Classify cleanup as `fix-now`, `follow-up`, or `note-only`. `fix-now` is mandatory when needed to fix the root cause safely or create the correct seam.
- **Domain refactor**: Should this behavior move into an existing domain boundary or a new domain-owned service/model as part of the fix? If the bug exists because domain logic is scattered across routes, UI, workers, scripts, or ad hoc helpers, domain refactoring is `fix-now` for the touched path.
- **Seam discipline**: What is the real seam where the bug pattern occurs? If no correct seam exists, that is a root-cause finding. Create or expose the seam when it is required for the fix.
- **Write/leak impact count**: Count direct writes, transitive writes, external side effects, data/auth/tenant leaks, cache invalidations, events, jobs, retries, and read paths that can amplify the bug. Name the affected records, users, tenants, operators, integrations, and business processes when knowable.
- **Whack-a-mole risk**: What sibling paths share the same shape? If one path failed because of ownership, SRP, seam, or write/leak coupling, search for siblings before declaring the fix complete.
- **Ratchet**: What permanent prevention makes this bug class harder to reintroduce? Prefer tests and domain invariants first, then gates, docs, or deleted duplicate paths when those are the right prevention layer.
- **Recent PR trap replay**: Which recent PR review comments, proof misses, blast-radius findings, canary failures, or post-deploy fixes involved the same domain, seam, data shape, status lifecycle, writer, integration, or proof lane? Replay the trap class or record why it does not apply.
- **Evidence freshness**: What exact head/SHA, branch, PR, database/schema source, runtime, proof artifact, log window, and original symptom does each claim refer to? Reject stale, dry-run-only, wrong-branch, wrong-PR, wrong-subject, mock-only, migration-only, or manually observed proof when stronger proof is required.
- **PR anchoring check**: If the bug report mentions a PR, does the PR merely mask, format, or route around the symptom while a lower owner still produces the bad state? Prove the deepest owner that can still create the symptom, not only the diff that recently changed the message.

## Required JSON diagnosis packet

Every `$diagnose` run must produce a machine-readable JSON packet that a build agent or multiple subagents can execute without rereading the whole conversation.

Default path:

```text
.codex/diagnose/<slug>-diagnosis.json
```

If repo artifact writes are blocked, write the packet to an approved scratch directory or return the full JSON in the final response and state why a file was not written. The packet must be valid JSON, not Markdown. Use `references/diagnosis-packet.schema.json` as the shape contract.

The packet must use:

```json
{ "schema_version": "diagnose.build_packet.v1" }
```

Numeric or ad hoc schema versions are invalid.

Minimum packet requirements:

- `schema_version`, `packet_id`, `created_at`, `repo_root`, `head_sha`, `branch`, `source_issue_or_pr`, and `original_prompt`
- `diagnosis_status`: `blocked`, `repro_ready`, `root_cause_ready`, `build_ready`, or `fixed_pending_verify`
- `root_cause_chain`: symptom -> immediate cause -> deeper cause -> root cause, with file/line evidence
- `ownership`: owning domain/module/table/job, consumers, wrong owners, and source of truth
- `srp_refactor`: `fix_now`, `follow_up`, and `note_only` lists with reasons
- `domain_refactor`: existing or new domain boundary, fix-now extraction, and non-goals
- `seam`: correct regression seam, false-confidence seams, and missing-seam findings
- `write_leak_impact`: direct writes, transitive writes, external side effects, leak paths, retries/jobs/events, and affected records/users/tenants/integrations
- `recent_trap_replay`, `evidence_freshness`, `sibling_search`, and `ratchets`
- `root_cause_confirmation`: decisive evidence, rejected hypotheses, remaining uncertainty, and whether root cause was confirmed before the build plan
- `consensus_review`: cohort or solo-low-risk agreement status, rounds, participants, agreed issue/root cause/resolution, dissent, stop reason, and optional diagnostic-cohort contract path
- `fix_evals`: evals that define expected failure before the fix and expected pass after the fix
- `goal_prompt`: pasteable `/goal` text, eval IDs it must pass, scope limits, and do-not-do guardrails
- `build_plan`: ordered tasks with exact files, owner role, dependencies, acceptance criteria, verification command, and stop rule
- `subagent_tasks`: disjoint tasks where each subagent has one job and a bounded file/symbol responsibility
- `verification_plan`: focused tests, live/migrated DB checks, headless/UI checks, canary/deploy proof, and what evidence is not yet available
- `blockers`, `assumptions`, `open_questions`, and `do_not_do`

Do not mark `diagnosis_status` as `build_ready` unless ownership, SRP, domain boundary, seam, write/leak impact, evidence freshness, trap replay, and verification plan are populated enough for another agent to start safely.

Also do not mark `diagnosis_status` as `build_ready` unless
`root_cause_confirmation.confirmed` is true, `consensus_review.agreement_status`
is `agreed`, `fix_evals` is non-empty, and `goal_prompt.pasteable_text`
contains a `/goal` handoff that references the required eval IDs.

The packet's `do_not_do` list must explicitly include a diagnosis-boundary item such as: `Do not edit, implement, mutate code, or make code changes during diagnosis.` Each `subagent_tasks[*].forbidden` list must also explicitly block edits, implementation, mutation, or code changes.

Validate every packet before using it as a handoff:

```bash
python3 /Users/ben/.agent-platform/skills/diagnose/scripts/validate_diagnosis_packet.py <packet.json> --diagnosis-only
```

When validating the skill itself, run:

```bash
python3 /Users/ben/.agent-platform/skills/diagnose/evals/run_packet_evals.py
```

## Required screen rundown

The JSON packet is the machine handoff, not the user-facing explanation. Every
`$diagnose` run must also print an easy-to-read Markdown or plaintext rundown to
the screen before finishing. Do this even when the packet was written to disk.

Keep the rundown compact and concrete:

- `Status`: one of the packet diagnosis statuses, plus whether the packet is
  validated or blocked.
- `Issue`: the original symptom in one or two sentences.
- `Root cause`: the causal chain in plain English, or the strongest current
  hypothesis when blocked before root cause.
- `Impact`: affected records, users, tenants, integrations, jobs, queues,
  writes, leaks, or operator workflows when known.
- `Evidence`: the decisive files, commands, logs, schema/runtime checks,
  subagent findings, and freshness subject.
- `Blockers / unknowns`: anything that prevents a build-ready diagnosis.
- `Build handoff`: the JSON packet path and the first three build-agent steps.
- `Fix evals`: the eval IDs, commands/proof actions, and expected pass/fail behavior.
- `Goal prompt`: the pasteable `/goal` handoff, or the blocker that prevents one.
- `Verification`: the focused proof loop the build agent must run.

Do not paste the full JSON as the rundown unless artifact writes are blocked and
the full packet must be returned inline. The rundown should let a human quickly
understand what is wrong, why it is wrong, what still is not proven, and what the
next agent should do.

## Phase 1 — Build a feedback loop

**This is the skill.** Everything else is mechanical. If you have a fast, deterministic, agent-runnable pass/fail signal for the bug, you will find the cause — bisection, hypothesis-testing, and instrumentation all just consume that signal. If you don't have one, no amount of staring at code will save you.

Spend disproportionate effort here. **Be aggressive. Be creative. Refuse to give up.**

### Ways to construct one — try them in roughly this order

1. **Failing test** at whatever seam reaches the bug — unit, integration, e2e.
2. **Curl / HTTP script** against a running dev server.
3. **CLI invocation** with a fixture input, diffing stdout against a known-good snapshot.
4. **Headless browser script** (Playwright / Puppeteer) — drives the UI, asserts on DOM/console/network.
5. **Replay a captured trace.** Save a real network request / payload / event log to disk; replay it through the code path in isolation.
6. **Throwaway harness.** Spin up a minimal subset of the system (one service, mocked deps) that exercises the bug code path with a single function call.
7. **Property / fuzz loop.** If the bug is "sometimes wrong output", run 1000 random inputs and look for the failure mode.
8. **Bisection harness.** If the bug appeared between two known states (commit, dataset, version), automate "boot at state X, check, repeat" so you can `git bisect run` it.
9. **Differential loop.** Run the same input through old-version vs new-version (or two configs) and diff outputs.
10. **HITL bash script.** Last resort. If a human must click, drive _them_ with `scripts/hitl-loop.template.sh` so the loop is still structured. Captured output feeds back to you.

Build the right feedback loop, and the bug is 90% fixed.

### Iterate on the loop itself

Treat the loop as a product. Once you have _a_ loop, ask:

- Can I make it faster? (Cache setup, skip unrelated init, narrow the test scope.)
- Can I make the signal sharper? (Assert on the specific symptom, not "didn't crash".)
- Can I make it more deterministic? (Pin time, seed RNG, isolate filesystem, freeze network.)

A 30-second flaky loop is barely better than no loop. A 2-second deterministic loop is a debugging superpower.

### Non-deterministic bugs

The goal is not a clean repro but a **higher reproduction rate**. Loop the trigger 100×, parallelise, add stress, narrow timing windows, inject sleeps. A 50%-flake bug is debuggable; 1% is not — keep raising the rate until it's debuggable.

### When you genuinely cannot build a loop

Stop and say so explicitly. List what you tried. Ask the user for: (a) access to whatever environment reproduces it, (b) a captured artifact (HAR file, log dump, core dump, screen recording with timestamps), or (c) permission to add temporary production instrumentation. Do **not** proceed to hypothesise without a loop.

Do not proceed to Phase 2 until you have a loop you believe in.

## Phase 2 — Reproduce

Run the loop. Watch the bug appear.

Confirm:

- [ ] The loop produces the failure mode the **user** described — not a different failure that happens to be nearby. Wrong bug = wrong fix.
- [ ] The failure is reproducible across multiple runs (or, for non-deterministic bugs, reproducible at a high enough rate to debug against).
- [ ] You have captured the exact symptom (error message, wrong output, slow timing) so later phases can verify the fix actually addresses it.

Do not proceed until you reproduce the bug.

## Phase 3 — Zoom out + assign investigators

Before hypothesising, map the bug one layer outward:

- Entry points, callers, consumers, sibling paths, jobs, caches, queues, and external systems.
- The owning module and the modules that should not own the behavior.
- The domain that owns the invariant, or the missing domain boundary that let the bug escape.
- All write/leak paths that can affect or amplify the bug.
- The correct seam for a regression test.
- Any file or boundary in the likely fix path that violates SRP or hides domain logic.
- Recent PR/review/proof traps for this domain, plus whether each trap class is applicable.
- Evidence subjects: current head/SHA, branch, PR, runtime, schema source, artifact date, and the user's original symptom.
- For named PRs, the layer below the PR diff: producer/writer, integration response, retry queue, formatter/display path, and side effects that can still produce the same user-visible failure.

If the map has independent branches, launch the relevant subagents from Orchestrator mode. Continue only after their evidence is integrated or their blockers are explicit.

## Phase 4 — Hypothesise

Generate **3–5 ranked hypotheses** before testing any of them. Single-hypothesis generation anchors on the first plausible idea.

Each hypothesis must be **falsifiable**: state the prediction it makes.

> Format: "If <X> is the cause, then <changing Y> will make the bug disappear / <changing Z> will make it worse."

If you cannot state the prediction, the hypothesis is a vibe — discard or sharpen it.

**Show the ranked list to the user before testing.** They often have domain knowledge that re-ranks instantly ("we just deployed a change to #3"), or know hypotheses they've already ruled out. Cheap checkpoint, big time saver. Don't block on it — proceed with your ranking if the user is AFK.

## Phase 5 — Instrument

Each probe must map to a specific prediction from Phase 4. **Change one variable at a time.**

Tool preference:

1. **Debugger / REPL inspection** if the env supports it. One breakpoint beats ten logs.
2. **Targeted logs** at the boundaries that distinguish hypotheses.
3. Never "log everything and grep".

**Tag every debug log** with a unique prefix, e.g. `[DEBUG-a4f2]`. Cleanup at the end becomes a single grep. Untagged logs survive; tagged logs die.

**Perf branch.** For performance regressions, logs are usually wrong. Instead: establish a baseline measurement (timing harness, `performance.now()`, profiler, query plan), then bisect. Measure first, fix second.

## Phase 6 — Build packet + regression design

Do not edit runtime, test, migration, documentation, or config files during a normal `$diagnose` run. The output is the JSON packet that tells the build agent exactly what to edit.

Design the regression test **before the fix** — but only if there is a **correct seam** for it. Put that test design in `seam.regression_test`, `build_plan`, and `verification_plan`.

A correct seam is one where the test exercises the **real bug pattern** as it occurs at the call site. If the only available seam is too shallow (single-caller test when the bug needs multiple callers, unit test that can't replicate the chain that triggered the bug), a regression test there gives false confidence.

**If no correct seam exists, that itself is the finding.** Note it. The codebase architecture is preventing the bug from being locked down. Flag this for the next phase.

The build plan must place the fix at the owning boundary. Do not route the build agent to a consumer/display path when the owner is producing bad state, missing validation, or leaking write responsibility. If the correct fix requires local SRP cleanup, seam extraction, domain extraction, or ownership consolidation in touched code, encode that cleanup as `fix_now` work in the packet.

Add the ratchet to the build plan. A ratchet can be a regression test at the domain seam, an invariant inside the domain service/model, a removed duplicate writer, a contract/gate that fails on the old shape, a replay of a recent trap class, or a source-truth doc update that prevents future ownership drift.

Plan fresh proof at the current head and name the exact proof subject. Do not carry forward older PR artifacts, dry-run output, screenshots, logs, local guesses, or deployment evidence unless they demonstrably match the current code and symptom.

Before setting `diagnosis_status` to `build_ready`, fill:

- `root_cause_confirmation`
- `consensus_review`
- `fix_evals`
- `goal_prompt`

If a formal consensus artifact was produced, reference it from
`consensus_review.contract_path_or_id`. If the cohort blocks, keep the packet but
lower the status and put the blocker in the screen rundown.

If a correct seam exists:

1. Specify how the build agent should turn the minimised repro into a failing test at that seam.
2. Specify the expected failure.
3. Specify the owning-boundary fix.
4. Specify the expected passing result.
5. Specify how to re-run the Phase 1 feedback loop against the original scenario.

If the user explicitly asks `$diagnose` to continue into implementation after the packet, treat that as a separate routed phase: re-check edit permission, worktree safety, enterprise gates, and verification requirements before any patch.

## Phase 7 — Cleanup + post-mortem

Required before declaring done:

- [ ] Original repro is captured or the blocker to reproducing it is explicit
- [ ] Regression test design is in the packet, or absence of seam is documented
- [ ] JSON diagnosis packet exists, validates as JSON, and is build-agent usable
- [ ] `validate_diagnosis_packet.py <packet> --diagnosis-only` passes
- [ ] Packet uses `schema_version: "diagnose.build_packet.v1"`
- [ ] Ownership boundary is named and the fix landed there, or the exception is justified
- [ ] SRP/refactor cleanup is classified, with `fix-now` cleanup completed
- [ ] Domain refactor decision is documented, with touched-path `fix-now` domain extraction completed when required
- [ ] Correct seam is covered, or missing seam is recorded as a root-cause architecture finding
- [ ] Write/leak impact count is documented, including direct writes, transitive writes, side effects, leaks, and amplified consumers
- [ ] Sibling whack-a-mole paths were searched or explicitly ruled out
- [ ] Ratchet is in place: test, invariant, gate, deleted duplicate path, or documented ownership guard
- [ ] Recent PR/review/proof trap classes were replayed or ruled out with evidence
- [ ] Evidence freshness is documented: current head/SHA, branch, PR, runtime/schema source, proof artifact, and symptom match
- [ ] Named PRs were treated as evidence, not diagnosis boundaries; lower owners that can still produce the symptom were tested or ruled out
- [ ] All `[DEBUG-...]` instrumentation removed (`grep` the prefix)
- [ ] Throwaway prototypes deleted (or moved to a clearly-marked debug location)
- [ ] The hypothesis that turned out correct is stated in the commit / PR message — so the next debugger learns

**Then ask: what would have prevented this bug?** If the answer involves architectural change (no good test seam, tangled callers, missing domain boundary, hidden coupling, too many writers, unclear ownership, or leak-prone boundaries), either complete the local `fix-now` cleanup or hand off the broader `follow-up` with specifics. Make the recommendation **after** the fix is in, not before — you have more information now than when you started.
