---
name: secure-cicd
description: >
  Hardening the delivery pipeline and wiring the security gates that run in it. Carries: why CI is
  the most over-privileged identity in the system, poisoned pipeline execution and the trigger rules
  that prevent it (fork PRs never receive secrets), OIDC federation to the cloud instead of stored
  keys, least-privilege job permissions and actions pinned by commit SHA, and the gate ladder —
  gitleaks, semgrep, Trivy/Grype, Syft SBOM, checkov/kubeconform/conftest, cosign signing and
  attestation, plus the agent-specific eval and red-team gates. Also: what should block a merge
  versus report. Load when building or reviewing a pipeline, adding a security gate, wiring cloud
  auth in CI, or deciding what fails a build. Triggers: CI, CD, pipeline, GitHub Actions, workflow,
  build security, SAST, DAST, semgrep, gitleaks, secret scanning, checkov, kubeconform, OIDC
  federation, poisoned pipeline execution, PPE, pull_request_target, pin actions, release pipeline,
  what should fail the build. Artifact tooling is `supply-chain-security`; the musts are
  `policy/supply-chain.md` C6.
---

# secure-cicd — the pipeline can deploy to production, so treat it like production

**Pinned:** gitleaks, semgrep, trivy, syft, cosign, checkov, kubeconform, conftest — unpinned ·
authored 2026-07 · run `/skill-update secure-cicd` once the pipeline exists.

> On-demand: load this when building or reviewing a pipeline. The non-negotiable rules are canon
> (`supply-chain.md` `C6`, and `identity-and-access.md` `I3`). The *tools* for SBOM, scanning, and
> signing are `supply-chain-security`; the policies the gates run are `policy-as-code`; delivery to
> the cluster is `gitops`.

## When this applies

Building or reviewing a pipeline. Adding a gate. Wiring cloud auth. Deciding what fails a build.

## The threat nobody models

CI can write to production, read every secret, and publish artifacts your users run. It is usually
the most over-privileged identity in the system and the least reviewed — and an agent that can
trigger a pipeline inherits everything the pipeline can do (`ai-security.md` `AI2`).

**Poisoned Pipeline Execution (`CICD-SEC-4`)** is the specific attack: attacker-controlled repository
content executes in the build environment with the build's credentials. It arrives through
build scripts, test files, `Makefile`s, pre-commit configs, and dependency install hooks — all of
which a fork PR can modify.

The defence is structural:

```yaml
on:
  pull_request:          # runs in the FORK's context: no secrets, read-only token
  push:
    branches: [main]     # trusted context, but only after review has merged
```

- **Never `pull_request_target` with a checkout of the PR head.** That combination runs untrusted
  code in a *trusted* context with secrets — it is the canonical PPE vulnerability.
- **Fork PRs get no secrets and no elevated identity.** Split the workflow: untrusted checks on the
  PR, privileged steps after merge or behind an environment approval.
- **Require approval for first-time contributors' workflow runs.**

## Least privilege in the pipeline

```yaml
permissions: {}                       # deny-all at the top; grant per job

jobs:
  scan:
    permissions: { contents: read }   # only what this job needs
  publish:
    permissions:
      contents: read
      id-token: write                 # OIDC federation — C6, I3
      packages: write
      attestations: write
```

- **Default to `permissions: {}` and grant per job.** The repo-wide default is usually far too broad.
- **Pin actions by commit SHA, not tag** (`C1`) — a tag is mutable, and a third-party action is code
  with write access to your build:
  ```yaml
  - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683   # v4.2.2
  ```
- **No long-lived cloud credentials.** OIDC federation to AWS/GCP/Azure, with the trust policy scoped
  to the specific repo *and branch* — a policy trusting `repo:ORG/REPO:*` accepts any branch,
  including one a contributor pushed.
- **Separate the jobs that can publish** from the jobs that run repository-supplied code.

## The gate ladder

Ordered fastest-and-cheapest first, so feedback is quick and the expensive gates only run on code
that passed the cheap ones.

