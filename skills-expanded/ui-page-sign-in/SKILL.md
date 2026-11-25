---
name: ui-page-sign-in
description: "How to build sign-in and the steps around it (sign-up link, password reset, two-factor): one centred column with no app shell, email and password or email first, SSO buttons with official marks, passkeys and magic links, autocomplete that password managers use, errors that reveal no accounts, loading, rate limit and lockout messages, and the phone layout. Read before building or reworking a sign-in, sign-up or password reset page."
---

# Sign-in

The generated sign-in page is a split screen: a gradient and a testimonial
on one side, a card saying "Welcome back!" on the other that drops below
the fold on a phone, fields labelled only by placeholders so password
managers skip them, "No account with that email" (telling anyone which
addresses have accounts), social buttons in made-up colours, and a button
that can be pressed twice. People come here to get in, quickly and safely,
with the password manager or passkey they already use. This skill gives
the page that lets them.

One kind of page. The measures are in `ui-layout`; field anatomy in
`ui-part-forms`, field behaviour in `frontend-forms`; the server side
(sessions, password hashing, reset tokens, rate limits) in `backend-auth`
and `backend-security`.

## 1. The layout

```
┌──────────────────────────────────────────────────┐
│                    ◉ Product                     │
│               Sign in to Product                 │
│                                                  │
│       [ G   Continue with Google           ]     │
│       [ ◎   Continue with GitHub           ]     │
│       ───────────────  or  ───────────────       │
│       Email                                      │
│       [                                    ]     │
│       Password                                   │
│       [                             ] (Show)     │
│       Forgot password?                           │
│       [              Sign in               ]     │
│       Sign in with a passkey                     │
│                                                  │
│       New to Product? Create an account          │
│               Terms · Privacy · Help             │
└──────────────────────────────────────────────────┘
```

- A single centred column 360 to 400px wide (420 at most), with no app
  shell, navigation or sticky header. The only place where a centred card
  on an empty page is the right layout.
- In the column: the product name or logo (linking to the site), the
  title as the `h1` (24 to 28px, "Sign in to [Product]"), the SSO buttons
  and the form, then the sign-up link, then a small footer (Terms,
  Privacy, Help or a status page).
- The column starts about 10 to 15% down the screen rather than centred
  vertically, so it does not jump when an error appears.
- A card border on wide screens only when the background needs it. A side
  panel (a real screenshot, one line on the product) only on wide screens,
  beside the form; on a phone it is gone, and never above the form.

## 2. Choose the flow

| Flow | When | How |
|---|---|---|
| Email and password together | Most products | Both fields in the HTML from the start: password managers fill them best |
| Email first, then the method | Several methods per account, company SSO found by domain | Ask the email, then show the password, passkey, SSO or "check your email" step |
| SSO only | Teams that all use Google Workspace, Microsoft or GitHub | The buttons alone, no form |
| No password | People who forget passwords; high security | Passkeys in the autofill, an email link or code as the fallback |

- Offer only the methods the backend has.
- Email first: the second step keeps a username field
  (`autocomplete="username"`, read-only, showing the address) so password
  managers save the pair, and an unknown address gets the same next step as
  a known one.

## 3. The form

```html
<form method="post" action="/sign-in">
  <label for="email">Email</label>
  <input id="email" name="email" type="email" required
         autocomplete="username webauthn" autocapitalize="none" spellcheck="false">
  <label for="password">Password</label>
  <input id="password" name="password" type="password" required
         autocomplete="current-password">
  <button type="button" aria-controls="password" aria-pressed="false">Show password</button>
  <a href="/forgot-password">Forgot password?</a>
  <button type="submit">Sign in</button>
</form>
```

- Visible labels; no placeholder standing in for one.
- `autocomplete="username"` on the identifier even when it is an email,
  with `webauthn` added last when passkeys are offered;
  `current-password` here, `new-password` on sign-up and reset,
  `one-time-code` on codes. Never `autocomplete="off"`; an `id` and a
  `name` on every field.
- Paste allowed; no length limit under 64; a show toggle instead of a
  second password field.
- The forgot link directly under the password field, so it is found when
  it is needed and the tab order matches what is seen.
- Autofocus the email field when the form is the main way in.
- `method="post"`: credentials never in a URL; the framework's CSRF
  protection (`backend-auth`).
- No third-party scripts on this page (tag managers, chat, session replay,
  heat maps): any script on the page can read what is typed. A strict
  Content Security Policy (`backend-security`).

## 4. SSO buttons

- Only the providers that are configured, in the order the audience uses
  them: GitHub first for developers; Google, then Apple, for the public;
  Microsoft for companies on Microsoft 365.
- Each with the provider's official mark and wording from its brand
  guidelines ("Continue with Google", "Sign in with Apple"), full width of
  the column, equal size, 44px tall or more. Marks are never recoloured;
  Google's button in its light or dark version to match the theme
  (`ui-themes`).
- Above the form with an "or" divider when most people use them; below it
  when most use email.
- "Sign in with SSO" for company SAML or OpenID Connect: it asks for the
  work email and sends the person to their company's provider. A failed or
  cancelled provider sign-in returns here with a plain message.

## 5. Passkeys, magic links and codes

