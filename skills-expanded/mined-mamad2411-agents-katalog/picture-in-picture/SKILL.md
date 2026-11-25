---
name: picture-in-picture
description: >-
  Picture-in-Picture: This specification provides APIs to allow websites to create a floating video window always on top of other windows so that users may continue consuming media while they interact with other content sites, or applications on their device. Covers Picture-in-Picture (track). Use when showing a video in a floating window. Triggers: Picture-in-Picture, requestPictureInPicture.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Picture-in-Picture

This specification provides APIs to allow websites to create a floating video window always on top of other windows so that users may continue consuming media while they interact with other content sites, or applications on their device.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when showing a video in a floating window.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Picture-in-Picture (default, posture track). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **3.2. Picture-in-Picture.** "It is RECOMMENDED that video frames are not rendered in the page and in the Picture-in-Picture window at the same time but if they are, they MUST be kept in sync."
2. **3.2. Picture-in-Picture.** "When a video is played in Picture-in-Picture mode, the states SHOULD transition as if it was played inline."
3. **3.2. Picture-in-Picture.** "That means that the events SHOULD fire at the same time, calling methods SHOULD have the same behaviour, etc."
4. **3.2. Picture-in-Picture.** "Styles applied to video (such as opacity, visibility, transform, etc.) MUST NOT apply in the Picture-in-Picture window."
5. **3.2. Picture-in-Picture.** "When a DocumentOrShadowRoot ’s Picture-in-Picture element is set, the Picture-in-Picture window MUST be visible, even when the DocumentOrShadowRoot ’s relevant global object ’s associated Document ’s visibility state is "hidden"."
6. **3.2. Picture-in-Picture.** "The user agent SHOULD provide a way for users to manually close the Picture-in-Picture window."
7. **3.3. Exit Picture-in-Picture.** "When the exit Picture-in-Picture algorithm is invoked, the user agent MUST run the following steps: If pictureInPictureElement is null , throw a InvalidStateError and abort these steps."
8. **3.3. Exit Picture-in-Picture.** "The website SHOULD be in control of the experience if it is website initiated."

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

- [Picture-in-Picture](https://www.w3.org/TR/picture-in-picture/): Working Draft, picture-in-picture WD-picture-in-picture-20260616 (Working Draft, 2026-06-16), checked 2026-10-06.
