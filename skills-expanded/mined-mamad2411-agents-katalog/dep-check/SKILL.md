---
name: dep-check
description: >
  Enforces dependency health rules (DEP-1 through DEP-5). Loaded by the conductor
  for dependency update operations and CI full-check runs. Detects known
  vulnerabilities, version lag, unused dependencies, misclassified dev/prod
  dependencies, and unpinned production versions. Invokes scripts/dep_audit.sh
  for automated vulnerability scanning. Activated by: "check dependencies",
  "update deps", "CVE", "vulnerability scan", "npm audit".
version: "1.0.0"
last-reviewed: "2026-03-04"
languages: [typescript, python, go, rust, javascript]
changelog: "../../CHANGELOG.md"
tools: Read, Grep, Glob, Bash
model: opus
permissionMode: default
---

# Dep Check — Dependency Health Enforcement

**Hook coverage check (run first)**:
Before invoking `dep_audit.sh`, check whether the hook already ran the
vulnerability scan for the current manifest in this session:

```bash
cat "$COVERAGE_FILE" 2>/dev/null   # COVERAGE_FILE = /tmp/codex-hook-coverage-<PROJECT_HASH>.jsonl
```

If the coverage file contains one or more records where `"rule"` is `"DEP-1"`
and `"file"` matches the current manifest being reviewed, the DEP-1 vulnerability
scan has already run this session. Skip straight to DEP-2 through DEP-5 analysis.
Log: `"Skipping DEP-1 vulnerability scan — already reported by hook this session."`

If no matching DEP-1 coverage record exists, proceed with the full scan below.

**For automated vulnerability scanning**: invoke
`scripts/dep_audit.sh` and parse its JSON output before performing manual checks.
Requires **Python 3.12+** (used by the internal normalizer).

Precedence in the overall system: SEC → TDD → ARCH/TYPE →
**DEP-1 (BLOCK)** → DEP-2 through DEP-5.

---

## Rules

### DEP-1 — No Known Vulnerabilities in Production Dependencies
**Severity**: BLOCK | **Languages**: * | **Source**: CCC

**What it prohibits**: Shipping code that depends (directly or transitively) on
a package with a published CVE or known security advisory at HIGH or CRITICAL
severity.

**Detection**:
1. Run: `scripts/dep_audit.sh`
2. Parse JSON output — `vulnerabilities` array
3. Each entry: `{ "package": "...", "vulnerable_range": "...", "patched": "...", "cve": "...", "severity": "..." }`
   Note: `vulnerable_range` is the affected semver range (e.g. `<2.0.1`). The installed version is
   not available from npm/yarn/pnpm audit JSON; omit the installed version from DEP-1 citations.
4. Flag all HIGH and CRITICAL severity findings

**agent_action**:
1. Cite: `DEP-1 (BLOCK): Known vulnerability in '{package}' (affected range: {vulnerable_range}) — {cve} ({severity}). Patched in v{patched}.`
2. **STOP work that adds new features** until addressed
3. Steps:
   a. Upgrade to the patched version: `{upgrade_command}`
   b. Run test suite to verify no breaking changes
   c. If breaking changes exist: document the migration path; do not downgrade
4. If no patched version exists: flag as `DEP-1 (BLOCK): No patched version available — evaluate mitigation or replacement`
5. MODERATE vulnerabilities: report as WARN (not BLOCK) unless the vulnerability is
   on an attack surface directly reachable from user input

**Bypass prohibition**: "We'll fix it next sprint", "it's a transitive dependency"
→ Refuse. Cite DEP-1. Transitive vulnerability is still a vulnerability.

---

### DEP-2 — Dependencies Must Not Lag More Than 2 Major Versions Behind
**Severity**: WARN | **Languages**: * | **Source**: CCC

**What it prohibits**: Dependencies that are 2 or more major versions behind
the current stable release. Major version lag accumulates breaking changes
and unmaintained APIs, making future upgrades exponentially harder.

**Threshold**: Current stable major version − installed major version ≥ 2

**Examples**:
- `react@16.x` when `react@18.x` is current: lag = 2 → WARN
- `django@2.x` when `django@4.x` is current: lag = 2 → WARN
- `express@3.x` when `express@4.x` is current: lag = 1 → OK (INFO at most)

