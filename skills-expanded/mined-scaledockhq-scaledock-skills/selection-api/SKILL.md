---
name: selection-api
description: >-
  Selection API: This document is a preliminary draft of a specification for the Selection API and selection related functionality. Covers Selection API (track). Use when reading the current text selection. Triggers: Selection API, window.getSelection.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Selection API

This document is a preliminary draft of a specification for the Selection API and selection related functionality. It replaces a couple of old sections of the HTML specification , the selection part of the old DOM Range specification . This document defines APIs for selection, which allows users and authors to select a portion of a document or specify a point of interest for copy, paste, and other editing operations.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when reading the current text selection.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Selection API (default, posture track). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **2..** "This one selection must be shared by all the content of the document (though not by nested documents ), including any editing hosts in the document ."
2. **2..** "Once a selection is associated with a given range , it must continue to be associated with that same range until this specification requires otherwise."
3. **2..** "Note For instance, if the DOM changes in a way that changes the range's boundary points, or a script modifies the boundary points of the range, the same range object must continue to be associated with the selection."
4. **2..** "However, if the user changes the selection or a script calls addRange () , the selection must be associated with a new range object, as required elsewhere in this specification."
5. **2..** "If the selection 's range is not null and is collapsed , then the caret position must be at that range 's boundary point ."
6. **2..** "When the selection is not collapsed , this specification does not define the caret position; user agents should follow platform conventions in deciding whether the caret is at the start of the selection , the end of the selection , or somewhere else."
7. **2..** "If the user creates a selection by indicating first one boundary point of the range and then the other (such as by clicking on one point and dragging to another), and the first indicated boundary point is after the second, then the corresponding selection must initially be backwards ."
8. **2..** "If the first indicated boundary point is before the second, then the corresponding selection must initially be forwards ."

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

- [Selection API](https://www.w3.org/TR/selection-api/): Working Draft, selection-api WD-selection-api-20260611 (Working Draft, 2026-06-11), checked 2026-10-06.
