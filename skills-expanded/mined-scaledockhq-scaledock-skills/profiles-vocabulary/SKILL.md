---
name: profiles-vocabulary
description: >-
  Profiles Vocabulary: The Profiles Vocabulary is an RDF vocabulary created to allow the machine-readable description of profiles of standards for information resources. Covers The Profiles Vocabulary 1.0 (track), Content Negotiation by Profile (track). Use when negotiating or describing a profile. Triggers: DX Prof, content negotiation by profile.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Profiles Vocabulary

The Profiles Vocabulary is an RDF vocabulary created to allow the machine-readable description of profiles of standards for information resources. It can be used to describe profile hierarchies wherein profiles of standards may themselves have profiles indicated. It can also be used to link together multiple profile resources that make up a profile - guidelines, validation tools, schemas, term lists and so on - and it allows for those profile resources to be described with formats, roles, and digital artifacts. The namespace for PROF terms is http://www.w3.org/ns/dx/prof/ . The PROF vocabulary, defined in OWL and encoded in RDF Turtle, is available at prof.ttl .

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when negotiating or describing a profile.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: The Profiles Vocabulary 1.0 (default, posture track); Content Negotiation by Profile (default, posture track). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **1.1 Profile background.** "Data that conforms to a profile, in PROF, must conform to anything the profile is a profile of."
2. **6.2 Data Catalog Vocabulary (DCAT).** "No normative alignment between DCAT & PROF is presented in this document however they can and should be used together and informative alignment between them (with revised DCAT [ VOCAB-DCAT-2 ]) is given in C.1 Dataset Catalogue Vocabulary ."
3. **6.3 Asset Description Metadata Schema (ADMS).** "As with DCAT, PROF can and should be used with ADMS however no normative alignment between them is presented here but an informative alignment is given in C.2 Asset Description Metadata Schema ."
4. **7. Conceptual Model.** "Resource Descriptor s must indicate the role they play (to guide, to validate etc.), the formalism they adhere to ( dct:format ) and any dct:Standard that they themselves conform to ( dct:conformsTo )."
5. **8.3.3 Property: isTransitiveProfileOf.** "If this property is used, then all such relationships should be present so a client can safely avoid hierarchy traversal."
6. **8.3.3 Property: isTransitiveProfileOf.** "While this vocabulary provides this prof:isProfileOf & prof:isTransitiveProfileOf pair of properties, it does not specify how a particular implementation of a Profile that is related to another Profile or Standard by prof:isTransitiveProfileOf should implement specific inferences."
7. **8.4.5 Property: isInheritedFrom.** "If this property is present, it should be used consistently and all relevant profile resources a client may need to utilise the profile should be present and described using this predicate Issue 18 : Replace isInheritedFrom with a subproperty of rdfs:isDefinedBy Proposal: replace isInhertiedFrom with a more general property that allows any ResourceDescriptor to directly indicate the Profile that…"
8. **8.5 Class: ResourceRole.** "OWL Class prof:ResourceRole Label: Resource Role Definition: A role that an profile resource, described by a Resource Descriptor, plays Sub class of: skos:Concept Usage note: Specific terms must come from a vocabulary."

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

- [The Profiles Vocabulary 1.0](https://www.w3.org/TR/dx-prof-1.0/): Working Draft, dx-prof-1.0 NOTE-dx-prof-20191218 (Working Draft, 2026-09-15), checked 2026-10-06.
- [Content Negotiation by Profile](https://www.w3.org/TR/dx-prof-conneg/): Working Draft, dx-prof-conneg WD-dx-prof-conneg-20260921 (Working Draft, 2026-09-21), checked 2026-10-06.
