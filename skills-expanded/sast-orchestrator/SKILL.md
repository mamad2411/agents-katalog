---
name: sast-orchestrator
description: SAST orchestration for Semgrep, CodeQL and SonarQube. Covers tool selection, ruleset curation, PR-comment integration, noise reduction with baselines, and language-specific linters (bandit, gosec, brakeman, eslint-security) when they add coverage.
---

# SAST Orchestrator

## When to use

This skill configures static-analysis tooling and keeps the noise low enough that findings stay actionable. It's the engine behind phase 3 of `security-review` and the SAST gate of `/security-gate`.

Activates on:

- A request like "set up Semgrep on this repo", "which CodeQL query suite should we use", "our SonarQube is full of false positives", "integrate SAST in CI".
- Existing SAST output that needs to be triaged before it goes to developers.
- PR-comment configuration where you have to decide between inline annotations and silent failure.
- A new repo where SAST is missing, or an existing one where the rule sets have grown without hygiene.
- A handoff from `security-review` phase 3 or the `security-gate` SAST gate.

### When NOT to use (handoff)

- Secrets in code → `secrets-scanner`. SAST tools have secret rules but they are not the sharpest layer.
- Vulnerabilities in dependencies → `cve-triage` and `supply-chain`. SCA is a separate discipline.
- Runtime / dynamic analysis → `dast-workflow`. SAST doesn't see live auth-flow or response headers.
- IaC misconfig → `iac-security`. Even though tools like Semgrep have IaC rules, the specialist coverage in `iac-security` is sharper.
- Framework-deep rules (Django, Rails, Spring, Next.js) → `django-security`, `rails-security`, `spring-security`, `nextjs-security` respectively. Those skills can call this one for CI integration of their framework-specific rule sets.
- Pure code-pattern questions without a tool context → `secure-coding`.

## Approach

Six phases. Phases 2 and 3 are the heart (which tools, which rules). The rest is workflow around them.

### 1. Scope and inventory

Know what you have before adding new tools.

- **Languages and frameworks in the repo.** `tokei` or `cloc` for the language breakdown, `package.json`/`pyproject.toml`/`go.mod`/`pom.xml` for frameworks. This determines which tools make sense.
- **Existing SAST setup.** What's already running (local linters, CI jobs, GitHub Advanced Security)? Which rule sets are active? What's the average hit rate per PR?
- **Goal.** Blocker-catch (pre-merge gate), compliance evidence (SOC2/ISO audit), quality trend (tech-debt dashboard), developer feedback (inline tips). The goal drives tool choice and how aggressively you fail on findings.
- **Deadline and appetite.** A blocker-gate setup is a different thing from a first reconnaissance. Tune aggressiveness accordingly.

Outcome: an inventory of languages plus existing checks plus goal. Without that you're choosing tools blindly.

### 2. Tool choice

Minimize overlap. Three tools that overlap 80% don't catch three times as much; they produce three times as much noise.

- **Semgrep** (open-source, Apache-2, pattern-based in YAML). Default choice for breadth. Community rule sets cover OWASP classes in all common languages. CI integration via `semgrep-action` or `semgrep ci`. Semgrep Pro (commercial) adds call-graph-based checks and reachability.
- **CodeQL** (GitHub, partly open-source, query-based in QL). Deeper taint tracking and dataflow analysis. Slower than Semgrep, finer in the analysis. Free for public repos, requires GitHub Advanced Security (paid) for private. Default for deep-mode reviews and security-critical codebases.
- **SonarQube / SonarCloud** (SonarSource, commercial). Scanner plus server plus dashboard. Strong in trend tracking and code quality (not just security). Overkill if you only want security findings; good if the team also wants to track tech debt.

