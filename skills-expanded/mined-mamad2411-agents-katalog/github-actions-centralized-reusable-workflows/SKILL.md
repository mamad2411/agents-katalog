---
name: github-actions-centralized-reusable-workflows
description: >
  Designs organization-level reusable GitHub Actions workflows
  (workflow_call) and shared composite actions hosted in a dedicated repo,
  so many repos call one standardized pipeline definition instead of
  duplicating workflow YAML. Use when the user asks to "centralize our
  GitHub Actions workflows," "create a reusable workflow with
  workflow_call," "enforce a standard CI pipeline across all repos,"
  "version a shared composite action," or "reduce duplicated workflow YAML
  across the organization."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: cicd-tooling
  maturity: stable
---

# GitHub Actions Centralized Reusable Workflows

## Purpose

When the same workflow YAML — build, test, security scan, deploy — is
copy-pasted across dozens of repos ([github-actions-single-repo-workflows](../github-actions-single-repo-workflows/SKILL.md)
covers that per-repo pattern), a policy change (a new required scan, a
registry migration) requires editing every repo individually and drifts
immediately. GitHub Actions solves this at the organization level with
**reusable workflows** (`workflow_call`), which let a caller workflow in
any repo invoke one centrally-maintained workflow definition with inputs/
secrets, and **shared composite actions** hosted in a dedicated repo for
smaller reusable step sequences. This skill covers designing, versioning,
and rolling out that centralized pattern so many repos consume one
standardized pipeline rather than diverging copies.

## When to use

- More than a handful of repos have near-identical `.github/workflows/*.yml`
  files and a change requires updating each one individually.
