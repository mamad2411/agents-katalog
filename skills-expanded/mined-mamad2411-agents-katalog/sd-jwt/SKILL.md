---
name: sd-jwt
description: >-
  RFC 9901 SD-JWT: issue, present and verify Selective Disclosure JWTs, with
  _sd and _sd_alg digests, object and array element Disclosures, decoys, the ~
  serialization, Key Binding JWTs with sd_hash, the JWS JSON serialization, and
  the processing, security and privacy rules. Also covers SD-JWT VC draft-19
  (draft-ietf-oauth-sd-jwt-vc: dc+sd-jwt, vct, aka_vcts, JWT VC Issuer
  Metadata, x5c, Type Metadata) and Token Status List draft-21
  (draft-ietf-oauth-status-list: status claim, Status List Tokens, bits,
  ZLIB, revocation checks), both with a build posture, plus upgrades from
  pre-RFC SD-JWT drafts and vc+sd-jwt. Use when building an issuer, wallet or
  verifier for selectively disclosable credentials, debugging a disclosure
  digest or KB-JWT, adding revocation or suspension, or reviewing an SD-JWT
  library. Triggers: SD-JWT, SD-JWT+KB, KB-JWT, kb+jwt, application/sd-jwt,
  selective disclosure, Disclosure, sd_hash, dc+sd-jwt, vc+sd-jwt, vct,
  jwt-vc-issuer, statuslist+jwt, status_list, idx, Referenced Token.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# SD-JWT (Selective Disclosure for JWTs)

RFC 9901, published by the IETF, defines SD-JWT: a JWS whose payload carries salted digests of claims, with the cleartext in separate Disclosures the Holder can choose to reveal, and an optional Key Binding JWT that proves possession of the Holder's key. The skill also covers two IETF OAuth WG drafts built on it: SD-JWT-based Verifiable Digital Credentials (SD-JWT VC) and Token Status List. With this skill the agent builds Issuers, Holders (wallets) and Verifiers that interoperate and keep undisclosed data private.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources), with the section it cites. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: Issuer, Holder (wallet), Verifier, Status Issuer or Status Provider. Most work touches two of them.
- Target version: three version families.
  - SD-JWT: RFC 9901 (default, the only valid target). Legacy, upgrade from and never author: SD-JWT drafts -09 to -22, SD-JWT drafts -07 and -08, SD-JWT drafts -05 and -06, SD-JWT drafts -04 and earlier.
  - SD-JWT VC: SD-JWT VC draft-19 (current, posture build). Legacy: SD-JWT VC drafts -12 to -18, SD-JWT VC drafts -06 to -11, SD-JWT VC drafts -05 and earlier (`vc+sd-jwt`).
  - Status: Token Status List draft-21 (current, posture build, in the RFC Editor queue). Legacy: Token Status List drafts -06 to -20, Token Status List drafts -01 to -05, Token Status List draft-00.
  - See [`references/versions.md`](references/versions.md).
