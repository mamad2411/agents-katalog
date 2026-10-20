---
name: contact-picker
description: >-
  Contact Picker API: An API to give one-off access to a user’s contact information with full control over the shared data. Covers Contact Picker API (track). Use when picking contacts from the device. Triggers: Contact Picker, navigator.contacts.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Contact Picker API

An API to give one-off access to a user’s contact information with full control over the shared data.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when picking contacts from the device.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Contact Picker API (default, posture track). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **7. Contact Picker.** "To launch a contact picker with allowMultiple (a boolean ), and properties (a list of DOMString s), the user agent MUST present a user interface that follows these rules: If presenting a user interface fails or accessing the contacts source 's available contacts fails, then return failure."
2. **7. Contact Picker.** "The UI MUST prominently display the top-level traversable 's origin ."
3. **7. Contact Picker.** "The UI MUST make it clear which properties of the contacts are requested."
4. **7. Contact Picker.** "The UI SHOULD provide a way for users to opt out of sharing certain contact information."
5. **7. Contact Picker.** "The UI MUST make it clear which information will be shared."
6. **7. Contact Picker.** "The UI MUST provide a way to select individual contacts."
7. **7. Contact Picker.** "The UI MUST provide an option to cancel/return without sharing any contacts, in which case remove the UI and return an empty list ."
8. **7. Contact Picker.** "The UI MUST provide an a way for users to indicate that they are done selecting, in which case remove the UI and return a list of the selected contacts as user contacts ."

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

- [Contact Picker API](https://www.w3.org/TR/contact-picker/): Working Draft, contact-picker WD-contact-picker-20240708 (Working Draft, 2024-07-08), checked 2026-10-06.
