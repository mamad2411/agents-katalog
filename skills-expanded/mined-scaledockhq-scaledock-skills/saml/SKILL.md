---
name: saml
description: >-
  SAML 2.0 SSO: build and securely validate SAML messages, pinned to the OASIS
  SAML 2.0 standard with Approved Errata 05 as the current line and SAML 1.1 as
  legacy to upgrade from. Covers assertions, AuthnRequest and Response,
  LogoutRequest and LogoutResponse, the HTTP-Redirect, HTTP-POST and
  HTTP-Artifact bindings, the Web Browser SSO and Single Logout profiles,
  metadata, XML Signature with Exclusive C14N, and encrypted assertions. Use
  when building or reviewing a SAML service provider or identity provider, an
  assertion consumer service (ACS) endpoint, SP or IdP metadata, or a SAML
  library integration, and when auditing response validation: signature
  wrapping (XSW), which element is signed, Audience, Recipient, Destination,
  InResponseTo, NotOnOrAfter, replay, clock skew, RelayState redirects,
  unsolicited IdP-initiated responses, XXE and DTDs. Triggers: SAMLResponse,
  SAMLRequest, SAMLart, RelayState, urn:oasis:names:tc:SAML:2.0, EntityDescriptor,
  SSO, SLO.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.2"
  kind: standard
---

# SAML

The Security Assertion Markup Language (SAML) is an OASIS standard for exchanging authentication and attribute assertions between an identity provider (IdP) and a service provider (SP), most often for browser single sign-on. With this skill the agent builds and reviews SAML requests, responses, metadata and the response validation an SP must perform.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources), with the section it cites. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

Cites: Core, Bind, Prof, Meta, Sec and Conf are the six SAML 2.0 documents; En is item n of SAML 2.0 Errata 05, which amends them; XMLDSig and BP are the W3C XML Signature 1.1 Recommendation and its Best Practices note.

## Inputs (fill in, or ask before starting)