- Revision: the pinned revisions in [Sources](#sources), unless the user or an ecosystem profile names another.
- Credential profile: plain SD-JWT with an application `typ`, or SD-JWT VC (`dc+sd-jwt`). Note any ecosystem that pins a draft revision.
- Key Binding: required by the Verifier's use case or not, and how the Holder key reaches the Issuer.
- Status: none, or Token Status List (JWT or CWT Status List Token).
- Sources: when refreshing this skill or when a rule looks out of date, re-read every URL in [Sources](#sources), check the Datatracker records for new revisions and the `became_rfc` relation, check the RFC Editor queue and the RFC 9901 record for errata, and update the pins.

## Invariants

1. **The Issuer-signed JWT is signed, never `none`** (RFC 9901 § 4.1, § 9.1). Verifiers always check the signature and reject on failure.
2. **Digests are over the encoded Disclosure.** Hash the US-ASCII bytes of the base64url string with `_sd_alg` (default `sha-256`, top level only), and base64url-encode the digest (§ 4.1.1, § 4.2.3).
3. **Salts are random, unique per claim and secret.** At least 128 random bits are RECOMMENDED; never reveal a salt except to the Holder (§ 4.2.1, § 9.3).
4. **Disclosure shapes are fixed.** Object property `[salt, name, value]` with a name that is not `_sd`, `...` or an existing clear claim; array element `[salt, value]`, embedded as `{"...": digest}` (§ 4.2.1, § 4.2.2, § 4.2.4.2).
5. **Validity claims stay in the clear.** Do not make `iss`, `exp`, `nbf`, `cnf` (or `aud`, except single entries) disclosable, and Verifiers require the claims they need (§ 9.7, § 7.1 step 6).
6. **Serialization keeps the trailing tilde.** `<JWT>~<D.1>~...~<D.N>~[<KB-JWT>]`, no duplicate or foreign Disclosures, parents included for nested ones (§ 4, § 4.2.6).
7. **The KB-JWT is typed and bound.** `typ: kb+jwt`, `iat`, a single-string `aud`, a string `nonce`, and `sd_hash` over the presented SD-JWT, signed with the `cnf` key (§ 4.3, § 4.3.1, § 4.3.2).
8. **Key Binding policy is set before verifying.** Never decide it from whether a KB-JWT was sent (§ 7.3 step 1, § 9.5).
9. **Verification is strict.** Reject wrong-length Disclosures, forbidden or duplicate claim names, repeated digests and unreferenced Disclosures; drop unmatched array digests and all `_sd`, `_sd_alg` (§ 7.1).
10. **SD-JWT VC is explicitly typed.** `typ: dc+sd-jwt`, a `vct` Collision-Resistant Name, and `vct`, `vct#integrity`, `aka_vcts`, `iss`, `nbf`, `exp`, `cnf` and `status` never disclosable (SD-JWT VC § 2.2.1, § 2.2.2.1, § 2.2.2.3).
11. **SD-JWT VC Issuer keys are validated by a permitted mechanism.** JWT VC Issuer Metadata with `issuer` equal to `iss`, or `x5c` in the protected header; otherwise reject (SD-JWT VC § 2.5, § 4.3).
12. **Status is checked after the token.** Validate the Referenced Token first; `sub` of the Status List Token equals `status_list.uri`; an out-of-bounds `idx` is rejected (Token Status List § 8.3).

## Workflow

1. **Pick the version per family.** RFC 9901 for SD-JWT, SD-JWT VC draft-19, Token Status List draft-21, unless an ecosystem pins an older revision for interop.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target revision of each family in use is recorded, and no legacy line is authored.
2. **Design the claim structure.** Decide per claim and per level what is clear, disclosable, flat, structured or recursive; keep validity claims clear; plan decoys and `typ`.
   -> [`references/issuance-and-disclosures.md`](references/issuance-and-disclosures.md)
   ✓ A table lists every claim with its disclosability, and no § 9.7 or SD-JWT VC § 2.2.2.3 claim is disclosable.
3. **Build the Issuer.** Create salts and Disclosures, embed and shuffle digests, add decoys, put the Holder key in `cnf`, sign, serialize with the trailing `~`.
   -> [`references/issuance-and-disclosures.md`](references/issuance-and-disclosures.md)
   ✓ The § 4.2.3 test vector reproduces, and the SD-JWT passes your own § 7.1 verifier.
4. **Build the Holder.** Verify on receipt, select Disclosures with their parents, create the KB-JWT when required, store credentials encrypted.
   -> [`references/presentation-and-key-binding.md`](references/presentation-and-key-binding.md)
   ✓ `sd_hash` matches the § 5.2 example, and presentations never include undisclosed salts.
5. **Build the Verifier.** Fix the Key Binding policy, run § 7.1 and § 7.3, check `typ`, and hand only the processed payload to the application.
   -> [`references/verification.md`](references/verification.md)
   ✓ Tampered, duplicated, unreferenced and stripped-KB-JWT presentations are rejected in tests.
6. **Apply the SD-JWT VC profile** (if used). `dc+sd-jwt`, `vct`, Issuer key discovery, safe HTTP retrieval, optional Type Metadata with integrity checks.
   -> [`references/sd-jwt-vc.md`](references/sd-jwt-vc.md)
   ✓ Metadata fetches are HTTPS-only with SSRF checks, and a mismatched `issuer` or integrity value causes rejection.
7. **Add status** (if used). Allocate indices, publish signed Status List Tokens with `exp` and `ttl`, add `status.status_list` to tokens, check status in Verifiers.
   -> [`references/status-list.md`](references/status-list.md)
   ✓ The Appendix C test vectors decode correctly, and indices are never reused.
8. **Review privacy.** Batch issuance with fresh keys and salts, randomized timestamps, decoys, minimal storage and logging, and herd privacy for status lists.
   -> [`references/issuance-and-disclosures.md`](references/issuance-and-disclosures.md), [`references/status-list.md`](references/status-list.md)
   ✓ Each RFC 9901 § 10 and Token Status List § 12 item has a decision recorded.
9. **Upgrade** (only when asked). Follow the checklist for each family from the source revision to the target.
   -> [`references/versions.md`](references/versions.md)
   ✓ Upgraded tokens validate under the target revision and disclose the same claims.

## Verify before done

- [ ] Digests and `sd_hash` are computed over base64url strings as US-ASCII bytes and encoded as base64url (RFC 9901 § 4.2.3, § 4.3.1).
- [ ] Every Disclosure has a fresh random salt of at least 128 bits (§ 9.3).
- [ ] `_sd_alg` is absent or at the top level only; `sha-256` is supported (§ 4.1.1).
- [ ] No security-critical claim is selectively disclosable (§ 9.7; SD-JWT VC § 2.2.2.3).
- [ ] Every serialized SD-JWT without a KB-JWT ends in `~` (§ 4).
- [ ] KB-JWTs have `typ: kb+jwt`, `iat`, a single-string `aud`, `nonce` and `sd_hash`, and are verified with the `cnf` key (§ 4.3, § 7.3).
- [ ] The Verifier's Key Binding decision does not depend on the presentation (§ 9.5).
- [ ] The § 7.1 rejections are covered by tests: bad Disclosure length, `_sd` or `...` names, duplicate names, repeated digests, unreferenced Disclosures.
- [ ] SD-JWT VCs use `typ: dc+sd-jwt`, and retrieval follows SD-JWT VC § 3 and § 7.1.
- [ ] Status List Tokens use `typ: statuslist+jwt` (or the CWT form), `sub` equals `uri`, and the Status List is ZLIB-compressed (Token Status List § 4.1, § 5).
- [ ] Nothing is authored against a legacy draft line.

## Reference index

- **`references/versions.md`**: every version line in the three families, what changed between drafts and the RFC, and upgrade checklists. Load for steps 1 and 9.
- **`references/issuance-and-disclosures.md`**: the payload data model, Disclosures, hashing with test vectors, nesting, decoys, Key Binding setup, serialization and issuance privacy. Load for steps 2, 3 and 8.
- **`references/presentation-and-key-binding.md`**: Holder processing, Disclosure selection, the KB-JWT and `sd_hash`, JSON serialization, forwarding and storage. Load for step 4.
- **`references/verification.md`**: the § 7.1 and § 7.3 algorithms, the security considerations and common mistakes. Load for step 5.
- **`references/sd-jwt-vc.md`**: SD-JWT VC draft-19 claims, Issuer key discovery, safe retrieval, Type Metadata, integrity, SVG rendering, trust and privacy. Load for step 6.
- **`references/status-list.md`**: Token Status List draft-21 encoding, tokens, the `status` claim, Status Types, fetching, validation, aggregation and privacy. Load for steps 7 and 8.

## Related skills

- `jwt` for JWS, JWT claims and RFC 8725 best practices underneath SD-JWT: `npx skills add ScaleDockHQ/scaledock-skills --skill jwt`.
- `openid4vc` for issuing and presenting SD-JWT VCs with OpenID4VCI and OpenID4VP: `npx skills add ScaleDockHQ/scaledock-skills --skill openid4vc`.
- `vc-data-model` for W3C Verifiable Credentials, the other credential data model: `npx skills add ScaleDockHQ/scaledock-skills --skill vc-data-model`.
- `eudi-wallet` for the EU Digital Identity Wallet rules that profile SD-JWT VC: `npx skills add ScaleDockHQ/scaledock-skills --skill eudi-wallet`.
- `oauth` for the OAuth framework and authorization server metadata: `npx skills add ScaleDockHQ/scaledock-skills --skill oauth`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [RFC 9901: Selective Disclosure for JSON Web Tokens](https://www.rfc-editor.org/rfc/rfc9901.html): RFC (Proposed Standard), RFC 9901 (November 2025), checked 2026-10-05.
- [RFC Editor metadata for RFC 9901](https://www.rfc-editor.org/rfc/rfc9901.json): RFC Editor record, no errata, not updated or obsoleted, checked 2026-10-05.
- [draft-ietf-oauth-selective-disclosure-jwt-22](https://www.ietf.org/archive/id/draft-ietf-oauth-selective-disclosure-jwt-22.txt): WG draft, became RFC 9901, revision 22 (29 May 2025) with the Document History, checked 2026-10-05.
- [draft-ietf-oauth-selective-disclosure-jwt-20](https://www.ietf.org/archive/id/draft-ietf-oauth-selective-disclosure-jwt-20.txt): WG draft, superseded, revision 20 (27 May 2025), checked 2026-10-05.
- [draft-ietf-oauth-selective-disclosure-jwt-09](https://www.ietf.org/archive/id/draft-ietf-oauth-selective-disclosure-jwt-09.txt): WG draft, superseded, revision 09 (13 June 2024), checked 2026-10-05.
- [draft-ietf-oauth-selective-disclosure-jwt-08](https://www.ietf.org/archive/id/draft-ietf-oauth-selective-disclosure-jwt-08.txt): WG draft, superseded, revision 08 (4 March 2024), checked 2026-10-05.
- [draft-ietf-oauth-selective-disclosure-jwt-07](https://www.ietf.org/archive/id/draft-ietf-oauth-selective-disclosure-jwt-07.txt): WG draft, superseded, revision 07 (11 December 2023), checked 2026-10-05.
- [draft-ietf-oauth-selective-disclosure-jwt-06](https://www.ietf.org/archive/id/draft-ietf-oauth-selective-disclosure-jwt-06.txt): WG draft, superseded, revision 06 (23 October 2023), checked 2026-10-05.
- [draft-ietf-oauth-selective-disclosure-jwt-05](https://www.ietf.org/archive/id/draft-ietf-oauth-selective-disclosure-jwt-05.txt): WG draft, superseded, revision 05 (30 June 2023), checked 2026-10-05.
- [draft-ietf-oauth-selective-disclosure-jwt-04](https://www.ietf.org/archive/id/draft-ietf-oauth-selective-disclosure-jwt-04.txt): WG draft, superseded, revision 04 (11 April 2023), checked 2026-10-05.
- [draft-ietf-oauth-sd-jwt-vc-19](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-19.txt): WG draft, submitted to the IESG for publication, revision 19 (31 August 2026), checked 2026-10-05.
- [Datatracker API: draft-ietf-oauth-sd-jwt-vc](https://datatracker.ietf.org/api/v1/doc/document/draft-ietf-oauth-sd-jwt-vc/): active WG draft, IESG state Waiting for AD Go-Ahead, rev 19, no RFC, checked 2026-10-05.
- [draft-ietf-oauth-sd-jwt-vc-12](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-12.txt): WG draft, superseded, revision 12 (20 October 2025), checked 2026-10-05.
- [draft-ietf-oauth-sd-jwt-vc-11](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-11.txt): WG draft, superseded, revision 11 (15 September 2025), checked 2026-10-05.
- [draft-ietf-oauth-sd-jwt-vc-06](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-06.txt): WG draft, superseded, revision 06 (13 November 2024), checked 2026-10-05.
- [draft-ietf-oauth-sd-jwt-vc-05](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-05.txt): WG draft, superseded, revision 05 (18 September 2024), checked 2026-10-05.
- [draft-ietf-oauth-sd-jwt-vc-00](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-00.txt): WG draft, superseded, revision 00 (16 August 2023), checked 2026-10-05.
- [draft-ietf-oauth-status-list-21](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-21.txt): WG draft, approved, in the RFC Editor queue, revision 21 (21 June 2026), checked 2026-10-05.
- [Datatracker API: draft-ietf-oauth-status-list](https://datatracker.ietf.org/api/v1/doc/document/draft-ietf-oauth-status-list/): active WG draft, IESG state RFC Ed Queue, RFC Editor state In Progress, rev 21, checked 2026-10-05.
- [Datatracker API: became_rfc for draft-ietf-oauth-status-list](https://datatracker.ietf.org/api/v1/doc/relateddocument/?source__name=draft-ietf-oauth-status-list&relationship__slug=became_rfc): relation query, 0 results (no RFC), checked 2026-10-05.
- [RFC Editor queue (XML)](https://www.rfc-editor.org/queue2.xml): RFC Editor queue, lists draft-ietf-oauth-status-list-20 received 2026-06-04, no SD-JWT VC entry, checked 2026-10-05.
- [draft-ietf-oauth-status-list-20](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-20.txt): WG draft, superseded, revision 20 (20 April 2026) with the Document History, checked 2026-10-05.
- [draft-ietf-oauth-status-list-06](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-06.txt): WG draft, superseded, revision 06 (3 December 2024), checked 2026-10-05.
- [draft-ietf-oauth-status-list-05](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-05.txt): WG draft, superseded, revision 05 (21 October 2024), checked 2026-10-05.
- [draft-ietf-oauth-status-list-03](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-03.txt): WG draft, superseded, revision 03 (8 July 2024), checked 2026-10-05.
- [draft-ietf-oauth-status-list-01](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-01.txt): WG draft, superseded, revision 01 (6 February 2024), checked 2026-10-05.
- [draft-ietf-oauth-status-list-00](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-00.txt): WG draft, superseded, revision 00 (23 October 2023), checked 2026-10-05.
