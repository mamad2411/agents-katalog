---
name: company-research
description: Research companies by domain with the HirePulse MCP tools. Covers company enrichment, open jobs, hiring intent, tech stack, Google Ads and published contacts, and filtering a list of companies by hiring activity. Useful for lead enrichment, account research and sales qualification.
---

# Company research with HirePulse

The `hirepulse-b2b` MCP server in this plugin has 9 tools. All take a bare company domain such as `ramp.com`.

## Which tool fits
- One company, everything at once: `get_company_profile`, $0.03 only when at least 2 of 4 sections have data.
- A list of companies, keep the ones that are hiring: `find_hot_buyers`, 2 to 25 domains. The scan is free and returns a `quote_id`; only hot companies are charged.
- A list of companies, one signal each: `batch_lookup`, up to 50 domains, free scan then a quote for the rows with data.
- Changes in open jobs over time: `watch_company_jobs` with the `known_job_ids` from the last answer.
- One signal: `detect_website_tech_stack`, `get_company_open_jobs`, `get_company_hiring_intent`, `get_google_ads_by_domain`.
- Unsure: `ask_hirepulse_advisor` is free and returns the tool, the price and a ready request.

## Cost
- Empty, blocked or not-found results are free.
- MCP tool calls include daily free calls. After that, a result is paid with x402 (USDC on Base), which needs an MCP client that can sign x402 payments; Claude Code cannot sign them by itself.
- `claim_free_trial` gives a one-time 25-call pass to an active Base wallet or a work email.
- Demo domains (`example.com`, `stripe.com`, `linear.app`) are always free and return labeled demo data.

## Good habits
- The optional `context` argument takes a short reason for the call. HirePulse uses it only to understand demand; leave out personal data.
- Treat hiring intent as a heuristic signal, not confirmed purchase intent.
- Growth estimates in `breakout_summary` are not forecasts.
