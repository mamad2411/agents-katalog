---
name: setup-visual-regression
description: Configure automated visual diffing for UI components and pages. Use when establishing pixel-level regression testing, cross-browser snapshot baselines, or CI visual gates.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, run_dev_server, execute_command]
---

# Setup Visual Regression

Use this skill to integrate Playwright or Chromatic into the CI pipeline to enforce pixel-perfect UI consistency and block styling regressions.

## Core Rules

- **Containerized Baselines Only**: Baselines must be generated and compared within the official Playwright Docker container (`mcr.microsoft.com/playwright`) matching the CI environment — comparing local macOS/Windows snapshots against Linux CI runners guarantees false failures
- **Bounded 2-Pass Self-QA**: Limit agent self-QA to a hard maximum of 2 passes post-authoring, inspecting Desktop (`>= 1280px`) and Mobile (`375px - 430px`) viewports simultaneously; edits must be triggered strictly by deterministic defects (horizontal overflow, fold clipping, broken markup, `< 44x44px` touch targets, contrast failures) to prevent infinite refinement loops
- **Negative Asset Constraints**: Strictly prohibit generating fabricated inline SVG logos ("NovaCorp") and synthetic customer testimonials with unverified metrics; mandate authentic typography, system monograms, verified Simple Icons marks, or honest structural placeholders
- **Animation Suppression**: All CSS animations, transitions, and cursor blinks must be disabled before snapshotting (`animations: 'disabled'`)
- **Dynamic Content Masking**: Mask or stub dynamic content (dates, user avatars, random IDs, ads) before capturing snapshots using `mask: [page.locator('...')]`
- **Explicit Tolerance Thresholds**: Standardize `maxDiffPixelRatio: 0.002` (0.2%) for isolated font-stabilized component snapshots in Docker Linux, and allow up to `maxDiffPixelRatio: 0.01` (1%) with `threshold: 0.2` only for full-page route diffs with masked dynamic regions — unconfigured default thresholds are too loose
- **Component Isolation**: Test UI components in isolation (Storybook + Chromatic with TurboSnap) alongside full-page Playwright visual regression tests
- **Cross-Browser Coverage**: Configure the matrix across Chromium, WebKit, and Firefox at mobile and desktop viewports
- **Hard CI Gate**: Visual regression failures must block merges unless explicitly approved by a `ui-ux-designer` or `frontend-developer`
- **Network Mocking**: Mock network responses using MSW to guarantee consistent visual fixtures — live external API snapshots are non-deterministic
- detailed verification protocols and anti-slop standards: [`../ui-ux-designer-anti-slop-standards.md`](../ui-ux-designer-anti-slop-standards.md)

## Suggested Process

### 1. Select and Install Visual Diffing Engine

Choose and install the appropriate framework based on repo architecture:
- Playwright Test (`@playwright/test`) with `toHaveScreenshot()` for full-page and integrated route diffs.
- Chromatic / Storybook Test Runner for isolated design system component snapshot suites.
- Configure snapshot storage directories and explicit tolerances (`maxDiffPixelRatio: 0.002` for isolated components, `0.01` max for masked full-page diffs).

### 2. Define Viewport and Browser Matrix

Configure responsive test parameters:
- Set up standard viewport configurations (Mobile: 375x667, Tablet: 768x1024, Desktop: 1280x800).
- Enable cross-browser execution across Chromium, WebKit, and Firefox.
- Configure color scheme variants (light mode and dark mode) where supported.

### 3. Implement Dynamic Content Masking & Mocking

Eliminate snapshot non-determinism:
- Disable CSS animations and transitions during test runs (`animations: 'disabled'`).
- Mask dynamic elements such as timestamps, user avatars, and fluctuating numeric feeds using test selectors (`mask: [page.locator('.timestamp')]`).
- Stub network API responses to serve fixed mock data.

### 4. Capture Initial Baselines in Containerized Environment

Generate canonical reference snapshots:
- Run baseline capture scripts inside the project's official Docker container or CI image to guarantee identical font rendering.
- Verify baseline image quality, cropping, and full-page layout coverage.
- Commit initial reference snapshots to the repository or artifact registry per project policy.

### 5. Integrate CI Pipeline Gate

