---
schema: skill/v1
id: project-picture
version: 1
title: Project picture
description: Build the best evidenced picture of a project from every source the worker can reach, local first, every source optional, with each claim tagged and sourced and every gap recorded.
status: draft
tags: [orientation, evidence, knowledge, coverage, read-only]
related: [repo-review, report-verification-state, evolve]
inputs:
  - "PROJECT: a repository, a set of repositories, or a name to resolve (default: the repository of the working directory)"
  - "SCOPE: paths or repositories to narrow to (default: all of PROJECT)"
  - "MODE: auto | local | global | offline (default: auto, detected, never asked)"
  - "BUDGET: wall-clock seconds and tokens for the whole run (default: 600 s; per source a tenth of it)"
  - "SINCE: the time window for activity (default: 30 days; history before it is summarised)"
  - "DEPTH: quick | standard | deep (default: standard)"
outputs:
  - the picture in Markdown, sections as in Output
  - the same picture as JSON with the same structure
  - a coverage ledger with one row per source tier and adapter
  - proposed records (knowledge candidates, questions, a handover body), written only when asked
---

# Purpose

Establish what is true about a project now, from every source this worker can reach, and say
exactly which sources it could not reach. The result is a picture that a person or the next
worker can act on: what the project is, where it stands, who waits on whom, what contradicts
what, and the few acts with the most leverage.

This is not a code review (`repo-review`), not an estimate, and not a fix. It sends nothing,
changes nothing outside the records allowed in stage 11, and never asks for a login.

# When to use

- entering a project cold, or resuming one after a gap longer than its stale threshold;
- before a status report, a planning call or a hand-over to another person;
- when sources are suspected to disagree: the plan, the forge, the tracker and the conversations;
- across all projects of a machine or a workspace (MODE global).

# Contract

1. **Read-only.** No message, comment, reaction, issue edit, transition, push, merge, rerun,
   cancel, deploy or publish on any system. The only writes are those in stage 11.
2. **Every source is optional.** Each one is probed before it is read, has a timeout and a share
   of BUDGET, and on failure (absent, unauthenticated, rate-limited, offline, denied) becomes a
   coverage row with the reason. A run with only the tree still yields a picture. Ask the
   shared server first (its MCP or HTTP surface answers the board, the brief and the plan from
   memory). A command line call that exceeds its share becomes a `partial: timed out` row; it
   never stalls the run. Some calls are slow on a large repository: `plan next`, `doctor`, and
   an integration-queue status.
3. **Local first.** Finish tiers T0 and T1 before any network call. With MODE offline, or when no
   network answers, stop after them and say so.
4. **Never mutate the checkout to read it.** Read trunk with `git fetch` and
   `git show origin/<trunk>:<path>`. Never merge, rebase, stash, switch or clean. The one write
   this skill allows itself is the dry-run merge of stage 6: `git merge-tree --write-tree` adds
   unreferenced tree objects to `.git` and moves no ref.
5. **Precedence.** The tree (git and files) outranks `.ai/` records. Records outrank forges and
   trackers. Those outrank conversations. Memory and recalled notes rank last and are
   re-verified before use. A higher source wins only after the contradiction is recorded.
6. **Confidentiality.** Apply the repository's confidentiality rules to the output. Label every
   finding with its audience (internal, shared-with-external, unknown). Summarise conversations
   and do not copy them. Redact personal data. Report a secret as "exposed at <locator>,
   rotate" and never reproduce it. Never place a value in a command line or a URL.

# Procedure

Detect the mode first: `.ai/manifest.yaml` present means supervised; absent means
unsupervised (never `majordomus init`). If PROJECT names several repositories, or there is no
repository, the mode is global. Then run the stages in order. DEPTH quick runs stages 1–5, 10
and the Output; deep follows every edge one hop further.

## 1. Discover what this installation can answer

Run `majordomus version`, `majordomus --help` and `--help` for every subcommand named below.
In addition, list the capabilities the server projects, if one serves this checkout. Find the
adapters with `command -v` (code-host CLIs, tracker CLIs) and the tools the session can call,
and find token variables by name only. Every command that this probe does not show is a gap
row, not an error. Record the Majordomus version in the picture.

## 2. T0: the tree

`git status`, `git branch -a`, `git worktree list`, the log over SINCE, tags, remotes,
`git stash list`, rescue refs, and ahead/behind against the remote trunk. Read the README,
docs index, status/roadmap documents, manifests and CI configuration from trunk. Note any
local uncommitted work and unpushed branches as risks; do not touch them.

## 3. T1: Majordomus state (supervised only)

`majordomus context`, `majordomus handover --resolve` (a stale handover is context, not an
instruction), `majordomus brief`, `majordomus history`, `majordomus decision list`,
`majordomus question list --all`, `majordomus plan status`, `plan next`, `plan blocked`,
`plan drift`, `plan delivery`, `majordomus adr list`, `majordomus rules list`,
`majordomus watch`, `majordomus worktree status`. Read the board and the mesh claims when the
server answers. Never read `.ai/local/` by hand.

## 4. T1: the knowledge graph

`majordomus knowledge search PROJECT` and the terms that stages 2–3 surfaced, then `knowledge
related <id>` outward from each hit, to the decisions, constraints and lessons they touch, and
`knowledge candidates` for what awaits review. Each node read is a source with its id.

