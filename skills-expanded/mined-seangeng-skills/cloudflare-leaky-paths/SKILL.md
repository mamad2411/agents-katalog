---
name: cloudflare-leaky-paths
description: Generate and apply a Cloudflare WAF custom rule that blocks common scanner/leaky paths (.env, .git, wp-login, phpMyAdmin, backups, infra config) at the edge before they reach the origin. Use when the user wants to block scanner traffic, harden a Cloudflare zone, stop .env/.git probing, reduce bot/scanner load, or asks about "leaky paths" or WAF custom rules.
---

# Cloudflare leaky-paths WAF rule

Block high-signal scanner paths at Cloudflare's edge so they never hit the
origin. Cuts log noise, origin load, and the risk of an exposed secret being
fetched. Inspired by the `leaky-paths` wordlist (github.com/ayoubfathi/leaky-paths).

## When to use

- "Block scanners / bots at the edge"
- "Stop .env / .git probing"
- "Harden my Cloudflare zone / add a WAF rule"
- "These scanner hits are spamming my logs"

## The rule

Build a single Cloudflare custom-rule **expression** by OR-ing the path groups
the user wants. Each clause is `(http.request.uri.path contains "<path>")`.

### Path groups

**Dotfiles & secrets**
`/.env` `/.git` `/.svn` `/.aws` `/.ssh` `/.config` `/.DS_Store` `/.htaccess` `/.htpasswd`

**WordPress**
`/wp-login` `/wp-admin` `/wp-includes` `/wp-content` `/xmlrpc`

**Admin & DB tools**
`/phpmyadmin` `/adminer` `/server-status` `/server-info`

**Backups & dumps**
`/backup` `/backup.zip` `/dump.sql` `/db.sql` `/database.sql`

**Infra & CI config**
`/docker-compose.yml` `/.dockerenv` `/.terraform` `/.github` `/.vscode` `/.idea`

> Only include WordPress / admin groups if the site actually has none of those —
> otherwise you may block legitimate `/wp-admin` logins. Confirm the stack first.

### Example expression

```
(http.request.uri.path contains "/.env")
or (http.request.uri.path contains "/.git")
or (http.request.uri.path contains "/.aws")
or (http.request.uri.path contains "/wp-login")
or (http.request.uri.path contains "/phpmyadmin")
or (http.request.uri.path contains "/xmlrpc")
```

## How to apply

### Option A — Dashboard (fastest)
1. Cloudflare dashboard → your zone → **Security → WAF → Custom rules**.
2. **Create rule**, name it `block-leaky-paths`.
3. Switch the expression editor to **Edit expression** and paste the expression.
4. Action: **Block**. Deploy.

### Option B — API
```bash
curl -X POST \
  "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/firewall/rules" \
  -H "Authorization: Bearer $CF_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '[{
    "filter": { "expression": "<EXPRESSION>" },
    "action": "block",
    "description": "block-leaky-paths"
  }]'
```

### Option C — Terraform
```hcl
resource "cloudflare_ruleset" "block_leaky_paths" {
  zone_id = var.zone_id
  name    = "block-leaky-paths"
  kind    = "zone"
  phase   = "http_request_firewall_custom"

  rules {
    action     = "block"
    expression = "<EXPRESSION>"
    description = "Block scanner/leaky paths at the edge"
    enabled    = true
  }
}
```

## Verify

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://example.com/.env   # expect 403
curl -s -o /dev/null -w "%{http_code}\n" https://example.com/        # expect 200
```

## Notes

- Prefer **Block** over Managed Challenge for these — there's no legitimate
  reason to request `/.env`.
- `contains` matches anywhere in the path, so `/foo/.git/config` is caught too.
- Keep the list lean; chasing every CVE path is a losing game. These are the
  high-signal "quick win" endpoints scanners hit first.

Credit: trick popularized by @vikingmute; paths distilled from
`ayoubfathi/leaky-paths`.
