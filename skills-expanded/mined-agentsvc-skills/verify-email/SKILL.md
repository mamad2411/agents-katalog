---
name: verify-email
description: Check whether an email address really exists before sending outreach, importing a lead list or accepting a sign-up. Asks the receiving mail server (SMTP check, no email is sent) on top of syntax, MX, disposable and role-address checks, and returns deliverable, undeliverable, catch_all, risky or unknown. agentsvc.io, $0.002 per address, no account.
---

# Verify email addresses

`POST https://agentsvc.io/api/v1/proxy/email-verify` with `{"email": "jane@example.com"}` asks the mail server whether the mailbox exists. No email is sent. $0.002 per address. Results are cached for 6 hours, so a repeated address answers instantly.

## What `data.status` means

- `deliverable`: the mailbox exists.
- `undeliverable`: it does not exist. Remove the address.
- `catch_all`: the domain accepts every address, so the mailbox cannot be confirmed.
- `risky`: disposable address or full mailbox.
- `unknown`: the server refused the check or uses greylisting. Try again later.

Also returned: `is_disposable`, `is_role_address` (info@, support@), `is_free_provider`, `mx_records` and the raw SMTP answer.

Only need syntax, MX and disposable checks without asking the mail server? `email-validate` does that with the same body.

## Try it free

```sh
curl -s -X POST https://agentsvc.io/api/v1/try/email-verify -H "Content-Type: application/json" -d '{}'
```

## Call it

With a credit token (bought at https://agentsvc.io/credits for $5 or more in USDC on Base, kept in `AGENTSVC_TOKEN`). A list, one address per line:

```sh
while read email; do
  curl -s -X POST https://agentsvc.io/api/v1/proxy/email-verify \
    -H "Authorization: Bearer $AGENTSVC_TOKEN" -H "Content-Type: application/json" \
    -d "{\"email\":\"$email\"}" | jq -r '[.data.email, .data.status] | @tsv'
done < leads.txt
```

Without a token the endpoint answers 402 and any x402 client pays it in USDC (Base, Solana, Polygon or Arbitrum): https://agentsvc.io/docs#quickstart. With the Zero CLI: `zero fetch https://agentsvc.io/api/v1/proxy/email-verify -d '{"email":"…"}'`

## Rules

Tell the user the total before checking a long list (addresses x $0.002). Remove duplicates first. Never ask for a private key in the chat.

Guide: https://agentsvc.io/guides/verify-email
