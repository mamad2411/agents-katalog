---
name: ci-cd-pipelines
description: Designs, speeds up and hardens CI/CD pipelines, covering stage ordering, caching, parallel and sharded tests, pinned actions, least-privilege tokens, OIDC cloud auth, build-once artifact promotion, flaky-test handling and safe deployments with rollback. Use when creating or editing GitHub Actions, GitLab CI, Azure Pipelines or similar pipelines, when CI is slow or flaky, or when setting up deployments. Not for writing the tests themselves.
license: MIT
---

# CI/CD Pipelines

A pipeline exists to give fast, trustworthy feedback and to ship the exact artifact that was tested. Optimize for time-to-first-failure, treat the pipeline as production code with production credentials, and make every deploy reversible.

## When to use

- Creating a pipeline for a new repository or service.
- CI is slow, flaky, expensive, or developers bypass it.
- Adding or hardening deployments, environments, secrets or cloud access.
- Reviewing workflow files for security problems.

Not for: writing or fixing the tests themselves, or Dockerfile contents (use the dockerfiles skill).

## Workflow

1. **Read the current pipeline and measure it.** List the jobs and their durations over the last runs, the critical path, and the failure rate (how many failures were flaky reruns rather than real breaks).
2. **Order stages for fast feedback** (table below). Cheap checks first; run independent jobs in parallel.
3. **Cache dependencies,** keyed on the lockfile hash.
4. **Parallelize and shard** the slowest test suites.
5. **Harden:** least-privilege token permissions, actions pinned to commit SHAs, no secrets in logs, OIDC instead of long-lived cloud keys, safe handling of pull requests from forks.
6. **Build once, promote:** build and tag one artifact per commit, and deploy that same artifact to each environment.
7. **Deploy safely:** a deployment strategy, health checks, environment approvals for production, and a tested rollback.
8. **Protect the branch:** required status checks, required reviews, no force pushes.
9. **Validate the config** before merging: `actionlint` for GitHub Actions, the CI Lint tool or API for GitLab, and a run on a branch for Azure Pipelines.
10. **Ask the user before** changing production deploy targets, secrets, environment protection rules or branch protection, and before triggering a deploy.

## Stage ordering

| Order | Stage | Runs on | Aim |
|---|---|---|---|
| 1 | Lint, format check, typecheck, compile | Every push | A few minutes |
| 2 | Unit tests | Every push | Under ~5 minutes; shard if longer |
| 3 | Integration tests (real database or broker via service containers) | Every PR | Parallel to the e2e build |
| 4 | Security: dependency audit, secret scan, SAST, image scan | Every PR, in parallel | Never on the critical path if avoidable |
| 5 | Build and publish the artifact or image | Main branch (and tags) | Once per commit |
| 6 | E2E / smoke tests | PR (sharded) or the merge queue, and after each deploy | — |
| 7 | Deploy staging → verify → deploy production | Main branch or release tags | Automated, with approval gates |

- Run stages 1-4 as parallel jobs where possible; use dependencies (`needs:` or `dependsOn:`) only where a job truly needs another's output.
- Set timeouts on every job (`timeout-minutes`, `timeout`, `timeoutInMinutes`) so a hung job does not burn an hour.
- In monorepos, use path filters so only the affected parts build and test.
- Cancel superseded runs on pull requests (GitHub `concurrency` with `cancel-in-progress`, GitLab `interruptible: true`, Azure PR auto-cancel). **Never auto-cancel an in-progress deploy.**

## Caching

| Platform | How |
|---|---|
| GitHub Actions | `actions/setup-node` with `cache: npm` (likewise `setup-python` with `cache: pip`, `setup-java` with `cache: maven` or `gradle`; `setup-go` caches by default), or `actions/cache` keyed on `hashFiles('**/package-lock.json')` |
| GitLab CI | `cache: key: files: [package-lock.json]` with `paths:` pointing at the package manager cache |
| Azure Pipelines | `Cache@2` task with a key such as `'npm \| "$(Agent.OS)" \| package-lock.json'` |
| Docker layers | `docker/build-push-action` with `cache-from: type=gha` and `cache-to: type=gha,mode=max`, or registry-based cache |

