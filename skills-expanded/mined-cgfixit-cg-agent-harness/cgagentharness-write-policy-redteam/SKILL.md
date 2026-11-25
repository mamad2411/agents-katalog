---
name: cgagentharness-write-policy-redteam
description: Adversarially exercise Harness write policy, approval binding, clone jail and hostile argv when those boundaries change or an audit is requested.
---

# Write-policy Redteam

Read the write, approval and clone-jail contracts in `INVARIANTS.md` and the
shared rules in `AGENTS.md`. Preserve disable-only kill-switch semantics and
separate run, approval, push and publication intent.

Use the Rust suites below. Inspect fresh-policy, approval and rollback
assertions before selecting probes; an old end-to-end success test alone does
not establish those boundaries.

| Surface | Primary corpus |
|---|---|
| Writer / gate order / plan integrity | `tests/real_repo_loop.rs::writer_gates_in_order_and_plan_integrity` (+ publish/confirm paths in the same file) |
| Fresh policy / separate intent | `tests/write_policy.rs`, `tests/write_kill_switch.rs` |
| Git approval / digest, mode, origin, exact commit, index lock, disabled extensions | `tests/git_approval.rs` |
| Exact edits / preflight / failed rollback quarantine | `tests/exact_edits.rs`, unit tests in `src/agentic/workspace.rs` |
| Shipped-on local retrieval / sensitive reads / cloud refusal | `tests/real_repo_loop.rs`; trace `src/agentic/repo_retrieval.rs` |
| Clone / read jail | `agentic_foundations::apply_proposal_refuses_jail_escapes_and_oversize_content`, `read_jail_refuses_symlink_escapes_without_following_the_leaf` |
| Hostile argv / confirm never manufactured | `tests/shim_and_agent_routes.rs` hostile-argv matrix, `a_request_can_never_carry_an_argv`, publish-missing-confirm → child exit 4 |
| Protected Rust check inputs | `invariant_guard::shipped_defaults_protect_rust_check_configuration` covers YAML and Rust fail-safe defaults |
| Kill switch AND-only / shipped gates | `invariant_guard::writer_kill_switch_is_and_not_or`, `shipped_config_enforces_accounts_tls_and_keeps_execution_gates_closed` |

## Exercise refusal paths

Inspect assertions and callers before choosing filters. For example:

```sh
GROK_API_KEY='' ANTHROPIC_API_KEY='' DEEPAGENT_API_KEY='' \
  cargo test --locked --test real_repo_loop writer_gates_in_order_and_plan_integrity -- --exact --nocapture
```

Verify the output names the intended test. Run the other affected refusal cases;
a request for a full write-policy audit requires every applicable table row.
Follow `AGENTS.md` for local scope rather than running unrelated targets.

## Classify results

| Bucket | Meaning | Action |
|---|---|---|
| **new_bypasses** | Attack that should refuse (exit 4 / 422 / jail) now succeeds or assert was deleted | **Regression.** Fix before anything else. Never loosen the assert. |
| **known_gaps** | Documented residual / weaker-than-name signal already called out in `INVARIANTS.md` | Fix within the authorized scope; otherwise report the remaining decision. Preserve policy. |
| **fixed_findings** | Prior gap now refuses with evidence | Bank a durable regression test; keep the assert. |
| **false_greens** | Suite green because confirm was defaulted, kill switch OR-ed, Seatbelt skipped, or shared listener used | Treat as FAIL of the verification method — reproduce with owned temp `CGAGENTHARNESS_HOME` + unique port. |

## Locate the owning boundary

- **Gate order** — `agentic.enabled` / mode / `writes_enabled` / reason /
  confirm / `allow_git_write_tools` (`src/agentic/writer.rs`)
- **Confirm+reason** — never defaulted; missing confirm → exit 4
- **Kill switch** — AND-only env disable
- **Argv boundary** — `--opt=value` single elements; browser never supplies argv
  (`src/shim`, `src/server/agent_policy.rs`)
- **Clone jail** — landed-path judgment, symlink / `.git` name-equivalence
  (`src/agentic/workspace.rs`)
- **Approval binding** — digest, modes, live tree, index, origin and approved commit
- **Policy revocation** — recheck disk at each mutation; confirm for run,
  approval, push and publication are separate intents

## Verify authorized fixes

- Prefer the smallest refuse path that restores the invariant (one gate check,
  one argv validation, one jail predicate).
- Add or extend a Rust test assert in the matching file above — same style as
  existing hostile matrices.
- Re-run Step 1 for the touched tests, then the related
  `invariant_guard` / `auth_guards` set if shared routing changed.
- **Never** default `confirm`, make `reason` optional, OR the kill switch, or
  delete/skip an assert to green.

Retain recovery backups after quarantine. Report exercised refusals (including
exit 4), commands, exits, SHA and gaps. Pair with `cgagentharness-invariant-guard`
for core-path assessment.
