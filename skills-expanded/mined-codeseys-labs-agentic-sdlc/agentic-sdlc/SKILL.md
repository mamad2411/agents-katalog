---
name: agentic-sdlc
description: >-
  Fires at the intake of project-scale work — framing, planning, executing, reviewing, or
  driving an agentic SDLC run, including Seeds-backed worktree waves, backlog-zero missions,
  multi-agent implementation, and concurrent critique — at the moment a session opens an
  SDLC-activated repository whose queue holds open seeds, and on the symptom of multi-agent
  implementation being improvised ad hoc instead of run as a planned wave. The baseline uses
  the current host's native agent and subagent capabilities and requires no cmux or tmux.
  cmux is an optional non-load-bearing view/event layer only when already active or
  explicitly requested.
---

# Agentic SDLC Orchestrator

Use this skill to run a repeatable, project-generic implementation loop. The skill gives
policy and coordination guidance only. It is not:

- an actor
- a credential
- a permission grant
- an evidence store
- a Git executor
- a validator

`Agent entrypoint -> provider-native delegation (or direct execution) -> Seeds queue -> worktrees -> tests/review -> squash/rebase -> PR`

Roles submit findings or candidate changes. Reviewer and critic labels are recommendations.
They never authorize an outward effect. One macro conductor records evidence and keeps the
queue. Only the integrator may execute an already authorized fan-in mutation. The
integrator never acquires the user's authority.

Keep the active host session as the macro conductor. Use its native delegation tools by
default. The full Frame -> Ship loop is available only after the required Git, Seeds, gate,
trust, and selected-adapter capabilities are probed and verified. Missing, unpinned,
untrusted, or ambiguous required capability fails closed. Add cmux only when it is already
active and useful for visibility or event messaging. Never install, start, or enable cmux or
tmux merely to run this skill. Use Seeds as the queue of record.

Global bundle distribution is a separate lifecycle plane from per-project activation.
Activate a repository through the `/sdlc-init` runbook (or the same intent on a non-Claude
host) before the first Frame or Wave. Activation establishes a reviewed tracked Git
baseline, Seeds, pinned gates, trust, and shared AGENTS.md guidance. If the target has no
Seeds queue, route to `/sdlc-init` and stop; Frame and Wave never improvise activation.
Mise is the only bootstrap prerequisite. From a reviewed distribution checkout, run the installed
flagship tool `seeds-launcher.mjs bootstrap --distribution <distribution-root>` under Node
`22.23.2`. Bootstrap requires an exact clean Git distribution root. It rejects any nested checkout
path. It also rejects a distribution whose tracked, staged, untracked, or ignored content differs
from the exact `HEAD` tree. Bootstrap alone runs the reviewed `mise --locked install`. That install
uses only the root `mise.toml`/adjacent lock, a fresh private mise data/cache/home, the fixed
official npm registry, distinct empty npmrc files, and a disabled hooks/config environment. Ambient
HOME, npmrc/registry, and mise config/data/cache cannot select acquisition. Bootstrap then resolves
exact config-free roots and atomically publishes an active tuple receipt. It verifies the executing
Node and the recorded Node are exactly `22.23.2`, and Bun is exactly `1.4.0`, and the package/bin
layout matches exact `@os-eco/seeds-cli@0.5.15`. It permits only the real package's benign string
`engines.bun` compatibility declaration; it rejects actual Bun/config/TypeScript/macro/preload
controls. It records a trusted empty Bun configuration, the exact Git root/commit/tree plus
`mise.toml`/`mise.lock`, and typed tree/file hashes. It retains the preceding receipt for explicit
rollback. A structurally intact preceding receipt that records a superseded tuple is retained and
its superseded tuple named, never refused: establishing a new tuple is precisely what bootstrap is
for, and a pin bump is the one expected reason a prior receipt disagrees with the launcher's
constants. Malformed preceding state is still refused and never repaired, and every other verb still
refuses a receipt whose recorded tuple is not the current one.
The receipt establishes an execution integrity boundary against ordinary accidental
drift. It does not establish tarball/transitive authenticity. It does not stop a
same-UID TOCTOU attacker that races verification against execution. An npm version, a backend,
and a lock do not authenticate a tarball or its transitive dependencies.

