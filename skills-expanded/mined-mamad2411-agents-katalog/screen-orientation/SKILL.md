---
name: screen-orientation
description: >-
  Screen Orientation: The Screen Orientation specification standardizes the types and angles for a device's screen orientation, and provides a means for locking and unlocking it. Covers Screen Orientation (track). Use when reading or locking screen orientation. Triggers: screen.orientation, Screen Orientation.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Screen Orientation

The Screen Orientation specification standardizes the types and angles for a device's screen orientation, and provides a means for locking and unlocking it. The API, defined by this specification, exposes the current type and angle of the device's screen orientation, and dispatches events when it changes. This enables web applications to programmatically adapt the user experience for multiple screen orientations, working alongside CSS. This API is particularly useful for applications such as computer games, where users physically rotate the device, but the screen orientation itself should not change. The API restricts locking the screen orientation only if certain pre-lock conditions are met

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when reading or locking screen orientation.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Screen Orientation (default, posture track). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **5.2.** "When the lock () method is invoked with OrientationLockType orientation , the user agent MUST run the following steps."
2. **5.3.** "unlock() method When the unlock () method is invoked, the user agent MUST run the following steps: Let document be this 's relevant global object 's associated Document ."
3. **8.1.** "Initializing the ScreenOrientation object When a browsing context context is created, the user agent MUST : Let screenOrientation be context 's associated ScreenOrientation ."
4. **8.2.** "Rejecting a document's current lock promise When steps require to reject and nullify the current lock promise of Document document with a DOMString exceptionName , the user agent MUST : Assert : [[orientationPendingPromise]] is not null ."
5. **8.3.** "orientation to Document document , the user agent MUST perform the following steps: If document stops being fully active while in parallel , and [[orientationPendingPromise]] is not null , reject and nullify the current lock promise of document with an " AbortError "."
6. **8.6.** "Handling unloading documents Whenever the unloading document cleanup steps run with a document , the user agent MUST run the following steps: If document is not a top-level traversable 's active document , abort these steps."
7. **9..** "Interaction with Fullscreen API A user agent MUST restrict the use of lock () to simple fullscreen documents as a pre-lock condition ."
8. **10..** "A user agent SHOULD require installed web applications to be presented in the "fullscreen" display mode as a pre-lock condition ."

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

- [Screen Orientation](https://www.w3.org/TR/screen-orientation/): Working Draft, screen-orientation WD-screen-orientation-20260806 (Working Draft, 2026-08-06), checked 2026-10-06.
