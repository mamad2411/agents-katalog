---
name: accessible-forms
description: Every form control must have a programmatic label, clear error identification, and grouped fields where appropriate
---

# Accessible Forms

Forms are among the most complex accessibility surfaces. WCAG 2.2 SC 1.3.1 (Info and Relationships), SC 3.3.1 (Error Identification), SC 3.3.2 (Labels or Instructions), and SC 4.1.2 (Name, Role, Value) all apply.

## Rules

- **Every input must have a programmatically associated label.** Use `<label htmlFor={id}>` pointing to the input's `id`. Placeholder text is not a label — it disappears on input and is not read by all screen readers on focus.
- **Visually hidden labels are acceptable, visible labels are preferred.** Use `.sr-only` to visually hide a label only when the surrounding context makes the label redundant (search field inside a search landmark). Do not skip the label element.
- **Use `aria-describedby` to associate hint text and error messages** with their control. Multiple ids are space-separated: `aria-describedby="hint-email error-email"`.
- **Error messages must identify the control and describe what is wrong** (WCAG 3.3.1). "This field is required" is acceptable; removing the field's border color alone is not.
- **Set `aria-invalid="true"` on a field when it has a validation error.** Screen readers announce this state; clear it when the error is resolved.
- **Group related controls with `<fieldset>` and `<legend>`.** Radio buttons, checkboxes, and date part fields (day/month/year) must be grouped so their collective label is available to assistive technology.
- **Indicate required fields.** Do not use color alone. A visible asterisk (`*`) is conventional; pair it with `aria-required="true"` (or the native `required` attribute) and explain the asterisk convention at the top of the form.

## Examples

```tsx
// BAD — placeholder only; no <label>; no error association
<input
  type="email"
  placeholder="Email address"
  className={hasError ? 'border-red' : ''}
/>
{hasError && <p>Invalid email</p>}

// GOOD
<div>
  <label htmlFor="email">
    Email address <span aria-hidden="true">*</span>
  </label>
  <input
    id="email"
    type="email"
    required
    aria-required="true"
    aria-describedby={hasError ? 'email-error' : 'email-hint'}
    aria-invalid={hasError ? 'true' : undefined}
  />
  {!hasError && (
    <p id="email-hint" className="hint">We'll never share your email.</p>
  )}
  {hasError && (
    <p id="email-error" role="alert">
      Enter a valid email address.
    </p>
  )}
</div>
```

```tsx
// BAD — radio buttons with no group label
<div>
  <input type="radio" id="card" name="payment" value="card" />
  <label htmlFor="card">Credit card</label>
  <input type="radio" id="paypal" name="payment" value="paypal" />
  <label htmlFor="paypal">PayPal</label>
</div>

// GOOD — fieldset + legend provides the group label
<fieldset>
  <legend>Payment method</legend>
  <label><input type="radio" name="payment" value="card" /> Credit card</label>
  <label><input type="radio" name="payment" value="paypal" /> PayPal</label>
</fieldset>
```

## Gotchas

- `aria-label` on an `<input>` overrides the `<label>` element in the accessibility tree. Use it only when there is no visible label and `<label>` cannot be used.
- `role="alert"` on an error container causes screen readers to announce it immediately when it appears or changes. Do not use it for static text that is always present.
- Autocomplete attributes (`autocomplete="email"`, `autocomplete="new-password"`) help password managers and users with cognitive disabilities; include them on personal data fields.
- Custom select/combobox components must replicate the full ARIA combobox pattern. Default to native `<select>` and style it; reach for a custom component only when the native element's styling constraints are genuinely blocking.
