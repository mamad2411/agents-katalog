---
name: x509-pkix
description: >-
  X.509 PKIX (RFC 5280): issue and validate certificates and CRLs, with OCSP and Certificate Transparency. Covers RFC 5280 Internet X.509 Public Key Infrastructure Certificate and Certificate Revocation List (CRL) Profile, RFC 6960 X.509 Internet Public Key Infrastructure Online Certificate Status Protocol - OCSP, RFC 9162 Certificate Transparency Version 2.0. Use when issuing or checking X.509 certificates. Triggers: PKIX, RFC 5280, OCSP, Certificate Transparency.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# Internet X.509 Public Key Infrastructure Certificate and Certificate Revocation List (CRL) Profile

Internet X.509 Public Key Infrastructure Certificate and Certificate Revocation List (CRL) Profile

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when issuing or checking X.509 certificates.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: RFC 5280 Internet X.509 Public Key Infrastructure Certificate and Certificate Revocation List (CRL) Profile (default); RFC 6960 X.509 Internet Public Key Infrastructure Online Certificate Status Protocol - OCSP (default); RFC 9162 Certificate Transparency Version 2.0 (default); RFC 6962 Certificate Transparency (legacy: read and upgrade, never author). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **RFC 5280 § 4.1.2.2.** "Certificate users MUST be able to handle serialNumber values up to 20 octets."
2. **RFC 5280 § 4.1.2.2.** "Conforming CAs MUST NOT use serialNumber values longer than 20 octets."
3. **RFC 5280 § 4.1.2.5.** "CAs conforming to this profile MUST always encode certificate validity dates through the year 2049 as UTCTime; certificate validity dates in 2050 or later MUST be encoded as GeneralizedTime."
4. **RFC 5280 § 4.2.** "A certificate-using system MUST reject the certificate if it encounters a critical extension it does not recognize or a critical extension that contains information that it cannot process."
5. **RFC 5280 § 4.2.1.3.** "If the keyCertSign bit is asserted, then the cA bit in the basic constraints extension (Section 4.2.1.9) MUST also be asserted."
6. **RFC 5280 § 4.2.1.9.** "If the basic constraints extension is not present in a version 3 certificate, or the extension is present but the cA boolean is not asserted, then the certified public key MUST NOT be used to verify certificate signatures."
7. **RFC 5280 § 5.2.** "If a CRL contains a critical extension that the application cannot process, then the application MUST NOT use that CRL to determine the status of certificates."
8. **RFC 5280 § 6.1.** "A certificate MUST NOT appear more than once in a prospective certification path."
9. **RFC 6960 § 2.2.** "All definitive response messages SHALL be digitally signed."
10. **RFC 6960 § 4.2.2.2.** "Systems or applications that rely on OCSP responses MUST be capable of detecting and enforcing the use of the id-kp-OCSPSigning value as described above."
11. **RFC 9162 § 8.1.1.** "If a TLS server includes the transparency_info TLS extension when resuming a TLS session, the TLS client MUST abort the handshake."

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
- **`references/requirements.md`**: quotes taken from the pinned specification. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [RFC 5280 Internet X.509 Public Key Infrastructure Certificate and Certificate Revocation List (CRL) Profile](https://www.rfc-editor.org/rfc/rfc5280.html): PROPOSED STANDARD, RFC 5280 (PROPOSED STANDARD, May 2008), checked 2026-10-06.
- [RFC 6960 X.509 Internet Public Key Infrastructure Online Certificate Status Protocol - OCSP](https://www.rfc-editor.org/rfc/rfc6960.html): PROPOSED STANDARD, RFC 6960 (PROPOSED STANDARD, June 2013), checked 2026-10-06.
- [RFC 9162 Certificate Transparency Version 2.0](https://www.rfc-editor.org/rfc/rfc9162.html): EXPERIMENTAL, RFC 9162 (EXPERIMENTAL, December 2), checked 2026-10-06.
- [RFC 6962 Certificate Transparency](https://www.rfc-editor.org/rfc/rfc6962.html): EXPERIMENTAL, RFC 6962 (EXPERIMENTAL, June 2013), checked 2026-10-06.
