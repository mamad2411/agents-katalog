---
name: email-dns-setup
description: Plan, generate, audit and verify the DNS records that make email work and keep it out of spam for any domain, on any DNS host (Cloudflare, Route 53, Namecheap, Porkbun, Vercel, OpenTofu/Terraform, external-dns, etc.) and any mail service (Google Workspace, Microsoft 365, Fastmail, Proton, Purelymail, self-hosted, plus Postmark/SES/Resend/Mailgun senders). Covers MX, SPF, DKIM, DMARC, MTA-STS, TLS-RPT, BIMI, subdomain strategy, and locking down domains that never send. Use this skill when the user mentions MX/SPF/DKIM/DMARC, "email DNS", setting up email on a domain, moving mail providers, adding a newsletter or transactional sender, "emails going to spam", "mail not arriving", DMARC reports, or asks how to structure mail for several domains or side businesses, even if they only say "set up email for mydomain.com".
---

# Email DNS setup

Email deliverability is mostly DNS: one wrong or missing record and mail lands in spam, or anyone
can send as the domain. Produce a complete record set, explain the architecture, verify the result.
Provider values (MX hosts, DKIM selectors, SPF includes) come from the provider's docs or portal,
never from memory: they change, and a stale selector fails silently.

## Workflow

### 1. Gather context (ask only for what you cannot look up)

Look up what you can with the step 2 audit script; ask for the rest in one message.

- **Domain(s)** and what each one is for: people's mailboxes, app/transactional mail, newsletters,
  parked / never sends.
- **Mailbox provider** (where humans read mail), if any.
- **Other senders**: transactional service, marketing platform, CRM, helpdesk, website contact form,
  anything else that puts the domain in a From header. Each needs SPF and DKIM authorization.
- **DNS host** (where the nameservers point) and **registrar** (where the domain is renewed). They are
  often different. Run `dig NS` to confirm the DNS host rather than trusting the registrar name.
- **How DNS is managed**: by hand in a dashboard, OpenTofu/Terraform, external-dns, a provider CLI/API.
  This changes where the records should live so automation does not fight manual entries.
- **Existing mail** on the domain: migrating from another provider means the old MX/SPF/DKIM must be
  removed, not added to.

### 2. Audit the current state

Run the bundled read-only script first; it shows what the world sees now.

```bash
scripts/check_mail_dns.sh example.com [dkim-selector ...]
```

It reports NS, MX, SPF (with the DNS lookup count against the limit of 10), DKIM for any selectors
you pass plus a list of common ones, DMARC, MTA-STS, TLS-RPT and BIMI, and flags the usual
problems: multiple SPF records, `+all`, missing DMARC, DMARC without `rua=`, a CNAME on the apex.
Needs `dig`. Set `NS=ns1.example.net` to query the authoritative server right after a change, or
`RESOLVER=1.1.1.1` when the local resolver truncates big TXT sets or hangs.

### 3. Decide the architecture

Settle these with the user, then write them down in the output. Read
`references/architecture.md` when a question goes beyond the summary below.

- **People use the root domain.** `you@business.com` is what customers expect. `you@mail.business.com`
  looks wrong and gains nothing.
- **Automated mail uses dedicated subdomains**, each through a service built for it: `news.` or `mail.`
  for marketing, `notify.`, `tx.` or `send.` for transactional. Reputation is tracked per domain, so
  a newsletter complaint spike does not take password-reset mail down with it, and the root domain's
  SPF record stays short.
- **Do not send bulk or app mail through the mailbox provider.** It rate-limits and does not handle
  bounces; transactional services do.
- **One SPF record per name.** Two `v=spf1` TXT records at the same name is a permanent SPF failure.
  Merge includes into one record and stay under 10 DNS-querying mechanisms.
- **Own the DMARC record.** Some providers offer a CNAME to their DMARC policy. Decline it: it skips
  the reporting phase and often starts at `p=reject`, so mail from any forgotten sender is dropped
  with no visibility. Publish a TXT record with `p=none` and an `rua=` address the user actually
  reads, then tighten. Rollout plan is in `references/records.md` (DMARC section).
