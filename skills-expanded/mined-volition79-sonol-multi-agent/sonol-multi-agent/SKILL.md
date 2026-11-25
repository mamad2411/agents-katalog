---
name: sonol-multi-agent
description: Sonol multi-agent orchestration skill. Use when a user wants one request decomposed into single-agent or multi-agent execution, with local-AI creative draft generation, hosted normalization/binding, adapter-backed sub-agent controls, runtime reporting, dashboard monitoring, plan/run persistence, and final result integration.
---

# sonol-multi-agent

Use this skill when the work benefits from structured orchestration instead of a
single linear agent.

This skill is the top-level orchestrator. It decides whether to stay
single-agent or switch to multi-agent, defines the agent set, creates a plan,
creates immutable runs, and coordinates runtime reporting through the current
Sonol runtime helper surface.

The current default adapter may be environment-selected. Treat sub-agents as
conversation-scoped delegated workers plus config-driven agent settings, not as
public handle-based child processes.

## When To Use

Use this skill when the request includes any of the following:

- distinct research, coding, testing, review, or documentation tracks
- a need to separate authority between planner, implementer, tester, reviewer
- work that benefits from a dashboard, run history, or live status reporting
- tasks that need final integration by a main agent

Do not use this skill for trivial one-step requests unless the user explicitly
wants orchestration.

## Workflow

1. Classify the request as single-agent or multi-agent.
2. Create a local creative draft, then submit it through `scripts/present-proposal.mjs`.
   In the public/community edition, the current Codex/Claude session must first
   create the creative draft and pass it into the command. A compatible hosted
   service then normalizes, validates, and binds that draft. It must not author
   the initial creative structure.
   Before writing the draft, open the canonical contract at
   `references/creative-draft-contract.md`
   and one of the checked-in examples:
   `references/creative-draft.example.ko.json`
   or
   `references/creative-draft.example.en.json`.
   The creative draft uses `subagents`, `slot_id`, and `role_label`. Do not
   author it with normalized plan fields such as `agent_id`, `role`,
   `workstream_id`, or `reporting_contract`.
   The Main agent is implicit and must not be written into the draft
   `subagents` array.
   Always pass the request with `--request-summary "..."`. Do not rely on
   positional text.
   At this stage, also generate a short `plan title` for dashboard display.
   This title should be a concise phrase, not the full user sentence.
2.5. Before any substantial web research, implementation, testing, or sub-agent
   delegation, stop and present the orchestration proposal first.
   Only minimal context gathering needed to size the work and shape the initial
   agent structure is allowed before this proposal.
3. If multi-agent is not beneficial, explicitly say so and proceed in the normal
   single-agent way.
4. If multi-agent is beneficial, present the locally authored count, roles,
   purposes, and constraints, including current adapter control fields such as
   base type, model, reasoning effort, sandbox mode, MCP surface, skills
   surface, and path policy. Tell the user to review the remote dashboard URL.
5. The operator reviews or edits the plan in the dashboard and approves it
   there.
5.1. Treat the `present-proposal.mjs` output as the authority for dashboard
   readiness in the current terminal session. Do not invent extra shell polling
   such as `sleep`, `curl`, or `echo` chains to second-guess it.
5.2. If `present-proposal.mjs` says automatic launch is unverified or failed,
   first tell the operator to open the dashboard URL directly in a browser.
   Only if that still fails should you suggest the printed manual
   `start-dashboard.mjs` command.
5.3. When manual dashboard start is needed, run `start-dashboard.mjs` only in a
   persistent session such as a normal terminal window. Do not background it
   from a one-shot Bash tool call and then poll health from a second chained
   command.
6. After dashboard approval, the operator only needs to type `승인` in the
   current Sonol terminal session.
7. The assistant then runs the internal terminal confirmation step against the
   latest active approved dashboard plan, not from stale terminal memory.
7.5. That terminal confirmation step may still block and return actionable
   guidance instead of launching immediately if dashboard approval is missing,
   validation failed, a different plan must be selected, or the plan changed
   and the operator must refresh and reconfirm.
8. Once the user confirms in terminal, create the run snapshot, runtime
   context, and launch manifest from the latest dashboard state, not from stale
   terminal memory.
