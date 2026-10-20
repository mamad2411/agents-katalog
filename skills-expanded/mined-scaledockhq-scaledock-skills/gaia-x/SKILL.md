---
name: gaia-x
description: >-
  Gaia-X Trust Framework: issue, sign and verify Gaia-X Credentials (W3C VC 2.0 as VC-JWT with did:web and x5c) and meet Gaia-X Compliance through the Digital Clearing House. Covers Architecture Document 3.1, ICAM 25.11 and Compliance Document 4.0.0. Use when building a Gaia-X participant, service offering or data space connector, producing Gaia-X Credentials, or checking them against SHACL shapes and Trust Anchors. Triggers: Gaia-X, GXDCH, Gaia-X Compliance, Gaia-X Credential, Trust Anchor, Gaia-X Label, ICAM.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Gaia-X

Gaia-X, the European association's trust framework for data spaces: the Architecture Document (technical compatibility), the Identity, Credentials and Access Management (ICAM) specification (Gaia-X Credential format and digital identities), and the Compliance Document (criteria, Trust Anchors and conformity assessment). Each is published from its Gaia-X GitLab repository at a release tag.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: Participant or Provider issuing Gaia-X Credentials, Verifier or Compliance Engine checking them, or Trust Service Provider or Notary.
- Target version: Architecture Document 3.1 (current); Architecture Document 25.11 (legacy); ICAM 25.11 (current); Compliance Document 4.0.0 (current); Compliance Document 3.1.0 (legacy). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **Verifying Gaia-X Credentials.** "To ensure a Gaia-X Credential's integrity and authenticity, its claims MUST be cryptographically signed by the Issuer to prevent tampering and enable verification of the origin of the claims."
2. **Verifying Gaia-X Credentials.** "The publicKeyJwk property MUST include either the RFC7517 x5c (X.509 Certificate Chain) parameter or RFC7517 x5u (X.509 URL) parameter."
3. **Verifying Gaia-X Credentials.** "To ensure the correct cryptographic tools are used with the public key, the alg property MUST be specified, and the value must comply with the JSON Web Algorithms RFC7518 alg."
4. **Gaia-X Schema.** "To ensure compliance with Gaia-X and/or specific ecosystem extensions, this data graph must be validated against the given SHACL shapes graph according to the SHACL specification."
5. **Identifiers.** "The `@id` MUST be present and unique for a given `issuer`."
6. **Header.** "The VC-JWT header MUST contain the following fields:"
7. **VC-JWT Payload.** "The `vc` and `vp` payload claims MUST NOT be present."
8. **Issuer Requirements.** "The value of the `issuer` property MUST be a resolvable URI."
9. **DID Resolution.** "If the credential relies on an X.509 certificate chain, the verifier MUST validate that the chain terminates at a root certificate authority recognised by the ecosystem’s Registry."
10. **Self-Sovereign Identity (SSI) Implementation.** "When implementing SSI with verifiable credentials, all claims MUST be bound to a single keypair rather than multiple keypairs to maintain cryptographic integrity and clear accountability."
11. **Trust Service Provider.** "The Trust Service Providers (TSP) accredited by Gaia-X must be entities issuing cryptographic material based on documented Know Your Business/Know Your Customer [(KYB/KYC)](https://en.wikipedia.org/wiki/Know_your_customer) processes."
12. **Inheritance mechanism.** "To achieve Gaia-X Standard Compliance each service listed as dependency must also meet the criteria for Gaia-X Standard Compliance."

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in [`references/requirements.md`](references/requirements.md) and implement each one that applies to the role.
   -> [`references/requirements.md`](references/requirements.md)
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the section it came from.
3. **Upgrade** (only when asked). Follow the upgrade section from the source line to the target.
   -> [`references/versions.md`](references/versions.md)
   ✓ The result cites the target line and no longer depends on a requirement that only the old line stated.

## Verify before done

- [ ] The artifact cites the target line's revision from [Sources](#sources).
- [ ] Every applicable quoted requirement in [`references/requirements.md`](references/requirements.md) holds.
- [ ] Every Gaia-X Credential validates against the Gaia-X SHACL shapes and passes a GXDCH compliance check for the targeted Compliance Document release.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `vc-data-model`, `did`, `jwt`, `shacl`, `eidas`, `eclipse-dataspace-protocol`, `odrl`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Gaia-X Architecture Document: technical compatibility specifications](https://gitlab.com/gaia-x/technical-committee/architecture-working-group/architecture-document/-/raw/3.1/docs/gaia-x_technical_compatibility_specifications.md): Gaia-X Architecture Document, tag 3.1, 2026-07-06, checked 2026-10-06.
- [Gaia-X ICAM: Gaia-X Credentials](https://gitlab.com/gaia-x/technical-committee/identity-credentials-and-access-management-working-group/icam/-/raw/25.11/docs/gaia-x_credentials.md): Gaia-X ICAM specification, tag 25.11, 2025-11-11, checked 2026-10-06.
- [Gaia-X ICAM: Digital identities](https://gitlab.com/gaia-x/technical-committee/identity-credentials-and-access-management-working-group/icam/-/raw/25.11/docs/digital_identities.md): Gaia-X ICAM specification, tag 25.11, 2025-11-11, checked 2026-10-06.
- [Gaia-X Compliance Document: Trust Anchors](https://gitlab.com/gaia-x/policy-rules-committee/compliance-document/-/raw/4.0.0/docs/Gaia-X_Trust_Anchors.md): Gaia-X Compliance Document, tag 4.0.0, 2026-09-28, checked 2026-10-06.
- [Gaia-X Compliance Document: overarching rules](https://gitlab.com/gaia-x/policy-rules-committee/compliance-document/-/raw/4.0.0/docs/overarching_rules.md): Gaia-X Compliance Document, tag 4.0.0, 2026-09-28, checked 2026-10-06.
