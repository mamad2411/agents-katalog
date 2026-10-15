# Slack Community

Guidelines for posting in the [your-company] Slack community channel.

## MCP connectors

| Connector | Purpose |
|-----------|---------|
| Slack | Read community channels, draft responses |

## Tone

- Casual, helpful, brief
- Peer-to-peer, not corporate announcement
- Use plain language, no marketing speak
- Match the energy of the channel - read recent messages first

## What to announce

| Type | Example | Post? |
|------|---------|-------|
| New feature shipped | "Just shipped date range filters on dashboards" | Yes |
| Bug fix (user-reported) | "Fixed the CSV export timeout - thanks for flagging" | Yes |
| Content published | "New blog post on [topic] - link" | Yes, if relevant to community |
| Event | "Hosting a meetup in [city] on [date]" | Yes |
| Milestone | "Hit 100 connected warehouses this week" | Yes, keep it humble |
| Minor patch | Dependency bump, typo fix | No |
| Internal ops | Hiring, fundraising, internal process | No |
| Sales/marketing | Outbound campaigns, pricing changes | No |

## Cadence

- Max 2-3 posts per week in the main community channel
- Space announcements at least 1 day apart
- Don't post on weekends unless it's urgent
- Batch small updates into a weekly roundup if there are many

## Message format

- Lead with what changed, not the backstory
- One short paragraph, 2-3 sentences max
- Link to docs, blog, or changelog for details
- Use emoji reactions, not threaded announcements (keeps it casual)

## Guardrails

- **Draft first** - never post directly; save to `content/slack/_drafts/`
- **No customer names** in community posts
- **No pricing or commercial info** in community channels
- **No negative framing** - "fixed" not "was broken", "improved" not "was slow"
- **CAO or team reviews** before posting

## Self-improvement

After the CAO reviews and approves a Slack community post:

1. Move the final version from `content/slack/_drafts/` to `content/slack/_published/`
2. Diff what was drafted vs what the CAO kept - identify patterns in her edits to tone, format, or what she announces
3. Update `content/slack/_insights.md` with what worked, what she changed, and why (note community reactions)
4. If her edits reveal a new rule (e.g. "never announce features without a link to docs", "always tag the engineer who shipped it"), add it to the Message format or What to announce sections
5. If a post gets strong community engagement, save it to `content/slack/_examples/`
