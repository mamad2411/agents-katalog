---
name: webxr
description: >-
  WebXR: This specification describes support for accessing virtual reality (VR) and augmented reality (AR) devices, including sensors and head-mounted displays, on the Web. Covers WebXR Device API (build), WebXR Augmented Reality Module - Level 1 (build), WebXR Depth Sensing Module Level 1 (track), WebXR DOM Overlays Module Level 1 (track), WebXR Gamepads Module - Level 1 (track), WebXR Hand Input Module - Level 1 (track), WebXR Hit Test Module Level 1 (track), WebXR Layers API Level 1 (track), WebXR Lighting Estimation API Level 1 (track). Use when building an immersive or inline XR experience. Triggers: WebXR, XRSession.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# WebXR

This specification describes support for accessing virtual reality (VR) and augmented reality (AR) devices, including sensors and head-mounted displays, on the Web.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when building an immersive or inline XR experience.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: WebXR Device API (default, posture build); WebXR Augmented Reality Module - Level 1 (default, posture build); WebXR Depth Sensing Module Level 1 (default, posture track); WebXR DOM Overlays Module Level 1 (default, posture track); WebXR Gamepads Module - Level 1 (default, posture track); WebXR Hand Input Module - Level 1 (default, posture track); WebXR Hit Test Module Level 1 (default, posture track); WebXR Layers API Level 1 (default, posture track); WebXR Lighting Estimation API Level 1 (default, posture track). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **2.1. XR device.** "Each XR device has a set of granted features for each XRSessionMode in its list of supported modes , which is a set of feature descriptors which MUST be initially an empty set ."
2. **2.1. XR device.** "The user agent has a list of immersive XR devices (a list of XR device ), which MUST be initially an empty list ."
3. **2.1. XR device.** "The user agent MUST have a default inline XR device , which is an XR device that MUST contain "inline" in its list of supported modes ."
4. **2.1. XR device.** "The default inline XR device MUST NOT report any pose information, and MUST NOT report XR input source s or events other than those created by pointer events."
5. **2.1. XR device.** "The user agent MUST have a inline XR device , which is an XR device that MUST contain "inline" in its list of supported modes ."
6. **2.1. XR device.** "These objects SHOULD NOT be directly accessed in steps that are not running in parallel ."
7. **3.1. navigator.xr.** "partial interface Navigator { [ SecureContext , SameObject ] readonly attribute XRSystem xr ; }; The xr attribute’s getter MUST return the XRSystem object that is associated with it."
8. **3.2. XRSystem.** "[ SecureContext , Exposed = Window ] interface XRSystem : EventTarget { // Methods Promise < boolean > isSessionSupported ( XRSessionMode mode ); [ NewObject ] Promise < XRSession > requestSession ( XRSessionMode mode , optional XRSessionInit options = {}); // Events attribute EventHandler ondevicechange ; }; The user agent MUST create an XRSystem object when a Navigator object is created and…"

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

- [WebXR Device API](https://www.w3.org/TR/webxr/): Candidate Recommendation Draft, webxr CRD-webxr-20260609 (Candidate Recommendation Draft, 2026-06-09), checked 2026-10-06.
- [WebXR Augmented Reality Module - Level 1](https://www.w3.org/TR/webxr-ar-module-1/): Candidate Recommendation Draft, webxr-ar-module-1 CRD-webxr-ar-module-1-20250425 (Candidate Recommendation Draft, 2025-04-25), checked 2026-10-06.
- [WebXR Depth Sensing Module](https://www.w3.org/TR/webxr-depth-sensing-1/): Working Draft, webxr-depth-sensing-1 WD-webxr-depth-sensing-1-20260825 (Working Draft, 2026-08-25), checked 2026-10-06.
- [WebXR DOM Overlays Module](https://www.w3.org/TR/webxr-dom-overlays-1/): Working Draft, webxr-dom-overlays-1 WD-webxr-dom-overlays-1-20240924 (Working Draft, 2024-09-24), checked 2026-10-06.
- [WebXR Gamepads Module - Level 1](https://www.w3.org/TR/webxr-gamepads-module-1/): Working Draft, webxr-gamepads-module-1 WD-webxr-gamepads-module-1-20250707 (Working Draft, 2025-07-07), checked 2026-10-06.
- [WebXR Hand Input Module - Level 1](https://www.w3.org/TR/webxr-hand-input-1/): Working Draft, webxr-hand-input-1 WD-webxr-hand-input-1-20240605 (Working Draft, 2024-06-05), checked 2026-10-06.
- [WebXR Hit Test Module](https://www.w3.org/TR/webxr-hit-test-1/): Working Draft, webxr-hit-test-1 WD-webxr-hit-test-1-20251211 (Working Draft, 2025-12-11), checked 2026-10-06.
- [WebXR Layers API Level 1](https://www.w3.org/TR/webxrlayers-1/): Working Draft, webxrlayers-1 WD-webxrlayers-1-20260811 (Working Draft, 2026-08-11), checked 2026-10-06.
- [WebXR Lighting Estimation API Level 1](https://www.w3.org/TR/webxr-lighting-estimation-1/): Working Draft, webxr-lighting-estimation-1 WD-webxr-lighting-estimation-1-20251211 (Working Draft, 2025-12-11), checked 2026-10-06.