8.5. If the adapter returns `dispatch_mode: manifest_only`, treat that outcome
   as `prepared`, not as already launched. Before any real sub-agent work,
   inspect the active launch manifest and delegate with the generated
   run-scoped prompt file for each planned `agent_id`.
8.6. If the manifest packet includes `assistant_launch_recipe.tool_name` and
   `assistant_launch_recipe.tool_args`, call that assistant tool immediately
   with those exact launchable args instead of rebuilding the launch by hand.
   Do not overclaim that this makes every Sonol policy field natively enforced
   by the host launch surface.
9. Require every sub-agent to follow the Sonol runtime reporting rules.
   Use the reporting transport named in the generated packet. `script_commands`
   is the common default path, and `json_ingest` is the provider-neutral
   fallback or provider-specific preferred path when the packet says so.
10. Generate run-scoped runtime context files and pass short file references
   instead of long repeated instructions.
11. When using real sub-agents, never invent an ad-hoc role prompt.
    Always build the delegation packet from the active run and planned `agent_id`
    first, then pass that exact run-scoped prompt.
11.25. In manifest-only adapters, a fresh free-form provider `spawn_agent`
    prompt is a coordination failure unless it is exactly the generated
    run-scoped prompt for the active `run_id`.
11.3. Prefer `assistant_launch_recipe.tool_args` when present. That field is
    the launch-ready recipe for the fields the host assistant surface can
    actually enforce. Sandbox, MCP, helper-skill, and path rules remain Sonol
    coordination policy unless the host surface enforces them natively.
11.5. Prefer the generated run-scoped prompt file under
    `<runtime_root>/<run_id>/prompts/<agent_id>.txt` for the actual
    delegation text so the current run id cannot drift after a newer run is
    launched for the same plan.
12. The delegated prompt must carry the exact current `plan_id`, `run_id`,
    `agent_id`, and `task_id`, and must tell the sub-agent to use those exact
    identifiers in `report-*` calls.
13. Integrate results in the Main Agent.
14. While and only while this skill is active, the Main Agent should report its
    own progress through the sonol wrapper command instead of ad-hoc prose.

## Approval Guardrails

- A user asking to "use Sonol multi-agent", "work in parallel", "research and
  then implement", or similar wording is a request to use this workflow, not an
  approval to launch it.
- Treat the first mandatory deliverable as the orchestration proposal:
  single-agent or multi-agent decision, initial agent structure, constraints,
  and next approval step.
- After presenting that proposal, stop and wait for explicit operator approval
  before launching any multi-agent run.
- Before approval, do not call `approve-plan.mjs`, `confirm-plan.mjs`, spawn
  sub-agents, or treat the run as active.
- Before approval, do not begin substantial web research, implementation,
  testing, or long-running parallel work. Limit yourself to lightweight repo and
  request inspection needed to decide the agent structure.
- Accept terminal launch only from explicit user confirmation after the plan
  has been presented and dashboard approval has completed.
- Do not infer approval from general positive language such as "go ahead",
  "proceed", "use the skill", or from the fact that the user asked for
  multi-agent work.
- If dashboard approval cannot be observed directly in the current environment,
  state that limitation plainly and do not simulate or silently assume it.
- CLI fallback approval is disabled. Dashboard approval is the only supported
  approval path before terminal confirmation.

## Supported Sub-Agent Controls

Use these as the canonical control knobs when proposing or editing sub-agents:

- semantic `role`
- `purpose`
- `provider_agent_type`: `default`, `worker`, `explorer`, or `custom`
- `codex_agent_type`: optional compatibility alias used by the current Codex adapter
- `execution_target`: prefer `provider: "inherit-run-adapter"` and `backend: "selected-at-launch"` unless a plan must pin a specific adapter
- `custom_agent_name`
- `custom_config_file`
- `developer_instructions`
- `model`
- `model_reasoning_effort`
- `sandbox_mode`
- `mcp_servers`
- `skills_config`
- `nickname_candidates`
- `approval_mode`: `inherit-session` in v1
- `communication_mode`: `delegated-thread-and-runtime-events` in v1
- `depends_on`
- `read_paths`
- `write_paths`
- `deny_paths`
- `operational_constraints`
- `reporting_contract`

