---
name: hermoso-launch-app
description: >-
  Launch and market an app or site you just built, using Hermoso. Sets up the brand from the app, makes launch
  ads and posts, schedules them on the owner's own social channels and, if asked, builds paused ad campaigns.
  Use when the user says "launch this", "market my app", "get me users", "make launch posts", "promote what we
  just built", or finishes a build in an app builder (Lovable, Replit, Bolt, v0, Base44) and asks what is next.
  NOT for: building the app itself, or a single image from a prompt (use hermoso-generate).
argument-hint: "[the app's URL or one line about what it does, e.g. 'https://myapp.com, a habit tracker for runners']"
---

# Hermoso: launch the app you just built

You built something. This gets it in front of people: a saved brand, launch creative, a week of scheduled posts
and, only if the user asks, paid campaigns created paused.

## Before you start
- Hermoso has to be connected to this host as an MCP server (URL `https://app.hermoso.ai/mcp`, sign in once).
  If its tools are not available, send the user to https://hermoso.ai/connect/ and pick their host
  (Lovable, Replit, Bolt, v0 and Base44 each have a page with the exact clicks).
- In a terminal there is no MCP server to connect: the same tools run through the Hermoso CLI. Sign in once with
  `npx -y hermoso auth login` (opens a browser; nothing to paste). On a machine with no browser:
  `npx -y hermoso auth login --device --no-wait` prints a link and a short code; send both to the user, and once
  they approve run `npx -y hermoso auth login --device --resume`. No key needed. Only if nobody can open a link:
  `npx -y hermoso auth login --token <your key>`, using a key from app.hermoso.ai under **MCP & CLI**. Then
  `hermoso tools --search <what you want>` finds a tool, `hermoso tools <name>` prints its arguments and
  `hermoso call <name> --json '{...}'` runs it (after `npm install -g hermoso`, or prefix each with `npx -y`).
  No account at all? An agent can sign itself up on a paid plan with `POST /v1/signup` at app.hermoso.ai; see
  the Hermoso README.
- A tool you do not see in your list still exists: `find_tools` searches every Hermoso tool and `call_tool`
  runs any of them by name.
- The connector works while you build. It is not part of the published app, so never wire Hermoso calls into
  the app's own code unless the user asks for an API integration.

## The launch, in order
Do only the steps the user wants. Say what you are about to do before anything that spends credits or posts.

1. **Know the product.** Use what you already know from the build: what the app does, who it is for, its name,
   its live URL. Ask only for what is missing. One line is enough.
2. **Save the brand.** If the app has a public URL, call `draft_brand` with it so every ad matches the app's
   look and voice. No URL yet? Call `draft_brand` with a short description instead. `get_brand` shows what is
   already saved; do not draft twice.
3. **See what works in this market (optional, costs credits).** `find_competitors` then `research_ads`, and
   report the two or three hooks that keep showing up. Skip this if the user just wants posts.
4. **Make the launch creative.** Three is a good first set: a static launch ad, a carousel or second static
   with a different angle, and one short vertical video if the user wants video. `generate_image` and
   `render_ad` pick sound defaults when you do not name a model. Video takes a few minutes: read the job with
   `get_job` and never call it done before it finishes. Show the user each result.
5. **Check the channels.** `list_connectors` says which social accounts are connected. None connected is not
   an error: give the user the connect link from the tool result, or tell them to open Hermoso and connect
   the channels they want under Connectors. Do not post anywhere the user did not name.
6. **Schedule the week.** Show the exact caption and the exact account for each post and get a yes. Then
   `schedule_post`, one a day, at the times the user picks or mornings in their time zone. `list_scheduled`
   reads the queue back. Never rewrite or shorten a caption the user wrote.
7. **Paid ads, only if asked.** Campaigns are created paused on the user's own ad accounts and read back
   before you describe them. Turning one on is the user's decision, stated in their own words.
8. **Report.** What was made (with links), what is scheduled and when, what is waiting on the user (a channel
   to connect, a campaign to turn on), and the one thing to do next week: read what performed with
   `post_performance` and make more of that.

## Rules
- Nothing is published, scheduled or spent on ads without the user saying so in this conversation.
- If the free credits run out, say so plainly and stop. Do not swap in a cheaper version of what was asked.
- Use the app's real name, screens and URL. Do not invent features, prices, reviews or numbers for the ads.
