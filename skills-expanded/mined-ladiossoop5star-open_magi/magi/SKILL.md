---
name: magi
description: Use when the user asks for magi, Open-Magi, @Open-Magi, deliberation, three sages, or multi-agent research
---

# Magi

## Herdr Magi Activation Hard Gate

When user explicitly asks to start/use Magi for a repository/project and
`HERDR_ENV=1`, apply this before any other action: before repository/project
read/search, other reference loading, state/checklist creation, runtime
bootstrap, or pane split/agent launch.

From the already-current working directory, without search, perform exactly one
initial `lstat` of exact absolute `<current-cwd>/.open-magi-herdr`. Its single result
determines `ENOENT` versus existing and supplies owner, type, and mode metadata.
On `ENOENT`, the next/only and first user-facing action directly asks for exact
`melchior`, `balthasar`, and `casper` commands. This is direct pre-activation:
`state.active` is not set and `question-request.md` is not created.

Before asking, do not search other directories/repositories, `.open_magi`, HOME,
filesystem, PATH, runtime/native configs, agent names, prior reports/history,
or standard commands. No Herdr/Git call, `find`/`rg`, fallback, or inference.
The existing branch must reuse the returned metadata; no second `lstat` or
existence check is allowed before asking or parsing. Only a proven owned regular
file with valid mode may be read/parsed. If it shows a symlink, non-regular
entry, foreign-owned entry, or unprovable owner, do not read or mutate it. With
ownership, type, permission, format, role, or command invalid, the next/only
action is to ask immediately with the direct user question, with zero other
action; search nowhere else.

Only after the user answers may it atomically write/update owner-only `0600`,
apply exclusion, and revalidate (a later `lstat` is allowed here). Only after local validity may it
run `herdr pane current --current`, load `references/herdr.md`, explore, create
state/checklists, bootstrap, split panes, or launch agents.

## Overview

Run a coding-agent proposal-first loop. Main owns decisions, edits, verification,
commits, rollback, and reporting; three read-only deliberators research.
Completion requires `acceptanceCriteria`, `verificationCommands`, and review
approval of the diff before `final-report.md`. Before selection, the
main agent prepares an evidence packet and does not propose a fix; deliberators propose,
then review the selection. Track `recon`, `decision`, or `review` in
`currentCouncilMode`.

## Required Reference Loading

Load each before its situation:

| Situation | Required reference |
|---|---|
| Start/resume Magi | `references/protocol.md` |
| Checklist creation/phase change | `references/checklist-template.md` |
| Prompt/report/synthesis/verdict writing | `references/deliberation.md` |
| Subagent launch/runtime adapter behavior | `references/runtime.md` |
| Herdr launch/reuse/cleanup | `references/herdr.md` |
| User-facing question | `references/question-firewall.md` |
| Execute/verify/checkpoint/rollback evidence | `references/execution-and-verification.md` |
| Plugin repair/corrupt state/timeout/repeated failure | `references/troubleshooting.md` |

## When to Use

Use this skill when the user says `start deliberation`, `magi`, `three sages`,
`deliberation loop`, `loop until done`, or requests repeated research ->
synthesize -> act -> verify until completion.

Do not use it for small one-shot answers.

## Roles

Main extracts the goal, criteria, and verification; writes artifacts; launches
three deliberators; synthesizes; edits, commits, and rolls back.

Sub-agents:
- `deliberator-melchior`: practical engineering feasibility and edge cases.
- `deliberator-balthasar`: architecture, maintainability, long-term design.
- `deliberator-casper`: debugging, root cause, failure paths.

