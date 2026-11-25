---
name: save-your-2fa-recovery-codes
domain: accounts
locale: [generic]
interface: mixed
difficulty: basic
est_time: 15min
risk: medium
prerequisites: []
status: draft
last_verified: 2026-07-21
---

## Goal

Generate and store two-factor authentication recovery codes so a lost phone or broken authenticator does not lock you out.

## Preconditions

- You can sign in to the account and pass current two-factor authentication.
- You have a password manager, encrypted storage, printed emergency folder, or other protected offline place.
- You are on the official account security page.
- You are not sharing your screen with anyone who should not see the codes.

## Steps

1. **Open security settings.** Go to account settings, security, two-step verification, or two-factor authentication. → *Expect:* the page lists current two-factor methods.
2. **Find recovery codes.** Select backup codes, recovery codes, emergency codes, or generate codes. → *Expect:* the service warns that each code works once.
3. **Reauthenticate if prompted.** Enter your password, passkey, authenticator code, or hardware key touch. → *Expect:* the recovery-code generation screen opens.
4. **Generate a fresh set.** Create new codes if none exist or if you are unsure who has seen the old set. ⚠️ *Irreversible:* generating new codes often invalidates old codes, so confirm you can save the new set now. → *Expect:* a full set of codes appears with a date or download option.
5. **Count the codes.** Note how many codes were issued and whether they are one-time use. → *Expect:* your storage note can later show how many remain.
6. **Save to a password manager.** Put the codes in the account's password-manager item or a secure note labeled with the service name and date. → *Expect:* the saved item is encrypted and searchable by account name.
7. **Create an offline backup.** Print or handwrite the codes and place them in a locked drawer, safe, or sealed emergency folder. → *Expect:* you have one copy that does not depend on your phone, laptop, or cloud account.
8. **Avoid unsafe storage.** Do not leave screenshots in camera roll, downloads, chat messages, or plain email. → *Expect:* temporary files containing the codes are deleted.
9. **Test one code if the service allows.** Sign in from a private window and use a single recovery code, then mark that code used. → *Expect:* the login succeeds and one code is crossed out or deleted.
10. **Regenerate after a test if needed.** If the service provides few codes or the test consumed one you want back, generate a new full set and replace all copies. → *Expect:* only the latest set remains in storage.
11. **Label the storage clearly.** Include service name, username, date generated, and "one-time codes" without adding the account password to the same paper sheet. → *Expect:* you can identify the right codes under stress.
12. **Schedule a review.** Add a reminder to check recovery methods after phone replacement, job change, or moving password managers. → *Expect:* the codes will not sit forgotten after major changes.

## Decision points

- You use a password manager with emergency access → store codes there and also keep one offline copy.
- You live with people who can access papers → use a sealed envelope in a locked container.
- The service shows existing unused codes → regenerate if anyone may have seen them.
- The account is high value → add a second factor such as a hardware key, not only recovery codes.

## Failure modes & recovery

- **F1 Codes not downloadable:** detect no download or print button, recover by copying carefully into a secure note and checking every character.
- **F2 Codes exposed:** detect a screenshot, email, or shared document containing codes, recover by regenerating immediately and deleting the exposed copy.
- **F3 Test code fails:** detect invalid-code errors, recover by checking spacing and choosing a different unused code, then regenerate if uncertain.
- **F4 Wrong account label:** detect codes saved under a similar service name, recover by adding username and date to the stored note.
- **F5 Offline copy lost:** detect the envelope or printout missing, recover by generating a new set and replacing both storage locations.

## Verification

You can retrieve the current recovery-code set from one encrypted location and one offline location, and at least one tested sign-in or visible settings page confirms the codes are valid.

## Variations

- Hardware-key accounts: recovery codes are still useful if both primary and spare keys are unavailable.
- Shared family account: store codes where authorized people can reach them during an emergency.
- Enterprise account: policy may disable recovery codes and require help-desk reset instead.
- Passwordless account: recovery codes may be the only fallback that does not need the original device.

## Safety & privacy

Recovery codes are effectively spare keys. Treat them like passwords, never send them to support chat, and regenerate them if they appear in screenshots, email, shared notes, or printed pages you no longer control.
