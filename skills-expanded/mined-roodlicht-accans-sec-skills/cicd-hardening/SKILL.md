---
name: cicd-hardening
description: CI/CD pipeline hardening for GitHub Actions and GitLab CI — trust-model (pull_request_target vs pull_request), action pinning to SHA, OIDC-based cloud access, permissions minimization, runner isolation, and supply-chain gates (SLSA provenance, signing).
---

# CI/CD Hardening

## When to use

This skill treats the pipeline itself as the attack surface, not the code flowing through it. CI/CD compromise is a supply-chain incident: whoever owns the pipeline owns the release artifacts.

Triggers on:

- A question like "review our workflow files for security", "set up OIDC between GitHub and AWS", "why is `pull_request_target` dangerous", "pin all actions to SHA", "can we hit SLSA-L3".
- New or changed `.github/workflows/*.yml`, `.gitlab-ci.yml`, Jenkinsfile, Azure Pipelines YAML, CircleCI config, reusable workflow definitions, composite actions.
- An incident or near-miss: a forked PR could use secrets, a third-party action had a compromise, a self-hosted runner was abused.
- A compliance audit asking for SSDF evidence or SLSA-level attestation.
- A supply-chain moment where the pipeline is the last link before release (`supply-chain` skill calls in here for build-provenance setup).

### When NOT (handoff)

- SAST in the pipeline → `sast-orchestrator` for tool choice and ruleset. This skill only decides that it runs somewhere in the workflow phase.
- Secret scanning in the pipeline → `secrets-scanner`. Same split.
- Dependency scanning and CVE triage → `cve-triage` and `supply-chain`. The gate logic is in `security-gate`.
- Container build itself (Dockerfile, base image) → `container-hardening`. We only cover the workflow that builds it here.
- Kubernetes deployment by a GitOps agent (Argo CD, Flux) → `k8s-security`.
- Infrastructure provisioning (Terraform apply from CI) → `iac-security` for the resources side, here only the creds flow via OIDC.
- IR for an actually compromised pipeline → `ir-runbook`.

## Approach

Seven phases. Phase 1 (trust model) is the heart — what goes wrong in CI attacks is often a misconception about who is allowed to run what.

### 1. Trust model and workflow triggers

**GitHub Actions — the `pull_request_target` trap.**

`pull_request` (default) runs workflow code from the PR branch and has **no** access to the base repo's secrets. Safe for fork PRs.

`pull_request_target` runs the workflow code from the **base branch** (so trusted) but with the PR context. Has secrets. Intended for scenarios like "label the PR after a lint check". **Extremely dangerous** if you execute the PR code (via checkout + test run), because then your base-trusted workflow runs untrusted fork code with secrets on board. This is the attack class GitHub itself calls "poisoned pipeline execution".

Rule: if you use `pull_request_target`, **never** check out the PR branch and **never** execute code from the PR. Do: set labels, post comments, read metadata.

**GitLab CI — merge request pipelines.**

`merge_request_event` runs on the source branch with access to variables depending on the protected flag. Protected variables are only available on protected branches — set prod secrets to protected. Cross-project triggers via pipeline trigger tokens are another vector; treat those tokens as secrets.

**Protected branches and required checks.**

Set main/release branches to protected: no direct push, review-required, status-checks-required, linear history, no force-push. `security-gate` as a required check. Without branch protection, a compromised developer account can start release pipelines directly.

**CODEOWNERS**: required review by specific teams for critical paths (`.github/workflows/`, `infra/`, `deploy/`). Without CODEOWNERS enforcement at branch protection, it is advice, not policy.

### 2. Action pinning and provenance

Third-party Actions are the underestimated supply-chain risk. An owner getting compromised or an action mutating affects everyone using the tag.

- **Pin to SHA, not to tag.** `uses: actions/checkout@v4` is mutable (the tag can be moved). `uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683` is immutable. For critical workflows (release, deploy): always SHA-pin.
- **Configure Renovate/Dependabot to update SHA pins** with changelog review. Without auto-updates you run on stale, vulnerable Actions.
- **Verified publishers and Actions from trusted orgs** (`actions/`, `github/`, `docker/`, `aws-actions/`, `azure/`, `google-github-actions/`). Third-party marketplace Actions with 10 stars and one maintainer are a choice you have to be able to defend.
- **Lint tools**: `zizmor` (Rust, OSS) for GitHub Actions audit — catches `pull_request_target` misuse, impersonation, expression injection. `actionlint` for syntax. `poutine` for cross-platform CI analysis.
- **GitLab equivalent**: pin included templates to a fixed version, no `@main` for `include: remote:` or shared templates.

