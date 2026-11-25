---
name: kendo-ui-ci-integration
description: Use when Kendo UI build quality, test execution, bundle size, theme compilation, security scanning, and license validation must be enforced automatically in CI to gate PRs and track regressions.
---

# Kendo UI CI Integration

## Specialization

Design and implement automated CI enforcement for Kendo UI quality obligations — covering test execution (QUnit, Jest, Jasmine), SASS theme compilation validation, bundle size budget enforcement, `npm audit` CVE detection scoped to Kendo UI dependencies, Kendo UI license validation, and template XSS gate via static analysis — across commits and PRs.

This skill is specialized for CI lifecycle and automated threshold enforcement. Manual evidence-first gate review is handled by `kendo-ui-quality-gate`. Test suite design is handled by `kendo-ui-testing`.

## Trigger Conditions

- A Kendo UI project needs automated test execution in CI with deterministic result artifacts.
- SASS theme compilation failures are not caught before merge.
- Kendo UI bundle size has no enforced upper bound across commits.
- Known jQuery CVEs embedded in the Kendo UI dependency chain are not being detected.
- Kendo UI commercial license validation is not enforced in the build pipeline.
- Template XSS risks (raw `#= #` expressions) are not flagged automatically.
- A Kendo UI version upgrade needs regression evidence captured automatically per commit.

## Scope Boundaries

In scope:

- CI test execution: QUnit (via QUnit CLI or Karma), Jest (KendoReact/Angular/Vue).
- SASS theme compilation: build step that fails on any `Undefined variable` or SASS error.
- Bundle size gate: measure gzip of Kendo UI + application JS bundle; fail if over budget.
- CVE scan: `npm audit --audit-level=high` scoped to Kendo UI dependency chain.
- License validation: Kendo UI commercial license check in the build step.
- Static XSS gate: ESLint or custom script detecting `#= ` patterns on non-trusted fields.
- Artifact storage: test results (JUnit XML), coverage reports, bundle size delta per build.

Out of scope:

- Manual evidence-first quality review (use `kendo-ui-quality-gate`).
- Designing the test suite — fixture isolation, mock DataSource, event simulation (use `kendo-ui-testing`).
- Migrating Kendo UI versions (use `kendo-ui-migration`).
- Reviewing individual XSS sinks in code (use `kendo-ui-security`).

## Inputs

- CI platform (GitHub Actions assumed; note platform differences where applicable).
- Test runner in use: QUnit CLI, Karma, Jest, or Jasmine.
- Kendo UI version and distribution: OSS (kendo-ui-core) or commercial (licensed).
- Bundle size budget for Kendo UI + application JS combined (project-specific; establish baseline on first run).
- PR gate classification per check: blocking or advisory.
- Evaluation date in ISO format (`YYYY-MM-DD`).

## Required Outputs

| Output | Description |
|---|---|
| Test execution job | CI step running QUnit CLI or Jest with JUnit XML output and coverage threshold enforcement |
| SASS build job | CI step compiling SASS theme; fails on any `Undefined variable` or compilation error |
| Bundle size gate | Build + gzip measure of Kendo UI + application bundle; fail if combined size exceeds budget |
| CVE scan step | `npm audit --audit-level=high` scoped to Kendo UI dependency chain; fail on unpatched high/critical CVEs |
| License validation step | Kendo UI commercial license key present and valid; build fails if missing |
| XSS static gate | Lint rule or custom script that flags `#= ` template expressions for manual trust review |
| Artifact storage contract | JUnit XML test results, coverage HTML, bundle size delta stored per build |
| CI job specification | Full GitHub Actions job with isolation controls, caching, and noise-reduction checklist |

## GitHub Actions Job Templates

### Test Execution (Jest)

```yaml
jobs:
  kendo-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - name: Run Kendo UI tests
        run: npx jest --ci --reporters=default --reporters=jest-junit
        env:
          JEST_JUNIT_OUTPUT_DIR: ./test-results
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: test-results
          path: ./test-results/*.xml
```

### SASS Theme Build Gate

```yaml
      - name: Compile Kendo UI SASS theme
        run: npm run build:styles
        # build:styles script must:
        # 1. Run SASS compiler on the custom theme entry point
        # 2. Exit non-zero on any SASS error or undefined variable
```

### Bundle Size Gate

```yaml
      - name: Measure bundle size
        run: |
          npm run build:prod
          BUNDLE_SIZE=$(gzip -c dist/app.js | wc -c)
          echo "Bundle size (gzip): ${BUNDLE_SIZE} bytes"
          # Fail if over budget (adjust threshold per project)
          if [ "$BUNDLE_SIZE" -gt 512000 ]; then
            echo "ERROR: Bundle size ${BUNDLE_SIZE} bytes exceeds 500 KB gzip budget."
            exit 1
          fi
```

### CVE Scan

```yaml
      - name: Kendo UI dependency CVE scan
        run: npm audit --audit-level=high
        # Note: suppress known-accepted CVEs via .nsprc or audit-resolve.json
        # Never suppress without documented approval
```

### License Validation

```yaml
      - name: Validate Kendo UI license
        run: npx kendo-licensing validate
        env:
          KENDO_UI_LICENSE: ${{ secrets.KENDO_UI_LICENSE }}
```

### XSS Template Static Gate (ESLint Custom Rule Stub)

```javascript
// .eslintrc.js custom rule: warn on raw #= template expressions
// Route findings to kendo-ui-security for manual trust classification
module.exports = {
    rules: {
        "no-raw-kendo-template": {
            create(context) {
                return {
                    Literal(node) {
                        if (typeof node.value === "string" && node.value.includes("#=")) {
                            context.report({
                                node,
                                message: "Raw Kendo UI template output (#= #) detected. Verify trust level with kendo-ui-security."
                            });
                        }
                    }
                };
            }
        }
    }
};
```

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Add test execution to an existing pipeline | Tests run and publish JUnit XML artifacts |
| L2 Practical Enforcement | Core gate: tests, SASS build, CVE scan | All three checks run on every PR; artifacts stored |
| L3 Full Conformance | Bundle gate + license validation + XSS static gate | All five checks active; zero undetected violations on sample PR |
| L4 Expert Standardization | Reusable cross-project CI template | Parameterized workflow template usable by any Kendo UI project; thresholds policy-documented |
