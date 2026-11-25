---
name: canon-forms
description: Use when designing or auditing forms, inputs, validation, error messages, labels, submit flows, or any data entry interface. Covers field structure, label placement, validation timing, error UX, autocomplete, multi-step flows, and the most common form anti-patterns. Trigger when the user mentions form, input, label, validation, error, submit, signup, login, or checkout.
---

# CANON · Forms

Forms are the highest-stakes interface in any product. A confusing form costs conversions in marketing, costs data in apps, and costs trust everywhere. Most form failures are predictable.

## Quantified Rules

### Field Structure

```html
<div class="field">
  <label for="email">Email address</label>
  <input
    id="email"
    name="email"
    type="email"
    autocomplete="email"
    required
    aria-describedby="email-hint"
  />
  <span id="email-hint" class="hint">We'll never share your email.</span>
</div>
```

| Element | Required | Reason |
|---|---|---|
| `<label>` with `for` | Yes | Click target + screen reader |
| `id` matching `for` | Yes | WCAG 1.3.1 |
| `name` | Yes (for submission) | Server identification |
| `type` | Yes | Native validation + mobile keyboard |
| `autocomplete` | Yes (where applicable) | Browser fill, password managers |
| `required` | If required | Native validation |
| `aria-describedby` | If hint or error | SR announces context |

### Label Placement

| Placement | When | Source |
|---|---|---|
| Above input (block) | **Default**. Best scan speed and mobile-friendly. | Nielsen Norman |
| Inline left | Settings panels with short fixed labels | Acceptable |
| Floating label | Material 3 style | OK; preserve label always-visible at zoom |
| Placeholder as label | **Never** | WCAG 3.3.2 violation |

**Default to labels above inputs.** Closer scan path, more mobile space, easier to align.

### Label-to-Input Gap

```
4–8px between label and its input.
```

Less = cramped. More breaks proximity grouping (Gestalt).

### Field-to-Field Gap

```
16–24px between fields.
```

Tighter feels rushed. Wider breaks form rhythm.

### Input Sizing

| Property | Value | Source |
|---|---|---|
| Height | 44–48px (touch) | iOS HIG, Material 3 |
| Padding | 12px V, 16px H | Material 3 |
| Font-size | **16px minimum on mobile** | Below 16px triggers iOS zoom-on-focus |
| Border | 1px solid, contrast >= 3:1 | WCAG 1.4.11 |
| Border radius | 4–8px | Match other components |
| Min width | 200px (single-line) | Usability |

**The 16px rule is non-negotiable for mobile inputs.** Smaller font triggers iOS zoom on focus, which feels broken.

### Input Types (HTML5)

Use the right type for the right data:

| Data | Type | Mobile keyboard |
|---|---|---|
| Email | `type="email"` | Email keyboard with @ |
| Phone | `type="tel"` | Numeric pad |
| Number | `type="number"` | Numeric (use `inputmode="numeric"` for codes) |
| URL | `type="url"` | URL keyboard |
| Search | `type="search"` | Search keyboard |
| Date | `type="date"` | Native date picker |
| Password | `type="password"` | Standard with show/hide |

```html
<!-- For OTP / numeric codes that aren't math -->
<input type="text" inputmode="numeric" pattern="[0-9]*" autocomplete="one-time-code">
```

### Autocomplete Tokens

```html
<input autocomplete="email">
<input autocomplete="given-name">
<input autocomplete="family-name">
<input autocomplete="street-address">
<input autocomplete="postal-code">
<input autocomplete="cc-number">
<input autocomplete="current-password">
<input autocomplete="new-password">
<input autocomplete="one-time-code">
```

**Always set `autocomplete`.** It powers password managers, browser fill, and saves users seconds. Full token list: https://html.spec.whatwg.org/multipage/form-control-infrastructure.html#autofill

### Validation Timing

| Trigger | When |
|---|---|
| **On submit** | Default. Validate everything, show all errors. |
| **On blur** | After user leaves a field. Good for format checks. |
| **On change** | While typing. Only for password strength meters and constraints (e.g., character count). |
| **Before user enters anything** | **Never.** Don't show errors on a field the user hasn't touched. |

