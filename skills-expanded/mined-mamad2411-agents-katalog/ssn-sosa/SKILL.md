---
name: ssn-sosa
description: >-
  SSN and SOSA: The Semantic Sensor Network (SSN) ontology is an ontology for describing sensors and their observations, the involved procedures, the studied features of interest, the samples used to do so, and the observed properties, as well as actuators. Covers Semantic Sensor Network Ontology Level 2017, Semantic Sensor Network Ontology - 2023 Edition (track preview). Use when describing sensors, observations or samples. Triggers: SSN, SOSA.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# SSN and SOSA

The Semantic Sensor Network (SSN) ontology is an ontology for describing sensors and their observations, the involved procedures, the studied features of interest, the samples used to do so, and the observed properties, as well as actuators. SSN follows a horizontal and vertical modularization architecture by including a lightweight but self-contained core ontology called SOSA (Sensor, Observation, Sample, and Actuator) for its elementary classes and properties. With their different scope and different degrees of axiomatization, SSN and SOSA are able to support a wide range of applications and use cases, including satellite imagery, large-scale scientific monitoring, industrial and household

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when describing sensors, observations or samples.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Semantic Sensor Network Ontology Level 2017 (default); Semantic Sensor Network Ontology - 2023 Edition (preview, posture track: emit only when the user opts in and the posture is build). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **7.4 Generic or Specific Instances of ssn:Property.** "On the other hand, one SHOULD NOT use OWL punning to make ex:Temperature denote both a subclass of ssn:Property and an instance of ssn:Property ."
2. **7.5 Generic or Specific Instances of ssn:System.** "On the other hand, one SHOULD NOT use OWL punning to make ex:Temperature denote both a subclass of ssn:Property and an instance of ssn:Property."
3. **2. Modularization.** "This means, that the result of certain reasoning tasks such as subsumption or query answering within a single module should be possible and result in the same answers without the need to access other modules of the ontology."
4. **3. Origins of SSN and SOSA.** "SensorML provides extensive support for serialization of numeric data arrays and is particularly optimized for data that includes multiple parallel streams that must be processed together."
5. **3. Origins of SSN and SOSA.** "For example, the data collected by cameras on airborne vehicles must be geo-referenced based on the instantaneous position of the platform and orientation of the camera."
6. **4.3.2.3 sosa:observedProperty.** "The ObservableProperty should be a property of the FeatureOfInterest (linked by hasFeatureOfInterest ) of this Observation ."
7. **7.3 Quantity Values and Unit of Measures.** "Such a datatype should be supported by RDF and SPARQL engines to support the comparison of quantity values."
8. **7.4 Generic or Specific Instances of ssn:Property.** "This specification does not specify whether an instance of ssn:Property should be generic to all features of interest (e.g., ex:Temperature , ex:OnOffStatus ), or specific to a single feature of interest (e.g., <myBodyTemperature> , <LightStatus> )."

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

- [Semantic Sensor Network Ontology](https://www.w3.org/TR/vocab-ssn-2017/): Recommendation, vocab-ssn-2017 REC-vocab-ssn-20171019 (Recommendation, 2017-10-19), checked 2026-10-06.
- [Semantic Sensor Network Ontology - 2023 Edition](https://www.w3.org/TR/vocab-ssn-2023/): Working Draft, vocab-ssn-2023 REC-vocab-ssn-20171019 (Working Draft, 2026-10-03), checked 2026-10-06.
