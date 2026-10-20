---
name: dkim
description: >-
  DKIM (RFC 6376): sign and verify email with DKIM-Signature header fields and
  _domainkey DNS key records. Use when adding, configuring, debugging or
  reviewing DKIM signing or verification in a mail server, MTA, mailing list,
  sending service, library or DNS zone: the v, a, b, bh, c, d, h, i, l, q, s, t,
  x and z tags, simple and relaxed canonicalization, which header fields to
  sign and oversigning, l= body length risks, selector TXT records at
  selector._domainkey.domain (v=DKIM1, h, k, n, p, s, t=y, t=s), revoking with
  an empty p=, key rotation with new selectors, rsa-sha256 with 2048-bit RSA
  keys, ed25519-sha256, why rsa-sha1 and RSA keys under 1024 bits fail, SUCCESS,
  PERMFAIL and TEMPFAIL results, and "body hash did not verify" errors. Targets
  RFC 6376 as updated by RFC 8301, RFC 8463, RFC 8553 and RFC 8616; upgrades
  from RFC 4871 and RFC 5672; tracks the IETF DKIM2 drafts as a preview.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# DKIM

DomainKeys Identified Mail (RFC 6376, STD 76, published by the IETF) lets a domain take responsibility for an email by signing selected header fields and the body, with the public key published in DNS under `<selector>._domainkey.<domain>`. RFC 8301 removes rsa-sha1 and short RSA keys, and RFC 8463 adds Ed25519. With this skill the agent configures signers, publishes and rotates key records, and builds or reviews verifiers.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources), with the section it cites. Bare section numbers are RFC 6376. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: signer (MSA, MTA, sending service, mailing list that re-signs), verifier (border MTA, filter), DNS operator publishing keys, or several.
- Target version: RFC 6376 with RFC 8301, RFC 8463, RFC 8553 and RFC 8616 (default). RFC 4871 (with RFC 5672) is legacy: read it and upgrade from it, never build to it. DKIM2 is a preview (posture: track): never emit its header fields. See [`references/versions.md`](references/versions.md).
- Revision: the pinned revisions in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill or when a rule looks out of date, re-read every URL in [Sources](#sources) first, check the RFC Editor entry for RFC 6376 for new updating RFCs and errata, the IANA DKIM parameters registry for new algorithms or tags, and the datatracker for a new DKIM2 revision, and update the pins.
- Signing domain (`d=`) and selector names, and the mail streams each one signs.
- Mail path: whether messages pass mailing lists or forwarders that modify them. This drives the canonicalization and `l=` choices.

## Invariants

1. **Algorithms.** Sign with `rsa-sha256`; also sign with `ed25519-sha256` where possible. `rsa-sha1` MUST NOT be used for signing or verifying, and such signatures are PERMFAIL (RFC 8301 § 3.1; RFC 8463 § 5). Verifiers MUST implement both rsa-sha256 and ed25519-sha256.
2. **RSA key size.** At least 1024 bits for all keys, and SHOULD be at least 2048. Verifiers MUST handle 1024 to 4096 bits and MUST NOT accept keys under 1024 (RFC 8301 § 3.2).
3. **Required tags.** `v=1`, `a`, `b`, `bh`, `d`, `h` and `s` are required; a duplicated tag invalidates the field; unknown tags are ignored but still hashed (§ 3.2, § 3.5, § 6.1.1).
4. **From is always signed.** `h=` MUST include `From`; verifiers return PERMFAIL otherwise (§ 5.4, § 6.1.1).
5. **`i=` stays inside `d=`.** The `i=` domain equals `d=` or is a subdomain of it, and equals `d=` exactly when the key has `t=s` (§ 3.5, § 3.10, § 6.1.1).
6. **Hash input.** Body hash over the canonicalized body, cut to `l=`. Header hash over the `h=` fields in `h=` order, then the DKIM-Signature field itself with an empty `b=` and no trailing CRLF (§ 3.7, erratum 5252). The field never lists itself in `h=` (§ 3.5).
7. **Sign what the verifier will receive.** CRLF line endings, 7-bit transfer encoding applied, hashed after MIME encoding and before dot-stuffing (§ 3.7, § 5.3).
8. **Prepend.** A new DKIM-Signature goes before every existing DKIM-Signature field (§ 5.6).
9. **One key record per selector.** TXT strings are concatenated without spaces; `v=DKIM1`, when present, is the first tag; empty `p=` means revoked (§ 3.6.1, § 3.6.2.2).
10. **New key, new selector.** Never reuse a selector for a new key (§ 3.1).
11. **Strict verification.** Validate every signature and key record value; any inconsistency is PERMFAIL (§ 6.1.1, § 6.1.2, § 8.8, § 8.9).
12. **Failed equals unsigned.** A message with only failed signatures is treated like an unsigned one; cryptographic failures never cause a 4xx SMTP reply (§ 6.1, § 6.3).
13. **`l=` only with a reason.** It lets anyone append content; omit it unless a known intermediary appends to the body (§ 5.4.1, § 8.2).

## Workflow

1. **Pick the version.** Use RFC 6376 with its updates. If code or documentation cites RFC 4871, or uses `g=`, rsa-sha1 or keys under 1024 bits, plan the upgrade (step 9).
   -> [`references/versions.md`](references/versions.md)
   ✓ New code and documentation cite RFC 6376 and RFC 8301; nothing emits DKIM2 header fields.
2. **Generate keys and name selectors.** One 2048-bit RSA key, plus an Ed25519 key under a second selector if the signer supports it (RFC 8463 § 6). Name selectors so they never need reuse, and avoid names that leak user data (§ 3.1).
   -> [`references/keys-and-dns.md`](references/keys-and-dns.md)
   ✓ Each key has its own selector; no RSA key is under 2048 bits without a recorded reason.
3. **Publish the key records.** One TXT record per selector at `<selector>._domainkey.<domain>`, with `v=DKIM1`, `k=`, `p=`, and `t=s` unless `i=` needs subdomains (§ 3.6.1). Use `t=y` only while testing.
   -> [`references/keys-and-dns.md`](references/keys-and-dns.md)
   ✓ A DNS lookup returns exactly one record per selector, it parses as a tag-list, and long keys are split into strings inside one record.
4. **Choose what to sign.** Sign `From` and the fields users see or that change processing (`Subject`, `Date`, `To`, `Cc`, `Reply-To`, `Sender`, `Message-ID`, MIME and `List-*` fields), skip `Received` and `Return-Path`, and oversign fields that must not be added, such as `From` and `Subject` (§ 5.4, § 5.4.1, § 8.15). Pick `c=` by mail type: `relaxed` for person-to-person mail that may be modified in transit, `simple` for mail no intermediary should touch (§ 5.4.1). Leave out `l=`.
   -> [`references/signature-and-tags.md`](references/signature-and-tags.md), [`references/canonicalization.md`](references/canonicalization.md)
   ✓ `h=` contains `From`, each oversigned name appears once more than in the message, and `l=` is absent or justified with `Content-Type` signed.
5. **Sign.** Normalize the message, compute `bh=` and `b=`, set `t=` and, if wanted, `x=` later than `t=`, then prepend the field (§ 3.7, § 5.3, § 5.6).
   -> [`references/signature-and-tags.md`](references/signature-and-tags.md)
   ✓ Your own verifier, or an independent one, verifies the sent message as received over SMTP, for each algorithm.
6. **Verify.** Validate the field, fetch and validate the key, compute both hashes, and map every failure to PERMFAIL or TEMPFAIL with its reason (§ 6.1).
   -> [`references/verification.md`](references/verification.md)
   ✓ rsa-sha1, RSA keys under 1024 bits, missing `From` in `h=`, revoked keys and `i=` outside `d=` all give PERMFAIL; a DNS timeout gives TEMPFAIL.
7. **Report and apply policy.** Pass `d=` and the result to the assessor, add an `Authentication-Results` field before existing ones, log the failure reason, and treat failed as unsigned (§ 3.11, § 6.2, § 6.3).
   -> [`references/verification.md`](references/verification.md)
   ✓ No 4xx reply for a cryptographic failure, and forged results header fields from outside cannot be mistaken for yours.
8. **Rotate keys.** Publish the new selector, switch signing, keep the old key published through the transit window, then remove it or revoke it with an empty `p=` (§ 3.1, § 5.2).
   -> [`references/keys-and-dns.md`](references/keys-and-dns.md)
   ✓ Mail signed with the old key still verifies until the end of the window, and no selector was reused.
9. **Upgrade** (only when asked). Follow the RFC 4871 to RFC 6376 steps: drop `g=`, stop rsa-sha1, replace short keys under new selectors, and report `d=` as the result.
   -> [`references/versions.md`](references/versions.md)
   ✓ The signer and verifier pass the checks in steps 5 and 6, and existing `d=` domains and signed header sets are unchanged.

## Verify before done

- [ ] Every signature uses `a=rsa-sha256` or `a=ed25519-sha256`, and there is an rsa-sha256 signature (RFC 8301 § 3.1).
- [ ] Every RSA key is at least 1024 bits, and new keys are at least 2048 (RFC 8301 § 3.2).
- [ ] `h=` includes `From`, excludes the signature field itself, and repeats names to oversign where intended (§ 5.4, § 8.15).
- [ ] `l=` is absent, or its use is justified and `Content-Type` is signed (§ 5.4.1, § 8.2).
- [ ] Each selector has exactly one TXT record, `v=DKIM1` is first if present, and there is no `g=` (§ 3.6.1, § 3.6.2.2, Appendix C.2).
- [ ] The relaxed canonicalization code follows errata 5839 and the hash code follows erratum 5252, tested against the RFC 8463 Appendix A message.
- [ ] The verifier maps each failure to the PERMFAIL or TEMPFAIL reason in § 6.1.1 to § 6.1.3 and outputs `d=` on SUCCESS (§ 3.9).
- [ ] Key rotation keeps the old public key published for a transit window, and no selector is reused (§ 3.1, § 5.2).
- [ ] Nothing emits DKIM2 header fields.

## Reference index

- **`references/versions.md`**: RFC 6376 and its updating RFCs, RFC 4871 and RFC 5672, what changed, the errata that matter, the upgrade steps, the DKIM2 preview and an ARC pointer. Load for steps 1 and 9.
- **`references/signature-and-tags.md`**: tag syntax, every DKIM-Signature tag, choosing and oversigning header fields, `l=`, message preparation, the hash computation, multiple signatures and an example. Load for steps 4 and 5.
- **`references/canonicalization.md`**: simple and relaxed for header and body, empty-body hashes, the RFC example, how to choose, and how to debug hash failures. Load for steps 4 to 6.
- **`references/keys-and-dns.md`**: the `_domainkey` name, key record tags, algorithms and key sizes, generating keys, selectors, rotation, revocation and parent domains. Load for steps 2, 3 and 8.
- **`references/verification.md`**: results, signature order, the validation, key and hash steps with their PERMFAIL and TEMPFAIL reasons, reporting, policy and verifier security checks. Load for steps 6 and 7.

## Related skills

- `dmarc` for From-domain alignment, policy and reporting on top of DKIM and SPF results: `npx skills add ScaleDockHQ/scaledock-skills --skill dmarc`.
- `spf` for authorizing sending hosts for the MAIL FROM and HELO domains: `npx skills add ScaleDockHQ/scaledock-skills --skill spf`.
- `list-unsubscribe` for the `List-Unsubscribe` header fields, which § 5.4.1 lists among the fields to sign: `npx skills add ScaleDockHQ/scaledock-skills --skill list-unsubscribe`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [RFC 6376: DomainKeys Identified Mail (DKIM) Signatures](https://www.rfc-editor.org/rfc/rfc6376): RFC (Internet Standard, STD 76; updated by RFC 8301, RFC 8463, RFC 8553 and RFC 8616), RFC 6376, checked 2026-10-05.
- [RFC 6376 errata](https://www.rfc-editor.org/errata/rfc6376): RFC Editor errata, 9 verified and 4 reported, checked 2026-10-05.
- [RFC 8301: Cryptographic Algorithm and Key Usage Update to DKIM](https://www.rfc-editor.org/rfc/rfc8301): RFC (Proposed Standard), RFC 8301, checked 2026-10-05.
- [RFC 8463: A New Cryptographic Signature Method for DKIM](https://www.rfc-editor.org/rfc/rfc8463): RFC (Proposed Standard), RFC 8463, checked 2026-10-05.
- [RFC 8616: Email Authentication for Internationalized Mail](https://www.rfc-editor.org/rfc/rfc8616): RFC (Proposed Standard), RFC 8616, checked 2026-10-05.
- [RFC 8553: DNS AttrLeaf Changes](https://www.rfc-editor.org/rfc/rfc8553): RFC (Best Current Practice, BCP 222), RFC 8553, checked 2026-10-05.
- [RFC 4871: DomainKeys Identified Mail (DKIM) Signatures](https://www.rfc-editor.org/rfc/rfc4871): RFC (Proposed Standard, obsoleted by RFC 6376), RFC 4871, checked 2026-10-05.
- [RFC 5672: RFC 4871 DKIM Signatures, Update](https://www.rfc-editor.org/rfc/rfc5672): RFC (Proposed Standard, obsoleted by RFC 6376), RFC 5672, checked 2026-10-05.
- [IANA DomainKeys Identified Mail (DKIM) Parameters](https://www.iana.org/assignments/dkim-parameters/): IANA registry, last updated 2018-07-06, checked 2026-10-05.
- [draft-ietf-dkim-dkim2-spec: DKIM2](https://datatracker.ietf.org/doc/draft-ietf-dkim-dkim2-spec/): IETF WG draft (WG Document), draft-ietf-dkim-dkim2-spec-06 (2026-08-28), checked 2026-10-05.
- [RFC 8617: The Authenticated Received Chain (ARC) Protocol](https://www.rfc-editor.org/rfc/rfc8617): RFC (Experimental), RFC 8617, checked 2026-10-05. Pointer only.
