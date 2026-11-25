---
name: cgagentharness-project-guidance
description: Locate current Harness operating rules, implementation sources and task-specific skills before repository work.
---

# Project guidance

Start with root `AGENTS.md`: it owns the architecture map, truth order, core-path
list, reading restrictions, local verification policy and PR requirements.
Use `INVARIANTS.md` for the affected contract, then trace its implementation,
configuration and callers. Resolve paths from the Harness checkout, including when loaded from user skills.
These are Codex instructions; the app exposes its own `/api/skills`.

## Select the task's sources

| Task | Start here |
|---|---|
| HTTP authority, roles, TLS, CSRF | `src/server/guards.rs`, `src/server/headers.rs`, `tests/auth_guards.rs`, `tests/secure_portal.rs` |
| Shim and child dispatch | `src/shim/mod.rs`, `src/agentic/commands.rs`, `tests/shim_and_agent_routes.rs` |
| Writes, approval, clone jail | `src/agentic/writer.rs`, `src/agentic/workspace.rs`, `tests/write_policy.rs`, `tests/git_approval.rs` |
| Process containment | `src/agentic/executor/sandbox.rs`, `src/common/process.rs`, `src/common/mcp.rs` |
| Defaults and reload | `assets/config.default.yaml`, `src/common/config.rs`, `src/server/config_reload.rs` |
| Routes and slash commands | `src/server/routes/mod.rs`, `src/server/slash.rs`, `src/server/views.rs`, `assets/static/harness.html` |
| Research: search, fetch, goal evidence | `src/server/web_search.rs`, `src/server/web_research.rs`, `src/server/chat_web/evidence.rs` |
| Browser tasks | `src/server/routes/browser.rs`, `src/common/browser_host.rs`, `browser/sidecar.mjs`; separate from goal/loop tools |
| PDF attachments, notes, web | `src/common/pdf_text.rs`; trace the caller before changing extraction or fallback |
| Model budgets and compaction | `src/llm`, `src/server/compaction.rs`, `tests/chat_and_sessions.rs` |
| Ownership, memory, MCP, schedules, notifications, netconnect | Contract-to-test map in `cgagentharness-invariant-guard`; select affected rows |
| Install and packaging | Root README's installation links, `scripts/package-desktop.sh`, `.github/workflows/desktop.yml` |

## Select a skill

See `.codex/skills/README.md` in the checkout. Select the skill for the task:

- Use `fable-protocol` when the premise or evidence needs investigation.
- Use `cgagentharness-invariant-guard` for contract review,
  `cgagentharness-config-guard` for shipped defaults, and
  `cgagentharness-write-policy-redteam` for hostile mutation probes.
- Use `cgagentharness-verify` for smoke/acceptance work or
  `verification-specialist` for an independent supplied-patch assessment.
- Use `cgagentharness-gotchas` to diagnose misleading failures or false passes.
- Use `cgagentharness-release` for artifact provenance and release acceptance;
  `cgagentharness-optimize` for evidence-backed improvements.

## Keep guidance current

Check paths, symbols and filters against the checkout. Keep rules in
`AGENTS.md`, contracts in `INVARIANTS.md` and mechanics in their skills.
Follow the Markdown budget. Skill selection grants no additional authority.
