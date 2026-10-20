---
name: sonarqube-code-quality-and-security
description: >
  Guides deep, tool-specific configuration of SonarQube/SonarCloud for
  combined code quality and security analysis — quality gate design,
  pull request decoration, technical debt ratio and maintainability
  rating, security hotspot triage, and sonar-project.properties/scanner
  CI wiring. Use when the user asks to "set up a SonarQube quality
  gate", "configure sonar-project.properties", "fix a failing quality
  gate", "review SonarQube security hotspots", "reduce technical debt
  ratio", "decorate pull requests with SonarQube findings", or "compare
  SonarQube new-code vs overall-code conditions". SonarQube-specific
  depth on quality gates and debt metrics; for the general SAST concept
  and tool-agnostic workflow see sast-integration in the devsecops
  domain.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: security-scanning-tooling
  maturity: stable
---

# SonarQube Code Quality and Security

## Purpose

SonarQube (self-hosted) and SonarCloud (its SaaS counterpart) analyze
source code for both security vulnerabilities and code-quality issues
(bugs, code smells, duplication, cyclomatic complexity) in a single
platform, and — unlike a pure SAST tool — attach a maintainability
rating and a "technical debt" time estimate to what it finds. Its
central operational mechanism is the **quality gate**: a named set of
pass/fail conditions, evaluated primarily against *new code* introduced
since a baseline, that a CI pipeline can query and fail on. Used well,
this turns "code review plus static analysis" into a single enforced bar
every PR must clear; used naively (gating on the whole codebase's
historical debt, or ignoring the new-code vs. overall-code distinction),
it becomes an unpassable or ignored gate within weeks. This skill goes
deep on SonarQube's specific quality-gate mechanics, PR decoration, and
debt-ratio/rating metrics. For the general SAST concept — tool
selection, triage workflow, suppression policy — see
[sast-integration](../../../devsecops/skills/sast-integration/SKILL.md).

## When to use

- The user asks to "set up a SonarQube/SonarCloud quality gate" or wants
  help configuring `sonar-project.properties`.
- A quality gate is failing and the user needs to understand which
  condition tripped (coverage on new code, duplicated lines, security
  rating, reliability rating) and how to fix it.
- The user wants pull requests decorated with inline SonarQube findings
  (GitHub/GitLab/Bitbucket/Azure DevOps PR comments) rather than only a
  dashboard.
- The user needs to triage **security hotspots** — code SonarQube flags
  as security-sensitive but requiring human judgment to confirm as a
  real vulnerability — as distinct from auto-confirmed vulnerabilities.
- The user wants to understand or reduce the **technical debt ratio**
  or improve a maintainability/reliability/security rating (A-E scale).
- The user is deciding whether to gate on "new code" (recommended
  default) vs. the whole codebase's historical baseline.
- The user is comparing SonarQube against another SAST tool for a given
  stack and needs SonarQube's specific strengths (broad multi-language
  coverage, built-in quality gate/debt model, native PR decoration) and
  limits (weaker deep taint-tracking than a dedicated dataflow engine
  like CodeQL for compiled languages).

## Prerequisites & environment

- A running SonarQube server (Community, Developer, or Enterprise
  Edition — Community Edition lacks PR decoration and branch analysis
  for some ecosystems, which are Developer Edition+ features) or a
  SonarCloud organization (SaaS, no server to operate, has a free tier
  for public repos).
- SonarQube `>= 10.x` / SonarCloud (continuously updated) for current
  quality-gate "new code" condition syntax; older `9.x` LTS servers use
  slightly different default gate condition names.
- A scanner matching the build ecosystem: `sonar-scanner` CLI
  (language-agnostic), `sonar-maven-plugin`/`sonar-gradle-plugin`
  (Java), or `dotnet-sonarscanner` (.NET) — the Maven/Gradle/.NET
  scanners integrate with the build's own dependency resolution and
  generally produce more accurate results than the generic CLI scanner
  for those ecosystems.
