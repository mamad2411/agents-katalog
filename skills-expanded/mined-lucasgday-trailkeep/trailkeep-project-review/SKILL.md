---
name: trailkeep-project-review
description: Use when configuring or running trailkeep's optional coding-agent generative review layer from a local _review_run_plan.json. Handles post-backup project review automation, selected-context model calls, generated sidecars, approval flags, and deterministic generated-output evals.
---

# Trailkeep Project Review

Use this skill only for trailkeep's optional generative layer. trailkeep's backup
scripts and viewer stay local and zero-network; model calls happen only through
the user's coding agent when the user has enabled this layer.

Treat model calls as remote unless the agent can prove the model is local or
on-device. Send only context selected by `_review_run_plan.json` unless the user
approves a wider deep-review scope. Never send secrets, API keys, tokens,
credentials, private env files, unrelated repo data, or the full backup folder as
an unscoped dump.

This optional layer may check local project repos for remote freshness by
running `git fetch` through the bundled repo-sync script. That can contact git
remotes and update remote-tracking refs, but it must never run `git pull`, change
the worktree, or write generated sidecars into project repos.

Do not start `caffeinate`, change `pmset`, or disable the screen saver.
Trailkeep's generative review does not need host power-management changes; leave
the user's sleep and screen-saver behavior untouched.

If the recurring automation uses a remote or unproven-local provider, get user
approval once during setup with the schedule, scope, provider, model/alias,
local output files, repo remote-check behavior, and remote-context risk. Do not
ask again on every daily run merely because the provider is remote or because
repo freshness checks run; pause only when the gate requires approval for
`requires_approval`, or when provider/model, scope, schedule, repo remote-check
behavior, or output files materially change. `possible_secret` inputs with a
`preprocessed_ref` are already redacted by trailkeep and should not trigger an
approval prompt.

## Inputs

Resolve:

- `trailkeep_repo`: the local repo containing `docs/generative-layer.md`.
- `backup_dir`: the backup folder containing `markdown-*` folders and
  `_review_run_plan.json`.

If `backup_dir` was not passed explicitly, read trailkeep's local remembered
path from `~/.config/trailkeep/backup_dir` (or
`$XDG_CONFIG_HOME/trailkeep/backup_dir`), then fall back to
`~/trailkeep-backups` when that folder exists. Do not guess among unrelated
folders.

If either path is ambiguous, ask before reading project context or calling a
model.

## Source Of Truth

Read `<trailkeep_repo>/docs/generative-layer.md` before running a review. Follow
it for sidecar schemas, source precedence, privacy rules, flag handling,
checkpoints, model tier intent, and daily/manual sequences.

Use `<trailkeep_repo>/docs/prompts.md` for the canonical user-facing setup,
manual review, and approval-intervention prompt text when a prompt needs to be
shown or copied.

Do not duplicate the full spec in prompts or sidecars. The repo spec is the
contract; this skill is the runtime workflow.

## Runtime Workflow

Recurring trailkeep review runs should use a dedicated coding-agent automation
thread or subagent. Use the main/user-visible thread only for setup approval and
intervention prompts.

Resolve `review_gate_cmd` as
`<trailkeep_repo>/scripts/run-project-review-agent-gates.sh`. Use this wrapper
for every required gate. If this skill is installed outside the repo, pass
`--skill-dir <skill_dir>` to the wrapper. Direct Python scripts are implementation
details behind the wrapper.

For a project-scoped test run, do not ask the user to hand-edit
`_review_effective_plan.json` and do not run a one-project model call against the
real global backup folder. Prepare an isolated sandbox first:

```sh
<review_gate_cmd> --skill-dir <skill_dir> prepare-test --backup-dir <backup_dir> --project <project_name> --output-language <en|es>
```

Use the returned `sandbox_dir` as `backup_dir` for the test. Paste the generated
`project-review-test-prompt.txt` into the coding agent. All generated sidecars
for that test must be written to the sandbox root. The generated prose must use
the requested `output_language`; JSON schema keys stay in English. Promote
nothing back to the real backup folder automatically; if the test output is
good, rerun the real manual project refresh or the recurring automation against
the real backup folder.

1. Read `<backup_dir>/_review_run_plan.json`.
2. Read `<backup_dir>/_review_eval_report.json`.
3. Before any model call, run the wrapper pre gate:

