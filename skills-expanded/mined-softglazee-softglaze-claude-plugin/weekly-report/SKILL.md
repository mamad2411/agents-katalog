---
name: weekly-report
description: "Writes a one-page weekly SoftGlaze Browser report: workspace activity, proxy health trends, the vendor scoreboard and the riskiest profiles. Use when the user asks for a weekly SoftGlaze report or summary."
---

# Weekly report

Follow the softglaze-browser skill: read `softglaze://memory/workspace` and
`softglaze://guide/how-softglaze-works` first and follow them. Anything that changes something asks
the user for approval in the SoftGlaze app, so tell them what you are about to change and why first.
Stop every profile you start when you are done.

Read only.

1. workspace_summary: profiles, proxies, groups, running sessions, plan and limits.
2. get_activity (limit 200): launches, edits, macro and warm-up runs this week, and by whom.
3. get_proxy_health with no proxy id: the recent health of the pool and the vendor scoreboard
   (success rate, speed, blocklist rate per vendor).
4. list_proxies with status "fail": proxies that need attention.
5. Report in short sections: what happened, proxy health and the best and worst vendors (from the
   user's own checks only), problems to fix next week, and the profiles with the highest CAPTCHA
   risk (profile_health on the 10 most used).

Keep it to one page and say where each number comes from.