- A generated authentication token (user token or project analysis
  token) with `Execute Analysis` permission, stored in the CI secrets
  store — never inline in `sonar-project.properties`. See
  [secrets-management](../../../devsecops/skills/secrets-management/SKILL.md).
- For PR decoration: the SonarQube/SonarCloud instance needs network
  reachability to call back to the source-control platform's API
  (GitHub/GitLab/Bitbucket/Azure DevOps App or PAT configured in
  server-wide DevOps Platform Integration settings).
- A defined baseline: a "new code" definition (since a fixed date, since
  the previous version, or since a reference branch) — the single most
  consequential quality-gate design decision (see step 3).

## Step-by-step guidance

1. **Configure `sonar-project.properties`** at the repo root (or pass
   equivalents as scanner CLI args/CI env vars):
   ```properties
   sonar.projectKey=example-org_checkout-service
   sonar.organization=example-org
   sonar.sources=src
   sonar.tests=test
   sonar.exclusions=**/vendor/**,**/node_modules/**,**/*.generated.ts
   sonar.test.exclusions=**/*.spec.ts,**/*.test.ts
   sonar.coverage.exclusions=**/migrations/**,**/*.d.ts
   sonar.javascript.lcov.reportPaths=coverage/lcov.info
   sonar.python.coverage.reportPaths=coverage.xml
   ```

2. **Run the scanner in CI**, feeding in the auth token as a secret,
   not a literal value:
   ```yaml
   # GitHub Actions
   name: sonarqube
   on:
     pull_request:
     push:
       branches: [main]
   jobs:
     sonar:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
           with:
             fetch-depth: 0   # required for accurate blame/new-code detection
         - name: Run tests with coverage
           run: npm test -- --coverage
         - name: SonarQube Scan
           uses: SonarSource/sonarqube-scan-action@v4
           env:
             SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
             SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}
         - name: Quality Gate check
           uses: SonarSource/sonarqube-quality-gate-action@v1
           timeout-minutes: 5
           env:
             SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
   ```
   `fetch-depth: 0` matters: SonarQube's new-code detection relies on
   git blame history, and a shallow clone produces incomplete or
   incorrect new-code attribution.

3. **Define "new code" deliberately** — Administration → Project →
   New Code — as one of:
   - **Previous version** (good for release-train projects).
   - **Number of days** (e.g. last 30 days — good default for
     continuously-deployed services).
   - **Reference branch** (compare feature branches against `main` —
     the standard choice for trunk-based/PR-heavy workflows).
   Gating on "new code" rather than the whole codebase's historical
   baseline is what makes a quality gate adoptable on an existing
   codebase with pre-existing debt — see the first Common pitfall.