This list is the dashboard-editable/operator-facing control surface.
Persisted agent records also carry generated or validated fields such as
`role_label`, `execution_class`, `workstream_id`, `selection_rationale`,
`assigned_task_ids`, and `current_task_id`.

Interpretation rules:

- base type, custom-agent binding, model, reasoning, sandbox, MCP, skills, and
  nickname are current adapter-compatible controls
- path policies, ownership, and merge order are Sonol coordination rules, not
  native Codex ACL guarantees
- in manifest-only launch recipes, `fork_context=false` is a hard Sonol launch
  invariant
- effective sub-agent count must stay within Sonol policy and the active
  adapter's thread/depth limits

## Communication Model

Sub-agents should be coordinated through:

- the generated prompt packet
- shared files and artifacts
- SQLite-backed runtime events
- Main Agent synthesis and follow-up routing
- `/agent` thread inspection when a human needs to inspect or continue a branch

Do not assume direct peer-to-peer chat, dashboard-to-terminal injection, or a
public per-thread stdin API.

## Unsupported Assumptions

Do not claim or rely on:

- dashboard-to-terminal text injection
- dashboard-to-sub-agent direct messaging
- a public low-level `spawn/list/wait/terminate/send_input` API for Codex
  sub-agents
- recursive child spawning by Sonol sub-agents in v1
- native per-agent file ACL enforcement by Codex

## Replacement Patterns

When users want stronger control than the public Codex surface provides, use
these substitutes:

- tighten `developer_instructions`
- lower `sandbox_mode`
- reduce `mcp_servers`
- reduce `skills_config`
- lower effective concurrency
- keep sub-agent depth at `1`
- push coordination through prompt packets, shared artifacts, and runtime events
- use `show-run-launch-manifest.mjs` or `/api/runs/<run_id>/launch-manifest`
  as the exact source of launch-ready agent packets
- if a packet includes `assistant_launch_recipe`, use that recipe directly
  instead of reconstructing a provider tool call by hand
- use `/agent` or normal main-thread follow-up for manual steering

## Community And Private Core Deployment

When Sonol is distributed as a public community edition, keep the authority
split explicit:

- keep SQLite, runtime events, dashboard state, and sub-agent execution local
- keep the creative draft on the local Codex/Claude side
- use a hosted normalization/binding service for turning that creative draft into an executable Sonol plan
- return normalized plan data or launch recipes from that control plane, not raw DB ownership
- keep high-load implementation, testing, and provider execution local whenever possible
- do not stream the full local runtime event log to the planner service by default
- publish only a generated public release when sharing the skills externally; do not publish raw working folders if you need private deployment artifacts excluded

Recommended hosted normalization environment:

- Standard public/community install:
  - no planner env vars are required
  - Sonol defaults to `https://agent.zooo.kr/v1/planner/draft`
  - Sonol defaults to `https://agent.zooo.kr/v1/planner/ticket`
  - Sonol defaults to `https://agent.zooo.kr/sonol-dashboard/`
- Optional private or self-hosted override:
  - `SONOL_PLANNER_DRIVER=remote_http`
  - `SONOL_REMOTE_PLAN_NORMALIZER_URL=https://your-planner.example/v1/planner/draft`
  - `SONOL_REMOTE_PLAN_NORMALIZER_TICKET_URL=https://your-planner.example/v1/planner/ticket`
  - `SONOL_REMOTE_PLAN_NORMALIZER_BEARER_TOKEN=<token>`
  - `SONOL_REMOTE_DASHBOARD_BASE_URL=https://your-planner.example/sonol-dashboard/`
    - optional: if omitted, Sonol derives `/sonol-dashboard/` from the hosted planner origin

In this mode:

- the local SQLite file remains the authoritative store for plans, runs, and events
- the local loopback dashboard bridge still reads the local DB
- the remote dashboard keeps the same operator surface as the legacy local dashboard while talking to the loopback bridge
- the remote service should return only normalized plan data or equivalent launch recipes
- browser storage such as localStorage is not used as an authority
- browser UI preferences may exist, but they must stay non-authoritative
- path-sensitive local values such as `authoritative_db_path` must not be treated as remote service inputs by default
- the public/community edition does not ship the private normalization/binding core
- if a custom remote normalization override is incomplete, Sonol fails fast instead of generating a local fallback draft
- remote normalization should be enabled per shell or per project, not forced globally in every terminal profile

