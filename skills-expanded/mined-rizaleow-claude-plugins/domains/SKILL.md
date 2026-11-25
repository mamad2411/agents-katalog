---
description: Manage domains on Hostinger — check availability across TLDs, list owned domains, lock/unlock transfers, update nameservers, manage WHOIS profiles and privacy, configure HTTP forwarding. Use when the user wants to look up or change anything about a domain (not its DNS zone — that's the dns-records skill).
---

# Domain operations via `hostinger-cli`

## Preflight

1. `command -v hostinger-cli` — install via `brew install rizaleow/tap/hostinger-cli` if absent.
2. `hostinger-cli auth status` — instruct `hostinger-cli auth login` if not authenticated.

## Availability check

```sh
hostinger-cli domains availability check --domain example --tlds com,net,io -o json
```

The `--domain` value is the **label** (without TLD); `--tlds` is a
comma-separated list of TLDs to probe. The response includes
per-TLD availability and indicative pricing.

## Owned-domain portfolio

| Goal | Command |
| --- | --- |
| List owned domains | `hostinger-cli domains portfolio list -o json` |
| Inspect one | `hostinger-cli domains portfolio get --domain example.com -o json` |
| Purchase | `hostinger-cli domains portfolio purchase --domain example.com --body @order.json` |
| Lock transfers | `hostinger-cli domains portfolio lock --domain example.com` |
| Unlock transfers | `hostinger-cli domains portfolio unlock --domain example.com` |
| Update nameservers | `hostinger-cli domains portfolio update-nameservers --domain example.com --body @ns.json` |
| Enable WHOIS privacy | `hostinger-cli domains portfolio enable-privacy --domain example.com` |
| Disable WHOIS privacy | `hostinger-cli domains portfolio disable-privacy --domain example.com` |

## WHOIS contact profiles

| Goal | Command |
| --- | --- |
| List profiles | `hostinger-cli domains whois list -o json` |
| Get profile | `hostinger-cli domains whois get --whois-id <id> -o json` |
| Create profile | `hostinger-cli domains whois create --body @profile.json` |
| Delete profile | `hostinger-cli domains whois delete --whois-id <id>` |
| Which domains use it | `hostinger-cli domains whois usage --whois-id <id> -o json` |

## Forwarding

| Goal | Command |
| --- | --- |
| Get forwarding | `hostinger-cli domains forwarding get --domain example.com -o json` |
| Create / replace | `hostinger-cli domains forwarding create --domain example.com --body @fwd.json` |
| Remove | `hostinger-cli domains forwarding delete --domain example.com` |

## Patterns

- **Confirm before purchase.** `domains portfolio purchase` is a billable
  action. Always show the user the resolved price from
  `domains availability check` and explicitly confirm before invoking.
- **Lock by default on long-lived domains.** Suggest `portfolio lock`
  after registration unless the user is mid-transfer.
- **Don't confuse with DNS edits.** Nameserver changes go through
  `portfolio update-nameservers`. Record-level edits (A, MX, TXT, etc.)
  go through the **dns-records** skill (`dns zone update`).