4. **Design the quality gate's conditions** around new code first;
   SonarQube's built-in "Sonar way" default gate is a reasonable
   starting point:
   ```
   Quality Gate: "checkout-service-gate"
   Conditions on New Code:
     - Coverage                    is less than   80%
     - Duplicated Lines (%)        is greater than 3%
     - Maintainability Rating      is worse than  A
     - Reliability Rating          is worse than  A
     - Security Rating             is worse than  A
     - Security Hotspots Reviewed  is less than   100%
   ```
   Add Overall Code conditions sparingly (e.g. "Security Rating on
   Overall Code is worse than C") only once the team has capacity to
   work down historical debt — an overall-code gate applied to an
   existing large codebase on day one typically fails immediately and
   permanently.

5. **Triage security hotspots as a distinct workflow from
   vulnerabilities.** SonarQube auto-confirms clear-cut vulnerabilities
   but marks security-sensitive code patterns (e.g. use of a
   cryptographic API, a regex that could be ReDoS-prone, a dynamic SQL
   builder) as "hotspots" requiring a human "Safe" / "Fixed" /
   "Acknowledged (won't fix, with reason)" review — they do not block
   the quality gate by count alone, only via the "Security Hotspots
   Reviewed %" condition, so an unreviewed backlog silently erodes that
   metric rather than failing loudly.

6. **Enable PR decoration** so findings appear as inline PR comments,
   not only on the SonarQube dashboard (Administration → DevOps
   Platform Integrations, then per-project binding to the repo):
   ```properties
   # sonar-project.properties (PR context, usually scanner-injected in CI)
   sonar.pullrequest.key=${PR_NUMBER}
   sonar.pullrequest.branch=${PR_BRANCH}
   sonar.pullrequest.base=main
   ```
   Most CI scanner actions/plugins auto-populate these from CI
   environment variables (`GITHUB_*`, `CI_MERGE_REQUEST_*`) — check the
   scanner action's docs before hand-setting them.

7. **Track the technical debt ratio and ratings as trend metrics**, not
   just gate pass/fail — the debt ratio (remediation cost of all
   issues ÷ cost to rewrite the codebase from scratch) is what drives
   the A-E Maintainability Rating, and watching it trend is a better
   long-term signal than a binary gate result on any single PR.

8. **Suppress with `// NOSONAR` or issue-level "Won't Fix"/"False
   Positive" resolution, with a mandatory comment**, mirroring the same
   discipline used for any SAST suppression:
   ```java
   String query = "SELECT * FROM users WHERE id = " + id; // NOSONAR — id is validated as int upstream in UserIdValidator, see JIRA-771
   ```

## Best practices

- Gate on **new code**, not the whole codebase's historical baseline,
  as the default and primary blocking mechanism — this is the single
  highest-leverage SonarQube configuration decision for an existing
  codebase.
- Always run with `fetch-depth: 0` (full git history) in CI — shallow
  clones break new-code blame attribution and can cause a gate to
  silently evaluate against the wrong baseline.
- Review security hotspots on a schedule (e.g. weekly), not only when
  they happen to block something — they don't fail the gate by raw
  count, so an unreviewed backlog is easy to lose track of.
- Treat SonarQube's Security Rating as one signal, not the whole
  program: its rule engine is broad but shallower on deep
  interprocedural taint-tracking for compiled languages than a
  dedicated engine like CodeQL; pair it with
  [fortify-static-analysis](../fortify-static-analysis/SKILL.md) or
  another deep-taint SAST tool for high-assurance compiled-language
  codebases, and with
  [owasp-zap-dast-configuration](../owasp-zap-dast-configuration/SKILL.md)
  for runtime-only issues neither can see.
- Version-pin the scanner action/CLI and coordinate SonarQube server
  upgrades deliberately — rule-set updates between versions can shift
  which findings are new vs. pre-existing and occasionally change
  quality-gate condition names.
- Keep exclusions (`sonar.exclusions`, `sonar.coverage.exclusions`)
  narrow and justified in a comment — broad exclusions (e.g. excluding
  an entire `src/` subtree) silently blind the gate to real code.

## Common pitfalls

- **Symptom:** A quality gate is enabled on an existing codebase and
  fails immediately for every single PR, regardless of what the PR
  changes.
  **Fix:** The gate is evaluating Overall Code conditions against
  years of pre-existing debt. Switch primary blocking conditions to
  "New Code" (step 3-4), and address overall-code debt as a separate,
  scheduled paydown effort with its own backlog, not a blocking gate.

- **Symptom:** New-code coverage/duplication numbers look wrong or
  inconsistent between local analysis and CI.
  **Fix:** Check `fetch-depth` in CI — a shallow git clone (the default
  in many CI templates) breaks SonarQube's blame-based new-code
  detection; set `fetch-depth: 0` (or `git fetch --unshallow`).

- **Symptom:** The security hotspot count keeps growing every sprint
  and nobody reviews them, even though the quality gate keeps passing.
  **Fix:** Hotspots don't block by count — only the "Security Hotspots
  Reviewed %" condition does, and only if it's in the gate. Add that
  condition explicitly to the quality gate, and assign a rotating owner
  to review the hotspot queue on a fixed cadence rather than leaving it
  ownerless.

- **Symptom:** A Java/Kotlin (or other JVM-ecosystem) project analyzed
  with the generic `sonar-scanner` CLI reports far fewer/different
  issues than expected, and coverage shows as 0%.
  **Fix:** Use the build-integrated scanner
  (`sonar-maven-plugin`/`sonar-gradle-plugin`) instead of the generic
  CLI for JVM ecosystems — it reuses the actual build's classpath and
  compiled bytecode, which the generic scanner cannot reconstruct on
  its own, and wire the coverage report path
  (`sonar.coverage.jacoco.xmlReportPaths`) explicitly.

- **Symptom:** PR decoration comments never appear on GitHub/GitLab
  pull requests even though the dashboard shows the analysis completed.
  **Fix:** DevOps Platform Integration isn't configured/bound for the
  project, or the token used lacks permission to post PR comments on
  the source-control side. Verify the server-wide integration
  (Administration → DevOps Platform Integrations) and the per-project
  binding, and confirm `sonar.pullrequest.*` properties are actually
  being populated in the CI run (check scanner logs for the PR context
  block).

## Worked example

A Python service (`payments-api`) adopts SonarCloud with a new-code
quality gate and PR decoration.

`sonar-project.properties`:
```properties
sonar.projectKey=example-org_payments-api
sonar.organization=example-org
sonar.sources=app
sonar.tests=tests
sonar.python.coverage.reportPaths=coverage.xml
sonar.exclusions=**/migrations/**,**/__pycache__/**
```

Quality gate ("payments-api-gate"), new-code conditions:
```
Coverage                    < 85%      -> FAIL
Duplicated Lines (%)        > 3%       -> FAIL
Maintainability Rating      worse than A -> FAIL
Security Rating             worse than A -> FAIL
Security Hotspots Reviewed  < 100%     -> FAIL
```

`.github/workflows/sonar.yml`:
```yaml
name: sonarqube
on:
  pull_request:
  push:
    branches: [main]
jobs:
  sonar:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Run tests with coverage
        run: |
          pip install -r requirements-dev.txt
          pytest --cov=app --cov-report=xml
      - name: SonarCloud Scan
        uses: SonarSource/sonarqube-scan-action@v4
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
      - name: Quality Gate check
        uses: SonarSource/sonarqube-quality-gate-action@v1
        timeout-minutes: 5
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

Sample failing PR decoration comment:
```
Quality Gate: FAILED

New Code:
  Security Rating: E (worse than required A)
    app/billing/charge.py:88 — Hardcoded secret used in a cryptographic
    key derivation (BLOCKER, CWE-798)
  Coverage: 71.2% (required >= 85%)
```
Remediation: replace the hardcoded key with one sourced from the secrets
manager (see
[secrets-management](../../../devsecops/skills/secrets-management/SKILL.md)),
add tests to cover `charge.py`'s new branch, push, and confirm the gate
re-evaluates to passed on the updated commit.

## Cross-references

- [sast-integration](../../../devsecops/skills/sast-integration/SKILL.md) —
  the tool-agnostic SAST concept, triage workflow, and suppression
  policy this skill goes deep on for SonarQube's quality-gate model
  specifically.
- [fortify-static-analysis](../fortify-static-analysis/SKILL.md) —
  an enterprise, deep-taint-tracking alternative worth pairing with
  SonarQube for high-assurance compiled-language codebases.
- [owasp-zap-dast-configuration](../owasp-zap-dast-configuration/SKILL.md) —
  runtime testing that catches issues SonarQube's static analysis
  cannot see.
- [secrets-management](../../../devsecops/skills/secrets-management/SKILL.md) —
  where a hardcoded-secret hotspot/finding should actually be remediated
  to (a secrets manager), not just suppressed.
