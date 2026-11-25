---
name: slsa
description: >-
  SLSA v1.2 supply-chain levels, build provenance and VSA verification. Produce
  and verify SLSA Provenance v1 (https://slsa.dev/provenance/v1) and Verification
  Summary Attestations (https://slsa.dev/verification_summary/v1), assign Build
  track L0-L3 and Source track L1-L4 requirements to producers, build platforms
  and source control systems, and check artifacts against roots of trust and
  expectations. Use when adding provenance to a CI/CD pipeline, claiming or
  requiring "SLSA Build L3", reviewing a build platform for hosted and isolated
  builds, writing a verifier for builder.id, buildType, externalParameters and
  resolvedDependencies, issuing Source VSAs, threat-modelling supply chain attacks
  A-I, or migrating provenance v0.2 to v1. Targets SLSA v1.2 with Provenance v1
  and VSA v1; upgrades from SLSA v1.1, v1.0 and v0.1 and from Provenance and VSA
  v0.2 and v0.1; tracks the SLSA working draft (Build Environment and Dependency
  tracks).
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# SLSA

SLSA (Supply-chain Levels for Software Artifacts) is an OpenSSF specification that sorts supply chain security into tracks of increasing levels, and defines in-toto attestation formats for build provenance and verification summaries. This skill pins SLSA v1.2 and produces provenance, platform designs, verifiers and level claims that meet its requirements.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources), with the section it cites. SLSA pages have no section numbers, so citations name the page and heading. When a rule and the pinned source disagree, the source wins. When the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role:
  - software producer;
  - build platform implementer;
  - source control system (SCS) or organization on the Source track;
  - package ecosystem or registry;
  - consumer or verifier;
  - VSA issuer.
- Target level: the Build level (L0–L3) and, if relevant, the Source level (L1–L4) to reach or require.
- Artifacts: what is built, where it is published, and the package ecosystem's provenance conventions.
- Target version:
  - SLSA v1.2 (current, the default), with SLSA Provenance v1 and SLSA VSA v1, both current.
  - SLSA v1.1, SLSA v1.0 and SLSA v0.1 are legacy, as are SLSA Provenance v0.2, SLSA Provenance v0.1, SLSA VSA v0.2 and SLSA VSA v0.1: read and upgrade them, never author them.
  - The SLSA working draft is a preview (posture: track): claim nothing from it.
  - See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill or when a rule looks out of date, re-read https://slsa.dev/spec/ and the version index for a new current version, then each What's new page and every URL in [Sources](#sources), and update the pins.

## Invariants

1. **Levels are per track and versioned.** Claim `SLSA Build L<n>` or `SLSA Source L<n>`, adding `(v1.2)` for precision. Levels are not transitive to dependencies (Specification Stages, Versioning; FAQ).
2. **The producer picks a capable platform and stays consistent.** It MUST choose a platform capable of the target Build level, build consistently so verifiers can form expectations, and distribute provenance (Build Requirements, Producer).
3. **Provenance identifies the output by digest.** It MUST describe how the output was produced, in a format the ecosystem or consumer accepts. SLSA Provenance is RECOMMENDED (Build Requirements, Provenance Exists).
4. **At Build L2 the control plane generates and signs provenance.** It MUST NOT come from a tenant; only `subject` and fields not required at L2 MAY come from the tenant, and consumers MUST be able to validate authenticity (Build Requirements, Provenance is Authentic).
5. **At Build L3 provenance is unforgeable and builds are isolated.**
   - Signing secrets MUST NOT be reachable from user-defined steps, and `externalParameters` MUST be complete.
   - Each build MUST get an ephemeral environment and MUST NOT influence another build or its cache (Build Requirements, Provenance is Unforgeable and Isolated).
6. **Use the exact predicate type.** `predicateType` is `https://slsa.dev/provenance/v1`, never the browser URL. Consumers MUST ignore unknown fields and treat unset, null and empty the same (Build: Provenance, Parsing rules).
7. **`builder.id` is the trust base.**
   - Each mode with different security MUST have its own `builder.id`.
   - Consumers MUST accept only specific signer–builder pairs (Build: Provenance, Builder).
8. **Verify signature, subject, type, builder, then expectations.** Check the envelope signature, the subject digest, `predicateType` and the roots-of-trust Build level. Then compare the builder, source repository, `buildType` and `externalParameters` with expectations, and reject unknown parameters (Verifying Artifacts, Steps 1–2).
9. **VSA consumers run the mandatory checks.** Verification MUST check signature, `subject`, `predicateType`, `verifier`, `resourceUri`, `verificationResult` `PASSED` and `verifiedLevels`. `verifiedLevels` MUST NOT hold two levels of one track, and custom values MUST NOT start with `SLSA_` (Verification Summary, How to verify; Fields; SlsaResult).
10. **Source levels need SCS evidence.**
    - The SCS MUST issue a Source VSA for every revision at Source L1+, and from L2 base it on contemporaneous source provenance.
    - Branches move only to descendants of their current revision.
    - Source L4 needs two trusted persons per change (Source Requirements).
11. **Build L3 does not cover a compromised platform.** Verifiers SHOULD carefully choose which builders and verifiers enter their roots of trust (Verifying Artifacts, Step 1; Verification Summary, How to verify).

## Workflow

1. **Pick the version.** Target SLSA v1.2 with Provenance v1 and VSA v1, and note any legacy documents to upgrade.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target is recorded, and it is not a legacy or draft line.
2. **Choose levels and assign requirements.** Map each Build (and Source) requirement to the producer, build platform, SCS or organization.
   -> [`references/levels-and-tracks.md`](references/levels-and-tracks.md)
   ✓ Every requirement for the target level has an owner and a control.
3. **Generate provenance.** Model `buildType`, keep `externalParameters` minimal and complete, and record `resolvedDependencies` with digests. Generate and sign in the control plane.
   -> [`references/provenance.md`](references/provenance.md)
   ✓ An example statement has the required fields for the level, and no tenant step can change any field other than `subject`.
4. **Distribute provenance.** Publish it with the artifact, in at least one place and preferably more, as immutable per-artifact attestations.
   -> [`references/provenance.md`](references/provenance.md#distributing-provenance)
   ✓ A consumer can find the provenance from the artifact alone.
5. **Verify.** Configure roots of trust and form expectations by trust on first use, producer definition or source definition. Then implement Steps 1–3 at upload, at download, or in a monitor.
   -> [`references/verification.md`](references/verification.md)
   ✓ An artifact from a fork, an unexpected builder or an extra parameter is rejected.
6. **Issue or check VSAs.** Summarize verification results, and Source levels for revisions, as `https://slsa.dev/verification_summary/v1`.
   -> [`references/verification.md`](references/verification.md#verification-summary-attestation)
   ✓ The VSA passes all seven mandatory checks for its intended consumer.
7. **Review the threat model.** Go through threats A–I and the dependency, availability and verification threats, and note which are out of scope.
   -> [`references/threats.md`](references/threats.md)
   ✓ Every threat has a level, a verification step, or a documented gap.
8. **Upgrade** (only when asked). Follow the upgrade section for each step from the source version or predicate to the target.
   -> [`references/versions.md`](references/versions.md)
   ✓ The upgraded document uses the current `predicateType`, validates, and still matches the same expectations.

## Verify before done

- [ ] `predicateType` is `https://slsa.dev/provenance/v1` (or `…/verification_summary/v1`) and `_type` is `https://in-toto.io/Statement/v1`.
- [ ] Every `subject` has a strong digest such as `sha256` that matches the artifact.
- [ ] `buildDefinition.buildType`, `buildDefinition.externalParameters` and `runDetails.builder.id` are present.
- [ ] For a Build L2+ claim, the provenance is signed by a key only the control plane holds, and the builds are hosted.
- [ ] For a Build L3 claim, builds are isolated and ephemeral, caches cannot be poisoned, and `externalParameters` is complete.
- [ ] The verifier maps (key, `builder.id`) to a maximum level and rejects unknown `externalParameters`.
- [ ] VSAs carry `verifier.id`, `resourceUri`, `policy.uri`, `verificationResult` and one level per track.
- [ ] No Build Environment or Dependency level, and no `https://slsa.dev/dependency/v1` predicate, is emitted.

## Reference index

- **`references/versions.md`**: every SLSA version and predicate version, its status, what changed, upgrade steps, and the working draft. Load for steps 1 and 8.
- **`references/levels-and-tracks.md`**: Build L0–L3 and Source L1–L4, the producer, build platform, organization and SCS requirements, platform assessment, and verified properties.
- **`references/provenance.md`**: the Provenance v1 model, schema and field rules, extension fields, distribution, and migration from v0.2.
- **`references/verification.md`**: roots of trust, expectations, verification steps and architecture, the VSA format and checks, and source revision verification.
- **`references/threats.md`**: threats A–I, dependency, availability and verification threats, and which level or check mitigates each.

## Related skills

- `in-toto`, for the attestation framework, DSSE envelopes and other predicates: `npx skills add ScaleDockHQ/scaledock-skills --skill in-toto`
- `cyclonedx`, for SBOMs and attestations next to provenance: `npx skills add ScaleDockHQ/scaledock-skills --skill cyclonedx`
- `spdx`, for SBOMs and SPDX download locations: `npx skills add ScaleDockHQ/scaledock-skills --skill spdx`
- `openssf-baseline`, for OpenSSF project security baselines: `npx skills add ScaleDockHQ/scaledock-skills --skill openssf-baseline`
- `scitt`, for transparency services that register signed statements: `npx skills add ScaleDockHQ/scaledock-skills --skill scitt`

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [SLSA specification (version index)](https://slsa.dev/spec/): Approved, v1.2 marked current, checked 2026-10-05.
- [SLSA Specification Stages and Versioning](https://slsa.dev/spec-stages): Site page, checked 2026-10-05.
- [SLSA v1.2](https://slsa.dev/spec/v1.2/): Approved, v1.2 (tag `v1.2`, branch `releases/v1.2` at ae7fc76), checked 2026-10-05.
- [SLSA v1.2 What's new](https://slsa.dev/spec/v1.2/whats-new): Approved, v1.2, checked 2026-10-05.
- [SLSA v1.2 Tracks](https://slsa.dev/spec/v1.2/tracks): Approved, v1.2, checked 2026-10-05.
- [SLSA v1.2 Build: Track Basics](https://slsa.dev/spec/v1.2/build-track-basics): Approved, v1.2, checked 2026-10-05.
- [SLSA v1.2 Build: Requirements for producing artifacts](https://slsa.dev/spec/v1.2/build-requirements): Approved, v1.2, checked 2026-10-05.
- [SLSA v1.2 Build: Provenance](https://slsa.dev/spec/v1.2/build-provenance): Approved, v1.2 (predicate `https://slsa.dev/provenance/v1`), checked 2026-10-05.
- [SLSA Provenance v1 (predicate URI)](https://slsa.dev/provenance/v1): Approved, redirects to the v1.1 page as of 2026-10-05, checked 2026-10-05.
- [SLSA v1.2 Build: Distributing provenance](https://slsa.dev/spec/v1.2/distributing-provenance): Approved, v1.2, checked 2026-10-05.
- [SLSA v1.2 Build: Verifying artifacts](https://slsa.dev/spec/v1.2/verifying-artifacts): Approved, v1.2, checked 2026-10-05.
- [SLSA v1.2 Build: Assessing build platforms](https://slsa.dev/spec/v1.2/assessing-build-platforms): Approved, v1.2, checked 2026-10-05.
- [SLSA v1.2 Source: Requirements for producing source](https://slsa.dev/spec/v1.2/source-requirements): Approved, v1.2, checked 2026-10-05.
- [SLSA v1.2 Source: Verifying source](https://slsa.dev/spec/v1.2/verifying-source): Approved, v1.2, checked 2026-10-05.
- [SLSA v1.2 Threats & mitigations](https://slsa.dev/spec/v1.2/threats): Approved, v1.2, checked 2026-10-05.
- [SLSA v1.2 Verification Summary Attestation](https://slsa.dev/spec/v1.2/verification_summary): Approved, v1.2 (predicate `https://slsa.dev/verification_summary/v1`), checked 2026-10-05.
- [SLSA v1.2 Verified Properties](https://slsa.dev/spec/v1.2/verified-properties): Approved, v1.2, checked 2026-10-05.
- [SLSA v1.2 Software attestations](https://slsa.dev/spec/v1.2/attestation-model): Approved, v1.2, checked 2026-10-05.
- [SLSA v1.2 FAQ](https://slsa.dev/spec/v1.2/faq): Approved, v1.2, checked 2026-10-05.
- [SLSA v1.1](https://slsa.dev/spec/v1.1/): Retired, v1.1 (tag `v1.1`), checked 2026-10-05.
- [SLSA v1.1 What's new](https://slsa.dev/spec/v1.1/whats-new): Retired, v1.1, checked 2026-10-05.
- [SLSA v1.0](https://slsa.dev/spec/v1.0/): Retired, v1.0 (tag `v1.0.0`), checked 2026-10-05.
- [SLSA v1.0 What's new](https://slsa.dev/spec/v1.0/whats-new): Retired, v1.0, checked 2026-10-05.
- [SLSA v0.1](https://slsa.dev/spec/v0.1/): Approved (superseded), v0.1 (tag `v0.1`), checked 2026-10-05.
- [SLSA v0.1 Security levels](https://slsa.dev/spec/v0.1/levels): Approved (superseded), v0.1, checked 2026-10-05.
- [SLSA Provenance v0.2](https://slsa.dev/provenance/v0.2): Approved (hidden version), v0.2, checked 2026-10-05.
- [SLSA Working Draft](https://slsa.dev/spec/draft/): Draft, `main` at 82b296d (2026-09-29), checked 2026-10-05. Draft posture: track.
- [SLSA Working Draft: Build Environment track](https://slsa.dev/spec/draft/build-env-track-basics): Draft, `main` at 82b296d, checked 2026-10-05. Draft posture: track.
- [SLSA Working Draft: Dependency Track](https://slsa.dev/spec/draft/dependency-track): Draft, `main` at 82b296d, checked 2026-10-05. Draft posture: track.
- [slsa-framework/slsa repository](https://github.com/slsa-framework/slsa): tags `v1.2`, `v1.1`, `v1.0.0`, `v0.1`, no GitHub Releases; `www/_data/versions.yml` at 82b296d, checked 2026-10-05.
- [in-toto Attestation Framework specification](https://github.com/in-toto/attestation/blob/main/spec/v1/README.md): Released, v1.2 (release v1.2.0, 2026-03-18), checked 2026-10-05.
- [in-toto Statement layer](https://github.com/in-toto/attestation/blob/main/spec/v1/statement.md): Released, v1.2.0, checked 2026-10-05.
- [in-toto Validation model](https://github.com/in-toto/attestation/blob/main/docs/validation.md): Released, v1.2.0, checked 2026-10-05.
