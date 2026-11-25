---
name: consensus-workflow
description: Operating procedures for working with consensus-mcp in any project. Trigger when the user asks to run a consensus consult, dispatch codex/gemini for review, evaluate a Workflow B vs Workflow A decision, debug a stalled or failed reviewer dispatch, or any question about HOW the cross-AI consensus workflow runs (as opposed to "consensus init" which only bootstraps). Phrases include "consensus review", "consensus iteration", "consensus consult", "run a consult", "dispatch codex", "dispatch gemini", "workflow 3", "workflow 4", "propose-converge", "post-review".
---

# Consensus-mcp operating procedures

Load-bearing rules for working with consensus-mcp. These are not
project-specific tips - they apply in every project that uses the
cross-AI consensus workflow. Follow them by default; deviate only when
the operator explicitly says otherwise.

## STEP 0 - Project preflight: AUTO-INITIALIZE an un-set-up project

BEFORE running any consult, confirm THIS project is set up. If
`.consensus/config.yaml` does NOT exist in the project root, the project is not
initialized yet - do NOT fail, and do NOT tell the user to go run `consensus-init`
themselves. Initialize it for them (the user installed consensus globally once;
per-project setup should be automatic):

1. **Detect the available AIs** - run `consensus-init --detect-contributors`
   (read-only; prints JSON: each independent contributor with `installed` + `host`).
2. **Confirm + choose the panel in ONE `AskUserQuestion`:**
   - Tell the user consensus isn't set up in this project yet and that initializing
     writes `.consensus/config.yaml`, `.mcp.json`, a managed `.gitignore` block, and
     seeds reviewer house-rules into `CLAUDE.md` / `AGENTS.md` / `GEMINI.md` /
     `GROK.md`. (So it is never a surprise file write.)
   - Offer a MULTI-SELECT of the detected AIs for the panel: pre-select the
     `installed` ones; list any not-installed ones as "available (needs install)".
     A panel needs **>= 2 independent reviewers**. Always include a way to cancel.
3. **On confirm**, run from the project root:
   `consensus-init --from-claude-code --non-interactive --contributors <chosen,comma,list>`
   Surface its output verbatim. You do NOT need a Claude Code reload to continue:
   the consult runs via the shell binaries below, which work immediately. (The MCP
   tools load on the next reload; they are optional for the consult.)
4. **On cancel**, stop - do not run the consult.

If `.consensus/config.yaml` already exists, skip STEP 0 entirely and proceed.

## Workflow selection

**Default to Workflow A (propose-converge with blind-first-reveal) for
any decision with real design surface** - API shape, trade-off, novel
mechanism, anything where reasonable people could disagree on the right
approach. Workflow B (post-review: claude implements the approved plan,
then **ONE single reviewer - codex - does a code review**) is the
lightweight code review run AFTER a Workflow A plan is approved, or for
hot-patches that block in-flight work. Claude weighs the reviewer's
suggestions on merit, finalizes, and ships.

The mistake to avoid is defaulting to B because it's faster and
calling everything "execution." Test: did the converged plan specify
the API shape, error contract, mechanism? If not, those choices are
themselves design surface - go through Workflow A.

Listing 2+ design choices in a single response = Workflow A
candidate. Stop and route to a consult.

## Tier routing - cost-proportional rigor (operative)

### Plain-language declarations

The conversational interface is primary. When the operator says "quick
consensus", "standard consensus", or "deep consensus" (including ordinary
sentences such as "we are going nowhere - get a deep consensus"), that is the
required explicit declaration. Route to the named tier and start the workflow;
do not ask them to restate it as a CLI flag or MCP field. Flags and structured
fields are automation interfaces, not prerequisites for AI-hosted use.

