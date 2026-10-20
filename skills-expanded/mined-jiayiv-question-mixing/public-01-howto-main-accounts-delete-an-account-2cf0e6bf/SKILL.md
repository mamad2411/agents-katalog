---
name: delete-an-account
domain: accounts
locale: [generic]
interface: web
difficulty: intermediate
est_time: 30min
risk: high
prerequisites: [accounts/log-in]
status: draft
last_verified: 2026-07-20
---

## Goal

An account you no longer want is permanently deleted (or confirmed scheduled for deletion), with your data exported first and nothing still depending on it.

## Preconditions

- You can log in to the account.
- You have checked what depends on this account: subscriptions billed to it, other services using it for SSO, data only it holds.

## Steps

1. **Inventory dependencies.** List active subscriptions, SSO uses ("Sign in with this account" elsewhere), and data to keep (photos, documents, purchase history). → *Expect:* a short written list; empty list → proceed directly.
2. **Export your data.** Use the service's export/takeout tool (Settings → Privacy/Data → Download your data). → *Expect:* an export archive downloaded and opened once to confirm it's readable.
3. **Detach dependencies.** Cancel subscriptions; switch SSO logins on other services to email+password; migrate anything pointing at this account's email. → *Expect:* the dependency list from step 1 is fully struck through.
4. **Find the deletion flow.** Settings → Account → "Delete account" / "Close account"; some services hide it behind help pages or require contacting support. → *Expect:* a deletion page stating what will be deleted and any grace period.
5. **Read the terms of deletion.** Note the grace period (often 14–30 days where logging in cancels deletion) and what is retained (invoices, legal records). → *Expect:* you can state the grace period and retention before confirming.
6. **Confirm deletion.** Re-enter the password / 2FA as demanded. ⚠️ *Irreversible:* after the grace period, data and the username are gone — this is the point of no return; confirm the export from step 2 is safe first. → *Expect:* on-screen and email confirmation that deletion is scheduled or complete.
7. **Do not log in during the grace period** (it usually cancels deletion). Optionally set a calendar note for the grace-period end. → *Expect:* after the period, login fails with "account not found" or equivalent.
8. **Clean up local traces.** Delete the password-manager entry (or mark deleted), remove the app from devices. → *Expect:* no active references to the account remain.

## Decision points

- Service offers "deactivate" vs "delete" → deactivation hides but keeps data; pick per your goal — this recipe's goal is deletion.
- Account holds money or credit (wallet balance, gift cards) → withdraw or spend it *before* step 6; balances are usually forfeited.
- Deletion requires contacting support → send the request from the account's registered email and keep the ticket number.

## Failure modes & recovery

- **F1 No deletion option exists:** GDPR/CCPA-style erasure request via the privacy contact (privacy@ or a web form); cite "right to erasure"; expect a statutory response window.
- **F2 Accidentally logged in during the grace period:** deletion likely canceled — restart from step 4.
- **F3 Export link expired before download:** re-request the export; large archives can take days to prepare — delay step 6 until it's in hand.

## Verification

Login attempts fail after the grace period, the confirmation email is archived, the exported data archive is stored and readable, and no other service still authenticates through the deleted account.

## Variations

- Financial accounts (banks, brokers): closure requires zero balance and often a signed request; records are retained by law regardless.
- `eu` residents: erasure requests have legal force under GDPR Article 17 — use F1's path if the UI refuses.

## Safety & privacy

High risk: irreversible data loss. The ordering is the safety mechanism — export (2) and detach (3) strictly before confirm (6). Beware lookalike "account deletion services": only ever delete through the service's own authenticated flow.