**Expression injection**. `${{ github.event.pull_request.title }}` directly in a `run:` block is command injection: a PR title with ``" ; rm -rf / #`` runs on the runner. Fix: pass the value via an env variable (`env: TITLE: ${{ github.event.pull_request.title }}`, then `"$TITLE"` in the script). Zizmor catches this.

### 3. Secrets and creds: OIDC first

Long-lived cloud credentials in CI secrets is the classic bad pattern. OIDC fixes it: the CI runner gets a short-lived, audience-bound token from the identity provider, the cloud side accepts that token and hands out temporary IAM creds.

- **GitHub → AWS**: OIDC provider in AWS (`token.actions.githubusercontent.com`), IAM role with trust policy on `repo:<org>/<repo>:ref:refs/heads/main` or `environment:<env>`. `aws-actions/configure-aws-credentials@v4` SHA-pinned.
- **GitHub → GCP**: Workload Identity Federation, `google-github-actions/auth`.
- **GitHub → Azure**: federated identity credentials on the App Registration.
- **GitLab → cloud**: `id_tokens` feature (JWT per job) with the equivalent OIDC setup on the cloud side.

OIDC trust policies:

- **Scope as narrowly as possible.** Trust only specific branches (`refs/heads/main`), or better: environments (`environment:production`). Not on `repo:<org>/<repo>:*`.
- **Audience claim explicit** on `sts.amazonaws.com` or cloud equivalent. Default is wide; you want it narrow.
- **No fallback to static keys.** If OIDC for whatever reason does not work, fail the pipeline — no "oh well, let's use the old `AWS_SECRET_ACCESS_KEY` for now". That key does not exist anymore, if all is well.

Remaining secrets (third-party API keys that do not support OIDC):

- **Environment-scoped** in GitHub Actions (`environment: production` with protected flag and required reviewers). Or GitLab protected variables on a protected branch.
- **Remove after use** where possible; some tooling (HashiCorp Vault integration) generates just-in-time creds.
- **Never echo.** A bug where a secret accidentally lands in log output: GitHub auto-masks but is not infallible. Disable `set -x` / `--debug` in steps that touch secrets.

### 4. Permissions: minimal per workflow

The default `GITHUB_TOKEN` in GitHub Actions was historically `write-all`. Since 2023 the default is read-only in new repos, but old repos do not flip automatically. Set explicitly:

```yaml
permissions:
  contents: read          # default for most workflows
jobs:
  deploy:
    permissions:
      contents: read
      id-token: write     # for OIDC
      packages: write     # for ghcr push, only in deploy job
    ...
```

Workflow-level permissions set a ceiling; job-level can refine downward. For jobs that need push rights, scope strictly to that job.

GitLab CI equivalent: `CI_JOB_TOKEN` permissions via Project → Settings → CI/CD → Token access, with an allowlist of projects your token may use.

### 5. Runners: isolation and choice

**GitHub-hosted runners** are ephemeral (fresh VM per job), good default. Cost: free for public repos, paid for private.

**Self-hosted runners** are persistent unless you re-provision them every run. Risks:

- **Persistent state**: a previous run can leave secrets/artifacts behind for the next run, cross-job contamination.
- **Fork-PR exposure**: a forked PR running on a self-hosted runner has access to the entire host. Default advice: **self-hosted runners only for workflows that cannot be triggered by forked PRs**. Private repos or internal-only workflows.
- **Network positioning**: a self-hosted runner in a VPC can reach things you do not want it to.

If you must self-host: **ephemeral runners** (actions-runner-controller on Kubernetes, or `--ephemeral` flag), **non-root service account**, **runner scope per repo or per org** and not cluster-wide, **network-egress policy**, no mount of docker.sock (gives a breakout).

Scale-set runners with firecracker/KVM isolation (GitLab) or runner groups with labels (GitHub) for further segmentation.

### 6. Supply-chain gates in the pipeline

The place where `supply-chain`, `secrets-scanner`, `cve-triage`, `sast-orchestrator`, and `security-gate` land as CI steps.

