---
name: ai-search-visibility
description: "Find out whether a brand shows up in AI answers (Google AI Overviews, ChatGPT, Perplexity, Claude) for the questions its buyers ask, how many visits AI assistants already send, which sources those answers cite instead of the site, and what to change so the site gets cited: answer-first content, clear facts and numbers, comparison and FAQ structure, schema, presence on the third-party pages AI answers cite, and crawler access for GPTBot, ClaudeBot, PerplexityBot and Google-Extended. Use when the user asks about AI SEO, AEO, GEO, LLM SEO, showing up in ChatGPT or AI Overviews, getting cited or recommended by AI assistants, or AI search traffic."
---

# HarborRank AI Search Visibility

## Goal

Show where the brand stands in AI answers for the questions its buyers ask, what traffic AI assistants already send, and which sources get cited instead. End with a short, ordered list of changes that make the site easier for AI answers to find, trust and cite. AI answers draw on pages that already rank and on pages that state facts plainly, so most of the work is ordinary SEO done with care.

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
- If the user asks to upgrade, change plan or buy credits, call `get_upgrade_link` (no credits) and give them the link. They pay on HarborRank by card; never say the upgrade is done until `whoami` shows the new plan.
- When `whoami` returns `mode: "self-hosted"`, there are no plan gates.

Search Console and the site crawl use no credits; `get_ai_referral_traffic` charges about 10 credits per call. Live SERPs (`get_serp_results`), ranked keywords and keyword metrics charge credits, so keep the question set small.

### Fallback mode (no HarborRank connection)

Use this mode only when Step 0 finds no connection. It works from web search, page reading, and files the user provides.

**Can still do**

- Read the site's `robots.txt` and report whether it allows or blocks GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot and Google-Extended.
- Ask AI assistants the buyer questions, with the user or with your own web tools, and record which brands and sources each answer names. Label this a sample from one date, not a ranking.
- Read the pages those answers cite and the site's own pages for answer-first structure, clear facts, comparison and FAQ sections, and schema.
- Use Google Analytics or Search Console CSV exports in the workspace for AI assistant visits and query data. Those figures are the user's own data; report them with the file as the source.

**Must not estimate**

Traffic, search volume, keyword difficulty, CPC, keyword counts, rankings, backlink counts, Maps pack positions, and Q&A counts. Write `unknown` for each. A web search shows which pages appeared for a query when you searched, not their Google ranking: report it as "appeared in web search", never as a position.

**Output**

- Start with the label **Web-evidence only: no HarborRank data.**
- Name the source (URL or file) of every figure you report.
- End, after any recommended next workflow, with one sentence that names the numbers this report is missing: "Connect HarborRank (start with a 7-day free trial) to add your AI assistant traffic from Google Analytics and the keywords where Google AI Overviews already cite your site." Do not add more sales copy than that.

## Required inputs

- `projectId`
- The brand name and site domain
- 5 to 15 questions buyers ask before they choose a product or service like this one, in their own words
- Optional competitors, market/location/language

If `projectId` is missing, use `list_projects` first. If the user has no question list, build one in workflow step 2 and confirm it with them before running paid calls.

## HarborRank MCP tools

