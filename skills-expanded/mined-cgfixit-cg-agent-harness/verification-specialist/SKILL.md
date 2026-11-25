---
name: verification-specialist
description: Independently assess a supplied Harness patch with negative probes and executed evidence, without modifying its implementation.
---

# Verification Specialist (harness)

Independently assess a supplied patch without modifying its implementation.
Use `cgagentharness-verify` for ordinary smoke/acceptance work.

## Hard rules

1. **Do not modify the project.** No create/edit/delete under the repo. No
   `git add/commit/push/checkout/rebase`. No dependency installs as part of
   this skill. Short-lived probes may use `/tmp` or `$TMPDIR` and must be
   cleaned up.
2. **PASS requires executed command output.** Set `CARGO_TARGET_DIR` outside
   the checkout; source inspection alone is not behavioral verification.
3. **At least one applicable negative probe** before an overall PASS: exercise
   a refusal path for behavior changes, or a broken-reference/invalid-input
   case for documentation and checker changes.

## Inputs

Original task, files touched, approach, optional plan/spec path. Record tested
HEAD/base and scope.

## Harness surfaces (select by change)

| Change class | Evidence / probes |
|---|---|
| HTTP guards / CSRF / Host | `tests/auth_guards.rs`, `tests/security_headers.rs`; same-origin + CSRF absent → reject; Host must be loopback; account/RBAC required for operations; harness API key optional and never authority; placeholders `__CYCLAW_CSRF_TOKEN__` / `__CYCLAW_CSP_NONCE__` / `X-CyClaw-CSRF` unchanged |
| Shim whitelist / exit codes | `tests/shim_and_agent_routes.rs`, `tests/invariant_guard.rs`; ACTIONS whitelist; hostile argv → 422; exit API `0/2/3/4` (`4` = write refused) |
| Write refused paths | `tests/write_policy.rs`, `tests/git_approval.rs`, `tests/write_kill_switch.rs`; fresh disk policy, separate confirmation, reviewed tree/origin binding |
| Clone / check sandbox | `tests/agentic_foundations.rs`, `tests/macos_cargo.rs`, `tests/linux_bwrap.rs`; verify the selected backend, including default refusal without bubblewrap on Linux |
| Config / shipped gates | `shipped_config_enforces_accounts_tls_and_keeps_execution_gates_closed`; `flag_is_true` (quoted `"true"` OFF) |
| Live serve / smoke | Owned temp `CGAGENTHARNESS_HOME` + **unique port**; never assume default `:8790` is this binary (`scripts/smoke-ollama.sh` pattern) |
| Ownership, memory, MCP, web, reload, jobs | Select refusal cases from `cgagentharness-invariant-guard`. For PDF changes, distinguish local worker refusal from authorized Firecrawl fallback; for `/browse`, check origin refusal or stop on hand-off. |
| Desktop package | Packaging/signing evidence ≠ HTTP console proof; WKWebView ≠ fetch/CSRF semantics; ad-hoc ≠ Developer ID |

Targeted tests only, planner keys blank (CI runs the suite):

```text
GROK_API_KEY="" ANTHROPIC_API_KEY="" DEEPAGENT_API_KEY="" \
  cargo test --locked --test <target> <filter> -- --nocapture
```

Follow `AGENTS.md` for local scope. Prose needs syntax, reference and budget checks.

## Workflow

1. Read `AGENTS.md`, `INVARIANTS.md`, the diff, and relevant callers.
2. Run the narrowest locking tests for the change; expand for shared
   routing/config/security.
3. Execute a negative probe at the changed boundary: hostile argv, missing
   confirm, foreign owner, jail escape, or malformed documentation/checker input.
4. For each finding: expected behavior, reachable trigger, actual impact,
   pre-existing vs introduced. Env/platform limits ≠ product defects.
5. Report per-check:

```text
### Check: <name>
**Command run:** <exact>
**Output observed:** <verbatim>
**Result: PASS|FAIL|NOT RUN**
```

Overall: exactly one of:

```text
VERDICT: PASS
VERDICT: FAIL
VERDICT: PARTIAL
```

PARTIAL means required evidence is missing or inconclusive; name the missing
check or unresolved question. FAIL requires an observed violated contract. PASS
covers only the stated scope, not unrelated platforms or authority boundaries.

## Evidence limits

A zero-test filter is NOT RUN. Match results to the source or artifact.
Use separate evidence for console Chrome, `/browse` and native WKWebView.

## Boundary

Apply Harness contracts from `INVARIANTS.md`; preserve assertions. This
assessment does not grant mutation, publication or merge authority.
