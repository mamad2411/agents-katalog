---
name: cargo-audit-workflow
description: >
  Rust cargo-audit / cargo-deny workflow for owned crates: install, CI gates, advisory
  triage, RUSTSEC ignores with expiry, license/ban policies, and fix-then-reaudit. Use
  when cargo audit, cargo deny check, RUSTSEC advisories, or Rust supply-chain CI —
  pair with `rust-style-and-clippy` for code quality.
---

# Cargo Audit Workflow

## Scope And Authorization

- **In scope:** Rust projects and registries you control.
- **Out of scope:** Publishing malicious crates; scanning private third-party repos without permission.
- Advisory data may mention vulnerable versions — keep internal app names redacted if needed.
- Pair with `code-quality-standards` and `rust-style-and-clippy`.

## When To Use

- Adding Rust dependency vulnerability scanning to local/CI workflow.
- Triaging `cargo audit` findings (RUSTSEC-IDs).
- Enforcing licenses, banned crates, or multiple versions with `cargo-deny`.
- Preparing release gates for Rust services/libraries.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Clippy/fmt/style | `rust-style-and-clippy` |
| General SBOM program | SBOM skills |
| Container image scan | Trivy/image skills |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Tool | Focus |
| --- | --- |
| `cargo audit` | Known vulnerable crate versions via RustSec DB |
| `cargo deny` | advisories + licenses + bans + sources |
| `Cargo.lock` | **Must** commit for binaries/apps for reproducible audit |
| Ignore files | `audit.toml` / `deny.toml` exceptions with reasons |
| CI | Fail on unfixed vulnerabilities of agreed severity |

## Workflow

### 1. Confirm scope and success criteria

1. Workspace layout, public vs private crates, release process.
2. Success: lockfile committed; audit/deny in CI; High/Critical fixed or exceptioned with owner/expiry; docs for ignore process.
3. MSRV considerations when bumping deps.

### 2. Inventory

```bash
rustc --version
cargo --version
ls Cargo.toml Cargo.lock deny.toml audit.toml 2>/dev/null
cargo tree -d  # duplicate versions overview
```

1. Ensure application crates commit `Cargo.lock` (libraries may differ — still audit in CI with lock generated).
2. Note git/path patches and private registry sources.

### 3. Install tools and baseline

```bash
cargo install cargo-audit --locked
cargo install cargo-deny --locked
# Or use action binaries in CI with pinned versions
cargo audit
cargo deny check
```

1. Save output as baseline artifact.
2. Record cargo-audit/deny versions.

### 4. Configure policies

**`deny.toml` sketch:**

```toml
[advisories]
vulnerability = "deny"
unmaintained = "warn"
yanked = "deny"
notice = "warn"
ignore = [
  # { id = "RUSTSEC-XXXX-XXXX", reason = "ticket-123; not reachable; review 2026-10-01" },
]

[licenses]
allow = ["MIT", "Apache-2.0", "BSD-3-Clause", "ISC", "Unicode-3.0"]
copyleft = "deny"

[bans]
multiple-versions = "warn"
wildcards = "deny"

[sources]
unknown-registry = "deny"
unknown-git = "warn"
allow-registry = ["https://github.com/rust-lang/crates.io-index"]
```

**`audit.toml` (cargo-audit) sketch:**

```toml
[advisories]
ignore = []
```

1. Prefer fixing/upgrading over ignores.
2. Every ignore: RUSTSEC id, reason, ticket, review date.
3. Ban yanked crates in deny policy.

### 5. Triage and remediate

| Finding | Actions |
| --- | --- |
| Direct dep vuln | Bump in Cargo.toml; `cargo update -p name` |
| Transitive | `cargo update -p vuln_crate`; or upgrade parent; or patch |
| No safe upgrade | Assess reachability; temporary ignore + plan; consider replace |
| Yanked | Force update off yanked version |
| License | Replace crate or legal exception process |

```bash
cargo update -p affected_crate
cargo audit
cargo test
cargo clippy -- -D warnings
```

1. Read advisory carefully (Windows-only? dev-dep only?).
2. For `dev-dependencies` only vulns, still track if used in CI/prod tooling paths.

### 6. CI gate

```yaml
# GitHub Actions sketch
- uses: dtolnay/rust-toolchain@stable
- name: Install cargo-deny
  run: cargo install cargo-deny --locked --version 0.16.1
- run: cargo fetch --locked
- run: cargo deny check
- run: cargo audit
```

1. Use `--locked` builds for apps.
2. Cache cargo registry carefully; still re-check advisories frequently (cron).
3. Optional: daily scheduled audit on default branch.

### 7. Hand off

1. Document ignore renewal process.
2. Dependabot/Renovate for Cargo enabled when possible.
3. SBOM export if org requires (cargo tools / syft).
4. Apply `code-quality-standards` and clippy on upgrade PRs.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Lockfile | Committed for apps | No lock; CI resolves floating |
| Ignores | Reason + expiry | Permanent silent ignore all |
| CI | deny+audit fail build | Audit only local optional |
| Fixes | Upgrade + tests | Stay on vuln “until rewrite” forever |
| Sources | crates.io allowlist | Random git deps unsigned |
| DevDeps | Track if in path | Always ignore dev vulns |

## Output Checklist

- [ ] Tool versions pinned
- [ ] Baseline audit/deny captured
- [ ] `deny.toml` / audit policy committed
- [ ] Findings triaged and fixed or exceptioned
- [ ] CI gate green on main
- [ ] Scheduled re-audit considered
- [ ] Tests/clippy after upgrades
- [ ] Ignore review dates set
- [ ] `code-quality-standards` applied

## Rules

- Prefer upgrades over ignores; time-box exceptions.
- Commit lockfiles for deployable crates.
- Re-run audits regularly — new RUSTSEC entries appear continuously.
- Authorized projects only.
- Style/lint remains `rust-style-and-clippy`; this skill is advisory workflow.
