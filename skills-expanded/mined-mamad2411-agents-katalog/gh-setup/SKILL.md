---
name: gh-setup
description: "Set up or align a repository's GitHub collaboration and delivery surface: repo settings, branch/ruleset policy, PR and security templates, Dependabot, Actions hardening, GitHub Environments, release workflows, and deploy workflows. Use when standardizing GitHub setup for repos, dependency updates, CI/CD, GitHub Actions, branch protection, release or publish pipelines, publishing versioned packages, or deploying running apps; route app deploy details to deploy references and package publish details to release references."
disable-model-invocation: true
---

# GitHub Setup

Make GitHub the boring, enforceable shell around a repo: settings, templates, Actions, secrets, releases, and deploys should all point at the same delivery contract.

This skill owns GitHub policy and workflow shape. It does not own product architecture, provider-specific infrastructure internals, app security review, or repo boot/readiness setup.

It also owns baseline existence and template shape for GitHub-facing collaboration files such as PR templates, issue templates, `SECURITY.md`, and `CONTRIBUTING.md`.

## Start Here

1. Inspect the repo before changing policy:
   - `.github/workflows/`
   - `.github/actions/`
   - `.github/pull_request_template.md`
   - `.github/ISSUE_TEMPLATE/`
   - `SECURITY.md`
   - `CONTRIBUTING.md`
   - the repository owner's public `<owner>/.github` default community-health
     files, when that defaults repository exists
   - `docs/`
   - package, build, release, deploy, and verification scripts
2. Check live GitHub settings before recommending changes: default branch, merge methods, branch/ruleset policy, Actions permissions, allowed GitHub Actions, Environments, Environment protection rules, secrets/vars locations, protected tags, and allowed push actors.
   Record the relevant as-is values for readback and rollback.
   Useful probes:
   - `gh repo view --json defaultBranchRef,mergeCommitAllowed,rebaseMergeAllowed,squashMergeAllowed,deleteBranchOnMerge`
   - `gh api repos/{owner}/{repo}/actions/permissions`
   - `gh api repos/{owner}/{repo}/private-vulnerability-reporting`
   - `gh api repos/{owner}/{repo}/vulnerability-alerts`
   - `gh api repos/{owner}/{repo}/automated-security-fixes`
   - `gh api repos/{owner}/{repo}/environments`
   - `gh api repos/{owner}/{repo}/rulesets`
3. Classify the repo:
   - **Versioned artifact**: package, library, CLI, GitHub Action, Homebrew-published binary, or registry publish -> read [release workflows](references/release-workflows.md) and [release targets](references/release-targets.md).
   - **Running app or service**: Pages, Cloudflare, SST, container, static app, backend, or hosted service -> read [deploy workflows](references/deploy-workflows.md), [deploy environments](references/deploy-environments.md), and [deploy secrets](references/deploy-secrets.md).
   - **Both**: publish the durable artifact first, then deploy from that published boundary. Read both release and deploy references.
4. Use repo-local commands as the source of truth. If a release repo lacks stable verification/package proof, or a deploy repo lacks stable verification, e2e, monitoring, or rollback hooks, pause GitHub wiring until the repo has durable readiness proof.
5. Keep `README.md`, `CONTRIBUTING.md`, `SECURITY.md`, `AGENTS.md`, and `docs/` current when GitHub changes affect contributor or operator workflows.
6. After changes, run the repo gates and read back live GitHub settings. Fix and retry until the result matches the intended diff, or restore the recorded state.

## Baseline Shape

- `main` is continuously releasable or deployable after verification passes.
- Pull requests run verification with read-only credentials.
- Merges to `main` run verification before release or deploy.
- Release/publish/deploy jobs are non-cancellable at the secret-bearing boundary.
- GitHub Environments hold release/deploy secrets and variables; repo-level secrets are bootstrap-only.
- Manual secret-bearing workflows validate inputs in a secretless job before checkout or credential loading.
- GitHub Actions artifacts are temporary CI scratch storage, not a release or deployment registry.
- Required workflows keep a stable final check when lane detection, matrices, or no-op paths can skip individual jobs.

