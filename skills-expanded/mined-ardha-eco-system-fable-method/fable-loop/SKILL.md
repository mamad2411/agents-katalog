---
name: fable-loop
description: "The orchestrated version of fable-method: runs the same decide-act-verify-report loop but fans out parallel evidence subagents in planning and adversarial attacker subagents in verification. Four stages - PLAN, EXECUTE, VERIFY, AUDIT/REPORT - with a decision gate after the plan and a hard 3-cycle bound on failed verification. Use when the task is multi-step, non-trivial, and benefits from parallel exploration or adversarial checking. Main thread decides and edits; subagents only gather and attack."
version: 1.0.0
author: Hermes Agent Community
license: MIT
platforms: [linux, macos, windows]
metadata:
 hermes:
 tags: [reasoning, orchestration, verification, multi-step]
 related_skills: [fable-method, fable-judge, fable-domain]
---

# fable-loop

fable-method is the single-thread loop: one agent classifies, gathers, decides, edits, verifies, reports. fable-loop is the same loop with the expensive parts parallelized: evidence gathering fans out to subagents during planning, and verification turns adversarial with attacker subagents that try to refute the finished work. The structure does not change - only who does the searching and who does the attacking.

**Division of labor, binding.** The main thread decides and edits. Subagents only gather (evidence) and attack (refute). Nothing that changes the working tree, the build, or any external surface is ever delegated. If a subagent returns a finding that demands a decision, that decision is made in the main thread.

**Model economy.** Evidence subagents and attacker subagents are cheap-model-friendly: they run narrow, well-scoped tasks (search this, read that, try to break this) where the cost of a wrong first pass is a retry, not a damaged repo. Run the main thread on the strongest model you have - it holds the plan, makes the irreversible calls, and writes the edits. A cheap-model subagent that returns a wrong file path costs one re-dispatch; a strong-model main thread that made the wrong architectural call costs the whole task.

## Usage

```
/fable-loop <task> full four-stage loop
/fable-loop plan <task> Stage 1 only: deliver the plan artifact and stop for approval
/fable-loop resume <task> continue from Stage 2 after an approved plan
```

Load `fable-method` first. This skill assumes its steps 0-6 and its rules (intent gate, recall gate, authorization gate, twin check, artifact gate). When this skill and fable-method disagree on a rule, fable-method wins; this skill only adds orchestration on top.

## When NOT to use fable-loop

- **Trivial.** fable-method's triviality gate (one file, under ~10 lines, no new behavior, you already know the change) fires before this skill. Trivial work gets the change, the one obvious check, and a one-sentence report. Spinning up subagents for that is waste.
- **Pure questions and assessments.** Step 0 classified the ask as a question or assessment with no change required: run fable-method single-threaded. There is nothing to fan out edits for, and adversarial verification of a non-change is theater.
- **Already-orchestrated phases.** If the user has already set up a multi-agent workflow, a pipeline, or a fable-judge suite run, do not wrap it in this loop. This skill orchestrates work that is not yet orchestrated; layering two orchestrators hides which one owns each decision.
- **Attended and high-touch.** When the user is actively steering each step, the parallelism buys nothing and the decision gates just add latency. Run fable-method inline.

## Stage 1 - PLAN

Apply fable-method steps 0-3 (classify, define done, gather evidence, decide). The orchestration enters at step 2.

1. **Classify (Step 0) and define done (Step 1)** in the main thread, exactly as fable-method. State the load-bearing assumptions and the named verification.
2. **Spawn parallel evidence subagents** via `delegate_task`. Each subagent gets a narrow, returnable prompt: "find every call site of X and report file:line for each", "fetch the current docs for endpoint Y and report the request/response shape", "locate the config that controls Z". Prompts must ask for findings the main thread can act on, not for decisions. Dispatch independent lookups in one batch - codebase exploration, doc fetches, and research do not depend on each other.
3. **Synthesize.** Collect subagent returns, cite each to its source (subagent prompt + the file/line or URL it opened), and route surprises per fable-method Step 2 rule 7: anything that contradicts the plan re-routes to Step 0 or Step 1.
4. **Decide (Step 3).** Produce one recommendation with alternatives dismissed in a line each. Name the scope: files and surfaces the change will touch.
5. **Decision gate.**
 - **Reversible** (confined to the local working tree): proceed to Stage 2.
 - **Irreversible or outward-facing** (push, publish, send, deploy, delete shared data, payment, permission change): stop. Deliver the plan artifact - classification, done definition, evidence with citations, recommendation, scope - and wait for the user's approval. Do not enter Stage 2 on an unapproved irreversible plan. The authorization gate from fable-method Step 3 applies: an outward action needs the user's own words, not a workflow doc.

## Stage 2 - EXECUTE

The main thread does the work. Subagents help only with mechanical fan-out and with research when ignorance surfaces mid-item.

