---
name: intersection-observer
description: >-
  Intersection Observer: This specification describes an API that can be used to understand the visibility and position of DOM elements ("targets") relative to a containing element or to the top-level viewport ("root"). Covers Intersection Observer (track). Use when observing element visibility. Triggers: IntersectionObserver.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Intersection Observer

This specification describes an API that can be used to understand the visibility and position of DOM elements ("targets") relative to a containing element or to the top-level viewport ("root"). The position is delivered asynchronously and is useful for understanding the visibility of elements and implementing pre-loading and deferred loading of DOM content.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when observing element visibility.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Intersection Observer (default, posture track). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **Document conventions.** "The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in the normative parts of this document are to be interpreted as described in RFC 2119."
2. **2.2. The IntersectionObserver interface.** "Any target of an explicit root observer is also a same-origin-domain target , since the target must be in the same document as the intersection root ."
3. **2.3. The IntersectionObserverEntry interface.** "time , of type DOMHighResTimeStamp , readonly The attribute must return a DOMHighResTimeStamp that corresponds to the time the intersection was recorded, relative to the time origin of the global object associated with the IntersectionObserver instance that generated the notification."
4. **2.4. The IntersectionObserverInit dictionary.** "Threshold values must be in the range of [0, 1.0] and represent a percentage of the area of the rectangle produced by getting the bounding box for target ."
5. **3. Processing Model.** "This section outlines the steps the user agent must take when implementing the Intersection Observer API."
6. **3.4.2. Pending initial IntersectionObserver targets.** "In the HTML Event Loops Processing Model , under the " Update the rendering " step, the " Unnecessary rendering " step should be modified to add an additional requirement for skipping the rendering update: The document does not have pending initial IntersectionObserver targets ."
7. **5. Privacy and Security.** "It should be noted that prior to IntersectionObserver , web developers used other API’s in very ingenious (and grotesque) ways to tease out the information available from IntersectionObserver ."
8. **Conformant Algorithms.** "Requirements phrased in the imperative as part of algorithms (such as "strip any leading space characters" or "return false and abort these steps") are to be interpreted with the meaning of the key word ("must", "should", "may", etc) used in introducing the algorithm."

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

- [Intersection Observer](https://www.w3.org/TR/intersection-observer/): Working Draft, intersection-observer WD-intersection-observer-20231018 (Working Draft, 2023-10-18), checked 2026-10-06.
