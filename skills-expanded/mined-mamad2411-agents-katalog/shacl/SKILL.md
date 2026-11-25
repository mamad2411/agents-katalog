---
name: shacl
description: >-
  SHACL: This document defines the SHACL Shapes Constraint Language, a language for validating RDF graphs against a set of conditions. Covers Shapes Constraint Language (SHACL), SHACL 1.2 Core (track preview). Use when validating an RDF graph with shapes. Triggers: SHACL, SHACL 1.2.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# SHACL

This document defines the SHACL Shapes Constraint Language, a language for validating RDF graphs against a set of conditions. These conditions are provided as shapes and other constructs expressed in the form of an RDF graph. RDF graphs that are used in this manner are called "shapes graphs" in SHACL and the RDF graphs that are validated against a shapes graph are called "data graphs". As SHACL shape graphs are used to validate that data graphs satisfy a set of conditions they can also be viewed as a description of the data graphs that do satisfy these conditions. Such descriptions may be used for a variety of purposes beside validation, including user interface building, code generation and

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when validating an RDF graph with shapes.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Shapes Constraint Language (SHACL) (default); SHACL 1.2 Core (preview, posture track: emit only when the user opts in and the posture is build). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **1.1 Terminology.** "All SHACL implementations MUST at least implement SHACL Core."
2. **1.3 Conformance.** "The key words MAY , MUST , MUST NOT , and SHOULD are to be interpreted as described in [ RFC2119 ]."
3. **1.5 Relationship between SHACL and RDFS inferencing.** "If a shapes graph contains any triple with the predicate sh:entailment and object E and the SHACL processor does not support E as an entailment regime for the given data graph then the processor MUST signal a failure ."
4. **1.5 Relationship between SHACL and RDFS inferencing.** "Otherwise, the SHACL processor MUST provide the entailments for all of the values of sh:entailment in the shapes graph , and any inferred triples MUST be returned by all queries against the data graph during the validation process."
5. **2.3.2.1 sh:name and sh:description.** "If present, tools SHOULD prefer those locally specified labels over globally specified labels at the rdf:Property itself."
6. **2.3.2.1 sh:name and sh:description.** "For example, if a form displays a node that is in the target of a given property shape with an sh:name , then the tool SHOULD use the provided name."
7. **3.1 Shapes Graph.** "As a pre-validation step, SHACL processors SHOULD extend the originally provided shapes graph by transitively following and importing all referenced shapes graphs through the owl:imports predicate."
8. **3.1 Shapes Graph.** "The resulting graph forms the input shapes graph for validation and MUST NOT be further modified during the validation process."

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

- [Shapes Constraint Language (SHACL)](https://www.w3.org/TR/shacl/): Recommendation, shacl REC-shacl-20170720 (Recommendation, 2017-07-20), checked 2026-10-06.
- [SHACL 1.2 Core](https://www.w3.org/TR/shacl12-core/): Working Draft, shacl12-core REC-shacl-20170720 (Working Draft, 2026-09-18), checked 2026-10-06.
