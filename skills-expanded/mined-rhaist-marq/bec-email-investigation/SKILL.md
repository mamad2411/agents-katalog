---
name: bec-email-investigation
description: Guides investigating a business-email-compromise or mailbox takeover in Microsoft 365 or Google Workspace, covering which logs to pull before they expire, the persistence to hunt (inbox rules, forwarding, delegates, OAuth grants, added MFA/devices), the containment order, and fast funds recovery via bank recall and the FBI IC3 Recovery Asset Team. Use when a mailbox is suspected compromised, a payment was diverted by email, or the user asks how to investigate BEC.
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# BEC / mailbox-takeover investigation

BEC is the most expensive email crime: about **$3.0B in reported US losses in 2025**,
second only to investment fraud.
verify: https://www.ic3.gov/AnnualReport/Reports/2025_IC3Report.pdf
This skill is the mailbox-specific work. The lifecycle is `load_skill incident-response`,
and notify/escalate decisions are `load_skill incident-response-leadership`.

## First 15 minutes: money before forensics

If a payment went out, run funds recovery **in parallel, now**. Recall odds fall by the hour.

1. **Phone** the originating bank's fraud/wire desk. Don't use email, because the
   mailbox may be watched. Request a **wire recall** (SWIFT recall internationally,
   Fedwire/ACH recall or reversal domestically) and a freeze request to the
   beneficiary bank. Have ready: amount, time, beneficiary bank, account,
   routing/SWIFT, and the IMAD/OMAD reference.
2. **File at ic3.gov** the same day with those details. The **Recovery Asset Team (RAT)**
   runs the **Financial Fraud Kill Chain** to freeze funds at recipient banks, for
   domestic (D-FFKC) and international transfers. The long-published international
   criteria are **≥ $50,000, within 72 hours, SWIFT recall already initiated**. Report
   smaller losses anyway, and confirm the current criteria with your FBI field office.
   The RAT froze roughly 60% of the amounts it acted on in 2025.
   verify: https://www.ic3.gov/Outreach/Brochures/IC3-FFKC_Domestic.pdf
3. Notify the **cyber insurer** before hiring IR if the policy mandates its panel
   (`load_skill legal-contractual`). Outside the US, call the national fraud
   centre and police, with the same urgency.

## Classify first: it decides whose logs matter

- **Account takeover**: your mailbox was compromised, and your tenant holds the evidence.
- **Vendor email compromise**: the vendor's mailbox was compromised and you paid new
  bank details. Evidence is in **their** tenant. You have the inbound headers
  (`load_skill phishing-email-analysis`). Alert the vendor through a known contact.
- **Impersonation** (lookalike domain, no compromise): header analysis and a takedown.
  `dnstwist` lists registered lookalikes of your domain; `rdap` gives the
  registrar and registration date for the takedown request.
  Check your DMARC (`load_skill email-security`).

## Preserve: retention is short

Export before you change anything, and snapshot rules before you delete them. Don't
let preservation delay containment while the attacker is actively sending.

- **Entra sign-in logs**: interactive **and non-interactive** (token replay hides there).
  Retention is **7 days Free, 30 days P1/P2**.
  verify: https://learn.microsoft.com/en-us/entra/identity/monitoring-health/reference-reports-data-retention
- **Unified audit log** (Purview; `Search-UnifiedAuditLog` or the Graph audit query
  API): **180 days Standard**, 1 year default with Audit Premium. Confirm ingestion
  was on with `Get-AdminAuditLogConfig`.
  verify: https://learn.microsoft.com/en-us/purview/audit-log-retention-policies
- **Message trace**: `Get-MessageTraceV2` covers **90 days**, in 10-day windows per query
  (the default is 48h). The legacy `Get-MessageTrace` has been deprecated since Sep 2025.
  verify: https://learn.microsoft.com/en-us/powershell/module/exchangepowershell/get-messagetracev2
- **Defender hunting** (`EmailEvents`, `UrlClickEvents`, `CloudAppEvents`) if licensed.
- **Bulk collection**: Invictus Microsoft-Extractor-Suite covers UAL, trace, sign-ins,
  rules, MFA and OAuth. CISA Untitled Goose Tool is an alternative. Check how
  actively each is maintained.
