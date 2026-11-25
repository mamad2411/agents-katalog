---
name: create-geo-profiles
description: "Creates a number of SoftGlaze Browser profiles in a group, each with a working proxy from one country. Use when the user asks to create or generate SoftGlaze profiles for a country."
argument-hint: "<count 1-50> <country code> <group name>"
arguments: [count, country, group]
disable-model-invocation: true
---

# Create profiles for a country

Follow the softglaze-browser skill: read `softglaze://memory/workspace` and
`softglaze://guide/how-softglaze-works` first and follow them. Anything that changes something asks
the user for approval in the SoftGlaze app, so tell them what you are about to change and why first.
Stop every profile you start when you are done.

Count: $count. Country: $country (two-letter code, upper case). Group: $group.
If any of these is empty, ask the user for it before you start.

1. Call list_groups. If the group does not exist, plan to create it with create_group.
2. Call list_proxies with the country and status "ok" to see how many working proxies from that
   country are free (not used by another profile).
3. If there are fewer free working proxies than the count, tell the user the shortfall before doing
   anything. Never create a profile without a proxy, and never use a proxy from another country.
4. Tell the user the plan: names (follow the naming rules in the workspace memory), group, proxy
   source, and that SoftGlaze will generate each fingerprint.
5. After they approve, call batch_generate_profiles with the count, the country, proxySource
   "unique" and the group.
6. Report what was created and any proxy that failed its live check. Do not start the new profiles
   unless the user asks.
