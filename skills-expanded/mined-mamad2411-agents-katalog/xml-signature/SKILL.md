---
name: xml-signature
description: >-
  XML Signature: This document specifies XML digital signature processing rules and syntax. Covers XML Signature Syntax and Processing Version 1.1, Canonical XML Version 1.1, Exclusive XML Canonicalization Version 1.0. Use when signing or verifying XML. Triggers: XML Signature, XML-DSig, C14N.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.1"
  kind: standard
---

# XML Signature

This document specifies XML digital signature processing rules and syntax. XML Signatures provide integrity , message authentication , and/or signer authentication services for data of any type, whether located within the XML that includes the signature or elsewhere.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when signing or verifying XML.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: XML Signature Syntax and Processing Version 1.1 (default); XML Signature Syntax and Processing (Second Edition) (legacy: read and upgrade, never author); Canonical XML Version 1.1 (default); Canonical XML Version 1.0 (legacy: read and upgrade, never author); Exclusive XML Canonicalization Version 1.0 (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **1.1 Conformance.** "The key words " MUST ", " MUST NOT ", " REQUIRED ", " SHALL ", " SHALL NOT ", " SHOULD ", " SHOULD NOT ", " RECOMMENDED ", " MAY ", and " OPTIONAL " in this specification are to be interpreted as described in [ RFC2119 ]."
2. **1.1 Conformance.** ""They MUST only be used where it is actually required for interoperation or to limit behavior which has potential for causing harm (e.g., limiting retransmissions)" Consequently, we use these capitalized key words to unambiguously specify requirements over protocol and application features and behavior that affect the interoperability and security of implementations."
3. **1.1 Conformance.** "For instance, an XML attribute might be described as being "optional." Compliance with the Namespaces in XML specification [ XML-NAMES ] is described as " REQUIRED ." This document specifies optional and mandatory to support algorithms, providing references for these algorithms."
4. **1.3 Versions, Namespaces and Identifiers.** "Implementations of this specification MUST use the following XML namespace URIs: URI namespace prefix XML internal entity http://www.w3.org/2000/09/xmldsig# default namespace , ds: , dsig: <!ENTITY dsig "http://www.w3.org/2000/09/xmldsig#"> http://www.w3.org/2009/xmldsig11# dsig11: <!ENTITY dsig11 "http://www.w3.org/2009/xmldsig11#"> While implementations MUST support XML and XML namespaces, and…"
5. **1.3 Versions, Namespaces and Identifiers.** "Implementations of this specification MUST be fully interoperable with the algorithms specified in [ RFC6931 ], but MAY compute the requisite values through any technique that leads to the same output."
6. **2.1 Simple Example ( Signature ,.** "To promote application interoperability we specify a set of signature algorithms that MUST be implemented, though their use is at the discretion of the signature creator."
7. **2.2 Extended Example ( Object and SignatureProperty ).** "References to an XML data element within an Object element SHOULD identify the actual element pointed to."
8. **2.2 Extended Example ( Object and SignatureProperty ).** "content is not XML (perhaps it is binary or encoded data) the reference should identify the Object and the Reference Type , if given, SHOULD indicate Object ."

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

- `saml`, when the work also follows that specification: `npx skills add ScaleDockHQ/scaledock-skills --skill saml`

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [XML Signature Syntax and Processing Version 1.1](https://www.w3.org/TR/xmldsig-core1/): Recommendation, xmldsig-core1 REC-xmldsig-core1-20130411 (Recommendation, 2013-04-11), checked 2026-10-06.
- [XML Signature Syntax and Processing (Second Edition)](https://www.w3.org/TR/xmldsig-core/): Recommendation, xmldsig-core REC-xmldsig-core1-20130411 (Recommendation, 2008-06-10), checked 2026-10-06.
- [Canonical XML Version 1.1](https://www.w3.org/TR/xml-c14n11/): Recommendation, xml-c14n11 REC-xml-c14n11-20080502 (Recommendation, 2008-05-02), checked 2026-10-06.
- [Canonical XML Version 1.0](https://www.w3.org/TR/xml-c14n/): Recommendation, xml-c14n10 REC-xml-c14n11-20080502 (Recommendation, 2001-03-15), checked 2026-10-06.
- [Exclusive XML Canonicalization Version 1.0](https://www.w3.org/TR/xml-exc-c14n/): Recommendation, xml-exc-c14n REC-xml-exc-c14n-20020718 (Recommendation, 2002-07-18), checked 2026-10-06.
