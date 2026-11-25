---
name: tailwind-ci-integration
description: Use when TailwindCSS bundle size, class ordering, content scanning, or Core Web Vitals thresholds must be enforced automatically in CI to gate PRs and track regressions across commits.
---

# TailwindCSS CI Integration

## Specialization

Design and review automated CI enforcement for TailwindCSS quality obligations — covering bundle size gating, Prettier class-ordering checks, content-scan regression detection, Lighthouse CI thresholds, and durable artifact storage across commits.

This skill is specialized for CI lifecycle and automated threshold enforcement. Manual evidence-first gate review of a release candidate is handled by `tailwind-quality-gate`.

## Trigger Conditions

- A project needs automated CSS bundle size enforcement on every PR.
- Prettier class-ordering violations are escaping code review and must be caught in CI.
- A content-scanning misconfiguration caused class purging regressions in a previous build.
- Lighthouse CI or Core Web Vitals thresholds need to be committed to config and enforced automatically.
- Bundle size reports are not stored across commits; longitudinal drift is not visible.
- A new Tailwind project needs a CI quality baseline from the start.

## When Not to Use

- Manual evidence-first quality review before promotion (use `tailwind-quality-gate`).
- Setup and build-pipeline wiring for the first time (use `tailwind-setup`).
- Designing component patterns or tokens (use `tailwind-component-design`).

## Inputs

- CI platform (GitHub Actions assumed; note platform differences where applicable).
- TailwindCSS version and build tool (Vite, PostCSS, Next.js, SvelteKit, etc.).
- Bundle size budget (default: ≤ 50 KB gzip for typical app).
- Core Web Vitals thresholds (default: LCP ≤ 2.5s, CLS ≤ 0.1, INP ≤ 200ms).
- PR gate classification: blocking or advisory per check.
- Artifact retention requirements.
- Evaluation date in ISO format (`YYYY-MM-DD`).

## Required Outputs

| Output | Description |
|---|---|
| Bundle size gate job | GitHub Actions workflow step: build, measure gzip output, fail if over budget |
| Prettier check job | CI step running `prettier --check` with `prettier-plugin-tailwindcss`; blocks PR on ordering violations |
| Content-scan verification step | Build step that confirms purged output contains no development-class leakage |
| Lighthouse CI config | `lighthouserc.json` or equivalent with committed thresholds for LCP, CLS, INP |
| Artifact storage contract | Bundle report naming, format, and retention policy for longitudinal comparison |
| Regression alert policy | Threshold breach routing and owner assignment |
| CI job specification | Full GitHub Actions job with isolation controls and noise-reduction checklist |

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Add one automated check to an existing pipeline | Bundle size or Prettier check runs and fails correctly on violation |
| L2 Practical Enforcement | Full automated gate covering bundle, ordering, and content scan | All three core checks run on every PR; artifacts stored per build |
| L3 Performance Gating | Lighthouse CI integrated with committed thresholds | LCP, CLS, INP checked on every PR against committed baselines |
| L4 Expert Standardization | Reusable cross-project CI template | Parameterized workflow template usable by any project; threshold policy documented |

## CI Job Architecture

### Core Checks (run on every PR)

| Check | Tool | Gate Classification | Failure Impact |
|---|---|---|---|
| Prettier class ordering | `prettier --check` + `prettier-plugin-tailwindcss` | Blocking | PR cannot merge with unordered classes |
| CSS bundle size | `gzip` measured on build output; compared to budget | Blocking (configurable) | Fail if over budget; report size delta vs. base branch |
| Content-scan completeness | Build with `NODE_ENV=production`; verify output is purged | Blocking | Fail if output exceeds 2× expected purged size |

### Extended Checks (run on PR targeting main/staging)

| Check | Tool | Gate Classification | Failure Impact |
|---|---|---|---|
| Lighthouse CI — LCP | `@lhci/cli` | Blocking | Fail if LCP > committed threshold |
| Lighthouse CI — CLS | `@lhci/cli` | Blocking | Fail if CLS > committed threshold |
| Lighthouse CI — INP | `@lhci/cli` | Advisory (promote to blocking when baseline is stable) | Warn on INP regression |
| Bundle size delta vs. base | `bundlesize` or custom script | Advisory | Report delta; flag increases > 10 KB gzip for review |

## GitHub Actions Reference Patterns

### Prettier Class-Ordering Check

```yaml
- name: Check Tailwind class ordering
  run: npx prettier --check "src/**/*.{html,jsx,tsx,vue,svelte,astro}"
```

