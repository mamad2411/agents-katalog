---
name: augment-speakers-panelists
description: Turn a speaker or panelist's thin event-app bio (often a screenshot) into a usable profile through web research, in a fixed order — social accounts first, then features (coverage about or by them), then mentions (they're quoted or named), then video (usually YouTube) — capped at the most relevant and most recent. Use whenever someone shares a speaker card, session page, or agenda screenshot and asks "who is this?", "look them up", "augment this speaker", "find their socials", "what have they said publicly?", or "prep me for this panel"; and whenever an event workspace (event-hog) needs speaker profiles. Research-tool agnostic: it first resolves which tools this user and organization have (Firecrawl, Tavily, Origami, the client's own web search, or anything else) and uses those, in their order. Encodes identity-confirmation before any lookup, the feature-versus-mention distinction, relevance-then-recency selection, and the rule that only links actually retrieved get reported.
---

# Augment Speakers and Panelists

> **Status: Draft (2026-10-26).** Written for event-hog during the 7x24
> Exchange Fall Conference; not yet run end to end against a real speaker.

Event apps give you a name, a title, a company, and two lines of bio, usually
as a screenshot. Listening and taking notes at the same time is hard, so the
team needs to know who someone is before or during the session, fast. This
skill turns that thin bio into a short profile, in a fixed order:

1. **Social accounts**: where to follow up or reach them.
2. **Features**: coverage *about* them, or *by* them.
3. **Mentions**: they're quoted or named in a broader story.
4. **Video**: talks and interviews, usually YouTube.

## 0. Resolve the configuration first

The method here is the same for everyone. **Which research tools to use is
not.** One person has Firecrawl and Tavily, a team has Origami, another has
only the web search built into their chat app.

- **Connected to event-hog:** call `get_config` with
  `skill: "augment-speakers-panelists"`. It returns the organization's
  defaults merged with this person's overrides: `research_tools` (in order of
  preference), `limits`, and where results are saved.
- **Otherwise:** read `config/private.json` next to this file (shape in
  `config/private.example.json`).
- **If neither exists, ask once** which research tools the person has. If
  event-hog is connected, save the answer with `set_my_research_tools` so
  they're never asked again.
- **Use the tools in the order listed.** Fall back to the next one when a tool
  is missing, errors, or returns nothing useful. The client's built-in web
  search is always the last resort. Never refuse to start because a preferred
  tool isn't there.

Defaults when the configuration doesn't say: **10** features and mentions
combined, **5** videos, look back **3 years**.

## 1. Read the input and anchor the identity

From the screenshot or text, extract exactly what's shown: **name, title,
organization**, the **session or panel title**, its time and room, and any
bio lines. Don't fill gaps from memory.

**Confirm identity before researching.** Common names collide constantly
("Ryan Bernstein" is several people). The anchor is name + organization, plus
title or location when shown. Every result must match the anchor:
- **High:** the account or article names the same organization or role.
- **Medium:** same name and industry, organization not stated. Keep it,
  marked *(probable match)*.
- **Low:** same name only. Leave it out.

If the very first searches can't find **any** high-confidence match, say so
and ask before continuing. A confident profile of the wrong person is worse
than none.

## 2. Social accounts (first, always)

Look for, in this order: **LinkedIn**, **X/Twitter**, **Bluesky**, a
**personal site or newsletter** (Substack, Medium, blog), **GitHub** (for
technical speakers), a **YouTube channel**, **Mastodon or Threads**. Include
Instagram or TikTok only if they're clearly professional.

- Report only accounts you actually found and opened, or that a reliable page
  links to (their company bio, the event's speaker page). **Never construct a
  handle or URL from the name.**
- Confirm each one against the anchor: bio mentions the organization or role,
  or the company site links to it.
- No personal or family accounts, home addresses, or personal phone numbers,
  even if found. This is professional information only.

**Then the organization's accounts:** its **LinkedIn company page** and its
**X account** (plus YouTube if it posts talks). Posts about the session tag
both the speaker and the organization, so both need to be ready. Take them
from the organization's own site (footer links) or a confirmed search
result, never from a guess at the name.

## 3. Features, then 4. mentions

- **Feature:** the piece is *about* them or *by* them: an interview, profile,
  podcast episode with them as a guest, an op-ed or byline they wrote, a talk
  write-up centered on them, a company announcement that's mainly about them.
- **Mention:** they're quoted or named in a story about something else.

Search mainstream and trade press (for data centers and energy, for example:
Data Center Dynamics, Data Center Frontier, Utility Dive, trade association
sites), plus podcasts.

**Selection, when there are many:**
1. **Relevance to their session or panel topic first.** If they're speaking on
   AI-era power density, a 2025 interview on cooling beats a 2026 item about a
   promotion.
2. **Then recency:** newer first.
3. **Cap features and mentions combined** at the configured limit (default
   10). Features usually earn more of the slots, but a highly relevant recent
   mention can outrank an old feature.

For each item: **date, outlet, title, URL**, and **one line on why it
matters for this session**.

## 5. Video

Talks, panels, interviews, webinars: usually YouTube, sometimes Vimeo or the
event's own site. Same rules: relevance to the session, then recency, capped
(default 5). Include date, title, channel, URL, and length if shown.

## 6. Output, then save

Show a card readable on a phone, in this order:

```
**<Name>** · <Title>, <Organization>
Session: <title> (<day, time>)
Why they matter here: <one line>

Social: LinkedIn · X · …              (only what was found and confirmed)
Organization: LinkedIn page · X · …
Features (n): date · outlet · title — why it matters
Mentions (n): …
Video (n): …
Not found / not confirmed: <what you looked for and didn't find>
```

Then **save it**:
- **Connected to event-hog:** call `save_speaker_profile`. It writes
  `speakers/<name>.md` in the event workspace and records each link as an
  observation (`has_social`, `featured_in`, `mentioned_in`, `has_video`) with
  its URL as the source, tied to this event. Pass the organization's
  accounts as `organization_socials`; they're recorded on the organization. Saving the same person again
  adds to the profile instead of duplicating it.
- **Otherwise:** write the card to a markdown file where the user keeps
  event notes, with every URL kept.

## Discipline

- **Only report links you actually retrieved.** If a tool returns a snippet
  but the page wouldn't load, mark it *(not opened)*.
- **Say what you didn't find.** "No X account found" is information; silence
  is ambiguous.
- **Dates matter.** An undated item goes after dated ones and is marked
  *(undated)*.
- **Speed over completeness at the event.** If time is short, do social
  accounts and the 3 most relevant features first, save, and offer to finish
  later.
- **Speakers aren't contacts.** A profile doesn't mean the team has met them.
  Use `log_contact` only after a real conversation.

## See also

- `event-prep`: the prep map this enriches; speakers ranked there are the first to augment
- `crawl-fetch-ingest`: the deeper ingest workflow for firm and portfolio pages
- `lossless-crm-interface-guidelines`: provenance habits (fetch first, offer model knowledge rather than smuggling it in)
