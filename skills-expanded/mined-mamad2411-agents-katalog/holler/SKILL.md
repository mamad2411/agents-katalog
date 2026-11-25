---
name: holler
description: >-
  Research contacts, draft per-platform outreach (X, LinkedIn, email), and fill
  campaigns through the Holler MCP server, writing messages that read like a real
  person wrote them. Use whenever you are connected to the Holler MCP (tools like
  create_campaign, upsert_contact, add_to_campaign, list_contacts) or are asked to
  do outreach, build a holler/campaign, find people to reach, or draft cold
  messages for X, LinkedIn, or email.
metadata:
  homepage: https://holler.sh
---

# Holler outreach

Holler is an outreach tool. The human sets a goal ("get 20 AI founders in NYC to
try our beta"), and you, the agent, do the legwork through the Holler MCP server:
research the right people, add them as contacts, and draft a message for each one
tuned to the platform you would send it on. The human reviews everything in the
Holler web app and presses send themselves. You never send anything; you fill the
campaign so every contact is ready to reach.

Two things make outreach land, and this skill covers both:

1. **Use the MCP server correctly** so the data is clean and nothing gets
   duplicated or rejected. See `references/mcp-tools.md`.
2. **Write like a human, not a bot.** A campaign full of "I hope this email finds
   you well" templates is worse than no campaign. See `references/writing-outreach.md`.

## The workflow

Do this end to end for a campaign:

1. **Understand the goal.** If the human has not given you one, ask: who are they
   trying to reach, and what is the ask? The goal drives every message.
2. **Create the campaign** with `create_campaign` (title + goal). Or use an
   existing one: `list_campaigns`, then `get_campaign` to see who is already in it.
3. **Find the right people.** Research real, specific people who fit the goal. For
   each, you need at least a name and one way to reach them (X handle, LinkedIn
   URL, website, or email).
4. **Check for existing contacts** with `list_contacts` before creating new ones,
   so you enrich rather than duplicate.
5. **Add each contact** with `upsert_contact`. Always write a `blurb`: one or two
   sentences on who they are and the specific hook you will use to reach them. The
   blurb is your research note to yourself; good drafts depend on it. **If the
   contact is a business (a company, agency, studio, store, or brand) rather than a
   single person, always add their website.** For a business the website is the
   primary identifier and often the best research hook, so do not save a business
   contact without it; track down the real homepage before moving on.
6. **Draft and attach** with `add_to_campaign`. For every contact you write three
   variants (X, LinkedIn, Gmail) plus a Gmail subject, and pick the
   `recommendedPlatform` (where this person is most reachable). The recommended
   platform MUST match a link the contact has.
7. **Report back** to the human: how many contacts you added, who they are, and
   anything you were unsure about. Then they review and send from the web app.

## Rules that matter most

Read the references for the full picture, but never violate these:

- **No template smell.** If you could send the same message to anyone on the list
  by swapping the name, rewrite it. Every message needs a specific reason it was
  sent to *that* person.
- **Lead with them, not you.** The first line earns the second. Open on something
  true and specific about them, not on who you are.
- **One ask, low friction.** Make it easy to say yes. A reply, a quick look, a
  15-minute call. Not three asks stacked together.
- **Match the platform.** An X DM is not a cold email. Short and peer-to-peer on
  X, warm and professional on LinkedIn, a little more structured over email. Never
  paste the same text into all three variant fields.
- **Never use em dashes.** Not in any message, subject line, blurb, or campaign
  copy. Em dashes (the long ones) are the single clearest AI tell. Use a comma, a
  parenthesis, or split the sentence in two. This is a hard rule, no exceptions.
- **Cut the corporate and AI tells.** No "I hope this finds you well," "I wanted
  to reach out," "circle back," "synergy," "excited to connect," "in today's
  fast-paced world." Drop empty intensifiers like "genuinely," "truly," and
  "incredibly." Use contractions. Vary sentence length.
- **Recommend where they actually are.** `recommendedPlatform` should be the
  channel this person is most likely to read, and it has to match a link you saved
  on the contact.
- **Businesses always get a website.** If the contact is a company or brand rather
  than a person, save its website. It is the primary link for a business and the
  best source of a real hook.

## When you are missing information

- No reachable link for a person you found: keep researching for a handle, profile,
  or email, or drop them. A contact with no link cannot be the recommended platform.
- No campaign goal: ask the human before drafting. Generic goal, generic messages.
- Unsure a person is a real fit: tell the human in your summary rather than padding
  the list. Quality of fit beats count.
