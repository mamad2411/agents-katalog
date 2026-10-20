---
name: web-of-things
description: >-
  Web of Things: The W3C Web of Things (WoT) enables interoperability across IoT platforms and application domains. Covers Web of Things (WoT) Architecture 1.1, Web of Things (WoT) Thing Description 1.1, Web of Things (WoT) Thing Description 2.0 (track preview), Web of Things (WoT) Discovery, Web of Things (WoT) Profiles (track). Use when describing or discovering a Thing. Triggers: WoT, Thing Description.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Web of Things

The W3C Web of Things (WoT) enables interoperability across IoT platforms and application domains. The goal of the WoT is to preserve and complement existing IoT standards and solutions. The W3C WoT architecture is designed to describe what exists, and only prescribes new mechanisms when necessary. This WoT Architecture specification describes the abstract architecture for the W3C Web of Things. This abstract architecture is based on requirements that were derived from use cases for multiple application domains.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when describing or discovering a Thing.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Web of Things (WoT) Architecture 1.1 (default); Web of Things (WoT) Architecture Level 1.0 (legacy: read and upgrade, never author); Web of Things (WoT) Thing Description 1.1 (default); Web of Things (WoT) Thing Description 2.0 (preview, posture track: emit only when the user opts in and the posture is build); Web of Things (WoT) Thing Description Level 1.0 (legacy: read and upgrade, never author); Web of Things (WoT) Discovery (default); Web of Things (WoT) Profiles (default, posture track). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **2..** "The key words MAY , MUST , MUST NOT , SHOULD , and SHOULD NOT in this document are to be interpreted as described in BCP 14 [ RFC2119 ] [ RFC8174 ] when, and only when, they appear in all capitals, as shown here."
2. **6.1.1.1 Thing Descriptions.** "In W3C WoT, the description metadata for a Thing instance MUST be available as a WoT Thing Description (TD) [ WOT-THING-DESCRIPTION ]."
3. **6.1.1.1 Thing Descriptions.** "To be considered a Thing , however, at least one TD representation MUST be available."
4. **6.1.2.** "Figure 17 Linked Things Things MUST be hosted on networked system components with a software stack to realize interaction through a network-facing interface, the WoT Interface of a Thing ."
5. **6.6.1.** "Extension relation types MUST be compared as strings using ASCII case-insensitive comparison, (c.f."
6. **6.6.1.** "Nevertheless, all-lowercase URIs SHOULD be used for extension relation types [ RFC8288 ]."
7. **6.6.2.** "Form contexts and submission targets MUST both be Internationalized Resource Identifiers (IRIs) [ RFC3987 ]."
8. **6.6.2.** "The request method MUST identify one method of the standard set of the protocol identified by the submission target URI scheme."

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

- [Web of Things (WoT) Architecture 1.1](https://www.w3.org/TR/wot-architecture11/): Recommendation, wot-architecture11 REC-wot-architecture-20200409 (Recommendation, 2023-12-05), checked 2026-10-06.
- [Web of Things (WoT) Architecture](https://www.w3.org/TR/wot-architecture10/): Recommendation, wot-architecture10 CR-wot-architecture-20190516 (Recommendation, 2020-04-09), checked 2026-10-06.
- [Web of Things (WoT) Thing Description 1.1](https://www.w3.org/TR/wot-thing-description11/): Recommendation, wot-thing-description11 REC-wot-thing-description-20200409 (Recommendation, 2023-12-05), checked 2026-10-06.
- [Web of Things (WoT) Thing Description 2.0](https://www.w3.org/TR/wot-thing-description-2.0/): First Public Working Draft, wot-thing-description-2.0 REC-wot-thing-description11-20231205 (First Public Working Draft, 2025-11-04), checked 2026-10-06.
- [Web of Things (WoT) Thing Description](https://www.w3.org/TR/wot-thing-description10/): Recommendation, wot-thing-description10 REC-wot-thing-description-20200409 (Recommendation, 2020-04-09), checked 2026-10-06.
- [Web of Things (WoT) Discovery](https://www.w3.org/TR/wot-discovery/): Recommendation, wot-discovery REC-wot-discovery-20231205 (Recommendation, 2023-12-05), checked 2026-10-06.
- [Web of Things (WoT) Profiles](https://www.w3.org/TR/wot-profile/): Working Draft, wot-profile WD-wot-profile-20251104 (Working Draft, 2025-11-04), checked 2026-10-06.
- [Web of Things (WoT) Binding Registry](https://www.w3.org/TR/wot-binding-registry/): Draft Registry, wot-binding-registry (Draft Registry, 2025-11-04), checked 2026-10-06.