After an explicit successful bootstrap, `Seeds(<target>, <args...>)` is implemented by
`seeds-launcher.mjs inspect --target <target> <args...>` under the exact recorded and currently
executing Node `22.23.2`.
`inspect` never installs, invokes mise, or networks. It never discovers replacement tooling,
repairs state, or accepts ambient provenance. It loads and validates only the active receipt and
the recorded current hashes. It accepts only `--version`, `prime`, `ready [--format json]`, and
`blocked [--format json]`, and rejects every other form before Bun starts. Node has `shell:false`
and invokes the exact recorded absolute Bun/entry pair with `--config=<trusted-file>`,
`--no-env-file`, and `--no-install`. The child process gets only a short environment allowlist.
Its PATH holds only the separately resolved and recorded Git directory, with portable
system/global Git config isolation. Target `bunfig`, `.env`, package config, ambient `BUN_*`,
`NODE_OPTIONS`, npm/mise overrides, and unreviewed Seeds debug variables have no execution effect.

The conductor's durable queue write is `seeds-launcher.mjs record --target <target>
--queue-writer conductor --expect-queue <expectation> <verb> ...`. An absent queue has exactly one
admitted form: `--expect-queue absent init`. It inherits the whole `inspect` admission, refuses any
existing/partial/file/symlink/redirected `.seeds`, snapshots `.gitattributes`, and refuses a
non-UTF-8 or exact-line/substr-match-ambiguous prestate before mutation. It invokes exact pinned
`init --json` and admits only the closed five-file initializer surface plus the precise missing
merge-union append. A failed child after either surface moves is an unknown effect; no movement is
a clean refusal. An existing queue requires its exact sha256 and admits only create or update — no
removal, pruning, closing, claiming, syncing, or other standalone mutation. It reuses the same
receipt, current-hash checks, absolute Bun/entry pair, and environment allowlist and adds a
compare-and-swap plus readback. A queue that moved is refused with both digests named. The observed
poststate must equal the prestate plus exactly the requested delta; unrequested fields, rewritten
or reordered neighbouring records, queue-file surface changes, and unbounded plan transitions are
refused. A prestate the writer would silently rewrite is refused before it starts. The explicit
`--queue-writer conductor` acknowledgement keeps the seam from becoming generally writable. The
queue's own lock stays the queue writer's; the seam adds none. A verified record is the conductor's
own evidence and authorizes no push, PR, merge, deployment, or other outward effect.

## Repo Location

This skill is maintained in a private repository. The checkout location varies
per machine. Locate the checkout by searching for this skill's directory
(`skills/agentic-sdlc/`) rather than assuming a fixed path or forge name.

When this skill refers to bundled scripts, use the repo copies:

- `<repo>/scripts/check-agentic-sdlc-prereqs.sh`

## Offline activation preview

From an installed copy of this skill, run:

```text
<installed-skill>/tools/offline-inspect.py --target <path>
```

The command is deterministic, offline, read-only, and Python-standard-library only. It inspects
local filesystem structure without subprocesses, providers, credentials, environment discovery,
network access, repairs, or target writes. Its `READY` / `NOT_READY` result is **preview readiness
only**: it does not establish Git-wave readiness or authorize activation. The explicit `skip` item
excludes PRIME apply, workflow overlay, gateway, routing, Seeds, archives, V7, config, and queue
mutation.

## First Moves

1. Confirm the project is activated before execution:
   - If the Seeds queue is absent, route to `/sdlc-init` (or the same activation intent on a
     non-Claude host) and stop. Do not create a queue, infer activation, or start a Frame/Wave
     from the missing state.
   - For an active queue, run `Seeds(<target>, prime)` and inspect
     `Seeds(<target>, ready --format json)`, `Seeds(<target>, blocked --format json)`, plus repo
     docs/ADRs/roadmap.
   - Check `git status --short` before planning worktrees.
2. Detect the host-native execution plane first:
   - Inventory direct execution, role agents/subagents, background delegation, and native
     result or messaging channels available in the current host.
   - Treat those capabilities as candidates, not proof of readiness: probe required
     capability, trust, and adapter/model readback before selecting the path. Missing,
     unpinned, untrusted, or ambiguous capability is a fail-closed stop.
   - Probe cmux only when `command -v cmux` succeeds and `CMUX_WORKSPACE_ID` is set. If
     either check fails, skip cmux silently. tmux is never part of the baseline probe.
3. Decide the run shape:
   - A certified delegation route: use provider-native workers in a Seeds-backed worktree wave.
   - No certified delegation route: a Frame may authorize exactly one bounded, non-delegated
     conductor execution only when the ready Seed is small, has an observable done condition, and
     fits one clean dedicated Git worktree. It has the same framed scope, acceptance criteria,
     gate, stable-snapshot review, and conductor-only queue reconciliation as a Wave, but has zero
     workers, zero model spawns, and makes no `RuntimeAssignment` claim.
   - Stop rather than use that exception when work needs a second direct pass or retry, another
     worker or model, parallel work, unbounded discovery, or review that cannot be independent of
     the executing conductor. The exception never turns a missing certified route into delegated
     execution.
   - Unclear architecture: discover -> research if needed -> plan -> act -> review.
   - Large backlog-zero work: bounded waves with continuous Seeds reconciliation.
4. Run `scripts/check-agentic-sdlc-prereqs.sh` from the repo root for local checks. Missing
   optional adapters must not block the run. Load `references/cmux-integration.md` only when
   cmux is already active or explicitly requested.
5. Create or update Seeds before implementation. Do not let findings live only in chat.

## Control Contract

Use this phase order unless the task is clearly smaller:

1. Frame: define done, constraints, repo state, queue state, and allowed blast radius. Seal a
   Mission-shaped Frame's durable objective with `tools/mission-contract.py define`, and record
   the observed repo/queue facts from Git and the queue directly.
2. Discover: assign read-only workers across code areas. Require file/line evidence.
3. Research: only for external or load-bearing unknowns — a deep-research pipeline if the
   host provides one, otherwise primary sources directly.
4. Plan: emit workstreams, dependencies, worktree strategy, gates, rollback, and Seeds updates.
   Record the plan where the wave's later evidence can be read against it, and re-read the observed
   repo state from Git directly before Act begins.
5. Act: launch workers in separate worktrees for independent workstreams.
6. Review: review stable branch/worktree snapshots, not only worker summaries. Read what each node
   actually did from Git — `git log --format='%H %s' <base>..<branch>` and
   `git show --stat <integration-commit>` — and verify each gate receipt's envelope and correlation
   graph with `tools/receipt-envelope.py verify`/`check-graph` before trusting it.
7. Reconcile: turn findings into Seeds, fix blockers, run gates, and update docs. State the wave's
   one terminal outcome — accepted, remediation-progress, blocked, aborted, failed, or
   unknown-effect — from the recorded evidence in `docs/evidence/waves/<wave-id>.md`, never from
   worker summaries. The first three are what the evidence shows; the last three are how the
   execution ended, and only the conductor's own record carries them. `unknown-effect` dominates
   and is never talked down by other evidence; an ended state overrides completion evidence; and
   an absent outcome is a named gap that fails closed, never an assumed accepted.
8. Ship: squash/rebase, sync Seeds, open PR or commit according to repo policy. Before proposing
   any commit, PR, or squash text, load `../change-writing/SKILL.md` to author it; this phase still
   owns the squash/rebase/PR operations and the human still authorizes publication.

Use backflow when review reveals an earlier phase was weak: re-enter Discover, Research, or Plan
with a scoped task instead of restarting the whole run. Compare the recorded plan against what the
branch actually contains before deciding backflow scope, and treat a scope or authority change as
new work needing a new approval rather than a continuation of the approved one.

## Wave Acceptance Rules

Four rules decide whether a wave may be called accepted. They are read, not derived, and each is
checkable against Git and one recorded receipt.

- **No self-review.** The node that reviews a workstream is a different node than the one that
  implemented it. A row reviewed by its own author is unreviewed.
- **Approval is dated before the fan-in.** The operator's verbatim approval carries its date, and
  that date precedes the integration commit's committer date. An authorization recorded after the
  effect it authorizes is not an authorization.
- **The gate passes on the merged snapshot.** Re-run the repository gate after integration and keep
  its receipt; a receipt from a worktree head says nothing about the merged tree.
- **A worker summary is never acceptance evidence.** Messages, status lines, and worker reports are
  advisory notifications. Acceptance reads commits, diffs, and the gate receipt.

Record all four for each wave in `docs/evidence/waves/<wave-id>.md`, copied from
`docs/evidence/waves/TEMPLATE.md`. A complete record is evidence only; it authorizes no push,
publication, PR mutation, merge, or deployment.

## Delegation Rules

- Prefer the host's native roles, subagents, workflows, teams, or background tasks. Direct
  execution is only the single bounded conductor exception stated in First Moves: it exists only
  when no certified delegation route is available, and is never a worker/model spawn or a
  `RuntimeAssignment` claim.
- Every actual worker or model spawn is delegated execution. It requires the certified
  `RuntimeAssignment` admission boundary below, admitted by `tools/runtime-assignment.py admit`
  and classified afterward by `tools/runtime-assignment.py classify`; a missing, inherited,
  unresolved, or unverified route stops before dispatch and spawn. Do not relabel a worker as
  direct execution to bypass it.
- Require every delegated worker to return a structured report for conductor capture. A
  write-capable worker may also maintain its assigned artifact; for a read-only worker, the
  conductor persists the captured submission. The conductor records each node's role, resolved
  model id, disposition, commit, and reviewer in the wave's evidence file, and reads a
  write-capable worker's claimed output back from its commit before treating it as captured. Treat
  messages, status, and summaries as advisory notifications, not acceptance evidence or authority.
- For long-running work, use the host's native background or persistent-task mechanism and
  durable artifact files. Do not hold one blocking call open indefinitely.
- Use Claude Code workers for nested dynamic workflow execution on one bounded workstream. Do not let a nested Claude workflow own the whole project queue unless explicitly requested.
- Use Codex workers for implementation, refactors, tests, docs, repo inspection, and review when provider-native Claude workflows are not needed.
- Keep nested orchestration to one mid-tier at most and give each tier an explicit worker list,
  regardless of delegation backend.
- Before any model dispatch, load `../model-tier-rightsizing/SKILL.md`. Classify the
  artifact into the four semantic tiers and choose within the eligible Sol/Fable, Terra/Opus,
  or Luna/Sonnet pair by task fit, independent perspective, quota, and verified transport.
  The caller must inject a certified exact model ID and **explicit requested effort** for
  every worker; provider-neutral role definitions do not select a model. For an OCX Ultracode
  Workflow, every explicit `agent()` model ID must use its exact `[1m]` request form. If that
  marked tuple is not certified, admitted, and readable through the required request/identity
  evidence, stop before dispatch and return one `SeedProposal`; never fall back to the
  unsuffixed form. The `[1m]` request remains distinct from base-ID identity readback and does
  not prove served context. The canonical marker rule is in
  `../model-tier-rightsizing/SKILL.md#ocx-ultracode-workflow-marker-rule`. Stop before dispatch
  when a route is inherited, unresolved, or unverified. No host-default policy or artificial
  all-six representation.