- `get_ai_referral_traffic`: real visits from AI assistants (ChatGPT, Perplexity, Gemini, Copilot, Claude and others) from Google Analytics, with sessions, engagement, key events and revenue per assistant, the share of all traffic, and with `byLandingPage` the pages they send people to. Use `compareTo` to see the trend. Needs Google Analytics connected; if it is not, the reply has a connect link to pass on.
- `get_ranked_keywords`: with `resultTypes: ["ai_overview_reference"]`, the keywords where Google's AI Overview cites a page from that domain as a source. Run it for the user's domain and for the competitors that keep coming up.
- `get_serp_results`: the live Google top 20 for 1-10 queries, with each row's type, domain, title and URL. When Google served an AI Overview, its row carries the answer text and the pages it cites; People also ask questions come back too. Use it to see what the Overview says and whether the site is among its sources.
- `get_ai_brand_visibility`: how often ChatGPT and Google's AI answers mention the brand, with AI search volume per platform, share of voice against competitors, the questions that bring the brand up and the sources those answers cite. Paid plans; uses the project's market.
- `ask_ai_models`: asks ChatGPT, Claude, Gemini and Perplexity one question with web search on and returns each answer, whether it names the brand, the pages it cites (flagging the brand's own) and the searches it ran. Paid plans; one of the larger calls, so ask before running it on many questions.
- `get_ai_brand_tracking`: the project's tracked AI share of voice over time, if tracking is set up on the Brand Lookup page. Free to read.
- `get_search_console_performance`: the question-style queries the site already earns impressions for, and the pages that earn them. Use it to find questions where the site ranks but may not be the source the answer cites.
- `get_keyword_metrics`: volume, KD and intent for the buyer questions, to rank them by how much demand sits behind each.
- `run_site_audit`, `get_audit_status`, `get_audit_issues`: crawl the site for problems that stop any crawler, including AI crawlers, from reading pages: blocked pages, noindex, broken links, thin content.
- `create_share_report`: publish the finished work as a read-only page at a shareable link (see "Shareable report" below). Only after the user agrees.

Without a paid plan, `get_ai_brand_visibility` and `ask_ai_models` are refused: then ask the assistants by hand (step 4) and point the user to Brand Lookup and Prompt Explorer in the app. Read `robots.txt` with your own web fetch.

## Workflow

If the project's SEO folder has `seo-context.md`, read it first for the site, market, audience, competitors and goals; otherwise ask only what this workflow needs.

1. Measure what AI already sends. Call `get_ai_referral_traffic` for the last 3 months with `compareTo` the previous period and `byLandingPage: true`. Report sessions, share of all traffic, key events by assistant, and the pages that receive the visits. If Google Analytics is not connected, say so, pass on the connect link, and continue.
2. Build the question set. Start from the user's list, then add question-style queries from `get_search_console_performance` (queries starting with how, what, which, best, vs, cost) and comparison queries that name a competitor. Confirm 5 to 15 questions with the user. Call `get_keyword_metrics` on them and order by business fit, then volume.
3. Check Google AI Overviews. Call `get_ranked_keywords` with `resultTypes: ["ai_overview_reference"]` for the user's domain and up to three competitors. List the questions where a competitor is cited and the site is not. Call `get_serp_results` on the top questions to read each AI Overview and the pages it cites, and which pages rank organically.
   Then call `get_ai_brand_visibility` for the brand: report its mentions per platform, its share of voice against the competitors it returns, and the questions and sources that bring the brand up. If the project tracks AI visibility, add the trend from `get_ai_brand_tracking`.
4. Sample the AI assistants. On a paid plan, call `ask_ai_models` for the three to five most important questions (say the count first). Otherwise, with the user or with your own web tools if you can reach them, ask each question in ChatGPT, Perplexity, Claude and Gemini. Record, per answer: whether the brand is named, which competitors are named, and which sources are cited or linked. Note the date and that answers vary between runs and users. Report it as a sample, never as a ranking or a share-of-voice figure.
5. List the sources cited instead of the site. Group them: competitor pages, review and comparison sites, directories, forums such as Reddit, news and industry publications, Wikipedia. Read the most cited ones and note what they say that the site's pages do not: a clear one-line answer, a number, a comparison table, a named recommendation.
6. Check crawler access. Read `https://<domain>/robots.txt` and report, for each of GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot and Google-Extended, whether it is allowed or blocked. Blocking Google-Extended does not remove the site from AI Overviews, which use Google's normal index; say so if the user asks. Run `run_site_audit` if no recent audit exists, and report blocked, noindex or broken pages among the pages that should be cited.
7. Check the pages that should be cited. For the page that targets each question, read it and check:
   - The question is answered in the first two or three sentences, in plain words, before any background.
   - Facts are stated as facts: prices, specs, dates, locations, counts, with a source or a date.
   - Comparisons use a table, and "X vs Y" or "best for" questions get their own section or page.
   - Real questions buyers ask have short, direct answers on the page; FAQ blocks hold only questions that are actually on the page.
   - Schema fits the page (Organization, Product, LocalBusiness, Article, FAQPage only for visible questions) and names the brand the same way everywhere.
   - The brand, what it does and who it serves are stated consistently on the site and on its main profiles.
8. Plan the off-site work. For the third-party pages that AI answers cite most, list which ones the brand could appear on: a listicle that could include it, a directory or review site profile to claim or complete, a comparison page to send corrected facts to, a forum thread where an honest answer from the company fits the rules.
9. Prioritize the changes: crawler or indexing blocks first, then answer-first rewrites of pages that already rank for the questions, then new comparison or answer pages for questions with no page, then third-party presence.

## Output format

Start with:

- **Verdict:** one or two sentences, for example "AI assistants sent 140 visits last quarter, up from 60, mostly from ChatGPT to the pricing page; Google AI Overviews cite two competitors for 9 of 12 buyer questions and the site for none."
- **Top 3 changes**, in order.

Then include:

| Question | AI Overview shown | Site cited in AI Overview | Named in sampled assistants | Sources cited instead |
| -------- | ----------------- | ------------------------- | --------------------------- | --------------------- |

Then the AI assistant traffic table (assistant, sessions, key events, top landing page), the crawler access list, the page checklist per question, and the off-site targets with the reason each one matters. Close with what was not checked and the date of the assistant sample.

- **Next workflow:** end with one recommended next workflow, the reason for it, and the input it starts from. Default: `content-brief` on the highest-value question where a competitor is cited and the site is not, to write the answer-first page. If most cited sources are third-party lists and review sites, recommend `link-prospecting` on those pages instead. If crawling or indexing blocks the pages, recommend `seo-audit` on the domain first.
- **Check back:** end with one dated follow-up: the date (today plus 30 days, written out, for example "Monday, November 9") and the exact question to ask then: "Is <brand> showing up in AI answers for our buyer questions yet?" Say in one line why it needs that wait: AI answers pick up changed pages only after they are recrawled and reindexed, which takes weeks, and the AI assistant traffic re-check costs about 10 credits. Add it to the `Follow-ups` list in the SEO folder's `README.md` (create the list if it is missing) so the next session finds it. One follow-up only; don't add reminders or repeat it. If scheduled tasks are available (Cowork and the Claude apps on paid plans), offer once to make this a weekly scheduled task instead, named for the site, so the check runs by itself; the user reviews and confirms the schedule.
- **Where the output goes:** the report as `ai-search/<domain>-<YYYY-MM-DD>.md`, with the question table as `ai-search/<domain>-<YYYY-MM-DD>.csv`. Save it in the project's SEO folder (see `seo-project-setup`); if there is none, ask once whether to create one or where to save instead. If the user prefers a doc or a sheet and a docs or spreadsheet tool is available, put reports in a doc and tables in a sheet instead. Tell the user where it was saved.
- **Shareable report:** once the work is done, offer one time to publish it as a shareable report with `create_share_report`: a read-only page at a link the user can send to a client, a boss or a teammate, no sign-in needed. Write it from this output: findings first, then next steps, then the supporting table. Publish only after the user says yes, and leave out their Search Console and Google Analytics numbers unless they agree to share them. Give them the link; `delete_share_report` removes it.

## Guardrails

- Do not invent metrics. If HarborRank does not return a value, write `unknown`. Never give an "AI visibility score" or a share-of-voice percentage from a handful of sampled answers; report share of voice only as `get_ai_brand_visibility` or `get_ai_brand_tracking` return it.
- Label every answer from ChatGPT, Perplexity, Claude or Gemini as a sample from one date. Answers change between runs, accounts and locations.
- Do not claim a change will get the site cited. Say it makes the page easier to find, read and quote.
- Do not recommend writing for AI instead of for people, keyword stuffing, hidden text, fake reviews, or posting promotional answers on forums. Third-party presence must be earned and disclosed.
- Do not tell the user to block or allow AI crawlers without explaining the trade-off: blocking keeps content out of those assistants' answers and their citations.
- Recommend changes, never make them. Ask before any write action.
