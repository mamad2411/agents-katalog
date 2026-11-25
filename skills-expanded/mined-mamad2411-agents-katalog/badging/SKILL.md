---
name: badging
description: >-
  Badging API: This specification defines an API that allows installed web applications to set an application badge, which is usually shown alongside the application's icon on the device's home screen or application dock. Covers Badging API (track). Use when setting an application badge. Triggers: Badging API, navigator.setAppBadge.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Badging API

This specification defines an API that allows installed web applications to set an application badge, which is usually shown alongside the application's icon on the device's home screen or application dock.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when setting an application badge.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Badging API (default, posture track). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **4..** "Displaying a badge When the application's badge is set , the user agent or operating system SHOULD display the application's badge alongside the primary iconic representation of the application in the user's operating system (for example, as a small overlay on top of the application's icon on the home screen on a device)."
2. **4..** "When a user agent requires such permission , it SHOULD tie the permission grant to the " notifications " permission."
3. **4..** "When the badge is set to "flag" , the user agent or operating system SHOULD display an indicator with a non-specific symbol (for example, a colored circle)."
4. **4..** "If the platform does not support displaying a "flag" badge, the user agent SHOULD display the badge using the closest available representation that indicates the presence of a badge (e.g., the value "1"), rather than clearing the badge entirely."
5. **4..** "When a badge 's value is set to "nothing" , the user agent or operating system SHOULD clear the badge by no longer displaying it."
6. **4..** "When the badge is set to a number , the user agent or operating system: SHOULD format and display the number according to the user's font and formatting preferences."
7. **4..** "SHOULD localize the number according to the user's locale preferences."
8. **4..** "Similarly, if the platform does not support "flag" badges, it MAY represent "flag" using a number or other appropriate visual indicator, but MUST NOT clear the badge when "flag" is requested."

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

- [Badging API](https://www.w3.org/TR/badging/): Working Draft, badging WD-badging-20260427 (Working Draft, 2026-04-27), checked 2026-10-06.