## Creative Draft Contract

- The creative draft is the local input contract. It is not the persisted
  normalized plan object.
- Required root fields are:
  `plan_title`, `preferred_language`, `single_or_multi`,
  `multi_agent_beneficial`, `recommendation_summary`,
  `recommendation_reasons`, and `subagents`.
- Each creative draft subagent must use:
  `slot_id`, `role_label`, `execution_class`, `purpose`, `task_title`,
  `selection_rationale`, `provider_agent_type`, `developer_instructions`,
  `model`, `model_reasoning_effort`, `sandbox_mode`, `mcp_servers`,
  `skills_config`, `nickname_candidates`, `read_paths`, `write_paths`,
  `deny_paths`, `operational_constraints`, and `depends_on`.
- Main agent semantics are runtime policy and remain implicit. Do not put Main
  into `subagents`.
- Use the canonical contract doc:
  `references/creative-draft-contract.md`
- Use the checked-in examples before authoring a new draft:
  `references/creative-draft.example.ko.json`
  and
  `references/creative-draft.example.en.json`
- The CLI now validates the creative draft before planner locks, pending
  workspace state, or planner job rows are created.

## Hard Rules

- Main Agent always exists and owns final integration.
- The initial recommendation is the first remotely normalized plan saved for the
  current workspace. After the operator edits the dashboard, the latest saved
  dashboard state is the source of truth.
- `planning_backend` describes the generic planner execution shape, while
  `planning_driver` records the concrete implementation used for that draft.
- Draft plan edits do not mutate an active run.
- Retry creates a new run; it does not overwrite the previous one.
- Runtime state must be reported through the runtime helper skill scripts.
- SQLite is the system of record for plans, runs, and events.
- The canonical SQLite event table is `events`. A compatibility view named
  `runtime_events` may exist for older diagnostics, but new tooling should
  prefer the Sonol APIs and current table name.
- `prepared` in a manifest-only adapter means “launch packet ready, provider
  subagents not launched yet”.
- A manifest-only `prepared` run should already appear in the dashboard with
  persisted run/session state before any sub-agent progress arrives.
- `provider_refs` must describe what Sonol actually knows from the provider
  surface. If launch is manifest-only and status is projected from local
  runtime events, record that honestly instead of implying provider-native
  control.
- Dashboard approval happens before terminal confirmation.
- Terminal confirmation must use the latest saved dashboard plan.
- `sonol multi-agent 스킬로 진행` means to enter this workflow, not to approve a
  plan, not to record dashboard approval, and not to confirm terminal launch.
- The assistant must not infer approval from implied intent or from the user
  wanting research, coding, or parallel work done quickly.
- The assistant must not call `confirm-plan.mjs` unless the operator has
  explicitly approved that exact step and dashboard approval has completed.
- The assistant must not launch or delegate real sub-agent work before the
  approval sequence is complete.
- The assistant must not invent ad-hoc dashboard health checks such as chained
  `sleep`, `curl`, or `echo` commands after `present-proposal.mjs`.
- The assistant must use the remote dashboard URL plus the launcher status returned by
  `present-proposal.mjs` as the source of truth for whether manual start
  guidance is needed.
- The first response in this skill should settle the orchestration system first:
  decide single-agent vs multi-agent, have the current local AI session shape
  the creative draft, and explain the next approval step before deeper
  execution work begins.
- If the dashboard is approved and the user explicitly types `승인` or clearly
  requests the final terminal step, run the internal `confirm-plan.mjs`
  confirmation against the latest active approved dashboard plan.
- After terminal confirmation in a manifest-only adapter, do not jump straight
  to ordinary provider delegation. Inspect the launch manifest and use the
  generated run-scoped prompt files exactly as written.
- If multi-agent is not beneficial, say so and proceed single-agent.
- Multi-agent benefit must be explained before proposing sub-agents.
- If a requested control exceeds public Codex support, say so explicitly and use
  a documented replacement pattern.
- Dashboard approval must not directly launch a multi-agent run.
- Sub-agents must not spawn child sub-agents in v1.
- Plan size must stay within the effective `max_threads` and `max_depth` policy.
- Treat `/agent` and main-thread follow-up as the strongest supported steering
  path after initial delegation.

