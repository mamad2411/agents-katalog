---
name: did-methods
description: >-
  DID methods: create and resolve did:web, did:key, did:jwk and did:webvh identifiers. Covers did:web, did:key, did:jwk, did:webvh. Use when resolving did:web, did:key, did:jwk, or did:webvh. Triggers: did:web, did:key, did:jwk, did:webvh.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# DID methods

Four DID methods read from their source repositories: did:web and did:key from the W3C Credentials Community Group, did:jwk from its author's repository, and did:webvh v1.0 from the Decentralized Identity Foundation. Each defines the identifier syntax, how a resolver turns the identifier into a DID document, and which operations the method supports.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: DID controller publishing a DID, DID resolver, or verifier consuming DID documents.
- Target version: did:web (current); did:key (current); did:jwk (current); did:webvh (current). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **did:web Method-specific identifier.** "The method specific identifier MUST match the common name used in the SSL/TLS certificate, and it MUST NOT include IP addresses."
2. **did:web Read (Resolve).** "Verify that the ID of the resolved DID document matches the Web DID being resolved."
3. **did:key Document Creation Algorithm.** "The scheme MUST be the value `did`. The method MUST be the value `key`. The version MUST be convertible to a positive integer value. The multibaseValue MUST be a string and begin with the letter `z`. If any of these requirements fail, an `invalidDid` error MUST be raised."
4. **did:key Update.** "This DID Method does not support updating the DID Document."
5. **did:jwk Security.** "Only JWKs containing public key material may be used, a JWK for a private key must never be used and must be rejected by all implementations when encountered."
6. **did:webvh Method-Specific Identifier.** "The `{SCID}` value used temporarily during DID creation is a placeholder and is not a conforming `scid`; it **MUST** be replaced before the DID is published or resolved."
7. **did:webvh Read (Resolve).** "The version number **MUST** be `1` for the first entry and **MUST** equal the previous entry's version number + 1 for each subsequent entry. Gaps (e.g., entry 3 after entry 1) **MUST** terminate resolution."
8. **did:webvh DID Method Parameters.** "Resolvers **MUST** verify the proof's `cryptosuite` property; an absent, mismatched, or non-conformant `cryptosuite` **MUST** cause the entry to be rejected."
9. **did:webvh Threats and Attacks.** "Plaintext HTTP **MUST NOT** be used except for testing or non-production deployments where confidentiality is not required."

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
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `did`, `vc-data-model`, `didcomm`, `jwt`, `tls`, `well-known-uris`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [did:web Method Specification](https://raw.githubusercontent.com/w3c-ccg/did-method-web/ea423c114e6f2537498ee6f94e8d794c64f60c18/index.html): Unofficial draft, W3C CCG, commit ea423c1, 2026-05-08, checked 2026-10-06.
- [The did:key Method v0.9](https://raw.githubusercontent.com/w3c-ccg/did-method-key/2cc490c38c5aacf58497a87fc0cf8794668bf716/index.html): Unofficial draft, W3C CCG, commit 2cc490c, 2025-11-02, checked 2026-10-06.
- [did:jwk Method Specification](https://raw.githubusercontent.com/quartzjer/did-jwk/44e186cf4cc215fc726afeecad1727cc9f9a66e8/spec.md): Community draft, commit 44e186c, 2023-08-19, checked 2026-10-06.
- [The did:webvh DID Method v1.0: Specification](https://raw.githubusercontent.com/decentralized-identity/didwebvh/7e39c700fd565ee47badf95c1eda11067dbcf2b7/spec-v1.0/specification.md): DIF specification, v1.0, commit 7e39c70, 2026-09-25, checked 2026-10-06.
- [The did:webvh DID Method v1.0: Security and Privacy Considerations](https://raw.githubusercontent.com/decentralized-identity/didwebvh/7e39c700fd565ee47badf95c1eda11067dbcf2b7/spec-v1.0/security_and_privacy.md): DIF specification, v1.0, commit 7e39c70, 2026-09-25, checked 2026-10-06.
