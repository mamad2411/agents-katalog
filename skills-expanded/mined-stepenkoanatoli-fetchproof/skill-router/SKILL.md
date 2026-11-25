---
name: skill-router
description: Picks which skill to use next from facts on disk - this machine's role (doctor), whether the corpus arrived (handoff), the research gate (preflight) and the brief - and never sends a builder to a skill that collects evidence. Use at the start of any task in a Fetchproof project, after an interruption, when unsure which skill applies, or when the user says "which skill", "route this", "what next", "start building", "continue", or names a skill that may not fit this machine. Routes skills, not models - model choice stays with lead-orchestrator's rule.
---

# Skill router

Route by **facts the kit already reports**, then by the task. Never by the task alone: the
same request ("build X") means a different skill on a machine whose corpus has not arrived.

This skill guides; it enforces nothing. The gates - preflight, the commit gate and the
edit-time gate - stay the enforcement. No route here is a reason to bypass one: never
`--no-verify`, never a `research/GATE_OFF` file, never a hand-fetched page.

## Step 1: confirm the project, then read the state

Confirm the intended project before running diagnostics (AGENTS.md). If the working
directory is not that project, stop and ask which one; a verdict for another directory
is not this project's readiness.

```
node "$HOME/.agents/fetchproof/bin/doctor.mjs"          # role=collector|builder, in its last line
node "$HOME/.agents/fetchproof/bin/handoff.mjs"         # exit 0: the corpus arrived whole
node "$HOME/.agents/fetchproof/bin/preflight.mjs"       # PASS or FAIL
node "$HOME/.agents/fetchproof/bin/brief.mjs" --state   # template | legacy | draft | authored
```

Record the actual doctor verdict and role. An unresolved role or blocking diagnostic
is not readiness. A chosen keyless collector does not need Firecrawl (ADR-0095).

Building also needs the review that `lib/artifact.mjs` derives: classified MAP,
rewritten extractor Findings, and an authored brief with both judged sections present
and answered. For a stamped brief, its inputs must match the current corpus;
`brief.mjs --state` does not prove that match. An authored unstamped brief keeps the
existing approval path with currency unknown (ADR-0138). Handoff and PASS are also
required. These approval conditions are the same on either machine; the role controls
collection. A `collected` request result or BRIEF file presence alone proves none of
this review (ADR-0150).

## Step 2: route by state

| Role | State | Use |
|---|---|---|
| either | role unresolved or doctor reports a blocker | `resume-from-disk`; record the diagnosis and stop |
| collector | gate failing, or no map yet | `research-first`, then `map-classifier`, `finding-rewriter`, `source-grader` |
| collector | gate PASS, review incomplete or stamped brief stale | finish `map-classifier`, `finding-rewriter`, `brief-writer` as needed |
| collector | handoff and gate pass, review complete and brief current under ADR-0138 | build: the task table below; before a release, `freshness-recheck` |
| collector | the task is an audit, or "what to build next" | `gap-audit`, `subproject-discovery` |
| builder | handoff fails | `resume-from-disk`; quote the delivery or checkout diagnosis and stop |
| builder | no brief, incomplete review or stamped brief stale | report the review gap to the collector and stop; use `fact-request` only for a missing external fact |
| builder | gate failing | `resume-from-disk`; report the failing check; use `fact-request` only for a missing external fact, and stop |
| builder | handoff and gate pass, review complete and brief current under ADR-0138 | `build-from-brief` first, then the task table below |
| either | interrupted session, unclear state | `resume-from-disk` |

A builder never runs a collecting skill: `research.mjs` and `decompose.mjs` refuse there
(exit 2), and a page fetched another way is not evidence (ADR-0010). A missing fact is a
`fact-request`, never a fetch. When the collector runs auto-collect, the request is a file,
`research/requests/<id>.json`, and the collector collects it and pushes the result
(ADR-0148). The builder requests a fact; the collector validates the request, fetches,
and records Findings, closures, map classification and the current authored brief.
The builder reads and judges the returned captures and reports review-only gaps in
prose; those gaps do not need another fetch. ADR-0052 still permits local review and
re-packaging of a received package, without collection or edits to the collector's Git
corpus. On a collector too, use existing captures when they answer the gap.