**Rule: do not show errors until the user has had a chance to make them.** A pristine field is not in error.

### Error Messages

| Property | Rule |
|---|---|
| Position | Below the field, before the next field |
| Color | Status error (red) AND an icon (color alone fails 1.4.1) |
| Tone | Specific and actionable, not "Invalid input" |
| Persistence | Stays until corrected, doesn't disappear on next keystroke |
| Live region | `aria-live="polite"` so SR announces |
| Aria | `aria-invalid="true"` on the input, `aria-describedby` linked to error |

```html
<div class="field">
  <label for="email">Email</label>
  <input
    id="email"
    type="email"
    aria-invalid="true"
    aria-describedby="email-error"
  />
  <span id="email-error" role="alert" class="error">
    <svg aria-hidden="true">...</svg>
    Enter a valid email address. Example: name@example.com.
  </span>
</div>
```

### Error Message Examples

| Bad | Good |
|---|---|
| Invalid input | Enter a valid email address. Example: name@example.com. |
| Required | Email is required. |
| Wrong | Password must be at least 8 characters. |
| Try again | This email is already registered. Sign in instead? |
| Field error | Card number must be 16 digits. |

### Submit Button

| Property | Value |
|---|---|
| Position | Bottom of the form, left-aligned (Western reading) or right-aligned (e.g., wizard "Next") |
| Label | Verb describing the action ("Create account", not "Submit") |
| Loading | Disable + spinner inside the button after click |
| Width | Full-width on mobile, content-width on desktop |

**Submit button label is the verb of the form.** "Submit" is generic. "Create account", "Send message", "Place order" tell the user what will happen.

```html
<button type="submit">
  <span>Create account</span>
  <!-- After click: -->
  <!-- <span class="spinner" aria-hidden="true"></span><span class="sr-only">Creating account…</span> -->
</button>
```

### Required vs Optional Markers

| Form length | Marker strategy |
|---|---|
| Short (1–4 fields, mostly required) | Mark **optional** fields |
| Long (5+ fields, mixed) | Mark **required** fields with asterisk + "* required" key |

Use one or the other consistently. Don't mark everything as required.

### Field Width Should Match Expected Input

| Input | Width |
|---|---|
| Postal code | 6–8 chars |
| State | 4 chars or short select |
| Year | 4 chars |
| Name | 20–30 chars |
| Email | 30–40 chars |
| Address line | 40+ chars or full-width |

Field width is a hint about expected input length. A 40-char-wide field for postal code is misleading.

## Multi-Step Forms

| Pattern | When |
|---|---|
| Single page | Forms < 8 fields |
| Stepper / wizard | Forms 8+ fields, conceptually grouped |
| Progressive disclosure | Optional sections that appear conditionally |

**Stepper UX requirements:**
- Show progress (3 of 5)
- Show step names (not just numbers)
- Allow back navigation
- Save progress between steps
- Don't validate future steps based on current

### Question Density Per Step

```
3–7 fields per step.
```

Below 3 feels wasted. Above 7 feels heavy. 5 is the sweet spot.

## Inline Help vs Tooltips

| Pattern | When |
|---|---|
| Inline hint below label | Always-relevant info ("We'll email you a confirmation") |
| Inline hint with icon | Info that requires icon for compactness |
| Tooltip (hover/focus) | Optional help that would otherwise clutter |

**Tooltips must trigger on focus too, not hover only.** Touch and keyboard users need access.

