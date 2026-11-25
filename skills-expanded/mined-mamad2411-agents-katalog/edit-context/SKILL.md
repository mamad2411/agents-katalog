---
name: edit-context
description: >-
  EditContext API: EditContext is an API that allows authors to more directly participate in the text input process. Covers EditContext API (track). Use when implementing a custom text editor. Triggers: EditContext.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# EditContext API

EditContext is an API that allows authors to more directly participate in the text input process.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when implementing a custom text editor.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: EditContext API (default, posture track). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **1.1 Background and Motivation.** "When an app wants to consume text input from these various sources, it must first provide a view of its currently editable text to the operating system."
2. **1.2.1 EditContext state.** "composition end must always be greater than or equal to composition start ."
3. **1.2.1 EditContext state.** "text format is a struct that indicates decorative properties that should be applied to the ranges of text ."
4. **1.2.1 EditContext state.** "The struct contains: range start which is an offset into text that respresents the position before the first codepoint that should be decorated."
5. **1.2.1 EditContext state.** "range end which is an offset into text that respresents the position after the last codepoint that should be decorated."
6. **1.2.2 Association and activation.** "Note An EditContext keeps its associated element alive, so developers should be aware that assigning an EditContext to an element's editContext property will prevent the element from being garbage collected until the property is cleared or the EditContext is garbage collected."
7. **1.2.3 Differences for an EditContext editing host.** "There are also some ways that an EditContext editing host differs from other types of editing hosts : When the Document being edited has an active EditContext , the user agent must not update the DOM as a direct result of a user action in the EditContext editing host (e.g., keyboard input in an editable region, deleting or formatting text, ...)."
8. **1.2.3 Differences for an EditContext editing host.** "When the Document being edited has an active EditContext , the user agent must not fire the input event against the EditContext editing host as a direct result of user action event as specified in [ uievents ]."

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

- [EditContext API](https://www.w3.org/TR/edit-context/): Working Draft, edit-context WD-edit-context-20260910 (Working Draft, 2026-09-10), checked 2026-10-06.
