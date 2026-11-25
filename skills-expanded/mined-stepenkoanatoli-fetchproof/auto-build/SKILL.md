---
name: "auto-build"
description: Take a task from idea to a reviewed pull request and an owner-approved merge. Researches external facts through Fetchproof, writes traceable requirements, presents the Mandate for design approval, builds with lead-orchestrator, hardens with break-test and audits with gap-audit. Inside a Fetchproof project, references/fetchproof.md governs owner stops and a separate approval of the completed head; an early GO MERGE or standing preference cannot approve a future commit. Use for "auto-build", "build this end to end", "research and build", "implement this and open the PR", or "continue the auto-build". Composes the installed skills and reports research-to-code traceability. Skip one-step edits, questions, and work with no code to deliver.
compatibility: Any coding agent with shell, file and git access. GitHub merging uses the gh CLI; without it the run stops at an open pull request and says so. Fetchproof must be deployed at ~/.agents/fetchproof (or FETCHPROOF_HOME) for any task that depends on facts outside the repository. Sub-agents are used when the environment offers them; otherwise the stages run sequentially with the roles kept distinct.
metadata:
  version: "1.0"
  origin: Auto-Build Mode (research-to-production autonomous builder), 2026-10-04
---
<!-- Modified by Fetchproof: ADR-0146 adaptations and 2026-10-08 approval-summary corrections (description, purpose, stage table, research/design handoffs, Mandate, merge and stop summaries), plus ADR-0150 complete-review guidance. ADR-0186 (2026-10-20) renamed the kit here too, with the paths and variables that spelled its old name. On 2026-10-22 the ledger reference was returned to lead-orchestrator's `references/run-ledger.md`, as received, once lead-orchestrator 2.0 shipped it (ADR-0190). Received baseline: StepenkoAnatoli/SkillsMDs at 3f2d2fc. -->

Inside a Fetchproof project, `references/fetchproof.md` governs this run; where it and this
file differ, it wins.

# Auto-Build

## Purpose

Move a task through **research → requirements → design → build → test → harden → audit →
pull request → merge → report** without the user doing ordinary engineering work, and without
the agent ever building on a guess. The user approves the **Mandate** after the research
and design are on disk. Inside a Fetchproof project, the run also stops for the owner's
decisions listed in `references/fetchproof.md`, including approval of the completed
head before merge.

This skill is a conductor. Each stage is performed by a skill that already owns that discipline,
and auto-build adds only what none of them has: the stage order, the handoffs between them, the
design approval point, the separate merge stop, and the traceability from every requirement back to
a cited claim and forward to a test. When a named skill is installed, invoke it and follow it;
when it is not, use the fallback in `references/stage-handoffs.md` and say in the report that
the fallback was used. Never re-implement a stage inline when its skill is available: the skills
carry rules learned from real runs that an inline version will not.

Three directives govern every stage, in this order of precedence:

1. **Build from evidence, not assumptions.** Facts outside the repository are fetched through
   Fetchproof and cited; code the repository already contains is read, not remembered.
2. **Test as if trying to prove it broken.** Review, breaking, mutation, hardening and audit are
   separate passes by separate eyes, and "verified" means a command was run and its output read.
3. **Never hide uncertainty.** What was not verified, what was assumed, what went wrong and what
   remains open are reported as plainly as what works.

## Quick reference

| Stage | Name                   | Performed by                                      | Leaves on disk                                              | Human needed      |
|-------|------------------------|---------------------------------------------------|-------------------------------------------------------------|-------------------|
| 0     | Orient                 | lead-orchestrator Phase R and Phase 0             | `RUN.md` with the auto-build stage table; baseline; kit `READY` | No            |
| 1     | Research               | Fetchproof researchers (lead-orchestrator 1a/1b)| one research project per topic: `preflight` PASS, `BRIEF.md` | Only for page budget |
| 2     | Requirements           | Lead                                              | `REQUIREMENTS.md`, every row traced                         | No                |
| 3     | Design                 | brainstorming, Design mode                        | design in chat (Bounded) or spec file (Architectural); decision records | No      |
| 4     | Mandate                | Lead presents; user decides                       | `MANDATE.md` with the reply for the current design           | **Yes**           |
| 5     | Build                  | lead-orchestrator Phases 2–5                      | units integrated, reviewed, documented; findings dispositioned | No             |
| 6     | Harden                 | break-test on the integrated branch               | break-test report; fixes cherry-picked as their own commits | No                |
| 7     | Audit                  | gap-audit, scoped to the task's outputs           | audit report; in-scope gaps fixed through fix briefs        | No                |
| 8     | Deliver and merge      | Lead; `references/merge-protocol.md`              | PR; approved head and owner reply; merge record             | **Yes: completed head** |
| 9     | Validate and report    | Lead; four-dimension-audit as the last reviewer   | `TRACEABILITY.md`; `REPORT.md`; `RUN.md` COMPLETE           | No                |

