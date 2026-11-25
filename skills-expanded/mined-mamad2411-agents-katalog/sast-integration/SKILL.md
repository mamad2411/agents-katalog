---
name: sast-integration
description: >
  Guides adding, tuning, and triaging Static Application Security Testing
  (SAST) in a codebase or CI/CD pipeline using tools such as Semgrep,
  CodeQL, SonarQube, or Bandit/gosec/ESLint-security-plugin per language.
  Use when the user asks to "add SAST scanning to a pipeline", "scan this
  repo for insecure code patterns", "set up static analysis security
  gates", "reduce SAST false positives", or "block merges on high-severity
  static findings". Not a substitute for DAST (runtime behavior) or SCA
  (third-party dependency vulnerabilities) — those are separate skills.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: devsecops
  maturity: stable
---

# SAST Integration

## Purpose

Static Application Security Testing (SAST) analyzes source code, bytecode,
or binaries without executing them, looking for insecure coding patterns
(SQL injection, command injection, hardcoded secrets, unsafe deserialization,
path traversal, weak crypto, missing input validation, etc.). Integrating
SAST into CI/CD shifts security feedback left — a developer sees a finding
in a pull request diff within minutes instead of a pentester or auditor
finding it months later in production. Done well, SAST becomes a fast,
automated first-pass filter; done badly (noisy rules, no triage workflow,
scanning the whole repo on every commit) it becomes an ignored gate that
teams route around. This skill covers choosing a SAST tool, wiring it into
CI/CD with sane defaults, tuning rules to keep signal-to-noise usable, and
building a triage/suppression workflow that survives contact with a real
codebase.

## When to use

- The user asks to "add SAST scanning to a pipeline" or "set up static
  analysis security gates" for a new or existing repo.
- A repo has no automated security scanning and the user wants a first
  pass at catching insecure code patterns before code review.
- An existing SAST tool is producing too many false positives and the
  user wants to tune rules, suppress noise, or introduce baseline/diff
  scanning.
