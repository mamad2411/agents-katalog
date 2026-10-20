---
name: lyra-ci-cd-automation
description: "CI/CD pipelines that are fast, safe, and reversible — 2026 edition: cost-ordered gates that block merge, SHA-pinned actions with least-privilege OIDC, deterministic caching, rootless Podman builds with registry layer cache, build-once/promote-by-digest with signing, tested rollback, and pipeline telemetry. Use when writing or reviewing pipeline configs, containerizing CI builds, designing deploy workflows, or debugging slow/flaky pipelines."
compatibility: "Examples use GitHub Actions; rules hold for GitLab CI and others. Optional: podman/buildah in CI, cosign, trivy or grype, gh CLI. Composes with lyra-podman-images, lyra-podman-deploy, lyra-security-supply-chain, lyra-bug-hunter. Version policy: examples target the latest stable release of every tool; minimum supported is the newest LTS (or last maintained major), and features newer than the minimum are flagged inline."
---

# lyra-ci-cd-automation

## What it does

Automates the path from commit to production so that nothing unverified ships and everything shipped can be un-shipped. The pipeline is the source of truth — "I tested it locally" is not a gate. Three properties are required together: **fast** (or people bypass it), **safe** (or it's theater), **reversible** (or every deploy is a bet). Container builds are first-class: rootless Podman in CI, registry-shared layer cache, digest promotion, signatures.

Positioning in the suite's CI/CD pair, honestly: the core discipline (gates, promotion, rollback, flake quarantine, telemetry) is shared with `lyra-ci-cd` — this skill restates it in its current form and adds the container-native and supply-chain machinery (rootless Podman builds, digest promotion, signing, scan gates, OIDC). **Where the two disagree, this skill is current** — e.g. actions pinned by SHA here vs `@v4` tags in the sibling's older examples. Reach for `lyra-ci-cd` only for a deliberately minimal, non-container pipeline.

## The rules

### 1. Gates run in cost order and block merge — no bypass

lint → typecheck → unit tests → build → integration → (post-staging) E2E. Cheap kills first: a two-second lint failure must never wait on a two-minute build. Every gate is a required status check behind branch protection; no `--no-verify`, no skip-CI labels, no `continue-on-error` on gates, no direct pushes to main. If a gate is wrong, fix the gate — don't route around it. Absolutism needs a pressure valve or it gets one improvised at 3 a.m.: define **break-glass** up front — who may invoke it (two named approvers), how (a protected manual workflow, never a setting toggled off), and what it leaves behind (an audit entry and a mandatory postmortem). A defined emergency path is what keeps the other 99.9% of merges gate-clean.

### 2. Pin and permission everything — CI is an attack surface

Actions pinned by commit SHA (`uses: actions/checkout@<sha> # v4`), base images by digest, toolchains by exact version. Workflow `permissions:` starts at `contents: read` and adds per-job only what that job needs — e.g. the sign-and-push job in rule 4 adds `id-token: write` (OIDC) and `packages: write`; least privilege means naming what each job *does* need, not just denying. Cloud and registry auth via **OIDC**, not long-lived secrets. Never run untrusted PR code with secrets in scope (`pull_request_target` + checkout of the PR head is the classic self-pwn). Workflow files are code: lint them (actionlint for syntax and shell bugs, zizmor for security smells) as part of the lint gate. This rule is the supply-chain skill's foothold in CI — see lyra-security-supply-chain.

### 3. Cache deterministically

Dependency caches keyed on the lockfile hash (`hashFiles('pnpm-lock.yaml')`), never on timestamps or run ids. Container layer cache lives in the registry so ephemeral runners benefit:

```yaml
- run: |
    # ghcr requires lowercase; github.repository preserves case — normalize first
    REPO="${GITHUB_REPOSITORY,,}"
    podman build --layers \
      --cache-from "ghcr.io/${REPO}-cache" \
      --cache-to   "ghcr.io/${REPO}-cache" \
      -t "ghcr.io/${REPO}:${GITHUB_SHA}" .
```

Rootless podman ships on standard GitHub runners — no privileged Docker-in-Docker service, no daemon socket exposure. Check the runner's actual version before leaning on 5.x-only features (`podman --version`; ubuntu-24.04 images have shipped 4.9-era podman — `--cache-from/--cache-to` is fine there, quadlet-5.x features are not). Registry cache covers RUN layers only (lyra-podman-images rule 11); overall effectiveness is set by Containerfile design (rules 3–4 there).

### 4. Build once, promote by digest, sign what you promote

One build per commit produces one artifact; the digest that passed staging is the digest that ships to prod — never rebuilt per environment, never deployed from a laptop. Tag for humans, promote by digest for machines. Sign with cosign (keyless, OIDC) at build; verify the signature at deploy — an unverified signature is decoration:

```yaml
# job permissions: id-token: write (OIDC identity), packages: write (push signature)
- run: podman push "ghcr.io/${REPO}:${GITHUB_SHA}" --digestfile /tmp/digest
- run: echo "DIGEST=$(cat /tmp/digest)" >> "$GITHUB_ENV"   # sha256:… — THE artifact id from here on
- run: cosign sign --yes "ghcr.io/${REPO}@${DIGEST}"
# at deploy — both flags are required; identity without issuer doesn't verify:
- run: >
    cosign verify
    --certificate-identity-regexp 'https://github.com/org/app/\.github/workflows/.+'
    --certificate-oidc-issuer https://token.actions.githubusercontent.com
    "ghcr.io/${REPO}@${DIGEST}"
```

Emit provenance too: `actions/attest-build-provenance` (verified with `gh attestation verify`) is the zero-infrastructure path to SLSA-style build attestations that lyra-security-supply-chain rule 7 asks consumers to check. Podman hosts can additionally enforce signatures at pull time via `/etc/containers/policy.json` (same rule) — CI verifies what it deploys, the host refuses what CI didn't sign.

### 5. Scan gates on the artifact, not just the source

Image scan (trivy/grype) failing on fixable Critical/High blocks promotion; dependency audit runs in PR; SBOM (syft) is attached to every release artifact. Scanning only at build time misses CVEs published afterwards — rescan what's deployed on a schedule (lyra-security-supply-chain owns the response process).

### 6. Parallelize, path-filter, and cancel superseded runs

Independent jobs run concurrently; matrix builds shard versions/platforms with `fail-fast: true`. Path filters skip jobs a change can't affect (docs-only PRs don't run E2E). `concurrency: { group: ci-${{ github.ref }}, cancel-in-progress: true }` stops burning minutes on obsolete commits — the cheapest speedup in the file, **for CI workflows only**: never put cancel-in-progress on a deployment workflow (killing a half-finished prod deploy is the classic self-inflicted outage; deploys get `cancel-in-progress: false` so runs queue instead). On busy repos, a **merge queue** closes the last race: PRs are tested against the merged result before landing, so two individually-green PRs can't break main together.

