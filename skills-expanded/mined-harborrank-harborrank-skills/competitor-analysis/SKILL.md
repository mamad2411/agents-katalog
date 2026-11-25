---
name: competitor-analysis
description: "Deep dive on one competitor's SEO: organic traffic, ranked keywords, top pages, content themes, backlinks, local visibility, and head-to-head SERPs against the user's site, ending in a plan to outrank them. Use when the user names a competitor domain and asks why it ranks, what it ranks for, how to beat it, or for a keyword gap. For a whole market, use competitive-landscape instead."
---

# HarborRank Competitor Analysis

## Goal

Analyze one competitor deeply enough to decide what to learn from, avoid, counter-position against, or outrank.

Use this for a named competitor. For identifying the market leaders first, use `competitive-landscape`.

## Step 0: Check connection

Before any other step, confirm the HarborRank MCP tools are loaded. Look for `get_domain_overview` or `list_leads` among your tools, including deferred tools you can load (the name may carry a prefix such as `mcp__harborrank__`). If they are there, call `whoami`: it uses no credits, confirms the user is signed in, and returns `creditsRemaining` for budgeting the run. Do not call a research tool to test the connection.

If neither tool is available, or `whoami` fails because the user is not signed in, tell the user plainly: "HarborRank isn't connected, so I can't pull live HarborRank data yet." Then tell them how to connect it:

- Claude Code with the HarborRank plugin: run `/mcp`, choose `harborrank`, and sign in.
- Claude Code without the plugin: run `claude mcp add --transport http --scope user harborrank https://app.harborrank.com/mcp`, then `/mcp` to sign in.
- Claude on the web, desktop or Cowork: open Customize, then Connectors, search for HarborRank, choose Connect, and sign in. New accounts start with a 7-day free trial.
- Cursor with the HarborRank plugin: open Cursor Settings, then MCP, and sign in to `harborrank`.
- Gemini CLI with the HarborRank extension: run `/mcp auth harborrank`.
- Other clients: add `https://app.harborrank.com/mcp` as a remote MCP server. Setup for each client is at https://harborrank.com/docs/mcp.

Tell them what happens when they connect: they sign in to HarborRank with Google or email and start a 7-day free trial. Then they come back to this conversation and say "connected", and you pick up the task where it stopped.

Do not stop there. Continue in fallback mode (below). If the user connects HarborRank mid-task, run Step 0 again and switch to the full workflow.

### Plan limits

On hosted HarborRank, research tools spend credits. New accounts start with a 7-day free trial (1,000 research credits, one project); paid plans start at $29/month with 15,000 credits. Search Console, saved keywords, rank tracker reads, and site crawls use no credits. A keyword search costs about 50 credits and a domain overview about 80. Full backlinks, lead research (`research_lead`), and Lighthouse checks need a paid plan; on Free, the backlinks tools return a preview (totals and the top 3 referring domains, about 50 credits) with an upgrade link.

- If `creditsRemaining` will not cover the planned calls, give the user the estimate and ask before spending. Use the free tools first.
- If a tool replies that a feature "is included in paid plans", tell the user once which feature needs a paid plan and pass on the upgrade link from the reply, skip that tool for the rest of the run, and finish with the other evidence. Do not retry it.
- If a tool fails for insufficient credits, stop making paid calls, tell the user, and finish with free tools and the data you already have. If `whoami` warns that credits are low, say so before a large run.
- If a HarborRank tool says the free trial hasn't started, or that credits ran out, give the user the link from that reply exactly as written, as a clickable link, and wait for them to say they're done before calling HarborRank again. Don't switch to answering without HarborRank data unless they ask you to.
- Two extras are included in Pro and Agency: local grids larger than 5x5 (a 7x7 `run_local_grid`) and more than 3 tracked competitors per rank tracker (`add_rank_tracker_competitors`). If a tool replies that something needs Pro or Agency, tell the user once what Pro adds, pass on the Pro link from the reply exactly as written, and carry on with what their plan includes (a 5x5 grid, the first 3 competitors). Do not retry it.
- Mention Pro unprompted only when the task needs it: a whole-town map, or watching more than 3 competitors. Say it once per run, in one sentence, with the link from `get_upgrade_link` (`plan: "pro"`).
- If the user asks to upgrade, change plan or buy credits, call `get_upgrade_link` (no credits) and give them the link. They pay on HarborRank by card; never say the upgrade is done until `whoami` shows the new plan.
- When `whoami` returns `mode: "self-hosted"`, there are no plan gates.

### Fallback mode (no HarborRank connection)

Use this mode only when Step 0 finds no connection. It works from web search, page reading, and files the user provides.

**Can still do**

- Read the competitor's site: navigation, sitemap, blog, product, and comparison pages.
- Map their page types, content themes, and positioning.
- Check live search results for target terms to compare the two sites head to head.
- Use the user's Search Console CSV exports, if any, as their own baseline.
- Frame the analysis as qualitative.

**Must not estimate**

Traffic, search volume, keyword difficulty, CPC, keyword counts, rankings, backlink counts, Maps pack positions, and Q&A counts. Write `unknown` for each. A web search shows which pages appeared for a query when you searched, not their Google ranking: report it as "appeared in web search", never as a position.

**Output**

- Start with the label **Web-evidence only: no HarborRank data.**
- Name the source (URL or file) of every figure you report.
- End, after any recommended next workflow, with one sentence that names the numbers this report is missing: "Connect HarborRank (start with a 7-day free trial) to add this competitor's traffic, ranked keywords, and backlink profile." Do not add more sales copy than that.

## Required inputs

If the project's SEO folder has `seo-context.md` (see `seo-context`), read it first for the site, market, audience, competitors and goals, and ask only for what it doesn't cover.

