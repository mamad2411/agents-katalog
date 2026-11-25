---
name: spf-dkim-dmarc-setup
description: Configure and debug SPF, DKIM and DMARC DNS records for a sending domain. Use whenever the user mentions SPF, DKIM, DMARC, BIMI, email authentication, DNS records for email, "emails failing authentication", dmarc reports, p=none or p=quarantine or p=reject, SPF lookup limit, or is setting up a new sending domain. Also use when mail is being rejected or junked and the cause is unclear.
---

# SPF, DKIM and DMARC

Three DNS records that tell receiving servers your mail is genuinely yours. Without all three, a significant share of your email is filtered before any content check happens — and since Google and Yahoo tightened bulk sender requirements, authentication is a prerequisite rather than an optimisation.

Set them up before sending anything. Debugging them after a domain has been damaged is much slower.

## SPF

A TXT record on the domain listing who may send for it.

```
v=spf1 include:_spf.google.com include:sendgrid.net ~all
```

| Part | Meaning |
|---|---|
| `v=spf1` | Version. Always first |
| `include:` | Delegate to a provider's own SPF record |
| `ip4:` / `ip6:` | Authorise a specific address or range |
| `~all` | Soft fail — anything else is suspicious |
| `-all` | Hard fail — anything else is forged |
| `?all` | Neutral. Pointless, don't use |

**The rules that break in practice:**

- **One SPF record per domain.** Two TXT records both starting `v=spf1` is a permanent fail, and it silently breaks all your mail. It happens when a second provider is added by someone who doesn't know a record already exists. Merge the includes into one record.
- **Ten DNS lookup limit.** Each `include:` costs at least one lookup and nested includes count too. Exceed ten and the result is `permerror`, which most receivers treat as a fail. Big providers' includes are expensive; four or five is often enough to hit the ceiling.
- **`~all` over `-all`** while getting started. Move to `-all` once DMARC reports confirm nothing legitimate is failing.
- **SPF breaks on forwarding.** A forwarded message keeps the original sender but arrives from a new IP. This is why DKIM matters and why DMARC accepts either.

```bash
# Check it exists and there's exactly one
dig +short TXT yourdomain.com | grep -c 'v=spf1'    # must be 1

# Count lookups (rough — includes nest)
dig +short TXT yourdomain.com | grep -o 'include:' | wc -l
```

## DKIM

A cryptographic signature. The provider signs outgoing mail with a private key; you publish the public key in DNS at a selector.

```
google._domainkey.yourdomain.com    TXT    "v=DKIM1; k=rsa; p=MIGfMA0GCSq..."
     ^selector
```

The selector varies by provider — `google`, `s1`, `k1`, `selector1` and `selector2` for Microsoft, and so on. Your provider tells you which and gives you the record; you publish it.

Practical notes:

- **2048-bit keys** where the provider supports it. Some DNS hosts require splitting the value across strings for long records.
- **Each sending service needs its own selector.** Google Workspace, a transactional provider and a marketing tool are three separate DKIM records, and all three can coexist.
- **Turn on signing after publishing the key.** Signing with a key that isn't in DNS yet fails everything.
- **Rotate periodically** by publishing a new selector, switching, then removing the old one.

```bash
dig +short TXT google._domainkey.yourdomain.com
dig +short TXT selector1._domainkey.yourdomain.com
```

## DMARC

Ties the other two together. It tells receivers what to do when authentication fails, and it's the only one that sends you reports.

```
_dmarc.yourdomain.com   TXT   "v=DMARC1; p=none; rua=mailto:dmarc@yourdomain.com; fo=1; adkim=r; aspf=r"
```

| Tag | Meaning |
|---|---|
| `p=` | Policy: `none`, `quarantine`, `reject` |
| `rua=` | Where aggregate reports go |
| `ruf=` | Forensic reports. Often unsupported, and they contain message data |
| `pct=` | Percentage of mail the policy applies to. Useful for phased rollout |
| `adkim=` / `aspf=` | Alignment: `r` relaxed (subdomains match), `s` strict |
| `sp=` | Policy for subdomains |

