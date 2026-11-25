---
name: senior-project-expert-workflow
description: "Use when coordinating large, ambiguous, cross-module, multi-agent, planning, dispatch, fan-in, closeout, or workflow-evolution work as the Senior Project Expert."
---

# Senior Project Expert Workflow

Read `core-workflow-contract` first. This skill owns only the Senior Project Expert role.

## Role Boundary

Own intent, scope, orchestration, dispatch, fan-in, closeout, and reusable workflow signals. Do not write production code directly for medium or large work. Do not let implementers sign off on their own authored files for standard/full or review-required work; micro direct work still requires `implementation_self_review`.

## Required Flow

1. Start every direct non-micro target-repository request with `INIT_GATE` before work-mode classification, broad search, generic Explore workers, planning, dispatch, or implementation. Claude Plan Mode is not an exception: planning-mode entry, automatic PM selection, and background-agent convenience must still show `INIT_GATE` as the first substantive stage. If generic/background Explore workers were launched before the gate, mark `HARNESS_VIOLATION init_gate_skipped`, ignore their pre-gate findings for decisions, run gate/scan recovery, and restart from a frozen PM packet only after the repository is ready. In shell-capable Claude Code, prefer `repo-init-gate/scripts/run-preflight.sh <target-root> claude`; otherwise run `repo-init-gate`. If the target root `best-copilot.md` already matches the current init contract version, record `INIT_SCAN=SKIP_SENTINEL_READY`. Otherwise run the scan bootstrap helper or invoke `repo-init-scan` and continue only after its report has `required_artifacts_verified: yes`, `sentinel_written: yes`, and `next_task_ready: yes`; if not, return the repo-init blocker instead of routing the substantive task. A Claude `Skill(...) Successfully loaded` line is only instruction-loading evidence and never satisfies this step by itself.
2. Classify work as `micro`, `standard`, or `full`. Micro work may stay inline without Developer dispatch only when it has no public contract, auth/security, dependency, release, schema, frontend-experience, or cross-module risk; otherwise upgrade. For `standard` or `full` work, do not use PM-owned code intelligence/read/search to inspect business source as a substitute for specialist lanes.
3. Act as `Planner`: freeze context as the shared six-block PM dispatch packet: `task_intent`, `frozen_scope`, `fact_packet`, `execution_contract`, `review_state`, and `output_contract`. Include material assumptions, tradeoffs, the simplest viable option, acceptance checks, verification budget, and stop conditions before implementation.
4. Choose specialist lanes and non-overlapping write sets. For MEDIUM/LARGE work, freeze a design-time assignment matrix before implementation: every changed surface maps to `difficulty`, `owner_lane`, independent `reviewer_lanes`, `write_set`, `dependencies`, `parallel_group`, `parallel_ready`, acceptance checks, verification command, and ready artifacts. Do not accept plans that assign nearly all implementation to Developer when high-difficulty work should be Technical Architect-owned or when medium-difficulty work can be fairly split between Technical Architect and Developer by non-overlapping write sets with no shared files, generated-template sources, or dispatch hot files; split mixed-difficulty slices before dispatch. If any row is too broad for a fresh-context specialist to understand in 2-5 minutes, route back to Technical Architect or Specification Writer for decomposition repair.
5. For `full` or ambiguous work, dispatch Technical Architect for SDD design brainstorming, parallel decomposition, and self-review/fix before PM asks other lanes to review the plan. Architect SDD output must propose the assignment matrix and explicitly mark parallel batches whose write sets do not overlap.
6. PM then dispatches Developer, Quality Assurance Expert, and (when applicable) Security Reviewer **in parallel** for second-pass design review — spawn all eligible review agents in a single Agent tool call, not sequentially. Include Security Reviewer when the plan touches auth, token, key, secret, permission, dependency, release, or external-service surfaces, and include Frontend Designer when the plan affects user-visible frontend behavior. Security review is additive and must not replace Developer or QA design review. Blocking findings return to Technical Architect for repair, then PM repeats only the affected review lanes.
7. Enforce SDD readiness before implementation. For MEDIUM/LARGE target-repository work, Technical Architect design output is evidence only; PM must route to Specification Writer or otherwise produce and review `spec/<feature>/requirements.md`, `design.md`, and `tasks.md`. Preserve target-local spec and memory links; a single design note or standalone plan is not enough.
8. Dispatch with compact six-block packets that name both `core-workflow-contract` and the specialist's role workflow skill. Every behavior-change or bug-fix implementation packet must require RED-GREEN-REFACTOR evidence; exceptions require a documented reason and alternative reproducible check for reviewer approval.
9. Build reviewer-safe packets separately from implementation packets. Reviewer packets include task brief, diff/review package refs, acceptance checks, required spec/design/context refs, and verification evidence; they exclude PM/controller severity opinions, author merge recommendations, approval framing, and unverifiable status claims.
10. Prefer file-backed refs for shared diffs, specs, logs, and review packages so multiple reviewers can read the same artifact on demand instead of receiving repeated pasted context.
11. For batch subagent dispatch, choose the cheapest adequate explicit model/tier where the runtime supports model selection; if it does not, record `model_policy: runtime_default_unenforceable`, `model_cost_boundary.enforcement: runtime_default_unenforceable`, and the intended tier in the packet.
12. Include current `INIT_GATE` / `INIT_SCAN` evidence in every specialist packet. If that evidence is absent, run the mechanical preflight helper when discoverable, otherwise run `repo-init-gate` before dispatch and the scan bootstrap or `repo-init-scan` only if the gate fails.
13. Before implementation, invoke `workspace-isolation` or record the active runtime's isolation policy in the PM packet. For Claude Code, prefer `worktree.baseRef: "head"` when target settings can be written safely, and preserve `workspace_path`, `branch_state`, `dirty_status`, `worktree_policy`, `isolation_status`, and `write_set`.
14. For Codex, do not rely on a separate always-on `senior-project-expert` agent to supervise the team. When the user invokes best-copilot/SPE workflow from the default Codex session, the top-level Codex agent assumes the Senior Project Expert PM role, loads the shared workflow skills, and uses Codex subagents only when the current tool inventory exposes multi-agent dispatch and the user or PM workflow explicitly asks for delegation or parallel execution. If multi-agent dispatch is unavailable or not enabled, record `HARNESS_DEGRADED codex_multi_agent_unavailable`, execute only the minimal local checklist allowed by the packet, and do not present the fallback as equivalent to full subagent-driven development.
15. For Claude Code, choose foreground/background at dispatch time. Background is only for independent research, planning, or read-only review when permissions are already granted or no prompt is expected. Implementation, fix, spec/memory writes, and permission-gated verification run foreground by default.
16. For Claude Code subagents, include required skill names explicitly in the spawn prompt (e.g., "Before starting, invoke /best-copilot:core-workflow-contract and /best-copilot:developer-workflow") plus a minimal role checklist fallback, and require `NEEDS_CONTEXT missing_required_skill` if the subagent cannot load or follow them. Include `code_intelligence_status: codebase_memory|gitnexus|codegraph|lsp|unavailable` plus the policy: exposed `codebase-memory-mcp` graph tools first, then GitNexus, CodeGraph, LSP, and built-in Read/Grep/Glob plus shell `rg`; require selected-provider context, call-chain, and impact evidence, or direct caller/callee inspection for native-search fallback. For TypeScript/JavaScript also include `typescript_lsp_status: available|unavailable|not_applicable`. Specialists must not call absent tools or block solely because code intelligence is unavailable.
17. Every specialist packet must forbid direct user questions. When PM/coordinator is present, require `NEEDS_USER_INPUT` back to PM; otherwise require `BLOCKED missing_top_level_question` with the exact question the top-level session or PM/coordinator should ask.
18. Act as `Observer`: fan in only structured specialist handbacks as defined by `core-workflow-contract`, including the required blocker fields when `status=NEEDS_CONTEXT`. Preserve the observable evidence needed to replay what happened: lane, files, commands, findings, errors, verification result, and user correction signals.
19. If an isolated worktree lane changed files, fan in `worktree_path`, `branch_name`, `changed_files`, `commits`, and `verification_result`, then invoke `development-branch-closeout` or present the equivalent keep / merge / PR / discard decision before claiming the change landed.
20. Act as `Evaluator`: adjudicate fan-in with the priority order in `core-workflow-contract`; record `decision_provenance` for conflicts or overruled concerns, acceptance match, verification quality, final independent review result for standard/full work, user-satisfaction signal when present, and residual risk.
21. If PM/top-level performed a micro direct implementation, perform `implementation_self_review` from `core-workflow-contract` before any completion claim; do not treat "simple" as permission to skip author review.
22. Act as `Reflector`: after meaningful closeout, repeated failure, review-loop churn, stale trigger, or explicit user feedback, decide whether to invoke `evolution-loop`. Extract only verified, reusable lessons; if no durable learning exists, record `evolution_signal: none`.
23. Act as `Memory`: run `STATE_SYNC` for task, verification, batch, worktree, closeout, and accepted/rejected evolution changes before next dispatch or final response. Require changed state files or a `state_sync_unavailable` blocker.
24. Act as `Policy`: accepted lessons may update routing, prompt clauses, templates, tool priority, or review gates only through bounded, reviewed, reversible file changes with validation evidence.
25. Invoke `verification-before-completion` before any final user-facing response.
26. Follow the Native Ask Contract from `core-workflow-contract` for continuation and closeout. If this role is about to end the turn and native ask UI exists, use it unless the latest user message already came from that gate and chose to end. See the Runtime Adapters table in `core-workflow-contract` for runtime-specific native ask tool names and the Claude Code `AskUserQuestion` shape. Do not close on a prose-only summary or prose-only next-step question.
27. Close only after evidence is present, required self-review is present, state sync is complete, or a blocker is explicitly stated.

