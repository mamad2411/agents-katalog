---
name: cgagentharness-invariant-guard
description: Assess Harness security contracts against a tree or diff, including core-path merge checks and requested invariant audits.
---

# CG-agent-harness invariant guard

Read `AGENTS.md` and affected `INVARIANTS.md` sections. Trace callers.
Select affected checks or run the target for a full invariant audit:

```sh
GROK_API_KEY="" ANTHROPIC_API_KEY="" DEEPAGENT_API_KEY="" \
  cargo test --locked --test invariant_guard -- --nocapture
```

Targets denote `tests/<target>.rs`; source modules add unit tests. Exercise
applicable refusals and check for contracts newer than this map.

| Contract | Evidence to select |
|---|---|
| I6, action whitelist, duplicated constants, CSRF placeholders, route registration | `invariant_guard`, `shim_and_agent_routes`; `src/shim/mod.rs`, `src/server/routes/mod.rs` |
| Account bootstrap, roles, TLS, Host/origin, CSRF, redaction | `auth_guards`, `secure_portal`, `security_headers`, `common_layer`, `panels` |
| Fresh mutation policy, separate approval/push/publication intent, kill switch | `write_policy`, `write_kill_switch`, `real_repo_loop` |
| Reviewed tree/mode/origin binding, index lock, Git extensions refused | `git_approval`, `agentic_foundations` |
| Clone/read jail, denied basenames, local-only retrieval, hash revalidation | `agentic_foundations`, `real_repo_loop`; `src/agentic/repo_retrieval.rs` |
| Whole-proposal preflight, rollback/quarantine, exact edits | `exact_edits`, `real_repo_loop`; `src/agentic/workspace.rs` |
| Sandbox selection, capture, cancellation and cleanup | `macos_cargo`, `linux_bwrap`, `process_lifecycle`, `process_writer_outcome`; `src/agentic/executor/sandbox.rs` |
| Sync/jobs/schedules share preparation, owner checks, reviewed goals, at-most-once occurrences | `shim_and_agent_routes`, `agent_schedules`, `owner_isolation` |
| Owned sessions/export/adoption, memory gates, pending-only proposals, recall revalidation | `owner_isolation`, `session_export`, `structured_memory`, `structured_memory_phase7`, `structured_memory_suggestions` |
| Web policy, DNS pinning, listing/arXiv grants and revocation | `web_research`, `web_phase2_redteam`, `chat_web`; `src/server/web_policy.rs` |
| Bounded PDF worker and same-URL Firecrawl eligibility | `src/common/pdf_text.rs`, `src/server/web_firecrawl.rs`; trace attachment, notes and web callers |
| /browse origin grants and stop on hold or hand-off | `src/server/routes/browser.rs`, `src/common/browser_host.rs`; fixtures in `scripts/browser-use-eval.sh` |
| Detached web jobs: owner, gates, restart loss, delivery-time policy | `web_research`; `src/server/web_research.rs`, `src/common/process.rs` |
| Outbound MCP capabilities, broker confirmation, platform containment, MCP excluded from loops | `mcp_client`, `mcp_lifecycle`, `mcp_windows`; `src/common/mcp.rs` |
| Inbound MCP machine-key authority, owner-only reads, empty grants, revocation | `mcp_server`; `src/server/mcp_keys.rs` |
| Atomic limit reload, unchanged authority/rate history, restart-only settings | `secure_portal`; `src/server/config_reload.rs::RELOADABLE` |
| Numeric types checked at load, missing versus malformed | `invariant_guard::numeric_config_reads_are_type_checked_at_load`; `src/common/config.rs` |
| Compaction, goal evidence and stopped turns | `chat_and_sessions`, `chat_web`, `loop_runner`; `src/server/compaction.rs`, `src/server/chat_web/evidence.rs` |
| Incomplete billed replies, prediction versus usage, private notification retries | `spend_ledger`, `notifications`; `src/llm/cloud_chat.rs` |
| Loopback Ollama pull/warmup, no num_ctx, native sidecar identity | `ollama_manage`, `scripts/test-desktop-backend.py`; `docs/DESKTOP.md` |
| Provider-key storage, plaintext opt-in, hot reload, child scrubbing, private Windows credentials | `src/common/credential_store.rs`, `src/server/env_keys.rs`; `windows_private_credentials`, `child_env` |
| LAN scope, closed netconnect gates, bounded dialing, passive status | `netconnect_flags`, `netconnect_scope`, `netconnect_cli`, `netconnect_syscall`; `src/netconnect/connect.rs` |
| Guidance and Markdown limits | `invariant_guard::markdown_stays_on_the_docs_budget`; inspect `DOCS_BUDGET` and group caps |

## Inspect boundaries and report

Check new routes/actions against the registration requirements in `AGENTS.md`
and shipped defaults with `cgagentharness-config-guard`.

Respect documented limits: process-global CSRF is not session-bound;
process-group cleanup is not strict containment; private storage is not
encryption; external policy edits and syscalls are not one transaction.

Report each contract as PASS, FAIL or NOT RUN with commands, results, SHA
and platform gaps. A zero-test filter is NOT RUN. Structural checks prove
only the asserted structure.