- Cache the package manager's download cache or store (`~/.npm`, pnpm store, `~/.cache/pip`, `~/.m2`, `~/.gradle/caches`), and run the frozen install (`npm ci`) every time.
- Always include the lockfile hash, and the OS if needed, in the key. A cache that never invalidates produces "works in CI, broken locally" bugs.

## Test parallelism

| Runner | Sharding |
|---|---|
| Jest (28+), Vitest, Playwright | `--shard=<index>/<total>` |
| pytest | `pytest-xdist` (`-n auto`) for parallelism within one machine; plugins such as `pytest-split` across machines |
| Go | `go test ./...` already runs packages in parallel; split packages across jobs if needed |
| Gradle / Maven | `maxParallelForks` / Surefire `forkCount`; split modules across jobs |

| Platform | Matrix for shards |
|---|---|
| GitHub Actions | `strategy: matrix: shard: [1, 2, 3, 4]`, then `--shard=${{ matrix.shard }}/4` |
| GitLab CI | `parallel: 4`, then `--shard=$CI_NODE_INDEX/$CI_NODE_TOTAL` |
| Azure Pipelines | `strategy: parallel: 4`, then `--shard=$(System.JobPositionInPhase)/$(System.TotalJobsInPhase)` |

## Security

### Permissions

- GitHub Actions: set `permissions: contents: read` at the top of every workflow, and grant more per job only where needed (`id-token: write` for OIDC, `packages: write` to push images, `pull-requests: write` to comment).
- GitLab and Azure: use the narrowest job token scope and service connection scope available. Restrict who can run pipelines against protected branches and environments.

### Pin everything

- Pin third-party actions, orbs and templates to a full commit SHA, with the version in a comment: `uses: owner/action@<40-character-sha> # v1.2.3`. Tags can be moved to malicious code; SHAs cannot.
- Resolve the SHA from the source; never invent one: `git ls-remote https://github.com/<owner>/<action> refs/tags/<tag>` (for annotated tags, use the line ending in `^{}`), or look at the tag's commit on GitHub.
- Let Dependabot or Renovate update pinned SHAs, so pinning does not freeze you on vulnerable versions.
- Pin tool versions too (`node-version-file: .nvmrc`, explicit CLI versions). Do not `curl | bash` installers from the internet.

### Untrusted input and forks

- **Script injection:** never interpolate attacker-controlled values directly into `run:` scripts (`${{ github.event.pull_request.title }}`, branch names, issue bodies, commit messages). Pass them through environment variables and quote them:

  ```yaml
  - run: echo "Title: $PR_TITLE"
    env:
      PR_TITLE: ${{ github.event.pull_request.title }}
  ```

- **`pull_request_target`** runs with the base repository's secrets and write token. Never check out and run the PR's code in it. Use `pull_request` for building and testing contributions.
- Do not use self-hosted runners for public repositories' pull requests; forked code would run on your machines.

### Secrets