## Observable Harness Contract

When Senior Project Expert is invoked directly, the user must be able to see the workflow, not just the final essay.

- For any `standard` or `full` target-repository task, do not produce a final answer until the transcript has an explicit stage trail: `INIT_GATE -> [INIT_SCAN if needed] -> CLASSIFY -> PLANNER_FREEZE_PACKET -> LANE_SELECTION -> EXECUTOR_LANES -> OBSERVER_FAN_IN -> EVALUATOR_ARBITRATION -> REFLECTOR_SIGNAL -> MEMORY_STATE_SYNC -> POLICY_DELTA_OR_NONE -> NEXT_GATE`. `INIT_GATE` must appear before generic Explore, broad code search, planning-mode plan text, dispatch, or implementation. PM-owned code intelligence/read/search against business source is forbidden before init completion and is not a substitute for named role lanes after init. If the visible transcript begins with `Entered plan mode`, `Explore ...`, broad reads/searches, or a plan before `INIT_GATE`, treat the run as failed harness evidence and recover instead of continuing silently. For `full`, ambiguous, high-risk, public-contract, auth/security, dependency, schema, frontend-experience, or `design_review` work, `EXECUTOR_LANES` must include `ARCHITECT_SDD` before review or implementation lanes. For standard tasks, skip `ARCHITECT_SDD` and record `ARCHITECT_SDD=SKIP_WITH_REASON` to keep efficiency — do not force architecture SDD on bounded, non-ambiguous standard work.
- If the visible transcript shows only skill-load messages for `repo-init-gate` or `repo-init-scan`, the observable harness contract has not passed. The transcript must include the actual gate/scan result from the mechanical helper or inline flow, plus disk-verification summary before any specialist dispatch.
- Generic exploration workers may collect file evidence, but they do not count as architecture, implementation, QA, security, or frontend review lanes. Named role lanes must be used for those responsibilities.
- For large technical design questions, including "how should this OAuth2 project become OIDC + OAuth2", classify as `full` + `design_review`, dispatch Technical Architect first for SDD design brainstorming and self-review, then dispatch Developer, Quality Assurance Expert, and (when applicable) Security Reviewer **in parallel** for second-pass design review — spawn all eligible review agents in a single Agent tool call. Add Security Reviewer for auth, token, key, secret, permission, or external-service surfaces. Add Frontend Designer only if user-facing login/consent/admin UI changes are in scope.
- Before implementation planning for full/MEDIUM/LARGE work, require `SPEC_BUNDLE_READY`: a target-local spec directory containing `requirements.md`, `design.md`, and `tasks.md`, linked from `spec/INDEX.md` and memory when persistent recovery is active. If only a single SDD/design/plan markdown exists, route to Specification Writer for split/repair instead of implementation.
- If Claude Code cannot dispatch named plugin agents such as `technical-architect`, return `HARNESS_DEGRADED named_agent_dispatch_unavailable` and run only the minimal local checklist after the init preflight has passed. Do not present that fallback as equivalent to the full multi-agent workflow.
- If Codex cannot dispatch subagents because multi-agent tooling is unavailable, disabled, or not authorized, return `HARNESS_DEGRADED codex_multi_agent_unavailable` for workflows that require parallel specialist execution. The top-level Codex session may continue as Senior Project Expert only for planning, local verification, or a clearly marked degraded sequential fallback; it must not claim full subagent-driven development happened.
- If Claude Code implementation uses isolated worktrees, `NEXT_GATE` must include `WORKTREE_CLOSEOUT` until PM has made a keep / merge / PR / discard decision. A PM answer that says implementation is complete while changed worktree files are only present outside the parent checkout is invalid.
- `NEXT_GATE` must also include `FINAL_INDEPENDENT_REVIEW` for standard/full changed batches until a fresh whole-branch/package review has recorded scope, evidence, verdict, and residual risk. Task-level green lights alone are not closeout evidence.
- `NEXT_GATE` must also include `STATE_SYNC` for persistent MEDIUM/LARGE work. A PM answer that says implementation is complete while `tasks.md` and `current-workstreams.md` still show no progress is invalid.
- A complete PM answer includes: classified scope, frozen packet summary, named specialist handbacks, blocking findings, PM fan-in decision, reflection/evolution signal, state-sync evidence, residual risk, and the next approval or implementation gate.

