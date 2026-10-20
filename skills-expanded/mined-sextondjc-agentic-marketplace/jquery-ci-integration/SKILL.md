---
name: jquery-ci-integration
description: Use when jQuery build, test, deprecation, security, and bundle workflows must be automated in CI/CD with deterministic toolchains, reproducible outputs, and promotion-grade evidence.
---

# jQuery CI Integration

## Specialization

Design and implement automated CI enforcement for jQuery quality obligations — covering QUnit/Jest test execution, jQuery Migrate deprecation detection, `eslint-plugin-jquery` API correctness gates, `npm audit` CVE detection scoped to jQuery dependencies, and bundle size budget enforcement across commits and PRs.

This skill is specialized for CI lifecycle and automated threshold enforcement for jQuery. Manual evidence-first gate review of a release candidate is handled by `jquery-quality-gate`. Test suite design and local execution patterns are handled by `jquery-testing`.

## Trigger Conditions

- A jQuery project needs automated test execution (QUnit or Jest) in CI with deterministic result artifacts.
- jQuery Migrate deprecation warnings are not being caught before merge.
- Deprecated jQuery API calls are escaping review (`.live()`, `.bind()`, `.size()`, etc.) without an automated check.
- Known jQuery CVEs (CVE-2019-11358, CVE-2020-11022/11023) are not being detected in the dependency pipeline.
- jQuery bundle size (core + plugins) has no enforced upper bound across commits.
- A new jQuery project needs a CI quality baseline from day one.
- A jQuery version upgrade needs regression evidence captured automatically per commit.

## When Not to Use

- Manual evidence-first quality review before promotion (use `jquery-quality-gate`).
- Designing the test suite itself — fixture isolation, event simulation, AJAX mocking (use `jquery-testing`).
- Migrating from jQuery v1/v2 to v3 (use `jquery-migration`).
- Reviewing individual XSS sinks or CSRF patterns in code (use `jquery-security`).
- Bundle optimization and DOM batching during implementation (use `jquery-performance`).

## Inputs

- CI platform (GitHub Actions assumed; note platform differences where applicable).
- Test runner in use: QUnit (browser or Node via `qunit` CLI) or Jest + jsdom.
- jQuery version in use and whether jQuery Migrate is installed.
- Bundle size budget for jQuery core + plugins combined (default: ≤ 90 KB gzip).
- PR gate classification per check: blocking or advisory.
- Evaluation date in ISO format (`YYYY-MM-DD`).

## Required Outputs

| Output | Description |
|---|---|
| Test execution job | CI step running QUnit (via `qunit` CLI) or Jest with coverage threshold enforcement |
| Migrate deprecation gate | CI step loading jQuery Migrate in headless mode and failing if warnings are emitted |
| ESLint API gate | `eslint-plugin-jquery` configured and run on every PR; fail on deprecated API calls |
| CVE scan step | `npm audit --audit-level=high` scoped to jQuery dependency chain; fail on unpatched high/critical CVEs |
| Bundle size gate | Build + measure gzip of jQuery core + plugin bundle; fail if combined size exceeds budget |
| Artifact storage contract | Test results (JUnit XML), coverage reports, and bundle size delta stored per build for longitudinal comparison |
| CI job specification | Full GitHub Actions job with isolation controls, caching, and noise-reduction checklist |

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Add one automated check to an existing pipeline | Test execution or CVE scan runs and fails correctly on violation |
| L2 Practical Enforcement | Core automated gate: tests, deprecated API, and CVE checks | All three core checks run on every PR; results stored as artifacts |
| L3 Full Conformance | Bundle gate and Migrate deprecation detection integrated | All five checks active; zero undetected violations on sample run |
| L4 Expert Standardization | Reusable cross-project CI template | Parameterized workflow template usable by any project; threshold policy documented |

## CI Check Catalog

### Core Checks (run on every PR)

