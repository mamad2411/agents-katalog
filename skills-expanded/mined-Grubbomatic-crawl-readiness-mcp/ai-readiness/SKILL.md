---
name: ai-readiness
description: Check whether AI crawlers (GPTBot, ClaudeBot, PerplexityBot, Google's and 50+ more) can read a website and what its access policy allows, generate the files that fix what is blocked, read the Answer Analysis, and check whether a page permits an AI use. Use when a user asks whether AI can read their site, how to make it readable, or whether a page may be used for search, answers, training or an agent.
---

# Readable by AI, with the Crawl Readiness tools

The `crawl-readiness` MCP server gives you nine tools that call the live
service at www.crawlreadiness.com (the permission check at
machinereadiness.com, the standard's own host). Use them in this order.

## 1. Check first

Run `check_ai_readiness` with the site's address before advising anything.
Read the result like this:

- `score` (0–100) and `grade.status` are the headline. The score counts only
  the crawlers that fetch pages for AI search and answers (OAI-SearchBot,
  ChatGPT-User, Claude-SearchBot, PerplexityBot and the rest). Blocking
  training-only crawlers such as GPTBot, ClaudeBot, CCBot or
  Applebot-Extended costs no points; say so if the user asks about them.
- Fixes marked `extra: true` are "Going further" items (llms.txt, agents.json,
  Content-Signal, a markdown copy, forms tagged for agents). They never change
  the score. Present them as optional.
- `grade.status` "Restricted by Design" means the site blocks AI crawlers on
  purpose. That is a choice, not a failure; do not tell the user to "fix" it
  unless they want AI to read the site.
- "Partly Checked" means the homepage could not be read (often a firewall or
  CDN answering our crawler with a 403). Run `check_content_parity` to see
  what each AI crawler's user agent actually receives.

## 2. Explain, then fix

- For robots.txt questions, run `validate_robots` and quote the exact lines
  at fault.
- For structured data, run `validate_schema` and name the missing or invalid
  types.
- The three generators (`generate_llms_txt`, `generate_robots_txt`,
  `generate_schema`) need the Crawl Readiness API key configured in the
  plugin's settings (free from https://www.crawlreadiness.com/dashboard).
  If a generator answers that the key is missing, tell the user where to get
  one and to set it in the plugin configuration. Never ask them to paste a
  key into the conversation.
- When the user asks you to apply a fix to their project, show the generated
  file and where it will go before writing it. Merge into an existing
  robots.txt rather than replacing it; `generate_robots_txt` can take the
  existing file and merge the AI policy in.

## 3. Monitor, when they have projects

`get_monitor_trend` reads the user's Answer Analyses; it never starts a
run. Each result is labelled by how it was measured: live search (Perplexity,
Google AI Overviews) or model knowledge (ChatGPT, Claude, from their APIs).
Say which is which when you report a number, and treat a single run as a
sample, not a verdict.

## 4. Permission, before using a page

`check_permission` asks whether a page may be used for one purpose:
`search`, `answer` (including retrieval for RAG), `train` or `agent`.
Run it before fetching pages for a dataset, an index or an agent action, and
when the user asks whether they may use, quote or train on a page.

- `verdict` is conservative on purpose. `denied` means at least one
  published signal reserves the use. `allowed-under-terms` means an RSL
  licence permits it on the conditions in `terms`. `allowed` means only
  that nothing reserves the use, which is not a licence. `unknown` means
  a source that could carry a reservation could not be read (robots.txt
  answered 401 or 403, the page refused the request, a licence could not
  be fetched); say "unknown", never "allowed".
- `signals` lists every source read (robots.txt, Content-Signal,
  Content-Usage, RSL, TDM, ai.txt, the page's own tags) with what it
  decided. Quote the one that decided the verdict.
- `observed` is only there when you asked with `observe: true`: how the
  server treated a representative crawler's user-agent string sent from
  Crawl Readiness's servers, not what the real crawler gets. A `denied` with
  `served` is still `denied`; never treat serving as permission.
- `receipt` is a dated, signed record of all of this. Offer to keep it when
  the user may later need to show what the site published on that date.
- It is a reading of published signals, not legal advice. Say so when the
  user is deciding what to do with the answer.

## What to avoid

- Do not promise rankings or traffic. The check measures access and the
  signals AI systems use to understand a page; the methodology at
  https://www.crawlreadiness.com/methodology lists what it deliberately does
  not measure.
- Do not re-run the same check repeatedly in one conversation; anonymous use
  is rate limited, and the result does not change in minutes.
