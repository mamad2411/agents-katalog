---
name: presentation-api
description: >-
  Presentation API: This specification defines an API to enable Web content to access presentation displays and use them for presenting Web content. Covers Presentation API (build). Use when presenting content on a second screen. Triggers: Presentation API, PresentationRequest.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Presentation API

This specification defines an API to enable Web content to access presentation displays and use them for presenting Web content.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when presenting content on a second screen.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Presentation API (default, posture build). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **3. Conformance.** "The key words MAY , MUST , MUST NOT , OPTIONAL , SHOULD , and SHOULD NOT in this document are to be interpreted as described in BCP 14 [ RFC2119 ] [ RFC8174 ] when, and only when, they appear in all capitals, as shown here."
2. **3. Conformance.** "Requirements phrased in the imperative as part of algorithms (such as "strip any leading space characters" or "return false and terminate these steps") are to be interpreted with the meaning of the key word (" MUST ", " SHOULD ", " MAY ", etc.) used in introducing the algorithm."
3. **6.1.** "When an algorithm queues a Presentation API task T , the user agent MUST queue a global task T on the presentation task source using the global object of the current realm ."
4. **6.2.** "It MUST return the Presentation instance."
5. **6.2.1.** "Controlling user agent Controlling user agents MUST implement the following partial interface: WebIDL partial interface Presentation { attribute PresentationRequest ?"
6. **6.2.1.** "defaultRequest ; }; The defaultRequest attribute MUST return the default presentation request if any, null otherwise."
7. **6.2.1.** "On setting, the default presentation request MUST be set to the new value."
8. **6.2.1.** "The controlling user agent SHOULD initiate presentation using the default presentation request only when the user has expressed an intention to do so via a user gesture, for example by clicking a button in the browser chrome."

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

- [Presentation API](https://www.w3.org/TR/presentation-api/): Candidate Recommendation Draft, presentation-api CRD-presentation-api-20250212 (Candidate Recommendation Draft, 2025-02-12), checked 2026-10-06.