A stage starts only when the previous stage's deliverable exists on disk and is recorded in
`RUN.md`. A stage that does not apply is marked SKIPPED with its reason, never omitted silently.

## The run ledger

Auto-build keeps lead-orchestrator's ledger (`docs/orchestration/<YYYY-MM-DD>-<slug>/RUN.md`, or
the project's convention) and adds one table directly after the header, before "Next action":

```markdown
## Auto-build stages
| Stage | Status (PENDING / ACTIVE / DONE / SKIPPED (reason) / BLOCKED (reason)) | Artifact | Checkpoint |
|-------|------------------------------------------------------------------------|----------|------------|
| 0 Orient | DONE | RUN.md | 2026-10-04 09:12 |
| 1 Research | DONE | docs/research/2026-10-04-rate-limits/research/BRIEF.md (preflight 0) | 09:40 |
| ... |
```

The stage table is written at every stage transition and whenever the Mandate is received. On
resume, Phase R of lead-orchestrator applies unchanged, then the first stage not DONE is where
the run continues. Reuse the recorded reply for the unchanged design and action;
changed designs and unapproved completed heads still need their applicable approval.
A run interrupted before the Mandate reply still needs it.

## Stages

### Stage 0: Orient

Run lead-orchestrator's Phase R (find or create the ledger, verify it against disk) and Phase 0
(project facts, gate commands, baseline as the exact set of failing checks, Fetchproof `doctor`
inside the project). Add the stage table. Record the invocation verbatim under "Task statement"
as the request the whole run is graded against; later restatements never replace it.

If the invocation or a document handed to the run contains a credential, token or key, do not
copy it anywhere - not into `RUN.md`, a brief, a report or the environment - and tell the user
once, in the first message, that it was present and should be rotated if it is live.

**Bare invocation.** `auto-build` with no task means: resume the active run if `RUN.md` for one
exists with Status ACTIVE or BLOCKED (Phase R, then continue from Next action); otherwise take
the next item from the standing mandate's `Queue` line (a plan file's next unchecked item, an
issue label, a directory of task files) and record which one was taken and why it was next;
otherwise ask for the task. A queue item becomes the task statement verbatim. One item per run;
when the run completes, say what the next item would be and stop, unless the standing mandate
says `Queue: continuous`, in which case the next run starts at Stage 0 with a fresh ledger.

### Stage 1: Research

