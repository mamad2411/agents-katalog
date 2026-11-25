---
name: brakeman-rails-scan
description: >
  Run and triage Brakeman static analysis on Ruby on Rails apps you own: install/pin,
  repo config, confidence filters, JSON/SARIF reports, CI gates, ignore-file hygiene,
  and fix-then-rescan for SQLi, XSS, mass assignment, redirects, and related Rails sinks.
  Use when Brakeman, brakeman.yml, Rails SAST, brakeman -A, brakeman ignore, Rails
  security scan CI, or interpreting Brakeman High/Medium/Weak warnings on authorized codebases.
---

# Brakeman Rails Scan

## Scope And Authorization

- **In scope:** Ruby on Rails repositories you own or are authorized to scan and fix.
- **Out of scope:** Scanning third-party apps without permission; treating Brakeman as a green-light for exploit development outside RoE.
- Prefer running on CI and developer laptops against full source, not production containers only.
- Redact connection strings and secrets that appear in report snippets.
- Pair fixes with `code-quality-standards` and Rails security review practices.

## When To Use

- Adding Rails SAST to a repo or CI pipeline.
- Triaging Brakeman findings (SQL injection, XSS, dangerous send, mass assignment, open redirect, unsafe constantize, etc.).
- Maintaining `config/brakeman.ignore` with justifications — not silent permanent mutes.
- Comparing `brakeman -A` (all checks) vs default for deeper review.
- Generating SARIF/JSON for security dashboards.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Ruby dependency CVEs (bundler-audit) | bundler-audit / SCA skills |
| General secure SDLC | `secure-sdlc-checklist` |
| Business logic / IDOR testing | `business-logic-vuln`, `idor-broken-object-authorization` |
| Secret scanning | `secrets-management-hygiene` / gitleaks skills |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Tool | Brakeman (path-sensitive SAST for Rails) |
| Config | `config/brakeman.yml` or CLI flags; pin gem version |
| Confidence | High / Medium / Weak — tune gates carefully |
| Ignore | `config/brakeman.ignore` with fingerprint + note + expiry |
| CI | Fail on new High (and agreed Medium); baseline mode optional |
| Limits | No full dataflow across all gems; re-check with manual review |

## Workflow

### 1. Confirm scope and success criteria

1. Record Rails version, Ruby version, engines/engines paths, multi-app monorepo layout.
2. Success: Brakeman pinned; CI gate defined; High issues fixed or exceptioned with owner; report artifact stored.
3. Note: only app code you can patch is in remediation scope.

### 2. Install and baseline scan

```bash
# Gemfile.dev / CI
bundle add brakeman --group development --version "~> 6.0"  # pin appropriately
bundle exec brakeman -q --no-pager
# Full checks
bundle exec brakeman -A -q
# JSON for archival
bundle exec brakeman -q -f json -o brakeman-report.json
# SARIF (version-dependent)
bundle exec brakeman -q -f sarif -o brakeman.sarif
```

1. Capture exit code policy (`--ensure-latest` optional in CI).
2. Separate engine paths if monorepo: `-p path/to/rails_app`.
3. Record Brakeman and Rails versions in the ticket.

### 3. Configure project defaults

**Example `config/brakeman.yml` ideas (adapt to version):**

```yaml
# Conceptual — verify keys for your Brakeman version
:run_all_checks: false
:min_confidence: 2
:output_files:
  - brakeman-report.html
:skip_files:
  - lib/legacy_vendor/
```

```bash
# Useful flags
bundle exec brakeman -q --only-files app/controllers
bundle exec brakeman -q -w 2          # min confidence threshold
bundle exec brakeman -q --compare old.json  # diff against baseline
```

1. Do not disable checks globally to go green — prefer fixes.
2. Skip third-party vendored trees explicitly if needed.
3. Align Ruby/Rails version detection (Brakeman may guess wrong on unusual layouts).

### 4. Triage findings

| Confidence | Typical action |
| --- | --- |
| High | Fix or urgent exception with compensating control |
| Medium | Fix in sprint or justify |
| Weak | Spot-check; often informational |

**Common Rails classes and directions:**

| Warning type | Fix direction |
| --- | --- |
| SQL injection | Arel / bound parameters; no string-interp SQL |
| XSS | `html_safe` audit; sanitize; CSP |
| Mass assignment | Strong params; avoid `params.permit!` |
| Redirect | Allowlist hosts; avoid user-controlled `redirect_to` |
| Dynamic render / constantize | Allowlist classes |
| File access | Path allowlist; no user paths to `send_file` |
| Dangerous send | Avoid user-controlled method names |

1. Reproduce with a unit/request test where feasible.
2. Prefer framework-safe APIs over silencing Brakeman.
3. For false positives: document why the sink is safe (e.g. constant allowlist).

### 5. Ignore file hygiene

```bash
# Interactive ignore (prefer generating fingerprints via Brakeman tooling)
bundle exec brakeman -I
```

**Ignore entry requirements:**

1. Fingerprint matches exact warning.
2. Human note: reason + ticket URL.
3. Expiry or review date (process); re-validate on Rails upgrades.
4. Code owner approval for security-sensitive ignores.

1. Review `brakeman.ignore` in PR like production code.
2. Ban empty notes and “false positive” without analysis.

### 6. CI gate and verify

```yaml
# GitHub Actions sketch
- name: Brakeman
  run: bundle exec brakeman -q --format json --output brakeman.json --exit-on-warn
```

```bash
# After fixes
bundle exec brakeman -q
bundle exec rspec   # or minitest — ensure behavior preserved
```

1. Optionally `--compare` against main’s JSON so only **new** findings fail PR.
2. Publish HTML/SARIF as CI artifacts (access-controlled).
3. Track trend: open High count over time.

### 7. Hand off

1. File issues per warning class with file:line and recommended fix.
2. Schedule full `-A` review quarterly or on major Rails upgrades.
3. Combine with `bundle audit` / Dependabot for gem CVEs (separate skill path).
4. Apply `code-quality-standards` on remediation PRs.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Pinning | Locked Brakeman in Gemfile.lock | Random latest on each CI | 
| Gates | Fail on new High | Ignore exit code |
| Ignores | Fingerprint + ticket + review | Mass ignore file dump |
| Fixes | Parameterized queries | `brakeman:ignore` on real SQLi |
| Scope | App + engines configured | Scanning wrong directory silently green |
| Dual checks | Brakeman + bundler-audit | SAST only, never deps |

## Output Checklist

- [ ] Rails app path and versions recorded
- [ ] Brakeman installed and version-pinned
- [ ] Baseline JSON/HTML report archived
- [ ] High/Medium triage completed
- [ ] Fixes merged or ignores justified
- [ ] CI gate active with agreed policy
- [ ] Rescan clean (or accepted residual documented)
- [ ] Tests run for behavior regressions
- [ ] `code-quality-standards` on code changes

## Rules

- Authorized codebases only.
- Prefer fixing sinks over growing ignore files.
- Re-run after Rails major upgrades — checks and FP rates change.
- Do not treat “0 Brakeman warnings” as proof of absence of vulns (authz/business logic still need testing).
- Keep this skill on Brakeman run/triage; route logic testing to business-logic skills.