## Step 3: route by task (once building is allowed)

The default build path is `build-from-brief` with `day-one-tasks`, `cite-in-code` and
`contract-tests`. `lead-orchestrator` is optional, for independent units that need parallel
agents, and is not part of the research-before-build core; when it runs, its builder briefs
carry the `cite-in-code` and `contract-tests` rules (lead-orchestrator's
`references/fetchproof.md`, section 5). `auto-build` runs through it, so it stays in the set
(ADR-0196).

| Task | Use |
|---|---|
| any code change | `careful-coding`, always |
| the shape of the work is open | `brainstorming`, then `build-from-brief` |
| the first steps of a build | `day-one-tasks` - the brief's known unknowns become the first tasks |
| a constant, endpoint, limit or schema field that came from the research | `cite-in-code` |
| tests that hold the code to the brief | `contract-tests` |
| multi-unit work, parallel agents | `lead-orchestrator`, optional, only for independent units that need parallel agents (on a builder, its Phase 1b becomes `fact-request`) |
| idea to merged pull request in one run | `auto-build`, run as its `references/fetchproof.md` says: Stage 0 starts from this table, on a builder its research stage becomes `fact-request`, and it asks the owner and stops at every decision that is his - the Mandate, money, secrets, anything destructive or critical, the merge |
| the structure of the diff just written | `architecture-pass` |
| friction across a subsystem | `improve-codebase-architecture` |
| will the build or CI break | `break-test` (on a builder, its Fetchproof step becomes `fact-request`) |
| grade what was built | `four-dimension-audit` |
| a decision set an alternative aside | `adr-writer` |
| committing | `commit-report` |

## Skill table

Every skill the kit ships, and where each may run. `Collects` is `yes` (the skill's
purpose is to collect or re-collect evidence), `stage` (one of its stages does) or `no`.
A `yes` skill is `never` on a builder; a `stage` skill runs there only with that stage
replaced by `fact-request`.

| Skill | Collects | Collector | Builder |
|---|---|---|---|
| research-first | yes | phase 1 | never |
| freshness-recheck | yes | before a build or a release | never |
| gap-audit | yes | an audit of a project's outputs | never |
| subproject-discovery | yes | choosing what to build next | never |
| map-classifier | no | after decompose | received-package local review only (ADR-0052); Git corpus records stay with the collector |
| finding-rewriter | no | after collect | received-package local review only (ADR-0052); Git corpus records stay with the collector |
| source-grader | no | after collect | received-package local review only (ADR-0052); Git corpus records stay with the collector |
| brief-writer | no | after the gate passes | received-package local review only (ADR-0052); Git corpus records stay with the collector |
| lead-orchestrator | stage | multi-unit work | multi-unit work, Phase 1b replaced by fact-request |
| auto-build | stage | idea to merged PR, per its references/fetchproof.md | idea to merged PR, per its references/fetchproof.md: research stage replaced by fact-request |
| break-test | stage | hardening a build | hardening a build, Fetchproof step replaced by fact-request |
| skill-router | no | always first | always first |
| resume-from-disk | no | after an interruption | after an interruption |
| fact-request | no | when a builder's request arrives (auto-collect answers a request file) | whenever a fact is missing; push research/requests/<id>.json |
| build-from-brief | no | after the gate passes | after the handoff and the gate pass |
| day-one-tasks | no | first build steps | first build steps |
| cite-in-code | no | while building | while building |
| contract-tests | no | while building | while building |
| careful-coding | no | any code change | any code change |
| brainstorming | no | open-shaped work | open-shaped work |
| architecture-pass | no | after a change | after a change |
| improve-codebase-architecture | no | structural review | structural review |
| four-dimension-audit | no | grading finished work | grading finished work |
| adr-writer | no | a rejected alternative | a rejected alternative |
| commit-report | no | every commit | every commit |

## Models

This router names no model and keeps none in configuration (ADR-0012). When a route
leads to delegated work, the model for each sub-agent follows `lead-orchestrator`'s rule:
the most capable model available, a faster one only where capability cannot affect
correctness, and on failure escalate the model first.
