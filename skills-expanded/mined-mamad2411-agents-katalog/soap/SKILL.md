---
name: soap
description: >-
  SOAP: SOAP Version 1.2 is a lightweight protocol intended for exchanging structured information in a decentralized, distributed environment. Covers SOAP Version 1.2 Part 0: Primer (Second Edition), SOAP Version 1.2 Part 1: Messaging Framework (Second Edition), SOAP Version 1.2 Part 2: Adjuncts (Second Edition), Web Services Description Language (WSDL) Version 2.0 Part 1: Core Language, Web Services Addressing 1.0 - Core, SOAP over Java Message Service 1.0. Use when building a SOAP service. Triggers: SOAP 1.2, WSDL 2.0.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# SOAP

SOAP Version 1.2 is a lightweight protocol intended for exchanging structured information in a decentralized, distributed environment. "Part 1: Messaging Framework" defines, using XML technologies, an extensible messaging framework containing a message construct that can be exchanged over a variety of underlying protocols.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when building a SOAP service.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: SOAP Version 1.2 Part 1: Messaging Framework (Second Edition) (default); SOAP Version 1.2 Part 2: Adjuncts (Second Edition) (default); Web Services Description Language (WSDL) Version 2.0 Part 1: Core Language (default); Web Services Addressing 1.0 - Core (default); SOAP over Java Message Service 1.0 (default). SOAP Version 1.2 Part 0: Primer (Second Edition) is the non-normative tutorial, W3C Recommendation 27 April 2007. See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **1.1 Notational Conventions.** "The keywords "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in RFC 2119 [RFC 2119] ."
2. **1.2 Conformance.** "For an implementation to claim conformance with the SOAP Version 1.2 specification, it MUST correctly implement all mandatory ("MUST") requirements expressed in Part 1 of the SOAP Version 1.2 specification (this document) that pertain to the activity being performed."
3. **1.2 Conformance.** "The implementation of an Adjunct MUST implement all the pertinent mandatory requirements expressed in the specification of the Adjunct to claim conformance with the Adjunct."
4. **1.3 Relation to Other Specifications.** "The values associated with element and attribute information items defined in this specification MUST be carried explicitly in the transmitted SOAP message except where stated otherwise (see 5."
5. **1.3 Relation to Other Specifications.** "The media type "application/soap+xml" SHOULD be used for XML 1.0 serializations of the SOAP message infoset (see SOAP 1.2 Part 2 [SOAP Part 2] , The "application/soap+xml" Media Type )."
6. **2.1 SOAP Nodes.** "A SOAP node receiving a SOAP message MUST perform processing according to the SOAP processing model as described in this section and in the remainder of this specification."
7. **2.2 SOAP Roles and SOAP Nodes.** "The roles assumed by a node MUST be invariant during the processing of an individual SOAP message."
8. **2.2 SOAP Roles and SOAP Nodes.** "Table 2: SOAP Roles defined by this specification Short-name Name Description next "http://www.w3.org/2003/05/soap-envelope/role/next" Each SOAP intermediary and the ultimate SOAP receiver MUST act in this role."

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

- [SOAP Version 1.2 Part 1: Messaging Framework (Second Edition)](https://www.w3.org/TR/soap12-part1/): Recommendation, soap12-part1 REC-soap12-part1-20070427 (Recommendation, 2007-04-27), checked 2026-10-06.
- [SOAP Version 1.2 Part 2: Adjuncts (Second Edition)](https://www.w3.org/TR/soap12-part2/): Recommendation, soap12-part2 REC-soap12-part2-20070427 (Recommendation, 2007-04-27), checked 2026-10-06.
- [Web Services Description Language (WSDL) Version 2.0 Part 1: Core Language](https://www.w3.org/TR/wsdl20/): Recommendation, wsdl20 REC-wsdl20-adjuncts-20070626 (Recommendation, 2007-06-26), checked 2026-10-06.
- [Web Services Addressing 1.0 - Core](https://www.w3.org/TR/ws-addr-core/): Recommendation, ws-addr-core REC-xml-infoset-20040204 (Recommendation, 2006-05-09), checked 2026-10-06.
- [SOAP over Java Message Service 1.0](https://www.w3.org/TR/soapjms/): Recommendation, soapjms REC-soapjms-20120216 (Recommendation, 2012-02-16), checked 2026-10-06.
- [SOAP Version 1.2 Part 0: Primer (Second Edition)](https://www.w3.org/TR/soap12-part0/): Recommendation, W3C Recommendation 27 April 2007, checked 2026-10-06.