## 5. T1: the `.ai/` layer by resolution

For each area the picture touches, run `majordomus context resolve <path>`, root first, so
that the rules and documents that apply are the ones the resolver chooses, never a hand-picked
subset. Note every rule that the picture's findings touch.

## 6. T2: forges

Probe each code-host CLI for authentication. Read the open issues and PRs/MRs, with their
checks, reviews, mergeability and age. Read the items closed and merged over SINCE,
milestones with due dates, CI and deploy runs on trunk, and releases. Dry-run a merge before
calling a PR clean (`git merge-tree --write-tree`).

## 7. T3: trackers

Use whatever CLI, connector or API token exists. Read the issues, epics, sprints and
worklogs that name PROJECT, and map their keys to the repository's keys (commit subjects, PR
bodies, plan records). Without access, use an offline export in the tree if one exists, and
say that you did.

## 8. T4: conversations

Read only channels, threads and direct messages that name PROJECT, within SINCE, including
the files and transcripts posted there. Mark any channel shared with an external party.
Extract commitments, dates, requirements, open asks and who they wait on.

## 9. T5: synced and global sources

Use other checkouts and worktrees of PROJECT, mesh nodes, published handovers, and documents
or pages linked from stages 6–8 (one hop, only when readable). In MODE global, enumerate the
repositories under the workspace root, resolve PROJECT to them, run stages 2–8 for each and
merge the results.

Stages 6–9 may run as parallel workers. Give each one a narrow, read-only brief, and have
each return findings in the shape below, not prose.

## 10. Reconcile and derive

- List every contradiction with both sides cited. Typical ones: an issue open while its work
  merged; a document that says "not built" while code exists; a plan that misses a scope
  agreed in a conversation; CI green while the deploy is red; a due date in the past.
  Before a contradiction is listed, read both sides at their locators yourself. A
  contradiction that a parallel worker returned is a lead, not a finding. A document's
  sentence is read whole: "X beyond Y is not built" does not contradict a merged Y.
- Re-verify, at the source, the two or three claims that the next actions depend on,
  including any claim a parallel worker returned.
- Derive: the critical path, who waits on whom, momentum (the last landing and what stopped
  it, if a source says), plan drift, release currency, and intent realization. Tag each one
  DERIVED with its derivation.
- Infer only what no source states. Tag it INFERRED with a confidence and what would confirm it.
- Draw one Mermaid diagram of the project's structure or flow from OBSERVED facts only.

## 11. Propose records (write only when asked, supervised, under a started task)

Propose, never write unasked, the following:

- knowledge candidates, through the commands `majordomus knowledge` provides;
- open questions, via `majordomus question add`;
- a handover body with `# Objective`, `# Current State`, `# Next Action`, for
  `majordomus handover`;
- stale records to fix and issues to open.

Never record a decision on anyone's behalf. Never write under `.ai/local/`. Never edit
between `majordomus:begin` and `majordomus:end`.

# Findings

Every finding carries these fields:

- `claim`
- `tag`: OBSERVED, DERIVED or INFERRED
- `kind`: fact, risk, contradiction, commitment, open-question or next-action
- `source`: the tier and adapter
- `locator`: file:line@sha, URL, issue id, message timestamp or record id
- `observed_at`
- `as_of`: when the source says it was true
- `confidence`
- `audience`

Intent is never written as status. An untraceable claim is dropped. "No source states it" is
a finding of its own.

# Output

Markdown and JSON with the same structure. Every section states its `as_of`, and is flagged
stale when its newest source is older than the repository's stale threshold.

1. **TL;DR**, five lines: what it is, where it stands, the biggest blocker, the next act, its owner.
2. **Identity**: repositories, remotes, owners, supervised or not, Majordomus version.
3. **Purpose**: intents and their stage, milestones, what "done" means here.
4. **State** per area, keeping "on trunk" and "in operation" apart: the trunk, released and
   unreleased work, CI and deploy health, open PRs/MRs, worktrees.
5. **Work**: in flight (board, claims, active tasks), next (`plan next`), blocked (with the blocker).
6. **Timeline** over SINCE, with dated, sourced events.
7. **People and peers**, by role from the board, mesh and sources, never guessed.
8. **Waiting**: on us, on them, on a decision (each decision with its owner).
9. **Risks and contradictions**, each with its evidence.
10. **Next actions**: three to five, ranked by what they unblock, each with an owner, evidence
    and the first command.
11. **Diagram**, Mermaid, from OBSERVED facts.
12. **Proposed records** from stage 11, marked as unwritten.
13. **Coverage ledger**: one row per tier and adapter. Each row states:
    - a state: `read` (at least one locator), `partial` (truncated by budget, pagination or a
      timeout), `skipped` (offline, or out of budget before it started) or `failed` (with the
      reason);
    - the elapsed seconds;
    - the locator count;
    - the newest timestamp the source held;
    - the time range covered.

    A row cannot claim coverage without evidence.

Every section has an evidence rule. A row with no locator is not printed. Use
`report-verification-state` for anything the picture claims was done. Depth means connected
and verified, not long.

# Compatibility

The commands named here were confirmed by stage 1's probe. Re-run that probe whenever the
installed version changes. A command it no longer shows becomes a gap row. A later version may
answer more (capabilities, intents, releases, delivery, gates), and the skill names those
commands only once a probe confirms them.