| Gate | Tool | Blocks? |
|---|---|---|
| Secret scanning | `gitleaks` | **Yes, always** — a committed secret needs rotation, not a warning |
| Lint / format | `ruff` | Yes |
| Unit + offline tests | `pytest` | Yes |
| Leakage tests | `pytest -k leakage` | Yes (inherited from the DS lineage) |
| SAST | `semgrep --config auto` | Block on high-confidence rules; report the rest |
| IaC / manifest config | `checkov`, `trivy config`, `kubeconform`, `conftest` | **Yes** — same policies as admission (`policy-as-code`) |
| Dependency + image CVEs | `grype`, `trivy image --ignore-unfixed` | Block on Critical; report High |
| SBOM | `syft -o cyclonedx-json` | Generate always; failure to generate blocks |
| Sign + attest | `cosign sign`, `attest-build-provenance` | Yes, on release |
| **Agent eval suite** | `agent-evaluation` harness | Capability: relative to baseline + tolerance |
| **Red-team safety suite** | `llm-red-teaming` cases | **Yes, absolutely** — any regression fails |

### What should block versus report

The judgement that determines whether the pipeline is respected or routed around:

**Block** on: anything with a fix available and a clear owner (a committed secret, a Critical CVE with
a patch, a policy violation, a failing test, a safety-suite regression).

**Report** on: findings with no available fix, low-confidence SAST results, and informational scans.
Route them to `risk-register.md` with an owner.

**The failure mode is blocking on things people can't fix.** A pipeline that fails for reasons
outside the author's control gets bypassed, and then the gates that mattered are bypassed too.
`--ignore-unfixed` exists for this reason.

## Shape of the security workflow

```yaml
name: security
on: [pull_request, push]
permissions: {}

jobs:
  static:
    permissions: { contents: read, security-events: write }
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683
        with: { fetch-depth: 0 }        # gitleaks needs history
      - run: gitleaks detect --redact --exit-code 1
      - run: semgrep ci
      - run: trivy config deploy/ --exit-code 1 --severity HIGH,CRITICAL
      - run: kubectl kustomize deploy/overlays/prod | conftest test -p policies/ -

  build-and-attest:
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    permissions: { contents: read, id-token: write, packages: write, attestations: write }
    steps:
      - # build -> digest
      - run: syft "$IMAGE@$DIGEST" -o cyclonedx-json > sbom.json
      - run: grype "$IMAGE@$DIGEST" --fail-on critical
      - run: cosign sign --yes "$IMAGE@$DIGEST"
      - run: cosign attest --predicate sbom.json --type cyclonedx "$IMAGE@$DIGEST"
      - uses: actions/attest-build-provenance@v2
        with: { subject-name: "$IMAGE", subject-digest: "$DIGEST" }
```

Full working template: `.claude/templates/security-ci.yml`.

## Cloud-native CI/CD — same bar, different buttons

CodePipeline/CodeBuild, Cloud Build, and Azure Pipelines are held to everything above; only the
mechanism changes. The per-cloud detail is in `infra-aws` / `infra-gcp` / `infra-azure`. The four
things that transfer unchanged:

1. **A least-privilege service identity per pipeline** — not the default build service account, which
   is broad on every cloud (`I3`).
2. **No stored credentials.** The build already has an identity; use it. Cross-cloud or
   cloud-from-GitHub means OIDC federation with the trust scoped to repo **and** branch (`C6`).
3. **Untrusted-contributor builds receive no secrets** — the PPE rule (`CICD-SEC-4`) is not a
   GitHub-specific concern.
4. **Artifact verification at deploy**, not just signing at build (`C3`). Each cloud has the
   mechanism: Binary Authorization on GCP, image signing verified at admission on EKS/AKS.

## Runners

Hosted runners are ephemeral and isolated by the provider — the usual right choice. **Self-hosted
runners on public repositories are dangerous**: a fork PR can run arbitrary code on your
infrastructure, and without per-job ephemerality the next job inherits whatever the last one left.
If self-hosting: ephemeral runners, isolated network, no ambient cloud credentials, never on a public
repo without approval gates.

## Gotchas

- **`pull_request_target` + PR checkout.** The one to grep for in any inherited pipeline.
- **Secrets in workflow logs.** Masking is best-effort and defeated by base64 or JSON embedding. Don't
  echo; use OIDC so there's less to leak.
- **Actions pinned by tag.** Feels pinned, isn't.
- **A cloud trust policy scoped to the repo but not the branch.** Any branch can then assume the role.
- **Caches as an attack path.** A poisoned cache from an untrusted branch is restored into a trusted
  job — scope cache keys by branch trust level.
- **Blocking on unfixable findings.** Covered above; it's how pipelines lose legitimacy.
- **Gates that only run on PR.** Anything merged by admin override skipped them; run on `push` to
  main too.
