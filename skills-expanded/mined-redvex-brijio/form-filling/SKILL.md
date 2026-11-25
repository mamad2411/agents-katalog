---
name: form-filling
description: "Complete forms on authenticated pages: detect field types, handle multi-step forms, fill inputs, select options, and submit safely."
---

# Smart Form Filling

Complete forms on authenticated pages using the user's real browser session
through Brijio. Handles multi-step forms, field type detection, and
common pitfalls.

## Key Improvements (P1.5)

Brijio now uses a **visible-only safe form state model** that:

- Tracks only visible form controls (ignores hidden fields)
- Tracks `valueState`: `empty | filled | unknown` for each control
- Tracks `filledBy`: `brijio | user_or_page` indicating who last set the value
- Prevents stale actions via `visibleContextId` validation
- Validates required fields before submission instead of blind submission

## When to Use

- Filling job applications, checkout forms, sign-up flows, and any web form
  on a page the user is already authenticated on.
- Any task where you need to fill multiple fields in sequence with
  verification between steps.

## Workflow

### 1. Check Connection

Call `list_browsers` to confirm a browser is connected. If the response is
empty or `data.browsers` is an empty array, ask the user to open their
browser and connect the Brijio extension before continuing.

When multiple browsers are connected, note the `browserInstanceId` values
and use the correct one for all subsequent calls.

### 2. Read the Page

Call `read_current_page` with `includeContent: true` to get the full page
context. The response contains:

- `links` — clickable navigation links (use `click_element` with
  `kind: \"link\"`)
- `actions` — button-like elements (use `click_element` with
  `kind: \"action\"`)
- `forms` — form structures with `controls` arrays (use `fill_input`,
  `fill_editable`, `set_checked`, `select_options`, `submit_form`)
- `editables` — standalone contenteditable areas (use `fill_editable`)

Each element has a short-lived `id` (e.g. `e5`) that **expires when the page
changes**. Additionally, the response includes a `visibleContextId` that
represents the current visible form structure state.

**Always re-read the page after any navigation, form submission, or
significant interaction to get fresh IDs and visibleContextId.**

### 3. Identify the Form

Locate the relevant form in the `forms` array. Each form has:

- `id` — use as `formId` in fill/set/select/submit calls
- `controls` — array of input fields, each with:
  - `id` — use as `controlId`
  - `label` — human-readable label (helps match data to fields)
  - `type` — `text`, `email`, `password`, `checkbox`, `radio`,
    `select-one`, `select-multiple`, `textarea`, `hidden`, etc.
  - `valueState` — `empty | filled | unknown` (based on visibility)
  - `filledBy` — `brijio | user_or_page` (who last set the value)
  - `value` — current value (useful for pre-filled fields)
  - `options` — for select/radio controls, the available choices
  - `requiredSource` — `undefined | required | aria-required` (for validation)

### 4. Fill Fields

Fill fields in a logical order (top-to-bottom) using the appropriate tool:

| Field Type          | Tool                                          | Notes                                      |
| ------------------- | --------------------------------------------- | ------------------------------------------ |
| Text input / Search | `fill_input`                                  | Most common field type                     |
| Email / URL / Tel   | `fill_input`                                  | Same tool, different semantic type         |
| Textarea            | `fill_input`                                  | Use `controlId` from the form              |
| Contenteditable     | `fill_editable`                               | Standalone editable, not inside a `<form>` |
| Checkbox            | `set_checked(formId, controlId, true/false)`  | Toggle checked state                       |
| Radio button        | `set_checked(formId, controlId, true)`        | Select one option; cannot uncheck          |
| Select (single)     | `select_options(formId, controlId, [value])`  | Pass one value                             |
| Select (multiple)   | `select_options(formId, controlId, [v1, v2])` | Pass multiple values                       |

**Important**: Each action tool now accepts an optional `visibleContextId`
parameter. When you re-read the page, include this ID in your subsequent
action calls to enable staleness detection:

```json
{
  "formId": "f1",
  "controlId": "c1",
  "text": "John",
  "visibleContextId": "ctx-123" // From read_current_page response
}
```

If the visible form structure has changed since you read the page, the action
will fail with a `stale_context` error instead of silently performing the
wrong action.

For several fields on the same stable page, prefer `perform_batch` over many
individual tool calls once you have read the page and matched all target IDs.
Keep batches small and same-page:

```json
{
  "actions": [
    {
      "type": "write_text",
      "target": { "formId": \"f1\", \"controlId\": \"c1\" },
      "text": \"John\",
      "visibleContextId": \"ctx-123\"
    },
    {
      "type": \"write_text\",
      \"target\": { \"formId\": \"f1\", \"controlId\": \"c2\" },
      \"text\": \"Smith\",
      \"visibleContextId\": \"ctx-123\"
    },
    {
      \"type\": \"select_options\",
      \"target\": { \"formId\": \"f1\", \"controlId\": \"c5\" },
      \"values\": [\"us\"],
      \"visibleContextId\": \"ctx-123\"
    },
    {
      \"type\": \"set_checked\",
      \"target\": { \"formId\": \"f1\", \"controlId\": \"c6\" },
      \"checked\": true,
      \"visibleContextId\": \"ctx-123\"
    }
  ],
  \"continueOnError\": false,
  \"readAfterActions\": true
}
```