### 7. Promotion is one-way with a human gate at prod

Merge to main auto-deploys staging; prod requires a version tag plus approval on a protected environment. Staging is prod-shaped (same artifact, same deploy mechanism — quadlet auto-update or digest rewrite, see lyra-podman-deploy) or it verifies nothing. When the blast radius warrants more than all-at-once, promote progressively: canary a slice (or blue-green the whole) behind health checks, expand on green, auto-revert on red — and feature flags decouple *release* from *deploy* so risky code ships dark and rolls back with a toggle, not a redeploy.

### 8. Rollback is automated, tested, and under five minutes

Rollback = previous digest redeployed, triggered by health-check failure, not by a human paging through dashboards. Drill it in staging monthly; an untested rollback is not a rollback. If rollback takes longer than five minutes, the deployment strategy is wrong — fix the strategy, not the runbook. Database migrations deploy separately from code and stay backward-compatible one release in each direction, or rollback is fiction.

### 9. Keep the loop under ten minutes and attack the slowest stage

PR feedback under five minutes, full deploy under ten. Measure per-stage duration; the offender is usually the test suite (shard it) or the container build (cache it — rules 3 and lyra-podman-images). A pipeline people wait on becomes a pipeline people bypass.

### 10. Flaky gates are quarantined within 24 hours, never retried-to-green

Retry-to-green teaches the team that red is negotiable. Quarantine on first flake, fix the root cause, un-quarantine with a regression test. Track flake rate; anything above 2% auto-quarantines.

### 11. The pipeline emits telemetry

Per-run: stage durations, pass/fail, artifact digest, deploy version, rollback events. Alert on duration regression > 20%, flake rate > 2%, rollback rate > 5% — the leading indicators of a pipeline quietly rotting. What isn't measured degrades politely until it fails loudly.

---

_Part of the [skill collection](../README.md)._
