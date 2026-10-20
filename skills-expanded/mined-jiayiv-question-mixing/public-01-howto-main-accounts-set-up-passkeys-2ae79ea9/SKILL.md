---
name: set-up-passkeys
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

Add a passkey to an account so you can sign in with a device unlock method instead of typing a reusable password code.

## Preconditions

- You can currently sign in to the account.
- Your device has a screen lock, biometric unlock, PIN, or hardware security key.
- You know whether you want a synced passkey, such as one stored by an operating system or password manager, or a device-bound passkey.
- You have a fallback sign-in method before changing anything important.

## Steps

1. **Open the official account settings.** Sign in through the service's official website or app and go to security, sign-in, or passkeys. → *Expect:* a page lists current sign-in methods.
2. **Check the existing fallback.** Confirm a recovery email, recovery phone, authenticator app, or recovery codes are already usable. → *Expect:* at least one fallback method is active before you add the passkey.
3. **Choose passkey enrollment.** Select add passkey, create passkey, or security key. → *Expect:* the browser or app opens a system prompt for where to save the passkey.
4. **Pick the storage location.** [BRANCH: synced passkey | device-bound passkey | hardware security key] choose the option that matches your backup plan. → *Expect:* the prompt names the platform, password manager, device, or security key that will hold the passkey.
5. **Approve with device unlock.** Use face unlock, fingerprint, PIN, password, or touch the hardware key when prompted. → *Expect:* the service reports that the passkey was created.
6. **Name the passkey clearly.** Use a label such as work laptop July 2026 or YubiKey blue. → *Expect:* the passkey list shows a name you can recognize later.
7. **Record how it is backed up.** Note whether the passkey syncs through your account, lives only on one device, or sits on a physical key. → *Expect:* you know what would happen if this device were lost.
8. **Test in a private window.** Open a private browser window or another device and start sign-in with the passkey. → *Expect:* the service offers the new passkey and asks for the expected unlock method.
9. **Complete the test sign-in.** Use the passkey once, then return to the security settings. → *Expect:* the account signs in without an SMS or authenticator code.
10. **Add a second passkey if possible.** Enroll another phone, laptop, password manager, or hardware key. → *Expect:* the account has at least two passkeys or one passkey plus another strong fallback.
11. **Keep password and recovery sane.** If the account still has a password, keep it unique in a password manager and keep recovery codes current. → *Expect:* losing one device does not mean losing the account.
12. **Remove only obsolete methods.** Delete old passkeys or devices you no longer control. ⚠️ *Irreversible:* removing the only passkey or fallback can block access, so complete a fresh test sign-in first. → *Expect:* active methods match devices you control.

## Decision points

- You use one phone only → choose a synced passkey or add a printed recovery code before relying on passkeys.
- The service says passkey replaces password → confirm you understand the recovery path before completing enrollment.
- You share a computer → do not store the passkey in a shared OS profile.
- You need phishing resistance → prefer a passkey or hardware key over SMS codes.

## Failure modes & recovery

- **F1 Browser unsupported:** detect no passkey prompt or a gray button, recover by updating the browser or using the service's mobile app.
- **F2 Wrong storage choice:** detect a prompt naming the wrong password manager or profile, recover by canceling and restarting with the correct account selected.
- **F3 Test sign-in fails:** detect the passkey not appearing, recover by checking sync status, Bluetooth, nearby-device prompts, or enrolling a second method.
- **F4 Lost device risk:** detect that the only passkey is device-bound, recover by adding a synced passkey, second device, hardware key, or recovery codes.
- **F5 Shared passkey exposure:** detect the passkey saved in a family or work vault unintentionally, recover by deleting it and enrolling in the correct private vault.

## Verification

A new private-window sign-in succeeds using the passkey, and account security settings show at least one fallback method that does not depend on the same device.

## Variations

- Mobile app: passkey enrollment may appear under profile, security, or login methods.
- Hardware key: the browser may ask for a PIN and then a physical touch.
- Enterprise account: administrators may restrict syncing or require device-bound keys.
- Password-manager passkey: confirm the vault is encrypted and recoverable before trusting sync.

## Safety & privacy

Passkeys reduce phishing risk because the secret is not typed into websites, but recovery still matters. Protect the device unlock code, avoid shared profiles, and keep at least one recovery route that survives theft or hardware failure.
