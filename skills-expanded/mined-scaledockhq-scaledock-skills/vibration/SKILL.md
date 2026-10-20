---
name: vibration
description: >-
  Vibration API: This specification defines an API that provides access to the vibration mechanism of the hosting device. Covers Vibration API (build). Use when vibrating a device. Triggers: Vibration API, navigator.vibrate.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# Vibration API

This specification defines an API that provides access to the vibration mechanism of the hosting device. Vibration is a form of tactile feedback.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when vibrating a device.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Vibration API (default, posture build). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **§ 3.** "If the document's visibility state is not visible, then return false and terminate these steps."
2. **§ 3.** "Let max length have the value 10."
3. **§ 3.** "If the length of pattern is greater than max length, truncate pattern, leaving only the first max length entries."
4. **§ 3.** "For each entry in pattern whose value is greater than max duration, set the entry's value to max duration."
5. **§ 3.** "If global does not have sticky activation, return false and terminate these steps."
6. **§ 3.** "If another instance of the perform vibration algorithm is already running, run the following substeps: Abort that other instance of the perform vibration algorithm, if any."
7. **§ 3.** "When the user agent determines that the visibility state of the Document of the top-level browsing context changes, it MUST abort the already running processing vibration patterns algorithm, if any."
8. **§ 4.** "The user agent SHOULD employ global rate limiting to restrict the number of vibration requests made within a certain period (e.g., per minute or hour) to prevent excessive use."

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in [`references/requirements.md`](references/requirements.md) and implement each one that applies to the role.
   -> [`references/requirements.md`](references/requirements.md)
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the section it came from.
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

- [Vibration API](https://www.w3.org/TR/vibration/): Candidate Recommendation Draft, vibration CRD-vibration-20260521 (Candidate Recommendation Draft, 2026-05-21), checked 2026-10-06.