- Role: service provider (relying party), identity provider (asserting party), or both.
- Target version: SAML 2.0 (default), read with Errata 05 applied. SAML 1.1 is legacy: read it and upgrade from it, never author it. No preview exists. See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Bindings in use: HTTP-Redirect, HTTP-POST, HTTP-Artifact (with SOAP for resolution). This decides where signatures live.
- Flows: SP-initiated SSO only, or IdP-initiated (unsolicited) responses too; Single Logout or not.
- Peer metadata: the other party's entityID, endpoints and keys, and how they are obtained and refreshed.
- Sources: when refreshing this skill or when a rule looks out of date, re-read every URL in [Sources](#sources) first, check the OASIS SAML TC page for a newer errata or version line, and update the pins.

## Invariants

1. **Only what was verified is used.** A SAML signature is enveloped, has exactly one `ds:Reference` whose URI is `#` plus the `ID` of the signed root element, and uses only the enveloped-signature and Exclusive C14N transforms (Core §5.4.1, §5.4.2, §5.4.4). Signatures containing `ds:Object` are rejected (E91). Every value the SP acts on comes from the element that reference resolved to, checked by name and position, never from a second lookup by element name (BP 14, XMLDSig §8.1.1).
2. **IDs are unique.** A data object declares a given ID exactly once (Core §1.3.4). A document with a duplicate ID is rejected before signature validation.
3. **Keys come from trust, not the message.** Verify with a key established out of band, normally from the peer's metadata `KeyDescriptor` (Meta §2.4.1.1, E62, E68). A signature that validates with a key from the message's own `ds:KeyInfo` proves nothing (BP 2, Sec §4.4.2).
4. **Every assertion delivered by HTTP-POST is signed,** either on the `Assertion` itself or on the enclosing `Response` (Prof §4.1.4.5 as amended by E26). When the SP's metadata sets `WantAssertionsSigned`, only an `Assertion` signature satisfies it (E7).
5. **Signed front-channel messages carry `Destination`,** and the recipient checks it equals the URL it received the message at (Bind §3.4.5.2, §3.5.5.2). Any present `Destination` is checked (Core §3.2.1, §3.2.2).
6. **Bearer confirmation is checked in full:** `Recipient` equals the ACS URL the response arrived at, `NotOnOrAfter` has not passed, and `InResponseTo` equals the ID of the SP's `AuthnRequest`, or is absent for an unsolicited response (Prof §4.1.4.3, §4.1.5).
7. **Audience is the SP.** Each bearer assertion has an `AudienceRestriction` containing the SP's entityID (Prof §4.1.4.2, E26). Audiences within one restriction are OR; separate restrictions are AND (Core §2.5.1.4, E46). An Invalid or Indeterminate `Conditions` result means reject (Core §2.5.1.1).
8. **One issuer, one subject.** Every assertion in a response comes from the responding IdP, and all refer to the same principal (E26). The `Response` `Issuer` is required if the response is signed or carries an encrypted assertion (E17).
9. **No replay.** Under HTTP-POST, the SP keeps used assertion IDs for as long as the assertion could be valid under its `SubjectConfirmationData` `NotOnOrAfter` (Prof §4.1.4.5). Artifacts are single use (Bind §3.6.5.2).
10. **Bounded clock skew.** Allow reasonable skew when comparing times, 3 to 5 minutes by default and configurable (Core §1.3.3 via E92).
11. **Integrity before decryption.** With CBC-mode encryption, require integrity protection, such as a verified `Response` signature, before decrypting (Core §6.2 via E93). Prefer RSA-OAEP over PKCS#1 v1.5 key transport (Sec §4.6 via E93).
12. **RelayState is untrusted.** It is at most 80 bytes (Bind §3.4.3, §3.5.3). Any URL derived from it is limited to `http` or `https` and sanitized (Bind §3.1.1, Prof §4.1.6 via E90).
13. **No DTDs or external entities.** No SAML schema uses a DTD. Parse SAML without DTD processing, entity expansion or network fetches. This is hardening derived from XMLDSig and BP: entity expansion during C14N can change content between validation and use (BP §2.2.1), external references must be controlled (BP 8), and signers must not send unparsed external entities (BP 23).
14. **The IdP verifies the ACS location.** An `AssertionConsumerServiceURL` or `AssertionConsumerServiceIndex` must belong to the requesting SP, signed or not (Prof §4.1.4.1, Core §3.4.1).

## Workflow

1. **Pick the version.** Use SAML 2.0 with Errata 05. If the peer speaks SAML 1.1, plan the upgrade (step 8).
   -> [`references/versions.md`](references/versions.md)
   ✓ Messages use `Version="2.0"` and the `urn:oasis:names:tc:SAML:2.0:*` namespaces.
2. **Exchange metadata and pin trust.** Record each peer's entityID, endpoints, signing and encryption keys, and validity.
   -> [`references/metadata.md`](references/metadata.md)
   ✓ Every key used to verify a peer comes from its metadata or another out-of-band channel, and metadata past `validUntil` is not used.
3. **Build or handle the `AuthnRequest`.** SP: unique ID, `Issuer`, ACS by URL or by index, `NameIDPolicy`, and the request ID stored for `InResponseTo`. IdP: authenticate the request where required and verify the ACS belongs to the SP.
   -> [`references/assertions-and-protocol.md`](references/assertions-and-protocol.md)
   ✓ The IdP rejects an unsigned request from an SP whose metadata says `AuthnRequestsSigned="true"` (E7).
4. **Encode for the binding.** Use Redirect (DEFLATE plus query-string signature), POST (base64 form) or Artifact (resolved over SOAP).
   -> [`references/bindings-and-profiles.md`](references/bindings-and-profiles.md)
   ✓ Redirect signatures are verified over the original URL-encoded parameters; POST responses carry signed assertions or a signed `Response`.
5. **Issue the response (IdP).** Build the assertion per the Web Browser SSO profile: bearer confirmation, `Recipient`, `NotOnOrAfter`, `InResponseTo`, `AudienceRestriction`, `AuthnStatement` and `SessionIndex`; then sign and, if needed, encrypt.
   -> [`references/assertions-and-protocol.md`](references/assertions-and-protocol.md)
   ✓ The response passes the SP checklist in step 6.
6. **Validate the response (SP).** Follow the ordered checklist: safe parsing, signature placement, Destination, Issuer, Status, decryption, subject confirmation, conditions, audience, replay, session.
   -> [`references/response-validation.md`](references/response-validation.md)
   ✓ Every check passes, in order, before a session is created; any failure rejects the whole response.
7. **Single Logout** (when used). Sign or otherwise authenticate `LogoutRequest` and `LogoutResponse`, include `SessionIndex`, and apply logout to late-arriving assertions.
   -> [`references/bindings-and-profiles.md`](references/bindings-and-profiles.md)
   ✓ Unauthenticated logout messages are ignored.
8. **Upgrade** (only when asked). Follow the SAML 1.1 to SAML 2.0 steps: new namespaces, `Version`, `ID`, `Issuer` element, `AudienceRestriction`, and the 2.0 profiles.
   -> [`references/versions.md`](references/versions.md)
   ✓ No SAML 1.x namespace, `MajorVersion` attribute or 1.1 artifact remains (E4).

## Verify before done

- [ ] Each verified signature has one reference to its parent's `ID`, only the allowed transforms, and no `ds:Object` (Core §5.4, E91).
- [ ] The code acts only on the nodes the verified reference covers; a wrapped copy of the assertion elsewhere in the document is never used (BP 14).
- [ ] Duplicate IDs, DTDs and external entities are rejected at parse time (Core §1.3.4; BP §2.2.1, BP 8).
- [ ] `Destination`, `Recipient`, `InResponseTo`, `Audience`, `Issuer`, `NotBefore` and `NotOnOrAfter` are all checked, with configurable skew (Prof §4.1.4.3, E92).
- [ ] Assertion IDs are cached until their confirmation expires, and a replayed response fails (Prof §4.1.4.5).
- [ ] Encrypted assertions are decrypted only after integrity is established, and the decrypted assertion's own signature is verified (Core §6.2).
- [ ] RelayState redirects are limited to safe URLs, and unsolicited responses can be disabled (E90).
- [ ] Signing and encryption keys come from pinned metadata, and the SP and IdP use distinct keys for signing and encryption where possible (BP 27).

## Reference index

- **`references/versions.md`**: SAML 2.0 with Errata 05 and SAML 1.1, which to use, what changed, the upgrade steps, and why no preview exists. Load for steps 1 and 8.
- **`references/assertions-and-protocol.md`**: assertions, subjects, conditions, statements, `AuthnRequest`, `Response`, status codes, logout, IDs, time values, signing and encryption rules from Core. Load for steps 3 and 5.
- **`references/bindings-and-profiles.md`**: HTTP-Redirect, HTTP-POST, HTTP-Artifact and SOAP, RelayState, the Web Browser SSO profile, unsolicited responses and Single Logout. Load for steps 4 and 7.
- **`references/metadata.md`**: entityIDs, endpoints, role descriptors, keys, signing, publication, caching and validity. Load for step 2.
- **`references/response-validation.md`**: the ordered SP validation checklist and the attacks each check stops (signature wrapping, replay, audience and recipient confusion, XXE, CBC attacks, RelayState). Load for step 6 and for any security review.

## Related skills

- `openid-connect` for single sign-on with OpenID Connect instead of SAML: `npx skills add ScaleDockHQ/scaledock-skills --skill openid-connect`.
- `scim` for provisioning the users and groups that SAML authenticates: `npx skills add ScaleDockHQ/scaledock-skills --skill scim`.
- `xml-signature`, when the work also follows that specification: `npx skills add ScaleDockHQ/scaledock-skills --skill xml-signature`

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Assertions and Protocols for SAML V2.0 (Core)](https://docs.oasis-open.org/security/saml/v2.0/saml-core-2.0-os.pdf): OASIS Standard, saml-core-2.0-os (15 March 2005), checked 2026-10-05.
- [Bindings for SAML V2.0 (Bind)](https://docs.oasis-open.org/security/saml/v2.0/saml-bindings-2.0-os.pdf): OASIS Standard, saml-bindings-2.0-os (15 March 2005), checked 2026-10-05.
- [Profiles for SAML V2.0 (Prof)](https://docs.oasis-open.org/security/saml/v2.0/saml-profiles-2.0-os.pdf): OASIS Standard, saml-profiles-2.0-os (15 March 2005), checked 2026-10-05.
- [Metadata for SAML V2.0 (Meta)](https://docs.oasis-open.org/security/saml/v2.0/saml-metadata-2.0-os.pdf): OASIS Standard, saml-metadata-2.0-os (15 March 2005), checked 2026-10-05.
- [Security and Privacy Considerations for SAML V2.0 (Sec)](https://docs.oasis-open.org/security/saml/v2.0/saml-sec-consider-2.0-os.pdf): OASIS Standard, saml-sec-consider-2.0-os (15 March 2005), checked 2026-10-05.
- [Conformance Requirements for SAML V2.0 (Conf)](https://docs.oasis-open.org/security/saml/v2.0/saml-conformance-2.0-os.pdf): OASIS Standard, saml-conformance-2.0-os (15 March 2005), checked 2026-10-05.
- [SAML Version 2.0 Errata 05](https://docs.oasis-open.org/security/saml/v2.0/errata05/os/saml-v2.0-errata05-os.pdf): OASIS Approved Errata, 01 May 2012, checked 2026-10-05.
- [SAML V2.0 Core Errata Composite](https://groups.oasis-open.org/higherlogic/ws/public/download/56776/sstc-saml-core-errata-2.0-wd-07.pdf/latest): non-normative Working Draft (the Approved Errata take precedence), sstc-saml-core-errata-2.0-wd-07 (8 September 2015), checked 2026-10-05.
- [Assertions and Protocol for SAML V1.1](https://www.oasis-open.org/committees/download.php/3406/oasis-sstc-saml-core-1.1.pdf): OASIS Standard, oasis-sstc-saml-core-1.1 (2 September 2003), checked 2026-10-05.
- [OASIS Security Services (SAML) TC](https://www.oasis-open.org/committees/security/): TC page, closed 08 July 2023, checked 2026-10-05.
- [XML Signature Syntax and Processing Version 1.1 (XMLDSig)](https://www.w3.org/TR/xmldsig-core1/): W3C Recommendation, 11 April 2013, checked 2026-10-05.
- [Exclusive XML Canonicalization Version 1.0](https://www.w3.org/TR/xml-exc-c14n/): W3C Recommendation, 18 July 2002, checked 2026-10-05.
- [XML Signature Best Practices (BP)](https://www.w3.org/TR/xmldsig-bestpractices/): W3C Working Group Note, 11 April 2013, checked 2026-10-05.
