---
name: use-auth-providers
description: >
  HOW a person gets in — passwords, Google, an emailed link — and which of those the owner switches on
  himself without a line of code. Load it when the owner says "let people sign in with Google", "send
  a login link by email", "I forgot my password", or when a sign-in method is simply missing from the
  form. What you cannot see from the guest layer: the sign-in methods are decided by which KEYS exist
  in the environment of a service you do not own, so a missing button is almost never a bug in the
  code — and one method everybody assumes is there does not exist at all.
---

# use-auth-providers

> Informational, not binding. **Know a better way for the case in front of you — do it your way and
> say so.** You are trusted with the creative work on this project.

Who may see what once they are in is `use-roles`; where the session lives and what the four tables are
is `use-auth`. This is only about the door people knock on.

---

## 1. 🔒 A method appears when its keys appear — nothing is edited

The auth service builds its list of providers at startup from the environment:

| Method | Turns on when | Set by |
|---|---|---|
| email + password | always | the substrate |
| **Google** | `GOOGLE_CLIENT_ID` **and** `GOOGLE_CLIENT_SECRET` are both present | the owner, in the panel → Login methods |
| **a link by email** (Resend) | `RESEND_API_KEY` is present | the owner, in the panel |
| architect token | `ARCHITECT_TOKEN` is present | the installer |

**Both Google values or neither** — a half-filled pair is treated as absent, deliberately, so a
mistyped setting fails visibly at setup rather than at a stranger's first sign-in attempt.

So when the owner says "there is no Google button": the answer is a key in the panel, not a change in
this project. Say that plainly instead of building a button that leads nowhere.

## 2. 🔒 There is no password recovery. Say it out loud

A person who forgets their password cannot get back in without the owner. There is no "forgot
password" route, and inventing one here is wrong twice: the flow belongs to the auth service, which is
not yours, and a half-built reset is worse than none.

When it comes up — and it will — hand it over as a platform request (`use-data` §5) and, meanwhile,
tell the owner the only path that exists today: he changes the account himself.

**Do not build a form that promises a reset email.** A promise the product cannot keep is the one bug
users report loudly.

## 3. The engine underneath is bigger than what is wired

NextAuth sits under the service, with dozens of providers upstream. Wiring another one is work in the
auth service — a platform change, requested through the owner. Nothing about it happens in this
repository, and a package installed here does not add a sign-in method.

## 4. What the guest layer may do

- **Send people to the auth service's own pages.** The sign-in surface belongs there; it is already
  translated into 82 languages and already knows which providers exist today.
- **Read the session, never issue one.** `getSession()` server-side; `/api/me` from an island. Do not
  copy the session cookie, do not parse the token, do not cache the answer beyond the request.
- **Never ask for a password in a page of this app.** Not on a form, not "just for testing". The only
  place a password is typed is the auth service's own screen.

## 5. Two facts that make a working site look broken

- **On `localhost` the owner at the keyboard is the architect without signing in**, and on the
  temporary address the panel is read-only to anyone with the link while sign-in and registration are
  closed. A screen "verified" on either is verified for the case that never fails — check on the own
  domain before saying a gate works (`use-roles`).
- **Registration on the own domain is open to everyone, and the first account is the architect for
  good.** Its password has no recovery (§2), so the person creates it on this computer before the
  domain is connected.
- **The session cookie belongs to the whole domain.** It is sent to every subdomain of the site,
  which is why the platform's own services check a role rather than trusting the cookie's presence
  (`use-data` §2). Nothing for you to configure — but if you ever wonder why a request "already
  authenticated" is refused, this is the shape of the answer.

## 6. Guest access exists in the substrate and is NOT described

There is a guest door (`/api/auth/guest`) and a guest tier in the roles. What a guest may do, how long
the session lives and what he loses on a real sign-in **is not written down anywhere and has never
been walked through live** (`CLAUDE.md`, the gap list).

So: do not build a product flow on guest access and do not tell the owner it works. Naming that
honestly is the correct answer today.

## 7. Before you call it done

1. A missing sign-in method was diagnosed as a missing KEY, and the owner was told which panel screen.
2. No password field, no reset promise and no session-issuing code was added to this app.
3. Whatever you checked, you checked on the own domain — not on `localhost`, where the owner passes everything.