## Quick Commands

- Set `SONOL_INSTALL_ROOT` to your Sonol install root on another machine before using the commands below.

- Recommend and save a plan:
  - `node $SONOL_INSTALL_ROOT/skills/sonol-multi-agent/scripts/recommend-plan.mjs --creative-draft-file /abs/draft.json --request-summary "request summary"`
  - Optional workspace override: `node $SONOL_INSTALL_ROOT/skills/sonol-multi-agent/scripts/recommend-plan.mjs --creative-draft-file /abs/draft.json --workspace-root /abs/workspace --db /abs/sonol.sqlite --request-summary "request summary"`
  - Public hosted normalizer default: `node $SONOL_INSTALL_ROOT/skills/sonol-multi-agent/scripts/recommend-plan.mjs --creative-draft-file /abs/draft.json --workspace-root /abs/workspace --db /abs/sonol.sqlite --request-summary "request summary"`
  - Private/self-hosted override: `SONOL_PLANNER_DRIVER=remote_http SONOL_REMOTE_PLAN_NORMALIZER_URL=https://your-planner.example/v1/planner/draft SONOL_REMOTE_PLAN_NORMALIZER_TICKET_URL=https://your-planner.example/v1/planner/ticket SONOL_REMOTE_PLAN_NORMALIZER_BEARER_TOKEN=<token> node $SONOL_INSTALL_ROOT/skills/sonol-multi-agent/scripts/recommend-plan.mjs --creative-draft-file /abs/draft.json --workspace-root /abs/workspace --db /abs/sonol.sqlite --request-summary "request summary"`
  - Without a compatible hosted normalizer or the built-in public endpoint, plan recommendation fails fast instead of running a bundled local planner core or generating a local fallback draft.
- Present the user-facing proposal:
  - `node $SONOL_INSTALL_ROOT/skills/sonol-multi-agent/scripts/present-proposal.mjs --creative-draft-file /abs/draft.json --request-summary "request summary"`
  - Optional workspace override: `node $SONOL_INSTALL_ROOT/skills/sonol-multi-agent/scripts/present-proposal.mjs --creative-draft-file /abs/draft.json --workspace-root /abs/workspace --db /abs/sonol.sqlite --request-summary "request summary"`
  - Optional dashboard bridge override: `node $SONOL_INSTALL_ROOT/skills/sonol-multi-agent/scripts/present-proposal.mjs --creative-draft-file /abs/draft.json --workspace-root /abs/workspace --db /abs/sonol.sqlite --dashboard-url http://127.0.0.1:18081 --request-summary "request summary"`
  - Force planner driver only when debugging: `SONOL_PLANNER_DRIVER=remote_http`
  - If the draft is invalid, Sonol fails before planner lock and DB mutation.
    Fix the draft against `references/creative-draft-contract.md`
    or the checked-in examples, then retry.
- Internal terminal confirmation helper used after the user types `승인`:
  - `node $SONOL_INSTALL_ROOT/skills/sonol-multi-agent/scripts/confirm-plan.mjs --workspace-root /abs/workspace`
  - Claude Code override: `node $SONOL_INSTALL_ROOT/skills/sonol-multi-agent/scripts/confirm-plan.mjs --workspace-root /abs/workspace --adapter-type claude-code-subagent --adapter-backend claude-code-manual`
  - Optional explicit binding: `node $SONOL_INSTALL_ROOT/skills/sonol-multi-agent/scripts/confirm-plan.mjs --workspace-root /abs/workspace --db /abs/sonol.sqlite --dashboard-url http://127.0.0.1:18081`
- Show the authoritative workspace binding before ad-hoc diagnostics:
  - `node $SONOL_INSTALL_ROOT/skills/sonol-multi-agent/scripts/show-authority.mjs --workspace-root /abs/workspace`
- Show the launch manifest prepared by the active adapter:
  - `node $SONOL_INSTALL_ROOT/skills/sonol-multi-agent/scripts/show-run-launch-manifest.mjs --run-id <run_id> --db <db_path>`
  - A prepared manifest-only run may also persist `<runtime_root>/<run_id>/launch-manifest.json` and `<runtime_root>/<run_id>/authority.json` for operator diagnostics.
