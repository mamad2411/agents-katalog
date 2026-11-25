---
name: cgagentharness-config-guard
description: Check shipped Harness configuration defaults and fail-closed gate semantics before config changes or a requested defaults audit.
---

# Config guard

Assess `assets/config.default.yaml` against current code and `INVARIANTS.md`.
This is a read-oriented assessment; corrections need an authorized change set.
Use `cgagentharness-invariant-guard` for implementation and topology review.

## Contracts

Report broken contracts as FAIL and unexecuted checks as NOT RUN.

| ID | Check and authoritative evidence |
|---|---|
| H1 | `flag_is_true` accepts only literal YAML `true`; missing keys and strings stay off. `tests/common_layer.rs::quoted_true_is_off`. |
| H2 | Use `invariant_guard::shipped_config_enforces_accounts_tls_and_keeps_execution_gates_closed` for shipped gates, empty grants and provider fallback. Local clone retrieval ships on; write gates and Linux netns fallback ship off. Check first-run Google-only URL seeding and existing-home preservation in `tests/common_layer.rs`. |
| H3 | Plaintext credential storage ships off and is restart-only. `security.api_key_optional` grants no authority. |
| H4 | Writes require human reason and per-call confirm; inspect writer, `tests/real_repo_loop.rs` and shim route assertions. |
| H5 | `CGAGENTHARNESS_AGENTIC_WRITE_DISABLE` only disables; `EXECUTION_ENABLED` cannot be flipped to fake a passing refusal. `tests/write_kill_switch.rs`. |
| H6 | Serve remains loopback-only; distinguish its bind policy in `src/server/mod.rs` from model endpoint validation in `src/llm`. |
| H7 | Mode/write-enabled alone grants no mutation: fresh disk policy, master/deepagent/clone-write gates and separate intents remain required. `tests/write_policy.rs`. |
| H8 | The shipped-config test locks the prompt-filter pattern count; inspect its current assertion rather than copying the count here. |
| H9 | Check `shipped_defaults_protect_agent_instruction_files`, `shipped_defaults_protect_rust_check_configuration` and `shipped_defaults_deny_sensitive_read_basenames`. |
| H10 | Auth/TLS reject invalid switch types: `tests/common_layer.rs::security_switches_require_boolean_values`. Numeric types are checked at `AppConfig::load`; missing retains defaults, malformed refuses. `tests/invariant_guard.rs::numeric_config_reads_are_type_checked_at_load`, `src/common/config.rs` units. |
| H11 | The shipped-config test locks pinned/structured-memory defaults. Saved explicit choices win; proposals remain pending until reviewed. Use `tests/common_layer.rs` and `tests/structured_memory_suggestions.rs` for persistence and proposal behavior. |
| H12 | Firecrawl ships off; its gate and hourly cap are restart-only. See `src/server/web_firecrawl.rs::tests::config_ships_off_and_refuses_a_bad_cap` and `config_reload::RELOADABLE`. |
| H13 | `browser.enabled` ships on, restart-only; literal true and admin authority are required. Trace `src/server/routes/browser.rs`. |
| H14 | `web.search.result_reads.enabled` ships on and uses `flag_missing_on`; malformed values fail boot. Its `arxiv_pdf` child ships on but requires literal true. See `MISSING_MEANS_ON` and `src/server/web_provider.rs`. |

## Execute and interpret

Select affected filters with the root rustup toolchain:

```sh
GROK_API_KEY='' ANTHROPIC_API_KEY='' DEEPAGENT_API_KEY='' \
  cargo test --locked --test invariant_guard shipped_ -- --nocapture
GROK_API_KEY='' ANTHROPIC_API_KEY='' DEEPAGENT_API_KEY='' \
  cargo test --locked --test common_layer -- quoted_true_is_off security_switches_require_boolean_values --nocapture
```

Confirm the selected tests ran. Exercise affected refusal paths separately.
Report each applicable ID with commands, results, SHA and gaps. Align approved
default changes with code, config and the PR invariant statement.
