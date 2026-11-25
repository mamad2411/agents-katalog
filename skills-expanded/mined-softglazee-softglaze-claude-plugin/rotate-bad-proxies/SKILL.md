---
name: rotate-bad-proxies
description: "Finds failing or blocklisted proxies in SoftGlaze Browser, then rotates their IP or moves their profiles to healthy proxies from the same country. Use when the user asks to fix, replace or rotate bad SoftGlaze proxies."
argument-hint: "[group]"
arguments: [group]
---

# Replace failing or blocklisted proxies

Follow the softglaze-browser skill: read `softglaze://memory/workspace` and
`softglaze://guide/how-softglaze-works` first and follow them. Anything that changes something asks
the user for approval in the SoftGlaze app, so tell them what you are about to change and why first.
Stop every profile you start when you are done.

Group: $group (empty means profiles in every group).

1. Call list_proxies with status "fail", then with blocklisted true. Call get_proxy_health for each to
   confirm it is a pattern and not a single bad check; re-check with check_proxy where the last check
   is old.
2. For each bad proxy, find which profiles use it (list_profiles shows each profile's proxy).
3. For a proxy whose vendor supports it (canRotate true), propose rotate_proxy_ip, then check_proxy
   again.
4. Otherwise propose moving its profiles to healthy, unused proxies from the same country with
   assign_proxy (mode "unique", source "unassigned").
5. Show the user the full plan first. Never move a profile to a proxy from another country, and
   never to a free proxy.
6. After the changes, report what changed and what still needs a new proxy from the vendor.