- Keep one macro conductor responsible for Seeds adjudication, worktree ownership, and
  evidence-backed recommendations. The conductor alone mutates Seeds; an authorized
  integrator alone performs an already-authorized fan-in. Humans authorize push,
  publication, PR mutation, merge, deployment, credential, and external evidence-store
  operations.
- If already inside cmux, optionally surface run state. Attach a `tmux` viewer only for an
  existing tmux-backed session; never create that dependency for a native run.

## References

Read only what is needed:

- `references/sdlc-loop.md`: phase gates, backflow, done criteria.
- `references/routing.md`: the moment→skill routing table for all thirteen skills in this bundle — the lifecycle moments and symptoms each description expresses, the two deliberate exceptions, and the four named refusals (no sticky modes, no standing-order descriptions, no self-insertion into delegation, no global-configuration capture) that bound any priming surface.
- `references/seeds-worktrees.md`: Seeds queue, worktree wave, squash/rebase, PR handling, and
  the canonical in-workspace `.worktrees/<seed-id>-<slug>/` substrate rule.
- `references/worktree-lifecycle.md`: one wave worktree end to end with the refusal and
  recovery case for every step — create (one writer, path-before-branch guard), gate inside
  the worktree, review from a snapshot, integrate (why this repo prefers squash), reconcile
  through the conductor-only record seam, and clean up (`remove`/`prune`/branch deletion,
  dirty and unmerged cases). Carries the executed Git facts and the harness-worktree
  interaction.
