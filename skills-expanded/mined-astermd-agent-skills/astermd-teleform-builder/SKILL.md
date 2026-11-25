---
name: astermd-teleform-builder
description: Generate or update AsterMD teleform builder JSON (the exact-export format that AsterMD's Teleforms → Import JSON accepts) from a list of intake/telemedicine questions — markdown, plain text, a doc, or questions typed in chat. Use whenever the user asks for an AsterMD teleform, teleform JSON, an intake form for a medication or condition to import into AsterMD, wants a question list turned into an importable teleform, or wants an existing teleform JSON fixed or updated.
license: MIT
---

# astermd-teleform-builder

Turn a written question list into JSON that imports through **Import JSON**, renders correctly in the form builder, and survives a builder save/export without losing anything.

The importer is forgiving — a file that imports is not proof it is right. Follow the rules below over any sample JSON, old export, or memory of how teleforms used to work. Older exports use legacy shapes: label-valued rules, timestamp ids, `buttonStyle`, top-level `"hidden": false`. Don't copy them — migrate them (see **Updating an existing JSON**).

## Workflow

1. **Parse** — list every question with its number, text, answer type and logic. Watch for contradictions; question lists often carry a superseded "original" section next to an "updated" one.
2. **Ask only what changes the output** — superseded/duplicate sections, how a "HARD STOP" should behave, page grouping when the source has none, BMI composite vs. plain numbers. Don't ask what this skill already answers.
3. **Map** each question to a field type (see **Answer type → field type**).
4. **Paginate** — one page per source section. Each page starts with its `heading`; on page 1, contact fields the source asks for (name, email, phone) come right after it. Don't add contact fields the source doesn't ask for; a single "full name" question is one `text` field with `db_field: "opportunity.name"`. Every page ends with a button row: page 1 Next; middle pages Back + Next; last page Back + Submit; a single-page form has Submit only.
5. **Write** the JSON — 2-space indent, named after the form in kebab-case (`nad-plus-intake.json`), saved next to the source file or where the user asks.
6. **Self-check** against the **Checklist** below and fix everything.
7. **Report** page, field and condition counts, and list anything from the source you could not express, with the reason. Never drop a question silently.
8. **Explain how to load it** — **Teleforms → New Form → Import JSON** opens *Import JSON Template*: pick *Form Type* (*Intake Form* is the default unless the General tab is active), paste the JSON or use *Choose JSON File* (only loads it into the editor), then click **Import Template**. To replace a form that's already open, use the builder's top-bar **JSON** button → *JSON Preview* → **Edit JSON** → **Save**. Edit JSON is stricter (every page needs `fields`, every field `fieldId`/`name`/`type`) and **merges** `settings` into the current ones — removing a settings key there doesn't clear it.

**Updating an existing JSON:** keep its ids and names, change only what was asked, migrate legacy shapes you touch (label-valued rules, `type: "date-of-birth"`, `buttonStyle`, top-level `"hidden": false`, duplicate `conditionId`s on one field, string `logic` on multi-rule conditions), and re-run the checklist on the whole file.

## Envelope

```json
{
  "formId": "nad_plus_intake_v1",
  "formName": "NAD+ Therapy Intake",
  "formType": "multi_step",
  "description": "",
  "version": 1,
  "createdAt": "2026-10-08T00:00:00.000Z",
  "updatedAt": "2026-10-08T00:00:00.000Z",
  "settings": {
    "saveDraft": true, "draftExpiryDays": 7, "autoSave": true, "resumeMethod": "link",
    "submitButtonText": "Submit Intake",
    "successMessage": "Thank you! A licensed provider will review your information shortly.",
    "successRedirectUrl": null, "showProgressBar": true,
    "injectCss": "", "injectJs": "",
    "pageColor": "#FFFFFF", "backgroundColor": "#FAFBFC", "accentColor": "#14b8a6",
    "pageConditionalRules": []
  },
  "pages": [
    { "pageId": "page_1", "title": "About You", "description": "", "order": 0, "conditions": [], "fields": [] }
  ]
}
```

- `formType`: `"multi_step"` for more than one page, else `"single_page"`.
- `formId` is replaced on import; keep it readable. Form type (General/Intake) and status come from the import modal, not the JSON.
- Page `order` is 0-based and contiguous. Page `pageId`/`title`/`description` are organisational only — export rewrites them. Per-page `conditions` are not evaluated; page logic goes in `settings.pageConditionalRules`.
- Only the settings keys shown above (plus `formConditions` and optional theming: `fontFamily`, `headingColor`, `subheadingColor`, `textLabelColor`, `textInputColor`, `inputFieldColor`, `descriptionTextColor`, `linkColor`, `dividerColor`) survive export.
- **`formConditions` is a legacy list with a different shape** (id-keyed rules, string logic, `require`/`optional`/`skip_page` actions) and no builder UI. Never author it — omit it or emit `[]`.
- The import modal only checks that page 1 has a first field with `fieldId`/`name`/`type`; don't rely on that — every field needs them.

## Field shape

```json
{
  "fieldId": "pancreatitis_history",
  "type": "choice-multi",
  "label": "Do you have a history of pancreatitis?",
  "name": "pancreatitis_history",
  "required": true,
  "sendToProvider": true,
  "providerInfo": "medical",
  "db_field": "",
  "order": 4,
  "validation": {},
  "conditions": [],
  "properties": {
    "options": [ { "label": "Yes", "value": "yes" }, { "label": "No", "value": "no" } ],
    "choiceInputType": "radio",
    "multiSelect": false,
    "layout": "horizontal",
    "cols": 1
  }
}
```

- **Every field needs string `fieldId`, `name` and `type`.** `fieldId` == `name` == snake_case of the question's subject — never a timestamp. Both must be globally unique, BMI subfields included, or the builder blocks Save (`form-progress` is exempt from the name check).
- **Every** field — headings, alerts, buttons, uploads and signatures included — carries `required`, `sendToProvider`, `db_field`, `order`, `validation`, `conditions` and `properties` (with `cols: 1` unless stated otherwise); non-questions use `false` / `""` / `{}` / `[]`.
- `order` is 0-based and contiguous within the page.
- `validation` keys read: `minValue`, `maxValue`, `minLength`, `maxLength`, `pattern`, `errorMessages`. `errorMessages` keys: `required`, `minLength`, `maxLength`, `pattern`, `options`, `minItems`, `maxItems`, `min`, `max`, `selectionLimit`, `fileSize` (e.g. `{ "required": "You must consent to continue." }`).
- `description` is the help text / subtitle under the label. `description` and `placeholder` are **top-level** keys, never inside `properties` (import overwrites them there).
- `placeholder` only on fields that show one (`text`, `textarea`, `number`, `email`, `phone`, `password`, `dropdown`, date/time pickers); omit it elsewhere.
- **Don't emit top-level `hidden`.** `true` switches a field off; `false` is noise export drops. `properties.hidden` is a different setting (see **Hidden fixed value**).
- **Options** are always `[{ "label", "value" }]` with an explicit, unique, kebab-case `value` containing **no commas**, and **unique labels** (the renderer, defaults and exclusive options key on labels). Labels may contain commas. Rules key on the value, so a label can be renamed freely; changing a value breaks rules. (The BMI unit dropdown is the one exception — plain string options.)
- Only write `properties.defaultValue` when the source gives a default — never empty placeholders. When you do, `properties.defaultValue` (+ `"hasDefaultValue": true`) is exported for every type except `signature` and `file-upload`. For option fields write the option value(s); for `picker-date` use `YYYY/MM/DD`.

### Answer type → field type

| Source says | Use |
|---|---|
| Yes/No, single-select, "pick one" | `choice-multi` + `choiceInputType: "radio"` + `multiSelect: false` — **never** `choice-single` (not in the palette). `layout: "horizontal"` for Yes/No, `"vertical"` for longer lists |
| "Select all that apply" | `choice-multi` + `choiceInputType: "checkbox"` + `multiSelect: true` (`"text"` gives pill buttons; omitted = `checkbox`, `layout` omitted = `vertical`) |
| Dropdown, or more than 8 options | `dropdown` (`searchable`, `multiSelect`) |
| Short text, "please specify" | `text` |
| Long text, "please describe/list" | `textarea` (`rows`, `autoResize`, `showCounter`) |
| Number, dosage | `number` + `validation.minValue`/`maxValue` |
| Email | `email` |
| Phone | `phone` with `"countryCode": "+1_US"` |
| Password | `password` (`showToggle`) |
| Date | `picker-date` (`dateYearStart`, `dateYearEnd`, `disableFuture`, `disablePast`, `minDate`, `maxDate`) |
| Date of birth | `picker-date` + `disableFuture: true` + `dateYearStart: 1900` + `dateYearEnd: <current year>` + placeholder "Select date of birth" — **never** `type: "date-of-birth"` (no renderer, becomes a text box) |
| Time / date + time | `picker-time` (`timeFormat` `12h`/`24h`, `minTime`, `maxTime`) / `picker-datetime` (`timeFormat`) |
| Height + weight (+ BMI) | one `bmi` composite — see **BMI** |
| "I consent", "I understand" checkbox | `terms` (`termsText` beside the box, `label` is the title above; `termsLinks: [{ "id", "text", "url" }]`, each `text` must appear in `termsText`) |
| Signature | `signature` (`signatureCanvasHeight`, min 200, default 220; add `allowUploadSignature: true` only if asked — it lets the patient upload an image instead of drawing). No `placeholder` or default value. Share as `providerInfo: "consent"` |
| File / photo / ID upload | `file-upload` (`maxFiles`, `maxFileSizeMb`, `fileTypes` as a comma-separated **string** e.g. `".jpg,.jpeg,.png,.pdf"`, `allowMultipleFiles`). Files are matched on the literal extension, so list every spelling — "JPG" means `.jpg,.jpeg`, "HEIC" means `.heic,.heif`. `maxFiles: 1` + `allowMultipleFiles: false` for a single file |
| Rating 1–10 | `rating` + `validation.minValue: 1`, `maxValue: 10`, `properties.step: 9` (`step` = number of intervals) |
| Slider | `slider` + `validation.maxValue`, `properties.step` (= number of intervals; scale starts at max/step, min is ignored) |
| On/off | `toggle` (`onLabel`, `offLabel`, `toggleText`) |
| Matrix question | `input-table` (`tableRows`, `tableColumns`) |
| Section title | `heading` (`headingTitle`, falls back to `label`; `description` is the subtitle; `headingLevel` `h1`–`h4`, default `h2`; `headingAlign`) — one at the top of each page; set `label` and `headingTitle` to the same text (the section name when the source gives no title) |
| Body copy | `paragraph` (`paragraphContent`, falls back to `description`; optional `paragraphHeading`) |
| Note / warning / hard stop | `alert` (`alertText` — the only text shown; empty shows a stock "Important notice text" — `alertType`: `info`/`warning`/`success`/`danger`, `alertIcon`: boolean, default `true`). Its `label` isn't displayed; set it to a short name or `""` |
| Separator | `divider` (`dividerStyle`, `dividerThickness`, `dividerColor`) |
| Logo / brand bar | `form-header` (`formHeaderMode` `logo`/text, `formHeaderText`, `formHeaderLogoUrl`, …) — only if the user asks |
| Step indicator | `form-progress` (`progressDisplayMode: "page"`, `progressColor`) — only if the user asks |
| Pop-up content | `modal` (`modalTitle`, `modalContent`, `modalWidth`, `modalAutoHeight`, `modalCloseOnOverlay`); fields inside it set `properties.parentId` = the modal's `fieldId` |
| Navigation | `button` — see **Buttons** |

Avoid types with no renderer: `date-of-birth`, `calculated`, `field_group`, `repeatable_section`, `agreement`. `video`, `report`, `checkbox`, `ranking`, `image-selection`, `captcha`, `hidden` and `choice-single` render but are hidden from the palette — don't use them unless asked.

**Width:** `cols` is 1–3 (`1` full row, `2` half, `3` third). `cols: 1` on every question. `cols: 2` only for short paired inputs (first/last name, email/phone).

## Conditions

The condition lives on the field it **acts on** (import ignores `target` and always applies it to the host field; still write `target` = the host's own `fieldId`). The trigger is named by its **`name`**.

```json
"conditions": [
  {
    "conditionId": "cond_pancreatitis_details",
    "logic": "and",
    "rules": [ { "field": "pancreatitis_history", "operator": "equals", "value": ["yes"] } ],
    "action": "show",
    "target": "pancreatitis_details"
  }
]
```

- **`conditionId`** = `cond_<target fieldId>` for the first condition on a field, `cond_<target fieldId>_2`, `_3`, … for more. Conditions on the same field with the same id are **merged** into one rule group that runs only the first action. Without the `cond_` prefix the id is regenerated on every save; with no id at all, every rule becomes its own group and multi-rule logic is lost.
- **Option triggers (`choice-multi`, `dropdown`, `choice-single`, `ranking`): `value` is an array of option VALUES** — `["yes"]`, never the label. Several entries mean "any of these". A string value is split on commas; an array is not. The auto-appended "None of these" option has no value — trigger it with the literal label `["None of these"]`.
- Other triggers take a scalar string: `terms`/`toggle`/`checkbox` `"true"`/`"false"`; `number`/`slider`/`rating` a number string; `text`/`textarea` a literal (compared case-insensitively; everything else is case-sensitive); `phone` compares national digits only; `picker-date` a literal `YYYY/MM/DD` (the stored format — `YYYY-MM-DD` never `equals`).
- `image-selection` / `input-table` triggers: use `is_empty` / `is_not_empty` only.
- **Single-select: use `equals`/`not_equals`, not `contains`** — on a single answer `contains` is a substring match (`["no"]` matches `none-of-these`). Multi-select answers: `equals`/`contains` mean "one of these is selected"; `not_*` mean "none of them".
- **One rule:** `logic: "and"`. **Multiple rules:** `logic` **must be an array** of joiners, one shorter than `rules` — `["and"]` for two, `["and", "or"]` for three (folded left to right, no precedence). A string `"or"` with two rules silently becomes AND.
- A field with any `show` rule **starts hidden**; with any `enable` rule it **starts disabled**. Hidden fields (and hidden/skipped pages) skip validation, so a conditional follow-up can be `required: true`. **Disabled fields are still validated** — a disabled required field blocks Next.
- Several conditions on one field apply in order; a later one wins (e.g. show then hide).
- **Operators:** `equals`, `not_equals`, `contains`, `not_contains`, `greater_than`, `less_than`, `greater_than_or_equal`, `less_than_or_equal`, `is_empty`, `is_not_empty`. Never `in`/`not_in` (not in the picker — use `equals`/`not_equals` with an array).
- **Actions:** `show`, `hide`, `enable`, `disable`, `make_required`, `make_optional`, `set_value` (+ `targetValue`), `apply_class_name` (+ `actionClassName`), `show_modal`/`hide_modal` (modal targets only), and **Next Page** below. Never `end_form`, `skip_page`, `reset_value`, `require`, `optional`, `enable_submit`, `disable_submit`.
- **`set_value`** forces the value on every render while the rule matches (respondent can't change it). For option targets `targetValue` is the option **label** (comma-separated for multi-select) — the one place labels, not values, are used.
- **Can't trigger a rule:** `signature`, `file-upload`, `heading`, `paragraph`, `divider`, `image`, `video`, `alert`, `button`, `modal`, `form-header`, `form-progress`, `report`.
- **No self-reference**, except Next Page.
- **No date arithmetic.** A date compares against a literal date, which drifts. For age cutoffs add "Are you 18 years of age or older?" and hang the hard stop off that.

**Next Page** — on a `choice-multi`, `dropdown` or `rating` field only, never on the last page: `action: "jump_to_page"`, `targetValue` = the **1-based number of the next page** as a string (page `order` + 2 — the field on `order: 0` uses `"2"`). Usually a self-rule (`field` = own `name`, `target` = own `fieldId`); a self-referencing field can only use Next Page. Runs in preview/runtime only, and fires as soon as the answer matches — it auto-advances and **holds** the respondent on that page until the answer changes. Use it for auto-advance, not general branching.

**Page rules** — `settings.pageConditionalRules[]`, reference the trigger by **`fieldId`** (not `name`; a BMI part by its `subfieldId`):

```json
{ "enabled": true, "fieldId": "pregnancy_status", "operator": "equals", "value": ["yes"],
  "action": "jump_to_page", "page": 6, "skipPages": [2, 3, 4, 5] }
```

- `action`: `show_page` | `hide_page` | `jump_to_page`.
- `page` and `skipPages` are **1-based** (`page: 0` is ignored). `skipPages` is optional — left out, it's the pages between the trigger's page and the target.
- One rule per entry, no AND/OR joiners — several entries act independently (effectively OR).
- A page with any `show_page` rule **starts hidden**; a jump only lands on a visible page. `jump_to_page` fires as soon as the answer matches and holds the respondent there while it matches — good for a dead-end ineligible page, risky for ordinary branching.

## Recipes

**Hard stop / disqualification** — there is no `end_form`. Put a conditional `alert` (`alertType: "danger"`, `sendToProvider: false`) directly under the question, shown when the disqualifying answer is picked. Alerts don't block submission. If the user wants it blocked (ask first), either:
- add a `disable` rule on the Next/Submit button with the same trigger, or
- add an ineligible last page (heading + alert, **no Submit**) with **two** page rules on the same trigger: `show_page` for that page (so eligible users never reach it) and `jump_to_page` to it.

**"Flag for MD review"** — no flag action exists. Set `sendToProvider: true` + `providerInfo: "medical"` on the question (optionally `properties.providerMetaPairs: [{ "id": "1", "key": "review_priority", "value": "high" }]`), and add a conditional `alert` with `alertType: "warning"` for the patient. Don't invent status fields.

**"Other — please specify"** — any multi-select `choice-multi` that isn't radio auto-appends a "None of these" option (turn off with `showNoneOfAbove: false`; dropdowns never get it). If the source lists its own "None of the above" (or similar), keep the source's option, set `showNoneOfAbove: false`, and put its **label** in `mutuallyExclusiveOptions` — an array of labels, e.g. `["None of the above"]` (JSON-only; no UI control). Otherwise rely on the auto option. Follow-up `text` field `<question fieldId>_other`, shown by `{ "operator": "contains", "value": ["other"] }` on a multi-select or `{ "operator": "equals", "value": ["other"] }` on a radio.

**Hidden fixed value** (campaign code, product slug) — `text` field with `"properties": { "hidden": true, "defaultValue": "nad-plus", "hasDefaultValue": true, "cols": 1 }`. Skipped in preview and validation; value still submitted.

## BMI

```json
{
  "fieldId": "bmi_measurement", "type": "bmi", "label": "Height & Weight", "name": "bmi_measurement",
  "required": false, "sendToProvider": true, "providerInfo": "medical",
  "db_field": "opportunity.clinical.bmi", "order": 6, "validation": {}, "conditions": [],
  "properties": { "cols": 1, "bmiShowScale": true }, "readOnly": true,
  "subfields": [
    { "subfieldId": "bmi_unit_system", "type": "dropdown", "label": "Unit System", "name": "bmi_unit_system",
      "required": false, "sendToProvider": false, "db_field": "", "order": 7, "validation": {}, "conditions": [],
      "properties": { "options": ["Metric (kg/cm)", "Imperial (lbs/inches)"],
                      "defaultValue": "Imperial (lbs/inches)", "hasDefaultValue": true, "cols": 1 },
      "placeholder": "Select unit system" },
    { "subfieldId": "bmi_height", "type": "number", "label": "Height", "name": "bmi_height",
      "required": true, "sendToProvider": true, "providerInfo": "medical",
      "db_field": "opportunity.clinical.height.value", "order": 8,
      "validation": { "minValue": 36, "maxValue": 100 }, "conditions": [],
      "properties": { "cols": 1 }, "placeholder": "inches" },
    { "subfieldId": "bmi_weight", "type": "number", "label": "Weight", "name": "bmi_weight",
      "required": true, "sendToProvider": true, "providerInfo": "medical",
      "db_field": "opportunity.clinical.weight.value", "order": 9,
      "validation": { "minValue": 50, "maxValue": 700 }, "conditions": [],
      "properties": { "cols": 1 }, "placeholder": "lbs" }
  ]
}
```

- Subfields use `subfieldId`. Roles are matched by type, then label (`unit`/`height`/`weight`/`age`/`gender`), then position — label them literally "Unit System", "Height", "Weight". A third `number` subfield becomes an optional **Age** role and a `choice-single` subfield a **Gender** role; don't add them unless asked.
- **The unit dropdown always has `defaultValue` matching the placeholders.** With no unit the canvas assumes metric and imperial inputs give a BMI ~5× too high (a builder save infers it, import doesn't). Keep the two string options exactly as shown. Visible, or `"hidden": true` on the unit subfield to lock it — both fine.
- Parent stays `required: false` (a `true` parent is copied onto every subfield; height/weight are forced required anyway).
- **Conditions are never hosted on subfields.** For logic, reference the parent's `name` — a numeric trigger whose value is the computed BMI: `{ "field": "bmi_measurement", "operator": "greater_than_or_equal", "value": "27" }`. Every rule is false until height and weight are both filled. Rules may also reference a subfield's `name` (e.g. `bmi_weight`) when the source asks about raw height/weight.
- Optional: `bmiScaleRanges`, `bmiAgeMin`/`bmiAgeMax`/`bmiAgeErrorMessage`.

## Buttons

One `button` field renders a whole row of up to 3 buttons. Back + Next is **one** field with `buttonCount: 2`: primary = left (Back), secondary = right (Next/Submit).

```json
{
  "fieldId": "button_nav_p3", "type": "button", "label": "← Back", "name": "button_nav_p3",
  "required": false, "sendToProvider": false, "db_field": "", "order": 12,
  "validation": {}, "conditions": [],
  "properties": {
    "cols": 1, "buttonCount": 2, "buttonWidth": "auto", "buttonRowAlign": "space-between",
    "buttonAction": "previous_page", "buttonColor": "#2b3441", "buttonTextColor": "#FFFFFF",
    "secondaryButtonLabel": "Next →", "secondaryButtonAction": "next_page",
    "secondaryButtonColor": "#2b3441", "secondaryButtonTextColor": "#FFFFFF",
    "buttonSubmitNext": "none"
  }
}
```

Single-page form: one Submit-only row — `buttonCount: 1`, `label` = `settings.submitButtonText`, `buttonAction: "submit"`, `buttonSubmitNext: "none"`, `buttonRowAlign: "flex-end"`.

Page 1 (Next only) is the same with `buttonCount: 1`, `label: "Next →"`, `buttonAction: "next_page"`, `buttonRowAlign: "flex-end"`, no `secondary*` keys.

Last page: same as above but `secondaryButtonLabel` = `settings.submitButtonText` (the right-hand button shows `secondaryButtonLabel`; `submitButtonText` itself isn't displayed, so keep them equal), `secondaryButtonAction: "submit"`, `secondaryButtonSubmitNext: "none"`.

- `buttonAction` / `secondaryButtonAction` / `tertiaryButtonAction`: `none` | `submit` | `next_page` | `previous_page` | `open_modal` (+ `buttonModalTargetId` / `secondaryButtonModalTargetId`) | `close_modal` | `callback`. No `click`.
- Per-button keys follow the prefix: `buttonWidth`/`secondaryButtonWidth`, `buttonColor`, `buttonTextColor`, `buttonTooltip`, and `buttonSubmit*` / `secondaryButtonSubmit*` / `tertiaryButtonSubmit*`.
- `buttonSubmitNext` (only used when that button's action is `submit`): `none` | `jump_page` (+ `buttonSubmitPage`) | `navigate_link` (+ `buttonSubmitUrl` **and** `buttonSubmitNavigateType`: `iframe`/`new_tab`/`replace` — no default, nothing happens without it) | `show_modal` (+ `buttonSubmitModalTargetId`).
- `buttonRowAlign`: `flex-start` | `center` | `flex-end` | `space-between`.
- **No `buttonStyle`** — it doesn't exist.
- Naming: `button_next_p1`, `button_nav_p3`, `button_submit`.

## Doctor's Network

`sendToProvider: true` shares the field with the provider. **Every shared field also needs top-level `providerInfo`:**

| `providerInfo` | use for |
|---|---|
| `patient` | name, email, phone, DOB, sex, address |
| `medical` | clinical answers, BMI, height/weight, meds, allergies, clinical photos (body, skin, scalp) |
| `consent` | `terms` consent boxes, signatures |
| `identity_verification_online` | ID / selfie uploaded in the form |
| `identity_verification_offline` | ID verification done offline |

Share clinical content and contact details; never headings, alerts, dividers or buttons. Omit `providerInfo` when `sendToProvider` is false. Independent of `db_field`.

Optional per-field extras in `properties`: `providerMetaPairs: [{ "id", "key", "value" }]`, and for shared option fields `providerOptions` — a JSON-object **string** mapping option label to provider code, e.g. `"{\"Yes\":\"abc123\"}"`. Only add when the user supplies the codes.

## db_field

`""` or exactly one of:

```
opportunity.first_name   opportunity.last_name   opportunity.name   opportunity.email
opportunity.phone        opportunity.dob         opportunity.gender
opportunity.communication_consent   opportunity.marketing_consent
opportunity.clinical.height.value   opportunity.clinical.weight.value
opportunity.clinical.bmi            opportunity.clinical.allergies
opportunity.clinical.medications
```

## Naming

`fieldId` == `name` == snake_case of the question's subject, not the whole question. Suffixes: `_details` for follow-up text, `_notice` for conditional alerts, `_other` for "please specify". Headings `heading_<section>`. Option values: kebab-case of the label's meaning (`yes`, `no`, `athletic-recovery`).

## Checklist

Run through this before handing the file over:

- [ ] Valid JSON, 2-space indent; `formType` matches page count; page and field `order` contiguous from 0.
- [ ] Every field has `fieldId`, `name`, `type`; all `fieldId`s and `name`s globally unique (BMI subfields included).
- [ ] No `choice-single`, `date-of-birth`, `buttonStyle`, top-level `"hidden": false`, authored `formConditions`.
- [ ] Every option is `{label, value}` with a unique, comma-free kebab-case value and a unique label (BMI unit dropdown excepted).
- [ ] Every rule's `field` is an existing `name` that can hold an answer; option-trigger values are arrays of real option values (or `"None of these"`); single-select uses `equals`, not `contains`; dates are `YYYY/MM/DD`.
- [ ] Every `conditionId` starts with `cond_` and is unique within its field; `target` is the host field's own `fieldId`; multi-rule `logic` is an array one shorter than `rules`.
- [ ] Only allowed operators and actions; self-reference only for Next Page, with `targetValue` = next page's 1-based number (`order` + 2), never on the last page.
- [ ] Page rules use `fieldId`, 1-based `page`/`skipPages`; an ineligible page has both `show_page` and `jump_to_page`.
- [ ] Every `sendToProvider: true` field has a valid `providerInfo`.
- [ ] BMI unit `defaultValue` matches the height/weight placeholders; parent `required: false`; no conditions hosted on subfields.
- [ ] Every `db_field` is `""` or in the list.
- [ ] Every page ends with one button row; middle pages Back + Next (`buttonCount: 2`); last page has `submit`; a single page has Submit only.
- [ ] `cols: 1` on questions; 2 only for paired short inputs.
- [ ] Every source question is present, or listed in the report as not expressible.

## Notes

- **Don't guess unsupported behavior.** If the source asks for something the builder can't do (date math, review queues, AND-ed page rules), say so in the report and use the closest recipe above.
- **The builder is the final check.** Suggest the user import the file, exercise each condition and page rule in Preview (Next Page and page rules only run there), then open the builder's **JSON** button — keys missing from that export were not kept.
- **Learn from hand-edits.** When the user re-exports an edited form and hands it back, diff it against what you generated. Treat each difference as a preference or a correction, apply corrections across the rest of the form, and call out in your report any that contradict this skill.
