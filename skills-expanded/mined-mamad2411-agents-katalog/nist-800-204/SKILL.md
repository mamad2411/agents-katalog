---
name: nist-800-204
description: >-
  NIST SP 800-204: secure microservices-based applications and their service-to-service communication. Covers SP 800-204, SP 800-204A, SP 800-204B, SP 800-204C, SP 800-204D. Use when securing microservices. Triggers: SP 800-204.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# NIST SP 800-204

The NIST SP 800-204 series on microservices security: SP 800-204 security strategies (MS-SS-1 to MS-SS-13), SP 800-204A service mesh recommendations (SM-DR1 to SM-DR23), SP 800-204B ABAC for service meshes, SP 800-204C DevSecOps and SP 800-204D software supply chain security in CI/CD pipelines.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when securing microservices.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: architect or platform team securing a microservices application, its service mesh or its CI/CD pipelines.
- Target version: SP 800-204 (default); SP 800-204A (default); SP 800-204B (default); SP 800-204C (default); SP 800-204D (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **MS-SS-1.** "Authentication to microservices APIs that have access to sensitive data should not be done simply by using API keys."
2. **MS-SS-4.** "Client to API gateway as well as Service to Service communication should take place after mutual authentication and be encrypted (e.g., using mutual TLS (mTLS) protocol)."
3. **SM-DR2.** "The set of services that a service proxy can reach must be limited."
4. **SM-DR15.** "Certificates used to identify microservices should not be signing certificates."
5. **§ 5.1.1.** "The attestations must be cryptographically signed using a secure key."

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in [`references/requirements.md`](references/requirements.md) and implement each one that applies to the role.
   -> [`references/requirements.md`](references/requirements.md)
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the heading it came from.
3. **Upgrade** (only when asked). Follow the upgrade section from the source line to the target.
   -> [`references/versions.md`](references/versions.md)
   ✓ The result cites the target line and no longer depends on a requirement that only the old line stated.

## Verify before done

- [ ] The artifact cites the target line's revision from [Sources](#sources).
- [ ] Every applicable quoted requirement in [`references/requirements.md`](references/requirements.md) holds.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [SP 800-204](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-204.pdf): NIST SP, SP 800-204, fetched 2026-10-06 (NIST SP, 2026-10-06), checked 2026-10-06.
- [SP 800-204A](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-204A.pdf): NIST SP, SP 800-204A, fetched 2026-10-06 (NIST SP, 2026-10-06), checked 2026-10-06.
- [SP 800-204B](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-204B.pdf): NIST SP, SP 800-204B, fetched 2026-10-06 (NIST SP, 2026-10-06), checked 2026-10-06.
- [SP 800-204C](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-204C.pdf): NIST SP, SP 800-204C, fetched 2026-10-06 (NIST SP, 2026-10-06), checked 2026-10-06.
- [SP 800-204D](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-204D.pdf): NIST SP, SP 800-204D, fetched 2026-10-06 (NIST SP, 2026-10-06), checked 2026-10-06.
