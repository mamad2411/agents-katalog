---
name: vibeops-domain
description: >
  Set up a custom web address (domain name) for a deployed app, including the DNS records
  needed and verifying the secure connection is active. Use whenever the user mentions their
  domain name, custom URL, DNS, HTTPS, or 'I want to use my own domain'.
  Also triggers on: "point my domain", "myapp.com", "SSL certificate", "custom URL".
---

# Vibeops — Domain

You are helping the user point a custom domain at their deployed app and confirming it works securely. There's no Railway CLI command for attaching a custom domain — this is a Dashboard-only step, so you guide the user through it rather than automating it.

**Required references:** the vibeops `references/railway.md` (custom domain section — Dashboard-only steps). This skill calls no shared scripts.

---

## Step 1 — Read config

Read `.infra/config.yml`. If missing, route to `vibeops-configure` first.

If `domain` is empty:
> "Right now your app is using a free Railway address. Do you want to set up your own domain (like myapp.com), or are you happy with the free one for now?"

If the user wants to keep the free address, stop here — nothing to do.

---

## Step 2 — Dashboard step (no CLI available)

Tell the user exactly where to click — do not guess at a CLI shortcut, Railway doesn't have one:
> "Go to your Railway Dashboard → your project → your app service → Settings → Domains → Custom Domain, and enter `[domain]`."

Railway's UI will then show a DNS record to add — relay only what it actually displays. Don't assume it's always a CNAME: for apex domains (`example.com` with no `www`), Railway may show an ALIAS/ANAME record or suggest redirecting to `www` instead, since plain CNAME at the apex isn't valid at most registrars. Ask the user to paste back what Railway's dashboard shows them, or read it together.

---

## Step 3 — Print DNS record instructions

Once you know the exact record Railway wants, tell the user precisely what to add at their registrar:

```
Go to wherever you bought your domain (your registrar) and add this record:

Type:  [exactly what Railway showed — CNAME, ALIAS, or ANAME]
Name:  [www or @ depending on what they're pointing]
Value: [exact value Railway showed]

This usually takes 10 minutes to a few hours to take effect.
```

Never invent the record value — only relay what Railway's own dashboard displayed.

---

## Step 4 — Verify propagation

Poll for DNS resolution:
```bash
dig +short [domain] CNAME
```
or if `dig` isn't available:
```bash
nslookup [domain]
```

Retry every ~30 seconds, a handful of times. Report once it resolves to Railway's target.

If neither tool is available locally, tell the user:
> "I can't check DNS propagation directly from here — try visiting https://dnschecker.org, or just wait a bit and try opening [domain] in your browser."

Always mention propagation can take time — never imply it should be instant.

---

## Step 5 — Confirm TLS is active

Once DNS resolves, check the secure connection:
```bash
curl -sI https://[domain]
```

If it returns a normal HTTP response (not a certificate error), report:
> "Your domain is live and secure — https://[domain] is working."

If it errors or shows a cert mismatch, report plainly:
> "DNS looks like it's pointing correctly, but the secure connection isn't ready yet — this can take a few extra minutes after DNS resolves while Railway issues the certificate. Want me to check again in a bit?"

**Never claim TLS is active without actually checking.**

---

## Step 6 — Update config

If `domain` in `.infra/config.yml` doesn't match the confirmed domain, update it — same overwrite-diff-confirm pattern used in `vibeops-configure`: show what's changing, ask "Save this change?" before writing.

---

## What you must never do

- Never claim TLS/HTTPS is active without checking via curl first
- Never invent a DNS record value — only relay what Railway's dashboard actually shows
- Never skip telling the user that DNS propagation takes time
- Never guess at a CLI command for custom domains — there isn't one; this is always a Dashboard step