- `references/cmux-integration.md`: optional cmux view/event integration. Load only when cmux is already active or explicitly requested.
- `references/delegation-planes.md`: native per-provider decision matrices, cost ladder, and write-conflict rules.
- `references/worktree-integration.md`: fan-in hazards — merge-base footprint (not HEAD diff), placeholder-trap assembly, re-gate-on-main (worktree-green ≠ main-green), clean 3-way apply ≠ semantic correctness, squash-scope discipline.
- `references/mission-loop.md`: the autonomous backlog-zero doctrine — milestone-blocking classification (8 classes, only ACTIVE_MILESTONE executes), seeds-first no-inline-fixes, WIP caps, priority math, concurrent critique team, honest definition of done. Read for MISSION-shaped assignments ("drive the backlog to zero", "keep going until done").
- `references/tiered-orchestration.md`: mission integration, canonical routing handoff,
  native-first capability ladder, bounded backflow, and worker lifecycle at scale.
- `references/deep-work-loop.md`: the bounded seven-phase deep-work loop for ONE workstream
  (frame → map/research → decide → act → verify → critique → reconcile) — artifacts and
  SeedProposals only, no second queue, no publication/integration authority, an explicit
  bounded delegation cap, and single-hop pointers for effort routing and fan-in. Read when a
  single workstream needs the full loop shape rather than a whole backlog-zero mission.
