---
name: email-security
description: "Covers email authentication and transport architecture: SPF/DKIM/DMARC with a staged rollout to p=reject, the Google/Yahoo/Microsoft bulk-sender rules, DMARCbis (RFC 9989), ARC, MTA-STS/TLS-RPT, BIMI, and secure email gateway vs API-based (ICES) protection. Use when the user asks about SPF, DKIM, DMARC, MTA-STS or BIMI records, spoofing protection, bulk-sender requirements, or choosing an email security gateway."
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# Email security architecture

Email auth answers one question: **may this server speak for the domain in the
visible From?** It stops exact-domain spoofing. It does not stop a lookalike domain, a
compromised real mailbox, or a lure sent through a legitimate SaaS, so layer it. The
human/process side is `load_skill social-engineering-defense`.

## What each record actually checks

- **SPF** (RFC 7208) authorizes IPs for the **envelope MAIL FROM** (Return-Path), not
  the From the user sees. Limit: **10 DNS-querying mechanisms** and 2 void lookups.
  Past that it's `permerror`, which counts as fail. Forwarding breaks SPF.
- **DKIM** (RFC 6376) signs with domain `d=`, using the key at `<selector>._domainkey.<d>`.
  Use RSA 2048 and rotate selectors. A vendor signing with **its own** `d=` does not
  count toward your DMARC.
- **DMARC** passes when SPF **or** DKIM passes **and aligns** with the From domain
  (relaxed: same organizational domain; strict: exact). Aligned DKIM carries the load
  because it survives forwarding.
- **DMARCbis is the standard now**: RFC 9989 (core), 9990 (aggregate) and 9991 (failure
  reports), published May 2026 as Proposed Standard. They obsolete RFC 7489 and 9091.
  Changes: a DNS **tree walk** replaces the Public Suffix List, and `pct=` is gone
  (use the `t=y` testing flag instead). New `np=` sets policy for non-existent
  subdomains, and `psd=` marks public suffixes. Write new records without `pct`.
  verify: https://www.rfc-editor.org/info/rfc9989/

## Staged rollout to p=reject

1. **Inventory first.** Publish `p=none; rua=mailto:...` for 2 to 4 weeks, across a
   month-end and a payroll run. Use a report processor, since raw XML doesn't scale. If
   `rua` points to another domain, that domain must publish
   `<yours>._report._dmarc.<theirs>` TXT.
2. **Fix each sender, not the policy.** Give every ESP/CRM/HR/ticketing platform a custom
   DKIM `d=` and bounce domain on your domain. Move bulk mail to its own subdomain so
   reputation and policy stay isolated.
3. **p=quarantine, then p=reject**, using `t=y` on the first step where receivers
   support it. Read the reports at each step.
4. **Close the side doors**: `sp=reject` and `np=reject`. For **parked domains**
   publish `v=spf1 -all`, `p=reject` and a null MX (RFC 7505).

Pitfalls:

- SPF include sprawl, which flattening hides until a vendor changes IPs.
- `sp=none` left open.
- Stalling at p=none forever.
- **MX not pointing at the mail platform + p=none + `~all`**, which lets "internal"
  spoofs through direct-send paths. The fix is reject, `-all` and correct connectors.
  verify: https://www.microsoft.com/en-us/security/blog/2026/01/06/phishing-actors-exploit-complex-routing-and-misconfigurations-to-spoof-domains/

## Mailbox-provider bulk-sender rules (current)

These apply to mail **to consumer mailboxes** at ≥5,000/day from one From domain.
Treat them as the floor for invoicing and notification mail too.

- **Gmail and Yahoo** (since Feb 2024): SPF **and** DKIM, DMARC at least `p=none`
  aligned with one of them, valid PTR/FCrDNS, TLS, and RFC 5322 compliance. Marketing
  mail needs **one-click unsubscribe** (RFC 8058), honored within 2 days. Reported spam
  must stay **under 0.3%** (aim for under 0.1%). Gmail **ramped enforcement in Nov 2025**
  with temporary and permanent rejections. Small senders still need SPF or DKIM.
  verify: https://support.google.com/mail/answer/81126 , https://senders.yahooinc.com/best-practices/
- **Microsoft consumer** (outlook.com/hotmail/live, since May 2025): SPF pass, DKIM
  pass, and DMARC at least `p=none` aligned with at least one. Failures are rejected
  with `550 5.7.515`.
  verify: https://support.microsoft.com/en-us/outlook/fix-ndr-error-550-5-7-515-in-outlook-com