- **Per-PR** (blocking): `/security-gate` as a required check, which internally runs `secrets-scanner` + `sast-orchestrator` + `cve-triage`.
- **Per-build** (artifact-related): generate SBOM (syft), sign attestation (cosign), SLSA provenance via `slsa-framework/slsa-github-generator`. See `supply-chain` phase 2.
- **Per-release** (additional): image scan with Trivy/Grype, signing verify, provenance verify. Fail-fast on unsigned or unresolved-critical.
- **OpenSSF Scorecard** as a periodic self-assessment of pipeline hygiene: pinned Actions, branch-protection, SAST present, etc. Reports a score plus per-check detail.

Log CI events to SIEM: who ran which workflow, which secrets were touched, which artifacts produced. Without an audit trail, a compromised-CI incident is not reconstructable.

### 7. Verification-loop

Layer 1: scope (all workflow files covered? self-hosted runners inventoried? OIDC applied everywhere possible?), assumptions ("we pin to SHA" only if you have actually read the `uses:` lines), gaps (pull_request_target carefully checked? expression-injection checks done?), consistency (permissions scope matches what the job actually does).

Layer 2: Action SHAs and publisher identities are correct, OWASP CICD Top 10 mapping correct, no invented zizmor/actionlint rule IDs, SLSA-level claims supported.

## Output

```
CI/CD hardening review — <repo/pipeline>
Platform: <GitHub Actions | GitLab CI | Jenkins | Azure | ...>

Trust model:
  Triggers used:           <list pull_request/pull_request_target/push/etc>
  pull_request_target risk:<clean | finding with context>
  Protected branches:      <config summary>
  CODEOWNERS active:       <yes/no>

Action pinning:
  % Actions SHA-pinned:    <N/M>
  Third-party from unknown orgs: <list>
  Expression injection:    <clean | findings>

Credentials:
  OIDC to cloud:           <AWS/GCP/Azure, trust scope>
  Long-lived secrets:      <N, which and why still>
  Environment-protected:   <yes/no per critical environment>

Permissions:
  Workflows with default write-all: <N>
  permissions: empty or too broad:  <list>

Runners:
  Self-hosted in use:      <yes/no + scope>
  Ephemeral:               <yes/no>
  Fork-PR access to self-hosted: <blocked | open>

Supply-chain gates:
  SAST in pipeline:        <sast-orchestrator handoff>
  Secret scan:             <secrets-scanner handoff>
  Dep scan:                <cve-triage handoff>
  SBOM + provenance:       <supply-chain handoff>
  Scorecard:               <score + weakest checks>

Findings (severity-sorted, follow security-review format)

Verification-loop: ...
```

## References

- GitHub Actions Security Hardening — [https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions). Primary GitHub docs on workflow security.
- GitHub Actions OIDC — [https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect).
- GitLab CI Security — [https://docs.gitlab.com/ee/ci/pipelines/](https://docs.gitlab.com/ee/ci/pipelines/) and [https://docs.gitlab.com/ee/ci/secrets/](https://docs.gitlab.com/ee/ci/secrets/).
- OWASP Top 10 CI/CD Security Risks — [https://owasp.org/www-project-top-10-ci-cd-security-risks/](https://owasp.org/www-project-top-10-ci-cd-security-risks/). Canonical categorization.
- NSA/CISA "Defending CI/CD Environments" — [https://media.defense.gov/2023/Jun/28/2003249466/-1/-1/0/CSI_DEFENDING_CI_CD_ENVIRONMENTS.PDF](https://media.defense.gov/2023/Jun/28/2003249466/-1/-1/0/CSI_DEFENDING_CI_CD_ENVIRONMENTS.PDF). 2023 guidance.
- SLSA — [https://slsa.dev/](https://slsa.dev/). Build-provenance framework, see also `supply-chain`.
- OpenSSF Scorecard — [https://github.com/ossf/scorecard](https://github.com/ossf/scorecard). Self-assessment of project hygiene.
- zizmor — [https://github.com/woodruffw/zizmor](https://github.com/woodruffw/zizmor). Static analysis for GitHub Actions.
- actionlint — [https://github.com/rhysd/actionlint](https://github.com/rhysd/actionlint). Workflow syntax linter.
- slsa-github-generator — [https://github.com/slsa-framework/slsa-github-generator](https://github.com/slsa-framework/slsa-github-generator). SLSA-L3 provenance in GitHub Actions.
- Trail of Bits — "Publishing Python packages from GitHub Actions" threat model ([https://blog.trailofbits.com/2023/05/23/trusted-publishing-a-new-benchmark-for-packaging-security/](https://blog.trailofbits.com/2023/05/23/trusted-publishing-a-new-benchmark-for-packaging-security/)). Good reference work for OIDC-trust setup.

## Categories

- appsec
