---
name: release-security
description: "Image gate runner: scan the built digest, SBOM, sign and attest, verify by exact identity; cosign ≥ 3.1.3."
kind: skill
pack: devops
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: release-security

## Premise

A built container image is a **supply-chain artifact**, not just a deploy blob. The build→registry gate has five jobs: **scan** the image for OS and library CVEs, **generate an SBOM**, **sign** the digest, **attest provenance**, and **verify** — by the exact workflow and ref that may build it — before anything deploys it. This skill is the runner that executes them.

It runs in two modes:
- **CI mode** — wired into the release job by `/dockerize` and `/add-ci`: scan, SBOM, sign, attest, verify. Signing and pushing happen here, in the user's pipeline, never from an audit.
- **Audit mode** — called by `release-integrity-scan` §5 (and by the security pack's `@security-auditor` A03 row) with a digest that already exists. **Read-only:** floors, scan, verify (positive and negative), digest reads. It never signs, attests, tags or pushes.

**Every finding cites the image as `<repo>@<digest>` + the CVE id (or the missing gate, or the identity a verify accepts) + the fix.** "Image looks insecure" without a cited CVE or digest is not a finding. Tool floors come from `THR-SCANNER-FLOOR` (`templates/governance/thresholds.json`); the oracles are [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § DevOps V223 (digest continuity) and V224 (verify negative test); settled questions are [`precedents/devops.md`](../../../../snippets/precedents/devops.md) § 19, § 21 and § 41.

## What this covers vs siblings

- `release-integrity-scan` (this pack) — **detects** a missing or hollow gate in the repo's CI (§5) and hands this runner the digest. This skill **executes** the gate on that digest.
- `deps-audit` (security pack) — application dependencies from the lockfile. This skill — the image's OS packages and baked libraries, which a lockfile scan cannot see.
- `container-build-scan` (this pack) — the **Dockerfile** and the built image's config (user, PID 1, layers). This skill — the image's **CVEs, SBOM, signature and provenance**.
- `admission-policy` (infrastructure pack) — **enforces** verify at the cluster. This skill proves the verify line would reject the wrong signer.

## Prerequisites — floors first (`THR-SCANNER-FLOOR`)

The scanners and the signer run with the pipeline's registry credentials, so they are supply chain too: on 2026-03-19, 76 of 77 `aquasecurity/trivy-action` tags were force-moved to a credential stealer, and cosign before 3.1.3 has a verification bypass via a public key in a legacy bundle (GHSA-fx35-mq7g-6g98, fixed 2026-08-06).

| Tool | Floor and pin | Read it with |
|---|---|---|
| cosign | **≥ 3.1.3** (`sigstore/cosign-installer` with `cosign-release: 'v3.1.3'` or later) | `cosign version` |
| trivy | version **and** digest: `aquasec/trivy:0.75.0@sha256:<digest>`; the action pinned by SHA | `crane digest aquasec/trivy:0.75.0` |
| syft · grype | version and digest (syft v1.54.1 in the 2026-10-10 research pass) | `syft version` |
| keyless signing | OIDC (Fulcio + Rekor) over a stored key: no key to leak; the identity is the CI workflow | — |

A tool below its floor, or missing, makes every row that depends on it `NOT-RUN (<tool> <version> below floor <floor>)` — never PASS (precedents § 41).

## Procedure

0. **Pin the subject.** Work on `<repo>@<digest>`, never a tag. In CI that is `steps.build.outputs.digest` from the one build that pushes; in audit mode it is the digest the caller passes. A tag can move between this step and the deploy.
1. **Scan — before the image is pullable, or gate the deploy on it.** Either push by digest to a staging repository the deploy cannot pull, scan, then promote that same digest; or scan the pushed digest and make the deploy job `needs:` the scan, and say which one you did. Never scan a `load: true` image and push a second build: that pushes an image nobody scanned, and `load: true` produces no attestations [R, Docker docs read 2026-10-10].
   ```bash
   trivy image --severity HIGH,CRITICAL --ignore-unfixed --exit-code 1 <repo>@<digest>
   ```
   `--ignore-unfixed` is the right default, and it means a PASS is "no *fixable* High/Critical" (precedents § 21): say which you ran. Triage by CVSS **plus** EPSS and CISA KEV.
2. **SBOM — generate, then attest.** For an audit, read every layer: syft's default `squashed` scope hides a package deleted in a later layer.
   ```bash
   syft scan <repo>@<digest> --scope all-layers -o cyclonedx-json=sbom.cdx.json
   cosign attest --yes --type cyclonedx --predicate sbom.cdx.json <repo>@<digest>
   ```
   Or `actions/attest` v4 with `sbom-path` (`actions/attest-sbom` is being deprecated in its favour). `cosign attach sbom` is deprecated — cosign declares `attach` "will be removed in v4.0.0" — and weaker: an attached SBOM is an unsigned blob anyone with push access can replace; an attestation is signed by the build identity.
3. **Sign the digest.** For a multi-arch index, sign every platform manifest too:
   ```bash
   cosign sign --yes --recursive <repo>@<digest>     # keyless: the CI OIDC identity → Fulcio cert, Rekor entry
   ```
4. **Provenance — SLSA v1.** `actions/attest` v4 (`actions/attest-build-provenance` v4 is now a thin wrapper over it), or `cosign attest --type slsaprovenance1 --predicate provenance.json <repo>@<digest>`. `--type slsaprovenance` is the v0.2 predicate. docker/build-push-action's own provenance defaults to SLSA v0.2 (`version=v1` opts in), `mode=min` on private repos and `mode=max` on public ones; `mode=max` records build-arg **values**, so a secret passed as a build arg is published in the attestation — that secret is the security pack's (`iac-scan` grep 2b), and the fix is `--mount=type=secret`.
5. **Verify by exact identity — and prove it rejects.**
   ```bash
   cosign verify --certificate-identity 'https://github.com/<o>/<r>/.github/workflows/<release>.yml@refs/heads/main' \
     --certificate-oidc-issuer https://token.actions.githubusercontent.com <repo>@<digest>
   gh attestation verify oci://<repo>@<digest> --repo <o>/<r> \
     --signer-workflow <o>/<r>/.github/workflows/<release>.yml --source-ref refs/heads/main --deny-self-hosted-runners
   ```
   A valid signature or attestation proves only that *some* workflow built the artifact: TanStack's npm packages (postmortem 2026-05-11) carried valid SLSA provenance from a poisoned build. So pin the workflow **and** the ref. `--certificate-identity-regexp '.*'`, an org-wide regexp, a missing issuer, `--insecure-ignore-tlog`, `gh attestation verify --owner <org>` alone (any repository of the org), a tag instead of a digest and `|| true` each make the verify accept what it should refuse. **Negative test (V224):** in a sandbox repo, sign a scratch image from another workflow file or another ref, push it to a scratch registry (`registry:2` on localhost), and run the project's verify line against it — it must exit non-zero. Never the user's registry.
6. **Digest equality (V223).** The digest scanned = the digest signed = the digest pushed = the digest each environment runs (`crane digest`; `kubectl get deploy -o jsonpath='{..image}' --kubeconfig=<scratch>` against a throwaway cluster, or the platform API).

Enforce at admission with a policy controller (Kyverno `verifyImages`, Sigstore policy-controller) pinned to the same identity — the infrastructure pack's `admission-policy`. A signer on cosign v3 (Sigstore bundles, OCI 1.1 referrers) with an admission verifier that cannot read them blocks every deploy or, left in audit mode, passes everything (CT-R07): upgrade the verifier with the signer.

## The runner contract (what `release-integrity-scan` §5 calls)

**Input:** the artifact `<repo>@<digest>`; the expected identity (`https://github.com/<o>/<r>/.github/workflows/<file>@<ref>`) and issuer; the platforms of the index; `THR-SCANNER-FLOOR`. **Output:** exactly these rows, each with its command and exit code, or `NOT-RUN (<reason>)`:

```
FLOOR    cosign=3.1.3 trivy=0.75.0@sha256:… syft=1.54.1                  (below floor → dependent rows NOT-RUN)
SCAN     <repo>@<digest> result=PASS|FAIL(n CRITICAL, m HIGH) mode=ignore-unfixed|all
SBOM     attested|attached|none  scope=all-layers|squashed
SIGN     signed=yes|no  platforms=<k>/<n> signed
VERIFY+  identity=<exact> issuer=<url>  result=pass|fail
VERIFY-  signer=<other workflow or ref>  result=REJECTED|ACCEPTED          (ACCEPTED = the verify verifies nothing, V224)
DIGEST   built=<d> scanned=<d> pushed=<d> deployed=<d>  equal=yes|no       (V223)
```

A registry it cannot reach, a credential it does not have, or a tool that errored is `NOT-RUN`, and the caller marks §5 `blocked`, never `checked`. Audit mode reads `SIGN` from the registry's referrers (`oras discover -o tree <repo>@<digest>`) and nothing else.

## Output

```
release-security — ghcr.io/acme/api@sha256:4f1c…   (mode: audit · scanner: trivy 0.75.0@sha256 · cosign 3.1.3)

FLOOR:    OK
CVE scan: FAIL — 1 CRITICAL, 2 HIGH (fixes available; --ignore-unfixed)
  - CVE-2025-XXXX (CRITICAL, EPSS 0.72, KEV=yes) openssl 3.0.x → 3.0.y  [BLOCKER]
SBOM:     attached, not attested (cosign attach) — replace with cosign attest / actions/attest
Sign:     index signed; 1 of 2 platform manifests unsigned (no --recursive)
Verify+:  pass  (identity …/release.yml@refs/heads/main, issuer token.actions.githubusercontent.com)
Verify-:  REJECTED  (a scratch image signed by …/preview-build.yml in the sandbox) — the verify pins its signer
Digest:   built = scanned = pushed; deployed: NOT-RUN (no cluster access)

Verdict: BLOCK — fix the CRITICAL and sign every platform before release.
```

## False positives / gotchas

- **Unfixed base-image CVEs** shouldn't block forever: `--ignore-unfixed` plus a slimmer base (distroless, Chainguard), with the accepted risk named — never suppress-and-forget.
- **Sign the digest, not the tag.** Signing `image:latest` signs whatever it points at today.
- **Signing ≠ verifying, and verifying ≠ pinning.** A signed-but-unverified pipeline is theatre; a verify that accepts any workflow in the org is theatre with a log line.
- **A per-architecture manifest list is one digest** (precedents § 19): promote the index digest; sign with `--recursive` so a per-platform pull also verifies.
- **`deps-audit` overlap** — don't re-report the app-lockfile CVEs here; this owns the image's OS and baked-library layer.

## When to run

- **CI mode:** every release or tag build. Scan the built digest **before** the push that makes it pullable — or scan the pushed digest and gate the deploy on the scan, said plainly in the workflow. Wired by `/dockerize` (release step) and `/add-ci` (the image job).
- **Audit mode:** when `release-integrity-scan` §5 or `@security-auditor` A03 hands it a digest; on a base-image bump or a new advisory against a running image.

## Halt conditions

- Halt on any CVE finding without the cited `<CVE-id>` + severity + fix path.
- Do NOT sign an image that failed the CVE gate — you would be attesting to a known-vulnerable artifact.
- Do NOT report PASS with an unfixed CRITICAL and no explicit, EPSS/KEV-informed risk acceptance.
- Do NOT claim "signed/verified" unless `cosign verify` (or `gh attestation verify`) actually ran **with an exact identity and issuer**, and say whether the negative test ran.
- Do NOT run a tool below `THR-SCANNER-FLOOR` and report its result: the row is `NOT-RUN`.
- In audit mode, never sign, attest, tag, push or delete on the user's registry; V224's negative test uses a sandbox repo and a scratch registry.

## Related

- `release-integrity-scan` (this pack) — the detector whose §5 calls this runner, and whose §4 owns "what ships is not what was tested".
- `/dockerize` / `/add-ci` — wire this as the release gate; `container-build-scan` — the Dockerfile half.
- `@ci-reviewer` / `@deployment-engineer` — judge the pipeline's gate (pinned actions, OIDC, digest hand-off).
- `security/agents/security-auditor.md` — its OWASP **A03 Software Supply Chain** check dispatches HERE; `security/skills/deps-audit/SKILL.md` — the manifest counterpart.
- `infrastructure` pack `admission-policy` — enforces verify-at-deploy with the same identity.