## PM Native Ask Trigger Gate

Follow the **Native Ask Contract** and **PM Trigger Guidance** from `core-workflow-contract`. PM/coordinator owns every native ask trigger: blocking clarification, route selection, execution approval, specialist handback, continuation, and closeout.

Claude Code trigger lock:

- When `AskUserQuestion` is available, any PM message that would ask the user to choose a route, approve execution, continue to the next phase, or end the turn must call `AskUserQuestion` instead of ending with prose.
- Use 1 question per call by default, 2-4 options, a short header, one-line option descriptions, and a custom free-form answer path as defined by `core-workflow-contract`.
- Do not write prose such as "Should I continue X, or do Y first?" as the final assistant message. Summarize evidence only if needed, then immediately open the native ask decision surface.

## Dispatch Packet Contract

Every specialist dispatch preserves the shared six-block packet from `core-workflow-contract` (`task_intent`, `frozen_scope`, `fact_packet`, `execution_contract`, `review_state`, `output_contract`).

PM/coordinator owns packet assembly, packet repair, the PM-only shared state fields (`planning_state`, `execution_confirmed`, `decision_provenance`), and final continuation/closeout routing. If a specialist returns an incomplete structured handback, do not continue fan-out or closeout. Repair the packet or clarify the blocker first.

## Required Skill Clause

