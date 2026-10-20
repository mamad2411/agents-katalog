---
name: performance-timeline
description: >-
  Performance Timeline: This specification extends the High Resolution Time specification [ HR-TIME-3 ] by providing methods to store and retrieve high resolution performance metric data. Covers Performance Timeline Level 1 (build), High Resolution Time Level 2, High Resolution Time Level 3 (track preview), Navigation Timing, Navigation Timing Level 2 (track preview), Resource Timing (build), User Timing Level 2, User Timing (build preview), Server Timing (track), Paint Timing Level 1 (track), Largest Contentful Paint (track), Event Timing API (track), Long Tasks API Level 1 (track), Long Animation Frames API (track), Beacon (build), requestIdleCallback() (track). Use when measuring load, paint, events, long tasks or server timing in the browser. Triggers: PerformanceObserver, LCP, Resource Timing, User Timing.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Performance Timeline

This specification extends the High Resolution Time specification [ HR-TIME-3 ] by providing methods to store and retrieve high resolution performance metric data.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when measuring load, paint, events, long tasks or server timing in the browser.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Performance Timeline Level 1 (default, posture build); Performance Timeline (legacy: read and upgrade, never author); High Resolution Time Level 2 (default); High Resolution Time Level 3 (preview, posture track: emit only when the user opts in and the posture is build); Navigation Timing (default); Navigation Timing Level 2 (preview, posture track: emit only when the user opts in and the posture is build); Resource Timing (default, posture build); User Timing Level 2 (default); User Timing (preview, posture build: emit only when the user opts in and the posture is build); Server Timing (default, posture track); Paint Timing Level 1 (default, posture track); Largest Contentful Paint (default, posture track); Event Timing API (default, posture track); Long Tasks API Level 1 (default, posture track); Long Animation Frames API (default, posture track); Beacon (default, posture build); requestIdleCallback() (default, posture track). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **2. Conformance.** "The key words MUST , MUST NOT , and SHOULD in this document are to be interpreted as described in BCP 14 [ RFC2119 ] [ RFC8174 ] when, and only when, they appear in all capitals, as shown here."
2. **4. The PerformanceEntry interface.** "navigationId This attribute MUST return the value it is initialized to."
3. **5.2 observe() method.** "The user agent SHOULD notify developers if entry types is modified."
4. **5.2 observe() method.** "The user agent SHOULD notify developers when the steps are aborted to notify that registration has been aborted."
5. **5.2 observe() method.** "The user agent SHOULD notify developers when this happens, for instance via a console warning."
6. **5.2.1 PerformanceObserverInit dictionary.** "If present, the list MUST NOT be empty and all other members MUST NOT be present."
7. **5.2.1 PerformanceObserverInit dictionary.** "Types not recognized by the user agent MUST be ignored."
8. **5.2.1 PerformanceObserverInit dictionary.** "A type that is not recognized by the user agent MUST be ignored."

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

- [Performance Timeline](https://www.w3.org/TR/performance-timeline/): Candidate Recommendation Draft, performance-timeline-1 CRD-performance-timeline-20250213 (Candidate Recommendation Draft, 2025-05-21), checked 2026-10-06.
- [High Resolution Time Level 2](https://www.w3.org/TR/hr-time-2/): Recommendation, hr-time-2 REC-hr-time-2-20191121 (Recommendation, 2019-11-21), checked 2026-10-06.
- [High Resolution Time](https://www.w3.org/TR/hr-time-3/): Working Draft, hr-time-3 WD-hr-time-3-20260901 (Working Draft, 2026-09-01), checked 2026-10-06.
- [Navigation Timing](https://www.w3.org/TR/navigation-timing/): Recommendation, navigation-timing REC-navigation-timing-20121217 (Recommendation, 2012-12-17), checked 2026-10-06.
- [Navigation Timing Level 2](https://www.w3.org/TR/navigation-timing-2/): Working Draft, navigation-timing-2 WD-navigation-timing-2-20260901 (Working Draft, 2026-09-01), checked 2026-10-06.
- [Resource Timing](https://www.w3.org/TR/resource-timing/): Candidate Recommendation Draft, resource-timing CRD-resource-timing-20260901 (Candidate Recommendation Draft, 2026-09-01), checked 2026-10-06.
- [User Timing Level 2](https://www.w3.org/TR/user-timing-2/): Recommendation, user-timing-2 REC-user-timing-2-20190226 (Recommendation, 2019-02-26), checked 2026-10-06.
- [User Timing](https://www.w3.org/TR/user-timing/): Candidate Recommendation Draft, user-timing CRD-user-timing-20260311 (Candidate Recommendation Draft, 2026-03-11), checked 2026-10-06.
- [Server Timing](https://www.w3.org/TR/server-timing/): Working Draft, server-timing WD-server-timing-20260407 (Working Draft, 2026-04-07), checked 2026-10-06.
- [Paint Timing](https://www.w3.org/TR/paint-timing/): Working Draft, paint-timing WD-paint-timing-20261002 (Working Draft, 2026-10-02), checked 2026-10-06.
- [Largest Contentful Paint](https://www.w3.org/TR/largest-contentful-paint/): Working Draft, largest-contentful-paint WD-largest-contentful-paint-20260826 (Working Draft, 2026-08-26), checked 2026-10-06.
- [Event Timing API](https://www.w3.org/TR/event-timing/): Working Draft, event-timing WD-event-timing-20260319 (Working Draft, 2026-03-19), checked 2026-10-06.
- [Long Tasks API](https://www.w3.org/TR/longtasks-1/): Working Draft, longtasks-1 WD-longtasks-1-20260319 (Working Draft, 2026-03-19), checked 2026-10-06.
- [Long Animation Frames API](https://www.w3.org/TR/long-animation-frames/): First Public Working Draft, long-animation-frames WD-long-animation-frames-20260428 (First Public Working Draft, 2026-04-28), checked 2026-10-06.
- [Beacon](https://www.w3.org/TR/beacon/): Candidate Recommendation Draft, beacon CRD-beacon-20220803 (Candidate Recommendation Draft, 2022-08-03), checked 2026-10-06.
- [requestIdleCallback()](https://www.w3.org/TR/requestidlecallback/): Working Draft, requestidlecallback WD-requestidlecallback-20250521 (Working Draft, 2025-05-21), checked 2026-10-06.
- [Core Web Vitals](https://web.dev/articles/vitals): web.dev article, read 2026-10-06, checked 2026-10-06.
