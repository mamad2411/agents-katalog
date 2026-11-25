---
name: multi-agent-evaluation
description: >-
  Orchestrate a rigorous, provider-neutral evaluation panel for software,
  websites, UI, design, writing, research, data, automation, or games. Use
  when the user asks for many agents or subagents, independent critics,
  competing approaches, adversarial testing, a hard evaluation mindset, or
  evidence-led improvement. Dispatch distinct roles through the host's native
  delegation interface when available, fall back to isolated clean-room review
  passes when it is not, and never declare success from self-review alone.
---

# Multi-Agent Evaluation

Use this skill as a dispatch and evaluation layer for work that needs several
independent perspectives. Inspect the real artifact, make each review falsify
the candidate rather than praise it, reconcile evidence, change the largest
gap, and run a fresh integration review.

This skill is separate from `gauntlet-loop`. It does not replace, rename, edit,
or weaken the existing `gauntlet-loop` skill. If both are requested, let
`gauntlet-loop` own the persistent objective and continuation state, and use
this skill to supply the independent panel, adversarial grading, and evidence
rechecks.

## Decide whether to use a panel

Use a panel when at least one of these is true:

- The user explicitly asks for lots of agents, subagents, critics, reviewers,
  or parallel work.
- The artifact has several quality dimensions that one reviewer could miss.
- A decision is costly, difficult to reverse, user-facing, or high risk.
- The first implementation looks polished but has not been tested against the
  actual user journey, reference, or production boundary.

Do not create agent work merely to make a trivial one-file change look larger.
For a genuinely small, low-risk task, use three short review lanes or explain
why a panel would add no useful independence.

## Establish the evaluation packet

Before dispatching, write a compact packet that every reviewer can understand
without the coordinator's hidden reasoning:

```text
Objective: the outcome that must become true.
Artifact: exact files, routes, build, document, dataset, or live read-only view.
Quality bar: reference, rubric, acceptance criteria, or measurable benchmark.
Proof available: tests, screenshots, source material, recordings, logs, or data.
Non-negotiables: facts, design decisions, interfaces, or boundaries to preserve.
Scope: what may be inspected or changed locally.
Gates: approval, credential, spend, publish, deploy, delete, or contact limits.
Revision: commit, file hash, timestamp, or other identity of the candidate.
```

If the objective, artifact, or quality bar is materially unclear, ask one
decision-changing question before dispatch. If a non-critical detail is
missing, record a defensible assumption and continue; do not silently invent
requirements.

Run a baseline inspection before asking others to judge the work. Capture the
actual starting tests, rendered output, source trace, or user journey result.
Never ask a reviewer to grade a summary instead of the artifact.

## Set panel size and independence

Use distinct lanes, not several copies of the same vague prompt:

- Small but non-trivial: three lanes.
- Normal non-trivial work: five lanes by default.
- Complex, multi-surface, or explicitly “use lots of agents” work: target six
  to eight lanes, subject to the host's capacity and the task's true seams.

Use the host's native agent or delegation mechanism when it provides one. Do
not assume Claude-specific, Codex-specific, or vendor-specific tool names. Pass
the evaluation packet and raw artifact access, not the builder's explanation or
another reviewer's conclusion.

Keep reviewers independent:

- Give each lane a different question and a fixed report schema.
- Start independent lanes from the same revision whenever possible.
- Keep critics read-only. Give implementation work to one coherent owner or
  to builders with disjoint, explicit write scopes.
- Do not let later reviewers inherit earlier scores, preferred solutions, or
  the coordinator's diagnosis before they have inspected the artifact.
- If the host cannot supply the target number of agents, use every available
  independent slot, record target versus actual, and disclose the shortfall.
  Do not pretend that a missing reviewer ran.

If no real delegation interface exists, run separate clean-room passes in the
same agent: reset to the packet and artifact for each lane, suppress prior
findings, and label the result as sequential internal review rather than
independent-agent verification.

## Dispatch the panel

Assign the following roles as the default panel. Combine roles only when the
task is genuinely small; add an alternative-builder lane when a design or
architecture choice is material.

| Lane | Question to answer |
|---|---|
| Acceptance judge | Does the candidate satisfy every stated requirement, and which requirement is not proven? |
| Domain specialist | Is the work technically, visually, factually, or commercially sound for its domain? |
| Adversarial critic | How could a real user, edge case, attacker, competitor, or skeptical reader break it? |
| User/journey judge | Can the intended audience understand and complete the real task without hidden help? |
| Evidence verifier | Do the tests, renders, sources, calculations, and observations actually support each claim? |
| Risk/integration judge | What regressions, boundary failures, accessibility, performance, security, or production-fit problems remain? |
| Alternative builder | Is there a materially stronger approach, and does it beat the candidate under the same rubric? |

