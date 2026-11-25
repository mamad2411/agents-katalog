---
name: fullscreen
description: >-
  Fullscreen API: The Fullscreen API standard defines an API for elements to display themselves fullscreen. Covers Fullscreen API Living Standard. Use when entering fullscreen. Triggers: requestFullscreen, Fullscreen.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Fullscreen API

The Fullscreen API standard defines an API for elements to display themselves fullscreen.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when entering fullscreen.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Fullscreen API Living Standard (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **Fullscreen API.** "Developers should refer to the Living Standard for the most current error corrections and other developments."
2. **3. API.** "The following are the event handlers (and their corresponding event handler event types ) that must be supported by Element and Document objects as event handler IDL attributes : event handler event handler event type onfullscreenchange fullscreenchange onfullscreenerror fullscreenerror These are not supported by ShadowRoot or Window objects, and there are no"
3. **4. UI.** "Users should be clearly notified when keyboard locking is active, possibly through browser UI indicators."
4. **4. UI.** "There should be a simple and intuitive method for users to override keyboard locking, reverting control back to the system or user agent."
5. **5.1. :fullscreen pseudo-class.** "The :fullscreen pseudo-class must match any element element for which one of the following conditions is true: element ’s fullscreen flag is set."
6. **6. Keyboard Locking.** "Whenever a document ’s keyboard lock is changed from active to inactive, user agents must deactivate the keyboard lock and restore the handling of keyboard inputs to the default behavior of the user agent and the operating system."
7. **6. Keyboard Locking.** "User agents should reserve an additional input for the purposes of exiting fullscreen."
8. **8. Security and Privacy Considerations.** "User agents should provide a means of exiting fullscreen that always works and advertise this to the user."

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

- [Fullscreen API Living Standard](https://fullscreen.spec.whatwg.org/review-drafts/2026-07/): Review Draft, Review Draft 2026-07 (Review Draft, 2026-07), checked 2026-10-06.
