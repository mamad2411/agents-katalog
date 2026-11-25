---
name: warm-up-profiles
description: "Plans and starts a SoftGlaze Cookie Warmer run so new profiles build normal browsing history. Use when the user asks to warm up SoftGlaze profiles or build cookies and history."
argument-hint: "<group> [sites, comma separated] [days 1-14]"
arguments: [group, sites, days]
disable-model-invocation: true
---

# Warm up profiles

Follow the softglaze-browser skill: read `softglaze://memory/workspace` and
`softglaze://guide/how-softglaze-works` first and follow them. Anything that changes something asks
the user for approval in the SoftGlaze app, so tell them what you are about to change and why first.
Stop every profile you start when you are done.

Group: $group (if empty, ask the user). Sites: $sites (empty means the default mix of popular
sites). Days: $days (empty means one run now).

1. Call list_profiles for the group and profile_health for each; pick the profiles whose "history"
   factor is "warn" (little browsing history).
2. Use the sites above, or leave sites empty for the default mix. Keep to general, legitimate
   browsing: no logins, sign-ups, posting or ad clicking.
3. Plan small batches (concurrency 1 or 2) and about 30 to 60 seconds per site, so the run looks like
   normal reading and does not overload this computer.
4. Show the user the plan, then call start_warmer for the first batch.
5. Track it with get_run_status and report cookies and sites loaded per profile.
6. If more than one day was asked for: a warm-up across several days needs the Warm-up autopilot in
   the app (Automation page). Tell the user the settings to use there; you cannot schedule future
   runs yourself.
