---
name: Launch
description: Build the full distribution system for a product. Use when the product is ready and you want to tell people it exists. Generates the channel list, phases, per-channel post drafts, attributed links, and execution board in one session. Works with or without a PM tool.
---

# /launch

Use this when the product is ready and you need to tell people it exists. Not for thinking about whether to launch. For building the system that gets it in front of the right people.

---

## Which surface are you on?

**Claude Code**
Read the product's spec first, wherever it lives (project root, `specs/`, a PM tool). Outputs go to one place only — see "Where outputs live" below.

**claude.ai chat**
Ask for the product description and audience if not already in context. Return all outputs inline, copy-ready. Tell the user exactly what goes where.

**Cowork**
Read the spec first. Save outputs to the product's growth folder, or to the PM tool if one is connected.

---

## Where outputs live

Detect, don't ask.

Look for signals in this order:

1. An MCP for a PM tool is connected (Notion, Linear, Jira, GitHub Projects). Use it.
2. The user's CLAUDE.md or profile names a PM tool as their source of truth. Use it.
3. Neither. Fall back to a `launch/` folder with plain markdown files.

If the setup is ambiguous (e.g. both a `launch/` folder exists and an MCP is connected), prefer the PM tool and say so in one line: *"Saving to Notion since that's your source of truth."*

One or the other, never both.

---

## Before you start

Read the spec, the user's profile, and the execution board (if any) first. Most answers are already there: audience, voice, previous channels, constraints.

Only ask what the environment cannot tell you:

1. **Trigger type** — warm launch (audience exists) or cold launch (starting from zero)?
2. **Publish date** — when does the anchor post go live?
3. **Hard constraint** — time budget per day, off-limit channels, quiet period, anything else that shapes the plan.

If any of these are already implied in the spec, skip that question.

---

## Step 1: Channel audit

List every channel that fits the product and audience. For each one:

- **Platform** (Reddit, Discord, X, LinkedIn, Substack, email, YouTube, podcast, etc.)
- **Type** — community, person, or owned channel
- **Phase** — 1, 2, 3, or 4
- **Angle** — what to lead with on this specific channel
- **Attributed link** — `baseurl.com?src=channel_name`

Use consistent `?src=` naming:

- Subreddits — `r_<subredditname>`
- Discord — `discord_<servername>`
- Owned channels — `x_post`, `linkedin_essay`, `substack_newsletter`
- DMs — `dm_<personname>`

**PM tool connected** — create a Distribution Channels database (or add to an existing one). Properties: Name, Platform, Type, Audience, Phase, Angle, Handle/Link, Attributed link, Status, Notes. Views: By Phase (board), People Only (filtered), By Platform (grouped).

**No PM tool** — write `launch/channels.md` with the same information as a table.

---

## Step 2: Phase plan

Phase shape depends on the trigger type.

**Warm launch** (audience exists):

- Phase 1 — Ship the anchor post to owned and warm channels. Email, Substack, LinkedIn, X. Tell the people who already know you.
- Phase 2 — Cross-post to aligned communities. Start DMs with a genuine ask.
- Phase 3 — Cold expand. Ship one artifact (PDF, cheat sheet, strong-opinion post). Pitch one guest placement.
- Phase 4 — Amplify the highest-converting channel. Decide pricing. Publish the retrospective.

**Cold launch** (starting from zero):

- Phase 1 — Join rooms, introduce yourself, lurk. Build the channel list and write drafts. No posting yet.
- Phase 2 — Post to owned channels once set up. Begin posting in communities where you have presence.
- Phase 3 — Cold expand. Same as above.
- Phase 4 — Same as above.

One week per phase is a reasonable default. Adjust based on the constraint.

---

## Step 3: Post drafts

For every channel in Phase 1 and Phase 2, write the actual post. Ready to copy and paste.

Every post needs:

- Title (Reddit) or opening line (X, LinkedIn, Discord)
- Full body
- Attributed link embedded
- Rules for posting: timing, subreddit conventions, what not to do

Voice rules that always apply:

- Lead with the problem, not the product.
- No em dashes.
- No importance inflation. No "game-changing," "revolutionary," "the one thing that."
- One version per platform. Never cross-post the same copy.
- Non-technical audience: lead with the human story.
- Builder audience: lead with the insight or the system.

Where drafts go:

- **PM tool connected** — in the body of the channel's page, or as a linked execution ticket.
- **No PM tool** — `launch/posts/<platform>-<channel>.md`, one file per channel.

---

## Step 4: Execution board

One ticket per task, tagged by Phase.

**PM tool connected** — create or extend an Execution Tickets database. Views: All Tasks (table), Kanban by Status (board), By Phase (grouped).

**No PM tool** — `launch/board.md` with a simple table.

Pre-populate Phase 1 tasks based on the trigger type.

**Warm launch Phase 1 tasks**

- Ship the anchor post to Substack or owned blog
- Share it on LinkedIn
- Share it on X
- Email it to the warm list
- DM five people with a genuine ask

**Cold launch Phase 1 tasks**

- Join the five most aligned communities
- Introduce yourself in two of them
- Lurk and learn the culture
- Write five DM templates
- Wire attribution tracking before any post

---

## Attribution

Before the first post goes live, attribution tracking must be in place on the target URL. Confirm it exists. If not, either:

- Create a short `attribution.js` for static sites. Reads `?src=` into localStorage, injects into any form submit.
- Point the user to their analytics tool (Plausible, Fathom, PostHog, Google Analytics) and show them how to configure `src` as a tracked dimension.

---

## Done when

- Channel list exists (in PM tool or `launch/channels.md`).
- Phase plan matches the trigger type.
- Post drafts written for every Phase 1 and 2 channel.
- Attributed links generated and ready to paste.
- Attribution tracking live on the target URL.
- Execution board created with Phase 1 tasks populated.
- Anchor post written and ready to publish.
