---
name: reset-2fa-when-you-lose-your-phone
domain: accounts
locale: [generic]
interface: mixed
difficulty: intermediate
est_time: 30min
risk: high
prerequisites: []
status: draft
last_verified: 2026-07-21
---

## Goal

Regain access to an account after losing the phone that held your two-factor authentication method.

## Preconditions

- You know the account username, email address, or phone number.
- You can access at least one trusted email inbox, backup device, printed recovery code, or official identity recovery flow.
- You are using the service's official website or app, reached from a saved bookmark or typed address.
- If the phone may be stolen, you have already locked the device remotely if that option exists.

## Steps

1. **Stop automatic retries.** Do not keep guessing codes or passwords after two failed attempts, because some services lock recovery for a cooling-off period. → *Expect:* you are still on a normal sign-in or recovery screen, not a lockout message.
2. **Open the official recovery path.** Use the service's sign-in page, choose lost device, try another way, or account recovery. → *Expect:* the page offers recovery codes, backup device, email, phone, or identity verification options.
3. **Try recovery codes first.** Find the saved one-time recovery codes in your password manager, printed emergency sheet, or offline vault. → *Expect:* you have an unused code that matches the service name.
4. **Submit one recovery code.** Paste or type a single unused code and mark it used in your storage only after it works. → *Expect:* the account accepts the code and lets you continue to security settings.
5. **Use a backup device if no code works.** [BRANCH: authenticator synced to another device | hardware security key | trusted signed-in session] approve the sign-in from that device. → *Expect:* the service confirms your identity without the lost phone.
6. **Use account recovery if backups fail.** Start the official recovery flow and provide only requested facts such as previous password, recovery email, billing details, or ID. → *Expect:* you receive a case number, email, or waiting-period notice from the service.
7. **Wait through enforced delays.** Leave recovery messages in place and do not restart the flow unless the service tells you to. → *Expect:* the next message references the same account and same recovery request.
8. **Enter security settings immediately after access returns.** Go to two-factor authentication or sign-in methods. → *Expect:* the lost phone is listed as a factor, device, authenticator app, or push method.
9. **Remove the lost factor.** Delete the old authenticator, push device, or phone prompt after adding a working replacement. ⚠️ *Irreversible:* removing the only working factor can lock you out, so confirm the replacement signs in first. → *Expect:* the old phone no longer appears as an approved sign-in method.
10. **Add at least two new factors.** Enroll a passkey or hardware key plus an authenticator app or recovery phone. → *Expect:* the account shows more than one active recovery or two-factor method.
11. **Regenerate recovery codes.** Create a fresh set because any code you found may have been exposed during the emergency. → *Expect:* a new dated set of codes is displayed or downloaded.
12. **Store the new codes safely.** Save them in an encrypted password manager note and one offline place such as a printed sheet in a locked drawer. → *Expect:* you can retrieve the codes without using the lost phone.
13. **Review active sessions.** Sign out unknown sessions and revoke app passwords or OAuth grants you do not recognize. → *Expect:* only current devices and expected connected apps remain.

## Decision points

- You still have a laptop signed in → use that session to add a new factor before signing out anywhere.
- The service offers SMS only → use it temporarily, then add an authenticator, passkey, or hardware key if available.
- The lost phone may be stolen → change the account password after recovery and remove remembered devices.
- The recovery email is also inaccessible → recover that email account first or use the service's identity review path.

## Failure modes & recovery

- **F1 Recovery code rejected:** detect repeated invalid-code errors, recover by checking for spaces, using another unused code, then switching to backup device recovery.
- **F2 Recovery loop:** detect the same form returning without a case number, recover by clearing browser extensions, trying a private window, and using the official help center link.
- **F3 Lockout timer:** detect a message with a wait time or date, recover by waiting and not creating duplicate attempts.
- **F4 Stolen device still trusted:** detect the lost phone listed under devices, recover by removing it and revoking sessions after a new factor is active.
- **F5 Fake recovery site:** detect misspelled domains, ads, or requests for full recovery-code lists, recover by closing the page and navigating from a known bookmark.

## Verification

You can sign out, sign back in on a separate device, satisfy two-factor authentication without the lost phone, and see fresh recovery codes stored in two safe places.

## Variations

- Enterprise account: the help desk may need to reset factors, and you should record the ticket number.
- Hardware-key account: keep a spare key enrolled and stored away from the daily key.
- Phone-number factor: replacing a SIM may restore SMS codes, but it does not restore authenticator app secrets.
- Passwordless account: recovery may require a passkey on another device or a printed recovery code.

## Safety & privacy

This is high risk because a mistake can lock you out and a fake recovery flow can steal the account. Never give anyone a full recovery-code list, never approve a sign-in you did not start, and use only official recovery pages.
