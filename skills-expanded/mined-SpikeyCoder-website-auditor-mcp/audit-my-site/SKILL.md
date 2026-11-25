---
name: audit-my-site
description: Run a full Website Auditor audit — AI visibility plus security headers, broken links, performance, and crawlability and markup in one report. Use when the user asks to audit their site, check its security or performance, or is preparing to launch or relaunch a site they own.
---

1. If the user has not named the website, ask which domain to audit.
2. Call `run_audit` for that domain.
3. Summarise the result by category — AI visibility, crawlability and markup,
   security headers, broken links and performance — then list the three
   fixes that would matter most, highest impact first.

If no API key is configured, call `get_sample_audit` instead so the user sees
exactly what the real audit returns, and tell them what it would take to run it
for real.
