---
name: linkedin-posting
description: Draft and share LinkedIn posts through the LinkedIn plugin's MCP server — content structure, voice, the confirm-before-share workflow, and failure handling. Use when the user wants to write, improve, or publish a LinkedIn post.
---

# LinkedIn Posting

Read the `linkedin` skill first for connection and the hard rules. The two
that matter most here: **show the exact final text and get explicit
confirmation before sharing**, and **never re-share on a failure without
checking** — a timeout may still have published.

## Drafting

- **Length**: hard limit ~3,000 characters; only the first ~200 characters
  show before "…see more", so the first line must earn the click.
- **Structure that works**: one-line hook → short paragraphs (1-2 sentences,
  blank line between) → concrete specifics (numbers, names, lessons) → a
  closing question or clear takeaway. No walls of text.
- **Voice**: write in the user's voice, not marketing-speak. Pull phrasing
  from what they told you; when the post announces work done in this session,
  use the real details. Never invent metrics, claims, mentions, or hashtags.
- **Hashtags**: 0-3, at the end, only ones the user would plausibly use.
- **Links**: LinkedIn deprioritizes external links in the post body; if a
  link matters, mention it can go in the first comment and let the user
  decide.
- Offer 1-2 variants when the ask is open-ended ("write a post about X"):
  e.g. a story-led version and a direct announcement, then iterate on the one
  they pick.

## Share workflow

1. Draft, iterate until the user is happy.
2. Show the final text verbatim and ask for explicit confirmation to post.
3. Call the share tool once. Report the result (and the post URL if the tool
   returns one).
4. On error: report it plainly. Ask the user to check their feed before any
   retry — a timeout may still have published. On a 403, the connected app
   lacks the `w_member_social` grant; reconnect from Settings → MCP.

## What you cannot do

The connection posts to the member's own feed only. No commenting, liking,
reposting, DMs, company-page posting, scheduling, or reading engagement
metrics on past posts (partner-gated). If asked, say so and offer the manual
path (e.g. draft the comment text for the user to paste).
