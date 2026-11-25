---
name: ui-page-form
description: "How to build a page whose job is one form (sign-up, booking, application, checkout step, contact): the column and its intro, grouped sections, steps and progress, trust notes only when true, inline validation, a review before submitting, a submit button that names the outcome, the confirmation page, keeping input through errors, the phone layout and accessibility. Read before building or reworking a form page."
---

# Form page (sign-up, booking, application, checkout, contact)

The generated form page: a hero above a card of twelve fields in two
columns, placeholders for labels, asterisks nobody explained, "Submit" at
the end, errors shown as red borders, a failure that empties every field,
and "Thank you!" with no reference and no next step. The person came to
finish one task. The page is the form, plus what they need to trust it and
get through it; this skill gives both.

One kind of page. The measures are in `ui-layout`; a field's anatomy is in
`ui-part-forms`, steps in `ui-part-steps`, the behaviour (when to validate,
libraries, server errors) in `frontend-forms`. Signing in has its own page
(`ui-page-sign-in`).

## 1. Before the first field

- Name the outcome; the title says it: "Book a first visit", not "Booking
  form". The submit button, the confirmation heading and the email all use
  the same words.
- List every field with why it is needed now. Cut what can be asked later
  or found another way: every field loses some people. Mark optional
  fields "(optional)" in the label; with most fields required, no
  asterisks.
- The intro, one to three lines under the title: what happens after sending
  and when ("We confirm by WhatsApp within one working day"), how long the
  form takes if you know, what to have ready (an ID number, a photo), the
  price if it costs anything. Facts you were not given stay placeholders.
- One page or steps (section 4).

## 2. The skeleton

```
┌──────────────────────────────────────────────────────────────────────┐
│ ◉ Clinic name                                  Questions? [phone]    │ quiet header
├──────────────────────────────────────────────────────────────────────┤
│   Book a first visit                          ┌ Your visit ────────┐ │
│   We confirm by WhatsApp within a working     │ Physio, 45 min     │ │
│   day. Takes about 3 minutes.                 │ Tue 14 Oct, 10:00  │ │
│                                               │ [Price]            │ │
│   Step 2 of 3 · Your details                  │ Change             │ │
│   ████████████████░░░░░░░░                    └────────────────────┘ │
│   Full name                                                          │
│   [                                   ]                              │
│   Phone (WhatsApp)                                                   │
│   We only use it for this booking.                                   │
│   [                                   ]                              │
│   Notes for the therapist (optional)                                 │
│   [                                   ]                              │
│   [ Continue to review ]   Back                                      │
└──────────────────────────────────────────────────────────────────────┘
```

- One column 480 to 560px wide (up to 640px when short fields pair),
  left-aligned with the page header inside an app shell, centred on a page
  of its own. Labels above fields.
- The summary (what is booked or bought, the total) beside the form on
  wide screens, 280 to 360px, sticky below the header; below it, or
  collapsed at the top with the total showing, on a phone.
- The steps shown when there are more than one; the primary action at the
  end, aligned with the fields' left edge, full width on a phone.
- Spacing: label to field 6 to 8px, field to field 16 to 24px, group to
  group 32 to 48px. Fields 40 to 48px tall, 44px or more to the touch.
- On a checkout or a long application the header is quiet: the name and a
  way to get help, no navigation to wander off through.

## 3. Fields and groups

- One column. Two side by side only for short pairs (city and postcode,
  expiry and security code).
