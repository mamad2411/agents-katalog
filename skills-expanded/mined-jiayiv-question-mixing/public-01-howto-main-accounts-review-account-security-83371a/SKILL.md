---
name: review-account-security
domain: accounts
locale: [generic]
interface: web
difficulty: intermediate
est_time: 1h
risk: medium
prerequisites: [accounts/log-in, accounts/enable-two-factor-authentication]
status: draft
last_verified: 2026-07-20
---

## Goal

An annual (or post-incident) sweep of your important accounts: sessions, factors, recovery paths, connected apps, and passwords are verified current and yours — the hygiene that makes account takeover boring to attempt.

## Preconditions

- A list of your tier-1 accounts: email (the master key — it resets everything else), banking, cloud storage, password manager, main social/shopping. Five to eight accounts; this recipe runs per account.
- Your password manager open; an hour blocked.

## Steps

1. **Start with the email account — it outranks everything.** Whoever holds your email holds your password resets; it gets the fullest version of every step below. → *Expect:* the sweep order acknowledges email as the root of the tree.
2. **Review active sessions/devices and evict strangers.** Security settings → "your devices" / "where you're logged in": recognize each entry (device, location, last active). Unknown or stale → sign it out; anything *suspicious* (a country you've never been) → sign out all + change the password now. → *Expect:* the session list reads as a biography of your actual devices.
3. **Audit sign-in methods and factors.** 2FA still on, and on the strongest available method (`accounts/enable-two-factor-authentication`)? Phone number current? Passkeys offered — enroll. Old factors (a previous phone, SMS-when-you-have-app) removed. → *Expect:* factors current, minimal, and strongest-available.
4. **Verify recovery paths — the forgotten backdoor.** Recovery email and phone: still yours, still active? (A recycled old number is an open door.) Recovery codes: located, and re-generated if you can't find them. Security questions (legacy accounts): answers rotated to non-guessable strings stored in the manager. → *Expect:* every recovery channel points at something you currently control.
5. **Prune third-party access.** "Connected apps"/"apps with account access": that quiz from 2019, the service you stopped using — revoke by default; keep only what you recognize *and* still use. Same for OAuth "sign in with" grants. → *Expect:* the connected-apps list is short and current.
6. **Handle the password itself on evidence, not ritual.** Check the account against breach-notification services (haveibeenpwned-class, or the manager's built-in audit): breached or reused → change it now to a generated unique one; strong-unique-unbreached → leave it (forced rotation without cause breeds weak patterns). → *Expect:* no reused or breached passwords among tier-1 accounts.
7. **Log the sweep and calendar the next.** A one-line note per account ("2026-07: sessions clean, passkey added, 3 apps revoked") and a recurring annual reminder — plus triggers: run this after any breach news, lost device, or breakup involving shared devices. → *Expect:* the review is a system, not a mood.

## Decision points

- Account you no longer use surfaces during the sweep → don't secure it, delete it (`accounts/delete-an-account`) — the smallest attack surface is no account.
- Shared/family accounts (streaming, utilities) → factors and recovery must route to the *managing* adult's channels; sessions include the household's devices legitimately.
- Post-incident mode (you clicked something, a breach email arrived) → run steps 2, 3, 6 immediately for the affected account *and* the email account, in that order — don't wait for the annual slot.

## Failure modes & recovery

- **F1 Found an unknown active session:** sign out all sessions, change the password, re-check the recovery paths (attackers park their own email there to persist) — recovery-path tampering is the tell of a real compromise, and it's step 4 that catches it.
- **F2 Locked yourself out mid-hygiene (changed number, old 2FA app):** the recovery codes you verified in step 4 are the ladder; this is why codes precede factor changes.
- **F3 The sweep reveals dozens of reused passwords (old habits):** don't fix all tonight — tier-1 accounts now, then the manager's audit list at five per week; scope prevents abandonment.
- **F4 A connected app you revoked broke something:** re-connect deliberately — revoke-by-default with occasional re-grants is the correct error direction.

## Verification

For each tier-1 account: sessions recognized, strongest 2FA active, recovery paths verified yours, connected apps pruned, password unique and unbreached — and the log line + next-year reminder exist. The email account got all of it first.

## Variations

- Password-manager-native audits (watchtower-class dashboards) automate step 6 and parts of 3 — the sessions/recovery/apps steps remain manual and remain the point.
- Work accounts: your org's SSO does much of this centrally; your part is the personal-device sessions and not parking work recovery on personal channels (or vice versa).

## Safety & privacy

Medium risk, entirely protective: the hour spent here is the cheapest insurance in your digital life. The two lines that catch real attacks: strangers in sessions (F1) and tampered recovery paths (step 4).
