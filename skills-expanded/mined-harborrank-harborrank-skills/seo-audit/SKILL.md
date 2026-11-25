---
name: seo-audit
description: "Audit a website's SEO health and diagnose traffic drops: crawl the site for technical issues (broken pages, redirects, duplicate or missing titles, noindex, canonicals, thin content, orphan pages), check indexing in Google Search Console, compare Search Console periods to find which pages and queries lost clicks, and rank the fixes by impact. Use when the user asks to audit their site, run an SEO check or health check, find technical SEO problems, asks why traffic, clicks, or rankings dropped, or why a page is not indexed."
---

# HarborRank SEO Audit

## Goal

Find what is holding a site back in search and fix the most important things first. Two modes, often used together:

- **Health audit:** crawl the site, read the issue report, check indexing for the pages that matter, and produce a prioritized fix list.
- **Traffic-drop diagnosis:** use Search Console to find when clicks fell, which pages and queries lost them, and why.

If the user asks about a drop, start with the diagnosis and run the crawl only where it helps explain the losing pages.

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

Most of this audit is free: the crawl, the issue report, Search Console performance, and URL inspection use no credits. Only the optional live-search checks spend credits. On Free the crawl covers up to 500 pages and skips Lighthouse.

- If `creditsRemaining` will not cover the planned calls, give the user the estimate and ask before spending. Use the free tools first.
- If a tool replies that a feature "is included in paid plans", tell the user once which feature needs a paid plan and pass on the upgrade link from the reply, skip that tool for the rest of the run, and finish with the other evidence. Do not retry it.
- If a tool fails for insufficient credits, stop making paid calls, tell the user, and finish with free tools and the data you already have. If `whoami` warns that credits are low, say so before a large run.
- If a HarborRank tool says the free trial hasn't started, or that credits ran out, give the user the link from that reply exactly as written, as a clickable link, and wait for them to say they're done before calling HarborRank again. Don't switch to answering without HarborRank data unless they ask you to.
- If the user asks to upgrade, change plan or buy credits, call `get_upgrade_link` (no credits) and give them the link. They pay on HarborRank by card; never say the upgrade is done until `whoami` shows the new plan.
- When `whoami` returns `mode: "self-hosted"`, there are no plan gates.

### Fallback mode (no HarborRank connection)

Use this mode only when Step 0 finds no connection. It works from web search, page reading, and files the user provides.

**Can still do**

- Read the homepage and key pages: titles, meta descriptions, headings, canonical tags, robots meta, and internal links.
- Read `robots.txt` and the XML sitemap, and spot-check sitemap URLs for errors or redirects.
- Review the user's Search Console CSV exports (Pages, Queries, Dates, Indexing reports), if provided, to find what dropped and when.
- Frame findings as a sample of pages, not a full crawl.

**Must not estimate**

Traffic, clicks, impressions, search volume, keyword difficulty, keyword counts, rankings, backlink counts, Maps pack positions, and Q&A counts. Write `unknown` for each. A web search shows which pages appeared for a query when you searched, not their Google ranking: report it as "appeared in web search", never as a position. Do not claim a page is or is not indexed from a web search.

**Output**

- Start with the label **Web-evidence only: no HarborRank data.**
- Name the source (URL or file) of every figure you report.
- End, after any recommended next workflow, with one sentence that names the numbers this report is missing: "Connect HarborRank (start with a 7-day free trial) to crawl the whole site and add your Search Console clicks and indexing status." Do not add more sales copy than that.

## Required inputs

If the project's SEO folder has `seo-context.md` (see `seo-context`), read it first for the site, market, audience, competitors and goals, and ask only for what it doesn't cover.