**Roll it out in stages. Never start at reject.**

```
Week 1-2     p=none                    Monitor only. Read the reports.
Week 3-4     p=quarantine; pct=10      Small share to junk
Week 5-6     p=quarantine              All failures to junk
Week 7+      p=reject                  Failures rejected outright
```

The point of `p=none` is the reports. They reveal every service sending as your domain — the CRM, the invoicing tool, the helpdesk, the thing marketing set up in 2019 — and there is always at least one nobody remembered. Going straight to `reject` deletes that mail with no warning.

DMARC passes if **either** SPF or DKIM passes **and** aligns with the From domain. Alignment is the part people miss: SPF can pass for the envelope sender while failing alignment because the From header shows a different domain.

## Reading DMARC reports

Aggregate reports arrive as gzipped XML, daily, from every major receiver. They're unreadable by hand at volume — use a parser or a monitoring service — but the questions are simple:

1. **Which sources are sending as my domain?** Every one should be recognised.
2. **Which are failing?** Legitimate ones need fixing before you tighten the policy.
3. **Is anything unrecognised passing?** That's a serious finding.
4. **What share passes?** Should reach 98%+ before moving to `reject`.

```bash
# Rough look at a single report
gunzip -c report.xml.gz | grep -oE '<source_ip>[^<]+|<disposition>[^<]+|<dkim>[^<]+|<spf>[^<]+'
```

## Debugging a failure

In order:

1. **Send to a seed address** and read the raw headers. `Authentication-Results` states plainly which of the three passed.
2. **Two SPF records?** Most common single cause.
3. **Over the lookup limit?** Look for `permerror`.
4. **DKIM selector published and signing enabled?** Both, not one.
5. **Alignment.** Does the From domain match what SPF and DKIM authenticated?
6. **DNS propagated?** New records take time; a low TTL before changes helps.
7. **Subdomain policy.** If sending from `mail.example.com`, check `sp=` on the parent.

```
Authentication-Results: mx.google.com;
       dkim=pass header.i=@yourdomain.com;
       spf=pass smtp.mailfrom=yourdomain.com;
       dmarc=pass (p=NONE) header.from=yourdomain.com
```

Three passes is the target. Anything else is the finding.

## Bulk sender requirements

Google and Yahoo now require, for anyone sending meaningful volume to their users:

- SPF and DKIM both configured
- A DMARC policy published, at minimum `p=none`
- Alignment between the From domain and the authenticated domain
- One-click unsubscribe headers on bulk mail (`List-Unsubscribe` and `List-Unsubscribe-Post`)
- Spam complaint rate kept under 0.3%, and ideally under 0.1%

These are enforced. Failing them means filtering rather than a warning.

## BIMI

Publishes your logo next to authenticated mail in supporting clients. It requires `p=quarantine` or `p=reject` first, plus an SVG Tiny PS logo, and for most inbox providers a Verified Mark Certificate, which costs real money annually.

Worth it for consumer brands with high volume. Not worth it for cold outbound, where you're sending from lookalike domains anyway.

## Don't do these

- **Don't publish two SPF records.** Merge them.
- **Don't start DMARC at `p=reject`.** You'll silently kill mail you forgot about.
- **Don't use `ruf=`** casually — forensic reports can contain message content and most receivers ignore the tag anyway.
- **Don't authenticate the primary domain and forget the outbound ones.** Each sending domain needs its own full set.
- **Don't assume the provider did it.** Most set up DKIM and leave SPF and DMARC to you.
- **Don't set `-all` before the reports are clean.**

## Related skills

`email-deliverability`, `email-warmup`, `spam-filter-triggers`, `bounce-recovery`, `inbox-rotation-scaling`