## Repository Settings

Read [repo settings](references/repo-settings.md) when changing merge policy, branch protections, rulesets, tag protection, Actions permissions, Environment settings, or repository descriptions.

Default posture (pair each change with a live probe or write):

- Prefer squash merge: `gh repo edit --enable-squash-merge --enable-delete-branch-on-merge`; disable unused methods with `--enable-merge-commit=false` / `--enable-rebase-merge=false` unless history preservation requires them.
- Confirm with `gh repo view --json squashMergeAllowed,deleteBranchOnMerge,mergeCommitAllowed,rebaseMergeAllowed`.
- Preserve existing approval, status-check, signed-commit, actor, and tag restrictions unless the user explicitly asks to change them (`gh api repos/{owner}/{repo}/rulesets`).
- Prefer signed-commit requirements on protected/default branches when the plan and automation path support them.
- Treat running CI and enforcing green CI as separate states. Prefer an organization ruleset for common PR policy and repository rules for checks whose names legitimately differ; read [repo settings](references/repo-settings.md) before rollout.
- If direct pushes to `main` must remain allowed, prefer branch protection with conversation resolution rather than forcing all default-branch changes through PRs by accident. A no-bypass PR or required-check rule is incompatible with arbitrary direct pushes; inventory every human and automated writer first.
- For release writeback, prefer the release tool's native GitHub App commit
  path so GitHub signs the commit. Use the semantic-release GitHub commit
  plugin for prepared version files and GoReleaser's
  `commit_author.use_github_app_token` for Homebrew updates. Use a generic API
  commit action only when the release tool has no native signed path. Before a
  source writeback, reject superseded runs whose analyzed SHA is no longer the
  live default-branch head. That check narrows stale runs but is not atomic:
  require either a concrete external branch lease that blocks every merge and
  direct push from before release analysis through the API ref update, or an
  App-signed API implementation with the analyzed SHA as an expected-head
  precondition. Actions concurrency and a preflight check are not that lease.

## Templates

Read [templates](references/templates.md) when creating or aligning PR templates, issue templates, `SECURITY.md`, or contributor-facing GitHub guidance.

Default posture:

- Prefer public `<owner>/.github` fallback files for genuinely shared community
  policy; keep visibility-specific or repository-specific guidance local.
- PR templates should ask for summary, changed surfaces, risks, verification, and complexity.
- `SECURITY.md` should be private-first and avoid public issue reporting for vulnerabilities.
- On public repos, enable GitHub private vulnerability reporting before (or with) shipping that `SECURITY.md`, so the documented route works.
- On private repos, do not document GitHub private vulnerability reporting; point reporters at an existing private maintainer channel instead.
- `CONTRIBUTING.md` should describe contributor setup, validation, and PR workflow only when the repo accepts outside or cross-team contributions.
- Issue templates should exist only when they improve triage; avoid checklist theater.
- Keep durable workflow detail in docs, not copied across README, CONTRIBUTING, templates, and agent guidance.

## Actions Security

Read [Actions security](references/actions-security.md) before editing workflows that execute code, load secrets, publish artifacts, sign binaries, or deploy.

Hard defaults:

- Do not use `pull_request_target` for workflows that check out, install, build, test, package, publish, sign, deploy, or execute project code.
- Default workflow permissions to read-only or `{}` and grant scopes per job (`permissions: {}` at workflow top; widen per job).
- Pin high-trust release, publish, upload, signing, and deploy actions to full commit SHAs with same-line version comments when the repo can maintain them.
- Enable `sha_pinning_required` after reading current policy:

  ```bash
  gh api repos/{owner}/{repo}/actions/permissions
  gh api --method PUT repos/{owner}/{repo}/actions/permissions --input - <<'EOF'
  {"enabled": true, "allowed_actions": "all", "sha_pinning_required": true}
  EOF
  ```

  Preserve any intentional `allowed_actions` / allowlist values from the GET.
