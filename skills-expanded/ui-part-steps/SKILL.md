---
name: ui-part-steps
description: "Multi-step flows and step indicators: when to split a task into steps, the indicator with done, current and error steps, moving back and forward, saving progress, validating each step, a review step, and the compact phone version. Read before building a wizard, a checkout or an onboarding flow."
---

# Steps and multi-step flows

The generated wizard splits a six-field form over four screens under a row
of numbered circles, loses the answers when Back is pressed, validates
everything at the end and then drops people on step one under a red banner,
and lets the browser's Back button walk straight out of the flow. This skill
says when steps help at all, how the indicator shows done, current and
failed steps, and how moving, saving, validating, reviewing and confirming
work. The look of the fields is `ui-part-forms`, their logic
`frontend-forms`.

## 1. When steps, and when not

- Use steps when later questions depend on earlier answers (delivery
  options depend on the address, a plan on the team size), when the task is
  long enough to tire (more than about 10 fields that fall into groups), or
  when the order is the real order of the work (a checkout, an application,
  setting up an account).
- 3 to 5 steps. Two steps are usually one page with two sections; past
  five, regroup or cut questions.
- One topic per step, named in one to three words: Contact, Delivery,
  Payment, Review.
- Not for sections people edit in any order (settings are one page with
  sections, `ui-page-settings`), and never tabs for a sequence: tabs are
  views of one thing (`ui-part-tabs`).

## 2. The indicator

```
 (✓) Contact ────── (2) Delivery ────── (3) Payment ────── (4) Review
     done, a link       current              upcoming           upcoming
```

- Above the form on wide screens, as wide as the form column (480 to
  640px): markers 24 to 32px, labels 14px beside or under them, a 1 to 2px
  connector, 24 to 32px above the step's heading.
- A vertical list in a side column (200 to 260px) for long setup flows
  where each step has a line of description.
- States:
  - Upcoming: the number in the muted colour, not a link until reachable.
  - Current: the accent marker, the label in bold, `aria-current="step"`.
  - Done: a check mark, a link back to the step, "(completed)" in its
    accessible name.
  - Needs attention: a warning icon and those words, when a step already
    passed has an error (the server rejected a field, or a later change
    made an earlier answer invalid).
  - Optional: "(optional)" in the label.
- Colour is never the only signal: the check, the number, the weight and
  the words carry the state too.

```html
<nav aria-label="Checkout steps">
  <ol class="steps">
    <li data-state="done"><a href="/checkout/contact">
      <span class="marker" aria-hidden="true">✓</span> Contact
      <span class="sr-only">(completed)</span></a></li>
    <li data-state="current" aria-current="step">
      <span class="marker" aria-hidden="true">2</span> Delivery</li>
    <li><span class="marker" aria-hidden="true">3</span> Payment</li>
    <li><span class="marker" aria-hidden="true">4</span> Review</li>
  </ol>
</nav>
```

A `nav` with an ordered list, not a `tablist`. The design system's stepper
is fine when it has one (Mantine `Stepper`, MUI `Stepper`, Chakra `Steps`,
PrimeVue `Stepper`, Nuxt UI `Stepper`), themed with the tokens; the flow's
logic still lives in the form and the router.

## 3. On a phone

```
 Step 2 of 4 · Delivery
 ▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░░
```

- Below about 640px the row of labels does not fit: "Step 2 of 4" and the
  step's name as text, a 4px progress bar under it, and the full list in a
  disclosure ("All steps") when going back to a done step matters.
- Continue full width at the end of the step; Back as a quiet button under
  it, or as the back arrow with its word in the top bar. One of the two,
  the same on every step.
- `enterkeyhint="next"` on fields that lead to another and `"done"` on the
  last, with the right keyboard for each field (`ui-part-forms`).

## 4. Moving back and forward

- Each step ends with Back at the left (secondary) and Continue at the
  right (primary), on one row aligned with the form's edges.
- Continue says where it goes ("Continue to payment"). The last button
  says what happens and, when it costs money, how much ("Pay Rp [total]",
  "Submit application"). Never "Next" or "Submit" on the final step.
- Back never loses answers and never validates: people go back with half a
  step filled.
- The first step has no Back. Leaving the flow asks to confirm only when
  something was entered.
