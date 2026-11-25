---
name: effect-form-e2e
description: Use when adding or changing a form, a field's validation rules, or a Playwright test in this repository. Covers why a form is effect-form and lives in the app rather than the design system, declaring field rules once in the contract, telling a validation failure apart from a refusal, and the e2e harness's rules — a user per test, waiting on a condition rather than sleeping.
---

# A write is a form, and a form is effect-form

`FormReact.make` over a `FormBuilder`, living in the **app** rather than in
`@vantion/ui`. The library binds the submit into the form definition, so a shared
presentational component taking `onCreate` as a prop cannot be one. `apps/design` renders
plain inputs for the layout, because validation and submit state are the part of a form
that has nothing to do with how it looks.

That also _removes_ a problem rather than managing it: effect-form does not render its
fields during SSR, so there is no window in which somebody can type into a control that is
not listening.

## A field's rules are declared once, in the contract

`ContactFields` in `ContactRpc.ts` is what the `CreateContact` payload is built from **and**
what the form validates with, so the form refuses exactly what the server would.

```ts
export const ContactFields = {
  fullName: Schema.String.check(Schema.isNonEmpty({ message: "Enter a name." })),
};
```

Every check carries a `message`, because that is what a person reads. They were two
declarations of one rule once — the procedure checked `isNonEmpty` with no message while
the screen kept a readable copy — and the server's was the version nobody could read.

For a rule a regex cannot express, `Schema.makeFilter` returns a sentence or `undefined`.
`EndpointFields.url` is the worked example, and the rule it enforces is the difference
between a webhook form and server-side request forgery.

## A failed submit is two different things

`submitMessage` in `apps/web/src/lib/form/result.ts` tells them apart: a `SchemaError` is
the form failing to decode, anything else came back from a server. Saying "check the fields
above" to somebody whose permission was denied sends them looking in the wrong place.

The validation case is named rather than inferred from everything that is not one
particular request error. Written the other way round, every error added later inherits the
wrong message.

**A refusal worth acting on gets its own sentence.** `LimitReached` carries the number, so
the screen says "this plan includes two API keys" rather than "could not create that key".
Read it out of the `Cause` with `AsyncResult.error`, not off the result.

## Browser tests

`pnpm e2e` needs nothing set up: its own Postgres container on a free port, migrated with
the same runner `bun run dev` uses, both servers on 3100 and 5273.

Two properties keep it parallel and deterministic:

- **Every test signs up its own user**, so none truncates a table and none shares a tenant.
- **Every test presents its own `x-forwarded-for`**, because the credential endpoints are
  rate-limited per caller and a parallel suite from one address exhausts the bucket.

Never sleep. `interactUntil` retries the action against the condition it was meant to
cause — a click on a server-rendered button before React attaches _succeeds_ and does
nothing, and the next assertion is what fails fifteen seconds later.

Three refusals an integration hits first, all worth knowing before debugging one:
`415` for no `Content-Type`, `403 MISSING_OR_NULL_ORIGIN` for no `Origin`, and a hydration
race that looks like a broken feature.

## Where to look

- `apps/web/src/components/contact/contact-form.tsx` — the worked form
- `apps/web/src/lib/form/result.ts` — the two sentences
- `e2e/fixtures.ts` — `signedIn`, `interactUntil`, `completeOnboarding`
- `repos/effect-form/packages/form*/src/` — the only reference; there are no published docs
  for the v4 API
