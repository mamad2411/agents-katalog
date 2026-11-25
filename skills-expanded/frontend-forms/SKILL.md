---
name: frontend-forms
description: "Form behaviour: native inputs first, a form library with a schema, when to validate, error messages that say how to fix, submission and double submit, server errors mapped to fields, unsaved changes, autosave, multi-step forms and file inputs. Read before building a form's logic; its look is `ui-part-forms`."
---

# Form behaviour

The generated form is a stack of `div`s with placeholders for labels,
`type="number"` for a card number, red borders from the first keystroke,
"Invalid input" under every field, a submit button that sends twice on a
double click, and a server error that wipes everything typed. People fill
forms to get something done; this is how a form helps them finish. The
look is `ui-part-forms`, the page `ui-page-form`, the whole frontend
`frontend`.

## 1. Native first

- A real `<form>` with a `<button type="submit">`, so Enter submits and
  browsers, password managers and assistive technology know what it is.
  Other buttons inside it are `type="button"`.
- A `<label for>` on every field (a placeholder is an example, never the
  label); radios and checkboxes that belong together in a `<fieldset>`
  with a `<legend>`.
- The right `type`, `autocomplete`, `inputmode` and `enterkeyhint`, so
  phones show the right keyboard and browsers fill what they know:

| Field | Attributes |
|---|---|
| Full name | `autocomplete="name"` |
| Email | `type="email" autocomplete="email"` |
| Phone | `type="tel" autocomplete="tel"` |
| Street address | `autocomplete="address-line1"` and `address-line2` (or `street-address` on one textarea) |
| City, region | `autocomplete="address-level2"`, `address-level1` |
| Postcode | `autocomplete="postal-code"`, plain text (many countries use letters) |
| Country | a searchable combobox (`ui-part-choices`) whose input has `autocomplete="country-name"` |
| Card number, expiry, CVC | `inputmode="numeric"` with `autocomplete="cc-number"`, `cc-exp`, `cc-csc` |
| One-time code | `inputmode="numeric" autocomplete="one-time-code"`, one field that takes a paste |
| New password (sign-up, change) | `type="password" autocomplete="new-password"` |
| Sign-in | `autocomplete="username"` (with `webauthn` for passkeys), then `current-password` |
| Search | `type="search" enterkeyhint="search"` |

- `type="number"` only for quantities people step through: it accepts `e`,
  drops leading zeros and changes on scroll. Codes and card numbers are
  text with `inputmode="numeric"`; postcodes too, where every code is digits.
- `required`, `minlength` and `maxlength` tell the browser and assistive
  technology the rules; when the library shows its own messages,
  `noValidate` on the form keeps the browser's bubbles from competing.
- Inputs at 16px or larger, or iOS Safari zooms the page on focus.

## 2. A library and one schema

- React: react-hook-form with `zodResolver` (`@hookform/resolvers`);
  TanStack Form for typed, framework-agnostic forms; Conform when forms
  post to server actions or React Router actions and must work without
  JavaScript. Vue: VeeValidate with `@vee-validate/zod`. SvelteKit:
  Superforms. Angular: typed reactive forms.
- One schema per form in the feature's `api/` folder, shared with the
  server when both are TypeScript (the server validates again anyway), its
  messages through i18n keys (`i18n`).

```tsx
const InviteSchema = z.object({
  email: z.email("Enter an email address, like name@example.com"),
  role: z.enum(["member", "admin"], { error: "Choose a role" }),
});
type Invite = z.infer<typeof InviteSchema>;

const form = useForm<Invite>({
  resolver: zodResolver(InviteSchema),
  mode: "onTouched", // first check when a field is left, then on every change
  defaultValues: { email: "", role: "member" },
});
```

## 3. When to validate

- A field is checked when it is left, then on every change once it shows
  an error, so the error clears the moment it is fixed (react-hook-form's
  `mode: "onTouched"`). Never on the first keystroke: "Enter a valid
  email" while someone is still typing it is shouting.