Require every reviewer to return this exact shape, even if the answer is a
pass:

```text
Evidence inspected:
Criterion verdicts: PASS / FAIL / UNKNOWN for each relevant criterion.
Findings: concrete failures or risks, with severity and reproduction evidence.
Largest remaining gap: one highest-impact unresolved issue.
Smallest high-leverage correction: exact target to change or test next.
Uncertainty: missing access, weak evidence, or assumptions.
```

Make every reviewer try to falsify the candidate. “Looks good,” a high score,
or agreement with the builder is not a finding. A PASS without current
artifact-level evidence is UNKNOWN, not success.

## Adapt the panel to the artifact

Select evidence that can be inspected directly. Use this matrix as a minimum,
then add task-specific lanes:

| Artifact | Minimum distinct checks | Useful proof |
|---|---|---|
| Software or API | contract/spec, tests and failure paths, security/performance, user/API integration, fresh regression review | acceptance tests, focused tests, static checks, reproducible commands, logs, diff review |
| Website or UI | visual desktop/mobile, real journey and conversion, accessibility/responsive, content/SEO, forms/provider boundary | rendered screenshots, route and form exercise, accessibility scan, metadata/source trace, network result |
| Design or collateral | brief fidelity, hierarchy/readability, brand/system fit, production/export correctness, first-impression challenge | final export, dimensions, colour/type checks, print or platform preview, blind comparison where practical |
| Writing | brief and structure, factual/source accuracy, audience reading, tone/editing, risk and continuity | final text, primary-source trace, claim map, fresh-reader critique, line-level continuity pass |
| Research or analysis | source quality, method and calculations, counterevidence, decision usefulness, uncertainty | primary sources, reproducible calculations, assumptions, competing interpretation, bounded conclusion |
| Data or automation | schema and input assumptions, deterministic behaviour, failure/retry paths, permissions, observability | fixtures, dry runs, logs, idempotency checks, permission boundary, rollback or recovery evidence |
| Game or interactive build | playable loop, usability/fun, technical/performance, edge/balance, platform/integration | real build, observed playthrough, profiling, failure cases, input/device checks, reference comparison |

For a reference-based comparison, hide labels and randomise order when practical.
Otherwise state exactly what the reviewer saw; never call a labelled comparison
blind.

## Reconcile evidence and improve

After the independent reports arrive:

1. Verify that each report names real evidence and the correct revision.
2. Separate facts, interpretations, preferences, and missing evidence.
3. Deduplicate findings, but do not erase corroborating evidence.
4. Resolve disagreements by returning to the artifact, primary source, or
   reproducible check. Do not decide factual questions by majority vote.
5. Rank gaps by impact on the objective, not by how easy they are to fix.
6. Select one coherent, high-leverage correction and one owner. Keep coupled
   changes together; do not fan them out just to create activity.
7. Re-run the relevant verifier, then give the changed artifact to a fresh
   adversarial panel. Do not reuse a stale approval after a material change.

If the same hypothesis fails twice without new evidence, change the strategy:
reduce it to an observable sub-problem, use a different verifier, test an
alternative implementation, or state the precise blocker. Repeating the same
prompt or patch is not persistence.

Keep external, destructive, or consequential actions behind their existing
approval gates. Prepare a preview, test, or evidence pack, then pause before
deploying, publishing, spending, deleting material data, changing a live
provider, using sensitive credentials, or contacting someone.

## Final integration gate

Call the work complete only when all of the following have current evidence:

1. Every requirement and non-negotiable has a PASS, not UNKNOWN.
2. No critical or high-impact finding remains unresolved.
3. The real artifact works as a whole after the changes, not only in isolated
   lanes.
4. A fresh integration judge has inspected the candidate and its proof without
   relying on the builder's confidence.
5. The panel target versus actual count and any unavailable evidence are stated.
6. No safety, scope, permission, or approval boundary was crossed.

If a boundary, capacity limit, or missing artifact prevents that gate, report
the result as `paused`, `blocked`, or `awaiting approval`, never complete. State
the last verified result, the remaining gap, the evidence still needed, and the
exact next safe action.

## Portability rules

Keep the workflow provider-neutral:

- Use plain Markdown instructions and capability-based language.
- Let each host map “dispatch a lane,” “read the artifact,” and “return the
  report” to its own native interfaces.
- Do not require a Claude command, a Codex command, a particular SDK, an API
  key, or a provider-specific orchestration file.
- Treat a host with no delegation support as limited, not as equivalent to a
  genuinely independent panel.
- Preserve the same packet, report schema, evidence standard, and completion
  gate across hosts.

If the user asks only for a panel plan or prompt, return the packet, lane
assignments, and completion gate. Do not claim that agents ran or that the
artifact improved.