- `projectId` (from `list_projects`)
- The site URL to audit (default: the project's domain)
- For a traffic drop: the approximate date it started, if the user knows it

## HarborRank MCP tools

- `run_site_audit`: crawls the site with HarborRank's crawler (robots.txt-aware) and checks every page for SEO issues. Free. `maxPages` defaults to 50; `runLighthouse` applies on paid plans only.
- `get_audit_status`: progress of a running audit. Free.
- `get_audit_issues`: the prioritized issue report; every issue carries a `how_to_fix`. Filter by `severity` (`critical`, `warning`, `info`) or `issueType`. Free.
- `get_audit_pages`: crawled pages with status code, title, description, word count, indexability, depth, and links. Filter by `fetchClass`, `statusCode`, or `urlContains`. Free.
- `get_search_console_performance`: clicks, impressions, CTR, and average position by `query`, `page`, `country`, `device`, or `date`, for a `dateRange` or explicit `startDate`/`endDate`, with optional filters. Free.
- `inspect_urls`: Google's URL Inspection for up to 10 URLs: indexed or not and why, last crawl, Google-selected vs declared canonical. Free.
- `get_landing_page_performance`: Search Console clicks and position joined with Google Analytics organic sessions, engagement, key events (conversions) and revenue per landing page; also lists pages that earn Google clicks but never show up in Analytics (broken tracking). Needs Google Analytics connected for the project.
- `get_analytics_report`: Google Analytics sessions, users, engagement and key events by channel, landing page, source, device, country or date, with optional `compareTo` (`previous_period` or `previous_year`). Needs Google Analytics connected.
- `get_serp_results`: live Google results for up to 10 keywords, to see who took a lost query or which SERP features appeared. Charges credits (about 30 to 60 per keyword).
- `get_domain_overview`: organic footprint estimate, for a site without Search Console. Charges credits.
- `create_share_report`: publish the finished work as a read-only page at a shareable link (see "Shareable report" below). Only after the user agrees.

## Workflow A: Health audit

1. Call `list_projects` and pick the project for the site. Use its domain as the start URL unless the user names another.
2. Call `run_site_audit`. Keep the default 50 pages for a quick check; for a full audit of a larger site ask before going above 500 pages, and say Free crawls stop at 500.
3. Call `get_audit_status` until the audit is `completed`. Wait between checks rather than calling it back to back.
4. Call `get_audit_issues` with `severity: "critical"`, then with `severity: "warning"`. Read `info` issues only if there is little else to fix.
5. If Search Console is connected, call `get_search_console_performance` with `dimensions: ["page"]` and `dateRange: "last_3_months"`. Use clicks per page to rank the fixes: an issue on a page with clicks comes before the same issue on a page with none. If Google Analytics is connected, call `get_landing_page_performance` instead: it returns the same clicks plus conversions per page, so an issue on a page that converts comes first, and any page in `pagesMissingFromAnalytics` is a tracking fix to report.
6. Call `inspect_urls` for up to 10 URLs that matter most: top pages by clicks, plus pages flagged `noindex-page`, `canonicalized-page`, `canonical-conflict`, or `blocked-page`. Confirm what Google actually indexed instead of assuming.
7. Group issues that share one cause. Duplicate titles across 200 pages from one template are one fix, not 200.
8. Rank the fixes: indexing and crawl blockers first (blocked, server errors, broken pages, noindex or canonical mistakes on pages that should rank), then problems on high-click pages, then sitewide template fixes, then everything else.

## Workflow B: Traffic-drop diagnosis

Search Console is required for this mode. If it is not connected, say so, point the user to the project's Integrations page in the HarborRank app (it is free), and run Workflow A meanwhile.

1. Call `get_search_console_performance` with `dimensions: ["date"]` and `dateRange: "last_6_months"` (or `last_16_months` for a long view) to see when clicks and impressions changed. Use the user's date if they gave one, and confirm it in the data.
   If Google Analytics is connected, also call `get_analytics_report` with `dimensions: ["sessionDefaultChannelGroup"]`, `metrics: ["sessions", "keyEvents"]` and `compareTo: "previous_period"` over the same dates. If only Organic Search fell, it is a search problem; if every channel fell at once, suspect broken tracking or a site outage before rankings.
2. Pick two windows of equal length and the same weekdays: the weeks before the drop and the weeks after it. Do not include the last 3 days, which are incomplete.
3. For each window, call `get_search_console_performance` with explicit `startDate` and `endDate`, first with `dimensions: ["page"]`, then with `dimensions: ["query"]`. List the pages and queries with the largest click losses.
4. Classify each big loss by what moved:
   - **Impressions fell, position held:** less demand or seasonality, or the page dropped out of the index. Check last year's same period if the data covers it.
   - **Position fell:** ranking loss to competitors, or a content or technical change on the page.
   - **Position held, CTR fell:** a SERP change (an AI Overview, new features, ads) or a worse title or snippet.
   - **Everything fell at once, sitewide:** look for a technical cause first (robots.txt, noindex, a migration, redirects), then a Google update.
5. Call `inspect_urls` on the top losing pages to check indexing, canonical, and last crawl.
6. If a technical cause is possible, run Workflow A steps 2 to 4, then call `get_audit_pages` with `urlContains` for the losing pages to see their status codes and indexability.
7. If position fell on important queries, call `get_serp_results` for the top 1 to 3 lost queries (ask first; it uses credits) to see who ranks now and which SERP features appeared.

## Output format

Start with:

- **Verdict:** one or two sentences, for example "Two critical problems, both fixable this week" or "Clicks fell 38% from Aug 12, concentrated on 6 blog posts that lost position to two competitors."
- **Top 3 fixes**, in order.

For a health audit, then include:

| Priority | Issue | Pages affected | Evidence | Fix | Effort |
| -------- | ----- | -------------- | -------- | --- | ------ |

Use the `how_to_fix` from the issue report in the Fix column, rewritten for this site. Effort is `quick`, `moderate`, or `project`.

For a traffic drop, then include:

- **Timeline:** when it started, how big it is (clicks and impressions, before vs after), and whether it is sitewide or concentrated.
- **What lost traffic:**

| Page or query | Clicks before | Clicks after | Change | What moved | Likely cause |
| ------------- | ------------- | ------------ | ------ | ---------- | ------------ |

- **Causes:** each cause with its evidence, labelled confirmed or likely.
- **Fixes:** in priority order.

Close both with what was not checked (pages beyond the crawl budget, Lighthouse on Free, queries without Search Console data).

- **Next workflow:** end with one recommended next workflow, the reason for it, and the input it starts from. If competitors took the lost queries, recommend `competitor-analysis` on the domain that gained. If pages compete for the same queries, recommend `keyword-clustering` on those queries. Otherwise recommend `keyword-research` on the striking-distance queries (positions 5 to 20) from Search Console.
- **Check back:** end with one dated follow-up: the date (today plus 14 days, written out, for example "Monday, November 9") and the exact question to ask then: "Did Google pick up the audit fixes on <domain>?" For a traffic drop, ask instead: "Did clicks come back on the pages that dropped?" Say in one line why it needs that wait: Google recrawls fixed pages over one to two weeks, and the re-check (a new crawl, URL inspection and Search Console) uses no credits. Add it to the `Follow-ups` list in the SEO folder's `README.md` (create the list if it is missing) so the next session finds it. One follow-up only; don't add reminders or repeat it. If scheduled tasks are available (Cowork and the Claude apps on paid plans), offer once to make this a weekly scheduled task instead, named for the site, so the check runs by itself; the user reviews and confirms the schedule.
- **Where the output goes:** the report as `audits/<domain>-<YYYY-MM-DD>.md`. Save it in the project's SEO folder (see `seo-project-setup`); if there is none, ask once whether to create one or where to save instead. If the user prefers a doc or a sheet and a docs or spreadsheet tool is available, put reports in a doc and tables in a sheet instead. Tell the user where it was saved.
- **Shareable report:** once the work is done, offer one time to publish it as a shareable report with `create_share_report`: a read-only page at a link the user can send to a client, a boss or a teammate, no sign-in needed. Write it from this output: findings first, then next steps, then the supporting table. Publish only after the user says yes, and leave out their Search Console and Google Analytics numbers unless they agree to share them. Give them the link; `delete_share_report` removes it.

## Guardrails

- Never invent a site health score or grade. Report counts of issues by severity, as the audit gives them.
- Do not blame a Google update without evidence. Say a drop is "consistent with" an update only when its timing matches and no technical or competitive cause explains it better.
- Compare windows of equal length and matching weekdays, and leave out the last 3 days of Search Console data. Search Console dates are Pacific Time.
- If the crawler was blocked, report the pages as blocked and say the audit could not see them; do not treat them as broken.
- Do not report Lighthouse or page-speed findings on the Free plan; the crawl skips Lighthouse there.
- Separate evidence from inference: every cause needs the numbers or the inspection result behind it.
- Recommend changes, never make them. Ask before any write action.
