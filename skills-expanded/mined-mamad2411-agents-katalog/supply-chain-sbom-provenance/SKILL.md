---
name: supply-chain-sbom-provenance
description: Hardens the software supply chain by generating/validating an SBOM (CycloneDX/SPDX via syft/cdxgen), signing artifacts keylessly (cosign + OIDC), emitting SLSA/in-toto build provenance, pinning deps and base images to digests, and enforcing signature/attestation policy at consumption.
when_to_use: User must prove what's in an artifact and that it was built from trusted source — producing/consuming an SBOM, signing containers/releases, adding provenance, raising SLSA level, or hardening CI against poisoned deps (EO 14028, EU CRA). Distinct from dependency-upgrade (bumping versions), secrets-management (handling credentials), and security-review (auditing source code).
---

## When to Use

Reach for this skill when the request is about **proving artifact integrity and origin**, not about the code's behavior:

- "Generate/attach an SBOM to our releases" or "a customer wants a CycloneDX/SPDX SBOM"
- "Sign our container images / release binaries" (cosign, keyless OIDC)
- "Add build provenance / attestations" or "get us to SLSA Level 3"
- "Pin base images to digests, not `:latest`" / "we got hit by a typosquat / dependency-confusion package"
- "Reject unsigned or unattested images at deploy/admission time"
- "Keep scanning what we already shipped for new CVEs against the SBOM"