## Anti-Patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| Placeholder as label | Vanishes on input; fails screen readers | Use `<label>` |
| `font-size: 14px` on mobile input | Triggers iOS zoom | 16px minimum |
| Validating before user types | Errors on pristine fields | Validate on blur or submit |
| Errors that disappear on keystroke | Corrected error gone before user sees | Persist until valid |
| Generic "Invalid input" | Doesn't tell user how to fix | Specific, actionable message |
| Missing `autocomplete` | Browsers can't fill | Set on every input |
| Missing input `type` | Wrong mobile keyboard | Use right type |
| Wrong `type` (e.g., `text` for email) | Wrong keyboard, no validation | Match data |
| Color-only error indication | Fails color blindness | Color + icon + text |
| Submit button labeled "Submit" | Generic, no preview | Use the verb |
| Disabled submit until form valid | User can't see what's wrong | Allow submit, show errors |
| Asterisk for required without legend | Unclear meaning | Add "* required" key |
| Marking everything required | No info value | Mark optional or required, not both |
| Required marker but field is optional | Lies | Audit |
| `<div>` form with no `<form>` element | No submit on Enter; no native validation | Use `<form>` |
| Multi-step without progress indicator | User lost in flow | Show step N of M |
| Multi-step that loses data on back | User furious | Persist between steps |
| Address split into 8 fields | Overwhelming | One street-address field with autocomplete |
| Country as text input | Typos, no validation | Use `<select>` or autocomplete |
| Date entered as 3 separate selects | Slow, error-prone | Use `type="date"` or single masked input |
| Phone format restriction (e.g., must be (xxx) xxx-xxxx) | Rejects valid international formats | Accept any format with digits |
| Password rules hidden until error | Frustrating | Show requirements upfront |
| Confirm-email/password fields | Doesn't catch typos; users copy-paste | Use show-password toggle instead |

## Login / Signup Specifics

```html
<!-- Login -->
<input type="email" autocomplete="username" required>
<input type="password" autocomplete="current-password" required>

<!-- Signup -->
<input type="email" autocomplete="username" required>
<input type="password" autocomplete="new-password" required>

<!-- Always include show-password toggle -->
<button type="button" aria-label="Show password" aria-pressed="false">
  <svg>...</svg>
</button>
```

| Pattern | Reason |
|---|---|
| `autocomplete="username"` on email | Password managers fill |
| `autocomplete="current-password"` on login | Distinct from new |
| `autocomplete="new-password"` on signup | Triggers password generator |
| Show-password toggle | Reduces typos, accessibility win |
| Don't forbid paste | Hurts password managers |

## Decision Tree

```
Building a form?
├─ Use <form> with proper submit handling
├─ Each field has <label for>, type, autocomplete, name
├─ Inputs: 16px font, 44px height, 12/16 padding
├─ Required fields: validated on blur or submit (not on load)
├─ Errors: specific message + icon + aria-live
├─ Submit button: verb describing action, full-width on mobile
├─ > 8 fields? Use multi-step with progress
└─ Login/signup? Use correct autocomplete tokens
```

## Audit Checklist

1. Every input has a `<label>` with `for` matching `id`. No placeholder-as-label.
2. Every input on mobile has font-size >= 16px.
3. Every input has the correct `type` (email, tel, url, etc).
4. Every input has `autocomplete` set where applicable.
5. Validation doesn't fire before user has had a chance to enter.
6. Errors are specific, persist until corrected, and have `aria-live="polite"`.
7. Submit button uses an action verb, not "Submit".
8. Submit button shows loading state after click; doesn't allow double-submit.
9. Required marker strategy is consistent (mark required OR mark optional, not both).
10. Multi-step forms show progress and allow back navigation.

## Citations

- WCAG 2.2 SC 3.3.1 Error Identification: https://www.w3.org/WAI/WCAG22/Understanding/error-identification.html
- WCAG 2.2 SC 3.3.2 Labels or Instructions: https://www.w3.org/WAI/WCAG22/Understanding/labels-or-instructions.html
- WCAG 2.2 SC 1.3.5 Identify Input Purpose: https://www.w3.org/WAI/WCAG22/Understanding/identify-input-purpose.html
- HTML autocomplete tokens: https://html.spec.whatwg.org/multipage/form-control-infrastructure.html#autofill
- Nielsen Norman Group, Form Design: https://www.nngroup.com/articles/form-design-placeholders/
- Material 3 Text Fields: https://m3.material.io/components/text-fields/overview
- Apple HIG Text Fields: https://developer.apple.com/design/human-interface-guidelines/text-fields
