---
name: kickoff-ready
description: "Sequence the ten ready-suite specialists for a greenfield project from raw user intent. Triggers on 'kickoff,' 'new project from scratch,' 'walk me through idea to launch,' 'help me ship it end-to-end,' 'orchestrate the whole arc,' 'I have an idea, what next.' Owns sequence decision, handoff invocation, progress ledger (`.kickoff-ready/PROGRESS.md`), resume protocol, skip-and-import detection. The only meta-tier skill; every other ready-suite sibling is downstream from this one. Refuses scope leak (writing PRD/architecture/roadmap/launch content the specialists own), rubber-stamp orchestration (advancing the ledger without verifying artifact on disk), phantom resume (claiming resume but starting fresh), ghost handoff (invoking a sibling without verifying upstream artifact), and happy-path orchestration (no policy for skip, re-invoke, import, or sibling failure). Does not produce specialist content; routes to prd-ready, architecture-ready, roadmap-ready, stack-ready, repo-ready, production-ready, deploy-ready, observe-ready, launch-ready, harden-ready. Greenfield only; existing-codebase migrations route to the relevant specialist directly. Full trigger list in README."
version: 3.1.0
updated: 2026-11-23
changelog: CHANGELOG.md
suite: ready-suite
tier: orchestration
upstream: []
downstream:
  - prd-ready
  - architecture-ready
  - roadmap-ready
  - stack-ready
  - repo-ready
  - production-ready
  - deploy-ready
  - observe-ready
  - launch-ready
  - harden-ready
pairs_with: []
compatible_with:
  - claude-code
  - codex
  - cursor
  - windsurf
  - antigravity
  - pi
  - openclaw
  - any-agentskills-compatible-harness
---

# Kickoff Ready

This skill exists to solve one specific failure mode. A user types "I have an idea, help me build and launch it." A general-purpose agent, faced with a blank page and ten installed specialist skills, does the easiest thing an LLM can do: it fills the blank page. It writes a PRD inline. It sketches an architecture in the same response. It dashes off a roadmap as a bulleted list. It picks a stack from training-data familiarity. It gestures at a launch plan. None of the ten specialist skills (prd-ready, architecture-ready, roadmap-ready, stack-ready, repo-ready, production-ready, deploy-ready, observe-ready, launch-ready, harden-ready) ever fires. The user gets a one-message project-in-miniature that fails every specialist's have-nots simultaneously.

