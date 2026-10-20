---
name: pointer-lock
description: >-
  Pointer Lock: This specification defines an API that provides scripted access to raw mouse movement data while locking the target of mouse events to a single element and removing the cursor from view. Covers Pointer Lock, Pointer Lock 2.0 (track preview). Use when locking the pointer to an element. Triggers: Pointer Lock, requestPointerLock.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Pointer Lock

This specification defines an API that provides scripted access to raw mouse movement data while locking the target of mouse events to a single element and removing the cursor from view. This is an essential input mode for certain classes of applications, especially first person perspective 3D applications and 3D modeling software.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when locking the pointer to an element.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Pointer Lock (default); Pointer Lock 2.0 (preview, posture track: emit only when the user opts in and the posture is build). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **2.1.** "Issue 97 : Section 2.1 should mention the effect of lock on PointerEvents This came up in this thread on #49 : Would it be possible to list these events normatively, instead of only giving some examples?"
2. **2.4.** "Exit Pointer Lock The process of exiting pointer lock, given an element , is as follows: The system mouse cursor must be displayed again and positioned at cursor position ."
3. **3..** "Issue 93 : Visibility state checks The spec should not allow hidden documents to request pointer lock."
4. **3..** "Additionally, should a document become hidden, it should release the pointer lock."
5. **3..** "Issue 91 : When a subsequent requestPointerLock is rejected, should an already locked target exit lock state?"
6. **3..** "In the PR #49 's algorithm of requestPointerLock is currently missing the description for the scenario: When a subsequent request failed (for any possible reason), should an already locked target exit lock state?"
7. **6..** "Extensions to the MouseEvent Interface WebIDL partial interface MouseEvent { readonly attribute double movementX ; readonly attribute double movementY ; }; movementX attribute movementY attribute The attributes movementX and movementY must provide the change in position of the pointer, as if the values of screenX , screenY , were stored between two subsequent mousemove events eNow and ePrevious…"
8. **6..** "movementX and movementY must be zero for all mouse events except mousemove and pointermove ."

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

- [Pointer Lock](https://www.w3.org/TR/pointerlock/): Recommendation, pointerlock WD-pointerlock-2-20260225 (Recommendation, 2016-10-27), checked 2026-10-06.
- [Pointer Lock 2.0](https://www.w3.org/TR/pointerlock-2/): Working Draft, pointerlock-2 WD-pointerlock-2-20260225 (Working Draft, 2026-02-25), checked 2026-10-06.