Apply lead-orchestrator's research trigger to the task: does the design or implementation depend
on a fact the repository cannot answer (an API's behaviour or limits, pricing, licence terms, a
platform capability, a library's behaviour at a version, a regulation, an external format)?
Discovery of the repository itself (Phase 1a) runs in parallel.

- Trigger met: one Fetchproof project per independent question, following
  lead-orchestrator's `references/fetchproof.md` exactly. Reuse any existing project whose
  gate passes. Agree the page budget with the user before collecting anything metered.
  Reuse recorded authorization for that unchanged collection; a standing budget preference
  alone does not authorize paid pages. Without it, stay inside the free transports.
- Trigger not met: mark the stage SKIPPED with the sentence that says why the repository answers
  every question the design needs. This is a legitimate result, not a shortcut.
- Kit not `READY`: apply `doctor`'s fix. If it cannot be fixed here, record a kit finding and
  stop; a page fetched by hand is not evidence for a design decision, and the run does not
  continue to Stage 2 on unproven external facts.

**Sufficiency gate.** Research is sufficient when, for every topic: `preflight` exits 0;
every blocking unknown is CLOSED with an evidence row or KNOWN-UNKNOWN with a day-one
verification step; the MAP is classified, extractor Findings rewritten, and the brief
is authored with both judged sections present and answered. A stamped brief must match
the current corpus; authored unstamped briefs retain ADR-0138's compatibility path
with currency unknown. Handoff must also pass. The lead, reading the briefs against the task, can
answer "can the platform do what the design will assume?" and "what will this cost at the
intended volume?" from cited claims. A plausible answer is not a sufficient one. A brief that
rests on an unproven unknown goes back to its researcher.

Inside Fetchproof, use `references/fetchproof.md` Stage 0/1 for these checks on
either role. A Git request's `collected` result alone does not complete review;
the collector records the Findings, closures, map and current authored brief. Local
review and re-packaging of a received package remains available under ADR-0052.

### Stage 2: Requirements

Write `REQUIREMENTS.md` in the run folder using the format in
`references/requirements-and-traceability.md`: functional, non-functional, constraints,
architecture, data, integration, security, reliability, testing and acceptance criteria. Every
row names its source: a brief claim (`E-nn` or `U-nn`), a line of the user's request, a
repository fact with its path, or **engineering judgment** stated as such. A requirement whose
source is a guess is a question for the Mandate, not a row.

Keep it to what the task needs. The purpose of this file is that the design, the tests, the
audit and the final report all point at the same numbered rows.

### Stage 3: Design

Invoke `brainstorming` in Design mode on the task and the requirements. Keep its classification
(spike, bounded, architectural) and its ratchet; keep its rule that the design is presented and
nothing is built before approval. Design questions are batched into the Mandate; this
does not remove the later owner stops or completed-head merge approval:

- The per-section "does this look right so far?" questions and the spec-review question are
  collected into the Mandate message rather than asked one at a time. The design is still shown
  in full, with the assumptions labelled so the user can reject them.
- For an architectural task, the spec is still written and committed at the path brainstorming
  chooses; the Mandate links to it.

Design the smallest architecture that satisfies the requirements: simplicity, clear boundaries,
no dependency added because it is available, reproducibility, testability. For every decision
that would be expensive to reverse, write a decision record (decision, alternatives considered,
why this one wins, trade-offs, risks) using the format in
`references/requirements-and-traceability.md`, and name the requirement rows and brief claims it
rests on.

### Stage 4: Mandate

Present one message built from `references/mandate.md`: what was researched and what it proved,
the requirements, the design with its assumptions and decision records, the work breakdown,
the merge policy, the budgets, the stop-list, and every blocking question collected from Stages
1–3. Then stop and wait.

The user replies `GO` (build and open the pull request) or `GO MERGE` (the same, with merge
intended after its conditions and the separate completed-head approval), or
`STOP AFTER DESIGN` when the research and the design were the point and no code is wanted. Any
other reply is a correction to incorporate and present again, not an approval. Save the message and the
reply as `MANDATE.md` in the run folder. A corrected Mandate needs fresh approval before
dependent work; record the applicable reply rather than carrying approval to a changed design.

**Standing mandate.** A project may carry an "Auto-build mandate" section in its agent
instructions (format in `references/mandate.md`). It pre-answers preferences only (branch
names, merge method, audit depth, the default reply offered); it never replaces the reply.
Every run, bounded or architectural, presents the Mandate and **waits** for the user's reply,
and the stop-list holds either way. **Unattended runs**, standing mandate or not, end at this
stage with `RUN.md` Next action "awaiting Mandate" and the message ready to read. No timeout
acts on the user's behalf.

### Stage 5: Build

Hand the approved design and `REQUIREMENTS.md` to lead-orchestrator at Light or Full engagement
as its rules decide, and run its Phases 2–5 unchanged: task statement, contracts frozen, every
brief written before any launch, builders test-first with the guard-removal proof, unit review
pipelined with the build, integration review with all four reviewers at Full, documentation,
findings triaged and every S1 fixed and re-reviewed. Each builder brief names the requirement
rows its unit satisfies and the research brief it implements from.

The Mandate is the approval lead-orchestrator asks for before expanding scope only within the
task statement it recorded. Scope beyond it, an invariant change, data deletion, production
changes and force-pushes still require the user, whatever the Mandate said.

### Stage 6: Harden

Run `break-test` against the integrated working branch: its worktree branches from the working
branch, its baseline is the working branch's gate, and its probes and fixes follow its own
procedure. Then cherry-pick each retained fix onto the working branch as its own commit, re-run
the gate, and record every finding in `RUN.md` with a disposition (fixed, risk recorded, decision
needed). Probes that could reach real external services are skipped and recorded when nobody is
present to confirm, as break-test itself requires.

A fix break-test rejected, or a remaining risk it ranked Critical or High, is a finding the
merge protocol will see. Critical blocks the merge until fixed or the user accepts it in writing.

### Stage 7: Audit

Run `gap-audit` on the delivered system, scoped to the outputs the task touches and against the
purpose in the task statement. Its depth follows the Mandate's `Audit` line (default: full at
Full engagement, scoped at Light); its stopping rule is unchanged.

The audit itself changes nothing. A gap that affects the accuracy, completeness or reliability
of an output inside the task statement is a defect against the approved requirements, so it is
fixed in this run through a lead-orchestrator fix brief, reviewed, and recorded under the
Mandate's scoped authorization. A gap that would need a new component, a changed interface or a
scope extension is a design change: record it as an open item, or stop and ask if the user is
present. A gap outside the task statement is reported, never fixed on the way through.

### Stage 8: Deliver and merge