- Create a run directly only for single-agent or internal testing paths:
  - `node $SONOL_INSTALL_ROOT/skills/sonol-multi-agent/scripts/create-run.mjs --plan-id <plan_id> --mode dry-run --db <db_path>`
- Build a sub-agent prompt packet:
  - `node $SONOL_INSTALL_ROOT/skills/sonol-multi-agent/scripts/build-subagent-prompt.mjs --run-id <run_id> --agent-id <agent_id> --db <db_path>`
- Build a plain-text delegation prompt for an actual provider sub-agent:
  - `node $SONOL_INSTALL_ROOT/skills/sonol-multi-agent/scripts/build-subagent-prompt.mjs --run-id <run_id> --agent-id <agent_id> --format text --db <db_path>`
- Canonical prompt file for a run:
  - `<runtime_root>/<run_id>/prompts/<agent_id>.txt`
  - Treat this run-scoped prompt as immutable for the active run.
- Do not treat any mutable plan-level alias as authoritative once a run exists.
- For an in-flight run, only the run-scoped prompt file above is authoritative.
- Retry a run:
  - `node $SONOL_INSTALL_ROOT/skills/sonol-multi-agent/scripts/retry-run.mjs --run-id <run_id> --db <db_path>`
  - Multi-agent retry is disabled. For multi-agent plans, re-approve in the dashboard and then type `승인` in the current Sonol terminal session.
- Change run status:
  - `node $SONOL_INSTALL_ROOT/skills/sonol-multi-agent/scripts/set-run-status.mjs --run-id <run_id> --status cancelled --db <db_path>`
  - Do not use this helper to revive a finished run. Terminal run finality must be preserved.
- Start dashboard:
  - `node $SONOL_INSTALL_ROOT/skills/sonol-multi-agent/scripts/start-dashboard.mjs`
  - Optional workspace override: `node $SONOL_INSTALL_ROOT/skills/sonol-multi-agent/scripts/start-dashboard.mjs --workspace-root /abs/workspace --db /abs/sonol.sqlite`
  - Optional dashboard override: `node $SONOL_INSTALL_ROOT/skills/sonol-multi-agent/scripts/start-dashboard.mjs --workspace-root /abs/workspace --db /abs/sonol.sqlite --dashboard-url http://127.0.0.1:18081`
- Hosted plan normalizer server:
  - The server implementation is private and is not bundled in the public/community edition.
  - `scripts/start-remote-control-plane.mjs` is a public stub that documents the supported client-side environment variables only.
- Export a self-contained two-skill portable bundle:
  - `node $SONOL_INSTALL_ROOT/skills/sonol-multi-agent/scripts/export-portable-bundle.mjs`
  - Optional destination override: `node $SONOL_INSTALL_ROOT/skills/sonol-multi-agent/scripts/export-portable-bundle.mjs --output-dir /abs/output --bundle-name sonol-portable`
- Export a GitHub/public release with only the two skill folders:
  - `node $SONOL_INSTALL_ROOT/skills/sonol-multi-agent/scripts/export-public-release.mjs`
  - Optional destination override: `node $SONOL_INSTALL_ROOT/skills/sonol-multi-agent/scripts/export-public-release.mjs --output-dir /abs/output --bundle-name sonol-public`
  - Validate an exported release root: `node $SONOL_INSTALL_ROOT/skills/sonol-multi-agent/scripts/check-public-release.mjs --release-root /abs/output/sonol-public`
- Inspect stored snapshot:
  - `node $SONOL_INSTALL_ROOT/skills/sonol-multi-agent/scripts/show-snapshot.mjs --db <db_path>`
- Sync the local skills to the user-global skill directory:
  - Source-install only. This command is not available inside an exported portable bundle.
  - `npm run skills:sync-global`
- Generate compact runtime context files for a run:
  - `node $SONOL_INSTALL_ROOT/skills/sonol-multi-agent/scripts/prepare-run-context.mjs --run-id <run_id> --db <db_path>`
- Report Main Agent progress for the active sonol run:
  - `node $SONOL_INSTALL_ROOT/skills/sonol-multi-agent/scripts/report-main.mjs --db <db_path> --type progress --message "최종 정리 시작" --detail "설계와 구현 결과를 함께 검토하고 있습니다. 충돌 지점을 먼저 정리합니다."`
