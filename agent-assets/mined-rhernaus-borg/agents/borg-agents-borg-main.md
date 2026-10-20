# AGENTS.md

This file provides guidance to agents when working with code in this repository.

- Config selection: the CLI uses config.production.toml by default and only falls back to config.toml when the default path was used and config.production.toml is missing ([src/main.rs](src/main.rs)).
- At startup, main ensures config.llm_logging.log_dir exists; missing directories are created ([src/main.rs](src/main.rs)).
- Workspace bootstrap: a Git repo is always initialized in agent.working_dir and an initial commit is auto-created if the repo has no commits to guarantee HEAD exists ([src/core/agent.rs](src/core/agent.rs)).
- Set BORG_USE_MOCK_LLM=true to replace all configured providers with a single mock “default” provider (overrides real API keys) ([src/main.rs](src/main.rs)).
- Ask LLM selection priority: llm.default → llm.code_generation → first available llm entry ([src/main.rs](src/main.rs)).
- Planning LLM fallback uses PLANNING_API_KEY, else OPENAI_API_KEY when no planning entry exists in config ([src/core/planning.rs](src/core/planning.rs)).
- Codegen tools protocol: models must emit JSON lines like {"tool":"Name","args":[...]} and will iterate up to code_generation.max_tool_iterations (default 25) before generating final edits ([src/code_generation/llm_generator.rs](src/code_generation/llm_generator.rs)).
- File targeting: if a code block lacks a nearby file indicator (“file:”/“filename:”/“for file …”), the change defaults to src/main.rs (be explicit to avoid accidental writes) ([src/code_generation/llm_generator.rs](src/code_generation/llm_generator.rs)).
- CodeImprovement parsing also expects “// File: path/to.rs” inside code fences; without it, a single default target is used and may be wrong ([src/core/strategies/code_improvement.rs](src/core/strategies/code_improvement.rs)).
- Commit and merge messages are LLM-generated; the mainline branch is chosen dynamically (master if present, else main). Conflicts abort with no auto-resolution ([src/core/strategies/code_improvement.rs](src/core/strategies/code_improvement.rs)).
- Current plan execution gap: CodeImprovement’s plan does not execute apply/test steps by default; merges can occur without actual applied changes if not handled explicitly ([src/core/strategies/code_improvement.rs](src/core/strategies/code_improvement.rs)).
- Test runners parse “test result:” summaries; rustfmt/clippy are optional and skipped if not installed; coverage/linting defaults are stubbed unless overridden ([src/testing/comprehensive.rs](src/testing/comprehensive.rs), [src/testing/test_runner.rs](src/testing/test_runner.rs)).
- Integration tests generate per-test configs with mock providers and temp workspaces and rely on env!("CARGO_BIN_EXE_borg"); prefer BORG_USE_MOCK_LLM to avoid external API dependencies ([tests/cli_test.rs](tests/cli_test.rs)).
- Quality gate (non-default): `cargo fmt --all && cargo clippy --all-targets --all-features -- -D warnings -W clippy::cognitive_complexity && cargo test --all --locked && cargo audit --deny warnings && cargo build --release --locked --all-features` ([.roo/rules/linting.md](.roo/rules/linting.md)).
- The borg git subcommand bypasses full Agent/Strategy initialization and invokes the LLM code generator directly ([src/main.rs](src/main.rs)).

## Modes v2 (Dispatcher and Six-Mode Architecture)

- Feature flag: modes.v2_enabled controls activation of the new dispatcher-based flow. When false, legacy behavior remains. When true, CLI and agent flows route through the mode dispatcher defined in [src/core/mode_dispatcher.rs](src/core/mode_dispatcher.rs).
- Default provider: OpenRouter. Dynamic model selection is available via [ModelSelectionService::select_for_intent()](src/model_selection/service.rs:379) with intents from [ModeIntent](src/model_selection/policy.rs:10). A sticky selection is used to minimize churn.

Six modes and responsibilities:
- Orchestrate: task decomposition, dependency graph, spawn mode tasks, collate progress, escalate errors.
- Architect: high-level plans, specs, acceptance criteria, constraints, interfaces; emits docs under docs/.
- Code: implementation execution, code edits, diffs, adheres to repo rules, invokes tools; writes via [GitManager](src/version_control/git.rs).
- Review: code review, style/lint/security checks, actionable feedback, approve or block decision; outputs under logs/review/.
- Debug: systematic troubleshooting, hypotheses, experiments, logging diffs, root-cause analysis; outputs under logs/debug/.
- Ethical assessment: evaluates goals and artifacts against ethical guidelines; emits auditable reports; uses [EthicsManager](src/core/ethics.rs:211).

Dispatcher and orchestration:
- Central dispatcher [src/core/mode_dispatcher.rs](src/core/mode_dispatcher.rs) instantiates per-mode runners and enforces guardrails.
- Orchestrate may call Architect → Code → Review → Ethical and Debug as needed; circuit breaker prevents repeated failures.
- Only Code is permitted to modify repository files; Review and Ethical are read-only; Debug writes logs only.

Model selection policy:
- Modes map to intents for model selection:
  - orchestrate → [ModeIntent::Orchestrate](src/model_selection/policy.rs:11)
  - architect → [ModeIntent::Architect](src/model_selection/policy.rs:12)
  - code → [ModeIntent::Code](src/model_selection/policy.rs:13)
  - review → [ModeIntent::Review](src/model_selection/policy.rs:14)
  - debug → [ModeIntent::Debug](src/model_selection/policy.rs:15)
  - ethical → [ModeIntent::Ethical](src/model_selection/policy.rs:16)
- Providers default to OpenRouter; selection is integrated with runtime snapshot set in [set_runtime_model_selection_from](src/core/config.rs:739).

Legacy role mapping and deprecation:
- Legacy llm keys are mapped on load when modes.v2_enabled is present; warn-level deprecation logs are emitted:
  - llm.code_generation → modes.code
  - llm.planning → modes.architect
  - llm.ethics → modes.ethical
  - llm.code_review → modes.review
  - llm.default remains; when unmapped, orchestrate falls back to [ModeIntent::LegacyDefault](src/model_selection/policy.rs:17)
- CLI UX remains unchanged. Ask routes through Orchestrate; Improve executes a single Orchestrate iteration. See [handle_ask_command](src/main.rs:302).

Ethical assessment and auditability:
- Ethical mode produces [EthicalReport] artifacts under logs/ethics/${task_id}/, including request_id, goal_id, risk_level, approval, principle_impacts, mitigations, and evidence. It leverages [EthicsManager](src/core/ethics.rs:211).
- Orchestrate must block merges or downstream Code when Ethical returns is_approved=false or risk_level High unless an explicit, logged override is provided.

Observability:
- Structured logging fields: mode, request_id, provider, model, timings, child_tasks, decisions. Selection logs include candidates and sticky state via [ModelSelectionService::select_for_intent()](src/model_selection/service.rs:379).
- Minimal metrics counters/histograms per mode can be emitted by runners; default no-op.

Implementation references:
- ModeRunner and ModeResult will be introduced alongside [Strategy](src/core/strategy.rs:145). Proposed trait entry point [ModeRunner::run(ctx) -&gt; ModeResult](src/core/strategy.rs:1) or under [src/modes/mod.rs](src/modes/mod.rs) with a dispatcher in [src/core/mode_dispatcher.rs](src/core/mode_dispatcher.rs).
- Full plan, config schema, and test matrix: [docs/rfcs/2025-09-modes-v2-implementation.md](docs/rfcs/2025-09-modes-v2-implementation.md).