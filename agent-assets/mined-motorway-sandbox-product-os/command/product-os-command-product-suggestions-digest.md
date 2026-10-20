<!-- owner: shared | audience: all-pms | last-updated: 2026-03 -->
<!-- purpose: Monthly digest of top product suggestions from {your-suggestions-channel} (FeatureOS) — ranked by votes with historical mention counts -->

# Product Suggestions Monthly Digest

Generate a monthly digest of the most popular product suggestions from the {your-suggestions-channel} Slack channel (FeatureOS integration). Ranks suggestions by votes, includes historical mention counts, and posts a summary to {your-pm-channel}.

## Instructions

### Step 1: Read product suggestions from Slack

1. Load Slack tools using ToolSearch
2. The {your-suggestions-channel} channel ID is `{your-channel-id}`
3. Read the full channel history using slack_read_channel with `limit: 100`. Paginate with cursor if needed — you want the complete history to count all historical mentions
4. Also search using slack_search_public:
   - `in:product-suggestions after:{30-days-ago-date}` for recent activity
   - `in:product-suggestions` broadly for historical context
5. The channel is fed by a FeatureOS bot:
   - `:sparkles:` = new suggestion posted (includes title, description, category, poster name)
   - `:thumbsup:` = upvote on existing suggestion (includes voter name and suggestion title)
   - Thread replies = discussion and comments on suggestions
6. For each unique suggestion, extract:
   - Title/name
   - FeatureOS URL
   - Category (e.g. "3. Product - B2B experience")
   - Who posted it and when
   - Description (from the :sparkles: post)
   - Total vote count (count of :sparkles: + :thumbsup: messages for that suggestion)
   - Total historical mentions (votes + thread replies + status changes)
   - All unique upvoters
   - Any status changes (e.g. "Planned", "In progress")
   - Any notable thread discussion

**Important:** Two FeatureOS URLs that differ only by a typo in the slug may be the same suggestion — merge them. Similarly, separate posts about the same underlying problem should be noted as related.

### Step 2: Rank and analyse

1. Rank all suggestions by total votes (descending)
2. Identify the top 20
3. For each of the top 10, write a detailed summary including why it matters
4. Categorise suggestions into themes (User experience, Admin experience, Platform tools, etc.)
5. Note which suggestions had activity in the past 30 days vs older
6. Flag any suggestions that have been actioned (status changes)

### Step 3: Save the digest

Write the full digest to `insights/` with filename `product-suggestions-monthly-digest-YYYY-MM.md` (current month).

Use this format:

```markdown
# Product Suggestions Monthly Digest — {Month Year}

**Period:** {start date} - {end date}
**Source:** {your-suggestions-channel} Slack channel (FeatureOS integration)
**Generated:** {today's date}

## Summary

{Brief overview: how many new suggestions this month, how many upvotes, overall channel activity level}

---

## Top 20 Product Suggestions (by historical channel votes)

| Rank | Suggestion | Votes | Historical mentions | Category | Latest activity |
|------|-----------|:-----:|:-------------------:|----------|----------------|
| 1 | {title} | {n} | {n} | {category} | {month year} |
...

---

## Top 10 — Detail

### 1. {Title}
**Votes:** {n} | **Historical mentions:** {n} | **Posted by:** {name} ({date})
**Upvoters:** {list}

{Description}

**Why it matters:** {Analysis}

---

(repeat for top 10)

## This month's activity ({date range})

| Date | Activity | Suggestion |
|------|----------|-----------|
...

## Category breakdown

| Category | Suggestions | % of top 20 |
|----------|:-----------:|:-----------:|
...

## Notable patterns

- {Key observations}
```

### Step 4: Post to Slack

1. The {your-pm-channel} channel ID is `{your-channel-id}`
2. Send a summary to {your-pm-channel} using slack_send_message

**Slack formatting rules** (critical — the Slack API rejects invalid formatting):
- Do NOT use emoji shortcodes — these cause `invalid_blocks` errors. Use Unicode emoji or plain text instead
- Do NOT use markdown tables — Slack mrkdwn does not support tables. Use numbered lists instead
- Keep the message under ~4000 characters

Use this Slack mrkdwn format:

```
*Product Suggestions Monthly Digest — {Month Year}*
_{date range} | Source: {your-suggestions-channel} (FeatureOS)_

{Brief summary of this month's activity}

*Top 10 Product Suggestions*
1. *{title}* — {votes} votes, {mentions} mentions ({category})
2. *{title}* — {votes} votes, {mentions} mentions ({category})
...

*This month's highlights:*
- {highlight 1}
- {highlight 2}
- {highlight 3}

_Votes = FeatureOS new post + upvote notifications in Slack. Actual FeatureOS votes may be higher. Full top 20: insights/product-suggestions-monthly-digest-{YYYY-MM}.md_
```

### Step 5: Notify the user

Tell the user:
- The message has been posted to {your-pm-channel}
- Show the file path of the full digest
- Highlight any notable changes from the previous month's digest (if one exists)

## Important Notes

- Count votes precisely — each :sparkles: and :thumbsup: bot message counts as 1 vote
- "Historical mentions" includes votes + thread replies + status changes — a broader engagement measure
- Merge duplicate FeatureOS URLs (typo variants) into a single suggestion
- Note suggestions that are related to each other (e.g. multiple posts about phone verification)
- Be transparent about methodology limitations — the 100-message Slack window may not capture all historical activity
- Use UK English and UK date format throughout
- Don't speculate — report what was suggested and how much support it received
