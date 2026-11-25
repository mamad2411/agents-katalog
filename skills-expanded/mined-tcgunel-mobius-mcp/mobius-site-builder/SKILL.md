---
name: mobius-site-builder
description: Build, populate and rewrite a Sweipe or FlatMobile WordPress site from a plain-English brief through the mobius-mcp tools (demo import, AI plan → build → review loop, per-page copy rewrite, core settings).
---

# Sweipe site builder

You are working on a WordPress site that runs the Sweipe theme (or its FlatMobile
flavor) with the Sweipe Companion plugin 1.2.1 or newer. The `mobius-mcp` server gives
you tools that drive the plugin's own site builder. The AI work (planning, copywriting,
photo selection, review) runs on the theme's service and is paid for by the site's
licence in credits; you never need an API key.

## Before anything

1. Call `sweipe_status`. Check:
   - `license.is_valid` is true. If not, stop and tell the owner to activate the purchase
     code under Sweipe → License. Nothing below works without it.
   - `ai.enabled` and `ai.configured` are true; `ai.blocker` is null. If AI is off, ask
     before calling `sweipe_ai_set_enabled` (it is the owner's switch).
   - `plan` tells you whether a site was already planned or built. Do not plan again on
     top of a built site without asking; the builder never overwrites existing pages,
     so a second build adds pages next to the first ones.
2. Call `sweipe_ai_ping` once to see the credit balance. A full site costs about 12
   credits; a page rewrite 1. Say how many credits a job will use before you spend
   more than 10, and stop when `credits.left` cannot cover the next step.

## Two ways to get a site

**From a demo (no credits).** `sweipe_list_demos`, pick the closest package, then
`sweipe_import_demo` with its slug. The import takes one to a few minutes and the tool
waits for it. WooCommerce demos need WooCommerce active first (`sweipe_status` →
`site.woocommerce`). Afterwards rewrite the copy for the business (next section).

**From a brief (about 12 credits).** Write a brief of three to six sentences: what the
business is, where, who it serves, what the site must do (sell, book, inform), tone.
Then either:

- `sweipe_site_from_brief` for the whole loop in one call (plan → build → review →
  rebuild → fix review), or
- step by step when the owner wants a say: `sweipe_ai_library` to see the templates,
  `sweipe_ai_plan` (1 credit) to get a plan, show the pages and sections to the owner,
  edit the plan object if asked (page titles, slugs, drop or reorder sections; section
  ids come from the library and must stay as they are), `sweipe_ai_build` (4 credits,
  imports and waits), `sweipe_ai_review` in `full` mode (5 credits). If the review
  reports `changed: true`, build again and review with `mode: "fix"` (2 credits, free
  when nothing is broken). Two rounds are enough; do not loop further.

The build writes copy from the brief and picks stock photos. Report the review score
and summary to the owner in plain words, with the page links from `sweipe_status`
(`site.url`) plus the page slugs.

## Rewriting copy on existing pages

`sweipe_brief_pages` lists every page and post with the number of text items each has.
Id 0 is the site identity (title, tagline, menu labels).

For each page the owner wants rewritten: `sweipe_brief_generate` (1 credit per page)
returns draft rows with `old` and `new` text. Show a few of them. Only then
`sweipe_brief_apply` with the page ids. Pass edited rows in `items` if the owner
changed something. `sweipe_brief_undo` restores the pre-apply backup at any time.
Legal pages (privacy, terms, refunds) should not be rewritten by AI; leave them out
unless asked.

## Settings

`wp_get_settings` / `wp_update_settings` change the site title, tagline, timezone,
language and front page. Set the timezone and language to match the business as part of
any build. `wp_list_pages` finds page ids for `page_on_front` / `page_for_posts`.

## Rules

- Never claim a step succeeded from the plan alone; read the tool result. Imports
  report `status: "complete"`; builds report `import.status`.
- Sends nothing to third parties beyond the theme's own service; do not paste the
  Application Password anywhere, it lives only in the server's environment.
- One site at a time. Imports hold a lock; if `sweipe_import_demo` fails with "already
  in progress", check `sweipe_import_status` and wait.
- If a tool returns `HTTP 402`, the month's credits are used up; report the reset date
  from the message and stop AI calls. `HTTP 403` from the AI tools means the licence is
  blocked; tell the owner to contact Mobius Studio.
