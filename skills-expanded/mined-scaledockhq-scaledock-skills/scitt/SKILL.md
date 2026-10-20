---
name: scitt
description: >-
  IETF SCITT RFC 9943 and SCRAPI draft-11: build and verify supply chain transparency with Signed Statements, Transparency Services, Receipts and the SCITT Reference API. Use when issuing COSE_Sign1 Signed Statements with CWT Claims iss and sub, kid, x5t or x5chain and a content type; running a Transparency Service with Registration Policies, trust anchors and an append-only, non-equivocating Verifiable Data Structure; producing or verifying RFC 9942 COSE Receipts (receipts 394, vds 395, vdp 396, RFC9162_SHA256 inclusion and consistency proofs) and Transparent Statements; implementing SCRAPI (POST /entries, 201 or 202 with Location, polling with 204, /.well-known/scitt-keys, concise problem details); or auditing a log. Targets RFC 9943 (current) and SCRAPI draft-11 (current, build); upgrades from architecture drafts with temporary labels -111 and -222 or 391 to 393, and SCRAPI drafts with 303 and 302 polling or /operations. Triggers: SCITT, scitt-statement+cose, scitt-receipt+cose, transparency log.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# SCITT: Supply Chain Integrity, Transparency and Trust

The IETF SCITT working group defines how an Issuer signs a Statement about a supply chain Artifact, how a Transparency Service (TS) registers it in an append-only Verifiable Data Structure (VDS) and returns a Receipt, and how Relying Parties and Auditors verify the result. RFC 9943 is the architecture and message format, RFC 9942 defines COSE Receipts, and SCRAPI (draft-ietf-scitt-scrapi) is the HTTP API. With this skill the agent produces Signed Statements, TS registration logic, SCRAPI endpoints or clients, and Receipt verifiers.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources), with the section it cites. Bare section numbers are RFC 9943; SCRAPI means draft-ietf-scitt-scrapi-11. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: Issuer, Transparency Service operator, Client that registers on behalf of Issuers, Relying Party (verifier), or Auditor.
- Target version: RFC 9943 (current) for messages and roles, and SCRAPI draft-11 (current, posture: build) for the HTTP API. Legacy, read and upgrade from but never author: architecture draft-05 to draft-22, architecture draft-04 and earlier, SCRAPI draft-04 to draft-10, and SCRAPI draft-03 and earlier. No preview exists. See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Issuer identity: X.509 (`x5t` or `x5chain`) or a key identified by `kid`, and how the TS's trust anchors reference it.
- Statement payload: its media type (for example CycloneDX, SPDX, in-toto or SLSA), and whether it is attached, detached, or a hash of the content.
- VDS: the Receipt algorithm, normally `RFC9162_SHA256` (vds 1).
- Sources: when refreshing this skill or when a rule looks out of date, re-read every URL in [Sources](#sources), check the datatracker for a SCRAPI RFC and the RFC Editor for errata or updates to RFC 9943 and RFC 9942, and update the pins.

## Invariants

1. **Signed Statements are tagged COSE_Sign1** (§ 6, § 6.1). Receipts and Transparent Statements are too (§ 7, RFC 9942 § 4.3).
2. **CWT Claims (label 15) with `iss` (1) and `sub` (2) are in the protected header** of every Signed Statement and Receipt (§ 6, RFC 9597 § 2).
3. **The Issuer key is identified in the protected header**: `x5t` or `x5chain` for X.509, otherwise `kid` MUST be present (§ 6). With X.509, `iss` is a URI string of 1 to 8192 characters (§ 6).
4. **A TS verifies the signature, applies its Registration Policy, and only then registers** (§ 5.1.1.1, § 6.3, SCRAPI § 2.3). It MUST register a Signed Statement before releasing its Receipt (§ 6.3).
5. **Registration Policies and trust anchors are themselves registered on the VDS**, and the policy most recently committed at registration time applies (§ 5.1.1.1). Auditors get enough to replay every check (§ 5.1.1.2).
6. **The unprotected header is emptied before the entry joins the Statement Sequence** (§ 6.3).
7. **The VDS is append-only, non-equivocating and replayable** (§ 5.1.3). TSs MUST produce COSE Receipts and every Receipt profile supports inclusion proofs (§ 3, § 5.1).
8. **Receipts go in unprotected header 394 as `bstr .cbor Receipt` entries**; the Receipt carries `vds` (395) protected and `vdp` (396) unprotected (§ 7, RFC 9942 § 2). Verifiers reject VDS or proof types not in the IANA registries (RFC 9942 § 4.3).
9. **Relying Parties verify per RFC 9052 § 4.4 and trust at least one Receipt Issuer** (§ 7.1). They do not accept Signed Statements without a Receipt from a TS they trust (§ 9.3).
10. **SCRAPI errors are `application/concise-problem-details+cbor`** with `title` and `detail`, and clients decide on the problem details, not the status code alone (SCRAPI § 2).
11. **SCRAPI registration returns `Location`**: 201 with the Receipt, or 202 to poll; the URL is the same in both modes (SCRAPI § 2.3.1, § 2.3.2).
12. **Unauthenticated HTTP signals never decide registration** (SCRAPI § 4.4.2.3). Without client authentication, rate limiting is mandatory (SCRAPI § 4.3).

## Workflow

1. **Pick the version.** RFC 9943 for messages, SCRAPI draft-11 for the API. Check incoming messages and endpoints for legacy markers.
   -> [`references/versions.md`](references/versions.md)
   ✓ The targets are recorded, and no legacy label (`-111`, `-222`, 391 to 393, 13) or legacy endpoint is emitted.
2. **Model the roles and the policy.** Decide the Issuer identities, the TS's trust anchors, its bootstrapping mechanism and its Registration Policy.
   -> [`references/architecture.md`](references/architecture.md)
   ✓ The policy and trust anchors are registered as Signed Statements, and the bootstrapping mechanism is one of the three in § 5.1.2.
3. **Issue Signed Statements.** Build the protected header (alg, content type, kid or x5t/x5chain, CWT Claims iss and sub), choose attached, detached or hashed payload, and sign.
   -> [`references/signed-statements-and-receipts.md`](references/signed-statements-and-receipts.md)
   ✓ The message matches RFC 9943 Figure 3, and time-dependent payloads carry a signed timestamp (SCRAPI § 4.4.2.1).
4. **Register and issue Receipts (TS).** Verify, apply the policy, empty the unprotected header, append to the VDS, sign the Receipt with vds and vdp.
   -> [`references/architecture.md`](references/architecture.md), [`references/signed-statements-and-receipts.md`](references/signed-statements-and-receipts.md)
   ✓ A Receipt is only released after the entry is committed, and its inclusion proof verifies against the log.
5. **Expose or call SCRAPI.** Implement key discovery, `POST /entries` with 201 or 202, and Receipt resolution with 200, 204 or 404; handle errors and retries.
   -> [`references/scrapi.md`](references/scrapi.md)
   ✓ Every error is a CBOR concise problem details body; clients honour `Retry-After` and back off with jitter.
6. **Verify and audit.** Attach Receipts to form Transparent Statements, verify them, and replay the log for audits.
   -> [`references/verification.md`](references/verification.md)
   ✓ The inclusion proof recomputes the root before the Receipt signature check, and the verdict is false when any required check fails.
7. **Upgrade** (only when asked). Follow the upgrade section from the source line to RFC 9943 or SCRAPI draft-11.
   -> [`references/versions.md`](references/versions.md)
   ✓ Messages validate against RFC 9943 and RFC 9942, endpoints match SCRAPI draft-11, and existing entries still resolve.

## Verify before done

- [ ] Signed Statements, Receipts and Transparent Statements are tagged COSE_Sign1 (`#6.18`).
- [ ] Protected CWT Claims (15) carry `iss` and `sub`; `kid` is present when `x5t`/`x5chain` are not (§ 6).
- [ ] Receipts use labels 394, 395 and 396 and a registered VDS such as `RFC9162_SHA256` (RFC 9942 § 2, § 5).
- [ ] The TS registers its Registration Policy and trust anchors, applies the latest one, and empties the unprotected header before logging (§ 5.1.1.1, § 6.3).
- [ ] SCRAPI: `/.well-known/scitt-keys` and `/{kid_value}` accept base64url kids; registration returns `Location`; polling returns 204 with `Retry-After` and `Cache-Control: no-store` (SCRAPI § 2).
- [ ] Media types are `application/scitt-statement+cose` and `application/scitt-receipt+cose` where those objects are labelled; SCRAPI bodies use `application/cose` (§ 10, SCRAPI § 2.3).
- [ ] Verifiers trust at least one Receipt Issuer and keep its key as long as they verify its Receipts (§ 7.1, SCRAPI § 2.1).

## Reference index

- **`references/versions.md`**: the architecture and SCRAPI version lines, what changed between drafts and the RFC, and upgrade steps. Load for steps 1 and 7.
- **`references/architecture.md`**: roles and terms, TS requirements, Registration Policies, bootstrapping, registration steps, key management and privacy. Load for steps 2 and 4.
- **`references/signed-statements-and-receipts.md`**: the CDDL for Signed Statements, Receipts and Transparent Statements, header labels, payload options, RFC9162_SHA256 proofs, media types. Load for steps 3 and 4.
- **`references/scrapi.md`**: every SCRAPI resource with requests, responses, errors, key discovery, retries and security. Load for step 5.
- **`references/verification.md`**: Relying Party and Auditor checks, Receipt verification order, key retention and privacy. Load for step 6.

## Related skills

- `in-toto` for attestations used as Statement payloads: `npx skills add ScaleDockHQ/scaledock-skills --skill in-toto`.
- `slsa` for build provenance Statements: `npx skills add ScaleDockHQ/scaledock-skills --skill slsa`.
- `cyclonedx` for SBOM Statements: `npx skills add ScaleDockHQ/scaledock-skills --skill cyclonedx`.
- `c2pa` for signed content provenance manifests: `npx skills add ScaleDockHQ/scaledock-skills --skill c2pa`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [RFC 9943: An Architecture for Trustworthy and Transparent Digital Supply Chains](https://www.rfc-editor.org/rfc/rfc9943.html): RFC (Standards Track), RFC 9943 (June 2026), checked 2026-10-05.
- [RFC 9942: CBOR Object Signing and Encryption (COSE) Receipts](https://www.rfc-editor.org/rfc/rfc9942.html): RFC (Standards Track), RFC 9942 (June 2026), checked 2026-10-05.
- [SCITT Reference APIs, draft-ietf-scitt-scrapi-11](https://www.ietf.org/archive/id/draft-ietf-scitt-scrapi-11.txt): WG draft, in the RFC Editor queue, revision 11 (2026-06-26), checked 2026-10-05.
- [Datatracker API: draft-ietf-scitt-scrapi](https://datatracker.ietf.org/api/v1/doc/document/draft-ietf-scitt-scrapi/): WG draft, intended Proposed Standard, revision 11 latest, checked 2026-10-05.
- [Datatracker API: draft-ietf-scitt-architecture](https://datatracker.ietf.org/api/v1/doc/document/draft-ietf-scitt-architecture/): published as RFC 9943, revision 22 latest, checked 2026-10-05.
- [Datatracker API: draft-ietf-cose-merkle-tree-proofs](https://datatracker.ietf.org/api/v1/doc/document/draft-ietf-cose-merkle-tree-proofs/): published as RFC 9942, revision 18 latest, checked 2026-10-05.
- [draft-ietf-scitt-architecture-22](https://www.ietf.org/archive/id/draft-ietf-scitt-architecture-22.txt): WG draft, superseded by RFC 9943, 2025-10-10, checked 2026-10-05.
- [draft-ietf-scitt-architecture-05](https://www.ietf.org/archive/id/draft-ietf-scitt-architecture-05.txt): WG draft, superseded, 2024-02-10, checked 2026-10-05.
- [draft-ietf-scitt-architecture-04](https://www.ietf.org/archive/id/draft-ietf-scitt-architecture-04.txt): WG draft, superseded, 2023-10-23, checked 2026-10-05.
- [draft-ietf-scitt-architecture-02](https://www.ietf.org/archive/id/draft-ietf-scitt-architecture-02.txt): WG draft, superseded, 2023-07-10, checked 2026-10-05.
- [draft-ietf-scitt-scrapi-10](https://www.ietf.org/archive/id/draft-ietf-scitt-scrapi-10.txt): WG draft, superseded, 2026-05-13, checked 2026-10-05.
- [draft-ietf-scitt-scrapi-06](https://www.ietf.org/archive/id/draft-ietf-scitt-scrapi-06.txt): WG draft, superseded, 2025-12-29, checked 2026-10-05.
- [draft-ietf-scitt-scrapi-04](https://www.ietf.org/archive/id/draft-ietf-scitt-scrapi-04.txt): WG draft, superseded, 2025-03-03, checked 2026-10-05.
- [draft-ietf-scitt-scrapi-03](https://www.ietf.org/archive/id/draft-ietf-scitt-scrapi-03.txt): WG draft, superseded, 2025-01-08, checked 2026-10-05.
- [draft-ietf-scitt-scrapi-00](https://www.ietf.org/archive/id/draft-ietf-scitt-scrapi-00.txt): WG draft, superseded, 2024-01-25, checked 2026-10-05.
- [IETF SCITT working group](https://datatracker.ietf.org/wg/scitt/about/): Active working group (Security Area), charter-ietf-scitt-01, checked 2026-10-05.
