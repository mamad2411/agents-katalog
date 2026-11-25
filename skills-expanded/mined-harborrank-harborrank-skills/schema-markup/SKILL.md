---
name: schema-markup
description: "Audit and write structured data (JSON-LD) for a website: list the site's page types, read each page's source to see what schema it has now, check which rich results Google supports today, write correct JSON-LD that matches the visible content, and validate it with the Rich Results Test, the Schema Markup Validator and Search Console URL Inspection. Use when the user asks about schema markup, structured data, JSON-LD, rich results or rich snippets, review stars, or Organization, LocalBusiness, Product, Article, Breadcrumb or FAQ schema."
---

# HarborRank Schema Markup

## Goal

Give every important page type correct, valid structured data that describes what is on the page, and fix markup that is broken, missing or misleading. Structured data helps Google understand a page and makes it eligible for some rich results; it never guarantees one. The output is a page-type inventory, ready-to-paste JSON-LD per template, and a validation record.

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

Most of this workflow is free: reading pages, the crawl, and URL inspection use no credits. Only the optional live-search check (`get_serp_results`) spends credits.

- If `creditsRemaining` will not cover the planned calls, give the user the estimate and ask before spending. Use the free tools first.
- If a tool replies that a feature "is included in paid plans", tell the user once which feature needs a paid plan and pass on the upgrade link from the reply, skip that tool for the rest of the run, and finish with the other evidence. Do not retry it.
- If a tool fails for insufficient credits, stop making paid calls, tell the user, and finish with free tools and the data you already have. If `whoami` warns that credits are low, say so before a large run.
- If a HarborRank tool says the free trial hasn't started, or that credits ran out, give the user the link from that reply exactly as written, as a clickable link, and wait for them to say they're done before calling HarborRank again. Don't switch to answering without HarborRank data unless they ask you to.
- If the user asks to upgrade, change plan or buy credits, call `get_upgrade_link` (no credits) and give them the link. They pay on HarborRank by card; never say the upgrade is done until `whoami` shows the new plan.
- When `whoami` returns `mode: "self-hosted"`, there are no plan gates.

### Fallback mode (no HarborRank connection)

Use this mode only when Step 0 finds no connection. It works from web search, page reading, and files the user provides.

**Can still do**

- Read the homepage, the sitemap, and one sample page per template to build the page-type inventory.
- Read each sample page's HTML source and list every `application/ld+json` block, plus any microdata or RDFa.
- Check Google's current rich-result eligibility in the search gallery, write the JSON-LD for each page type, and give the user the Rich Results Test and Schema Markup Validator steps to confirm it.
- Frame findings as a sample of pages, not a full crawl.

**Must not estimate**

Traffic, search volume, keyword difficulty, CPC, keyword counts, rankings, backlink counts, Maps pack positions, and Q&A counts. Write `unknown` for each. A web search shows which pages appeared for a query when you searched, not their Google ranking: report it as "appeared in web search", never as a position.

**Output**

- Start with the label **Web-evidence only: no HarborRank data.**
- Name the source (URL or file) of every figure you report.
- End, after any recommended next workflow, with one sentence that names the numbers this report is missing: "Connect HarborRank (start with a 7-day free trial) to crawl the whole site and add Google's own rich-result and indexing verdicts from Search Console." Do not add more sales copy than that.

## Required inputs