- Related fields in a `fieldset` with a `legend` ("Contact", "Delivery
  address"); on a long page each group also gets an `h2`.
- Help text between the label and the field, tied with `aria-describedby`,
  so it is read before typing. Field width hints the length expected on
  wide screens (a postcode is short); full width on a phone.
- The right type and `autocomplete`, so phones show the right keyboard and
  browsers fill what they know:

| Field | Markup |
|---|---|
| Full name | `autocomplete="name"`, one field unless the system needs parts |
| Email | `type="email" autocomplete="email"` |
| Phone | `type="tel" autocomplete="tel"` |
| Address | `street-address` (or `address-line1`, `address-line2`), `postal-code`, `address-level2` for the city, `country` |
| Date of birth | three short fields with `bday-day`, `bday-month`, `bday-year`, not a calendar |
| Amount | `inputmode="decimal"`, the currency as text before the field |
| A code sent by SMS or email | `autocomplete="one-time-code" inputmode="numeric"` |
| Card details | the payment provider's own fields, never yours |

- Choices: radios for up to about five, visible at once; a `select` for a
  long list; a searchable combobox for a very long one (`ui-part-choices`).
- Names are not validated for letters (apostrophes, single names, spaces);
  phone numbers accept spaces and are normalised on the server.
- Never ask twice: "Billing address same as delivery", ticked; answers from
  earlier steps carried forward (WCAG 2.2, Redundant Entry).

## 4. Steps and progress

- One page when it fits in about two phone screens or the parts are
  independent. Steps when later questions depend on earlier ones, or the
  task has stages (details, delivery, payment): three to five of them
  (`ui-part-steps`).
- "Step 2 of 3 · Your details" in text above the step's heading, with a
  bar or a step list on wide screens; done steps can be revisited.
- Each step validated before moving on; Back keeps every answer; the
  forward button names the next step ("Continue to payment").
- Progress kept: a URL per step, or a saved draft, so a reload or a lost
  connection does not start over. "Save and continue later" (a link by
  email) only when the backend keeps drafts.

## 5. Validation and errors

- When a field is left, then as they type once it has shown an error; on
  submit, check everything and move focus to the first invalid field, or
  to an error summary at the top of a long form linking to each field
  (`frontend-forms`).
- The message under its field says how to fix it: "Enter a date after
  today", "Enter a phone number with its area code, like 0812 3456 7890".
  `aria-invalid="true"` and `aria-describedby` on the field; never colour
  alone.
- The submit button stays enabled: a disabled one cannot say what is wrong.
- Server answers: field errors (422) put on their fields; anything else
  above the button with what to do ("We could not send this. Check your
  connection and try again."). Every value stays where it was.
- A declined payment: the provider's reason in plain words and another way
  to pay. An expired session: the input saved (a draft in `sessionStorage`)
  and restored after signing in again. Leaving a filled form asks first.

## 6. Trust, only when true

- A privacy note beside the field it concerns ("We only use it for this
  booking"), linking to the privacy policy that exists.
- Payment through the provider's hosted fields or checkout (Stripe Payment
  Element, Midtrans Snap, Xendit), said plainly ("Payment by Stripe. We
  never see your card number."), with the accepted methods as text or
  their official marks. No invented security seals or "SSL secure" badges.
- Every cost (fees, delivery, tax) shown before the last step; nothing new
  appears on the review.
- A way to get help (phone, WhatsApp, email) in view on long forms.
- Marketing consent unticked; terms as a sentence with a link beside the
  button ("By booking you agree to the [cancellation policy]"), a checkbox
  only where the law or the business requires one.
- Spam: a honeypot field and a server rate limit first; Cloudflare
  Turnstile or hCaptcha in their managed modes when needed; never a puzzle.
- No countdown timers or "2 slots left" unless the system counts them.

## 7. Review and submit

- For long or costly forms, a review step: the answers grouped as asked,
  a "Change" link per group (it returns to the step, then back to the
  review), the total, the terms line.
- The button names the outcome: "Book appointment", "Send application",
  "Pay Rp 450.000"; never "Submit". While sending: a spinner inside, the
  width kept, "Booking…", `aria-busy="true"`, further clicks ignored; an
  order or payment is sent with an idempotency key (`backend-api`).
- On success, redirect to the confirmation's own URL (post, redirect, get)
  so a reload does not send it again.

## 8. The confirmation page

```
│  Your visit is booked                                        │
│  Reference  KLN-48213  (Copy)                                │
│  Physio, 45 min · Tue 14 Oct, 10:00 · [Clinic address]       │
│  What happens next                                           │
│  1. We confirm by WhatsApp by 17:00 today.                   │
│  2. Arrive 10 minutes early; bring [what to bring].          │
│  We sent the details to name@example.com.                    │
│  [ Add to calendar ]   Change or cancel · Back to the site   │
```

- The heading states the outcome, not "Success!" or "Thank you!".
- The reference number, copyable; the details as a short summary.
- What happens next and when, and what the person must do, only as the
  business states it. "We sent the details to…" only if an email is sent.
- For bookings, "Add to calendar" (an `.ics` file, a Google Calendar
  link); how to change or cancel; a link onward. Printable. No confetti.
- `noindex`, and no personal data in the URL.

## 9. On a phone

- One column, 16 to 20px side padding, fields full width and 44 to 48px
  tall, input text 16px or more (iOS Safari zooms into smaller text).
- The keyboard fits the field (`type`, `inputmode`), `enterkeyhint="next"`
  to move on and `"send"` or `"done"` on the last field.
- The summary collapsed at the top with its total ("Show summary ·
  Rp 450.000"), or after the form.
- The primary action at the end, full width, with Back as a quieter link;
  no sticky bar that sits over the fields while the keyboard is open.
- After a failed submit, the error summary or the first error scrolled
  into view with focus on it.

## 10. Accessibility

- A visible `label` for every field; `fieldset` and `legend` for radio and
  checkbox groups; required and optional said in words.
- A real `form` with a submit button, so Enter sends it; the tab order
  follows the visual order; custom widgets from the component library.
- Errors announced: the summary with `role="alert"`, or focus moved to it.
- A time limit warns before it ends and can be extended (WCAG 2.2.1).
- Paste allowed everywhere, password managers welcome (WCAG 2.2, Accessible
  Authentication).

## 11. Public forms and search

A contact, booking or application page is found by search: a title with
the task and the business ("Book a physio visit · [Clinic name]"), a
description, the form in the served HTML. Review, step and confirmation
pages are `noindex` (`frontend-seo`).

## Check it

- Fill it with the keyboard only, then with the browser's autofill: name,
  email, phone and address fill in.
- Submit it empty: every error in words, focus on the first; fix one and
  watch its message clear as you type.
- Force a failure (offline, or a mocked 422 and 500): nothing typed is
  lost, the fields are marked, the message says what to do.
- Double-click the submit button: one request. Reload the confirmation and
  press Back from it: nothing is sent twice.
- `preview` at 360, 768 and 1440px: no overflow, touch targets, contrast,
  named controls; `ui_check` for "Submit", invented badges and filler.

## Avoid

Placeholders as labels; two columns of unrelated fields; asterisks with no
key; "Submit"; a disabled button with no reason; errors as red borders
only; a failure that clears the form; fees revealed at the end; invented
trust badges, countdowns and scarcity; a second field to confirm the email;
CAPTCHA puzzles; an account required before a guest can pay; a pop-up over
the form; "Thank you!" with no reference and no next step.