- Every step has its own URL (`/checkout/delivery`, or `?step=delivery`):
  the browser's Back goes to the previous step, reload stays put, and a
  later step opened before its turn redirects to the first incomplete one.
- Done steps are links in the indicator. After editing one, the user comes
  back to where they were ("Save and return to review"), not through every
  step again.

## 5. Keeping progress

- One store for the whole flow, each step rendering its slice: one
  react-hook-form `useForm` (or TanStack Form, or a small store) across the
  steps. A step leaving the screen must not clear its fields
  (`shouldUnregister: false`, react-hook-form's default).
- Persist by the stakes:
  - A short flow (a checkout): the server's cart and order draft, or
    `sessionStorage` for plain fields.
  - A long one (an application, onboarding): a draft saved on the server
    at every Continue, resumable on another device, with "Saved" shown and
    a "Continue where you left off" way back in.
  - Never card numbers, passwords or identity documents in browser storage.
- Warn before leaving only while something is unsaved (`beforeunload` and
  the router's blocker, `frontend-forms`).

## 6. Validating each step

- On Continue, validate that step's fields only, then move. Fields also
  validate when left, and on each change once they have shown an error.

  ```tsx
  import type { Path } from "react-hook-form";

  const steps: { id: string; fields: Path<Application>[] }[] = [
    { id: "about-you", fields: ["name", "email"] },
    { id: "business", fields: ["business.name", "business.country"] },
    { id: "documents", fields: ["documents"] },
    { id: "review", fields: ["consent"] },
  ];

  async function next() {
    const ok = await form.trigger(steps[index].fields, { shouldFocus: true });
    if (ok) router.push(`/apply/${steps[index + 1].id}`);
  }
  ```

- On error: stay, focus the first invalid field, and on a step with more
  than a few fields put a summary at the top linking to each field.
- Asynchronous checks (is the name free, can we deliver there) run on the
  step where the field is, their wait shown on the Continue button.
- The server validates everything again at the end. An error that belongs
  to an earlier step opens that step with the message on its field, and
  the indicator marks it "Needs attention".
- One schema shared with the server where the stack allows (zod, valibot),
  split per step, so both sides say the same thing.

## 7. Review, submit, confirm

- A review step before anything that costs money or cannot be undone:
  every answer grouped by step, an "Edit" link per group, the totals, the
  consent the law requires (never pre-ticked), and the final button naming
  the action.
- Submitting: the button shows progress and keeps its width, a second click
  does nothing, and the request carries an idempotency key so a retry
  cannot create a second order (`backend-api`, section 6).
- The confirmation is a page, not a toast: that it is done, the reference
  number, what happens next and when, where the email went. Redirect after
  the POST so reload and Back cannot submit again, and Back does not
  re-enter the finished flow.

## 8. Focus, themes, motion

- When the step changes, move focus to its heading (`tabindex="-1"` and
  `focus()`) and update the title ("Delivery (step 2 of 4) · Checkout"),
  so a screen reader says where the user is.
- Errors are read with their fields (`aria-describedby`, `aria-invalid`);
  the summary takes focus when it appears.
- Markers and connectors from tokens, with 3:1 for the current and done
  states in both themes (`ui-themes`).
- The step's content changes at once or with a 150 to 200ms crossfade,
  never sliding sideways (`motion-interface`, section 7); the phone's bar
  fills with `scaleX`; nothing moves under reduced motion.

## Check it

- The whole flow by keyboard: each step's heading takes focus, Enter in a
  field does not skip validation, done steps are links.
- Browser Back and Forward on every step, reload on every step, a later
  step's URL opened directly: answers kept, the first incomplete step
  shown.
- An invalid step, then a server rejection of a field from an earlier
  step: the right step opens with the message, marked in the indicator.
- Double-click the final button on a throttled network: one order.
- `preview` at 360px: "Step 2 of 4", a full-width Continue, nothing
  overflowing; at 1440px, the indicator as wide as the form.

## Avoid

Steps for a short form; more than five; numbered circles without labels;
the current step shown by colour alone; Back that clears or validates; a
flow the browser's Back button leaves; validation only at the end; "Next"
or "Submit" on the final button; a review without Edit links; a toast as
the confirmation; tabs used as steps; progress lost on reload.