- The user needs to explain or justify a SAST finding (e.g. "why did
  Semgrep flag this line?") or wants help remediating one.
- The user wants to enforce a security gate that blocks merges/deploys on
  new high/critical findings while not blocking on pre-existing debt.
- The user is comparing SAST tools (Semgrep vs. CodeQL vs. SonarQube vs.
  a language-native linter-with-security-rules) for a specific stack.

## Prerequisites & environment

- A CI/CD system capable of running a container or CLI step (GitHub
  Actions, GitLab CI, Jenkins, Azure Pipelines, CircleCI — examples below
  use GitHub Actions and GitLab CI).
- Tool choice depends on stack and licensing constraints:
  - **Semgrep** (OSS core + optional Semgrep AppSec Platform/paid rules) —
    fast, multi-language, easy to run locally and in CI, good for custom
    rules. CLI: `semgrep --config auto` or pinned rulesets. Version
    `semgrep >= 1.45` for stable `--baseline-commit` diff-aware scanning.
  - **CodeQL** — GitHub's engine, strongest for deep dataflow/taint
    analysis on compiled and interpreted languages; requires a build step
    for compiled languages (Java, C/C++, C#, Go) or "autobuild"; free for
    public repos, requires GitHub Advanced Security license for private
    repos on GitHub Enterprise.
  - **SonarQube/SonarCloud** — broad multi-language coverage plus code
    quality metrics; self-hosted SonarQube needs a running server and a
    scanner CLI or Maven/Gradle/`.NET` plugin.
  - Language-native security linters (Bandit for Python, gosec for Go,
    `eslint-plugin-security`/`eslint-plugin-no-unsanitized` for
    JS/TS, `brakeman` for Rails) are lighter-weight and worth running in
    addition to a general-purpose tool for language-specific idioms.
- Repository write access (or a bot/service account) to comment on pull
  requests and to add required-status-check configuration.
- A baseline decision: will the gate apply to the whole codebase (likely
  drowning teams in pre-existing findings) or only to the diff/new code
  (recommended starting point)?

## Step-by-step guidance

1. **Pick the tool(s)** based on language mix and license constraints. For
   a typical polyglot service, a good default is Semgrep (fast, cheap,
   easy custom rules) plus one language-native linter for the primary
   language. Add CodeQL if the org already has GitHub Advanced Security
   or needs deep taint-tracking for compiled languages.

2. **Run locally first** to see real signal before wiring into CI:
   ```bash
   # Semgrep, using the community "auto" ruleset plus OWASP Top 10 pack
   semgrep --config auto --config p/owasp-top-ten --error --json -o semgrep-results.json .
   ```

3. **Add a CI step scoped to the pull request diff**, not the whole repo,
   for day-to-day gating (full-repo baseline scans run separately, e.g.
   nightly). Example, GitHub Actions:
   ```yaml
   name: sast
   on:
     pull_request:
   jobs:
     semgrep:
       runs-on: ubuntu-latest
       container:
         image: semgrep/semgrep:1.78.0
       steps:
         - uses: actions/checkout@v4
           with:
             fetch-depth: 0
         - name: Run Semgrep (diff-aware)
           run: |
             semgrep ci \
               --config p/owasp-top-ten \
               --config p/secrets \
               --baseline-commit "${{ github.event.pull_request.base.sha }}"
           env:
             SEMGREP_APP_TOKEN: ${{ secrets.SEMGREP_APP_TOKEN }}
   ```
   Equivalent GitLab CI (SAST is built in as a template):
   ```yaml
   include:
     - template: Security/SAST.gitlab-ci.yml
   variables:
     SAST_EXCLUDED_PATHS: "vendor, node_modules, test/fixtures"
   ```

4. **Set severity thresholds for the merge gate**, not "zero findings."
   Start by failing the build only on `ERROR`/`critical`/`high` severity
   findings in *new* code; route `WARNING`/`medium` and below to a
   dashboard or PR comment (informational, non-blocking) until the team
   has bandwidth to raise the bar.

5. **Add an inline suppression mechanism with mandatory justification**,
   not silent ignores. Semgrep example:
   ```python
   # nosemgrep: python.lang.security.audit.subprocess-shell-true
   # Justification: `cmd` is built from a fixed allowlist, see ALLOWED_CMDS above.
   subprocess.run(cmd, shell=True)
   ```
   Require a linked ticket or comment for every suppression, and review
   suppressions periodically (e.g. quarterly) rather than letting them
   accumulate silently.

6. **Wire results into the PR** as inline review comments (most tools
   support SARIF upload to GitHub code scanning, or native PR comments)
   so developers see findings where they're already looking, not in a
   separate dashboard they have to remember to check.

7. **Track a baseline and trend**, not just pass/fail. Export SARIF or
   JSON to a central store (or the GitHub Security tab / SonarQube
   dashboard) so the team can see whether the finding count is trending
   down over time, and periodically schedule a full-repo scan to catch
   drift.

## Best practices

- Scope blocking gates to **new/changed code** (diff-aware or
  baseline-commit scanning); apply a separate, non-blocking full scan on
  a schedule to slowly work down pre-existing debt. A gate that blocks on
  the entire existing codebase on day one gets disabled within a week.
- Curate rulesets instead of running every default rule. A default "kitchen
  sink" ruleset can produce hundreds of low-value findings per repo;
  start with a focused set (OWASP Top 10, secrets, your language's
  official pack) and add rules deliberately.
- Write 2-3 custom rules for your org's actual footguns (e.g. a homegrown
  auth helper that's easy to misuse) — generic rulesets rarely catch
  organization-specific anti-patterns, and custom rules tend to have the
  best signal-to-noise ratio of all.
- Treat SAST as one layer, not the whole program: it cannot see runtime
  configuration issues, business-logic flaws, or vulnerable third-party
  code — pair it with [dast-integration](../dast-integration/SKILL.md)
  for runtime behavior and
  [software-composition-analysis-sca](../software-composition-analysis-sca/SKILL.md)
  for dependency vulnerabilities.
- Version-pin the scanner image/action (e.g. `semgrep/semgrep:1.78.0`, not
  `:latest`) so rule updates don't silently change what fails a build
  overnight.
- Give developers a fast local pre-commit or pre-push hook running the
  same ruleset as CI, so failures surface before a PR round-trip, not
  after.
- Track false-positive rate as a first-class metric; a SAST program that
  developers distrust gets its findings dismissed reflexively, including
  the real ones.

## Common pitfalls

- **Symptom:** The SAST gate is enabled, but every PR has 40+ findings and
  developers click "merge anyway" or disable the check.
  **Fix:** Switch to diff/baseline scanning so only new findings block,
  triage the existing backlog separately with its own remediation SLA,
  and cut the ruleset down to a curated, high-confidence set.

- **Symptom:** CodeQL job fails with "no source code was seen during the
  build" for a compiled language (Java, Go, C++).
  **Fix:** CodeQL needs to observe an actual compilation to build its
  database for compiled languages — replace `autobuild` with an explicit
  build step (`mvn compile`, `go build ./...`) matching your real build,
  and make sure the CodeQL init step's `languages:` list matches what you
  actually build.

- **Symptom:** A hardcoded-secret rule keeps firing on test fixtures and
  example config files, and developers start blanket-suppressing the
  whole rule.
  **Fix:** Exclude fixture/test-data paths explicitly in tool config
  (`SAST_EXCLUDED_PATHS`, `.semgrepignore`, `paths.exclude` in Sonar)
  rather than suppressing the rule everywhere — fixtures are exactly
  where accidentally-real secrets tend to leak.

- **Symptom:** The pipeline takes 25 minutes longer after adding SAST, and
  teams complain about CI latency.
  **Fix:** Scope the scan to changed files/diff instead of full-repo,
  cache tool dependencies/rule bundles between runs, and move the
  full-repo deep scan to a nightly/weekly schedule instead of every PR.

- **Symptom:** A finding is suppressed with `// nosemgrep` and no comment;
  six months later nobody remembers why, and a real vulnerability with
  the same pattern ships unnoticed.
  **Fix:** Require a justification comment and a linked ticket for every
  suppression as a matter of code review policy, and schedule periodic
  suppression audits.

## Worked example

A Python/Flask service adds Semgrep as a blocking PR gate, with a
one-time full-repo baseline scan run separately.

`.github/workflows/sast.yml`:
```yaml
name: sast
on:
  pull_request:
    branches: [main]

jobs:
  semgrep:
    runs-on: ubuntu-latest
    container:
      image: semgrep/semgrep:1.78.0
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Semgrep diff-aware scan
        run: |
          semgrep ci \
            --config p/owasp-top-ten \
            --config p/python \
            --config p/secrets \
            --baseline-commit "${{ github.event.pull_request.base.sha }}" \
            --sarif --output semgrep.sarif
        continue-on-error: true

      - name: Upload SARIF to code scanning
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: semgrep.sarif

      - name: Fail on new high/critical findings
        run: |
          python3 - <<'EOF'
          import json, sys
          with open("semgrep.sarif") as f:
              sarif = json.load(f)
          blocking = [
              r for run in sarif["runs"] for r in run["results"]
              if r.get("level") == "error"
          ]
          if blocking:
              print(f"{len(blocking)} blocking finding(s) in new code")
              sys.exit(1)
          EOF
   ```

Sample finding surfaced on a PR (SARIF excerpt, trimmed):
```json
{
  "ruleId": "python.flask.security.injection.sql-injection.flask-sqli",
  "level": "error",
  "message": { "text": "User-controlled data flows into a raw SQL query." },
  "locations": [{ "physicalLocation": { "artifactLocation": { "uri": "app/views/search.py" }, "region": { "startLine": 42 } } }]
}
```
Remediation: parameterize the query (`cursor.execute("... WHERE id = %s", (user_id,))`)
instead of string-formatting user input into SQL, then re-run
`semgrep ci --baseline-commit <base-sha>` locally to confirm the finding
clears before pushing.

## Cross-references

- [dast-integration](../dast-integration/SKILL.md) — runtime testing that
  catches issues SAST cannot see (auth/session flaws, server
  misconfiguration, issues only observable when the app is running).
- [software-composition-analysis-sca](../software-composition-analysis-sca/SKILL.md) —
  covers vulnerable third-party dependencies, which SAST rules generally
  do not analyze.
- [secure-cicd-gates](../secure-cicd-gates/SKILL.md) — how to combine SAST
  with other scan types into a coherent, non-redundant set of pipeline
  gates.
