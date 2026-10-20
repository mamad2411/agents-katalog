---
name: cicd-pipeline-author
description: Designs and hardens CI/CD pipelines across GitHub Actions, GitLab CI, Jenkins, and CircleCI — caching, matrix builds, least-privilege tokens, pinned actions, and OIDC instead of long-lived secrets. Triggers when writing or fixing a pipeline/workflow file, speeding up CI, or securing a build.
when_to_use: เขียน/แก้ .github/workflows, .gitlab-ci.yml, Jenkinsfile; CI ช้า/แพง; ต้อง harden pipeline หรือเปลี่ยนไป OIDC
---

## When to Use

Use this skill when the task touches a pipeline definition file or its performance/security:

- Authoring or editing `.github/workflows/*.yml`, `.gitlab-ci.yml`, `Jenkinsfile`, or `.circleci/config.yml`.
- CI is slow or expensive — reduce wall-clock time and runner minutes.
- Hardening a build: removing long-lived secrets, pinning third-party actions, scoping token permissions.
- Migrating cloud auth from static keys to OIDC (federated identity).
- Splitting a monolithic pipeline into reusable workflows/templates.

Skip if the change is a one-line tweak whose diff you can state in a sentence (bump a runner image tag, fix a typo in a step name) — just make it.

## Steps

1. **Detect platform and read the existing pipeline first.** Match the file: `.github/workflows/*` → Actions, `.gitlab-ci.yml` → GitLab, `Jenkinsfile` → Jenkins, `.circleci/config.yml` → CircleCI. Never rewrite blind — read the current file, note language/build tool, where secrets are consumed, and which steps dominate runtime.

2. **Lay out stages as a DAG, not a straight line.** Target order: `lint+typecheck` → `build` → `test` → `security-scan` → `deploy` (gated). Run independent stages in parallel; only serialize on real data dependencies. In Actions use `needs:`; in GitLab `stage:` + `needs:` for out-of-order DAG; in CircleCI `requires:` under workflows.

3. **Cache the dependency layer, key it on the lockfile.** Cache key = hash of the lockfile, with a restore-key fallback for partial hits. Cache the package dir, not `node_modules`-style install output that must stay in sync with the runner.
   - Actions: `actions/cache` with `key: deps-${{ runner.os }}-${{ hashFiles('**/lock*') }}` and `restore-keys: deps-${{ runner.os }}-`. For common ecosystems prefer the built-in cache (e.g. `setup-*` with `cache:` input) which keys the lockfile for you.
   - GitLab: `cache: { key: { files: [lockfile] }, paths: [...], policy: pull-push }`; set `policy: pull` on jobs that only read.
   - Never cache build artifacts that change every commit — that just thrashes the cache. Pass those between stages as artifacts instead.

4. **Add a matrix only where it earns parallelism.** Fan out across versions/OS that you actually support. Set `fail-fast: false` when you need the full failure map (e.g. compatibility testing); leave it `true` (default) to abort early and save minutes on normal PR runs. Shard a large test suite across N parallel jobs and merge results.

5. **Pin third-party actions/images by full commit SHA, not a tag.** Tags (`@v4`) are mutable and a supply-chain hole. Pin `uses: owner/action@<40-char-sha>  # v4.1.2` and keep the version in a trailing comment so a bot can bump it. Pin container/runner images by digest where the platform allows. First-party `actions/*` may use a major tag if your policy permits, but SHA is the safe default.

6. **Scope token permissions to least privilege.** In Actions, set top-level `permissions: { contents: read }` (default-deny everything else) and widen per-job only for what that job needs (e.g. `id-token: write` for OIDC, `packages: write` to publish). In GitLab, prefer job tokens with limited scope over project access tokens. Never give a test job write access.