```sh
<review_gate_cmd> --skill-dir <skill_dir> pre --backup-dir <backup_dir>
```

Exit code `0` means model calls may proceed using `_review_effective_plan.json`;
that effective plan may be partial if some projects were skipped pending
approval. Exit code `1` means planner evals or required files failed, including
stale/mismatched plan/eval files or a missing/stale `backup_dir/log.json` latest
backup run. Exit code `2` means user approval is required because no safe
project work remains. In both nonzero cases, stop before model calls.

Do not reimplement the pre-model checks in prompts, reasoning, or ad hoc code.
The gate is the executable source of truth for planner eval status,
stale/mismatched plan/eval detection, latest-backup freshness, approval flags,
partial safe-project effective plans, sanitized approval batches, and
effective-plan generation.

4. If the gate exits `0` with `partial: true`, continue only with projects in
   `_review_effective_plan.json`, and surface the pending approval batch from
   the gate output as a non-blocking intervention. Do not send skipped projects
   or inputs to the model.
   If the gate reports `auto_excluded_secret_inputs`, treat those as non-fatal
   privacy exclusions. Do not recover them from raw markdown during this run.
5. If the gate exits `2`, open or resume the coding-agent thread and ask the
   user once with the full approval batch from the gate output. Use only
   sanitized project names and input ids. Never print suspected secret values.
   Do not ask project-by-project. If this agent cannot open/resume a thread, use
   its closest supported user-intervention surface. Do not continue model calls
   until the user explicitly approves inputs, excludes inputs, or stops the run.
   Record that choice in `<backup_dir>/_review_gate_decisions.json`, scoped to
   the current plan `generated_at` and input content hashes, then rerun the
   wrapper pre gate.
   `needs_approval` is a transient pause; it is not a permanent blocker.
6. After the gate exits `0`, use `<backup_dir>/_review_effective_plan.json` if
   present. It contains the selected context after approval/exclusion decisions.
   Excluded inputs must not be sent to the model.
   If a selected input has `preprocessed_ref`, read that entry from
   `<backup_dir>/_review_preprocessed_inputs.json` and use the sanitized text as
   model context. It may be redacted for secrets, sanitized for instruction
   context, stripped of generated local-command UI turns, or a combination. Do
   not read or send the raw markdown for that input unless
   the user explicitly asks for a raw deep-review rerun.
7. Before model calls for local git repos, run the wrapper repo-sync check:

```sh
<review_gate_cmd> --skill-dir <skill_dir> repo-sync --backup-dir <backup_dir>
```

   It writes `_review_repo_sync.json`. It may run `git fetch` by default to check
   remote-tracking refs, but must never pull, merge, rebase, checkout, commit, or
   modify the worktree. If a project has `repo_may_be_stale: true`, reflect that
   in the project review and set `needs_deep_review` or an open question before
   treating the review as complete. If sync is uncertain, record the uncertainty
   instead of pretending the repo is fresh.
8. Use only the selected inputs from the effective plan, the repo-sync sidecar,
   plus extra context explicitly allowed by a deep-review flow.
9. Default daily runs are incremental: use previous sidecars, repo
   planning/design docs, and only new or changed conversations. Full raw
   conversation reads are allowed only for explicit bootstrap/deep-review modes,
   scoped to the project being reviewed unless the user approves a global
   full-archive pass.
10. For bootstrap and deep-review runs, checkpoint continuously. Before merging
   each conversation summary, run:

```sh
<review_gate_cmd> --skill-dir <skill_dir> validate-summary --summary-json <summary-entry.json> --session-id <session-id> --expected-content-hash <content-hash>
```

   Only atomically merge `_conversation_summaries.json` after that deterministic
   validation passes. Use a temporary file in `backup_dir` and rename it into
   place. After each project review, atomically merge `_project_reviews.json`.
   If usage/context/time or provider limits stop the run, keep valid partial
   sidecars, record `needs_attention` with pending counts in
   `_review_update_log.json`, and resume next time only from checkpoints with
   matching `content_hash` and `summary_quality_version`. Never hold all
   generated output only in memory until the finalizer.
11. Write generated sidecars only at the root of `backup_dir`:
   `_conversation_summaries.json`, `_project_reviews.json`,
   `_agent_profile.json`, `_review_repo_sync.json`, and
   `_review_update_log.json`.
12. After writing sidecars, run the wrapper finalizer:

