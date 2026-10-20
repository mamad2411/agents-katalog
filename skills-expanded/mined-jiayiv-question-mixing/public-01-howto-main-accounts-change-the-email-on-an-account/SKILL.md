---
name: change-the-email-on-an-account
domain: accounts
locale: [generic]
interface: web
difficulty: basic
est_time: 20min
risk: medium
prerequisites: []
status: draft
last_verified: 2026-07-21
---

## Goal

Change the primary email address on an online account without losing access or leaving the old address as a recovery path.

## Preconditions

- You can sign in to the account now.
- You can receive mail at the new email address.
- You can still receive mail at the old email address until the change is complete.
- Two-factor authentication or recovery codes are available in case the change triggers reauthentication.

## Steps

1. **Sign in from a trusted device.** Use the official website or app and avoid public computers for the change. → *Expect:* the account dashboard opens normally.
2. **Open account identity settings.** Go to profile, account, login, or email settings. → *Expect:* the current email address is visible.
3. **Check recovery methods first.** Confirm a recovery phone, recovery email, passkey, or recovery codes are active. → *Expect:* you have a way back in if email verification stalls.
4. **Add the new email.** Enter the new address carefully, checking spelling and domain. → *Expect:* the service sends a verification message to the new address.
5. **Verify the new address.** Open the new inbox directly, not from a forwarded message, and click or enter the verification code. → *Expect:* the service marks the new email as verified.
6. **Handle old-email confirmation.** If the service asks the old address to approve the change, open that inbox and confirm only the change you started. → *Expect:* the old inbox message names the same account and new address.
7. **Make the new email primary.** Select make primary, use for login, or preferred email. → *Expect:* the account shows the new email as primary.
8. **Update recovery addresses.** Remove the old email from recovery if you no longer control it, and add a separate recovery email if possible. → *Expect:* recovery settings no longer point only to the old address.
9. **Check notification settings.** Make sure security alerts, receipts, and password reset emails go to the new address. → *Expect:* notification preferences show the new email.
10. **Sign out and test.** Sign out, then sign in using the new email and current password or passkey. → *Expect:* login succeeds with the new email.
11. **Confirm old email behavior.** Try the old email only if the service supports username checks, or inspect settings for aliases. → *Expect:* the old email is absent or listed only as a non-login alias you intentionally kept.
12. **Save proof of the change.** Keep the confirmation message or account activity entry until the next successful billing cycle or important transaction. → *Expect:* you have a dated record of the email update.

## Decision points

- The old inbox is compromised → change the account password and revoke sessions before adding the new email.
- The service allows aliases → keep the old email only if you still control it and want it for mail delivery.
- The account is work-managed → ask the administrator before changing login identity.
- The change affects billing or taxes → download recent statements before making the update.

## Failure modes & recovery

- **F1 Verification email missing:** detect no message after five minutes, recover by checking spam, search from the sender, and resend once.
- **F2 Typo in new address:** detect the verification message never arrives or the address is wrong in settings, recover by canceling and adding the correct address.
- **F3 Lockout after change:** detect rejected sign-in with both old and new email, recover with recovery codes or the account recovery flow.
- **F4 Old email still primary:** detect notifications still arriving at the old inbox, recover by changing the primary or notification address separately.
- **F5 Suspicious confirmation:** detect a change email you did not initiate, recover by canceling through the official site and changing the password.

## Verification

After signing out, you can sign in with the new email, receive a security alert there, and see the old email removed from login and recovery unless intentionally kept as an alias.

## Variations

- Banking account: the email change may require phone verification or a waiting period.
- Social account: public contact email and login email may be separate settings.
- Email provider account: changing the primary address may mean adding an alias instead of replacing the mailbox.
- Mobile app: some services require using the web settings page for email changes.

## Safety & privacy

Email controls password resets, receipts, and account alerts. Do not change it from a device you do not trust, and do not remove the old address until the new address has been verified and tested.
