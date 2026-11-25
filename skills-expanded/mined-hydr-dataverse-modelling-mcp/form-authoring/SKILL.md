---
name: form-authoring
description: Read and change model-driven Dataverse forms (systemform) via the dataverse-modelling-mcp server — inspect a form's structure, put a PCF code component on it, replace an existing control, remove a tab. Covers the sequence a code component needs, the platform errors that punish a wrong FormXML, and why a form change is invisible until it is published. Use when the user wants to see or change what sits on a Dynamics 365 / model-driven form, place a custom control, or is debugging a control that does not appear.
version: 1.0
---

# Forms on Dataverse

**Never write FormXML by hand.** It is verbose, order-sensitive, and its errors surface far from
their cause. The tools exist so you do not have to, and this skill is about what they guarantee and
what the platform punishes — not about the format.

## Tool map

| Question | Tool |
|---|---|
| Which forms does this table have? | `form_list(table, type?)` |
| What sits on this form? | `form_get(formId)` — **always start here** |
| Put a control on a form | `form_add_control(formId, tab, section, controlJson)` |
| Swap an existing control for another | `form_replace_control(formId, controlId, controlJson)` |
| Remove a whole tab | `form_remove_tab(formId, tab)` |

`form_get` returns a tree — tabs → columns → sections → cells → controls — and resolves classids to
names. It also joins the control descriptions, which is the part you cannot do by eye: a cell
hosting a code component carries only a generic classid and a `uniqueid`, and *which* component
renders is decided by a `controlDescription` elsewhere in the document.

Form types: `2` Main, `6` QuickViewForm, `7` QuickCreate, `8` Dialog, `0` Dashboard, `11` Card.

## Putting a code component (PCF) on a form

The order is not optional. Each step exists because skipping it produces one of the errors below.

1. **Create the column and publish it.** `column_add(..., publish: true)`. A bound control whose
   column is not yet published is rejected.
2. **Find the component's stored name.** Query `customcontrols` — the name there carries the
   publisher prefix that the manifest does not.
3. **Read the manifest** for properties with `usage="bound"`. If one is `required="true"`, the
   control cannot go on the form unbound.
4. **Set the control**, binding it and declaring the required properties:

```json
{
  "dataFieldName": "sample_documentviewer",
  "customControlName": "sample_Contoso.DocumentViewer",
  "label": "Documents",
  "rowSpan": 6,
  "colSpan": 2,
  "parameters": {
    "boundField": { "value": "sample_documentviewer", "static": false },
    "authMode":   { "value": "auto", "static": true, "type": "Enum" }
  }
}
```

A **bound** property gets `static: false` — its value is a column name. A fixed configuration value
gets `static: true`. A bare string is treated as static: `"parameters": { "authMode": "auto" }`.

5. **Verify.** The result reports `versionNumberBefore` / `versionNumberAfter`. A changed version is
   the evidence that the edit landed; an unchanged one means the XML was identical or nothing took.

## The errors, and what they actually mean

| Error | Cause |
|---|---|
| `0x80160007 Custom control with name … does not exist` | You used the **manifest** name. FormXML wants `customcontrol.name`, which has the publisher prefix — manifest `Contoso.DocumentViewer` is stored as `sample_Contoso.DocumentViewer`. |
| `0x80160051 Property boundField is bound to a non-existent attribute` | The column exists but is **not published yet**. Publish the table, then set the control. |
| `0x80160032 Property boundField is required, but the declaration is missing` | The component's manifest declares a required bound property. It cannot be added unbound — pass `dataFieldName` and the matching parameter. |
| `Custom control declaration for form factor(s) 0,1,2 is missing` | A control description must cover web, tablet and phone. The tools always write all three. |
| `0x80048425 The element 'tabs' has incomplete content` | You tried to remove the last tab. A form cannot have none. `form_remove_tab` refuses this up front. |

All five are raised **before** anything is written, so a failed call leaves the form untouched.

## A form change is invisible until it is published

This is the one that causes wrong diagnoses, so it is worth stating plainly:

> A `PATCH` writes the **unpublished** form. A `GET` returns the **published** one. Until you
> publish, they are different states — and a read-back keeps returning the old XML and the old
> `versionnumber` indefinitely.

Measured on a live environment: unchanged after 120 seconds, then current the moment the table was
published. **A stale read-back is not evidence that the write failed.** No amount of waiting fixes
it, unlike table metadata, which is merely eventually consistent and catches up on its own.

That is why the write tools publish by default. If you pass `publish: false`, the result says so and
tells you what to run.

## Practical notes

- **Identify a tab or section by its id or name, not its label.** A label read straight after
  another write can still be the stale one. All three are accepted, and the error message lists what
  it did find.
- **`form_replace_control` keeps the cell** and removes the old control's description, so the
  previous component cannot keep rendering. Identify the old control by its `id` or its `uniqueid`,
  both from `form_get`.
- **`form_remove_tab` cleans up orphaned control descriptions.** A description pointing at a control
  that no longer exists is a dangling reference, not a cosmetic leftover.
- **Not covered:** there is no `form_add_tab`, `form_add_section` or `form_remove_control`. Adding a
  tab or removing a single control still means editing the form in the Maker, or extending these
  tools.
- `systemform` has **no `modifiedon`** and no `modifiedby` — a `$select` of either fails with
  `0x80060888`. Compare states with `versionnumber`.

Deeper reference, including the FormXML details these tools encapsulate:
[`docs/tools/forms.md`](https://github.com/hydr/dataverse-modelling-mcp/blob/master/docs/tools/forms.md).
