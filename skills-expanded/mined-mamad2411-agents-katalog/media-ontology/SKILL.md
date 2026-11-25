---
name: media-ontology
description: >-
  Ontology for Media Resources: This document defines the Ontology for Media Resources 1.0. Covers Ontology for Media Resources 1.0, Metadata API for Media Resources 1.0. Use when describing media resources. Triggers: Media Ontology, ma-ont.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Ontology for Media Resources

This document defines the Ontology for Media Resources 1.0. The term "Ontology" is used in its broadest possible definition: a core vocabulary. The intent of this vocabulary is to bridge the different descriptions of media resources, and provide a core set of descriptive properties. This document defines a core set of metadata properties for media resources, along with their mappings to elements from a set of existing metadata formats. Besides that, the document presents a Semantic Web compatible implementation of the abstract ontology using RDF/OWL. The document is mostly targeted towards media resources available on the Web, as opposed to media resources that are only accessible in local r

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when describing media resources.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Ontology for Media Resources 1.0 (default); Metadata API for Media Resources 1.0 (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **2 Conformance.** "For normative sections only, the keywords "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "RECOMMENDED", "MAY", and "OPTIONAL" are to be interpreted as described in RFC2119 [ RFC 2119 ]."
2. **2 Conformance.** "To facilitate the differentiation between the normative use of these terms as defined in RFC2119 and a non-normative use of these terms, the normative use of these terms MUST occur in all capital letters."
3. **2 Conformance.** "A "strictly conforming" application is one that satisfies all "MUST" and "SHALL" provisions in this document."
4. **2 Conformance.** "In contrast, a "conditionally conforming" application is one that satisfies all "MUST" provisions in this document, but not all "SHALL" provisions."
5. **2 Conformance.** "It should be noted that an application that does not specify all "MUST" provisions in this document is not conforming"."
6. **4.** "Applications that wish to be conformant with this specification MUST use the data types specified in this section for property values that are defined in this specification."
7. **4.1 URI.** "Hence, in this specification, the term "URI" MUST be interpreted to also include IRI."
8. **4.2 String.** "A String value MUST be represented using the XML Schema string data type."

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

- [Ontology for Media Resources 1.0](https://www.w3.org/TR/mediaont-10/): Recommendation, mediaont-10 REC-mediaont-10-20120209 (Recommendation, 2012-02-09), checked 2026-10-06.
- [Metadata API for Media Resources 1.0](https://www.w3.org/TR/mediaont-api-1.0/): Recommendation, mediaont-api-1.0 REC-mediaont-api-1.0-20140313 (Recommendation, 2014-03-13), checked 2026-10-06.
