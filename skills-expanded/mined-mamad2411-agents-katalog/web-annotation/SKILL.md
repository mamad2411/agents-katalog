---
name: web-annotation
description: >-
  Web Annotation: Annotations are typically used to convey information about a resource or associations between resources. Covers Web Annotation Data Model, Web Annotation Protocol, Web Annotation Vocabulary. Use when creating or exchanging annotations. Triggers: Web Annotation.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Web Annotation

Annotations are typically used to convey information about a resource or associations between resources. Simple examples include a comment or tag on a single web page or image, or a blog post about a news article. The Web Annotation Data Model specification describes a structured model and format to enable annotations to be shared and reused across different hardware and software platforms. Common use cases can be modeled in a manner that is simple and convenient, while at the same time enabling more complex requirements, including linking arbitrary content to a particular data point or to segments of timed multimedia resources. The specification provides a specific JSON format for ease of c

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when creating or exchanging annotations.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Web Annotation Data Model (default); Web Annotation Protocol (default); Web Annotation Vocabulary (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **1.3 Conformance.** "The key words MAY , MUST , MUST NOT , NOT RECOMMENDED , RECOMMENDED , SHOULD , and SHOULD NOT are to be interpreted as described in [ RFC2119 ]."
2. **1.3.1 Conformance Requirements Related to Selectors.** "A conforming implementation MUST implement that particular combination if it handles the corresponding media type."
3. **1.3.1 Conformance Requirements Related to Selectors.** "Conforming implementations SHOULD ignore that particular combination."
4. **1.4 Terminology.** "Web Resource A Resource that MUST be identified by an IRI , as described in the Web Architecture [ webarch ]."
5. **Model.** "The Annotation MUST have 1 or more @context values and http://www.w3.org/ns/anno.jsonld MUST be one of them."
6. **Model.** "If there is only one value, then it MUST be provided as a string."
7. **Model.** "An Annotation MUST have exactly 1 IRI that identifies it."
8. **Model.** "An Annotation MUST have 1 or more types, and the Annotation class MUST be one of them."

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

- [Web Annotation Data Model](https://www.w3.org/TR/annotation-model/): Recommendation, annotation-model REC-annotation-model-20170223 (Recommendation, 2017-02-23), checked 2026-10-06.
- [Web Annotation Protocol](https://www.w3.org/TR/annotation-protocol/): Recommendation, annotation-protocol REC-annotation-protocol-20170223 (Recommendation, 2017-02-23), checked 2026-10-06.
- [Web Annotation Vocabulary](https://www.w3.org/TR/annotation-vocab/): Recommendation, annotation-vocab REC-annotation-vocab-20170223 (Recommendation, 2017-02-23), checked 2026-10-06.
