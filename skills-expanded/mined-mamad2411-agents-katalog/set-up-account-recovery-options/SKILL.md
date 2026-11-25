---
name: set-up-account-recovery-options
domain: accounts
locale: [generic]
interface: web
difficulty: intermediate
est_time: 30min-1h
risk: medium
prerequisites: [accounts/log-in, accounts/enable-two-factor-authentication]
status: draft
last_verified: 2026-07-20
---

## Goal

Your important account has a working recovery email, a recovery phone, and backup codes stored safely, and you have proven at least one recovery path actually works, so a lost password or lost phone does not lock you out permanently.

## Preconditions

- Access to the account right now (this only works while you are logged in).
- A second email address you control, ideally on a different provider than the account itself.
- A phone number that is yours long-term, and a place to store codes offline (password manager or paper).

## Steps

1. **Open the account's security or recovery settings.** Usually under Security, Sign-in, or Recovery. → *Expect:* fields for recovery email, phone, and backup/recovery codes are visible.
2. **Set a recovery email on a different provider.** If the account is a Gmail account, do not use another Gmail as recovery; one provider outage or breach should not take both. → *Expect:* the recovery email shows "verify" and a verification message arrives at that inbox.
3. **Verify the recovery email.** Open the message, click or enter the code. → *Expect:* the setting flips to "verified", not "pending".
4. **Add a recovery phone number and verify the SMS code.** Prefer a number that will not change soon. → *Expect:* phone shows verified; a test code was received.
5. **Generate backup/recovery codes and save them offline.** These are the fallback when both phone and email fail. ⚠️ *Irreversible:* generating a new set invalidates any old printed codes, so replace your stored copy every time. → *Expect:* a list of one-time codes displayed; you have copied all of them.
6. **Store the codes where you can reach them without the account.** Password manager entry, or printed and kept with important documents. Do not store them only inside the same account they unlock. → *Expect:* codes saved in at least one out-of-account location.
7. **Record recovery contacts in your password manager entry for this account.** → *Expect:* the entry notes which email and phone recover it.
8. **Test one recovery path now, while you still have full access.** Log out, choose "forgot password" or "try another way", and confirm a code reaches your recovery email or phone, then log back in. → *Expect:* the recovery challenge delivers a working code and you regain access.
9. **Set a reminder to re-check yearly.** Numbers and backup emails go stale. → *Expect:* a recurring calendar reminder exists.

## Decision points

- Only one email and no spare → create a dedicated recovery mailbox first; do not skip this, single-point-of-failure is the whole risk.
- High-value account (primary email, bank, password manager) → prefer an authenticator app or hardware key over SMS, since SMS is vulnerable to SIM-swap.
- Shared or work-issued account → recovery may be controlled by an admin; confirm who holds the reset before assuming you can self-recover.

## Failure modes & recovery

- **F1 Verification code never arrives:** detect no message after a few minutes → check spam, confirm the address/number has no typo, and resend; try the other channel.
- **F2 Recovery loop (recovery email itself needs recovery):** detect each account points at the other → break the circle by giving each a distinct, independently recoverable contact.
- **F3 Lost phone after relying only on SMS:** detect you cannot receive codes → use stored backup codes; this is exactly why step 5 exists.
- **F4 Backup codes stored inside the locked account:** detect you cannot open them without logging in → in future store them offline; for now recover via phone/email path.

## Verification

Recovery email and phone both show "verified", a current set of backup codes sits in an out-of-account location, and a live test of at least one recovery path returned a working code and let you back in.

## Variations

- `us`: carriers offer a SIM-swap lock (number-transfer PIN); enable it to harden SMS recovery.
- Authenticator-app accounts: "backup codes" replace SMS entirely; treat them as the primary fallback and store two copies.

## Safety & privacy

Medium risk because recovery options are exactly what an attacker targets to hijack an account. Never add a recovery email or phone you do not fully control, review these settings after any breach notice, and keep backup codes as protected as the password itself.