Configure automated workflow execution:
- Add a visual regression step to CI workflows triggered on pull requests touching frontend assets.
- Configure visual diff artifact uploads on failure to simplify PR review.
- Set up failure reporting that links directly to visual comparison summaries.

### 6. Establish Baseline Update & Approval Workflow

Document snapshot maintenance procedures:
- Define the CLI command for regenerating baselines when intentional UI changes land (e.g., `npm run test:visual -- -u`).
- Enforce mandatory reviewer sign-off from designated UI/UX or frontend leads before updating baselines.

## Failure Modes

- **Baseline not captured for new component**: a new component ships without a visual baseline. Mitigation: require a Chromatic or Percy baseline at component registration; reject components without the baseline.
- **Baseline drift undetected**: a visual baseline changes without a corresponding PR. Mitigation: lock the baseline to the component version; surface drift in the diff report.
- **Driver version drift**: the visual driver (Chromatic, Percy) is updated without re-baselining. Mitigation: re-baseline every component on driver upgrades; surface the missing re-baseline in CI.
- **Threshold too loose**: a visual regression exceeds the calibrated tolerance without failing CI. Mitigation: enforce `maxDiffPixelRatio: 0.002` for isolated components and `<= 0.01` for masked full-page routes; reject unconfigured thresholds.

## Output Contracts

When this skill is invoked as part of a coordinated multi-role delivery, emit:

- **`contracts/schemas/implementation-result.json`** — Required fields: `change_summary`, `files_touched[]`, `tests_added[]`, and `validation_run` output proving the visual baseline generation succeeded.

## Checklist

- [ ] Visual testing framework (Playwright/Chromatic) installed and configured.
- [ ] Viewport matrix (mobile, tablet, desktop) and browser targets configured.
- [ ] Dynamic content masking and animation disabling implemented to prevent flakes.
- [ ] Network mocks configured for deterministic state rendering.
- [ ] Baseline snapshots generated in containerized environment.
- [ ] CI pipeline step configured as a hard quality gate blocking visual regressions.
- [ ] `implementation-result.json` emitted.
- [ ] **Official Playwright Docker container** (`mcr.microsoft.com/playwright`) for baseline generation
- [ ] **Bounded self-QA**: max 2 passes, dual viewport (Desktop + Mobile), defect-driven edits only
- [ ] **Negative asset constraints**: no fabricated SVGs, no synthetic testimonials
- [ ] **Explicit tolerance thresholds**: `maxDiffPixelRatio: 0.002` (component) / `<= 0.01` (masked full-page), `threshold: 0.2`
- [ ] **Component isolation**: Storybook + Chromatic TurboSnap + Playwright full-page
- [ ] **Cross-browser matrix**: Chromium, WebKit, Firefox at mobile/desktop
- [ ] **Hard CI gate**: visual failures block merges unless `ui-ux-designer`/`frontend-developer` approves
- [ ] **Network mocking**: MSW for deterministic visual fixtures
- [ ] **TurboSnap integration**: Chromatic only re-tests changed component stories

## Security Guardrails (OWASP ASI)

- **ASI04 Supply Chain**: visual regression drivers, baseline storage, and snapshot libraries must be schema-validated against the expected manifest; treat unknown versions as untrusted.
- **ASI05 RCE Guard**: never construct visual diff scripts or baselines from external content without strict validation.
- **ASI07 Inter-Agent Communication**: the regression report is consumed by Frontend and QA roles; emit a structured contract so each consumer can validate.
- **ASI09 Human-Agent Trust Exploitation**: do not present a visual regression as "no diff" without the actual baseline comparison; surface the residual risk.

## Related Skills

- **frontend-testing**: Complement visual diffs with functional and interaction unit/integration tests
- **accessibility-review**: Pair visual regression testing with automated axe-core accessibility gates
- **add-ui-component**: Validate new or modified UI components against visual snapshot baselines
- **design-review**: Review visual snapshot diffs against design specifications and design tokens
- **review-code**: Audit visual test coverage and snapshot approval evidence during code review
- Companion reference: `references/visual-regression-docker-and-masking-specs.md`
- Companion example: `examples/visual-regression-playwright.config.ts`

Last updated: 2026-11-08