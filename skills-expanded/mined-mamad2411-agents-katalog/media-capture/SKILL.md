---
name: media-capture
description: >-
  Media Capture: This document defines a set of JavaScript APIs that allow local media, including audio and video, to be requested from a platform. Covers Media Capture and Streams (build), MediaStream Image Capture (track), MediaStream Recording (track), Media Capture from DOM Elements (track), MediaStreamTrack Insertable Media Processing using Streams (track), MediaStreamTrack Content Hints (track), Region Capture (track), Viewport Capture (track), Screen Capture (track), Capture Handle - Bootstrapping Collaboration when Screensharing (track), Audio Output Devices API (build). Use when capturing camera, microphone, screen or element media. Triggers: getUserMedia, getDisplayMedia, MediaStream.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Media Capture

This document defines a set of JavaScript APIs that allow local media, including audio and video, to be requested from a platform.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when capturing camera, microphone, screen or element media.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Media Capture and Streams (default, posture build); MediaStream Image Capture (default, posture track); MediaStream Recording (default, posture track); Media Capture from DOM Elements (default, posture track); MediaStreamTrack Insertable Media Processing using Streams (default, posture track); MediaStreamTrack Content Hints (default, posture track); Region Capture (default, posture track); Viewport Capture (default, posture track); Screen Capture (default, posture track); Capture Handle - Bootstrapping Collaboration when Screensharing (default, posture track); Audio Output Devices API (default, posture build). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **2. Conformance.** "The key words MAY , MUST , MUST NOT , NOT REQUIRED , and SHOULD in this document are to be interpreted as described in BCP 14 [ RFC2119 ] [ RFC8174 ] when, and only when, they appear in all capitals, as shown here."
2. **3. Terminology.** "The platform SHOULD try to minimize such excursions as far as possible, but will continue to deliver media even when a temporary or permanent condition exists that prevents satisfying the constraints."
3. **4.2 MediaStream.** "The track set MUST contain the MediaStreamTrack objects that correspond to the tracks of the stream."
4. **4.2 MediaStream.** "To add a track track to a MediaStream stream , the User Agent MUST run the following steps: If track is already in stream's track set , then abort these steps."
5. **4.2 MediaStream.** "To remove a track track from a MediaStream stream , the User Agent MUST"
6. **Attributes.** "id of type DOMString , readonly The id attribute MUST return the value to which it was initialized when the object was created."
7. **Attributes.** "When a MediaStream is created, the User Agent MUST generate an identifier string, and MUST initialize the object's id attribute to that string, unless the object is created as part of a special purpose algorithm that specifies how the stream id must be initialized."
8. **Attributes.** "To avoid fingerprinting, implementations SHOULD use the forms in section 4.4 or 4.5 of RFC 4122 when generating UUIDs."

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

- [Media Capture and Streams](https://www.w3.org/TR/mediacapture-streams/): Candidate Recommendation Draft, mediacapture-streams CRD-mediacapture-streams-20251009 (Candidate Recommendation Draft, 2025-10-09), checked 2026-10-06.
- [MediaStream Image Capture](https://www.w3.org/TR/image-capture/): Working Draft, image-capture WD-image-capture-20250423 (Working Draft, 2025-04-23), checked 2026-10-06.
- [MediaStream Recording](https://www.w3.org/TR/mediastream-recording/): Working Draft, mediastream-recording WD-mediastream-recording-20260316 (Working Draft, 2026-03-16), checked 2026-10-06.
- [Media Capture from DOM Elements](https://www.w3.org/TR/mediacapture-fromelement/): Working Draft, mediacapture-fromelement WD-mediacapture-fromelement-20250212 (Working Draft, 2025-02-12), checked 2026-10-06.
- [MediaStreamTrack Insertable Media Processing using Streams](https://www.w3.org/TR/mediacapture-transform/): Working Draft, mediacapture-transform WD-mediacapture-transform-20260416 (Working Draft, 2026-04-16), checked 2026-10-06.
- [MediaStreamTrack Content Hints](https://www.w3.org/TR/mst-content-hint/): Working Draft, mst-content-hint WD-mst-content-hint-20250919 (Working Draft, 2025-09-19), checked 2026-10-06.
- [Region Capture](https://www.w3.org/TR/mediacapture-region/): Working Draft, mediacapture-region WD-mediacapture-region-20230712 (Working Draft, 2023-07-12), checked 2026-10-06.
- [Viewport Capture](https://www.w3.org/TR/mediacapture-viewport/): Working Draft, mediacapture-viewport WD-mediacapture-viewport-20241009 (Working Draft, 2024-10-09), checked 2026-10-06.
- [Screen Capture](https://www.w3.org/TR/screen-capture/): Working Draft, screen-capture WD-screen-capture-20260827 (Working Draft, 2026-08-27), checked 2026-10-06.
- [Capture Handle - Bootstrapping Collaboration when Screensharing](https://www.w3.org/TR/capture-handle-identity/): Working Draft, capture-handle-identity WD-capture-handle-identity-20250306 (Working Draft, 2025-03-06), checked 2026-10-06.
- [Audio Output Devices API](https://www.w3.org/TR/audio-output/): Candidate Recommendation Draft, audio-output CRD-audio-output-20251009 (Candidate Recommendation Draft, 2025-10-09), checked 2026-10-06.