Use `readAfterActions: true` when you want the returned batch result to
include a fresh page context for verification. If `data.aborted` is true, the
page navigated during the batch; stop, call `read_current_page`, and continue
with fresh IDs.

### 5. Verify Before Submitting

After filling, call `read_current_page` again to verify:

- All fields show the expected values
- No validation errors are visible
- The form is ready for submission

**Critical**: Before attempting to submit, Brijio automatically validates
visible required fields. If any visible required fields are empty or invalid,
the `submit_form` action will **not** submit the form. Instead, it will return
a `FormValidationError[]` listing the problematic fields.

You **must** check the submit result:

- If `{ ok: true }`: The form was submitted successfully
- If `{ ok: false, error: { code: 'stale_context' } }`: The page changed; re-read and retry
- If `{ ok: false, error: { code: 'browser_error', detail: { reason: 'validation_failed', validationErrors: [...] } } }`: Fix the validation errors listed in `detail.validationErrors`

Never auto-submit forms. Always ask the user to review and submit
manually, unless the user has explicitly asked you to submit.

### 6. Multi-Page Forms (Wizards)

For multi-step forms with \"Next\" / \"Continue\" buttons:

1. Fill all fields on the current page.
2. Verify fields are correct.
3. Click the \"Next\" / \"Continue\" action button.
4. Wait for the page to update (re-read with `read_current_page`).
5. Fill the next set of fields.
6. Repeat until the final review/submit page.

After each page navigation, all previous element `id` values and
`visibleContextId` values are **invalid**. You must re-read the page to get
fresh IDs and context.

## Pitfalls

### Password Fields

`fill_input` returns `browser_error` for `type=\"password\"` inputs. This is
correct browser security behavior. **Skip password fields** and let the
user fill them manually. Do not retry or attempt workarounds.

### Radio Buttons

You **cannot uncheck** a radio button. `set_checked(checked: false)` on a
radio returns `browser_error`. Instead, select a different radio option in
the same group.

### Readonly and Disabled Fields

`fill_input` returns `browser_error` for `readonly` or `disabled` inputs.
Skip these fields — they are not meant to be edited. Their values are often
auto-calculated or pre-populated by the page.

### Short-Lived IDs and Staleness Protection

Element IDs (`e5`, `f2`, `c3`) are **ephemeral**. They expire when:

- The page navigates (any navigation, including form submissions)
- The DOM changes significantly (dynamic content updates, SPA navigation)
- The page refreshes

Additionally, Brijio tracks visible form structure via `visibleContextId`.
If the visible form changes between reading and acting, actions will fail
with a `stale_context` error.

**Always re-read the page after any action that changes the DOM before
referencing new element IDs or visibleContextId.**

Do not run one `perform_batch` across wizard steps or navigation boundaries.
Navigation aborts remaining batch actions and invalidates IDs from the previous
page.

### React and SPA Forms

Brijio injects values via the DOM, which triggers React's synthetic
event system. This works for most modern inputs. If a React textarea or
input doesn't update after filling, it may be a hidden internal editor — look
for a named textarea with content content instead.

### Multiple Browsers

When both Chrome and Safari are connected, `list_browsers` returns multiple
instances. Always specify `browserInstanceId` to target the correct browser.
The IDs look like:

- `safari-d30265e2-04ad-4e44-907a-a79fe287ae46`
- `chrome-eaa9b8ca-1713-42a1-871a-e6747db5341b`

### Contenteditable Outside Forms

Standalone contenteditable elements (rich text editors, comment boxes) appear
in the `editables` list, **not** inside forms. Use `fill_editable` with the
editable's `id`, not `fill_input` with a form/control pair.

## Example: Job Application Form

```
1. list_browsers → Confirm browser connected
2. read_current_page(includeContent: true) → Get page context + visibleContextId
3. Identify application form (id: \"f1\")
4. perform_batch(actions: [
     { type: \"write_text\", target: { formId: \"f1\", controlId: \"c1\" }, text: \"John\", visibleContextId: \"ctx-123\" },
     { type: \"write_text\", target: { formId: \"f1\", controlId: \"c2\" }, text: \"Smith\", visibleContextId: \"ctx-123\" },
     { type: \"write_text\", target: { formId: \"f1\", controlId: \"c3\" }, text: \"john@example.com\", visibleContextId: \"ctx-123\" },
     { type: \"select_options\", target: { formId: \"f1\", controlId: \"c5\" }, values: [\"us\"], visibleContextId: \"ctx-123\" },
     { type: \"set_checked\", target: { formId: \"f1\", controlId: \"c6\" }, checked: true, visibleContextId: \"ctx-123\" }
   ], continueOnError: false, readAfterActions: true)
5. Inspect batch results:
   - If any action failed with stale_context: Go to step 2 to re-read
   - If batch aborted (data.aborted: true): Go to step 2 to re-read
   - Otherwise: Continue
6. read_current_page → Verify filled values are correct
7. submit_form(formId: \"f1\", visibleContextId: \"ctx-456\") →
   - If ok: true → Form submitted, inform user
   - If browser_error with validation_failed: Show validation errors to user
   - If stale_context: Go to step 2 to re-read
8. Inform user: \"Form is filled. Please review and submit when ready.\" (if not auto-submitted)
```