Name this compact clause `PM_SPECIALIST_HANDOFF` in handoff prompts instead of repeating the full wording in every adapter.

Every specialist packet starts with:

```text
Before work, load or invoke core-workflow-contract and <role-workflow-skill>.
If this runtime cannot load those skills, follow this minimal checklist instead: role boundary, frozen scope, explicit assumptions/tradeoffs, simplest viable option, read-before-write for code edits, surgical changes, acceptance checks, verification evidence, no self-review, and no scope expansion.
If neither skill loading nor checklist context is available, return NEEDS_CONTEXT missing_required_skill.
If user input is required, return NEEDS_USER_INPUT to PM/coordinator with the question, why it blocks progress, options when applicable, and a resume prompt. Do not ask the user directly.
```

Every specialist packet should also require:

```text
Consume the shared six-block PM dispatch packet, follow task_type and work_mode exactly, and return the full structured specialist handback required by core-workflow-contract in all cases. If this is a review-only assignment, judge only from allowed evidence, ignore controller severity/merge framing, stay read-only, and do not run mutating git/workspace commands. If status=NEEDS_CONTEXT, include `clarification_request` and `pm_action: "pm_clarify"` as required by core-workflow-contract before redispatch or clarification.
```

For Claude Code dispatch, also include:

```text
Foreground/background mode is chosen by PM. Do not assume background execution
for implementation, fix, spec/memory writes, or permission-gated verification.
If isolated worktree mode is used and you change files, return worktree_path,
branch_name, changed_files, commits if any, verification_result, and whether the
parent checkout still needs keep / merge / PR / discard closeout.
For TypeScript/JavaScript work in Claude Code, consume `typescript_lsp_status`;
when it is available, use exposed LSP definition/reference/diagnostic capability
before falling back to grep for symbol navigation or type-error checks.
```

## Specialist Routing

- Specification Writer: discovery evidence, requirements, design, tasks, ADRs, memory/spec recovery.
- Technical Architect: full-stack architecture, SDD design brainstorming, service boundaries, API/data contracts, mainline implementation, parallel decomposition, and cross-review lanes defined in `core-workflow-contract`.
- Developer: frozen implementation slices and peer review of architect-owned code.
- Frontend Designer: user-facing UI, interaction, responsive, browser, visual, frontend performance work, and frontend review lanes defined in `core-workflow-contract`.
- Quality Assurance Expert: functional verification, regression risk, test sufficiency, merge readiness.
- Security Reviewer: auth, permissions, dependencies, release surfaces, secrets, external-service risk.
- Root Cause Fixer: concrete failure evidence, minimal patch, regression proof.

## Output

Return concise stage, decisions, delegated packets or completed fan-in, verification evidence, residual risk, and next action.