- Standing up an organization-wide CI/CD standard (e.g. "every service
  repo must run this exact set of security gates before deploy") that
  individual teams shouldn't be able to silently drift from.
- An existing reusable workflow needs a new input/secret, or a breaking
  change that must be versioned so callers can opt in on their own
  schedule.
- Deciding whether a step sequence belongs in a per-repo composite action
  (see
  [github-actions-single-repo-workflows](../github-actions-single-repo-workflows/SKILL.md))
  versus a centrally-hosted one consumed by many repos.
- Migrating from Jenkins shared libraries to GitHub Actions and wanting
  the equivalent centralization model — compare with
  [jenkins-centralized-shared-library](../jenkins-centralized-shared-library/SKILL.md).

## Prerequisites & environment

- A dedicated repository to host reusable workflows/composite actions
  (commonly `.github` at the org level for org-wide defaults, or a
  purpose-named repo like `actions-library`).
- Organization (or repo, for repo-scoped reuse) admin access to configure
  which repos may call reusable workflows: **Organization Settings →
  Actions → General → "Access" for reusable workflows and actions**, since
  by default a private reusable workflow is only callable from repos in
  the same organization unless explicitly opened up.
- Caller repos need `permissions:` granted appropriately, since a
  reusable workflow runs with the permissions the *caller* grants it, not
  its own hardcoded defaults.
- Secrets: either passed explicitly via `secrets: inherit` (simplest, but
  passes everything the caller has) or named individually
  (`secrets: { DEPLOY_TOKEN: ${{ secrets.DEPLOY_TOKEN }} }`, more
  auditable about exactly what the reusable workflow receives).
- Semantic version tags (or at minimum SHA pinning discipline) on the
  reusable-workflow repo so callers can pin a version rather than track
  `@main`.

## Step-by-step guidance

1. **Define the reusable workflow with `workflow_call` as its trigger**,
   declaring explicit `inputs:` and `secrets:` — this is what makes it
   callable from another repo rather than only runnable in its own repo:
   ```yaml
   # .github/workflows/standard-node-ci.yml  (in org/actions-library)
   name: standard-node-ci
   on:
     workflow_call:
       inputs:
         node-version:
           type: string
           default: "20"
         deploy-target:
           type: string
           required: false
       secrets:
         DEPLOY_TOKEN:
           required: false
   jobs:
     test:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - uses: actions/setup-node@v4
           with: { node-version: ${{ inputs.node-version }}, cache: "npm" }
         - run: npm ci
         - run: npm test

     deploy:
       needs: test
       if: inputs.deploy-target != ''
       runs-on: ubuntu-latest
       environment: ${{ inputs.deploy-target }}
       steps:
         - run: ./deploy.sh ${{ inputs.deploy-target }}
           env:
             DEPLOY_TOKEN: ${{ secrets.DEPLOY_TOKEN }}
   ```

2. **Call it from a consumer repo with a pinned version**, keeping the
   caller workflow thin:
   ```yaml
   # .github/workflows/ci.yml  (in org/checkout-api)
   name: ci
   on:
     pull_request:
       branches: [main]
     push:
       branches: [main]
   jobs:
     ci:
       uses: org/actions-library/.github/workflows/standard-node-ci.yml@v1.3.0
       with:
         node-version: "20"
         deploy-target: staging
       secrets:
         DEPLOY_TOKEN: ${{ secrets.DEPLOY_TOKEN }}
   ```
   Pin `@v1.3.0` (a tag), not `@main` — the same versioning discipline as a
   Jenkins shared library (see
   [jenkins-centralized-shared-library](../jenkins-centralized-shared-library/SKILL.md)
   for the direct analog).

3. **Use `secrets: inherit` only when the caller repo's full secret set is
   genuinely intended for the reusable workflow** — otherwise pass secrets
   explicitly by name so it's auditable exactly what a centrally-maintained
   workflow can access from each caller.

4. **Host smaller, non-workflow reusable pieces as composite actions in
   the same or a sibling repo**, versioned the same way:
   ```yaml
   # org/actions-library/setup-node-env/action.yml
   name: "Setup Node env (org standard)"
   runs:
     using: "composite"
     steps:
       - uses: actions/setup-node@v4
         with: { node-version: "20", cache: "npm" }
       - run: npm ci
         shell: bash
   ```
   Consumed as:
   ```yaml
   - uses: org/actions-library/setup-node-env@v1.3.0
   ```

5. **Nest reusable workflows sparingly** — GitHub Actions allows calling a
   reusable workflow from within another reusable workflow up to a depth
   limit (4 levels as of current GitHub Actions); design the org's
   standard workflows as a shallow, well-documented hierarchy rather than
   deep nesting that's hard to trace.

6. **Version and changelog the library repo deliberately**: tag releases,
   document each `inputs:`/`secrets:` change, and treat removing or
   renaming an input as a breaking (major) change requiring caller
   migration, exactly like a public API.

7. **Roll out breaking changes gradually**: cut a new major tag, migrate a
   few pilot repos to `@v2.0.0`, validate, then open individual PRs against
   the remaining caller repos to bump the pin — never silently rewrite the
   floating `@main` ref that other repos might still be depending on and
   never bulk-force-push changes into consumer repos' workflow files
   without their own review.

8. **Enforce adoption, don't just offer it**, via a required organization
   ruleset or a periodic audit (e.g. a scheduled workflow that scans repos
   for `.github/workflows/*.yml` files that don't call the standard
   reusable workflow) if the goal is a hard organization-wide standard
   rather than an opt-in convenience.

## Best practices

- Pin callers to a tagged version (`@v1.3.0`) or full commit SHA, never
  `@main`, for the same reason third-party actions should be pinned — see
  [github-actions-single-repo-workflows](../github-actions-single-repo-workflows/SKILL.md).
- Keep the reusable workflow's `inputs:`/`secrets:` surface small and
  well-documented (a table in the library repo's README); every input
  should have a sensible `default` unless it's genuinely required.
- Prefer named `secrets:` passing over `secrets: inherit` for anything
  security-sensitive, so an audit of the reusable workflow's YAML alone
  shows exactly what secrets it can touch.
- Give the reusable-workflow repo its own tests: a workflow in that same
  repo that calls the reusable workflow against a throwaway/sample
  scenario on every change, so a broken reusable workflow is caught before
  a version tag goes out to every caller.
- Grant the minimum `permissions:` needed in the *caller* workflow — a
  reusable workflow only gets the permissions the caller's job explicitly
  passes down, so scoping the caller tightly protects every repo that
  invokes the shared workflow.
- Document a clear deprecation/migration path (a fixed window, e.g. 90
  days) when retiring an old major version, mirroring the same discipline
  used for Jenkins shared library majors — see
  [jenkins-centralized-shared-library](../jenkins-centralized-shared-library/SKILL.md).

## Common pitfalls

- **Symptom:** A caller repo's deploy step fails with "secret not found"
  even though the secret clearly exists in that repo's settings.
  **Fix:** Reusable workflows do not automatically inherit the caller's
  secrets — either add `secrets: inherit` at the call site, or pass the
  specific secret explicitly (`secrets: { DEPLOY_TOKEN: ${{
  secrets.DEPLOY_TOKEN }} }`); a `workflow_call` job with an undeclared
  secret input silently receives nothing.

- **Symptom:** Updating the reusable workflow's `main` branch immediately
  changes behavior for every caller repo pinned to `@main`, breaking
  several simultaneously.
  **Fix:** This is the cost of unpinned callers; migrate all callers to
  pin an explicit version tag, and treat `@main` as for the library
  repo's own testing only, never as a supported caller reference.

- **Symptom:** A private reusable workflow works when called from one repo
  but a different repo in the same org gets "workflow was not found" or
  an access-denied error.
  **Fix:** Check **Organization Settings → Actions → General → Access**
  for reusable workflows — a private reusable workflow's repo must
  explicitly allow access from the calling repo (or the org broadly), it
  is not automatically callable org-wide by default.

- **Symptom:** Adding a new required input to the reusable workflow breaks
  every caller simultaneously the moment it merges.
  **Fix:** Give new inputs a `default:` value for a minor version so
  existing callers keep working unchanged; reserve genuinely required new
  inputs for a major version bump callers must opt into.

- **Symptom:** Someone deletes an old reusable-workflow version tag or
  renames the hosting repo without checking who still references it,
  breaking pipelines across the org simultaneously with no warning.
  **Fix:** Before deleting a version tag or moving/renaming the
  actions-library repo, search caller repos (e.g. a GitHub code search for
  `uses: org/actions-library/.github/workflows/standard-node-ci.yml@v1`)
  for references still pinned to that tag/path — treat this the same as
  the "don't delete a still-referenced Jenkins shared library version"
  warning in
  [jenkins-centralized-shared-library](../jenkins-centralized-shared-library/SKILL.md).

## Worked example

**Scenario:** An organization has 40 Node.js service repos, each
duplicating a nearly-identical CI/CD workflow. They centralize into one
reusable workflow so each repo's caller file is ~10 lines, and adding a
new required security scan later needs only one PR to the library repo
plus each caller bumping its version pin.

`org/actions-library/.github/workflows/standard-node-ci.yml` (excerpt
adding a scan stage in `v1.4.0`):
```yaml
on:
  workflow_call:
    inputs:
      node-version: { type: string, default: "20" }
    secrets:
      DEPLOY_TOKEN: { required: false }
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: ${{ inputs.node-version }}, cache: "npm" }
      - run: npm ci && npm test

  security-scan:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: aquasecurity/trivy-action@0.24.0
        with: { scan-type: 'fs', severity: 'CRITICAL,HIGH', exit-code: '1' }

  deploy:
    needs: security-scan
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - run: ./deploy.sh staging
        env: { DEPLOY_TOKEN: "${{ secrets.DEPLOY_TOKEN }}" }
```

Caller repo (`org/checkout-api/.github/workflows/ci.yml`), unchanged
except bumping the version pin when ready to adopt the new scan stage:
```yaml
name: ci
on:
  pull_request: { branches: [main] }
  push: { branches: [main] }
jobs:
  ci:
    uses: org/actions-library/.github/workflows/standard-node-ci.yml@v1.4.0
    with: { node-version: "20" }
    secrets:
      DEPLOY_TOKEN: ${{ secrets.DEPLOY_TOKEN }}
```
Each of the 40 repos bumps `@v1.3.0` → `@v1.4.0` on its own schedule via a
one-line PR, instead of 40 separate workflow-file rewrites to add the
`security-scan` job.

## Cross-references

- [github-actions-single-repo-workflows](../github-actions-single-repo-workflows/SKILL.md) — the per-repo workflow/composite-action pattern this centralizes once duplicated across repos.
- [jenkins-centralized-shared-library](../jenkins-centralized-shared-library/SKILL.md) — the equivalent centralization pattern and versioning discipline on Jenkins.
- [secure-cicd-gates](../../../devsecops/skills/secure-cicd-gates/SKILL.md) — designing the security-scan stage this reusable workflow enforces consistently across all callers.
