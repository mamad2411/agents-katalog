---
name: screen-wake-lock
description: >-
  Screen Wake Lock API: This document specifies an API that allows web applications to request a screen wake lock. Covers Screen Wake Lock API (track). Use when keeping the screen awake. Triggers: Screen Wake Lock, WakeLock.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Screen Wake Lock API

This document specifies an API that allows web applications to request a screen wake lock. Under the right conditions, and if allowed, the screen wake lock prevents the system from turning off a device's screen.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when keeping the screen awake.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Screen Wake Lock API (default, posture track). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **9.6.** "Garbage collection While a WakeLockSentinel object has one or more event listeners registered for " release ", and the WakeLockSentinel object hasn't already been released, there MUST be a strong reference from the Window object that the WakeLockSentinel object's constructor was invoked from to the WakeLockSentinel object itself."
2. **9.6.** "While there is a task queued by an WakeLockSentinel object on the screen wake lock task source , there MUST be a strong reference from the Window object that the WakeLockSentinel object's constructor was invoked from to that WakeLockSentinel object."
3. **11..** "In other words, user agents MUST treat wake lock acquisition as advisory-only ."
4. **11..** "The screen wake lock MUST NOT be applicable after the screen is manually switched off by the user until it is switched on again."
5. **15. Conformance.** "The key words MAY , MUST , MUST NOT , and RECOMMENDED in this document are to be interpreted as described in BCP 14 [ RFC2119 ] [ RFC8174 ] when, and only when, they appear in all capitals, as shown here."
6. **11.2.** "Handling document loss of full activity When a Document document becomes no longer fully active , the user agent must run these steps: For each lock in document ."

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

- [Screen Wake Lock API](https://www.w3.org/TR/screen-wake-lock/): Working Draft, screen-wake-lock WD-screen-wake-lock-20260929 (Working Draft, 2026-09-29), checked 2026-10-06.