7. **Replace static cloud secrets with OIDC.** Stop storing long-lived `AWS_*`/`GCP_*`/`AZURE_*` keys. Have the pipeline mint a short-lived token via the provider's federated identity:
   - Job needs `permissions: id-token: write` (Actions) or the platform's OIDC equivalent.
   - Configure a trust policy on the cloud side scoped to **this repo + this branch/environment + this workflow** (don't trust `repo:*`).
   - Use the provider's official auth action to exchange the OIDC token for temporary credentials. Remove the old secrets after the OIDC path is verified — not before.

8. **Factor shared logic into reusable workflows/templates.** Actions: reusable workflow called via `uses: ./.github/workflows/x.yml` or a composite action. GitLab: `include:` + `extends:` + `!reference`. CircleCI: orbs/commands. Jenkins: shared library. One source of truth beats copy-pasted YAML across services.

9. **Make failures fast and required.** Put cheap checks (lint, typecheck) before expensive ones so a bad PR fails in seconds. Add `timeout-minutes` to every job so a hung step can't burn an hour. Wire the gating jobs into branch protection / required status checks so deploy literally cannot run on a red build. Gate deploy on a protected environment with manual approval for prod.

10. **Validate locally and report the diff.** Lint the file, dry-run if possible (see Verify), then report **before/after wall-clock and estimated runner-minutes**, plus the security delta (secrets removed, permissions narrowed, actions pinned). A pipeline change without a measured result is unfinished.

## Common Errors

- **`permissions` block at top level silently kills the whole-workflow grant.** The moment you add any `permissions:` key, every unlisted scope becomes `none`. A push/comment step that worked before will now 403. Add back exactly what each job needs at job level.
- **Cache restored but the install step still runs full.** Usually the cache path is wrong, or the key changes every run (you hashed a file that mutates). Verify with the cache-hit output, and cache the package manager's store dir, not the project-local install dir.
- **OIDC `Error: Not authorized to perform sts:AssumeRoleWithWebIdentity` / audience mismatch.** The cloud-side trust condition doesn't match the token's `sub`/`aud`. Check the exact subject string format (it differs for branch vs tag vs environment vs pull_request) and that the audience matches what the auth step requests.
- **Pinned SHA points at a tag that was force-moved → action runs different code than reviewed.** Always re-verify the SHA belongs to the version in your comment; don't copy a SHA from an untrusted PR.
- **`fail-fast` cancels sibling matrix jobs and you lose the failure you needed.** For compatibility/flake debugging set `fail-fast: false`; for normal PRs keep it on to save minutes — they're opposite goals, pick deliberately.
- **Secrets passed into a reusable workflow vanish.** Reusable workflows don't inherit secrets implicitly — pass them with `secrets: inherit` or map each one explicitly.
- **`pull_request` from a fork can't read secrets / OIDC.** That's by design (untrusted code). Don't "fix" it by switching to `pull_request_target` with checkout of the PR head — that's a known privilege-escalation footgun. Run untrusted PR builds without secrets.
- **No `timeout-minutes` → a hung network call burns the full default timeout (often 6h) of paid minutes.** Set an explicit per-job timeout always.
- **Caching across untrusted PRs can poison the cache.** Scope/segregate caches so a fork PR can't write a cache a trusted branch later reads.

## Verify

- **Syntax/lint:** Actions → `actionlint` (catches expression and context errors a YAML linter misses). GitLab → CI Lint API/UI. CircleCI → `circleci config validate`. Jenkins → `jenkins-cli declarative-linter`. Any platform → a plain YAML linter as a floor.
- **Dry run where supported:** run the workflow locally (e.g. `act` for Actions) for fast iterate-on-failure before pushing; if the job has external/cloud deps that can't run locally, push to a throwaway branch and read the live run.
- **Security checklist passes:** no `secrets.*` for cloud creds remaining (OIDC instead); top-level `permissions` is read-only with per-job widening; every third-party action pinned to a full SHA; every job has `timeout-minutes`; deploy gated by required checks + protected environment.
- **Performance proven:** capture wall-clock and runner-minutes before vs after on a real run; confirm the cache reports a hit on the second run and parallel jobs actually overlap. Report the numbers — "should be faster" is not verification.
- **Branch protection enforced:** confirm the gating jobs are listed as required status checks so a red build blocks merge/deploy.
