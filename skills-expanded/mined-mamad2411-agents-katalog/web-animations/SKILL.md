---
name: web-animations
description: >-
  Web Animations: This specification defines a model for synchronization and timing of changes to the presentation of a Web page. Covers Web Animations Module Level 2 (track). Use when animating with the Web Animations API. Triggers: Web Animations, Animation.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Web Animations

This specification defines a model for synchronization and timing of changes to the presentation of a Web page. This specification also defines an application programming interface for interacting with this model and it is expected that further specifications will define declarative means for exposing these features. CSS is a language for describing the rendering of structured documents (such as HTML and XML) on screen, on paper, etc.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when animating with the Web Animations API.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Web Animations Module Level 2 (default, posture track); Web Animations Level 1 (legacy: read and upgrade, never author). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **4.12. The EffectCallback callback function.** "When this is null , the function SHOULD remove the effect."
2. **Document conventions.** "The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in the normative parts of this document are to be interpreted as described in RFC 2119."
3. **Document conventions.** "Advisements are normative sections styled to evoke special attention and are set apart from other normative text with <strong class="advisement"> , like this: UAs MUST provide an accessible alternative."
4. **2.4.1. Setting the timeline of an animation.** "Issue: If new timeline is null, we should ensure that custom effects get called with an unresolved iteration progress (unless a subsequent change in the same script execution context makes this redundant)."
5. **2.4.2. Setting the target effect of an.** "If old effect is attached to another animation in the same task then we should probably not do an extra callback with unresolved ."
6. **2.4.7. Playing an animation.** "If a user agent determines that animation is immediately ready , it may schedule the above task as a microtask such that it runs at the next microtask checkpoint , but it must not perform the task synchronously."
7. **2.5.2. The active interval.** "The subsequent diagram should also refer to the animation effect start time as opposed to the animation start time ."
8. **2.7. Animation effect speed control.** "For runtime speed control the playback rate of the animation should be used."

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

- [Web Animations Module Level 2](https://www.w3.org/TR/web-animations-2/): Working Draft, web-animations-2 WD-web-animations-2-20251120 (Working Draft, 2025-11-20), checked 2026-10-06.
- [Web Animations](https://www.w3.org/TR/web-animations-1/): Working Draft, web-animations-1 WD-web-animations-1-20230605 (Working Draft, 2023-06-05), checked 2026-10-06.
