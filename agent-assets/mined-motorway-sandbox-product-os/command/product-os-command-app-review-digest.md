<!-- owner: shared | audience: all-pms | last-updated: 2026-03 -->
<!-- purpose: 30-day rolling app review digest from {your-reviews-channel} Slack channel — top positive/negative themes with quotes and links -->

# App Review Digest

Generate a rolling 30-day digest of app reviews from the {your-reviews-channel} Slack channel. Surfaces the top positive and negative themes to help the team prioritise fixes.

## Instructions

### Step 1: Read app reviews from Slack

1. Load Slack tools using ToolSearch
2. The {your-reviews-channel} channel ID is `{your-channel-id}`
3. Calculate the Unix timestamp for 30 days ago from today
4. Read messages from {your-reviews-channel} using slack_read_channel with `oldest` set to the 30-days-ago timestamp. Use `limit: 100` and paginate with the cursor if needed to get all messages in the window
5. Also search using slack_search_public with `in:{your-reviews-channel} after:{30-days-ago-date}` to catch reviews in rich attachments. Try multiple searches:
   - `in:{your-reviews-channel} after:{date}` (general)
   - `in:{your-reviews-channel} star after:{date}` (star ratings)
   - `in:{your-reviews-channel} review after:{date}`
6. Extract review content: star rating, review text, reviewer name (if available), date, platform (App Store / Google Play), and the Slack message permalink

**Important:** Many reviews are posted by bots as rich attachments with empty text fields. Use both slack_read_channel and slack_search_public to maximise coverage. Note how many messages were in the channel vs how many had extractable review content.

### Step 2: Categorise into themes

From all collected reviews, identify themes. Analyse every review and assign it to one or more themes.

**Positive themes:** Identify the **top 3** positive themes by volume.
**Negative themes:** Identify the **top 5** negative themes by volume.

For each theme provide:
- A clear, descriptive theme name
- The number of reviews that align with this theme (exact count)
- Whether it is positive or negative
- 2-3 direct customer quotes with attribution (reviewer name if available, date, star rating)
- Slack message permalinks for the quoted reviews so the team can click through

Common themes to watch for (don't limit to these):
- **Positive:** Easy/simple process, fair valuation, fast payment, helpful staff, better than alternatives, good communication
- **Negative:** Onboarding friction, pricing confusion, poor communication/updates, app bugs/UX issues, collection delays, customer support responsiveness

### Step 3: Save the digest

Write the full digest to `insights/qual/cx-analysis/` with filename `app-review-digest-YYYY-MM-DD.md` (today's date).

Use this format:

```markdown
# App Review Digest — {date range, e.g. 12 February – 13 March 2026}

**Source:** {your-reviews-channel} Slack channel
**Total messages in window:** {count}
**Reviews with extractable content:** {count}
**Platforms:** App Store, Google Play

---

## Top 3 Positive Themes

### 1. {Theme name} ({count} reviews)

{Brief description of what reviewers are saying}

> "{Quote 1}" — {Reviewer}, {date}, {star rating} ⭐ [View in Slack]({permalink})

> "{Quote 2}" — {Reviewer}, {date}, {star rating} ⭐ [View in Slack]({permalink})

### 2. {Theme name} ({count} reviews)

...

### 3. {Theme name} ({count} reviews)

...

---

## Top 5 Negative Themes

### 1. {Theme name} ({count} reviews)

{Brief description of what reviewers are complaining about}

> "{Quote 1}" — {Reviewer}, {date}, {star rating} ⭐ [View in Slack]({permalink})

> "{Quote 2}" — {Reviewer}, {date}, {star rating} ⭐ [View in Slack]({permalink})

> "{Quote 3}" — {Reviewer}, {date}, {star rating} ⭐ [View in Slack]({permalink})

### 2. {Theme name} ({count} reviews)

...

(continue for all 5)

---

## Summary

| Rank | Theme | Sentiment | Reviews | Key Quote |
|------|-------|-----------|---------|-----------|
| 1 | {name} | ✅ Positive | {count} | "{short quote}" |
| 2 | {name} | ✅ Positive | {count} | "{short quote}" |
| 3 | {name} | ✅ Positive | {count} | "{short quote}" |
| 1 | {name} | ❌ Negative | {count} | "{short quote}" |
| 2 | {name} | ❌ Negative | {count} | "{short quote}" |
| 3 | {name} | ❌ Negative | {count} | "{short quote}" |
| 4 | {name} | ❌ Negative | {count} | "{short quote}" |
| 5 | {name} | ❌ Negative | {count} | "{short quote}" |

## Methodology & Caveats

- Window: 30-day rolling period ending {today's date}
- Source: {your-reviews-channel} Slack channel only (bot-posted reviews from App Store and Google Play)
- {Note any extraction limitations — e.g. reviews in rich attachments that couldn't be parsed}
- Review counts are exact where content was extractable; some reviews may have been missed due to attachment formatting
- Themes are not mutually exclusive — a single review may appear under multiple themes
```

### Step 4: Draft Slack message

1. The {your-team-channel} channel ID is `{your-channel-id}`
2. Draft a summary to {your-team-channel} using slack_send_message_draft

Use this Slack mrkdwn format.

**Slack formatting rules** (critical — the Slack API rejects invalid formatting):
- Do NOT use emoji shortcodes — these cause `invalid_blocks` errors in `slack_send_message`. Use Unicode emoji or plain text instead
- Do NOT use markdown tables — Slack mrkdwn does not support tables. Use bullet lists instead
- Keep the message under ~4000 characters

```
*App Review Digest — {date range}*
{count} app experience reviews analysed from {your-reviews-channel} (30-day window)

*Top positive themes:*
1. *{Theme}* ({count} reviews) — "{short user quote}"
2. *{Theme}* ({count} reviews) — "{short user quote}"
3. *{Theme}* ({count} reviews) — "{short user quote}"

*Top negative themes:*
1. *{Theme}* ({count} reviews) — "{short user quote}"
2. *{Theme}* ({count} reviews) — "{short user quote}"
3. *{Theme}* ({count} reviews) — "{short user quote}"
4. *{Theme}* ({count} reviews) — "{short user quote}"
5. *{Theme}* ({count} reviews) — "{short user quote}"

_Full digest with all quotes and links: insights/qual/cx-analysis/app-review-digest-{date}.md_
```

### Step 5: Notify the user

Tell the user the draft is ready for review in {your-team-channel} and show them the file path of the full digest.

## Important Notes

- Only include actual customer reviews, not internal comments, bot status messages, or team discussions
- Count reviews precisely — the whole point is to show the team the volume behind each theme
- Every quoted review must include a Slack permalink so the team can click through to the original
- Be transparent about extraction limitations — note how many messages couldn't be parsed
- Use UK English and UK date format throughout
- Don't speculate about what themes mean — report what customers said