- `projectId`
- Competitor domain
- User's domain when comparison is requested
- Optional topic/category/location/language

## HarborRank MCP tools

- `get_domain_overview`: baseline organic traffic and keyword count.
- `get_search_console_performance`: when comparing to the user's own domain and Search Console is connected, use it as the first-party baseline (real clicks/impressions/CTR/position) instead of estimating the user's own performance from third-party data.
- `get_ranked_keywords`: exact keyword, URL, rank, intent, traffic, CPC, and SERP-type rows for the competitor domain or page.
- `get_backlinks_overview`: backlink/referring-domain profile.
- `find_serp_competitors`: validate whether the named competitor is a real search competitor across the target keyword set.
- `search_local_businesses`, `get_local_serp_results`, and `get_google_business_questions`: use for local SEO competitors when Maps/local-pack visibility, nearby businesses, categories, or Google Q&A matter.
- `get_serp_results`: validate direct head-to-head SERPs for important keywords.
- `research_keywords`: expand gaps or category terms when needed.
- `get_rank_tracker`, `add_rank_tracker_competitors`: read the user's rank trackers, and add competitor domains to one so every check also records where they rank for the tracked keywords. Adding a competitor uses no credits. Basic compares up to 3 per tracker; Pro and Agency up to 10.
- `create_share_report`: publish the finished work as a read-only page at a shareable link (see "Shareable report" below). Only after the user agrees.

## Workflow

1. Call `get_domain_overview` for the competitor, passing provided location/language when supported.
2. If comparing to the user, call `get_domain_overview` for the user's domain too — and if Search Console is connected, `get_search_console_performance` for the user's real baseline.
3. Call `get_ranked_keywords` for the competitor. Use filters like `maxRank`, `minSearchVolume`, `excludeBrandTerms`, and `resultTypes` to keep rows relevant.
4. If comparing to the user, call `get_ranked_keywords` for the user's domain/page too, or use `get_serp_results` for the shared terms when a lighter check is enough.
5. For local SEO, use `search_local_businesses` and `get_local_serp_results` around the relevant business location(s) before drawing local-pack conclusions. Add `get_google_business_questions` only when Q&A evidence matters.
6. Use `find_serp_competitors` when the competitor was supplied by the user but its search overlap is unclear.
7. Group competitor keywords into themes:
   - Product/category terms
   - Alternatives/comparisons
   - Templates/tools/calculators
   - Educational guides
   - Branded demand
   - Local/neighborhood terms when relevant
8. Call `get_backlinks_overview` for the competitor, especially if authority appears to explain rankings. On Free this returns a preview (totals and the top 3 referring domains); use it, note that the full profile needs a paid plan, and continue.
9. Use `get_serp_results` for important shared or target keywords to compare positioning, passing provided location/language when supported.
10. Produce an actionable plan:
    - What they are doing well
    - Where they are vulnerable
    - Which pages/keywords to pursue
    - What to avoid copying
11. If the user's project has a rank tracker (`get_rank_tracker`) and the competitor shares its keywords, offer once to keep watching it: `add_rank_tracker_competitors` with the tracker ID and the competitor's domain. Its positions show next to the user's from the next check. Add it only after the user says yes.

## Output format

Start with:

- Competitor snapshot
- Biggest lesson
- Best opportunity to beat them

Then include:

| Area | Competitor pattern | Evidence | HarborRank opportunity |
| ---- | ------------------ | -------- | ---------------------- |

Include sections for:

- Top keyword themes
- Content/page types working for them
- Backlink/authority notes
- Head-to-head SERP observations
- Priority actions for the user

- **Next workflow:** end with one recommended next workflow, the reason for it, and the input it starts from. Default: `link-prospecting` against the competitor's strongest pages, the ones that rank for the keywords the user wants, to find the sites that link to them.
- **Check back:** end with one dated follow-up: the date (today plus 30 days, written out, for example "Monday, November 9") and the exact question to ask then: "What changed for <competitor-domain> since <today's date>?" Say in one line why it needs that wait: ranking footprints shift month to month, and a month gives a fair comparison with this report. Add it to the `Follow-ups` list in the SEO folder's `README.md` (create the list if it is missing) so the next session finds it. One follow-up only; don't add reminders or repeat it. If scheduled tasks are available (Cowork and the Claude apps on paid plans), offer once to make this a weekly scheduled task instead, named for the site, so the check runs by itself; the user reviews and confirms the schedule.
- **Where the output goes:** the report as `competitors/<competitor-domain>-<YYYY-MM-DD>.md`. Save it in the project's SEO folder (see `seo-project-setup`); if there is none, ask once whether to create one or where to save instead. If the user prefers a doc or a sheet and a docs or spreadsheet tool is available, put reports in a doc and tables in a sheet instead. Tell the user where it was saved.
- **Shareable report:** once the work is done, offer one time to publish it as a shareable report with `create_share_report`: a read-only page at a link the user can send to a client, a boss or a teammate, no sign-in needed. Write it from this output: findings first, then next steps, then the supporting table. Publish only after the user says yes, and leave out their Search Console and Google Analytics numbers unless they agree to share them. Give them the link; `delete_share_report` removes it.

## Guardrails

- Do not treat all competitor keywords as desirable. Filter for business fit.
- Separate evidence from inference.
- Do not infer competitor page/content-type patterns from keyword rows alone; use SERP or web evidence for page-level claims.
- For local SEO, do not infer Maps/local-pack strength from national organic domain metrics alone; use local business and local SERP tools when the location is known or reasonably discoverable.
- Do not recommend copying content; recommend a stronger angle or better answer to the same intent.
- If the user's domain is unavailable, frame the analysis as competitor-only.