- Report Main Agent completion for the active sonol run:
  - `node $SONOL_INSTALL_ROOT/skills/sonol-multi-agent/scripts/report-main.mjs --db <db_path> --type completion --result success --summary "최종 정리 완료" --detail "구현과 검증 결과를 하나로 묶었습니다. 이제 사용자에게 결과를 설명할 수 있습니다."`
- Show run diagnostics and recent runtime logs:
  - `node $SONOL_INSTALL_ROOT/skills/sonol-multi-agent/scripts/show-run-diagnostics.mjs --run-id <run_id> --db <db_path>`

## References

- Read [references/agent-shaping.md](references/agent-shaping.md) for public role and sizing guidance.
- Read [references/dashboard-workflow.md](references/dashboard-workflow.md) for the operator flow and dashboard meaning.
- Read [references/runtime-bridge.md](references/runtime-bridge.md) for how sub-agents must be instructed.
- Read [references/remote-control-plane.md](references/remote-control-plane.md) for the public hosted-planner client contract.
- Read [references/public-release.md](references/public-release.md) for the supported GitHub/public release boundary.
- When comparing Sonol against other providers, rely on the bundled references in this skill and any local notes you intentionally ship alongside the portable bundle or public release.
- For moving Sonol to another computer, read [portable-setup.md](references/portable-setup.md).

## Coordination With sonol-agent-runtime

When spawning or instructing sub-agents, explicitly require them to follow the
current Sonol runtime reporting contract and use the generated runtime context.

The supported communication pattern is:

- one bounded delegation packet per sub-agent
- optional follow-up in the main conversation or via `/agent`
- runtime event reporting back to SQLite for dashboard visibility
- final synthesis through the Main Agent

Do not assume a public API exists to inject new text directly into an arbitrary
existing child thread from the dashboard or from an external controller.

Required event families:

- `progress_event`
- `artifact_event`
- `completion_event`
- `session_updated` when status changes materially

The Main Agent should treat missing runtime reports as a coordination failure.
If diagnostics show that a sub-agent wrote reports to a different `run_id`, treat
that as a prompt/delegation mismatch and regenerate the prompt from the active
run before continuing.
The Main Agent should also rely on the same `report-*` path and generated
runtime context files to keep prompts and report text short.
This Main Agent reporting rule applies only while `sonol-multi-agent` is the
active orchestration skill for the current task.
In a manifest-only adapter, the Main Agent should emit a `report-main` event as
soon as terminal confirmation returns, even while the run is still only
`prepared`.
That event is coordination state only. It must not be treated as proof that any
provider sub-agent has already launched.
When an agent finishes its current unit but is not fully complete, it should
emit `session_updated` with `status=idle` so the dashboard shows “다음 작업 대기”
instead of looking stuck or unstarted.
When emitting runtime reports, use:
- `message`: a short headline
- `detail`: `1` to `3` short user-facing sentences about the actual work
Do not rely on the dashboard to invent meaningful detail from generic task ids.
The Main Agent should also report in small work units, not only large phases.
At minimum, it should report:
- immediate task start
- meaningful file creation or edit
- validation/build/test checkpoints
- integration/handoff checkpoints
All runtime reporting and event persistence also write structured diagnostics to
the log directory resolved by Sonol at runtime, typically `<data_dir>/logs/sonol-runtime-YYYY-MM-DD.jsonl`.

## Dashboard Binding Notes

- The default dashboard URL is now workspace-scoped. Sonol derives a stable local port from `workspace_root` instead of assuming one global fixed port.
- Treat `plan.dashboard_url` as the operator-facing URL for that workspace and plan.
- Treat `plan.authoritative_db_path` as the DB authority for terminal confirmation and dashboard health checks.
- `present-proposal.mjs` should be the normal entrypoint. It saves the plan, decides the authoritative DB path, and makes sure the dashboard for that workspace points at the same DB.
- Use `--dashboard-url` only when you intentionally want to override the workspace-derived default.
- Avoid exporting one global `SONOL_DASHBOARD_URL` or `SONOL_DASHBOARD_PORT` across multiple workspaces unless you intentionally want every workspace to share that override.