```sh
<review_gate_cmd> --skill-dir <skill_dir> finalize --backup-dir <backup_dir> --output-language <en|es>
```

The finalizer runs trailkeep's generated-output evals, writes
`_review_generated_eval_report.json`, appends the review run to
`_review_update_log.json`, validates the log, and exits nonzero if the run must
not be trusted. It may mark a passing run as `needs_attention` when generated
evals have warnings or the concrete model used is unknown; that is a non-fatal
warning state, not a failed run.

Pass `--model-provider`, `--model-routing`, `--model-used`, and
`--output-language` when the agent knows them; otherwise the finalizer records
unknown/unavailable values and may finish as `needs_attention`.

The skill must not reimplement generated-output checks in prompts or ad hoc
logic. Those checks live in
`<trailkeep_repo>/converters/eval_generated_reviews.py`; the finalizer calls
that repo runner and records the result in `_review_update_log.json`.

## Sidecar Responsibilities

- `_conversation_summaries.json`: update only new, changed, or stale-quality
  conversations by session id and preserve existing valid entries. The current
  `summary_quality_version` is `actionable-v3`; summaries without that version
  or matching `evidence_refs` are stale even if their `content_hash` still
  matches. Each summary must include `summary_quality_version`, `signal_level`,
  `include_in_project_rollup`, `user_intents`, `implemented_changes`,
  `verification`, `task_candidates`, `ignored_or_low_signal`, `files_or_areas`,
  and `coverage_check`.
  Allowed signal levels are `administrative`, `low_signal`,
  `context_dependent`, `decision`, `implementation`, and `blocker`.
  Administrative/low-signal/context-dependent conversations should be
  checkpointed with `include_in_project_rollup: false` and empty
  `decisions`/`blockers`/`task_candidates`/`implemented_changes`/`verification`
  unless there is explicit durable evidence. They should set
  `not_rollup_reason` and explain the omission in `ignored_or_low_signal`.
  Do not invent full summaries for short or low-signal conversations.
  Each summary must include `evidence_refs` with at least one `conversation`
  reference carrying the summarized input `content_hash`.
  Conversation summaries must answer only what the selected context supports:
  what the user wanted, what was decided, what changed, files/areas touched,
  real blockers, and actionable next hints. Reject and regenerate summaries that
  contain "Bootstrap summary for", "Evidence clusters around", repeated role
  markers such as "Claude You Claude", redaction/preprocessing notes as the main
  content, or serialized object/dict text instead of readable prose.
  `actionable-v3` summaries are a coverage matrix, not just prose. Use:
  `user_intents` for explicit user asks, `decisions` for durable decisions,
  `implemented_changes` for concrete changes with tool evidence, `verification`
  for checks run or explicitly not run, `blockers` for real blockers,
  `task_candidates` for possible pending work, `ignored_or_low_signal` for
  intentionally discarded/administrative material, `files_or_areas` for touched
  surfaces, and `coverage_check` to state whether anything important was left
  uncovered.
  `files_or_areas` must be structured evidence, not loose strings. Each item
  needs either `path` for a concrete file/doc or `area` for a product/code area
  when no single file is known, a `role` from
  `mentioned | discussed | reviewed | changed | created | removed | tested |
  configured | designed | blocked | unknown`, and short `evidence_refs`.
  Use `mentioned` or `discussed` for weak references; use stronger roles only
  when selected conversation/tool evidence supports the claim.
  Treat `task_candidates` as conversation-level candidates, not project backlog
  tasks. Each candidate must have a stable `id`, `status`, text, and
  `evidence_refs`. They may capture possible pending work with evidence, but
  they must be promoted, merged, questioned, or rejected by the project review
  before appearing in `_project_reviews.json.tasks`. `task_hints` is a legacy
  v2 field and must not be written by actionable-v3 summaries.
- Treat initial coding-agent instruction/header blocks as constraints, not user
  intent. Codex conversations may include AGENTS.md, global instructions,
  developer context, environment data, permissions, or skill/plugin headers in
  the first turn. If the plan marks an input with `instruction_context` or
  `preprocessed_ref`, use the sanitized text and do not create summaries,
  decisions, tasks, `next_step`, or `roadmap_status` from those headers alone.
  They may support repo conventions, agent profile, constraints/instructions,
  and verification/security rules. If the conversation is mostly instruction
  context with little user intent, classify it as `context_dependent` or
  `administrative`, set `include_in_project_rollup: false`, and leave durable
  task/decision/blocker fields empty.