**Language-specific linters** (as a complement where they're sharper):

- **Bandit** (Python) — catches Python-specific foot-guns Semgrep also sees, but with tighter pre-commit integration.
- **gosec** (Go) — same idea for Go.
- **Brakeman** (Rails) — Rails-specific checks that have much deeper Rails knowledge than general-purpose tools. See `rails-security` for details.
- **eslint-plugin-security** + **eslint-plugin-security-node** (JS/TS) — inline in the standard linter, no extra CI step.
- **PMD** / **SpotBugs** with **FindSecBugs** (Java).
- **psalm** / **phpstan** + security plugins (PHP).

Selection heuristic: one breadth tool (Semgrep) always. CodeQL for deep mode and security-critical codebases. SonarQube only when quality-trend is also a goal. Language-specific tools when the breadth tool has been shown to be too shallow (e.g. Rails without Brakeman misses a lot).

### 3. Ruleset curation

Tool default rule sets are a starting point, not an end point. Curation means: turn on what's valuable, turn off what doesn't fit this codebase, and write your own rules for org-specific foot-guns.

**Semgrep** registry rule sets (via `rules:` or `config:` directive):

- `p/security-audit` — broad security set for all languages.
- `p/owasp-top-ten` — focuses on OWASP categories, maps to A0x.
- `p/ci` — subset that's not too slow for every PR.
- `p/<language>` — language-specific (e.g. `p/python`, `p/javascript`, `p/java`, `p/go`, `p/typescript`, `p/ruby`).
- `p/r2c-security-audit` — r2c-curated security set, slightly different mix from OWASP.

Write custom Semgrep rules in `.semgrep/` for org patterns (e.g. "don't use `requests.get` without a timeout", "always use our internal `log_pii()` wrapper"). Use the Semgrep playground for development.

**CodeQL** query suites:

- `security-extended` — standard set plus extra-strict queries.
- `security-and-quality` — security plus code-quality queries; larger, more noise.

Custom CodeQL queries in `.github/codeql/` when org-specific patterns are too deep for Semgrep pattern matching.

**SonarQube**: select a Quality Profile (built-in "Sonar way" or your own). Security Hotspots and Vulnerabilities are the security-relevant categories; Code Smells is quality, not security — report separately.

Per-codebase rule tuning: some rules consistently false-positive on patterns that are deliberate in this codebase (e.g. `subprocess.run` with fixed arguments in an admin tool). Document the disable, never wildcard.

### 4. CI integration and PR comments

Running tools in CI is standard. The work is in how developers see the output.

**Semgrep in GitHub Actions** (minimal):

```yaml
# .github/workflows/semgrep.yml
name: semgrep
on:
  pull_request:
    branches: [main]
jobs:
  semgrep:
    runs-on: ubuntu-latest
    container: returntocorp/semgrep
    steps:
      - uses: actions/checkout@v4
      - run: semgrep ci --config p/security-audit --config p/owasp-top-ten
```

PR comments: Semgrep App (commercial) or a third-party action like `reviewdog` can post findings as GitHub review comments on the exact line. Alternative: upload Semgrep as SARIF to GitHub code-scanning; findings then appear in the Security tab and as inline annotations.

**CodeQL in GitHub Actions**:

```yaml
# .github/workflows/codeql.yml
name: codeql
on:
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 6 * * 1'
jobs:
  analyze:
    runs-on: ubuntu-latest
    permissions:
      security-events: write
    steps:
      - uses: actions/checkout@v4
      - uses: github/codeql-action/init@v3
        with:
          languages: python, javascript
          queries: security-extended
      - uses: github/codeql-action/analyze@v3
```

CodeQL findings land automatically in the Security tab. Inline annotations on the PR via the github/codeql-action.

**SonarQube**: scanner as CI step, server-side rules, quality-gate config. PR decoration via the SonarQube app installed on GitHub/GitLab.

Blocker behaviour: make the job fail on new findings above a certain severity (e.g. semgrep's `--severity=ERROR` plus exit-code check). Don't treat findings that pre-date tool introduction as blockers; see phase 5 (baseline).

### 5. Noise reduction

Too many findings = findings get ignored. This is the craft.

- **Baseline at introduction.** The first run records all existing findings as "known"; the gate fails only on new ones. Semgrep: `--baseline-ref=main` or `semgrep-managed` baselines. CodeQL: the GitHub Advanced Security dashboard marks new vs existing. SonarQube: "new code" analysis per PR.
- **In-code suppressions** with reasons. Semgrep: `// nosemgrep: rule-id reason` (line level). CodeQL: `// lgtm[rule-id]` or `// codeql[rule-id]` plus review comment. SonarQube: `// NOSONAR reason`. Never wildcard suppressions; always rule-id and reason.
- **Rule disabling.** Rules that are structurally false-positive on this codebase: turn them off in tool config with a short rationale in the commit message. Review periodically (every quarter, or after large refactors).
- **Severity regrouping.** Some default severities don't fit this repo. E.g. a rule that's Info-level by default but Critical here because it touches the auth flow: promote it. In Semgrep via `severity` override, in CodeQL via query packs.
- **Ignore paths.** `.semgrepignore`, `paths-ignore` in CodeQL config. Generated code (`vendor/`, `node_modules/`, `migrations/`), test fixtures, and third-party copies typically belong here.
- **Exit criteria.** The gate fails when: a new High/Critical finding lands, or a new Medium in a critical path (auth/crypto/IO). Existing findings are not blocked but are visible. PR pass-rate should be at least 70%; below that, tuning isn't done.

### 6. Verification-loop

Apply `verification-loop` to the configuration before you let it loose on a team.

- Layer 1: scope (every language in the repo covered? every critical path excluded from the ignore-path list?), assumptions (the rule sets you turned on are current and exist?), gaps (secrets and deps referred to their own skills?), consistency (severities comparable across tools?).
- Layer 2: rule IDs and ruleset names are real, CWE / OWASP references verifiable, no custom rules claiming to detect a specific CVE without a PoC.

## Output

For a new setup: CI workflow files, tool configs, and a short explanation. For triage on existing output: a categorized report.

**Setup mode**:

```
SAST setup — <repo>
Languages: <list>
Goal:      <gate | compliance | quality | feedback>

Selected tools:
- Semgrep (breadth)          — rule sets: p/security-audit, p/owasp-top-ten, p/<lang>
- CodeQL (deep)              — suite: security-extended (if GHAS available)
- <optional quality tool>    — <SonarQube | disabled>
- Language-specific:           <bandit | gosec | brakeman | eslint-security>

Delivered:
- .github/workflows/semgrep.yml
- .github/workflows/codeql.yml (if CodeQL)
- .semgrep/<org>-rules.yml (custom rules, if needed)
- .semgrepignore / paths-ignore in CodeQL
- Baseline instruction: first run on main before the gate goes live
- PR-comment strategy: <inline via SARIF | separate comment via reviewdog | Security tab only>
- Exit criteria: <severity threshold, new-only logic>

Verification-loop:
  Verdict: ...
  Security verdict: ...
```

**Triage mode** (screening existing output):

```
SAST triage — <tool>, <N findings>
After triage:
  Real blockers:       n1
  Real non-blockers:   n2
  False positives:     n3  (with per-rule reason)
  Rules to disable:    <rule IDs + rationale>

Per real finding:
- Rule: <tool>/<rule-id> — CWE-<N>
- Location: <file:line>
- Severity: <blocker | high | medium | low>
- Why this is real (not a false positive)
- Fix suggestion or handoff

Forwarded to security-review: <N findings>
Ignored with documentation: <N, with reasons>
```

No raw tool dumps in the deliverable. Those belong in the CI log, not the reviewer's inbox.

## References

- Semgrep docs — [https://semgrep.dev/docs/](https://semgrep.dev/docs/). Tool docs, rule syntax, CI integration.
- Semgrep Registry — [https://semgrep.dev/r](https://semgrep.dev/r). Search interface for rule sets and individual rules.
- CodeQL docs — [https://codeql.github.com/docs/](https://codeql.github.com/docs/). Queries, query suites, dataflow analysis.
- GitHub Code Scanning — [https://docs.github.com/en/code-security/code-scanning](https://docs.github.com/en/code-security/code-scanning). How SARIF findings land in the UI.
- SonarQube Rules — [https://rules.sonarsource.com/](https://rules.sonarsource.com/). Rule inventory per language.
- OWASP Benchmark — [https://owasp.org/www-project-benchmark/](https://owasp.org/www-project-benchmark/). SAST tool comparison (note: dated, but methodologically still relevant).
- SARIF spec — [https://docs.oasis-open.org/sarif/sarif/v2.1.0/os/sarif-v2.1.0-os.html](https://docs.oasis-open.org/sarif/sarif/v2.1.0/os/sarif-v2.1.0-os.html). Interchange format for scan output; carries findings between tools.
- Bandit — [https://github.com/PyCQA/bandit](https://github.com/PyCQA/bandit). Python-specific linter.
- gosec — [https://github.com/securego/gosec](https://github.com/securego/gosec). Go-specific linter.
- Brakeman — [https://brakemanscanner.org/](https://brakemanscanner.org/). Rails-specific SAST.

## Categories

- appsec