| Check | Tool | Gate Classification | Failure Impact |
|---|---|---|---|
| Test suite execution | `qunit` CLI or `jest` | Blocking | PR blocked if any test fails |
| Code coverage threshold | Jest `--coverage` or Istanbul | Blocking (configurable) | Fail if branch/line coverage drops below declared threshold |
| Deprecated jQuery API | `eslint-plugin-jquery` | Blocking | Fail on deprecated calls (`.live()`, `.bind()`, `.size()`, `.success()`, etc.) |
| CVE detection | `npm audit --audit-level=high` | Blocking | Fail on high or critical severity CVEs in jQuery or plugin dependencies |

### Extended Checks (run on PRs targeting main/staging)

| Check | Tool | Gate Classification | Failure Impact |
|---|---|---|---|
| jQuery Migrate deprecation | `jquery-migrate` in headless Node | Blocking | Fail if any Migrate warnings are emitted against the production codebase |
| Bundle size gate | `gzip` on concatenated jQuery build output | Blocking (configurable) | Fail if combined jQuery + plugin gzip exceeds budget |
| Bundle size delta | Compare vs. base branch | Advisory | Warn on increases > 5 KB gzip without justification |
| Outdated jQuery version | `npm outdated jquery` or Renovate | Advisory | Warn when jQuery is more than one minor version behind current stable |

## GitHub Actions Reference Patterns

### Test Execution (Jest)

```yaml
- name: Run jQuery test suite
  run: npx jest --coverage --ci --reporters=default --reporters=jest-junit
  env:
    JEST_JUNIT_OUTPUT_DIR: ./test-results
    JEST_JUNIT_OUTPUT_NAME: jest-results.xml

- name: Upload test results
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: test-results-${{ github.run_id }}
    path: ./test-results/jest-results.xml
    retention-days: 30
```

### Test Execution (QUnit CLI)

```yaml
- name: Run QUnit test suite
  run: |
    npx qunit tests/ --reporter junit 2>&1 | tee qunit-results.xml
    # Non-zero exit code propagates test failures automatically
```

### ESLint jQuery API Gate

```yaml
- name: Lint for deprecated jQuery API usage
  run: npx eslint . --ext .js --rule '{}' -c .eslintrc.jquery.json

# .eslintrc.jquery.json
# {
#   "plugins": ["jquery"],
#   "rules": {
#     "jquery/no-ajax": "off",
#     "jquery/no-bind": "error",
#     "jquery/no-live": "error",
#     "jquery/no-die": "error",
#     "jquery/no-size": "error",
#     "jquery/no-success": "error",
#     "jquery/no-error-shorthand": "error",
#     "jquery/no-sub": "error",
#     "jquery/no-deferred": "warn",
#     "jquery/no-global-eval": "error",
#     "jquery/no-selector-prop": "error"
#   }
# }
```

**Rule severity guidance:**
- `error` (blocking): APIs removed in jQuery 3 or with known XSS risk
- `warn` (advisory): APIs deprecated but not yet removed (e.g., `$.Deferred()` if targeting native Promise migration)

### CVE Scan

```yaml
- name: Audit jQuery dependencies for CVEs
  run: |
    npm audit --audit-level=high --json | tee npm-audit.json
    # Exit code 1 if high/critical vulnerabilities exist
    
- name: Upload audit results
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: npm-audit-${{ github.run_id }}
    path: npm-audit.json
    retention-days: 30
```

**Known CVE minimum version requirements** (enforce via `npm audit` or explicit version pin):
- CVE-2019-11358 (prototype pollution): jQuery ≥ 3.4.0
- CVE-2020-11022 (XSS via `<script>` tags in `.html()`): jQuery ≥ 3.5.0
- CVE-2020-11023 (XSS via `<option>` in `.html()`): jQuery ≥ 3.5.0

If the project cannot upgrade, document the accepted risk as a named suppression in `npm-audit-exceptions.json` with a named approver and expiry date.

### jQuery Migrate Deprecation Gate