**Match rigor to risk; don't apply the heavy path uniformly. The rigor tier is
OPERATOR-DECLARED - never inferred** (heuristics are the shared-prior trap; the
engine's `_goal_risk_class` already refuses to infer risk). At consult launch:

1. **Operator DECLARES the tier** (`quick` / `standard` / `deep`) in the
   goal_packet. `consensus_mcp/_tier_router.effective_tier(declared_tier,
   touches_governance_surface=, security_or_irreversible=)` is the AUTHORITATIVE
   router -> tier + preset (workflow A/B, all-enabled panel policy, path A/B). A missing/invalid
   declaration RAISES - escalate, never default silently.
2. **Optional, NON-BINDING suggestion:** `_tier_router.suggest_tier(...)` returns
   an advisory object (`advisory: True`, `suggested_tier`, reason) to help the
   operator decide. The engine NEVER routes on it. A picker surfacing it must NOT
   pre-fill / pre-select / default-on-timeout to it - the operator declares
   explicitly; log declared-vs-suggested so rubber-stamp rate is auditable.
3. `_tier_router.estimate_cost(tier, independent_reviewers=<enabled independent count>, median_dispatch_seconds=<from telemetry>)`
   -> n_dispatches + est wall-clock + token band. **Show this estimate before any
   dispatch.**
4. **Sole automatic move - the MONOTONE governance safety floor:** a change
   touching governance machinery (`.consensus` config / hooks / gates /
   dispatchers / the engine) or that is security/irreversible is auto-UPGRADED to
   `deep` and LOCKED (`effective_tier` applies it; `is_downgrade_allowed` refuses a
   downgrade). It can only RAISE rigor, never select/lower it - a safeguard, not an
   inference. This is the ONE permitted automatic move.

**AI lean is operator-declared too** - informed by a performance SCORECARD (the
learner/ledger/telemetry as decision-support, NOT an auto-applied weight); applied
ONLY to synthesis-narrative tie-breaks, never gates/weights/dispatch-set.

The full decision table (R0-R3, presets, advisory weighting, interaction-surface /
integration-smoke guard) lives in `docs/consensus/routing-decision-table.md`.

## Workflow A / B / C in one line each

**As of v1.14.4: letter aliases (A/B/C) replace numeric (3/4) as
canonical operator vocabulary. Numeric aliases stay accepted for
one cycle with `DeprecationWarning`.**

- **Workflow A (propose-converge)** - DEFAULT. All enabled
  contributors propose independently in round 1 (blind), then
  converge across reviewed rounds. Used for design questions.
  (Was numbered #4.)
- **Workflow B (post-review)** - LIGHTWEIGHT/QUICK. Run AFTER an
  approved Workflow A plan: Claude implements per spec, then **exactly
  ONE reviewer (codex) does a code review** - NOT the full panel (that's
  A). Claude weighs the suggestions on merit and ships. Also used for
  hot-patches. (Was numbered #3.)
- **Workflow C (autonomous-execute)** - LONG-FORM/OVERNIGHT. Runs
  to completion without operator-in-the-loop, auto-approves
  emergent scope items within operator-pre-declared
  `autonomy_contract` boundaries. v1.14.4 ships the contract
  (config alias, validators, scope_check helper, schema); the
  multi-iteration **engine is UNIMPLEMENTED as of v1.15.2 - no
  committed target version; running Workflow C raises a clear
  `NotImplementedError`**. Status:
  `docs/workflows/workflow-c-autonomous.md`.

> **Consistency invariant (count-agnostic governance).** This
> doctrine and the v1.15.1 machine-enforcement are scoped by
> WORKFLOW MODE, never by contributor count. A 2-AI install
> (claude + codex) and a 3-AI install (claude + codex + gemini)
> are governed identically - same doctrine, same seal-time gate,
> same enforcement knob. No default depends on contributor count:
> reviews are input and the host decides each idea on its merits
> (cherry-pick). Vote-counting rules (`unanimous`,
> `strict-majority`) exist only as an explicit opt-in, never a
> default. (`propose-converge` requires
> N>=2, so 2-AI gets full Workflow A enforcement; only
> `autonomous-execute` requires exactly 3.)
- **Advisory** - reviews are gathered for information only; nothing is approved or sealed. Rare.

## Passes by tier: cherry-pick, then the panel reviews your plan

You (the host) cherry-pick ideas, but you never have the final word on your
own choices:

- **quick** - one ideas pass; disposition every idea, then approve.
- **standard** (default) - ideas pass, then ONE plan pass:
  `consensus-mcp-consult --iteration <id> --plan-pass` (MCP:
  `pass_kind: plan`). Reviewers see your `converged-plan.yaml` and
  `dispositions.yaml` and object with tagged findings (`[wrong_rejection]`,
  `[wrong_deferral]`, `[wrong_acceptance]`, `[conflict]`, `[gap]`, `[other]`).
  Run `consensus-mcp-approve --iteration <id> --init-objections` and answer
  each row: `accepted` (change the plan) or `rebutted` with evidence.
  Every rebuttal is a holdout for the USER. If you changed the plan or
  dispositions, run `consensus-mcp-consult --iteration <id> --confirm-pass`:
  reviewers see only the diff and the accepted objections and confirm the
  edit does only that; any `[unfaithful]` / `[unrelated_change]` finding goes
  to the user.
- **deep** - repeat plan passes until no reviewer holds an open objection.
  Your rebuttals go back to the reviewers in the next pass; an objection
  closes only when the reviewer who raised it returns a clean review of the
  current plan (or the user decides). After 5 passes
  (`consult.max_plan_passes`) the run returns `needs_user_decision`.

Holdouts: show the user each one (reviewer, model, objection, your response)
and ask. Record their answer with
`consensus-mcp-approve --iteration <id> --user-decision '<id>=yay|nay|send_back'`
(yay = accept it and update the plan; nay = dismiss; send_back = up to 5 more
deep passes). Never answer for the user, and never settle an objection by
counting reviewers.

## End-to-end iteration pipeline (superpowers <-> consensus)

One repeatable pipeline. Each superpowers stage maps to a consensus role:

1. `consensus:brainstorming` -> intent + design exploration.
2. **Consensus consult = the design approval gate** (consensus is the approver):
   author goal_packet + review-packet; run the panel; converge (weighted-synthesis).
3. `consensus:writing-plans` -> TDD implementation plan from the converged design.
4. `consensus:subagent-driven-development` -> implement task-by-task (implementer
   + spec-compliance review + code-quality review per task).
5. `consensus:finishing-a-development-branch` -> release cut (see "Release cadence").

### Dual-path consult selection
- **Path B - `consensus.run_iteration`** (the built engine dispatches
  codex/gemini/kimi via adapters + claude/host_peer via callbacks, runs
  blind-first-reveal, seals): use for **post-review / execution / clear-design /
  hot-patches**. claude + host_peer are supplied as `claude_proposal_yaml` /
  `host_peer_review_yaml` (static across rounds - acceptable here).
- **Path A - orchestrator-driven** (dispatch shell binaries + host-supplied blind
  subagents + manual weighted-synthesis): use for **propose-converge with real
  design surface**, where claude/host_peer must genuinely re-converge across
  rounds. KEPT as the documented advanced path; its sole justification is genuine
  multi-round host convergence. (Known follow-up: per-round host re-convergence in
  Path B needs a `run_iteration` pause/resume API - not yet built.)
- **host_peer is first-class in BOTH paths.**

### host_peer dispatch procedure (repeatable, not improvised)
1. Dispatch a **blind** Claude subagent (fresh context, NO peer artifacts) as the
   host_peer reviewer, using `host_peer_review_template.md` (located in the package's `dispatch_templates/` directory).
2. Capture its output as `host_peer_review_yaml` with this schema:
   ```yaml
   findings: []            # list
   goal_satisfied: true    # bool
   blocking_objections: [] # list
   ```
3. Path B: pass it as `consensus.run_iteration(..., host_peer_review_yaml=<yaml>)`.
   Path A: seal it via the host_peer path. One-shot; never loop.

### Codified consult flow - SAME every install (no improvisation)

The consult pipeline is fixed. Run it the SAME way every time; do NOT invent
per-session steps.

1. **Author the goal_packet + review-packet.** Finalize them BEFORE dispatching
   (mid-flight rewrites waste dispatches).
   - **Let reviewers read.** Never forbid "all commands" or "all shell use" in the
     goal: for several harnesses (Codex, OpenCode) a read-only command such as
     `cat` or `rg` IS the file-reading tool, and a reviewer told not to run any
     command reviews only the embedded excerpt (DriverLogs FU-06). Forbid writes,
     tests, installs, project-code execution and model/provider calls instead; the
     dispatch templates already allow read-only commands.
   - **Name the reviewed bytes.** The packet is built from the working tree and
     records `reviewed_bytes: working_tree` and `worktree_dirty`. If you review an
     isolated snapshot, identify it by its manifest/file hashes, never by a
     baseline commit that does not contain those bytes (DriverLogs FU-11).
2. **Fan out to ALL enabled reviewers AT ONCE - in parallel.** Make the packet,
   send it to every reviewer concurrently, wait for all to seal. **Do NOT** run a
   "validate the plumbing with a single reviewer first, then parallelize the rest"
   probe - that improvised serial pre-flight is FORBIDDEN. The engine
   (`run_iteration`) now fans out within a phase automatically. For a consult, use
   the ONE command:
   - **`consensus-mcp-consult --iteration <name> [--tier quick|standard|deep]`**
     (or the `consensus.consult_panel` MCP tool, which runs as an async job). It
     starts every enabled seat concurrently (the free self-hosted DeepSeek seat first when
     `CONSENSUS_MCP_DEEPSEEK_BASE_URL` is set), applies a per-seat timeout and a
     total deadline, isolates failures (one seat failing never cancels the others),
     falls back within a seat on quota (e.g. Fable -> Opus, Astra -> Sol), and
     writes `consult-summary.yaml` with the model each seat requested and used,
     its failure class and wall time. Zero sealed reviews is reported as
     `no_reviews`, never success.
   - The per-reviewer shell binaries (`consensus-mcp-dispatch-<reviewer>`) remain
     for re-running a single seat; the MCP `reviewer_dispatch_*` tools run as
     async jobs and no longer have a short cold-start timeout.
   - **`--pass-id`: omit it.** If you must pass one, make it RANDOM. The T6 seal index is a GLOBAL
     pass_id namespace across ALL iterations ever (it is a content-identity tamper
     guard: a given pass_id must always carry the same content). Reusing a pass_id
     from any prior consult - including bare integers like `1`/`2`/`3` - collides
     with a cryptic `index_collision` error that even cites the OTHER iteration's
     file. So make the pass_id RANDOM: `--pass-id <reviewer>-$(openssl rand -hex 6)`
     (or any random token). NEVER reuse bare integers or any value from a prior
     consult. (As of the random-default hardening, omitting `--pass-id` auto-
     generates a hash of (iteration, packet, contributor) - prefer that.)
   - **Kimi no longer has to run last.** Tool-using seats (kimi, grok, claude,
     opencode) review a disposable copy of the worktree, and the post-dispatch
     integrity check ignores `consensus-state/` (the panel's own write area), so
     sibling seals no longer fail kimi/grok (old P0-OPS.3/.4). Still do not edit
     the repo itself while a consult is running: a real change outside
     `consensus-state/` correctly fails the integrity check.
3. **Synthesize** the sealed reviews into ONE host-authored `converged-plan.yaml`
   (weighted-synthesis). This is YOUR artifact - the approve step never authors it.
4. **Approve in ONE step:** `consensus-mcp-approve --iteration <name> --scope-glob
   <glob>` (or the `consensus.approve` MCP tool). It validates the >=2-non-claude
   precondition, seals the outcome mechanically (no manual `EDIT_ME` editing),
   mints `.consensus/design-approved`, and re-validates - emitting an ACTIONABLE
   error on any unmet precondition. Both the CLI and the MCP tool use the SAME
   strict repo-root resolver (`CONSENSUS_MCP_REPO_ROOT` env-first), so they can
   never resolve different roots. Accepts `--converged-plan` as a bare name or a
   full path. Do NOT hand-roll the prepare -> edit -> mint sequence.

Containment-marker dirs (`consensus-state/`, `consensus_mcp/`,
`consensus_mcp/validators/`) must exist at the repo root for resolution; in the
consensus-mcp repo itself they already do.

### `.consensus` gate caveat
The PreToolUse enforcement gate (seal `.consensus/design-approved`, mint a
delivery token) is **project-scoped**: it only fires where a `.consensus/config.yaml`
exists. In a repo without one (e.g. consensus-mcp itself dogfooding via shell
binaries), those seal/mint steps are **aspirational** - follow the discipline by
convention, or activate the gate via `consensus init` to make it enforced.

### Concurrency warning (4-AI engine runs)
Do NOT mutate the repo (edits, or concurrent subagent writes) while a
`run_iteration` engine run is dispatching kimi - kimi's integrity check shells
`git status` and false-positives on concurrent changes, spuriously rejecting the
review.

## Maximize parallelism - always

**Default to parallel; serial is the choice that needs justification.**
Every operation in a consensus workflow that can run independently
SHOULD run in parallel. This applies to:

- Round-1 peer dispatches (codex + gemini in background, claude
  authors proposal in parallel)
- Round-2+ batches where multiple peers are re-dispatched
- Reading multiple sealed artifacts (one batched call, not N
  serial reads)
- Investigating multiple files / running multiple greps during
  iteration scoping
- Background long-running operations (snapshots, audits, blast-
  radius scans) kicked off to run alongside foreground work
- Cross-iteration parallelism: when two iterations have no data
  dependency, dispatch them as parallel branches (worktrees) and
  converge results

Practice has demonstrated drastic performance improvement when
parallelism is fully exploited. Burden of proof flips: if you
choose serial, the reason must be a real data dependency
(operation B needs operation A's output), not "felt simpler" or
"easier to reason about."

### Round-1 dispatch order (Workflow A) - specific case

Dispatch peer contributors FIRST in background, then author your
own proposal in parallel while they run. Independence (blind-
first-reveal) depends on **visibility**, not **temporal order**.
No contributor sees another's output -> independence preserved
regardless of who started writing first. This optimization saves
wall-clock and surfaces dispatcher errors earlier.

Constraints: the goal_packet MUST be final before kicking off
contributors (mid-flight rewrites mean wasted dispatches), and the
"author in parallel" optimization applies to round 1 only - round
2+ explicitly require seeing round-1 outputs.

## Consensus runs to COMPLETION - no gratuitous deferral

**Default: consensus runs to completion when goals + acceptance
gates are clear. Defer only when open design surface genuinely
requires more analysis, the implementation cost is large
(multiple sessions worth), or the work has a real dependency
on something not-yet-built.**

The deferral instinct comes from "splitting reduces blast
radius" + "small PRs are better." Both are RIGHT for genuinely
independent units of work; both are WRONG when the items share
a doctrine boundary or when splitting just postpones the same
decisions without adding analysis.

### The completion test

When authoring a converged-plan.yaml or scoping a deliverable,
ask for each candidate item:

1. Are the acceptance gates concrete and verifiable?
2. Is there ANY open design question remaining (API shape,
   trade-off, mechanism) that actually needs more thought?
3. Is the implementation cost SMALL enough to fit in this
   session? (rough heuristic: <60 minutes of edits + tests)

If (1)=yes AND (2)=no AND (3)=yes -> **execute in the same
session, not a future iteration.** "Future iteration" is the
cop-out - a way to pass the work to a hypothetical later-self
without admitting later-self has the same context window and
will face the same decision.

### Anti-patterns to abort

- "iter-XXXX candidate: <thing>" with no concrete reason it
  can't be done now -> fold into current iteration.
- "Phase B / Phase C" sequencing when phases share the same
  doctrine boundary -> bundle into one.
- "Defer to dedicated iteration" because something is "complex"
  when the complexity is BOUNDED (concrete decisions, finite
  alternatives) -> execute now; consult only on the open part.
- Splitting a hot-patch across multiple version bumps when the
  fixes share a single failure-mode -> bundle into one tag.
- Writing a goal_packet that ASSUMES future iterations will
  exist -> write goal_packets that assume completion is the
  default.

### Application to live consults

Before writing `next_iteration_id: ...` or `deferred to ...`
in a converged plan, run the completion test on each item.
If the test passes, delete the deferral and add the work to
the current scope. Only ratify the deferral if the test
genuinely fails, and name the SPECIFIC blocker
(not "complexity," not "out of scope" - name the missing
data, the dependency, or the design question).

### Sequencing-as-deferral is the same anti-pattern

Don't sequence three independent fixes across three
hot-patches when bundling them into one passes the
completion test. Sequencing produces the same end-state with
more bookkeeping and more chances for drift. The cost of
"big PR" is real but bounded; the cost of perpetual deferral
backlog is unbounded.

## Convergence model - weighted-synthesis by default

**Default convergence model: weighted-synthesis.** All ideas of
all proposals are weighed for benefit to the project as a whole.
No good ideas are lost; no babies tossed with the bathwater.

When writing a `converged-plan.yaml`:

- Structure synthesis per-question (or per-decision-point), naming
  each contributor's position and explaining which element was
  adopted and why.
- When a contributor's position was NOT adopted, explicitly note
  WHY (sequencing, scope, evidence quality) so the good idea is
  preserved as a follow-up rather than lost.
- Scan each rejected proposal element: if there's no follow-up
  iteration, ADR, or CHANGELOG note capturing it, write one.
- Report each contributor's position per question (transparency);
  the synthesis is an integration of the best ideas, never a tally.

`all-or-nothing` finding-disposition is **edge-case opt-in only.**
Reserve it for binary scope decisions ("ship X or not"), security/
safety gates ("approve patch or reject"), or legal/compliance
verdicts where partial acceptance is incoherent. Operator must
explicitly opt in via `goal_packet.convergence.finding_disposition:
all-or-nothing` with rationale.

**Engine state (current, not a follow-up):** the
`config.py` validator accepts BOTH `weighted-synthesis` and
`all-or-nothing` for `workflow.mode=propose-converge`
(`VALID_DISPOSITION_FOR_PROPOSE_CONVERGE`), and `weighted-synthesis`
is the default for every workflow mode. The earlier "engine ENFORCES
all-or-nothing, goal_packet must still declare it until a future
iteration lifts the constraint" caveat is **obsolete** - that
constraint was lifted (iter-three-gaps). Author goal_packets with
`weighted-synthesis` (the default); no all-or-nothing declaration
is required to pass validation.

## Safety interlock first (HEADLINE - highest-value rule)

For **safety-critical / data-loss / bricking / irreversible-risk**
defects: a root-cause-**INDEPENDENT** safeguard that is valuable
even if the root-cause hypothesis is 100% false **MUST** ship in
the same change as the hypothesized fix. **Stopping the bleeding
outranks perfecting the diagnosis.**

Field-proven (ChilipadScreen i2c boot-loop report, 2026-05-15): an
independent boot-loop breaker, made hypothesis-independent *by
design*, un-bricked a medical-safety device and kept it serving
across **two** consecutive consensus iterations whose converged
root causes were both later refuted on-device. It was called "the
single highest-value decision."

Auditable bar: **"would this safeguard still work if the root cause
were entirely different?"** If a reviewer cannot answer *yes* from
the safeguard's mechanism alone, it does not qualify - it is a
disguised bet on the hypothesis, not an interlock.

## Convergence is agreement, not truth

**Convergence measures agreement, not correctness.** Two clean
strict-majority 2-of-2 convergences (and one round-1 *unanimous*
one) shipped root causes that on-device tests then refuted.

**Fast independent unanimity is a VERIFY-HARDER flag, not
confidence.** When contributors agree quickly, suspect a *shared
prior*: independent agents reasoning from the same incomplete
differential is the multi-agent analog of single-agent
rationalize-away (see the disconfirming-evidence doctrine). Unanimity
is evidence only when the contributors reasoned from *different*
differentials - so make the differential visible (the dispatch
templates now require each contributor to state the prior it
reasoned from; at reveal, a shared prior is exposed instead of
laundered as "independent agreement").

### Provisional-until-proven (defined defect class)

For claims **not falsifiable from the artifacts in evidence** -
hardware/firmware state, environment/toolchain, concurrency/timing,
anything refutable only by an *external* observation - a converged
root cause is **PROVISIONAL**. The converged plan's
`falsification.empirical_status` is `pending` until the named
discriminating experiment runs; it then becomes `proven` (the
refutation observation did NOT occur) or **`refuted`** (it did -
the load-bearing terminal state; the hypothesis is dead, the
iteration does not close on it, and the decisive experiment for
the next iteration carries forward). **"Fixed" / "shipped" /
"root-cause-correct" language is forbidden before `proven`.**
(Pure-code defects refutable by a unit test already carry their
proof - no extra ceremony; forcing one there is the theater this
rule is meant to prevent.)

### Anti-theater property (what makes falsification real)

A falsification is real **only if its refuting observation is
(1) pre-specified, (2) a specific observable, and (3) for the
defined class, EXTERNAL to the reasoning that produced the
hypothesis.** External tests can't be rationalized in the room -
that is precisely why the device refuted what code-reading could
not. "We'll test it" is not a falsification; "X at address Y still
returns 0x103 on a clean POWERON" is.

Also name **the single decisive experiment that must run before
the next iteration** (the report's Exp-4 pattern) - the one test
that most cleanly partitions the remaining hypothesis space.

See `docs/workflows/converged-plan-convention.md` for the
converged-plan blocks (`falsification`, `independent_safeguard`,
`decisive_experiment_before_next_iteration`). These are an
authoring convention AND, **as of v1.15.1, machine-enforced**:
`validators/validate_converged_plan.py` + a fail-closed seal-time
gate in `workflow_engine._seal_converged_plan` validate the blocks
(structure + consequence only - never soundness), governed by
`convergence.converged_plan_enforcement`
(`off|warn|graduated|strict`, default `graduated`). The v1.15.0
tag is doctrine-only; machine enforcement exists only from the
v1.15.1 tag forward.

## Dispatching codex / gemini

**`--review-target` must be a `.yaml` review-packet, not a raw `.md`
or `.diff` file.** The peer reviewer sandboxes refuse to read paths
under `consensus-state/`, so the file contents have to be embedded
inline. Use `python -m consensus_mcp._author_review_packet
--iteration-dir <dir> --files <comma-list>` to author a packet with
`defect_target.touched_files_contents` populated, then pass
`<dir>/review-packet.yaml` as the review target.

**Silence watchdog:** dispatches honor `CONSENSUS_MCP_STALL_SILENCE_SECONDS`
(default 180s). The MCP `reviewer_dispatch_*` tools run as async jobs, so
there is no short MCP-side timeout. `agy` (Gemini) prints only at the end,
so its watchdog waits for the full run timeout.

**Proposal-mode dispatch requires `--mode proposal`** on the shell
binaries. The MCP wrappers as of v1.14.0 don't expose this flag -
fall back to the shell CLI for round-1 Workflow A dispatch.

## Gemini 429 handling (priority-tiered)

- **Low-priority iterations** (chores, doc syncs, simple migrations):
  if gemini returns a single 429, skip it and proceed with a 2-AI
  consensus (claude + codex). Don't retry.
- **High-priority iterations** (design questions, security review,
  blocking decisions): allow one retry on 429; skip only after 2
  consecutive 429s.

The signal "skip vs retry" is the cost of getting it wrong - when a
chore goes through with 2-AI consensus, the worst case is "we get a
weaker review"; when a design decision goes through with 2-AI
consensus, the worst case is "we ratify a flawed design."

**Empty gemini output is NOT a 429 - don't burn the retry budget.**
gemini CLI >= `0.43.0-preview.0` refuses headless runs in an
"untrusted" directory: it writes the trust error to stderr and
produces **empty stdout**, which fails as `GeminiOutputParseError`
("Expecting value: line 1 column 1"), often twice (initial +
auto-retry) - looking like a transient 429 but it is deterministic.
**Fixed in v1.15.2:** `_dispatch_gemini` injects
`GEMINI_CLI_TRUST_WORKSPACE=true` into the subprocess env. On
**<= v1.15.1** apply the manual workaround:
`GEMINI_CLI_TRUST_WORKSPACE=true` in the environment that runs the
dispatcher (or MCP server). `--skip-trust` alone is NOT
load-bearing on this CLI version. Diagnose by probing `gemini -p
"reply OK"` directly - the trust error prints plainly. See
`docs/advisories.md` (Advisory 2026-05-15, resolved v1.15.2).

## Codex auth model

Codex uses **token-based auth, not API keys.** If a dispatch hangs
with "AuthRequired" messages, the most common cause is a **secondary
MCP** that codex itself is configured to use - not codex's own auth.
Check codex's MCP config (`~/.codex/config.toml`) for any nested MCP
references; remove or disable the offending entry. Codex's own auth
refresh is rarely the culprit.

## Iteration-state persistence (data-loss risk)

`consensus-state/active/iteration-*/` is **gitignored by design** -
in-flight iteration scratch (proposals, audits, partial reviews)
should not pollute the main branch's commit history. But this means
**a `git clean -fdX` (or a CI build agent that wipes untracked
files) will silently delete your in-progress consensus work.**

Mitigation: `python -m consensus_mcp._snapshot_state snapshot --label
<short-label>` after each iteration close. Snapshots live on the
orphan branch `consensus-state-snapshots`. To recover:
`python -m consensus_mcp._snapshot_state restore --tag <tag-name>`.

For long iterations: snapshot mid-flight too. Cheap insurance.

## Verifying peer-cited file content

When a codex or gemini reviewer cites file content in a finding,
**grep the cited file to confirm the content exists** before
acting on the finding. Reviewers occasionally hallucinate
("README.md line 67 contains @docs/roadmap/v1.14.0-deferred.md"
when line 67 actually contains `@v1.14.0`).

If the cited content doesn't exist (verified via grep), dismiss the
finding with empirical evidence in the commit message:
"codex-rev-NNN dismissed: cited content at <path>:<line> does not
exist (grep shows `<actual>`). Reviewer hallucination."

Don't ignore reviewer findings silently - write the dismissal as a
matter of record so the audit trail survives.

## Verify before invent - cite before propose

**Before introducing any step that touches an external system,
channel, distribution mechanism, or inferred environmental
capability - verify it exists in the project and CITE the
verification source inline.**

The rule applies to publish/install/deploy/distribute steps;
sending messages (Slack, email, webhooks); posting to external
services; uploading to registries (PyPI, npm, Docker Hub,
GitHub Packages); registering anywhere; inferring CI/CD
pipelines, license terms, dependency availability, tool
presence, database schemas - any inferred capability or
channel.

Required citation form: a one-line inline reference next to
the proposed step:
- `verified via README.md:40 - install URL is git+https`
- `verified via .github/workflows/release.yml:12 - publish job exists`
- `verified via curl https://pypi.org/.../json - registered`
- `not found - not proposing` (when verification fails)

**When verification produces DISCONFIRMING evidence (no creds,
no workflow, registry 404), treat that as the SIGNAL - not as
a credential gap to fill.** "no creds" -> check first whether
the channel exists in the project at all; do not jump to
"operator needs to provide creds." Operator pushback ("what
is X?") -> check whether X was introduced by inference rather
than verification; do not jump to "operator unfamiliar with X."

**Anti-pattern to abort on sight:** "I'll handle X and hand
you Y at the end" framing makes invented requirements feel
inevitable. Better framing: "verified-required steps: <list
with citations>; uncertain steps: <list>; please confirm or
correct uncertain ones."

Scope: required for high-impact actions (external system,
channel, irreversible op, anything operator-visible). NOT
required for routine local-dev steps (git status, file reads,
test runs against a known repo).

## Artifact-scoped claims - no global "fixed" or "shipped"

**When making any "fixed", "shipped", "done", "complete"
claim, the claim must be ARTIFACT-SCOPED - naming the
specific version + commit/tag + install path + bundled
content + known residual defects.** Globally-quantified
claims like "X is fully shipped" or "Y is fixed" are
forbidden when the affected surface is broader than the
artifact you actually changed.

**The canonical scenario:** an immutable tag and a dev
branch with a fix are NOT the same artifact. Don't glue
them together. If you fixed something on the v1.14.1 dev
branch, the v1.14.0 tag at commit 8e0dab2 STILL ships the
defect embedded in its wheel/install - name that explicitly.

Required claim form when announcing a fix or completion:
- Name the artifact: `v1.14.1 tag at commit 5f6cfe7`
- Name what the artifact contains: "the corrected skill"
- Name the unfixed surface explicitly: "the v1.14.0 tag is
  immutable and STILL ships the buggy skill; users on
  v1.14.0 need to upgrade to v1.14.1 to get the fix"
- For multi-artifact surfaces, list each with status:
  "fixed in dev branch [ok], fixed in v1.14.1 tag [ok], v1.14.0
  tag still defective [x]"

**Forbidden phrases when surface > what you changed:**
- "X is fully shipped"
- "X is done"
- "X is fixed" (without scoping)
- "the only channel that exists" (when an artifact-content
  caveat is being suppressed)
- "all clear" / "no issues remaining"

## Non-trivial changes go through peer review

Any **non-trivial change to consensus-mcp itself** must go through
peer review (Workflow A if design surface, Workflow B if pure
execution). The threshold for "trivial" is small: typo fixes, doc
formatting, individual log-line tweaks. Anything touching
contributor adapters, dispatchers, tool registration, sealing, or
goal-packet validation = non-trivial.

This rule does NOT apply to the user's own project work using
consensus-mcp as a tool - there, the operator decides what's
non-trivial in their codebase.

## "Consensus" trigger word

When the user says "consensus" in a sentence about reviewing,
deciding, or analyzing - **use the consensus-mcp tools (Workflow A
or Workflow B as appropriate), NOT the older /council skill.**
Council was a single-Claude multi-persona simulation; consensus-mcp
is a real cross-AI workflow with sealed-provenance peer reviewers.

## Release cadence - Friday cut if anything landed

**Cut a release tag every Friday if at least one iteration closed
that week. Release-cut is a procedure with a trigger, not an
ad-hoc decision.**

The structural failure mode this prevents: iterations close
continuously (acceptance gates pass -> done), but the release-cut
ceremony has no trigger of its own. So work accumulates on the
`v<X.Y.Z>` branch indefinitely and downstream pipx/PyPI users get
stale versions while the README documents features they cannot
install. This actually happened - v1.14.0 sat at 37 commits across
iter-0009..iter-0043 over 3 days with a release-ready CHANGELOG
and no tag.

**Cut sequence (apply in order on the v<X.Y.Z> branch tip):**

1. Update `CHANGELOG.md` date stamp to the cut date; add an
   addendum for any iterations that landed after the section was
   first authored.
2. Verify `pyproject.toml` `version` matches the branch.
3. **Bump README install URLs + `## Status` to `@v<X.Y.Z>` on the
   release branch tip - BEFORE tagging.** Since v1.15.4 `main`
   fast-forwards to the just-cut tag, the README *inside the tag*
   IS the GitHub landing page. If it still says the previous
   version, the landing page tells users to install the old
   release the moment `main` advances - the exact bleeding-wound
   this is meant to prevent. Grep `@v<old-prefix>` + the Status
   line; fix all in one commit on the release branch before step 5.
   (Pre-v1.15.4 this was a post-tag dev-branch step; under
   main=tag it MUST be pre-tag.)
   **ALSO verify the INSTALL + HOW-TO-USE instructions themselves are
   current - not just the version number (recurring miss, operator-
   flagged 2026-05-22: usage docs drifted stale repeatedly).** The pipx
   command, the `consensus-init` flags/usage, the quick-start steps, and
   any "how it works" claims must match the CURRENT CLI behavior for this
   version. Spot-check that every documented command/flag actually exists
   and works (e.g. `grep` the flags against the argparser; run
   `--print-defaults`) - stale instructions are a release defect.
4. Run the full test suite; surface regressions before tagging.
   Document any pre-existing known-issue flakes in CHANGELOG so
   they aren't mistaken for v<X.Y.Z> regressions.
5. `git tag -a v<X.Y.Z> -m "..."` on the branch tip.
6. `git push origin refs/heads/v<X.Y.Z> refs/tags/v<X.Y.Z>` (use
   explicit `refs/heads/` and `refs/tags/` to disambiguate; the
   branch and tag now share a name).
7. **Create the GitHub Release (REQUIRED - EVERY cut, no exceptions).**
   Pushing a tag does NOT create a GitHub Release object - the
   Releases page stays stale (showing the previous version) until
   you do this explicitly:
   `gh release create v<X.Y.Z> --verify-tag --latest --title
   "v<X.Y.Z> - <headline>" --notes-from-tag`. **A cut is NOT
   complete until ALL THREE hold: (a) the tag is on origin, (b)
   README + project info are current (step 3 - install URLs, the
   `## Status` line, and the GitHub repo description/topics if they
   changed), AND (c) the GitHub Release exists and is marked Latest.**
   Distribution is git-tag-based - users install via `pipx install
   git+https://github.com/StGarca/consensus-mcp.git@v<X.Y.Z>`; there
   is NO PyPI step. But the operator rule (2026-05-22) is explicit:
   the README/project info AND the Releases page are updated on
   EVERY version, every single time - never leave either lagging the
   installable tag. Optional: `python -m build` for local smoke only.
8. **Fast-forward `main` to the just-cut tag**
   (`git push origin refs/tags/v<X.Y.Z>^{}:refs/heads/main`, or
   `git push origin v<X.Y.Z>-tip:main`). This is ALWAYS a clean
   fast-forward because each release branch descends linearly from
   the previous release tip, which descends from `main`. `main` is
   the GitHub default branch, so this keeps the landing page +
   GitHub Actions CI on the latest released state. Verify with
   `git merge-base --is-ancestor origin/main <tag>` first; if it is
   NOT an ancestor, STOP - that means history diverged and a
   force-update would rewrite public `main` (escalate, do not
   force).
- **Make the release LIVE locally (install-currency - REQUIRED):**
  1. `pipx install --force git+https://github.com/StGarca/consensus-mcp.git@vX.Y.Z`
     (the global install is a non-editable COPY pinned to a tag; `pipx upgrade`
     will NOT move a tag pin).
  2. `consensus-init --install-claude-code --force` (refresh `~/.claude`
     skills/commands to the new version).
  3. **Smoke the INSTALLED binary AND assert its version == `vX.Y.Z`** - the
     stale-pipx failure is a binary that *runs* but reports the OLD version, so a
     "binary runs" check is insufficient.
9. Branch the next release from the v<X.Y.Z> tip: `v<X.Y.Z+1>`
   for hot-patches, OR `v<X.(Y+1).0>` for the next minor. Bump
   `pyproject.toml` on the new branch to the new dev version
   (e.g., `1.14.1.dev0`); add a `## X.Y.Z+1 - unreleased` stub
   to CHANGELOG.md.
10. **Verify** the README on the new dev branch still shows
    `@v<X.Y.Z>` (the just-cut tag) - it should already, because
    step 3 bumped it pre-tag and the dev branch descends from the
    tag. This is now a no-op verification, NOT a bump (the bump
    moved to pre-tag step 3 in v1.15.4 so the tag's README - which
    `main` fast-forwards onto - is correct at tag time). If it is
    somehow stale, that is a bug in step 3, not a routine bump.
11. Push the new branch: `git push -u origin v<X.Y.Z+1>`.
12. **If the just-cut tag has a known issue worth flagging to
    users on older versions** - add an entry to
    `docs/advisories.md` naming the affected versions, the
    issue, the correct upgrade target, and the user action
    required. The advisory is the long-lived record; CHANGELOG
    entries get buried as new releases ship.

**Distribution convention:** consensus-mcp ships via git tags +
pipx, NOT PyPI. README documents `pipx install
git+https://github.com/.../consensus-mcp.git@vX.Y.Z`. No
`twine upload`, no `~/.pypirc`, no PyPI workflow exists. If you
catch yourself proposing a PyPI step, stop - you're adding a
channel that is not part of this project's release flow.

**Branch convention (evolved in v1.15.4):** `main` is the GitHub
default branch and tracks **the latest released state**. After
every release cut, `main` is **fast-forwarded to the just-cut tag**
(cut-sequence step 8) - never a merge, never a force-push (the
fast-forward is always clean because each release branch descends
linearly from the prior release tip, which descends from `main`).
Active development happens on the `v<X.Y.Z>` branches, which are
self-contained and branch from the previous release's tip; they are
NOT merged into `main` - `main` only ever *fast-forwards* to a
released tag. Rationale: the pre-v1.15.4 "main frozen forever"
convention left the GitHub landing page stuck at v1.13.0 and
GitHub Actions CI dormant from v1.13.0->v1.15.3 (CI triggered only
on `main`). `main` = newest tag; `v<next>` = where work lands;
release = the moment a tag is pushed AND `main` is fast-forwarded
onto it.

**Keep `main` CURRENT - never frozen (operator, 2026-05-22):** the
GitHub landing page IS `main`, so `main` must always reflect the
current state. Beyond the at-cut fast-forward to the tag, `main` may
also be fast-forwarded to the active dev-branch tip *between* cuts to
keep the README / landing page current (clean FF only; `git
merge-base --is-ancestor origin/main <tip>` guard; never merge, never
force). The v1.17.x cuts had DRIFTED - they left `main` frozen at the
PII-scrub root `d948334` instead of FF-ing per step 8; this was
corrected at v1.18.x (`main` fast-forwarded to the v1.18.1 tip). If
you ever find `main` lagging the latest release/dev tip, FF it.

**Sanctioned-exception carve-out (added v1.15.5):** "never a
force-push" governs ROUTINE operation. A **full-history rewrite**
(`git filter-repo`) - e.g., an account migration or a
provenance/secret scrub that must reach immutable commit/tag
messages - is the ONE sanctioned reason to force-push `main` and
re-create every tag. It is NOT routine and requires ALL of:
(1) explicit operator authorization of the rewrite specifically
(not implied by any other task); (2) a verified full backup
bundle (`git bundle --all`) stored OUTSIDE the repo before
running; (3) post-rewrite verification BEFORE pushing -
`git grep`/`git log --all` show zero target strings across all
refs, all release tags + branches still present, full suite green
on the rewritten tip (token replacements must stay internally
consistent); (4) force-push all branches + all tags together, then
re-verify `origin/main` == local. Precedent: the 2026-05-15
GitHub-account migration (handle now `stgarca`) + former-upstream
provenance scrub (127 commits, 18 branches, 66 tags rewritten;
backup `consensus-mcp-prefilter-backup-20260515-125935.bundle`).
Consequence to state plainly when it happens: every published tag
SHA changed; tag-pinned `pipx install @vX.Y.Z` URLs keep working
(tags moved) but any raw-SHA pin or old clone is dead.

**Variations:**

- **Empty-week skip:** if zero iterations landed, no cut. Never
  cut empty releases.
- **Hot-patches between Fridays:** cut as `v<X.Y.Z+1>` whenever a
  hot-patch lands; don't wait for Friday for a fix release.
- **Operator hold:** the operator may explicitly delay a cut
  ("hold v1.14.0 until iter-0050"). Default without explicit
  hold is "cut Friday."

Release-cut is itself an operating procedure - not a design
decision and not subject to peer consensus.

## When in doubt

The conservative move is **Workflow A with all enabled contributors**.
The extra wall-clock is bounded; the cost of ratifying a flawed
design via 2-AI audit is not.

If a dispatch is failing in a way you can't diagnose in 5 minutes,
stop and ask the operator. Don't keep retrying - there is almost
always a config or auth issue upstream, and burning more dispatches
deepens the hole.