NOT this skill:
- Bumping a dependency to a newer version / resolving a lockfile → dependency-upgrade
- Storing/rotating the signing key or registry token itself → secrets-management (this skill prefers **keyless**, so there's no key to store)
- Auditing the source for vulnerabilities/logic bugs → security-review (this proves *where the artifact came from*, not whether the code is safe)
- Optimizing the Dockerfile layers/size → dockerfile-optimize
- Writing the deploy/CI YAML in general → cicd-pipeline-author / gitops-deploy-workflow / deploy-release
- Enforcing the policy specifically inside Kubernetes manifests → k8s-manifest-review

## Steps

1. **Inventory inputs, then pick format + tool by ecosystem — do not hand-write an SBOM.** An SBOM must cover **direct + transitive** deps, base image layers, and build tools. Choose:

   | Need | Format | Generator | Why |
   |---|---|---|---|
   | Container/filesystem, broadest ecosystem coverage | **CycloneDX** (`--output cyclonedx-json`) | **syft** | Best default; reads installed packages from the built image, not just manifests |
   | Same, when consumer mandates SPDX (US federal / NTIA) | **SPDX** (`--output spdx-json`) | **syft** | One flag swap; emit both if asked |
   | Source-tree / app deps with rich pURLs + license + VEX | CycloneDX | **cdxgen** | Deeper per-language resolution (npm/maven/gradle/go/pip) |

   Default to **CycloneDX JSON from syft, run against the final built image** (`syft <image>@sha256:... -o cyclonedx-json=sbom.cdx.json`). Generating from source misses what the base image actually ships.

2. **Generate the SBOM in CI as a build step, attach to the release, and validate completeness.** Pin the digest you scanned. A valid SBOM has `bom-ref`/pURL for every component, declared versions, and a license field. Validate, don't trust:

   ```bash
   syft "$IMAGE@$DIGEST" -o cyclonedx-json=sbom.cdx.json
   cyclonedx-cli validate --input-file sbom.cdx.json --fail-on-errors   # schema valid
   jq -e '[.components[] | select(.version==null or .version=="")] | length == 0' sbom.cdx.json  # no unversioned comps
   ```
   Reject the build if validation fails. An SBOM with missing versions/hashes is worse than none — it lies.

3. **Pin and verify every input to a hash, never a moving tag.** This is the actual tamper defense; the SBOM only *describes* it.
   - **Base images:** `FROM node:20.11-bookworm@sha256:<digest>` — never `:latest`, never a bare tag. A tag can be repointed under you.
   - **Deps:** require a lockfile with **integrity hashes** and install in frozen mode: `npm ci` (uses `package-lock.json` `integrity`), `pip install --require-hashes -r requirements.txt`, `go mod verify` + committed `go.sum`, `cargo --locked`. A lockfile without hashes (or `npm install`, which mutates it) is not pinning.
   - **Defend dependency-confusion / typosquatting:** set a **scoped private registry** (`@yourscope:registry=...`) so internal names never resolve to public; **reserve your namespace** on the public registry; pin `registry`/`@scope` in `.npmrc`/`pip.conf`; maintain an **allowlist** and fail CI on any new top-level dep not on it. Confusion attacks beat any signature because you signed the wrong package.

4. **Sign artifacts and the SBOM keylessly with cosign via the CI OIDC identity.** No long-lived key to leak or rotate — the signature is bound to the workflow identity and logged in the Rekor transparency log.

   ```bash
   # cosign 2.x: keyless is the default — no COSIGN_EXPERIMENTAL flag needed
   cosign sign --yes "$IMAGE@$DIGEST"                                  # keyless, OIDC → Fulcio cert → Rekor
   cosign attest --yes --type cyclonedx --predicate sbom.cdx.json "$IMAGE@$DIGEST"   # SBOM as an attestation
   ```
   Sign the **digest**, not the tag. Pushing a tag after signing leaves the signature pointing at a digest a re-tag can bypass.

5. **Emit SLSA build provenance (in-toto attestation) linking artifact → source commit → builder, then harden to raise the level.** Provenance answers "which commit, which builder, what inputs." On GitHub the cheapest path is the official generator/`actions/attest-build-provenance`; verify the chain with cosign:

   ```bash
   cosign verify-attestation --type slsaprovenance \
     --certificate-identity-regexp '^https://github.com/<org>/.+/.github/workflows/.+@refs/' \
     --certificate-oidc-issuer https://token.actions.githubusercontent.com "$IMAGE@$DIGEST"
   ```

   | SLSA Build level | Requirement | How to reach it |
   |---|---|---|
   | L1 | Provenance exists | Generate + attach any provenance |
   | L2 | Signed provenance, hosted build | Keyless cosign + CI-hosted runner (above) |
   | **L3** | Non-falsifiable, isolated build | Use a trusted builder that isolates the run from the steps it builds (reusable trusted workflow); no secrets exposed to user build steps |

   Target **L3** for anything customer-facing; L2 is the floor.

6. **Enforce on consumption — reject unsigned / unattested artifacts at the gate.** Signing nothing-checks is theater. Put a verifying admission/policy controller (e.g. a Sigstore policy controller or `cosign verify` gate in the deploy job) that **denies** images lacking a valid signature *and* required attestations from the *expected* identity:

   ```yaml
   # policy intent: only images signed by OUR workflow, with an SBOM attestation, may deploy
   require:
     signature:
       issuer: https://token.actions.githubusercontent.com
       subjectRegExp: ^https://github.com/<org>/<repo>/.github/workflows/release.yml@refs/tags/.+$
     attestations: [cyclonedx, slsaprovenance]
   ```
   Pin the **identity**, not just "is it signed" — anyone can sign with keyless. Fail closed.

7. **Continuously scan the shipped SBOM for new CVEs.** Vulns are disclosed after you ship. Re-scan the stored SBOM on a schedule (not just at build) so a component clean yesterday flags today:

   ```bash
   osv-scanner scan --sbom sbom.cdx.json --fail-on-vuln    # or: grype sbom:sbom.cdx.json --fail-on high
   ```
   Use a VEX document to suppress not-exploitable findings deliberately — never by lowering the threshold.

## Common Errors

- **Pinning to a tag, not a digest.** `FROM python:3.12` / `cosign sign $IMAGE:latest` — a tag is mutable and can be repointed after you scan/sign. Always `@sha256:<digest>`.
- **SBOM generated from source, attached to a binary built elsewhere.** It won't list the base-image OS packages that actually ship in the artifact. Scan the **built image at its digest**.
- **`npm install` / unfrozen install in CI.** Mutates the lockfile and can pull an unpinned version, voiding the hashes. Use `npm ci` / `--require-hashes` / `--locked` / `--frozen-lockfile`.
- **Signing without verifying identity on the consumer side.** `cosign verify` with no `--certificate-identity*` accepts a signature from *anyone* keyless. Always pin issuer + subject regexp.
- **Treating the SBOM as the tamper control.** The SBOM only *describes*; integrity comes from **digest pins + hashes + signatures**. An accurate SBOM of a poisoned artifact is still poisoned.
- **Lockfile without integrity hashes.** `go.sum` missing, `requirements.txt` without `--hash=`, a `package-lock.json` from `lockfileVersion:1`. Versions alone don't detect content swaps; require hashes.
- **Internal package name resolvable on the public registry.** Classic dependency confusion — the public one wins by higher version. Scope it, reserve the name, and allowlist.
- **Provenance that doesn't bind to a commit/builder.** Provenance with no `materials`/`buildDefinition` source ref proves nothing. It must name the exact commit SHA and builder.
- **Policy in "audit"/warn mode forever.** A controller that logs violations but admits anyway is not enforcement. Flip to **deny / fail-closed** once green.
- **Suppressing scanner findings by raising the severity threshold.** Hides real CVEs. Suppress specific not-exploitable CVEs via VEX with a reason, leave the threshold strict.
- **Storing a long-lived cosign private key in CI secrets.** Defeats the point and creates a rotation burden. Use keyless OIDC; if a key is truly required, that's a secrets-management problem.

## Verify

1. **SBOM completeness:** `cyclonedx-cli validate --fail-on-errors` passes, and `jq` confirms zero components with null/empty `version`. Spot-check that a known base-image OS package (e.g. `glibc`) appears — proves it scanned the image, not just the manifest.
2. **Digest pinning:** `grep -rE 'FROM .+:[^@]+$' Dockerfile*` returns nothing (every `FROM` ends in `@sha256:`); the lockfile carries integrity hashes; frozen-install command is the one used in CI.
3. **Signature + attestation present:** `cosign verify --certificate-identity-regexp ... --certificate-oidc-issuer ...` exits `0` against the **digest**, and `cosign verify-attestation --type cyclonedx ...` returns the SBOM predicate. Tampering with one byte of the image flips both to non-zero.
4. **Provenance binds source+builder:** the SLSA predicate's `buildDefinition`/`materials` names the exact commit SHA and the builder identity; `cosign verify-attestation --type slsaprovenance` exits `0`.
5. **Enforcement is fail-closed:** deploy an image that is unsigned (or signed by a *different* identity) → the gate/admission controller **denies** it; the legitimately-signed image admits. A wrong-identity signature must be rejected, not just an unsigned one.
6. **Confusion defense:** attempt to install an internal package name from the public registry → resolution fails or is blocked by the scoped registry/allowlist; a new unlisted top-level dep fails CI.
7. **Continuous scan wired:** `osv-scanner --sbom ... --fail-on-vuln` (or `grype --fail-on high`) runs on a schedule against the stored SBOM and breaks the job on a new CVE; any suppression is a VEX entry with a reason, not a lowered threshold.

Done = SBOM (CycloneDX/SPDX) validates and is attested to the artifact; every base image and dependency is digest/hash-pinned with confusion defenses; the artifact and SBOM are keyless-signed with SLSA L2+ provenance binding source commit and builder; the consumption gate fails closed against unsigned and wrong-identity artifacts; and a scheduled scanner re-checks the SBOM for new CVEs.
