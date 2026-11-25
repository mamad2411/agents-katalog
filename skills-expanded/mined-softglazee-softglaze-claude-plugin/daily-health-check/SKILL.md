---
name: daily-health-check
description: "Daily health check of SoftGlaze Browser: checks running and recently used profiles and their proxies, then reports problems with the fix for each. Use when the user asks for a SoftGlaze health check, a morning check, or which profiles or proxies have problems."
argument-hint: "[group]"
arguments: [group]
---

# Daily health check

Follow the softglaze-browser skill: read `softglaze://memory/workspace` and
`softglaze://guide/how-softglaze-works` first and follow them. Anything that changes something asks
the user for approval in the SoftGlaze app, so tell them what you are about to change and why first.
Stop every profile you start when you are done.

Group: $group (empty means every group).

1. Call workspace_summary, then list_sessions to see what is running.
2. Call list_profiles (with the group above, if one was given) and take the running profiles plus
   the 20 most recently used.
3. For each of those profiles call profile_health (live: false) and note every factor that is
   "fail" or "warn".
4. For each distinct proxy those profiles use, call get_proxy_health. If a proxy was last checked
   more than a day ago, call check_proxy on it.
5. Report one table: profile, CAPTCHA risk grade, proxy (name, country, last status, latency), and
   the problems found.
6. Under the table, list the fixes in order of impact, each with the exact tool call you would make.
   Do not apply any fix until the user says which ones to apply.