- Deterministic validation is mandatory for every conversation summary before
  checkpointing. Semantic/LLM quality review is sampled, not run for every
  summary by default: sample at least one out of every 25 generated summaries,
  and always review summaries with low confidence, `context_dependent` signal,
  non-empty `decisions`/`blockers`/`task_candidates`, very long source
  conversations, preprocessed/redacted input, or direct use in a project review
  rollup. Batch this semantic judge when possible. Record the result in
  `_review_update_log.json.semantic_quality_review` with `status`,
  `sample_every`, sampled counts, `model_used`, warnings, and failures. If the
  semantic judge cannot run because model access is unavailable, record
  `status: "skipped"` and mark the review run `needs_attention`.
- `_project_reviews.json`: use repo planning/design docs as source of truth,
  conversation summaries as evidence, preserve stable task ids, preserve the
  user's roadmap/backlog priority order, and make suggested next steps advance
  the existing roadmap when present. If conversations reveal new legitimate work
  not present in the roadmap, add it as a pending/candidate task or open
  question with evidence; do not silently promote it above existing roadmap
  priorities. If repo planning docs are stale, duplicated, or contradictory,
  record focused recommendations in `recommended_repo_doc_updates` with
  `file`, `reason`, `action`, `confidence`, `evidence_refs`, and
  `requires_user_approval: true`. Never modify `ROADMAP.md`, `BACKLOG.md`,
  `TODO.md`, `docs/design.md`, or equivalent repo docs automatically during
  recurring runs.
  Project `tasks` are consolidated backlog items. Every project task must map to
  repo planning docs, a prior project task, or one or more conversation-summary
  `task_candidates`, blockers, decisions, or implemented changes. Do not create
  orphan tasks. Legacy v2 `task_hints` may be read as stale evidence during
  migration, but new project reviews should prefer `task_candidates`.
  Every relevant `task_candidates[]` item from a conversation summary with
  `include_in_project_rollup: true` must end in one durable project-review
  outcome:
  - promoted or merged into `tasks`;
  - represented as an evidence-backed `open_questions[]` item;
  - recorded in `discarded_candidates[]` with `conversation_id`, `candidate_id`,
    `not_promoted_reason`, and `evidence_refs`.
  For conversation-derived tasks or open questions, cite the exact candidate in
  `evidence_refs` with `type: "conversation_summary"`,
  `field: "task_candidates:<candidate-id>"`, and
  `task_candidate_id: "<candidate-id>"`. Conversation-derived tasks must match
  the cited conversation-summary item; do not cite an unrelated candidate,
  blocker, decision, or implemented change just to satisfy evidence shape. If a
  candidate is duplicated, low-signal, already done, not now, or conflicts with
  the repo roadmap, merge it, capture an evidence-backed open question, or put
  it in `discarded_candidates[]` with a concrete `not_promoted_reason`.
- Reject and regenerate project reviews whose `summary`, `next_step`,
  `roadmap_status`, tasks, open questions, design-system notes, or recommended
  repo-doc updates contain bootstrap boilerplate such as "Bootstrap summary
  for", "Evidence clusters around", "selected because new or changed
  conversation", redaction/preprocessing notes as product content, repeated role
  markers, raw tool output, or serialized object/dict text.
- Ground every durable project-review claim with explicit short `evidence_refs`.
  Project `summary`, `standing_context`, `next_step`, `roadmap_status`, tasks,
  open questions, and recommended repo-doc updates must cite selected
  conversations, conversation summaries, repo docs, metadata, repo-sync output,
  or prior sidecars. Do not include long raw quotes or secrets in evidence refs.
  Every task must include `source` and `evidence_refs`; `source: "inferred"`
  tasks also need `confidence` and `reason` and must remain candidate work. If
  evidence is insufficient, write `unknown` or an evidence-backed open question
  instead of promoting the guess into a task, next step, or roadmap status.
- Generated prose fields must be plain strings written in `output_language` for
  that run. The setup/manual/test prompts set `output_language` explicitly.
  Keep JSON schema keys in English. Do not create bilingual sidecar objects
  unless the user explicitly asks for that format in a future run. Record
  `output_language` in `_review_update_log.json`.
  The setup prompt owns the recurring automation language: if the setup prompt is
  Spanish, set `output_language: "es"`; if it is English, set
  `output_language: "en"`. Use that value for all generated sidecar prose in
  recurring runs and keep JSON schema keys in English.
