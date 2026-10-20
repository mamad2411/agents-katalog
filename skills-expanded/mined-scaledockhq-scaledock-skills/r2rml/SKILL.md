---
name: r2rml
description: >-
  R2RML: This document describes R2RML, a language for expressing customized mappings from relational databases to RDF datasets. Covers R2RML: RDB to RDF Mapping Language, A Direct Mapping of Relational Data to RDF. Use when mapping relational data to RDF. Triggers: R2RML, Direct Mapping.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# R2RML

This document describes R2RML, a language for expressing customized mappings from relational databases to RDF datasets. Such mappings provide the ability to view existing relational data in the RDF data model, expressed in a structure and target vocabulary of the mapping author's choice. R2RML mappings are themselves RDF graphs and written down in Turtle syntax. R2RML enables different types of mapping implementations. Processors could, for example, offer a virtual SPARQL endpoint over the mapped relational data, or generate RDF dumps, or offer a Linked Data interface.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when mapping relational data to RDF.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: R2RML: RDB to RDF Mapping Language (default); A Direct Mapping of Relational Data to RDF (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **4 R2RML Processors and Mapping Documents.** "It MUST be established with sufficient privileges for read access to all base tables and views that are referenced in the R2RML mapping."
2. **4 R2RML Processors and Mapping Documents.** "It MUST be configured with a default catalog and default schema that will be used when tables and views are accessed without an explicit catalog or schema reference."
3. **4 R2RML Processors and Mapping Documents.** "It SHOULD NOT contain question mark (“ ?"
4. **4 R2RML Processors and Mapping Documents.** "”) or hash (“ # ”) characters and SHOULD end in a slash (“ / ”) character."
5. **4 R2RML Processors and Mapping Documents.** "When checking the input database, a data validator MUST report any data errors that are raised in the process of generating the output dataset."
6. **4.1 Mapping Graphs and the R2RML Vocabulary.** "The R2RML vocabulary is the set of IRIs defined in this specification that start with the rr: namespace IRI: http://www.w3.org/ns/r2rml# An R2RML mapping graph : SHOULD NOT include any IRIs that start with the rr: namespace IRI, but are not defined in the R2RML vocabulary ."
7. **4.1 Mapping Graphs and the R2RML Vocabulary.** "SHOULD NOT include IRIs from the R2RML vocabulary where such use is not explicitly allowed or required by a clause in this specification."
8. **4.1 Mapping Graphs and the R2RML Vocabulary.** "SHOULD contain only mapping components that are referenced by some triples map (in other words, all mapping components should actually be “used” in the mapping)."

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

- [R2RML: RDB to RDF Mapping Language](https://www.w3.org/TR/r2rml/): Recommendation, r2rml REC-r2rml-20120927 (Recommendation, 2012-09-27), checked 2026-10-06.
- [A Direct Mapping of Relational Data to RDF](https://www.w3.org/TR/rdb-direct-mapping/): Recommendation, rdb-direct-mapping REC-rdb-direct-mapping-20120927 (Recommendation, 2012-09-27), checked 2026-10-06.