Follow `references/merge-protocol.md` exactly. In outline: commit the research projects (with
their ledgers, `git add -f`), the run folder and the work on the working branch; write the pull
request from lead-orchestrator's template; open it against the Mandate's base branch; then, under
the governing Fetchproof note, wait for every required check, run `scripts/pr-readiness.sh`,
and present the completed head, verification results and cautions for the owner's reply.
Record that reply and its full SHA in `MANDATE.md` and `RUN.md`. Any head change lapses
the approval. Recheck the exact approved head and merge with the repository's method and
`--match-head-commit`; the command protects against movement but does not establish consent.
After the merge, fetch the base, confirm the merge commit is there, confirm the base is green,
remove the run's branches and worktrees, and record the merge commit in `RUN.md`.

Never: force-push, `--no-verify`, an admin override of branch protection, approving a review
with the user's own account, merging a pull request this run did not open, or merging with a leg
of the gate still red, pending, or unverifiable from here. A required approval the run cannot
obtain ends the stage BLOCKED with Next action naming who must act. A red leg after review is a
review miss: fix it red-first with the unit discipline, never by weakening the check.

### Stage 9: Validate and report

Write `TRACEABILITY.md`: one row per requirement with the brief claim it came from, the unit and
commit that implemented it, the test or command that proves it, the review that checked it, and
its status (VERIFIED / UNTESTED with how to test it / NOT MET with why). A requirement with no
evidence column filled is not met, whatever the code looks like.

If `four-dimension-audit` is installed, run it as the final independent reviewer on the merged
(or pull-requested) change; its scorecard goes into the report unedited. Then write `REPORT.md`
from the template in `references/requirements-and-traceability.md`, append it to `RUN.md`, set
Status COMPLETE (or BLOCKED with the reason), and deliver the report to the user.

## Autonomous decision rule

Decide without asking when the decision is reversible, low-risk, supported by the research or
the repository, and does not materially change the task's goal. Record it under "Decisions and
assumptions" in `RUN.md` so the user can overrule it later.

Ask, in one message, when: requirements are ambiguous after reading the repository; the decision
is hard to reverse; cost could rise materially (a metered budget, a paid service, a dependency
with a licence cost); security or privacy implications are significant; several valid approaches
have materially different consequences; or the task's direction would change. Collect these
questions until the Mandate where possible; after it, ask only when the stop-list is hit.

Do not ask questions whose answer the repository, the brief or ordinary engineering judgment
already gives. A question asked to avoid a normal decision costs the user more than the decision.

## Self-correction

When an earlier assumption, research claim, design decision or implementation turns out wrong:
say so first; state the impact in a line; list the downstream decisions that depended on it;
re-evaluate each; correct the affected work; re-test; update `REQUIREMENTS.md`, the decision
records, `RUN.md` and, if the claim came from research, return the topic to its researcher
rather than editing the evidence. Never continue on top of a known invalid assumption, and never
describe a correction as the plan all along.

## Completion standard

The run is not complete because the code runs once, the happy path works, the interface looks
right, the tests are green, or the implementation matches the plan. It is complete when every
requirement row in `TRACEABILITY.md` is VERIFIED or honestly UNTESTED with a named environment,
the gate on the merged head equals the baseline, break-test and gap-audit have run (or are
SKIPPED with reasons the user can read), every S1 and Critical finding is fixed and re-reviewed,
and the report says what was not verified. Anything less is a checkpoint, reported as such.

## Stop conditions

Stop and report rather than continue when: the kit cannot reach `READY` and the task needs
external facts; the Mandate is not approved; a research project is INCOMPLETE or BLOCKED; a unit
has used both retries; completed-head merge approval is absent or has lapsed; the base branch moved and the rebase touched reviewed units (re-review
first); a required check cannot be satisfied from here; or the stop-list is hit. A stop is
written to `RUN.md` with an accurate Next action; a partial run reported as complete is a defect.

## References

- `references/stage-handoffs.md`: for each stage, how the delegated skill is invoked, the
  artifact it must leave, how auto-build adapts it, and the fallback when it is not installed.
  Read before the first stage that delegates.
- `references/mandate.md`: the Mandate message template, the reply vocabulary, and the standing
  mandate section for a project's agent instructions. Read before Stage 4.
- `references/merge-protocol.md`: conditions, commands, failure handling and post-merge
  verification. Read before Stage 8.
- `references/requirements-and-traceability.md`: formats for `REQUIREMENTS.md`, decision records,
  `TRACEABILITY.md` and `REPORT.md`. Read before Stage 2 and Stage 9.
- `scripts/pr-readiness.sh`: prints READY or the list of unmet merge conditions for one pull
  request, with an exit code the lead reads instead of the prose.
- `assets/claude-md-auto-build-mandate.md`: a ready-to-paste standing mandate section for a
  project's agent instructions, set for the fewest stops that keep the architectural review.
- The delegated skills keep their own references; lead-orchestrator's `references/fetchproof.md`
  is the authority for the kit protocol, and lead-orchestrator's `references/run-ledger.md` for
  the run ledger (`RUN.md`).