- `../model-tier-rightsizing/SKILL.md`: required router before any model dispatch; its
  canonical calibration is the sole generation-specific routing authority.
- `../change-writing/SKILL.md`: message authoring, output-only — commit, PR, squash, and
  draft-review text. It never stages, commits, pushes, mutates PRs, merges, or deploys.
- `references/research-team.md`: evidence-graded multi-agent research for standing research efforts — the evidence ladder (promote slowly, downgrade quickly), role separation-of-powers (scout ≠ novelty-judge; attacker ≠ fixer; writer ≠ originator), one-loop discipline with a recorded next-action, greenfield/brownfield loops, cheapest-decisive-experiment rule, gates-as-executables.
- `references/evidence-discipline.md`: whether any advisory submission's claim may be made at all — the five-class evidence vocabulary, the anti-inflation rule (a class is assigned once and never raised later), disposition-row/gap-register discipline, and the receipt-is-not-a-control-when-author-equals-verifier rule.
- `references/readiness-composition.md`: which surface owns each pre-effect readiness
  dimension and in what order — `ccodex sdlc doctor` (host and install state) and the
  Git-anchored wave-effect read at `/sdlc-wave` step 8 — plus why no unified readiness
  guard is queued (`agentic-sdlc-9857`).
- `references/jj-vcs.md`: a one-release refusal pointer; Git worktrees are supported and no
  alternate VCS substrate is activated by this bundle.
