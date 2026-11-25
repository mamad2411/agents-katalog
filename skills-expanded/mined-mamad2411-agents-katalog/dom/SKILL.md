---
name: dom
description: >-
  DOM: DOM defines a platform-neutral model for events, aborting activities, and node trees. Covers DOM Living Standard. Use when walking or mutating the DOM. Triggers: DOM, DOM Living Standard.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# DOM

DOM defines a platform-neutral model for events, aborting activities, and node trees.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when walking or mutating the DOM.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: DOM Living Standard (default); W3C DOM 4 (legacy: read and upgrade, never author). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **DOM.** "Developers should refer to the Living Standard for the most current error corrections and other developments."
2. **2.2. Interface Event.** "The type attribute must return the value it was initialized to."
3. **2.2. Interface Event.** "When an event is created the attribute must be initialized to the empty string."
4. **2.2. Interface Event.** "The currentTarget attribute must return the value it was initialized to."
5. **2.2. Interface Event.** "When an event is created the attribute must be initialized to null."
6. **2.2. Interface Event.** "The eventPhase attribute must return the value it was initialized to, which must be one of the following: NONE (numeric value 0) Events not currently dispatched are in this phase."
7. **2.2. Interface Event.** "Initially the attribute must be initialized to NONE ."
8. **2.2. Interface Event.** "The bubbles and cancelable attributes must return the values they were initialized to."

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

- [DOM Living Standard](https://dom.spec.whatwg.org/review-drafts/2026-06/): Review Draft, Review Draft 2026-06 (Review Draft, 2026-06), checked 2026-10-06.
- [W3C DOM 4](https://www.w3.org/TR/2015/REC-dom-20151119/): W3C Recommendation, REC-dom-20151119 (W3C Recommendation, 2015-11-19), checked 2026-10-06.