## ARC: use it, don't build on it

ARC (RFC 8617, **Experimental**) lets intermediaries (lists, forwarders, your SEG) seal
the auth results they saw. Receivers honor a seal only from **trusted sealers**, so in
M365 add your gateway as a trusted ARC sealer. ARC's status is moving. The IETF DMARC WG
adopted a draft to reclassify ARC as **Historic** (2026), and the DKIM WG is drafting
**DKIM2** as the replacement for forwarding-safe auth.
verify: https://datatracker.ietf.org/group/dmarc/documents/

## Transport: MTA-STS, TLS-RPT, DANE

STARTTLS is opportunistic and can be stripped. **MTA-STS** (RFC 8461) closes that
without DNSSEC:

- Publish `_mta-sts.<d>` TXT `v=STSv1; id=<bump-on-edit>`.
- Serve the policy at `https://mta-sts.<d>/.well-known/mta-sts.txt`. Its `mx:` lines
  must match every real MX.
- Run `mode: testing`, then switch to `enforce`.

**TLS-RPT** (RFC 8460, `_smtp._tls` TXT `v=TLSRPTv1; rua=...`) reports failures, so turn
it on before `enforce`. **DANE** (RFC 7672) is stronger but needs DNSSEC. Exchange Online
validates MTA-STS and DANE outbound by default. Inbound DANE needs DNSSEC plus
`Enable-SmtpDaneInbound`.
verify: https://learn.microsoft.com/en-us/exchange/security-and-compliance/enhance-mail-flow-using-strict-transport-security

## BIMI

BIMI is the inbox logo (`default._bimi.<d>` TXT pointing to an SVG Tiny PS file plus
a mark certificate). It **requires DMARC enforcement** (quarantine or reject, no
`sp=none`). Gmail accepts a **VMC** (registered trademark) or a **CMC** (no trademark,
prior-use logo). It is a brand feature, not a control. Its value is as the exec-friendly
reason to finish DMARC. verify: https://support.google.com/a/answer/10911320

## SEG vs API-based (ICES)

| Model                                     | Strengths                                                          | Weaknesses                                                                                                                                  |
| ----------------------------------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------- |
| **SEG** (MX → gateway, inline)            | Blocks pre-delivery; outbound DLP/encryption; any mail platform    | Blind to internal mail; in M365 needs Enhanced Filtering for Connectors or auth sees the gateway IP; bypassable by direct-to-tenant routing |
| **ICES** (Graph/Gmail API, post-delivery) | Sees internal/lateral phish and ATO/BEC behavior; deploys in hours | Short in-inbox race; a tenant-wide high-privilege OAuth app (supply-chain risk); API throttling                                             |
| **Native** (Defender for O365 / Gmail)    | Already licensed; auth, ZAP/purge, user reporting built in         | Detection depth varies with tuning                                                                                                          |

Decision: on M365/Workspace, start with **native, tuned**, and add **ICES** for BEC/ATO
depth. Choose a **SEG** for pre-delivery blocking across mixed platforms or heavy outbound
needs. Never stack a SEG in front of native filtering without fixing connector/IP
visibility. verify: https://www.gartner.com/reviews/market/email-security

## marq tie-in (auditing your own domain)

- `dns_lookup` needs an explicit `record_type`, because the default `ANY` is refused by
  many resolvers (RFC 8482). Query:
  - `TXT` on the apex (SPF), `_dmarc.<d>`, `<sel>._domainkey.<d>`, `_mta-sts.<d>`,
    `_smtp._tls.<d>` and `default._bimi.<d>`
  - `MX`, plus each MX's PTR
- Follow each SPF `include:` to count lookups. Use `dns_lookup` to check parked domains.
  Fetch the MTA-STS policy with web fetch.
- Active checks with swaks against your **own** MX only (marq runs none):
  - `--to <mailbox> --from <addr> --tls` tests STARTTLS and delivery. Read the delivered
    copy's Authentication-Results.
  - `--quit-after RCPT` with an outside from/to tests for an open relay without sending.
- `testssl.sh -t smtp` on `host:25` grades STARTTLS (own MX only).
- `report_finding` gaps: no DMARC, p=none past 90 days, SPF permerror, no MTA-STS,
  parked domains without reject. Use CWE-290 for spoofability. Inspecting a suspect
  message is `load_skill phishing-email-analysis`.
