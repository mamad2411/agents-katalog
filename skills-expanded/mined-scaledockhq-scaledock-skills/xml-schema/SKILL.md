---
name: xml-schema
description: >-
  XML Schema: This document specifies the XML Schema Definition Language, which offers facilities for describing the structure and constraining the contents of XML documents, including those which exploit the XML Namespace facility. Covers W3C XML Schema Definition Language (XSD) 1.1 Part 1: Structures, W3C XML Schema Definition Language (XSD) 1.1 Part 2: Datatypes. Use when validating XML with XSD. Triggers: XSD, XML Schema.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.2.0"
  kind: standard
---

# XML Schema

This document specifies the XML Schema Definition Language, which offers facilities for describing the structure and constraining the contents of XML documents, including those which exploit the XML Namespace facility. The schema language, which is itself represented in an XML vocabulary and uses namespaces, substantially reconstructs and considerably extends the capabilities found in XML document type definitions (DTDs). This specification depends on XML Schema Definition Language 1.1 Part 2: Datatypes .

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when validating XML with XSD.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: W3C XML Schema Definition Language (XSD) 1.1 Part 1: Structures (default); XML Schema Part 1: Structures Second Edition (legacy: read and upgrade, never author); W3C XML Schema Definition Language (XSD) 1.1 Part 2: Datatypes (default); XML Schema Part 2: Datatypes Second Edition (legacy: read and upgrade, never author). XML Schema Part 0: Primer Second Edition is the non-normative XML Schema 1.0 primer, W3C Recommendation 28 October 2004, and is legacy. See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **Part 1 § 1.5.** "Except as otherwise specified, processors must distinguish error-free (conforming) schemas and schema documents used in ·assessment· from those with errors;"
2. **Part 1 § 1.5.** "if a schema used in ·assessment· or a schema document used in constructing a schema is in error, processors must report the fact; if more than one is in error, it is ·implementation-dependent· whether more than one is reported as being in error."
3. **Part 1 § 3.2.3.** "default and fixed must not both be present."
4. **Part 1 § 3.2.6.4.** "The {target namespace} of an attribute declaration, whether local or top-level, must not match http://www.w3.org/2001/XMLSchema-instance (unless it is one of the four built-in declarations given in the next section)."
5. **Part 1 § 3.8.6.4.** "A content model must not contain two ·element particles· which ·compete· with each other, nor two ·wildcard particles· which ·compete· with each other."
6. **Part 1 § 4.2.1.** "The schemaLocation attributes on the `<include>`, `<override>`, and `<redefine>` elements in a schema document, on the other hand, are not hints: conforming processors must attempt to de-reference the schema document named by the attribute."
7. **Part 2 § 2.4.1.3.** "The ·transitive membership· of a ·union· must not contain the ·union· itself, nor any datatype ·derived· or ·constructed· from the ·union·."
8. **Part 2 § 2.4.2.** "As normatively specified elsewhere, conforming processors must support all the primitive datatypes defined in this specification; it is ·implementation-defined· whether other primitive datatypes are supported."
9. **Part 2 § 2.4.3.** "A datatype must not be ·derived· from itself."

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

- [W3C XML Schema Definition Language (XSD) 1.1 Part 1: Structures](https://www.w3.org/TR/xmlschema11-1/): Recommendation, xmlschema11-1 REC-xmlschema11-1-20120405 (Recommendation, 2012-04-05), checked 2026-10-06.
- [XML Schema Part 1: Structures Second Edition](https://www.w3.org/TR/xmlschema-1/): Recommendation, xmlschema-1 REC-xmlschema-1-20041028 (Recommendation, 2004-10-28), checked 2026-10-06.
- [W3C XML Schema Definition Language (XSD) 1.1 Part 2: Datatypes](https://www.w3.org/TR/xmlschema11-2/): Recommendation, xmlschema11-2 REC-xmlschema11-2-20120405 (Recommendation, 2012-04-05), checked 2026-10-06.
- [XML Schema Part 2: Datatypes Second Edition](https://www.w3.org/TR/xmlschema-2/): Recommendation, xmlschema-2 REC-xmlschema-2-20041028 (Recommendation, 2004-10-28), checked 2026-10-06.
- [XML Schema Part 0: Primer Second Edition](https://www.w3.org/TR/xmlschema-0/): Recommendation, W3C Recommendation 28 October 2004, checked 2026-10-06.
