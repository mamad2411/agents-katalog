---
name: build-growth-plan
description: Turn the user's latest Website Auditor audit into a written growth plan, grounded in the pages AI assistants actually cite. Use when the user asks what to do about their AI visibility, wants their audit turned into a plan, or asks for a growth, GTM or marketing plan for their site.
---

Only build a plan for a site the user owns or represents — never to prepare
marketing advice about someone else's business.

1. If the user has not named the website, ask which domain to plan for
   (e.g. example.com).
2. Call `get_gtm_plan` for that domain. If it reports no audit on record, call
   `run_audit` for the domain first, then call `get_gtm_plan` again.
3. Report the phases and the actions in each, in plain language.
4. Say which of the cited sources are the user's own and which belong to a
   competitor. Competitor pages explain the gap; they are never where the user
   should publish.

If the user mentions a budget, a team size or a deadline, pass it as
`constraints`. If they want a different emphasis — local directories, content,
a launch — pass it as `focus`. To refine a plan rather than start over, pass the
earlier plan's markdown as `prior_plan`.

If no API key is configured, call `get_sample_audit` instead so the user sees
exactly what the real check returns, and tell them what it would take to run it
for real.
