---
name: set-up-a-password-manager
domain: accounts
locale: [generic]
interface: mixed
difficulty: intermediate
est_time: 2h
risk: medium
prerequisites: [have-email-address]
status: draft
last_verified: 2026-07-20
---

## Goal

A password manager installed, protected by one strong memorized passphrase, seeded with your important accounts, and wired into your browsers and phone — retiring the reused-password habit that underlies most personal account takeovers.

## Preconditions

- A chosen manager: a reputable dedicated app (Bitwarden/1Password-class) or your platform's built-in (Apple/Google password systems); the honest advice is that *any* of these beats no manager by a mile, and the dedicated ones travel across ecosystems better.
- One uninterrupted evening for setup and the tier-1 seeding; total migration happens over weeks, by design.

## Steps

1. **Create the vault with a master passphrase you can actually memorize.** Four to five random common words (the dice-and-wordlist method or your manager's generator), typed a few times until fluent. This is now one of the two secrets you memorize forever (the other unlocks your phone); it is never reused anywhere else. → *Expect:* a passphrase you can type from memory, unlike anything you've used before.
2. **Immediately store the emergency kit.** The manager's recovery/secret key and recovery codes printed or written, stored where you keep passports (`accounts/enable-two-factor-authentication` step 5's insurance logic: losing both the passphrase and this kit can mean losing the vault, which is the design). → *Expect:* a physical recovery artifact in a safe place, tested readable.
3. **Protect the vault account itself with 2FA.** The manager's own account gets your strongest second factor. → *Expect:* the vault behind passphrase + factor; the keys to the kingdom guarded like it.
4. **Install everywhere you type passwords.** Browser extension(s), phone app, and enable it as the phone's autofill provider (settings → passwords/autofill); disable the old browser's built-in saving to end the two-systems confusion. → *Expect:* one autofill system answering everywhere; test on any login (`accounts/log-in` step 3's autofill-as-phishing-detector now works for you).
5. **Seed tier-1 accounts tonight, by logging in and updating.** Email first (the master key: `accounts/review-account-security` step 1's ordering), then banking, then the manager's list of your most-used: for each, log in, generate a new unique password in the manager, save. Eight to twelve accounts is a complete first night. → *Expect:* tier-1 all on generated-unique passwords stored in the vault.
6. **Migrate the long tail opportunistically, and let the audit nag.** Every login over the coming weeks: save-on-use, upgrade-on-touch; run the manager's built-in audit (reused/breached/weak lists) monthly until it quiets (`accounts/review-account-security` step 6 now automated). → *Expect:* the vault growing to match your real account surface; the audit's red numbers shrinking weekly.

## Decision points

- Family setup: family plans give each person their own vault plus a shared collection (wifi, streaming, utilities `housing/set-up-utilities` logins); the shared vault is also the practical answer to household continuity.
- Emergency access: configure the manager's emergency-contact/legacy feature or put the emergency kit's location in your real-world affairs notes — accounts outlive their owners' incapacity, and this feature is the humane answer.
- The "what if the manager is breached" worry, answered honestly: reputable managers encrypt client-side (breaches yield sealed vaults), and the alternative — human-memorable reuse — is breached *continuously* via every site leak; the audit trail favors the vault by orders of magnitude.

## Failure modes & recovery

- **F1 Forgot the master passphrase in week one:** the emergency kit (step 2) exists for exactly this; recover, then re-drill the passphrase daily for a week — fluency comes from typing, not intending.
- **F2 Autofill fights between old browser storage and the manager:** finish disabling the built-ins and import-then-delete their stored passwords (managers import these in one step); two systems half-on is the worst configuration.
- **F3 A site rejects generated passwords (length/symbol rules):** adjust the generator's settings per-site; the rare site that caps at 12 characters gets 12 random ones, which still beats the recycled classic.
- **F4 Locked out on a new device at a bad moment:** the phone app's offline cache is the backup plan; keep the app installed and synced on two devices minimum.

## Verification

The master passphrase types from memory, the emergency kit physically exists, the vault has 2FA, one autofill system answers on desktop and phone, tier-1 runs on unique generated passwords, and the monthly audit trend points at zero reused.

## Variations

- Passkey era: managers now store passkeys alongside passwords — enroll passkeys where offered (`accounts/enable-two-factor-authentication`'s preference) and the vault becomes the bridge across devices.
- High-risk profiles (public figures, crypto holders): hardware-key 2FA on the vault, separate email for the vault account, and a longer passphrase; the architecture holds, the parameters harden.

## Safety & privacy

Medium risk in setup, massively risk-negative in operation. The two absolutes: the master passphrase exists nowhere digital except your head, and the emergency kit exists nowhere digital at all. The vault is the single most leveraged hour in this corpus's entire digital track.