- `projectId` (from `list_projects`)
- The site URL (default: the project's domain)
- Optional: the page types or templates the user cares about most, and the CMS or plugin that outputs schema today (Yoast, Rank Math, Shopify theme, hand-coded)

## HarborRank MCP tools

- `run_site_audit`, `get_audit_status`, `get_audit_pages`: crawl the site and list its pages with status, title, indexability and depth. Use them to find the page types and pick sample URLs. The audit does not report structured data or schema issues, so read the page source for that. Free.
- `inspect_urls`: Google's URL Inspection for up to 10 URLs. Besides index status and canonical, each result's `richResultsResult` holds Google's rich-result verdict and, when Google found eligible markup, the detected rich-result types and their errors or warnings. No `richResultsResult` means Google detected no eligible rich result on its last crawl. Needs Search Console connected. Free.
- `get_search_console_performance`: clicks and impressions by `page`, to rank which templates matter most. Free.
- `get_serp_results`: live Google results for up to 10 keywords. Each item has a `type` (such as organic, featured_snippet, people_also_ask, local_pack), which shows which features the results page carries, but not whether a single organic result shows stars or other snippet details. Charges credits (about 30 to 60 per keyword); ask first.
- `create_share_report`: publish the finished work as a read-only page at a shareable link (see "Shareable report" below). Only after the user agrees.

Reading page HTML is done with your own web fetch or browser tools, not a HarborRank tool. Read the raw source, and if the site renders with JavaScript, also check the rendered page, since schema injected by scripts only shows there.

## Workflow

1. If the project's SEO folder has `seo-context.md`, read it first for the site, market, audience, competitors and goals; otherwise ask only what this workflow needs.
2. Build the page-type inventory. Call `list_projects`, then `run_site_audit` (default 50 pages) and `get_audit_pages` once it is `completed`. Group URLs by template: homepage, about or contact, location pages, service pages, product pages, category pages, blog posts, FAQ or help pages. Pick one or two sample URLs per type. If Search Console is connected, use `get_search_console_performance` with `dimensions: ["page"]` to put the templates with the most clicks first.
3. Read what each sample page has now. Fetch the source and list each JSON-LD block: its `@type`, key properties, and whether it parses. Note duplicates (a theme and a plugin both outputting Organization), microdata left over from an old theme, and values that do not match the page (a price, rating, address or author that differs from what the visitor sees).
4. Check what Google supports today. Open https://developers.google.com/search/docs/appearance/structured-data/search-gallery and the page for each type you plan to use, and confirm its required and recommended properties and who is eligible. Do this every run: Google changes eligibility. As of the last update to this skill:
   - **Organization** (logo, name, contact, `sameAs`) and **LocalBusiness** (address, hours, phone, geo) help Google with knowledge panels and business details.
   - **Product** with **Offer**, **AggregateRating** and **Review** can earn price, availability and review snippets. Self-serving reviews of a business on its own site (LocalBusiness or Organization rating its own services) are not eligible for review stars.
   - **Article** (headline, image, dates, author) and **BreadcrumbList** are broadly supported.
   - **FAQPage** rich results have been limited to well-known, authoritative government and health sites since August 2023. **HowTo** rich results are deprecated. FAQ markup is still valid schema, but do not tell other sites it will show in results.
5. Write the JSON-LD per template, not per page. Use only facts visible on that page, use absolute URLs, link entities with `@id` (one Organization the other blocks reference), and keep one block per entity. For CMS sites, say where the template value comes from (a theme field, a plugin setting) so it stays correct as content changes. If a plugin already outputs a type, fix its settings instead of adding a second copy.
6. Validate before handing it over. Run the code through the Rich Results Test (https://search.google.com/test/rich-results) for Google eligibility, and the Schema Markup Validator (https://validator.schema.org) for schema.org correctness. If you cannot run them, give the user the exact steps and the code to paste. Fix every error; explain any warning you leave.
7. After the user deploys, call `inspect_urls` on the sample URLs and read `richResultsResult`. Before Google recrawls, it reflects the old page; say so. Search Console's enhancement reports (Merchant listings, Product snippets, Review snippets, Breadcrumbs) show the same issues sitewide; point the user to them for templates with many pages.
8. Optionally, call `get_serp_results` for one to three money keywords (ask first; it uses credits) to see which features the results page carries and whether competitors earn them.

## Output format

Start with:

- **Verdict:** one or two sentences, for example "Product pages have no Offer data and the homepage outputs Organization twice; both fixable in the theme."
- **Top 3 fixes**, in order.

Then include:

| Page type | Sample URL | Schema now | Problems | Recommended types | Rich result eligible? |
| --------- | ---------- | ---------- | -------- | ----------------- | --------------------- |

Write "Rich result eligible?" as `yes`, `no`, or `limited` with the reason, from Google's documentation, never as a promise. Then give one ready-to-paste JSON-LD block per page type, with a line on where it goes and which fields come from the template, and the validation result for each.

Close with what was not checked (page types without a sample, pages Google has not recrawled, JavaScript-rendered schema you could not see).

- **Next workflow:** end with one recommended next workflow, the reason for it, and the input it starts from. Default: `seo-audit` on the site, since schema fixes help most on pages that are already indexed and crawlable. For a local business, recommend `local-seo` instead, to match the LocalBusiness data with the Google Business Profile.
- **Check back:** end with one dated follow-up: the date (14 days after the user deploys the markup, written out, for example "Monday, November 9") and the exact question to ask then: "Did Google pick up the schema on <domain>?" Say in one line why it needs that wait: Google recrawls updated pages over one to two weeks, and the re-check (URL inspection of the same sample URLs) uses no credits. Add it to the `Follow-ups` list in the SEO folder's `README.md` (create the list if it is missing) so the next session finds it. One follow-up only; don't add reminders or repeat it. If scheduled tasks are available (Cowork and the Claude apps on paid plans), offer once to make this a weekly scheduled task instead, named for the site, so the check runs by itself; the user reviews and confirms the schedule.
- **Where the output goes:** the report as `schema/<domain>-<YYYY-MM-DD>.md`, with each JSON-LD block also saved as `schema/<page-type>.json`. Save it in the project's SEO folder (see `seo-project-setup`); if there is none, ask once whether to create one or where to save instead. If the user prefers a doc or a sheet and a docs or spreadsheet tool is available, put reports in a doc and tables in a sheet instead. Tell the user where it was saved.
- **Shareable report:** once the work is done, offer one time to publish it as a shareable report with `create_share_report`: a read-only page at a link the user can send to a client, a boss or a teammate, no sign-in needed. Write it from this output: findings first, then next steps, then the supporting table. Publish only after the user says yes, and leave out their Search Console and Google Analytics numbers unless they agree to share them. Give them the link; `delete_share_report` removes it.

## Guardrails

- Never mark up content that is not visible on the page. No hidden FAQs, reviews, ratings, prices or addresses that a visitor cannot see. Google treats that as spam and can issue a manual action.
- Never promise a rich result. Valid markup makes a page eligible; Google decides what to show. Say "eligible for", never "will get".
- Check Google's search gallery before recommending a type for rich results, and say when a type is limited or deprecated.
- Never invent ratings, review counts, prices, hours, or any other values. If the page does not show a value, leave the property out.
- Do not invent credit costs or numbers. If HarborRank does not return a value, write `unknown`.
- Separate evidence from inference: every problem names the URL and the source line or validator message behind it.
- Recommend changes, never make them. Ask before any write action.
