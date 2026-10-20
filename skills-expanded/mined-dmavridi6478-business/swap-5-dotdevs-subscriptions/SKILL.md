---
name: swap-5-dotdevs-subscriptions
description: The "5 open source apps that replace paid subscriptions" carousel from @dotdevs (Uptime Kuma, Linkwarden, Plausible, Paperless-ngx, Vaultwarden) with each tool's repo, licence and self-hosting catch, read from clones on 5 October 2026 - including that four of five are copyleft (AGPL or GPL), that Vaultwarden is an unofficial Bitwarden-compatible server, and that Plausible and Linkwarden also sell hosted plans. Use when deciding whether to self-host a replacement for a paid monitor, bookmark manager, analytics, document archive or password manager.
---

# 5 open-source swaps for paid subscriptions

Source: a @dotdevs carousel (cover, five tool slides and a "follow for one swap a week" slide). Repos and licences were read from clones on 5 October 2026. Star counts on the slides are unverified.

| Tool | Replaces (slide) | Repo | Licence | Catch |
|---|---|---|---|---|
| Uptime Kuma | paid uptime monitors | louislam/uptime-kuma | MIT | You host it: if the server goes down, so does the monitor. Run it on a different machine from what it watches. README Docker line: `docker run -d --restart=always -p 3001:3001 -v uptime-kuma:/app/data louislam/uptime-kuma:2` |
| Linkwarden | Pocket and Raindrop | linkwarden/linkwarden | AGPL-3.0 | Cloud plan funds development; SSO is listed for Enterprise and self-hosted users; archiving pages stores copies of other people's content |
| Plausible | Google Analytics | plausible/analytics | AGPL-3.0 | Self-hosted community edition is free; the maintainers sell a managed cloud, and the README explains why it is not free. You run Postgres and ClickHouse |
| Paperless-ngx | Evernote for scanned documents | paperless-ngx/paperless-ngx | GPL-3.0 | Install via Docker Compose; your scanned documents become your responsibility (backups, access control) |
| Vaultwarden | 1Password | dani-garcia/vaultwarden | AGPL-3.0 | An **unofficial** Rust server compatible with Bitwarden clients, not 1Password and not run by Bitwarden; report bugs to Vaultwarden, not Bitwarden. Self-hosting a password manager makes you the one who must secure and back it up |

## Honest limits

- "Replaces" means "overlaps": check your real needs first (alerts, mobile apps, team seats, support).
- Copyleft (AGPL, GPL) is no problem for internal use; if you modify and offer the software to others over a network, AGPL requires you to offer them the source.
- Self-hosting trades a subscription for your time: updates, backups, uptime and security are yours. Compare on a trial before cancelling anything.

See also `open-source-swap-stack-8` and `self-hosted-docker-stack`. Use `/self-host-swap`.
