---
name: dns-engineering
description: Manage DNS records and their effects on services. Use when
  configuring domains and records.
metadata:
  tags: dns, engineering
---

# DNS Engineering

## Use this skill when
- Designing record layouts (A, CNAME, TXT, MX)
- Tuning TTL for migration and failover
- Troubleshooting DNS-related failures

## Do not use this skill when
- Web/API application logic
- Only following a provider wizard

## Instructions
1. Know record types and when each is correct (CNAME vs A/ALIAS).
2. Use short TTLs during migrations; raise after.
3. Add SPF/DKIM/DMARC for mail domains; verify with dig.
4. Prefer a single source of truth; use IaC/API over GUI clickops.
5. Set CDN/shared providers consistently (apex vs www).
6. Verify propagation with dig, not memory.
7. Document domain ownership and aliases.

## Checklist
- Records confirmed with dig
- TTLs deliberate for migrations
- Email auth records set

## Output Format
- Record map | TTL plan | verification commands | ownership

## Common Mistakes
- CNAME at the apex
- TTL 1s forever after migration
- No SPF/DKIM/DMARC on mail domains