- Treat tool turns as execution evidence, not narrative. Use user/assistant
  turns for intent and decisions; use tool turns only to prove files changed,
  commands ran, tests/builds passed or failed, errors happened, git state
  changed, or artifacts were produced. Do not paste long raw tool output into
  summaries or reviews. Any claim that work was implemented, fixed, verified,
  tested, built, committed, pushed, passed, or failed must cite a short
  `evidence_refs` item with `type: "tool"` when tool evidence exists.
- Cumulative review means using previous sidecars and checkpoints as compact
  memory, sending only selected deltas to the model by default, preserving stable
  ids/notes, and escalating to broader review only for bootstrap, explicit
  manual deep-review, deterministic broad/conflicting changes, low confidence,
  evidence-backed stale checkpoints, or major metadata changes. Time passing
  alone is not a reason to reread the full project.
- For each project: compare current sessions, repo docs, metadata, git state,
  repo sync state, and deploy state against `_project_reviews.json` checkpoints;
  skip unchanged projects; for small conversation-only changes, send the
  previous compact review plus the new/changed conversation evidence only; run
  broader review or set a deep-review flag only when deterministic change
  signals, remote commits ahead of local, or low confidence show the prior
  project summary may be stale; preserve task ids unless evidence says to
  update, close, split, or replace them. A reviewed-session checkpoint is current
  only when both `content_hash` and `summary_quality_version` match the current
  policy.
- Keep runs token-efficient: use cheaper configured tiers for classification and
  summarization, and stronger tiers only for deep project review or
  design-system extraction.
- Daily design-system review is incremental: skip projects without UI/design
  changes; use `design.md`, `docs/design.md`, `docs/design-patterns.md`, and
  component files as source of truth; use new conversations only as evidence;
  update the design-system summary only with new evidence; set
  `needs_deep_design_review: true` for broad or conflicting changes instead of
  rereading the full project automatically.
- `_agent_profile.json`: update recurring preferences, working style, repo
  conventions, and prompt patterns from compact project reviews.
- Every updated `_project_reviews.json` project entry must include a non-empty
  `suggested_next_prompt`. It should be a concrete, executable prompt for the
  next coding-agent session for that project, not a placeholder.
  It must name a concrete file, section, view, component, or flow; identify the
  selected follow-up task; include the verification step to run or perform; and
  state the expected output or sidecar/doc update. Avoid boilerplate such as
  "review the generated sidecars", "compare open tasks with repo planning docs",
  or "choose the highest-priority next step" unless those phrases are followed
  by a concrete target and action.
- `_review_update_log.json`: record the automation result, provider/routing
  metadata when known, concrete `model_used`, `output_language`, repo-sync
  summary, affected projects, outputs, eval report path, semantic quality
  sampling result, warnings, and errors.
  Keep it as one global chronological log in `backup_dir`; do not create
  per-project review logs unless trailkeep later needs them for size or
  performance.

Do not write generated sidecars into project repos, source-tool raw folders,
`markdown-*` folders, or the trailkeep repo. Do not commit private backups or
generated sidecars.

Never transmit the entire backup folder as an archive or unscoped dump. The
review plan is the input manifest: project, files/session ids selected, reason,
estimated tokens, and model tier.

## Scheduling

Prefer a true post-backup trigger if the user's coding agent supports it. If the
agent can only schedule by time, infer the daily trailkeep backup/update time
from the installed launchd/cron job or recent `backup_dir/log.json` entries, and
schedule the review 10-15 minutes later. The pre-model gate still validates that
the plan/eval are current and aligned, and that the latest backup run in
`log.json` is less than 24 hours old before any model call.

## Model Routing

Use one skill with modes, not one skill per model. If the agent supports model
routing, map the spec's `cheap`, `default`, and `strong` tiers to the user's
configured models. If per-task routing is unavailable but the automation can
choose one model, configure that automation to use the `strong` tier by default.
If the agent cannot choose a model at all, continue with the available model,
write `model_routing: "unavailable"` in `_review_update_log.json`, and still
record `model_used` with the concrete model name, configured alias, or
`"unknown"` if the agent/provider hides it.
