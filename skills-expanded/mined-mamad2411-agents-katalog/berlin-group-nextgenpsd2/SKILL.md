---
name: berlin-group-nextgenpsd2
description: >-
  Berlin Group NextGenPSD2 XS2A API: build PSD2 payment initiation, account information and SCA flows as an ASPSP or TPP. Covers the openFinance API Framework PSD2 Compliance V2 Suite, XS2A Implementation Guidelines 2.4.2 and Protocol Functions and Security Measures 2.4.1 (31 July 2026). Use when implementing a NextGenPSD2 or XS2A interface, PSD2 payment initiation (PIS) or account information (AIS), redirect, decoupled, embedded or OAuth SCA, or HTTP message signing with eIDAS certificates. Triggers: NextGenPSD2, Berlin Group, XS2A, PSD2 API, PIS, AIS, PIIS, SCA, scaRedirect, Digest, TPP-Signature-Certificate.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Berlin Group NextGenPSD2

The Berlin Group NextGenPSD2 XS2A interface, now published as the openFinance API Framework PSD2 Compliance V2 Suite: the XS2A API Implementation Guidelines 2.4.2 (payment initiation, account information, confirmation of funds) and the Protocol Functions and Security Measures 2.4.1 (API structure, SCA approaches, TLS, request signing and encryption).

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: ASPSP (bank) exposing the XS2A interface, or TPP / API Client (PISP, AISP, PIISP) calling it.
- Target version: PSD2 Compliance V2 Suite (current); NextGenPSD2 1.3.x (legacy). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **§ 3.5.** "If the PSU does not complete a required SCA within the required timeframe the payment resource's status must be set to "RJCT"."
2. **§ 3.7.** "According to item 40 of [EBA-OP2] the payment resource shall contain the debtorAccount after the payment has been initiated successfully, even if it was not provided by the TPP within the initial call."
3. **§ 4.4.1.** "In case, no account is accessible, the ASPSP shall return an empty array.As this is also considered a positive response, the Response code must still be 200."
4. **§ 6.2.2.1.** "When an API Client includes a signature according to this signature profile, it must also include a "Digest" header as defined in [RFC3230]."
5. **§ 6.2.2.1.** "If the message does not contain a body, the "Digest" header must contain the hash of an empty byte list."
6. **§ 7.1.4.** "The recipient MUST validate the certificate chain according to RFC 5280 and consider the certificate or certificate chain to be invalid if any validation failure occurs."
7. **§ 9.4.** "For this reason, the same Client-Redirect-URI as used when creating the related resource shall be provided by the TPP."
8. **§ 9.8.2.2.** "As a consequence of this requirement, it follows that ASPSPs shall not include a query parameter named "state" in their "scaRedirect" links."
9. **§ 9.8.3.** "The TPP must check whether the state parameter is linked to the current session as described in Section 9.8.2."
10. **§ 9.8.3.** "If the check fails, the transaction must be stopped by the TPP and the above defined request messages shall not be used."

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
- [ ] Every signed request carries a Digest header and a signature whose first certificate holds the signing key; the ASPSP validates the chain per RFC 5280.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `open-banking-uk`, `oauth`, `jwt`, `eidas`, `x509-pkix`, `json-patch`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Berlin Group XS2A API Implementation Guidelines 2.4.2](https://berlin-group.org/wp-content/uploads/2026/09/11b.-Berlin-Group-openFinance-API-Framework-Core-PSD2-Compliance-V2-Suite-Compliance-Services-XS2A-API-Implementation-Guidelines-V2.4.2-20260731.pdf): Berlin Group Specification, Version 2.4.2, 31 July 2026, checked 2026-10-06.
- [Berlin Group Protocol Functions and Security Measures 2.4.1](https://berlin-group.org/wp-content/uploads/2026/09/11c.-Berlin-Group-openFinance-API-Framework-Core-PSD2-Compliance-V2-Suite-Protocol-Functions-and-Security-Measures-V2.4.1-20260731.pdf): Berlin Group Specification, Version 2.4.1, 31 July 2026, checked 2026-10-06.