- On submit, everything is checked and focus moves to the first invalid
  field (react-hook-form's `shouldFocusError`, on by default).
- The submit button stays enabled while fields are invalid: a disabled
  button cannot say what is missing. Pressing it shows the errors.
- Checks that need the server (a username taken, a coupon valid) run when
  the field is left, or debounced 300 to 500ms, with "Checking" shown, and
  again on submit.
- Rules across fields (end after start, passwords match) report on the
  field the person will change: `refine` with a `path` in the schema.

## 4. Messages that say how to fix it

- Under the field, in words, tied with `aria-describedby`, with
  `aria-invalid="true"` on the input; never only a red border
  (`frontend-accessibility`).
- What is wrong and what to do, in the person's terms:

| Not | Say |
|---|---|
| Invalid input | Enter a date after today |
| Required | Enter your email address |
| Invalid format | Enter a postcode, like 40115 |
| Too short | Use 12 characters or more |
| Out of range | Enter an amount between 10,000 and 5,000,000 |

- A long form also shows, after a failed submit, a summary at the top: a
  heading ("There is a problem"), each error as a link to its field, focus
  moved to the summary, and "Error: " added to the start of the page title.

```tsx
const id = useId();
const error = form.formState.errors.email;
const describedBy = [`${id}-hint`, error && `${id}-error`].filter(Boolean).join(" ");

<label htmlFor={id}>Email</label>
<p id={`${id}-hint`}>We send the invitation to this address.</p>
<input id={id} type="email" autoComplete="email" aria-invalid={error ? true : undefined}
  aria-describedby={describedBy} {...form.register("email")} />
{error && <p id={`${id}-error`}>{error.message}</p>}
```

## 5. Submission

- While sending, the button says what is happening ("Sending invite") with
  a spinner, keeps its width, and takes no second press
  (`disabled={formState.isSubmitting}`), so a double click sends once.
- Success is said (a `role="status"` message, or the next page), then the
  form resets or the page moves on, focus on the message or the new
  heading. Failure keeps everything typed; the dialog or page stays open.
- A `422` with field errors marks those fields; anything else shows at the
  top of the form with what to do (`frontend-errors`):

```ts
async function onSubmit(values: Invite) {
  try {
    await sendInvite.mutateAsync(values);
    form.reset();
  } catch (error) {
    if (error instanceof ApiError && error.status === 422) {
      Object.entries(error.fields).forEach(([field, code], i) =>
        form.setError(field as keyof Invite, { type: "server", message: t(`errors.${code}`) },
          { shouldFocus: i === 0 }));
      return;
    }
    form.setError("root.server", { message: describeError(error).message });
  }
}
```

- Payments and orders carry an idempotency key, so a retry after a timeout
  does not charge twice (`frontend-data`).
- Progressive enhancement where the stack offers it: server actions
  (`<form action={action}>` with React 19's `useActionState`), React
  Router's `<Form>`, SvelteKit form actions with `use:enhance`. The form
  posts before the JavaScript loads; Conform or Superforms keep one schema
  for both sides.

## 6. Unsaved changes

- Warn on leaving only when the form is dirty and not being submitted
  (`formState.isDirty`); never on a form that autosaves.
- Reload, closing the tab, typing a URL: `beforeunload`, which shows the
  browser's own text:

```ts
useEffect(() => {
  if (!isDirty) return;
  const warn = (event: BeforeUnloadEvent) => {
    event.preventDefault();
    event.returnValue = true; // older Chromium needs it
  };
  window.addEventListener("beforeunload", warn);
  return () => window.removeEventListener("beforeunload", warn);
}, [isDirty]);
```

- Navigation inside the app: the router's blocker (React Router's
  `useBlocker`, TanStack Router's `useBlocker`, Vue Router's
  `onBeforeRouteLeave`, SvelteKit's `beforeNavigate` with `cancel()`),
  with a dialog naming the loss: "Leave without saving? Your changes to
  this invoice will be lost.", "Keep editing" as the default, and
  "Leave". The Next.js App Router has no full blocker (`<Link onNavigate>`
  cancels link clicks, not Back): save a draft there instead.

## 7. Autosave

- For long edits (a document, a profile, settings with many fields), not
  for actions with consequences: sending, paying and publishing keep an
  explicit button.
- Save 1 to 2s after the last change, when a field is left, and when the
  page is hidden (`visibilitychange`, with `fetch(url, { keepalive: true })`),
  one save in flight at a time; changes made meanwhile go in the next.
- Status in a `role="status"` region near the title: "Saving", "Saved at
  14:02", "Not saved: you are offline" with what happens to the changes,
  "Could not save. Retry".
- Send the version the edit started from (`If-Match` or a `version`
  field); on a `409`, show that it changed elsewhere and let the person
  compare, never overwrite silently (`backend-api`).

## 8. Multi-step forms

- Only when the task is long or later steps depend on earlier answers:
  three to five steps, each with a name.
- One URL per step (`/checkout/shipping`) or one state per step; Back, the
  browser's or the button, returns with the answers kept: one form
  instance across steps, or a draft in `sessionStorage` (never card numbers
  or passwords).
- Validate the step before moving on (react-hook-form's
  `trigger(stepFields)`), focusing the first error.
- Show the place: "Step 2 of 4: Shipping", the step names, done steps
  clickable.
- A review step before the one final submit, each section with a "Change"
  link that returns to the review; the confirmation gives a reference and
  what happens next.

## 9. Particular inputs

- **Names**: one "Full name" field (and "What should we call you?" when
  needed). Any script, apostrophes, hyphens, spaces and one-letter names are
  valid: no "letters only" rule, no forced capitals.
- **Email**: trimmed, lightly checked; the confirmation email is the test.
- **Phone**: a country code defaulting to the user's country, parsed and
  validated with `libphonenumber-js`, stored as E.164 (`+6281234567890`),
  shown in the national format.
- **Addresses**: country first, and the fields follow it (not every
  country has states or postcodes); an address lookup as a shortcut, never
  the only way in.
- **Dates**: `ui-part-dates`. A date of birth as three fields (day, month,
  year: `bday-day`, `bday-month`, `bday-year`); send ISO `YYYY-MM-DD`.
- **Money**: text with `inputmode="decimal"` and the currency beside it,
  parsed by locale (`1.500.000` in Indonesian, `1,500,000` in English),
  sent as an integer in the smallest unit with its currency.
- **Passwords**: a show and hide button (`aria-pressed`, "Show password"),
  paste allowed, the rules shown before typing, at least 64 characters
  accepted (`backend-auth`). Do not fight password managers with
  `autocomplete="off"`.
- **Passkeys**: `autocomplete="username webauthn"` on the sign-in username
  offers saved passkeys in the autofill list.
- **Choices**: radios for up to about 7 options, a select or combobox
  beyond; consent as one checkbox, unticked.
- **Files**: a real button that opens the chooser, types and size limit
  stated before choosing (`ui-part-uploads`); client checks give quick
  feedback, the server decides (`backend-files`).

## 10. Security

The server validates everything: client validation is a convenience
anyone can skip. Prices, roles and owner ids never come from a form field,
hidden or not. Forms that change state are protected against CSRF
(`frontend-security`); sign-in, sign-up and reset answer a `429` with
"Too many attempts. Try again in 30 seconds." (`backend-security`).

## Check it

- Keyboard only: Tab reaches every field in order, Enter submits, focus
  lands on the first error, the summary's links jump to their fields.
- A screen reader reads each label, hint and error when the field is
  focused (`frontend-accessibility`).
- Autofill: the browser fills name, email, address and card; a password
  manager offers to save on sign-up and fills on sign-in.
- On a phone at 360px: the right keyboard for each field, no zoom on focus.
- Throttled network, double click on submit: one request (the Network
  panel, or a counter in the MSW handler); the pending state shows.
- MSW answers 422 with field errors, then 500: fields marked, then a
  message at the form; nothing typed is lost.
- A dirty form warns on reload; a clean one does not.
- Tests fill, submit and assert the errors and the success
  (`frontend-testing`); `preview` finds no unnamed control.

## Avoid

Placeholders as labels; `type="number"` for codes; errors on the first
keystroke; a disabled submit button that never says why; "Invalid input";
errors shown only in red; a form that sends twice or forgets what was
typed; server field errors shown as one generic toast; warnings on clean
forms; autosave for payments; client validation trusted by the server; a
price or role taken from a hidden field; `autocomplete="off"` on
credentials.