- Passkeys: with `webauthn` in the identifier's `autocomplete`, the browser
  offers saved passkeys in the autofill (conditional mediation:
  `navigator.credentials.get({ mediation: "conditional", publicKey })`,
  started on load once `PublicKeyCredential.isConditionalMediationAvailable()`
  resolves true), plus a visible "Sign in with a passkey" button. Use the
  auth library's passkey support or SimpleWebAuthn
  (`@simplewebauthn/browser` and `@simplewebauthn/server`), never
  hand-written verification. After a password sign-in, offer to add a
  passkey once, dismissibly.
- Magic link: "Email me a sign-in link", then a page naming the address,
  the sender and subject to look for, Resend after 30 to 60 seconds, and
  "Use a different email". The link is short-lived (15 minutes is common)
  and works once; opened on another device, offer a code instead.
- Codes by email or SMS: one field (`autocomplete="one-time-code"
  inputmode="numeric" maxlength="6"`) that accepts a paste and submits on
  the sixth digit or Enter. Six separate boxes break pasting and screen
  readers; if a design insists, paste fills all six and Backspace moves
  back.

## 6. Errors, limits and lockout

- A wrong email or password gets one message for both: "Email or password
  is incorrect." Above the form with `role="alert"`, the email kept, focus
  on the password field. Unknown email and wrong password answer the same
  way, in the same time (`backend-auth`).
- Format errors (an empty field, not an email) under the field.
- Too many attempts: "Too many attempts. Try again in 5 minutes, or reset
  your password.", the wait taken from the server's `Retry-After`, and the
  same message whether or not the account exists. A challenge (Cloudflare
  Turnstile) only after repeated failures, never a puzzle first.
- A locked account: the details go to the account's email, not to whoever
  is typing; the page says what to do next.
- Network or server failure: "We could not reach the server. Check your
  connection and try again.", with everything typed kept.
- An unverified email, only after the password was right: "Confirm your
  email first. We sent a new link to [address]."

## 7. Submitting, and the steps after

- On submit the button shows a spinner and "Signing in…", keeps its width,
  sets `aria-busy="true"` and ignores further presses.
- Remember me only when it changes how long the session lasts, saying so
  ("Keep me signed in for 30 days"), unticked by default.
- Two-factor: its own screen after the password ("Enter the 6-digit code
  from your authenticator app"), the code field from section 5, links to
  "Use a recovery code" and "Use a passkey or security key", and "Trust
  this device for 30 days" only when the backend supports it.
- Afterwards: back to where the person was going, from a `returnTo` that
  the server checks is a path on this site (never any URL from the query);
  someone already signed in skips this page.
- The sign-up link under the form ("New to [Product]? Create an account");
  an invite-only product says so and how to get in.
- Forgot password: the email field and "Send reset link", then "If an
  account exists for [email], we sent a link. It expires in 60 minutes."
  whether or not one exists. The reset page asks for the new password
  (`new-password`, the rule in words, a show toggle); every other session
  ends (`backend-auth`).

## 8. On a phone

- The column is the page: 16 to 24px side padding, fields and buttons full
  width and 48px tall, input text 16px or more (iOS Safari zooms into
  smaller text).
- The first field and the SSO buttons in the first screen, with no panel,
  hero or banner over them (the system's password and passkey sheets need
  the fields visible). The logo small, 32 to 40px.
- The right keyboards (`type="email"`, `inputmode="numeric"` for codes),
  `enterkeyhint="next"` on the email and `"go"` on the password.

## 9. Accessibility

- One `h1`; labels on every field; errors tied to their fields, and the
  form's error announced.
- Accessible Authentication (WCAG 2.2): no puzzle, no retyping from an
  image, without another way through; paste and password managers work;
  passkeys and email links count as that other way.
- The tab order follows the page: SSO, email, password, show, forgot, Sign
  in, sign-up. A visible focus ring on every control, the SSO buttons too.
- The document title says the state: "Sign in · [Product]", and "Error:
  Sign in · [Product]" after a failed attempt.

## 10. Search engines

The sign-in page may be indexed (people search "[product] login"), with the
title "Sign in · [Product]" and no marketing content. The reset, two-factor
and "check your email" pages are `noindex`.

## Check it

- Sign in with a password manager (the browser's own, 1Password or
  Bitwarden): it offers to save, and fills both fields next time. With a
  passkey saved, focusing the email field offers it.
- A wrong password and an unknown email: the same message, the same
  status, about the same time (`curl -w '%{time_total}'`).
- Fail until the limit: the message gives the wait. Double-click Sign in:
  one request.
- Keyboard only through the buttons, fields and links; a screen reader
  reads the labels and the error.
- `preview` at 360px: the form in the first screen, nothing overflowing,
  touch targets; `preview` with `login` signs in through this form to see
  the screens behind it, which standard fields make possible. `ui_check`.

## Avoid

A split screen whose panel pushes the form down on a phone; "Welcome back!"
as the title; placeholders as labels; `autocomplete="off"`; "No account
with that email"; SSO buttons in invented colours or with redrawn marks;
buttons for providers that are not set up; a "Remember me" that changes
nothing; a CAPTCHA before the first attempt; six boxes that break paste;
analytics and chat scripts on the page; credentials in the URL; a
`returnTo` that sends people to any site; lockouts anyone can trigger by
typing someone's email.