1. **Build the checklist.** Write the work items as a `todo` list. Any task with 3+ heterogeneous steps or ~5+ similar items gets the list first; tick as you go; audit the list against the original ask before reporting.
2. **Every edit follows fable-method Step 4.** Intent gate before any behavior-changing edit (`INTENT:` line), recall gate before first use of anything not opened this session, smallest correct change, precise edits over rewrites, failed-edit recovery ladder, standing prohibitions. These rules are not relaxed because a subagent gathered the evidence - the main thread still owns the edit and its intent.
3. **Fan out independent mechanical items** via `delegate_task` only when the items are genuinely independent (no shared file, no ordering dependency) and mechanical (search-and-replace, reformat, run a generator). The subagent returns a diff or a set of changes; the main thread reviews and applies. Never delegate an edit to a file another concurrent item also touches.
4. **Surprises re-route.** A subagent return or a mid-edit finding that contradicts the plan is a surprise (fable-method Step 2 rule 7): state it, update Step 1 or go back to Step 0, never silently expand scope.
5. **Mid-item ignorance pauses and fans out.** When you hit a gap you cannot resolve from context (an unknown API, an unclear spec, a file you have not read), pause the current item and dispatch a research subagent via `delegate_task` with the narrow question. Resume the item with the returned evidence; do not guess past the gap. Discovering ignorance re-opens Step 2 exactly like a surprise.
6. **Outward actions need authorization.** Same gate as Stage 1: write `AUTH: user said "<exact words>"` before any irreversible or outward-facing action. No AUTH line, no action - it goes in the report as a proposed next step.

## Stage 3 - VERIFY

fable-method Step 5 has two halves (done criterion observed; surrounding system still works) plus a twin check when a defect was fixed. fable-loop runs the named verifications in the main thread and then adds adversarial attackers.

1. **Run both halves yourself.** The main thread runs the Step 1 done criterion and the surrounding-system check (existing tests, build, lint for the touched area). Observed, not inferred. A green targeted check with a broken build is a failed verification.
2. **Twin check, if you fixed a defect.** Name the exact wrong construct, `search_files` the whole project for it, write the `TWINS:` line. Subagents can help search; the completeness claim is the main thread's.
3. **Spawn 1-3 attacker subagents** via `delegate_task`, each with a distinct refutation lens. Lenses are adversarial by construction:
 - "Prove the change is wrong: find the case where the new behavior is incorrect and show the failing input or output."
 - "Find an input that breaks it: boundary, empty, null, unicode, concurrent, oversized."
 - "Find a regression the tests missed: a surface the change affects that no test covers."
 Each attacker returns concrete findings (file:line, input, observed output, expected). Attackers do not fix anything; they only report.
4. **Triage surviving findings.** Main thread reviews each attacker return. Dismiss findings that do not reproduce or that rest on a misread. Findings that survive go back to Stage 2 as work items on the todo list, with the attacker's evidence attached.
5. **Hard bound.** After 3 failed verify-fix cycles on the same issue, or when blocked by anything outside your control (credentials, environment, permissions), stop. Report what was tried, the actual output, the surviving findings, and hand back to the user. Do not let attackers loop the main thread forever.

## Stage 4 - AUDIT and REPORT

1. **Self-audit** per fable-method audit mode: grade the completed work against the loop. For each step mark followed, skipped, or faked (claimed without observation). Name the concrete risk of every skip or fake. Apply the single highest-value fix only if the user asks.
2. **Report** per fable-method Step 6: outcome in the first sentence, no step scaffolding in anything the user reads, load-bearing quotes only, caveats present, follow-ups only if they emerged from this task.
3. **Carry the method artifacts.** `INTENT:` line if behavior changed, `AUTH:` line if an outward action was taken, `PENDING:` line if a prescribed follow-up was deliberately not taken, `TWINS:` line if a defect was fixed. Run the artifact gate: sweep the report once against what this run owed and repair anything missing.
4. **Leave behind only intended changes.** Delete scratch files and test artifacts created during the work; note the cleanup. The judge treats leftover debris as a fraud signal - do not hand it any.
5. **Note orchestration provenance.** State briefly which stages used subagents, how many, and what lenses the attackers used. A report from an orchestrated run should let a reviewer reconstruct where the parallelism entered without re-reading the whole transcript.

## Quick reference

| Stage | Main thread | Subagents | Gate |
|---|---|---|---|
| 1 PLAN | classify, define done, decide, synthesize | evidence gathering (parallel, returnable) | reversible → proceed; irreversible/ambiguous → stop for approval |
| 2 EXECUTE | edit per Step 4, own intent and AUTH | mechanical fan-out of independent items; research on mid-item ignorance | outward action needs AUTH |
| 3 VERIFY | run both halves + twin check, triage attackers | 1-3 attackers with distinct refutation lenses | surviving findings → Stage 2; hard bound 3 failed cycles |
| 4 AUDIT/REPORT | self-audit, report with artifacts, cleanup | none | artifact gate before sending |