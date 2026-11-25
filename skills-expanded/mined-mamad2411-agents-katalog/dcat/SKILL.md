---
name: dcat
description: >-
  DCAT: DCAT is an RDF vocabulary designed to facilitate interoperability between data catalogs published on the Web. Covers Data Catalog Vocabulary (DCAT) - Version 3. Use when describing a data catalog. Triggers: DCAT, Data Catalog Vocabulary.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# DCAT

DCAT is an RDF vocabulary designed to facilitate interoperability between data catalogs published on the Web. This document defines the schema and provides examples for its use. DCAT enables a publisher to describe datasets and data services in a catalog using a standard model and vocabulary that facilitates the consumption and aggregation of metadata from multiple catalogs. This can increase the discoverability of datasets and data services. It also makes it possible to have a decentralized approach to publishing data catalogs and makes federated search for datasets across catalogs in multiple sites possible using the same query mechanism and structure. Aggregated DCAT metadata can serve as

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when describing a data catalog.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Data Catalog Vocabulary (DCAT) - Version 3 (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **4. Conformance.** "The key words MAY , MUST , MUST NOT , and SHOULD in this document are to be interpreted as described in BCP 14 [ RFC2119 ] [ RFC8174 ] when, and only when, they appear in all capitals, as shown here."
2. **6.2.2 Element definitions.** "The definitions (including domain and range) of terms outside the DCAT namespace are provided here only for convenience and MUST NOT be considered normative."
3. **6.3.1 Property: homepage.** "Range: foaf:Document Usage note: foaf:homepage is an inverse functional property (IFP) which means that it MUST be unique and precisely identify the Web-page for the resource."
4. **6.4 Class: Cataloged Resource.** "The instances of this class SHOULD be included in a catalog."
5. **6.4.2 Property: conforms to.** "Range: dcterms:Standard ("A basis for comparison; a reference point against which other things can be evaluated." [ DCTERMS ]) Usage note: This property SHOULD be used to indicate the model, schema, ontology, view or profile that the cataloged resource content conforms to."
6. **6.4.7 Property: release date.** "Usage note: This property SHOULD be set using the first known date of issuance."
7. **6.4.9 Property: language.** "This refers to the natural language used for textual metadata (i.e., titles, descriptions, etc.) of a cataloged resource (i.e., dataset or service) or the textual values of a dataset distribution Range: dcterms:LinguisticSystem Resources defined by the Library of Congress ( ISO 639-1 , ISO 639-2 ) SHOULD be used."
8. **6.4.9 Property: language.** "If a ISO 639-1 (two-letter) code is defined for language, then its corresponding IRI SHOULD be used; if no ISO 639-1 code is defined, then IRI corresponding to the ISO 639-2 (three-letter) code SHOULD be used."

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

- [Data Catalog Vocabulary (DCAT) - Version 3](https://www.w3.org/TR/vocab-dcat-3/): Recommendation, vocab-dcat-3 REC-vocab-dcat-3-20200204 (Recommendation, 2024-08-22), checked 2026-10-06.