Use these names in reports. Sub-agents only report analysis to the main agent:
no edits (except a Herdr sage's assigned report per `references/herdr.md`),
build/test/format/deploy commands, or final user answer.

## Runtime State

State file: `.open_magi/magi-log/state.json`.

Before first research, create complete `schemaVersion: 2` state using the schema
and artifact layout in `references/protocol.md`.

Outside Herdr, the runtime adapter owns `inFlight`, `inFlightSince`,
`lastPromptedRound`, `lastPromptedAt`, `activeDeliberators`, and
`deliberatorTimeoutCounts`; the main agent cannot set `inFlight=true`. In Herdr
only, the main agent/controller owns them per `references/herdr.md` and may set
`inFlight=true` itself.

Use atomic complete writes where possible; never leave partial JSON.
`goal_definition` is only valid for initial setup. currentRound > 1 must never use `goal_definition`; resume later rounds at `status_assessment`.
Reproduction commands may be declared in `baselineCommands`; guards allow them
outside execution, but code edits stay execution-only.

## Phase Transition Checklist Gate

Create `.open_magi/magi-log/checklist.md` immediately after `state.json` using
`references/checklist-template.md`.

Before every phase transition, read `.open_magi/magi-log/checklist.md`, verify
the current transition section item by item, and only then update
`state.json.currentPhase`.

The checklist is a required runtime artifact, not optional documentation. Its
universal gate includes:
- `question_classification` was completed before any user question.
- No procedural question was asked; all procedural choices followed the Magi contract.

If a deliberator does not return a usable result, still write that
deliberator's `report-*.md` file with failure evidence and a blocking question
instead of omitting the file.

## Report Integrity Gate

Before ending a turn while `active=true`, verify log files match state:
- `research_task` has `round-NNN/research-prompt.md`.
- Round 1 at `research_task` or later has `round-NNN/recon-001/prompt.md`, all
  three recon reports, and `round-NNN/evidence-base.md`.
- Synthesis or later has all three current council reports.
- `synthesis` or later has current `synthesis.md`.
- Review pass 2 or later has `round-NNN/direction-selection.md`.
- `ready_for_verdict`, `execution`, or later has `verdict.md`.
- Any executed command has `verification.md` with command, exit code, and important output.
- `completion_review` has `round-NNN/cleanup.md`, `review-001/prompt.md`,
  and all three review reports; closing adds `round-NNN/review-verdict.md`
  with `outcome: approved` and `verdict_adherence_confirmed: yes`.
- Satisfied acceptance criteria have an approved review verdict and
  `final-report.md` before `active=false`.

After writing each artifact, update `state.json`. Set `needsContinue=true`
whenever work remains. Never end with `active=true`, a non-terminal
`currentPhase`, and `needsContinue=false`.

## Council Pass Gate

Use bounded multi-pass proposal-first deliberation in `decision` mode before
editing code or running verification. State fields are
`currentDeliberationPass` and `maxDeliberationPasses`.

Rules:
- `maxDeliberationPasses` defaults to and has a minimum of 3; maximum is 5.
  Proposal-first needs proposal, review, and refinement/decision capacity.
- Effective veto passes are `maxDeliberationPasses - 2`.
- Pass 1 is the proposal pass. Deliberators propose directions from the
  evidence packet. Pass 1 is not a veto pass.
- After Pass 1, the main agent writes `round-NNN/direction-selection.md` with
  the selected direction, rejected alternatives, and verification pressure.
- Pass 2 starts veto review of the selected direction: any `stance: oppose`,
  `stance: needs_evidence`, or `blocking_objection: yes` requires another pass
  unless `maxDeliberationPasses` has been reached.
- From Pass 2 onward, write a verdict only when at least two of three
  deliberators support the same executable plan, no new high-risk blocking
  objection exists, and a clear verification plan exists.
- At `maxDeliberationPasses`, do not ask the user for direction. Choose the
  smallest reversible verifiable diagnostic or modification, write it into
  `verdict.md`, and continue.

Do not ask the user whether another council pass is needed. The gate decides.

## Cleanup and Completion Review Gates

Before the completion claim, set `currentPhase=cleanup`: split the round's
full diff into fix changes and supporting changes; verify each fix change one
by one and remove the rest, list supporting changes for the review council,
re-run verification, and write `round-NNN/cleanup.md`.

Then run one adversarial review pass per `references/deliberation.md`: set
`currentPhase=completion_review` and `currentCouncilMode=review`, write
`round-NNN/review-001/prompt.md` with the actual diff (never a summary),
launch all three deliberators, then write `round-NNN/review-verdict.md`.
`final-report.md` requires `outcome: approved` and
`verdict_adherence_confirmed: yes`; then squash the loop's checkpoint commits
into one, re-run verification, and write `final-report.md` with
`squash_commit: <hash|none>`; then Set `currentPhase=complete` and
`active=false`. An objected review starts the next round.

## Procedural Autonomy Gate

Do not ask procedural questions. If the answer is defined by the Magi skill,
checklist, `state.json`, phase contract, log layout, role table, or report
format, execute the defined action and write the required artifact.

Forbidden procedural questions include:
- whether to write report files;
- which role each deliberator should play;
- whether to launch all three deliberator subtasks;
- whether to use one shared research prompt;
- where report files should be written;
- whether to create `synthesis.md`, `verdict.md`, or `verification.md`;
- whether verification failure should start the next round;
- whether another council pass is needed.

When unsure about a procedural step, read `checklist.md`, this skill, and the
required reference, then do the specified action. Do not convert procedural
uncertainty into a user question.

## Before Asking User Gate

Before asking, apply `question_classification` per the question firewall.
`procedural` is forbidden. `goal_ambiguity` and `debug_direction` are first-round
only; ask unresolved `execution_blocker`, `destructive_or_unrelated_risk`, or
`ambiguous_file_ownership` questions only in their allowed phases. Otherwise do
not ask; execute the next step and record the decision.

## Question Request Firewall

During an active loop, never ask directly. Read
`references/question-firewall.md`, then write `question-request.md` with its
required fields. If the plugin writes `question-denied.md`, do not repeat the
question; choose the safest verifiable local action, record it, and continue.

Allowed requests are limited to first-round `goal_ambiguity`, first-round
`debug_direction`, `execution_blocker`, `impossible_verification`,
`destructive_or_unrelated_risk`, and `ambiguous_file_ownership`. `procedural`
is always denied.

## Debug Direction Gate

Direction questions are allowed only during first-round Phase 1, before
execution starts. During first-round status_assessment, ask only for missing
constraints that cannot be inferred from the repository, logs, tests, or user
goal.

From Phase 2 onward: Do not ask the user which debug direction to try next.
The main agent must choose the next debug direction from evidence, reports,
verification output, and acceptance criteria.

The only allowed questions after Phase 1 are:
- verification is impossible because required hardware, credentials, network,
  devices, or external services are unavailable;
- an execution blocker prevents progress and cannot be resolved from local context;
- proceeding would risk destructive or unrelated changes.

If none of those exceptions apply, write the chosen direction into `verdict.md`,
execute it, verify it, and continue the loop.

## Checkpoint Commit and Rollback Gate

If Phase 5 changes code:
- run the build or compile verification before runtime verification;
- if build succeeds, create a local git checkpoint commit before continuing;
- stage only files changed by the main agent for this round;
- do not stage `.open_magi/` runtime logs or unrelated user changes;
- use a message like `magi: round-NNN checkpoint - <summary>`;
- write its hash into `round-NNN/verification.md`.

If build fails:
- do not create a checkpoint commit;
- write the build command, exit code, and important output into `verification.md`;
- record that the next round must revert this round's uncommitted code changes
  before writing the next `research-prompt.md`.

If build succeeds but later runtime verification fails, keep the checkpoint
commit and pass the hash plus failure evidence to the next round. The next
`verdict.md` must choose either continue from the checkpoint or revert the
checkpoint commit.

## Round Transition Gate

When a round fails and the goal is still incomplete:
- append the Phase 6 history entry with failure and diagnostic evidence;
- include `progress: true|false`;
- increment `currentRound`;
- reset `currentDeliberationPass=1`;
- reset `deliberationStatus=not_started`;
- reset `currentCouncilMode=decision`;
- set `currentPhase=status_assessment`, not `goal_definition`;
- set `needsContinue=true`;
- clear `inFlight` and `inFlightSince`.

If build failed before a checkpoint commit, revert this round's uncommitted code
changes before the next Phase 2 research prompt.

Phase 1 in later rounds is a short status check only. Phase 2 only writes the
next prompt artifacts. Do not perform extended single-agent debugging between
failed verification and the next deliberator pass.

## Six Phases

0. Goal Definition: infer or define goal, `acceptanceCriteria`, and
   `verificationCommands`; inspect relevant project context; write initial
   `state.json` and checklist.
1. Status Assessment: compare criteria, latest `verification.md`, and current
   filesystem. Round 1 splits into Phase 1a minimal scoping (main agent writes
   `recon-001/prompt.md`, no deep-dive) and Phase 1b parallel recon (all three
   deliberators investigate read-only; main agent writes `evidence-base.md`).
   Recon is repeatable in any round (`recon-MMM`, at most 3 per round); after
   a failed round, the next round starts with a recon pass carrying the
   failure evidence. While a recon pass is in flight, never write the decision
   council prompt or the verdict.
2. Research Task: write `round-NNN/research-prompt.md` (round 1 draws from
   `evidence-base.md`) and `round-NNN/council-PPP/prompt.md`; for pass 1 this
   is an evidence packet, not a proposed fix; for pass 2+ include
   `direction-selection.md`.
3. Parallel Deliberation: start all three configured deliberator subtasks with
   the same prompt and write all three `report-*.md` files. Pass 1 reports are
   direction proposals; later reports review the selected direction.
4. Synthesis and Decision: write current `synthesis.md`; apply Council Pass
   Gate; after pass 1 write `direction-selection.md`, otherwise start another
   pass or write `verdict.md`.
5. Execute and Verify: only the main agent acts; apply verdict, build, checkpoint
   if build succeeds, verify, run fail-only diagnostics if needed, and write
   `verification.md`.
6. Goal Check: judge acceptance criteria; on a completion claim run the
   Cleanup Gate (`cleanup.md`), then the Completion Review Gate
   (`completion_review` phase, review council, `review-verdict.md`); complete
   only on `outcome: approved`, otherwise continue next round, or block only
   after the no-progress limit.
