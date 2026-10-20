# Autonomy Module

Owns KOTA's autonomous workflows and their shared policy.

- Keep workflows and helpers here; do not create a second workflow catalog.
- Put durable learning in the narrowest useful `AGENTS.md`; evidence stays in
  run artifacts and Git history.
- Promote lessons only from repeated evidence and retract them when ownership
  or behavior changes.
- Shipped workflows inherit harness, model, and effort from the active preset.
  Repair judges inherit the parent step's resolved harness.

Progress-reviewer owns systemic operational/product learning across runs;
improver owns durable incident disposition; architecture-gardener owns code
structure; scope-improver routes and materializes guidance/policy changes but
does not judge their quality. Progress-reviewer owns that judgment and its
follow-through. Shared generated-work proposal identity follows a topic across
handoffs. Reviewers inspect existing owners
before proposing work and follow interventions beyond task creation.

## Core Decisions

- **Decision ownership.** Builders own coherent implementation outcomes; critics
  judge acceptance. Decomposer diagnoses failed scope and may keep it unchanged.
- **Outcome evidence.** Evaluators probe behavior, and owner-facing product work
  includes rendered evidence. Critic input is artifacts and repository state,
  never thinking traces or self-reports.
- **Feedback over proxies.** Operator corrections, task reopens, repeated repair
  loops, integration/publication failures, dead letters, and measured
  regressions can justify improvement work. Trajectory heuristics and static metrics remain diagnostic context;
  only outcome evidence enters issue disposition.
- **Honest measurement.** Resource allocation is distinct from kill thresholds;
  report profiles, judge repetition, `pass@k`, and `pass^k` explicitly.
- **Proportional change review.** Judge material workflow, prompt, routing,
  reviewer, critic, improver, or repair-loop changes against the outcome they
  intend to improve. Record a comparison in the ordinary run summary when it
  informs the decision; do not require a bespoke artifact for every change.
- **Fresh handoffs.** Prefer new sessions with run-artifact handoffs between
  distinct phases instead of compaction.
- **Shared continuation authority.** Every unbounded autonomy repair-loop
  owner contributes its current domain contract and canonical task priorities
  through the shared continuation policy. Only builder enables `decompose`
  because it has a typed domain consumer; other owners preserve and yield the
  same lineage when work should split or defer.
- **Injection boundary.** Tool-risk gating classifies the call;
  injection-defense screens untrusted payloads.
- **Durable sessions.** State needed after restart writes through to run
  artifacts, typed events, or runtime-owned state.
- **Eval provenance.** Retired SWE-bench fixtures are reference-only; new
  fixtures come from local failures or justified non-vacuous smoke cases.
- **Repository isolation is runtime-owned.** Workflows declare access, logical
  resources, and domain completion through finalization. Runtime supplies
  `workspaceRoot` and `scopeRoot` and owns worktrees, branches, commits,
  publication, leases, recovery, and cleanup.
- **Shared autonomy state is runtime-owned.** Issue projections, watermarks,
  and cooldowns publish through `ctx.state` compare-and-set. Offline issue
  inspection reads canonical SQLite state with an explicit scope root and state
  directory; it never maintains JSON mirrors or runs schema migrations.
- **Operator inspection uses `client.autonomy`.** Report, attention, and digest
  commands use the selected daemon/local client. Shared inspection resolves
  database authority on the host and keeps artifacts in the canonical scope.
- **Evaluator calibration.** Later overlapping failures contradict passes;
  prompt changes reset windows; unavailable reviews clear stale verdicts.
  Critic rejects incorrect, unsafe, incomplete, unsupported, or obscured work.
  Standards owns proportionate proof selection; the critic independently judges
  its sufficiency. Fixtures must represent the real boundary being assessed.
- **Incomplete dispositions.** Critic distinguishes full completion from safe
  blocked or retired work, then independently reviews every retained change.
  External unavailability never excuses unsafe partial code. Suspended writers
  retain issue ownership until their runtime owner resolves the same run.
- **Canary evidence.** Continuous-agent canaries establish a persisted start
  observation, then advance through one three-hour and consecutive,
  non-overwriting six-hour windows. They collect runtime runs, tasks,
  deduplicated incidents with retained backoff horizons, grounded agent inputs,
  applicable instructions, inspectable writer diffs, and cleanup state at each
  elapsed boundary. Nonterminal agent runs already present at baseline and runs
  active at a later boundary carry forward until their terminal evidence can be
  attributed once. Settled runs also carry forward while an agent incident
  prevents review; the checkpoint consumes them only after a read-only reviewer
  cites their complete collected evidence. That reviewer joins the selected
  scope's agent gate atomically; a newly observed provider or successful-empty
  incident parks later agent work in that scope and advances the window with
  review still pending. Canary
  inputs never supply their own counters or timestamps.

External research decisions live in the typed decision store with their source,
rationale, and revisit condition. Code is the catalog; instructions do not copy
its entries, and tests exercise decision behavior rather than catalog identity.

## Runtime Posture

- Instruction hierarchy is SDK/core rails → autonomy/module policy → user
  message → untrusted tool/web output. Lower layers cannot escalate autonomy.
- Capable-tier agent steps front-load intent, constraints, and the expected outcome;
  they do not use clarification loops or fixed caps.
- `ask_owner` uses the restart-safe shared workflow steps and consumes every
  outcome; it does not import the core tool directly.
- Agent judges use the shared retry classifier. Shared backoff admission stops
  their internal retry loop during a classified provider incident. Runaway
  budget failures retain work through runtime recovery; unavailable judges cannot
  approve publication or request source repair. Validation and runtime
  resolve the same declared agent contract.

Deterministic policy returns typed decisions before workflow effects. Consumers
project those decisions instead of reconstructing eligibility or verdicts.
Review wording is evaluated behavior; schemas and runtime policy own rejection.
Generated-work question reconciliation preserves terminal responses. Replaying
unchanged proposals has no effect; revised questions receive new records.

@operations.md