- `references/skill-authoring.md`: admission floor, the four-gate test, the ≥2-of-5
  promotion test, the foreign-skill-library rule (this bundle ships only its own skills and
  never fetches a third-party library), and retire-by-redirect for deciding whether a
  candidate earns its own `SKILL.md` versus a section of an existing skill or a
  `references/*.md` file. Read before adding, revising, or retiring any skill in this
  bundle.
- `references/worktree-failclosed-tests.md`: a language-agnostic test-design contract for
  fail-closed worktree isolation — planted-violation cases (occupied branch, non-git cwd,
  throwing observer, mid-flight abort, timeout), redaction and start/end pair-completeness
  assertions, and the two happy-path controls. A future implementer's spec, not evidence
  that this repo already runs isolated dispatch.
- `references/mermaid-authoring.md`: authoring Mermaid diagrams for ADRs, design docs, and
  review artifacts — perspective scoping, the leaf-or-group depth rule, mandatory edge labels,
  node caps, and the execution-verified parse traps (including the ones that exit 0 and draw
  the wrong diagram). Authoring only; rendering belongs to the pinned rendering pipeline.

Bundled role agents (installed globally by `scripts/install-skill-bundle.sh`), each in
Claude (`agents/claude/*.md`) and Codex (`agents/codex/*.toml`) form:
`sdlc-cartographer` (read-only Discover mapper — file:line evidence, actual gate
commands, unknowns-that-would-change-the-plan), `sdlc-planner`, `sdlc-implementer`,
`sdlc-reviewer`, `sdlc-researcher` (bounded load-bearing-unknown resolution,
stops-when-decided), `sdlc-critic` (the standing critique team — snapshot-only,
classified seeds, attacks-never-fixes), `sdlc-integrator` (the ONLY merging agent —
merge-base footprints, placeholder-trap assembly, re-gate-on-integration), and
`sdlc-documentarian` (read-only documentation worker — runs every checkable sentence,
proposes evidence-linked doc refreshes for conductor capture, writes only its own
artifact). The full loop
wiring: cartographers (parallel, per area) → planner → implementers (one per worktree)
→ reviewers → integrator, with the critic standing concurrent, researchers on demand,
and the documentarian after a wave lands. REPO-SCOPED extra roster: `agents/codex/research/` carries the 17-role
research team (see its README — installed per-repo via the codex-research-os scaffolder,
never globally). Slash commands (Claude Code): `/sdlc-init`, `/sdlc-frame`, `/sdlc-wave`,
`/sdlc-mission`. Other hosts invoke the flagship skill with the same activation/frame/wave/mission intents. Optional cmux bus helper: `scripts/cmux-bus.sh` (pub/sub/seq).

## Hard Stops

- Do not run write-capable workers in the user's dirty checkout. Use a clean worktree.
- Do not close Seeds from worker claims alone. Verify files, tests, and acceptance criteria.
- Do not install, start, or enable cmux or tmux unless the user explicitly requests that environment change.
- Do not recursively launch agents without a bound: cap workers, passes, and review/fix rounds;
  charge each pass against the conductor-owned ledger with `tools/pass-budget.py charge` (or
  inspect it with `status`) so the cap is evidence-backed, not memory.
- Do not push, force-push, rewrite history, alter secrets, or change CI settings unless the user explicitly authorizes that action.
