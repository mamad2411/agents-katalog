---
name: fix-proxy-mismatches
description: "Finds SoftGlaze Browser profiles whose timezone, language or geolocation disagree with their proxy country and proposes fixes for approval. Use when the user asks to fix mismatches, check timezones or languages against proxies, or reduce CAPTCHAs across a group."
argument-hint: "[group]"
arguments: [group]
---

# Fix timezone, language and location mismatches

Follow the softglaze-browser skill: read `softglaze://memory/workspace` and
`softglaze://guide/how-softglaze-works` first and follow them. Anything that changes something asks
the user for approval in the SoftGlaze app, so tell them what you are about to change and why first.
Stop every profile you start when you are done.

Group: $group (empty means every group).

1. Call list_profiles (with the group above, if one was given) and page through all of them.
2. Call profile_health (live: false) for each profile that has a proxy. Collect the factors
   timezone, language, geolocation and webrtc that are not "pass".
3. For profiles whose proxy country is unknown or older than a week, call check_proxy on that proxy
   first, then score again.
4. Report a table: profile, proxy country, what disagrees, and the fix (for example "timezone: set
   to Based on IP").
5. Propose the setting fixes as update_profile calls with the "fixes" list (tz-auto, lang-auto,
   geo-auto, webrtc-safe), grouped so the user approves them in as few requests as possible. Where
   the proxy itself is wrong, propose assign_proxy with a healthy proxy from the right country
   instead. Apply nothing until the user approves.