- Store secrets in the platform's secret store, scoped to the environment that needs them (staging secrets cannot reach production).
- Never print them. Masking is best-effort: base64-encoding or splitting a secret defeats it.
- Prefer short-lived credentials (next section) over stored keys. Rotate any secret that appeared in a log.
- Add secret scanning (for example gitleaks, or the platform's built-in scanner) to CI and to pre-commit hooks.

### OIDC instead of long-lived cloud keys

The pipeline exchanges a short-lived identity token for cloud credentials. Nothing long-lived is stored.

| CI → Cloud | Mechanism |
|---|---|
| GitHub Actions → AWS | `aws-actions/configure-aws-credentials` with `role-to-assume`; IAM role trust policy for `token.actions.githubusercontent.com` |
| GitHub Actions → Azure | `azure/login` with client, tenant and subscription ids; federated credential on an app registration or managed identity |
| GitHub Actions → GCP | `google-github-actions/auth` with a Workload Identity Federation provider |
| GitLab CI | `id_tokens:` keyword with an audience, exchanged by the cloud's federation config |
| Azure Pipelines | Service connections using workload identity federation |

Restrict the trust to the exact repository **and** branch or environment (the token's `sub` claim, for example `repo:org/repo:environment:production`). A trust that accepts any branch lets any branch deploy to production.

## Build once, promote

- Build the artifact (image, package, bundle) **once per commit**. Tag it with the commit SHA and record its digest.
- Deploy that same artifact or digest to staging, then production. Never rebuild per environment; a rebuild is a different, untested artifact.
- Inject environment-specific config at deploy time (environment variables, config service), not at build time.
- Never deploy a moving tag such as `latest`. Deploy by digest or immutable tag.
- Generate provenance and an SBOM where the platform supports it (for example GitHub artifact attestations), so you can prove what was deployed.

## Flaky tests

- Track them: a test that fails and then passes on retry, without a code change, is flaky. Keep a list.
- Quarantine quickly: mark the test as skipped or move it to a non-blocking job, **with an issue link, an owner and a deadline**. A blocking flaky test trains everyone to ignore red builds.
- Fix the causes: shared state between tests, test order, real time or time zones, sleeps instead of waiting for conditions, real network calls, random data without a seed, resource leaks.
- Automatic retries, if any, belong at the single-test level and must be reported. Never blanket-retry whole jobs to hide failures.

## Deployment strategies

| Strategy | How | Rollback | Use when |
|---|---|---|---|
| Rolling | Replace instances in batches | Roll forward or back in batches | Default for stateless services |
| Blue/green | Deploy to an idle copy, switch traffic | Switch back | Fast, all-at-once cutover with instant revert |
| Canary | Send a small percentage of traffic to the new version, watch metrics, increase | Route all traffic back | High-traffic services with good metrics |
| Feature flags | Deploy code dark, enable per user or percentage | Turn the flag off | Decoupling deploy from release |
| Recreate | Stop old, start new | Redeploy old | Only when two versions cannot run together (avoid) |

- Every deploy needs an automated health check after it (smoke test, error rate, latency). Fail the pipeline, and roll back automatically if possible, when the check fails.
- Rollback = redeploy the previous known-good artifact digest. Practise it, and keep it one command or one click.
- App rollback is only safe if database migrations are backward compatible (expand/contract). Follow the database-migrations skill, and run migrations as a separate pipeline step, once, not from every replica.
- Production deploys need an approval gate or an explicit release action: GitHub Environments with required reviewers, GitLab protected environments, Azure Pipelines environment approvals and checks.

## Branch protection

- Require pull requests and at least one approving review for the main branch. Use CODEOWNERS for critical paths.
- Require the CI checks to pass. The required check names must exactly match the job names, and renaming a job silently drops the requirement.
- Block force pushes and branch deletion on main and release branches.
- Use a merge queue (or "require branches to be up to date") so main is tested with the exact merged code.

## Anti-patterns

- **One giant sequential job** that takes 40 minutes and fails at minute 38 on a lint error.
- **Unpinned third-party actions** (`@main`, `@v1`) with access to secrets.
- **Long-lived cloud keys** stored as CI secrets when OIDC is available.
- **Default write-all token permissions.**
- **Rebuilding for each environment**, or deploying `latest`.
- **`continue-on-error: true` / `allow_failure: true`** on checks that matter, which turns failures into noise.
- **`sleep 30` waiting for services** instead of health checks or readiness waits.
- **Manual production steps** that are not in the pipeline, which nobody can reproduce or roll back.
- **Ignoring flaky tests** until everyone clicks "re-run" by reflex.

## Done when

- The critical path is measured, and the fast checks report within minutes.
- Dependencies are cached with lockfile-based keys, and slow suites are sharded.
- Workflows declare least-privilege permissions, third-party actions are SHA-pinned, and no attacker-controlled input is interpolated into scripts.
- Cloud access uses OIDC restricted to the repository and environment, or the reason it cannot is documented.
- One artifact per commit is promoted across environments by digest.
- Production deploys have an approval gate, a post-deploy health check and a tested rollback.
- The main branch requires passing checks and reviews.

## References

- [references/examples.md](references/examples.md) — read when writing a new pipeline; contains minimal, hardened examples for GitHub Actions, GitLab CI and Azure Pipelines.
