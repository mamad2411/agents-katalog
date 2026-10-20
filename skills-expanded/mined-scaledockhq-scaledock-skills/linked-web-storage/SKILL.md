---
name: linked-web-storage
description: >-
  Linked Web Storage: The Linked Web Storage Protocol specification aims to provide applications with secure and permissioned access to externally stored data in an interoperable way. Covers Linked Web Storage Protocol 1.0 (track), LWS 1.0 Authentication Suite: OpenID Connect (track), LWS 1.0 Authentication Suite: SAML 2.0 (track), LWS 1.0 Authentication Suite: Self-signed Identity using Controlled Identifiers (track). Use when reading or writing a Linked Web Storage pod, including the OpenID, SAML and CID authentication suites. Triggers: Linked Web Storage, LWS, solid pod.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Linked Web Storage

The Linked Web Storage Protocol specification aims to provide applications with secure and permissioned access to externally stored data in an interoperable way.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when reading or writing a Linked Web Storage pod, including the OpenID, SAML and CID authentication suites.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Linked Web Storage Protocol 1.0 (default, posture track); LWS 1.0 Authentication Suite: OpenID Connect (default, posture track); LWS 1.0 Authentication Suite: SAML 2.0 (default, posture track); LWS 1.0 Authentication Suite: Self-signed Identity using Controlled Identifiers (default, posture track). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **2.3 Conformance.** "The key words MAY , MUST , MUST NOT , OPTIONAL , RECOMMENDED , REQUIRED , SHOULD , and SHOULD NOT in this document are to be interpreted as described in BCP 14 [ RFC2119 ] [ RFC8174 ] when, and only when, they appear in all capitals, as shown here."
2. **2.3 Conformance.** "A LWS Server is an HTTP server [ rfc9112 ] that complies with all of the relevant " MUST " statements in this specification."
3. **2.3 Conformance.** "Specifically, the relevant normative " MUST " statements in 9."
4. **2.3 Conformance.** "Operations of this document MUST be respected."
5. **2.3 Conformance.** "An LWS Client is an HTTP client [ rfc9112 ] that complies with all of the relevant " MUST " statements in this specification."
6. **4.1 Authentication Credential Data Model.** "An authentication credential MUST include tamper evident claims about a subject, including: subject REQUIRED — an identifier for an end user."
7. **4.1 Authentication Credential Data Model.** "issuer REQUIRED — an identifier for the entity that issued the authentication credential ."
8. **4.1 Authentication Credential Data Model.** "client REQUIRED — an identifier for a client application."

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

- [Linked Web Storage Protocol 1.0](https://www.w3.org/TR/lws10-core/): Working Draft, lws10-core WD-lws10-core-20260921 (Working Draft, 2026-10-05), checked 2026-10-06.
- [LWS 1.0 Authentication Suite: OpenID Connect](https://www.w3.org/TR/lws10-authn-openid/): Working Draft, lws10-authn-openid WD-lws10-authn-openid-20260803 (Working Draft, 2026-08-03), checked 2026-10-06.
- [LWS 1.0 Authentication Suite: SAML 2.0](https://www.w3.org/TR/lws10-authn-saml/): Working Draft, lws10-authn-saml WD-lws10-authn-saml-20260803 (Working Draft, 2026-08-03), checked 2026-10-06.
- [LWS 1.0 Authentication Suite: Self-signed Identity using Controlled Identifiers](https://www.w3.org/TR/lws10-authn-ssi-cid/): Working Draft, lws10-authn-ssi-cid WD-lws10-authn-ssi-cid-20260921 (Working Draft, 2026-09-21), checked 2026-10-06.
- [Linked Web Storage Use Cases](https://www.w3.org/TR/lws-ucs/): Draft Note, lws-ucs (Draft Note, 2026-02-10), checked 2026-10-06.
- [Linked Web Storage Vocabulary](https://www.w3.org/TR/lws10-vocab/): Draft Note, lws10-vocab (Draft Note, 2026-07-14), checked 2026-10-06.