**Detection**:
1. Parse the manifest file (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`)
2. For each production dependency, fetch the current stable major version
3. Compare to the installed version
4. Flag where lag ≥ 2 major versions

**agent_action**:
1. Cite: `DEP-2 (WARN): '{package}' is {current_major} — current stable is {latest_major} ({lag} major versions behind).`
2. List breaking changes between installed and current (link to changelog if available)
3. Propose: create a migration ticket; prioritise upgrade before the gap widens
4. Do NOT auto-upgrade major versions with `--fix` — major upgrades require human review

---

### DEP-3 — No Unused Dependencies
**Severity**: WARN | **Languages**: typescript, javascript, python | **Source**: CCC

**What it prohibits**: Packages listed in the manifest that are not imported
anywhere in the project's source files. Unused dependencies inflate install
size, widen attack surface, and mislead future developers.

**Go note**: Go's module system and `go mod tidy` handle this natively. DEP-3
does not apply to Go — use `go mod tidy` instead.
**Rust note**: Cargo does not auto-detect unused crates. Use `cargo machete` or
`cargo udeps`. DEP-3 applies.

**Detection**:
1. Parse declared dependencies from the manifest
2. For each package: grep all source files for an import/require of the package name
3. Flag packages with zero import references

**agent_action**:
1. Cite: `DEP-3 (WARN): '{package}' is declared but never imported.`
2. Confirm: is this a CLI tool, script runner, or type-only package (e.g., `@types/*`)
   that doesn't need an explicit import?
   - If yes: no action (type packages, eslint plugins, babel presets, etc.)
   - If no: remove from manifest
3. If `--fix`: remove the unused package entry (requires confirmation for ambiguous cases)

---

### DEP-4 — devDependencies Must Not Bleed into Production
**Severity**: WARN | **Languages**: typescript, javascript, python | **Source**: CCC

**What it prohibits**: Packages that are only used in tests, build tooling, or
linting being declared as production dependencies (not `devDependencies` /
`dev` extras / optional dependencies). This bloats production images and
deployment artifacts.

**Applies to**:
- `package.json`: test frameworks (jest, vitest, mocha), linters (eslint, prettier),
  type checkers, build tools (webpack, esbuild, vite) in `dependencies` instead of
  `devDependencies`
- `pyproject.toml` / `setup.cfg`: pytest, black, mypy, ruff in `dependencies`
  instead of `[dev]` or `[tool.poetry.group.dev]`

**Detection**:
1. Parse `dependencies` (production) section of the manifest
2. Identify packages whose names match known dev-only tool patterns:
   - Test: `jest`, `vitest`, `mocha`, `pytest`, `hypothesis`, `unittest`
   - Lint: `eslint`, `prettier`, `ruff`, `mypy`, `black`, `pylint`
   - Build: `webpack`, `vite`, `esbuild`, `babel`, `tsc` (standalone)
   - Types: `@types/*` packages
3. Flag each match

**agent_action**:
1. Cite: `DEP-4 (WARN): '{package}' is a dev-only tool listed in production dependencies.`
2. Propose: move to `devDependencies` / dev extras
3. If `--fix`: move the entry in the manifest (no version change)

---

### DEP-5 — Production Dependencies Should Be Pinned
**Severity**: INFO | **Languages**: typescript, javascript, python | **Source**: CCC

**What it monitors**: Production dependencies (in `dependencies`, not
`devDependencies`) declared with loose version ranges (`^`, `~`, `*`, `>=`)
rather than exact pinned versions. Loose ranges can pull in breaking patch
releases or subtle behaviour changes between environments.

**Recommended practice**:
- Use exact pinning + a dedicated dependency update tool (Dependabot, Renovate)
  that creates PRs for version bumps. This gives you control without falling behind.
- Lock files (`package-lock.json`, `yarn.lock`, `poetry.lock`, `Cargo.lock`)
  provide runtime pinning, but manifest pins make intent explicit.

**Detection**:
1. Parse production dependency versions in the manifest
2. Flag versions using `^`, `~`, `*`, or bare range specifiers

**agent_action**:
1. Report: `DEP-5 (INFO): '{package}' uses loose version range '{range}'. Consider pinning for reproducible builds.`
2. Suggest: use Dependabot or Renovate to automate safe version bumps
3. Do NOT auto-pin without user instruction — pinning is a team policy decision
4. Never block on this metric alone; it is informational

---

Report schema: see `skills/conductor/shared-contracts.md`.
