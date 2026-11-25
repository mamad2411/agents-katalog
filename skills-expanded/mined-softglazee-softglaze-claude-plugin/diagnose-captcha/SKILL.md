---
name: diagnose-captcha
description: "Explains why one SoftGlaze Browser profile keeps getting CAPTCHAs or block pages, using profile_health and proxy checks, and proposes the smallest set of fixes. Use when the user says a SoftGlaze profile gets CAPTCHAs, is blocked, or is flagged."
argument-hint: "<profile name or id>"
arguments: [profile]
---

# Why does this profile get CAPTCHAs?

Follow the softglaze-browser skill: read `softglaze://memory/workspace` and
`softglaze://guide/how-softglaze-works` first and follow them. Anything that changes something asks
the user for approval in the SoftGlaze app, so tell them what you are about to change and why first.
Stop every profile you start when you are done.

Profile: $profile (if empty, ask the user which profile).

1. Find it with list_profiles (search by name) or get_profile (by id).
2. Call profile_health with live: true. This tests its proxy now and compares the exit IP's country
   and timezone with the profile's settings.
3. Explain each failing or warning factor in plain words: what it is, why sites react to it, and how
   much it matters (use the factor's impact).
4. Check the proxy itself with get_proxy_health and, if it has not been checked today, check_proxy.
   Say whether it is a datacenter or home IP, whether it is blocklisted, and whether other profiles
   share it.
5. Propose the smallest set of fixes that removes the biggest risks, for example: put timezone,
   language, location or WebRTC back to safe values with update_profile and its "fixes" list
   (tz-auto, lang-auto, geo-auto, webrtc-safe); move a failing or blocklisted proxy's profile to a
   healthy proxy from the same country with assign_proxy; warm the profile up with start_warmer if
   it has little history.
6. Ask before changing anything. Never suggest ways to get past a CAPTCHA itself.