kickoff-ready refuses to fill the blank page. Its only outputs are sequence metadata: a per-step record in `.kickoff-ready/PROGRESS.md`, an invocation per specialist (via the harness's Skill tool, or guidance text on harnesses without one), and a verification gate after each invocation that confirms the sibling actually wrote its artifact to disk. The skill is small by construction; if it grows, it has drifted into a sibling's lane.

This is the eleventh skill in the ready-suite and the only one in the meta-tier. The other ten are specialists; kickoff-ready is the conductor. The single load-bearing principle: kickoff-ready calls siblings; it never impersonates them. Research citations for every refusal name and every sequencing decision are in [`references/RESEARCH-2026-04.md`](references/RESEARCH-2026-04.md).

## Core principle: the orchestrator calls specialists; the orchestrator never impersonates them

The load-bearing discipline is that kickoff-ready's product is sequence and handoff metadata, not specialist deliverables. kickoff-ready enforces:

> Every step in `.kickoff-ready/PROGRESS.md` resolves into one of: a Skill-tool invocation of a specific sibling, a guidance string for harnesses without a Skill tool, a verification result against a specific `.{skill}-ready/<artifact>.md` path on disk, or a recorded user decision (skip, re-invoke, import). No step in PROGRESS.md is satisfied by content kickoff-ready produced.

This principle is non-negotiable. An AI-generated kickoff that responds to "I have an idea, help me ship it" by writing the PRD, the architecture, and the launch plan in the same conversation fails it on the first turn. The grep test: after kickoff-ready runs, the project's `.{skill}-ready/` directories are produced by their respective siblings, not by kickoff-ready. If kickoff-ready ever writes a `.prd-ready/PRD.md`, the boundary is broken and the suite collapses.

## Named failure modes the skill refuses

kickoff-ready inherits the ready-suite's naming discipline: a sloppy pattern gets a specific name the skill can refuse by name. These are the patterns; each maps to a citation in the research report.

- **Scope leak.** The orchestrator drifts into producing specialist content rather than invoking the specialist. kickoff-ready writes a PRD inline instead of calling prd-ready; sketches an architecture instead of calling architecture-ready; produces a launch checklist instead of calling launch-ready. The grep test for SKILL.md: any kickoff-ready output that is not (a) sequence metadata, (b) a Skill-tool invocation, (c) PROGRESS.md update, or (d) a one-paragraph guidance string for harnesses without Skill-tool support, is a scope-leak violation. Cited: production-ready/ORCHESTRATORS.md invariant 1; Praetorian on deterministic orchestration; the AgentOrchestra anti-pattern of supervisors becoming silent co-authors of worker output.
- **Rubber-stamp orchestration.** PROGRESS.md is advanced to "done" for a step without verifying the specialist actually produced its declared artifact on disk. The grep test: every step has both a sibling-invocation timestamp and an artifact-verification timestamp, and the verification result is "exists and non-empty," not "the agent said it was done." Cited: Cogent's 2026 multi-agent orchestration playbook; Cybermaniacs on rubber-stamp risk; the AWS / DEV piece on multi-agent validation.
- **Phantom resume.** kickoff-ready claims to resume from `.kickoff-ready/PROGRESS.md` step N but starts fresh because (a) the prompt cache was invalidated and the agent did not re-read PROGRESS.md, (b) the agent re-ran step 1 because of compression-summary loss, or (c) the agent inherited stale tool-result state and made decisions on yesterday's truth. The grep test: every kickoff-ready turn begins with `Read .kickoff-ready/PROGRESS.md` and an `ls` of every claimed-complete `.{skill}-ready/` directory. Never trust the cached conversation about resume state. Cited: Anthropic claude-code issues #42338, #42260, #42309; NousResearch hermes-agent#17344; paperclipai#635.
- **Ghost handoff.** kickoff-ready invokes a sibling without first verifying the upstream artifact exists. The architect agent runs before `.prd-ready/PRD.md` is on disk; it hallucinates a PRD-equivalent from the user's one-paragraph idea; the downstream chain proceeds on a fictional foundation. The grep test: every sibling invocation is preceded by an upstream-artifact-exists check derived from the sibling's documented `upstream:` list. Cited: Galileo's multi-agent coordination failure analysis; the LLM-agent hallucination survey on agents-asked-to-infer-state.
- **Happy-path orchestration.** kickoff-ready handles the case where every sibling succeeds and writes its artifact, but has no policy for: sibling X failed, sibling X claimed success but artifact is missing, the user wants to skip sibling X entirely, the user already has a PRD from before kickoff-ready started and wants to import it instead of running prd-ready, the user wants to re-run sibling X because the input changed. The grep test: PROGRESS.md schema includes statuses for `skipped` (with reason), `imported` (with source path), `failed` (with retry budget), and `re-invoked` (with prior-version pointer), not just `done`.

Vocabulary used but not claimed: **state-vs-artifact drift** (the visible symptom of rubber-stamp orchestration; useful as a grep target during verification), **god-skill** (cautionary endpoint, not a refusal name), **ouroboros progress** (secondary metaphor; prefer "state-vs-artifact drift").

## When this skill does NOT apply

The scope fence is the most important thing about this skill. Route elsewhere if the request is:

- **Writing the PRD.** That is `prd-ready`. kickoff-ready invokes it and reads `.prd-ready/PRD.md`; it never produces PRD content inline.
- **Designing the architecture.** That is `architecture-ready`. kickoff-ready invokes it and reads `.architecture-ready/ARCH.md`; it never sketches architecture inline.
- **Sequencing the roadmap.** That is `roadmap-ready`. kickoff-ready invokes it and reads `.roadmap-ready/ROADMAP.md`; it never proposes Now/Next/Later inline.
- **Picking a stack.** That is `stack-ready`. kickoff-ready invokes it and reads `.stack-ready/DECISION.md`; it never recommends a framework inline.
- **Setting up the repo.** That is `repo-ready`.
- **Building the app.** That is `production-ready`.
- **Deploying anything.** That is `deploy-ready`.
- **Wiring observability.** That is `observe-ready`.
- **Producing launch materials.** That is `launch-ready`.
- **Adversarial security review.** That is `harden-ready`.
- **Existing-codebase migrations.** kickoff-ready is greenfield-only. If the user already has a partial app, an existing PRD without an ARCH, an architecture without a roadmap, etc., route them to the specific specialist that fills the gap. kickoff-ready's skip-and-import detection (Step 1) handles this gracefully when the user explicitly invokes kickoff-ready, but the default routing for "I have a half-built thing" is the specialist, not the orchestrator.
- **Project-level state above PROGRESS.md.** Phases, milestones, sign-off ceremonies, and per-feature work breakdowns belong to whatever orchestrates the project (GSD, BMAD, the user's own process). kickoff-ready's PROGRESS.md tracks one thing: where in the suite arc the project currently sits. It does not track sprint plans, ticket queues, or per-feature work.
- **Routing decisions for non-suite work.** If the user asks for something outside the ready-suite (write a blog post, debug a memory leak, refactor an existing module), kickoff-ready refuses and surfaces the request to the harness. The orchestrator-of-everything is not the orchestrator-of-this-suite.

This section is the scope fence. Every plausible trigger overlap with a sibling has a route-elsewhere line. Reference: [`references/scope-fence.md`](references/scope-fence.md) catalogs the boundary in detail with grep tests per refusal.

## Workflow

Eight steps. Skipping any step produces one of the named failure modes above. Reference files are loaded on demand per the table at the bottom of this file.

### Step 0. Detect harness, mode, and invocation context

Read [`references/handoff-protocols.md`](references/handoff-protocols.md). Determine three things in writing before any other action:

1. **Harness.** Claude Code (has Skill tool, slash invocation), Codex (has Skill tool, dollar-sign invocation), Antigravity (has Skill tool, Agent Skills standard), Cursor (no Skill tool; rules and notepads), Windsurf (no Skill tool; workflows), or generic chat frontend (no file system, single-conversation). The harness determines whether handoff is programmatic or guidance-text.
2. **Mode.** New kickoff (no `.kickoff-ready/PROGRESS.md` on disk), resume (PROGRESS.md exists; re-derive state from disk), or import (PROGRESS.md absent but one or more `.{skill}-ready/` directories exist; the user is bringing prior work into the chain).
3. **Project-state hint.** Check whether siblings are installed. If a sibling kickoff-ready intends to invoke is missing from the harness's skill list, surface the install instruction before reaching that step. Do not silently fail mid-chain.

**Passes when:** the harness, mode, and install state are written to PROGRESS.md (or, on file-system-less harnesses, to the conversation as a structured block); the resume protocol from Step 1 has run; the user has confirmed the detected state is correct.

### Step 1. Resume protocol: re-derive state from disk

Read [`references/progress-tracking.md`](references/progress-tracking.md). On every kickoff-ready turn (not just explicit resume), do:

1. `Read .kickoff-ready/PROGRESS.md` if it exists. The cached conversation memory of "we already did step N" is not authoritative. Disk is.
2. `ls .{skill}-ready/` for every sibling claimed complete in PROGRESS.md. Verify each declared artifact path exists and is non-empty. Empty or missing means the step is **not** done; PROGRESS.md is wrong; correct it before proceeding.
3. Identify the next step from disk, not from conversation. If PROGRESS.md says step 5 but `.production-ready/STATE.md` does not exist, the next step is to re-invoke production-ready, not to advance to deploy-ready.
4. Record the resume verification in PROGRESS.md with a timestamp and the disk-state hash (file mtime is sufficient).

This protocol runs every turn. It is the only defense against phantom resume. The cited Anthropic claude-code resume failure modes (#42338, #42260, #42309) are all variants of "the agent trusted its conversation memory instead of disk." kickoff-ready does not.

**Passes when:** PROGRESS.md state matches disk state; the next step is identified; any drift between PROGRESS.md and disk is corrected in PROGRESS.md (disk wins).

### Step 2. Confirm or capture the kickoff intent

Before invoking specialists, capture the user's project intent in one paragraph. This is the only "writing" kickoff-ready does, and it is metadata, not specialist content.

Produce, in PROGRESS.md, a `## Kickoff intent` block:

1. **One-line project description** in the user's own words, quoted verbatim from their request.
2. **Greenfield-or-not check.** Confirm no existing app exists. If there is partial existing work (a draft PRD, a started repo), declare it as imports in PROGRESS.md per [`references/progress-tracking.md`](references/progress-tracking.md) import schema.
3. **Skip declarations.** If the user already knows they want to skip a sibling (e.g., "skip the launch tier; this is internal"), record it now. Skip is a recorded event, not silence.
4. **Time-budget hint.** Optional. The user may declare an appetite ("I want to be live in two weeks" or "I am exploring; no timeline"). This does not bind the chain but informs which siblings are skipped (a one-day prototype likely skips harden-ready and most of launch-ready).

This is **not** a PRD. The PRD is what prd-ready will produce in Step 3. This is one paragraph of orchestration context that lets kickoff-ready route correctly.

**Passes when:** the kickoff intent block is in PROGRESS.md; greenfield is confirmed (or imports are declared); skip declarations are recorded; the user has confirmed the intent paragraph is correct.

### Step 3. Invoke planning tier: prd-ready -> architecture-ready -> roadmap-ready -> stack-ready

Read [`references/sequencing-rules.md`](references/sequencing-rules.md). Invoke the planning-tier siblings in dependency order. For each:

1. **Verify upstream artifacts exist on disk.** This is the ghost-handoff guard. The artifact paths are documented in each sibling's "Consumes from upstream" section.
2. **Invoke the sibling.** On harnesses with a Skill tool: programmatic invocation. On harnesses without one: surface the guidance string from [`references/handoff-protocols.md`](references/handoff-protocols.md), wait for the user to run the specialist, return when the artifact appears.
3. **Verify the produced artifact.** Two checks: file exists, file is non-empty (not the unmodified template scaffold). This is the rubber-stamp-orchestration guard.
4. **Update PROGRESS.md.** Record sibling, invocation timestamp, artifact path, verification result, verification timestamp.
5. **Stop on skip.** If the user has declared a skip for this sibling, record `status: skipped` with reason and proceed to the next.

The planning tier is strictly sequential because each sibling consumes the prior one's artifact. prd-ready (no upstream), then architecture-ready (consumes PRD), then roadmap-ready (consumes PRD and ARCH), then stack-ready (benefits from PRD and ARCH; runs even without them per its graceful-degradation declaration).

**Passes when:** every planning-tier sibling has either a verified-done step or a recorded-skip step in PROGRESS.md; no step is in `done` status without artifact verification.

### Step 4. Invoke building tier: repo-ready -> production-ready

Same protocol as Step 3. The building tier is sequential by default. Reference [`references/sequencing-rules.md`](references/sequencing-rules.md) Section 4.1 for parallelism options.

repo-ready first because production-ready running on a properly-scaffolded repo (correct lint config, CI pipeline already present, test runner installed) produces better results than the reverse. Both write to the same `package.json`; sequential avoids the merge problem.

If the user has declared advanced parallelism in Step 2, invoke them in two harness sessions and reconcile package.json manually. Default: sequential.

**Passes when:** repo scaffolding presence verifies (the `repo-ready` canonical files are on disk; see [`references/sequencing-rules.md`](references/sequencing-rules.md) per-sibling upstream contract for the multi-file check), `.production-ready/STATE.md` exists and verifies; PROGRESS.md records both steps as done with verification timestamps.

### Step 5. Invoke shipping tier: deploy-ready -> observe-ready -> (launch-ready || harden-ready)

Read [`references/sequencing-rules.md`](references/sequencing-rules.md) Section 5. Invoke deploy-ready, then observe-ready, then launch-ready and harden-ready in parallel.

The parallel branch: launch-ready and harden-ready do not list each other as upstream. They both consume the same shipping-tier inputs (deployed app, monitored app). They can run concurrently as long as the user has access to two harness sessions, or sequentially in either order if not.

**Critical-finding gate.** If harden-ready emits a finding at severity Critical, kickoff-ready halts launch-ready until the finding is resolved or the user explicitly accepts the risk in PROGRESS.md (with named risk owner, justification, and dated acceptance per the harden-ready risk-register pattern). This is the default; the user can override with an explicit "gate-launch-on-hardening" preference (security-sensitive projects: healthcare, finance, regulated industries) or "skip harden-ready" (prototypes with no real user surface). Both overrides are recorded in PROGRESS.md.

**Passes when:** every shipping-tier sibling has either verified-done, recorded-skip, or explicit-deferred status; the critical-finding gate has resolved; PROGRESS.md is the auditor view of what shipped, what was skipped, and why.

### Step 6. Final ledger and handoff to ongoing operations

Once all in-scope siblings are verified-done or recorded-skip, kickoff-ready's job is finished. The kickoff arc is complete. PROGRESS.md becomes the durable record of how the project was kicked off.

Produce in PROGRESS.md a `## Kickoff complete` block:

1. **Per-sibling summary table.** Sibling, status (done / skipped / deferred / imported), artifact path, verification timestamp.
2. **Open items handed off to ongoing work.** Anything kickoff-ready did not complete (deferred harden-ready findings, post-launch follow-ups, etc.). These are not kickoff-ready's responsibility going forward; they are the project's responsibility.
3. **Recommended next-step orchestrator.** If the user wants ongoing phase/milestone work, point at GSD or whichever phase orchestrator they prefer. kickoff-ready is one-shot per project; the iteration loop after kickoff is a different orchestration pattern. Reference: production-ready's ORCHESTRATORS.md GSD section.

#### Sub-step 6a. Emit project-root `AGENTS.md` if absent

If no `AGENTS.md` exists at project root, kickoff-ready writes a minimal one. This is the only file kickoff-ready writes outside `.kickoff-ready/`, and it is orchestration metadata: it names the suite, points at the artifact map, and tells any harness that reads `AGENTS.md` (Codex CLI, GitHub Copilot, Cursor, Windsurf, Aider, Zed, Warp, Roo Code, Jules, Factory, Amp, Devin) where the kickoff produced its specialist artifacts. Without this file, the suite is invisible to non-Claude harnesses arriving at the project cold.

The emit conditions are strict:

1. **Only if absent.** If `AGENTS.md` already exists (e.g., the user's repo had one, or repo-ready scaffolded one), kickoff-ready leaves it untouched. Do not append, do not overwrite, do not "merge." The existing file is authoritative; kickoff-ready records `AGENTS.md: existing-respected` in PROGRESS.md and moves on.
2. **Only artifact metadata.** The emitted file lists the ready-suite artifacts the kickoff produced and a one-paragraph pointer to the suite. It does not contain stack, build commands, conventions, forbidden actions, or any specialist content. Those belong to repo-ready's `AGENTS.md` scaffolding (when invoked) or to the user. Mixing the two re-introduces the scope-leak failure mode this skill exists to prevent.
3. **Skip on out-of-fs harnesses.** On chat-only frontends with no file system, kickoff-ready surfaces the AGENTS.md template as a guidance string for the user to paste, instead of writing.

The emitted template lives at [`references/agents-md-template.md`](references/agents-md-template.md). Variable substitutions: project name (from PROGRESS.md kickoff intent), per-sibling status table (from the Step 6 summary), and a single-line "this project was kicked off via ready-suite" attribution.

Record the emit (or the respected-existing decision) in PROGRESS.md under the `## Kickoff complete` block as `agents_md_emitted: <path | existing-respected | guidance-text>`.

**Passes when:** the summary table is in PROGRESS.md; deferred items are explicit; `AGENTS.md` exists at project root (either user-authored or kickoff-emitted); the emit decision is recorded; the user has the information needed to continue without kickoff-ready in the loop.

### Step 7. Refuse-and-surface for out-of-scope requests

At any point during Steps 0-6, if the user asks kickoff-ready to do something outside its scope (write a PRD inline, sketch an architecture in chat, refactor an existing module, debug a memory leak, write blog copy, pick a logo), the response is:

1. **Refuse the inline production.** Do not start writing.
2. **Name the failure mode.** "That is scope leak. kickoff-ready does not produce specialist content."
3. **Route.** Surface the correct sibling or external skill. If it is a ready-suite specialist's job, name the sibling and (on harnesses with a Skill tool) offer to invoke it. If it is outside the suite entirely, surface the request to the harness for general routing.
4. **Continue.** Resume the kickoff arc from the prior step without modification.

This is the load-bearing scope-fence behavior. Cited: production-ready/ORCHESTRATORS.md invariant 1.

**Passes when:** every out-of-scope request the user makes mid-arc receives one of (inline-refusal, named-failure-mode, route, resume) and never an inline-fulfillment.

## The "have-nots"

If any of these appear, the kickoff fails this skill's contract and must be fixed before declaring done:

- **kickoff-ready writes specialist content.** Any markdown content produced by kickoff-ready that should have come from a sibling. Grep target: search the conversation for kickoff-ready output that contains a section header from a sibling's artifact template (`# Product Requirements`, `## Trust Boundaries`, `## Now / Next / Later`, `## OWASP Walkthrough`, etc.). If kickoff-ready emitted any of those, scope leak fired.
- **PROGRESS.md says step done with no artifact on disk.** Grep target: for every PROGRESS.md row where `status: done`, the declared `artifact:` path exists in the file system and is non-empty. If any row fails this check, rubber-stamp orchestration fired. The `gsd-validate-phase`-style discipline applies.
- **Resume that did not re-derive state from disk.** Grep target: every kickoff-ready turn begins with a `Read .kickoff-ready/PROGRESS.md` and an `ls` of every claimed-complete `.{skill}-ready/`. If a turn skipped these and acted on cached conversation memory, phantom resume fired.
- **Sibling invoked before its declared upstream artifact exists.** Grep target: for every Skill-tool invocation, the prior step's artifact-verification timestamp is earlier than the invocation timestamp. If invocation happens without verified upstream, ghost handoff fired.
- **No status code in PROGRESS.md for the failure / skip / import / re-invoke cases.** Grep target: every PROGRESS.md row's `status` field is one of `pending`, `in-flight`, `done`, `skipped`, `imported`, `failed`, `re-invoked`. If only `pending` and `done` exist, happy-path orchestration fired.
- **kickoff-ready continues after a Critical finding from harden-ready without an explicit risk-acceptance entry.** Grep target: if `.harden-ready/FINDINGS.md` contains an unresolved Critical and PROGRESS.md shows launch-ready as `done` without a corresponding `risk-acceptance:` block, the critical-finding gate failed.
- **Out-of-scope request received an inline answer.** Grep target: any conversation turn where the user asked for a PRD / architecture / launch copy / etc., and kickoff-ready produced markdown that fulfills the request rather than refusing and routing.
- **PROGRESS.md exists but skips are recorded as silence.** Grep target: a sibling that does not appear in PROGRESS.md at all (neither as done nor as skipped). Silence is not a status; record skips explicitly per the Shape Up no-gos discipline.

These have-nots are concrete and grep-testable. The references catalog has the full catalog at [`references/kickoff-antipatterns.md`](references/kickoff-antipatterns.md).

## Reference files: load on demand

| Reference file | When to load |
|---|---|
| [`references/RESEARCH-2026-04.md`](references/RESEARCH-2026-04.md) | **Always at Step 0.** The evidence base for every refusal name and every sequencing decision. Cited from README's "What this skill prevents" table. |
| [`references/sequencing-rules.md`](references/sequencing-rules.md) | **Step 3, 4, 5.** The DAG of sibling dependencies, parallelism rules, harden-ready gate logic, and skip-detection semantics. |
| [`references/handoff-protocols.md`](references/handoff-protocols.md) | **Step 0, 3, 4, 5.** Per-harness Skill-tool invocation patterns. Guidance-text fallback for harnesses without a Skill tool. |
| [`references/progress-tracking.md`](references/progress-tracking.md) | **Step 1, 2, 6.** PROGRESS.md schema, status vocabulary, resume protocol, skip-when-artifact-exists logic, audit-ledger view. |
| [`references/scope-fence.md`](references/scope-fence.md) | **Step 7 always; on demand otherwise.** The boundary catalog. What kickoff-ready refuses, why each refusal is load-bearing, the routing target per refusal. |
| [`references/kickoff-antipatterns.md`](references/kickoff-antipatterns.md) | **On demand during verification.** The named failure modes from the research pass with grep tests, severity, and the kickoff-ready guard for each. |
| [`references/agents-md-template.md`](references/agents-md-template.md) | **Step 6 sub-step 6a.** The `AGENTS.md` template kickoff-ready emits to project root when no `AGENTS.md` exists. Substitution rules, emit conditions, the kickoff-ready / repo-ready handshake on a shared file. |

## Suite membership

This skill is part of the **ready-suite**. See [`SUITE.md`](SUITE.md) at the repo root for the full map. Every other ready-suite skill is downstream from this one in the orchestration sense.

- **Orchestration tier (this tier):** `kickoff-ready` (the only skill in the meta-tier).
- **Planning tier:** `prd-ready` (what), `architecture-ready` (how), `roadmap-ready` (when), `stack-ready` (with what tools).
- **Building tier:** `repo-ready` (the repo scaffolding), `production-ready` (the app).
- **Shipping tier:** `deploy-ready` (ship it), `observe-ready` (keep it healthy), `launch-ready` (tell the world), `harden-ready` (survive adversarial attention).

kickoff-ready is the conductor, not a peer. Every sibling stands alone and runs without kickoff-ready. kickoff-ready exists for the case where the user has a raw idea and wants the entire arc orchestrated at once.

## Consumes from upstream

kickoff-ready has no upstream siblings. It triggers from raw user intent and reads from disk to detect the import mode.

When the agent starts, it checks for sibling artifacts that already exist (the import case) and adjusts the chain accordingly:

| If present | Effect | Recorded as |
|---|---|---|
| `.prd-ready/PRD.md` | Skip prd-ready invocation; verify the imported file is non-empty; advance to Step 3.b (architecture-ready) | `prd-ready: imported` in PROGRESS.md |
| `.architecture-ready/ARCH.md` | Skip architecture-ready invocation; verify the file; advance | `architecture-ready: imported` |
| `.roadmap-ready/ROADMAP.md` | Skip roadmap-ready invocation; verify; advance | `roadmap-ready: imported` |
| `.stack-ready/DECISION.md` | Skip stack-ready invocation; verify; advance | `stack-ready: imported` |
| Repo scaffolding presence (README.md at repo root, or `.github/workflows/*.yml`, or `.repo-ready/SECURITY.md`; repo-ready does not produce a single canonical STATE.md, so the check is a multi-file presence test) | Skip repo-ready invocation; verify scaffolding; advance | `repo-ready: imported` |
| `.production-ready/STATE.md` | Skip production-ready invocation; verify | `production-ready: imported` |
| `.deploy-ready/STATE.md` (or equivalent) | Skip deploy-ready; verify | `deploy-ready: imported` |
| `.observe-ready/STATE.md` (or equivalent) | Skip observe-ready; verify | `observe-ready: imported` |
| `.launch-ready/STATE.md` (or equivalent) | Skip launch-ready; verify | `launch-ready: imported` |
| `.harden-ready/STATE.md` (or equivalent) | Skip harden-ready; verify | `harden-ready: imported` |

If an imported artifact is present but the user wants to re-run the sibling (because the input changed), the user explicitly invokes the sibling and PROGRESS.md is rolled back from that step forward. Re-invocation is a recorded event, not silent overwrite.

## Produces for downstream

kickoff-ready produces one artifact: the kickoff progress ledger. Every other artifact in the project comes from a sibling.

| Artifact | Path | Consumed by |
|---|---|---|
| **Kickoff progress ledger** | `.kickoff-ready/PROGRESS.md` | The user (auditor view), the next kickoff-ready session (resume), and any orchestrator that takes over after kickoff (GSD, BMAD, etc.) for context on what was kicked off. |

The ledger is small by construction. The schema is in [`references/progress-tracking.md`](references/progress-tracking.md). The siblings do not consume PROGRESS.md; they consume each other's artifacts directly. PROGRESS.md is for the human and for the next kickoff session.

## Handoff: every specialist task is a sibling's job

If the work is producing the PRD, delegate to `prd-ready`. kickoff-ready invokes the sibling, verifies the artifact, advances PROGRESS.md.

If the work is designing the architecture, delegate to `architecture-ready`. Same protocol.

If the work is sequencing the roadmap, delegate to `roadmap-ready`. Same protocol.

If the work is picking a stack, delegate to `stack-ready`. Same protocol.

If the work is scaffolding the repo, delegate to `repo-ready`. Same protocol.

If the work is building the app, delegate to `production-ready`. Same protocol.

If the work is deploying it, delegate to `deploy-ready`. Same protocol.

If the work is wiring monitoring, delegate to `observe-ready`. Same protocol.

If the work is producing launch materials, delegate to `launch-ready`. Same protocol.

If the work is adversarial review, delegate to `harden-ready`. Same protocol.

If the work is ongoing phase or milestone management after the kickoff arc completes, delegate to a phase orchestrator (GSD's command tree is one option; BMAD with the boundary translation in production-ready/ORCHESTRATORS.md is another). kickoff-ready is one-shot per project.

**If your harness exposes a skill-invocation tool** (Claude Code's slash command, Codex's dollar-sign form, Antigravity's Agent Skills standard), invoke the sibling directly when the handoff trigger fires. **Otherwise**, surface the handoff to the user as guidance text per [`references/handoff-protocols.md`](references/handoff-protocols.md): "This step needs `prd-ready`. Install it from https://github.com/hannsxpeter/ready-suite/tree/main/skills/prd-ready, then run it on this project. When `.prd-ready/PRD.md` exists, return to kickoff-ready and we will verify and advance." Do not generate the sibling's output inline from this skill; the handoff is the contract.

## Session state and resume

The kickoff arc spans sessions. The planning tier alone can span days. The building tier can span weeks. The full arc (planning through launch and harden) routinely spans a month or more. Without a state file, every resume rediscovers the chain from scratch and re-invokes siblings that have already run.

Maintain `.kickoff-ready/PROGRESS.md` as the source of truth about the kickoff arc. Read it first on every turn. If it conflicts with disk (artifacts present that PROGRESS.md does not record, or PROGRESS.md says done for a step whose artifact is missing), trust disk and update PROGRESS.md.

The schema is in [`references/progress-tracking.md`](references/progress-tracking.md). The resume protocol is the load-bearing defense against phantom resume. Run it every turn. Never trust the cached conversation about what step we are on.

## When in doubt, invoke the sibling

If kickoff-ready ever feels the urge to "just sketch" what a sibling would produce, the urge is the failure mode. The right answer is to invoke the sibling and stop typing. Every line kickoff-ready writes that is not orchestration metadata is a step toward becoming the god-skill the suite exists to prevent.

The first inline content from kickoff-ready that should have come from a sibling is the next thing to refuse.