- **Lock down domains that never send.** A parked domain with no mail records is a free phishing
  domain. Publish null MX, `v=spf1 -all`, `p=reject` DMARC and an empty wildcard DKIM.
- **Add the newer protections** when the provider supports them: MTA-STS and TLS-RPT for transport
  encryption, BIMI only after DMARC is at enforcement (and it needs a VMC for most receivers).

### 4. Generate the record set

Get provider values from `references/providers.md` for the common
providers, or from the provider's current docs / admin portal for anything else. When a value
(DKIM selector, verification token, MX priority) comes from the user's portal, leave a clear
placeholder like `<from Purelymail portal>` rather than inventing one. Record syntax, length limits
and quoting rules are in `references/records.md`.

Present records in this exact table shape, one table per zone, so they can be pasted into any host:

| Host (relative) | Type | Priority | Value | TTL | Notes |
|---|---|---|---|---|---|
| `@` | MX | 10 | `mx.provider.example.` | 3600 | |
| `@` | TXT | | `v=spf1 include:_spf.provider.example -all` | 3600 | only SPF record on `@` |
| `sel1._domainkey` | CNAME | | `sel1.dkim.provider.example.` | 3600 | DNS only, never proxied |
| `_dmarc` | TXT | | `v=DMARC1; p=none; rua=mailto:dmarc@example.com` | 3600 | tighten after 2 to 4 weeks |

Then give, separately:

1. **Records to delete** (old MX, old SPF, old DKIM, duplicate TXT). Deletions are the step people
   skip and the most common cause of "I added everything and it still fails".
2. **Host-specific entry notes** from `references/dns-hosts.md`: apex notation, zone
   auto-append, TXT quoting, proxy toggles, API/IaC snippets.
3. **Mailbox-side setup** DNS cannot do: `postmaster@`, `abuse@` (RFC 2142), the `dmarc@` report
   address, role aliases, 2FA, app passwords.
4. **Verification steps** (step 5).

Before writing the answer, read `references/answer-checklist.md`: the best practices every answer
states, the pitfalls to check the records against, and the output template to follow.

### 5. Verify

1. Re-run `scripts/check_mail_dns.sh` with the DKIM selectors; use `NS=` to separate "not
   published" from "not propagated yet". In the answer, give the user plain `dig` commands (list in
   `references/records.md`), not this script: they usually do not have the skill's files. Offer to
   re-run the audit for them.
2. Send a message from the new setup to a Gmail or Outlook.com mailbox and open "Show original" /
   "View message source". SPF, DKIM and DMARC must all show PASS, and the DKIM `d=` must be the
   user's domain, not the provider's. A provider-domain `d=` means the DKIM CNAMEs are wrong or
   proxied.
3. For transactional and marketing subdomains, trigger a real send from the service and check the
   same headers.
4. Optionally get a third-party read from mail-tester.com or MXToolbox.
5. Review the first DMARC aggregate reports in two weeks (Cloudflare DMARC Management, Postmark's
   free digest, or dmarcian parse the XML), then move to `p=quarantine`, then `p=reject`.

## Reference files

- `references/answer-checklist.md`: best practices to state every time, common pitfalls, output template.
- `references/records.md`: every record type, exact syntax, limits, DMARC rollout, MTA-STS/TLS-RPT/BIMI, null-MX lockdown.
- `references/providers.md`: record templates and doc links for mailbox providers, transactional and marketing senders, self-hosted servers.
- `references/dns-hosts.md`: per-host UI quirks, CLI/API examples, OpenTofu/Terraform and external-dns guidance.
- `references/architecture.md`: root vs subdomain reasoning, multi-domain/multi-business layouts, migration sequencing, forwarding and ARC.
- `scripts/check_mail_dns.sh`: read-only audit of a domain's mail DNS.