- Run `actionlint` for syntax and `zizmor` for GitHub Actions security before inventing bespoke validators.
- Run repository-history secret detection in a dedicated GitHub Actions workflow.
- Keep workflow YAML boring: prefer maintained actions and repo-owned commands over large inline shell/JavaScript blocks.
- Keep untrusted PR caches separate from privileged push, release, deploy, signing, or publish caches.

## Dependency Updates

- Enable vulnerability alerts and automatic Dependabot security updates broadly; they do not require a `dependabot.yml`:

  ```bash
  gh api --method PUT repos/{owner}/{repo}/vulnerability-alerts
  gh api --method PUT repos/{owner}/{repo}/automated-security-fixes
  ```

- Add `.github/dependabot.yml` only when the repository contains a supported package manifest, lockfile, or GitHub Actions workflow. Do not add inert boilerplate to content-only or empty repositories.
- Match each update entry to the actual ecosystem and manifest directory. Include `github-actions` only when workflows exist.
- Prefer a low-noise default for scheduled version updates: monthly cadence, one-day cooldown, and separate patch/minor and major groups. Preserve repo-specific release or compatibility constraints.
- Treat Dependabot PRs like ordinary advisory maintenance unless the repository already requires PR checks. Do not introduce PR-only rules or mandatory checks merely to enable dependency updates.
- Read back both settings after writes and confirm the config exists on the default branch. Run the repository's normal validation when adding or changing the config.

## Release Route

Use this route for versioned packages, libraries, CLIs, marketplace actions, Homebrew-published tools, Swift/CocoaPods packages, Go/Rust releases, and registry publishes.

Core shape:

```text
pull request -> verification
push to main -> verification -> prepare signed version commit when needed
             -> assemble and verify release -> publish immutable
             -> verify registry/tap/default-branch parity
```

Read only the target-specific references needed:

- [release workflows](references/release-workflows.md) - workflow layout, triggers, checkout, permissions, caches, skip-CI, signed writebacks, and trusted refs
- [release targets](references/release-targets.md) - npm, Swift, GoReleaser, Rust, GitHub Action, and Homebrew target shapes
- [semantic-release](references/semantic-release.md) - semantic-release config and dry-run checks
- [release troubleshooting](references/release-troubleshooting.md) - common release failures

Before enabling immutable releases at repository or organization scope, audit
every workflow that creates a GitHub Release. Metadata-only releases are
usually compatible; workflows that upload or replace assets after publication
must move to a draft-first transaction described in the release workflow
reference. Do not call a rollout complete from a green workflow alone: require
one real release for every distinct release shape, exercising each applicable
package, version-file, registry, and tap path. Read back immutability, release
attestation, signed writebacks, default-branch containment, and downstream
state for every surface that applies to that repository.

## Deploy Route

Use this route for running apps and services: static sites, SST apps, Cloudflare, containers, APIs, and hosted frontends.

Core shape:

```text
push to main
  -> detect changes
  -> run lane verification and build immutable payload
  -> e2e against that payload
  -> deploy through GitHub Environment
  -> monitoring and rollback handoff
```

Read only the deploy references needed:

- [deploy workflows](references/deploy-workflows.md) - lane detection, concurrency, manual deploy, permissions, monitoring handoff, and summaries
- [deploy environments](references/deploy-environments.md) - Environment contracts, OIDC, SST, Cloudflare/static-token boundaries
- [deploy secrets](references/deploy-secrets.md) - credential categories, logging, runtime secrets, OIDC, and token fallback
- [deploy troubleshooting](references/deploy-troubleshooting.md) - common deploy failures

## Output

Report the setup compactly:

- files changed
- GitHub settings or Environments to update manually
- release/deploy target and durable payload boundary
- verification run
- remaining risks or blockers

If live GitHub settings were not checked, say so. Do not present inferred settings as confirmed.

Example:

```text
files changed: .github/workflows/release.yml, SECURITY.md
settings: live rulesets not checked; require manual confirmation
target: npm package release from verified main
evidence: actionlint, npm test
risks: publish token environment still needs maintainer update
```