- **Workspace**: Reporting → Audit and investigation → Gmail, User (suspicious login,
  2SV/password changes), OAuth (token grants) and Admin log events. Retention is
  generally **6 months** and not adjustable, so export to BigQuery where the edition
  allows. The security investigation tool's default filter is 7 days.
  verify: https://support.google.com/a/answer/7061566
- **Workspace mail settings**: dump per-user filters, forwarding, delegates and
  POP/IMAP with GAM or the Gmail API.

## Reconstruct: the persistence checklist

- **Initial access**: a new IP/ASN/user agent right after the phish click. For AiTM:
  "MFA satisfied by claim in token" from a new IP, and the **same session ID** in two
  geographies, means a stolen cookie. Also watch for `deviceCode` protocol, legacy
  auth (`BAV2ROPC`, IMAP/SMTP AUTH), and scripted UAs.
- **Inbox rules** (`New-InboxRule`, `Set-InboxRule`, `UpdateInboxRules`): delete,
  mark-read, or move to RSS Feeds/Conversation History/Archive. Keywords like
  invoice/payment/wire/bank or the vendor's name. Rule names like `.`. Run
  `Get-InboxRule -IncludeHidden`, because MAPI-hidden rules don't show in OWA.
  verify: https://learn.microsoft.com/en-us/purview/audit-log-search-mailbox-rules
- **Forwarding**: `Set-Mailbox ForwardingSmtpAddress` and rule ForwardTo/RedirectTo. If
  an admin was touched, also transport rules and a relaxed outbound auto-forward block.
- **Rights**: FullAccess (`Add-MailboxPermission`), SendAs/SendOnBehalf, folder
  permissions, new mobile/EAS partnerships, IMAP/POP re-enabled.
- **OAuth**: `Consent to application`/`Add app role assignment` with `Mail.Read`,
  `Mail.Send` or `offline_access`. User-approved sync and bulk-mail apps survive a
  password reset. Also new app registrations and new service-principal credentials.
  A Microsoft-managed consent policy has been the default since mid-2025. It narrows
  this vector but doesn't close it.
  verify: https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/configure-user-consent
- **Auth methods**: `User registered security info` (attacker authenticator or phone),
  device registration (a PRT, common after device-code phish), Temporary Access Pass,
  app passwords.
- **Objective**:
  - `MailItemsAccessed` shows what was read. `Sync` means a whole folder, which feeds
    `load_skill privacy-us`/`privacy-eu`.
  - `SearchQueryInitiatedExchange` (Premium) shows attacker searches.
  - `Send`/`SendAs`, deleted sent items, outbound phish bursts, and OneDrive lure shares.
- Pivot every attacker IP, UA and session **tenant-wide**, since crews take several
  mailboxes. ATT&CK: T1114.003 forwarding rule, T1564.008 hiding rules, T1098.005 device
  registration, T1539 cookie theft, T1528 app-token theft.

## Containment order

1. **Disable sign-in and revoke sessions** (`Revoke-MgUserSignInSession`). A reset
   alone leaves refresh tokens and stolen cookies live. CAE-aware apps cut off in
   minutes, others when the access token expires (~1h).
2. **Reset the password** from a clean device. **Remove attacker MFA methods and
   devices.** Re-register the user on phishing-resistant MFA (`load_skill iam`).
3. **Strip persistence**: rules, forwarding, delegates and folder permissions, OAuth
   grants (delete the grant **and** disable the service principal), mobile
   partnerships, app passwords. Turn off IMAP/POP/SMTP AUTH. EXO disables Basic SMTP
   AUTH by default from end of Dec 2026.
   verify: https://techcommunity.microsoft.com/blog/exchange/updated-exchange-online-smtp-auth-basic-authentication-deprecation-timeline/4489835
4. **Block the infrastructure** (CA location block, tenant block list for lookalikes).
   **Purge** the attacker's mail from every mailbox.
5. Re-enable, then watch 30 days for the same IP, ASN or app returning.

Step 3 before step 1 lets a live attacker re-add everything. Step 2 before step 1 is
the most common failure.

## Close the loop

- Warn **every external party** the account emailed. Their payments to "you" may be in flight.
- Harden against a repeat:
  - phishing-resistant MFA plus token protection or compliant-device CA
  - block the device-code flow where unused
  - admin consent workflow
  - external auto-forward block
  - a **callback-verified payment-change process** (`load_skill social-engineering-defense`)
- `report_finding` each persistence item with its audit-record evidence, then `render_report`.