- Requires `prettier-plugin-tailwindcss` in `devDependencies` and registered in `.prettierrc`.
- Run before build steps so failures are fast.

### CSS Bundle Size Gate

```yaml
- name: Build and measure CSS output
  run: |
    npm run build
    CSS_SIZE=$(find dist -name "*.css" | xargs gzip -c | wc -c)
    echo "CSS gzip size: ${CSS_SIZE} bytes"
    if [ "$CSS_SIZE" -gt "${{ vars.CSS_BUDGET_BYTES }}" ]; then
      echo "::error::CSS bundle exceeds budget (${CSS_SIZE} > ${{ vars.CSS_BUDGET_BYTES }} bytes)"
      exit 1
    fi
```

- Store `CSS_BUDGET_BYTES` as a repository variable (default: 51200 for 50 KB).
- Upload the CSS size as a build artifact with the commit SHA for longitudinal tracking.

### Lighthouse CI Integration

```yaml
- name: Run Lighthouse CI
  run: |
    npm install -g @lhci/cli
    lhci autorun
  env:
    LHCI_GITHUB_APP_TOKEN: ${{ secrets.LHCI_GITHUB_APP_TOKEN }}
```

`lighthouserc.json`:

```json
{
  "ci": {
    "collect": { "url": ["http://localhost:3000"] },
    "assert": {
      "assertions": {
        "largest-contentful-paint": ["error", { "maxNumericValue": 2500 }],
        "cumulative-layout-shift": ["error", { "maxNumericValue": 0.1 }],
        "total-blocking-time": ["warn", { "maxNumericValue": 300 }]
      }
    },
    "upload": { "target": "temporary-public-storage" }
  }
}
```

- Commit `lighthouserc.json` to the repository root; do not generate thresholds dynamically.
- Use `temporary-public-storage` for PR reporting or a self-hosted LHCI server for durable history.

## Artifact Storage Contract

| Artifact | Format | Naming Convention | Retention |
|---|---|---|---|
| CSS bundle size report | JSON `{ "size": <bytes>, "gzip": <bytes>, "sha": "<commit>" }` | `css-bundle-report-<sha>.json` | 90 days |
| Lighthouse CI report | LHCI JSON or HTML | `lhci-report-<sha>/` | 30 days (PR); 90 days (main) |
| Prettier check log | CI step log | Stored in CI run logs | CI platform default |

## Noise-Reduction Controls

CI benchmark and quality jobs produce unreliable results when run on shared, noisy infrastructure. Apply these controls:

- [ ] Bundle size job uses a dedicated runner or a stable hosted runner (not self-hosted with variable load).
- [ ] Lighthouse CI runs against a built, served preview (not `npm run dev`); use a deterministic port.
- [ ] Lighthouse CI runs a minimum of 3 audits per URL; median is used for assertion.
- [ ] Bundle size check uses the production build config (`NODE_ENV=production`); not the dev server output.
- [ ] CSS output path is stable across builds; glob is pinned, not dynamic.

## Regression Alert Policy

| Breach Type | Severity | Routing | SLA |
|---|---|---|---|
| Bundle size over budget | High | Frontend lead notified via PR check; merge blocked | Resolve before merge |
| Prettier ordering violation | High | Author of offending commit; merge blocked | Resolve before merge |
| LCP regression > 10% | High | Frontend lead + performance owner | Resolve before merge to main |
| CLS regression | High | Frontend lead | Resolve before merge to main |
| Bundle size delta > 10 KB gzip | Medium | PR comment with delta summary | Advisory; resolve within sprint |

## Security Configuration Checklist

- [ ] `LHCI_GITHUB_APP_TOKEN` stored as a repository secret; not hardcoded.
- [ ] CSS budget bytes stored as a repository variable, not hardcoded in workflow.
- [ ] No production credentials present in Lighthouse CI target URLs used in CI.
- [ ] Third-party Lighthouse CI upload target reviewed; use self-hosted LHCI server for sensitive projects.

## Done Criteria

- [ ] Prettier class-ordering check runs on every PR and blocks on violations.
- [ ] CSS bundle size gate runs on every PR; budget is committed to repository configuration.
- [ ] Content-scan verification confirms purged output on every production build.
- [ ] Lighthouse CI config (`lighthouserc.json`) is committed with explicit thresholds.
- [ ] Artifact storage contract is defined with naming, format, and retention policy.
- [ ] Noise-reduction controls checklist applied.
- [ ] Regression alert policy documents routing and SLA per breach type.
- [ ] Security checklist passes.

## References

- [Source Catalog](./references/source-catalog.md)