```yaml
- name: Run jQuery Migrate deprecation check
  run: |
    node -e "
      const jQuery = require('jquery');
      require('jquery-migrate');
      jQuery.migrateWarnings = [];
      // Import and run your JS entry points here
      require('./src/app.js');
      if (jQuery.migrateWarnings.length > 0) {
        console.error('jQuery Migrate warnings detected:');
        jQuery.migrateWarnings.forEach(w => console.error(' -', w));
        process.exit(1);
      }
      console.log('No jQuery Migrate warnings.');
    "
```

This requires your application JS to be runnable in Node (i.e., no direct `document` access at import time). For browser-only code, substitute a Playwright or jsdom wrapper.

### Bundle Size Gate

```yaml
- name: Measure jQuery bundle size
  run: |
    # Adjust the glob to match your concatenated/built jQuery output
    BUNDLE_SIZE=$(cat dist/vendor/jquery.bundle.js | gzip -c | wc -c)
    echo "jQuery bundle gzip size: ${BUNDLE_SIZE} bytes"
    BUDGET="${{ vars.JQUERY_BUNDLE_BUDGET_BYTES || 92160 }}"  # default: 90 KB
    if [ "$BUNDLE_SIZE" -gt "$BUDGET" ]; then
      echo "::error::jQuery bundle exceeds budget (${BUNDLE_SIZE} > ${BUDGET} bytes)"
      exit 1
    fi
    echo "::notice::jQuery bundle within budget (${BUNDLE_SIZE} / ${BUDGET} bytes)"
```

## Artifact Storage Contract

| Artifact | Format | Retention | Purpose |
|---|---|---|---|
| Test results | JUnit XML | 30 days | Test failure triage and CI dashboard integration |
| Coverage report | LCOV / HTML | 30 days | Coverage trend visibility |
| npm audit log | JSON | 30 days | CVE traceability for compliance evidence |
| Bundle size log | Plain text with timestamp | 90 days | Longitudinal size regression detection |
| Migrate warnings log | Plain text | 30 days | Deprecation triage before version upgrade |

Artifact names must include `${{ github.run_id }}` to prevent collision across concurrent runs.

## Noise Reduction Checklist

- Cache `node_modules` keyed on `package-lock.json` hash to prevent flaky installs.
- Pin the `qunit` or `jest` version in `devDependencies` — do not use `@latest` in CI.
- Use `--ci` flag with Jest to prevent interactive prompts and enforce reproducible snapshot behavior.
- Separate the Migrate check into its own job so a single Migrate warning does not mask test failures.
- Use `if: always()` on artifact upload steps so evidence is preserved even when tests fail.
- Scope `npm audit` to `--audit-level=high` and document any accepted lower-severity exceptions explicitly.

## Done Criteria

- All declared checks execute and produce deterministic pass/fail output on every PR.
- Artifacts (test results, coverage, audit log, bundle size) are stored and retained per the contract.
- At least one blocking check covers tests, deprecated API, and CVE detection.
- The Migrate deprecation gate runs on PRs targeting main or staging.
- Bundle size gate has an explicit budget value stored as a CI variable (not hardcoded).
- Noise-reduction checklist is satisfied: dependency caching, pinned versions, `--ci` flag.
- Threshold policy (budgets, coverage floors) is documented as named CI variables.

## References

- [ESLint Plugin jQuery](https://github.com/wikimedia/eslint-plugin-jquery)
- [jQuery Migrate Plugin](https://github.com/jquery/jquery-migrate)
- [QUnit CLI](https://qunitjs.com/cli/)
- [Jest Configuration](https://jestjs.io/docs/configuration)
- [npm audit](https://docs.npmjs.com/cli/v10/commands/npm-audit)
- [jQuery CVE-2019-11358](https://nvd.nist.gov/vuln/detail/CVE-2019-11358)
- [jQuery CVE-2020-11022](https://nvd.nist.gov/vuln/detail/CVE-2020-11022)
- [jQuery CVE-2020-11023](https://nvd.nist.gov/vuln/detail/CVE-2020-11023)
- [GitHub Actions: Upload Artifact](https://github.com/actions/upload-artifact)
- Companion skills: `jquery-testing`, `jquery-security`, `jquery-migration`, `jquery-quality-gate`, `jquery-performance`
