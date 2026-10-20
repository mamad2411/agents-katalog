<!-- owner: shared | audience: all-pms | last-updated: 2026-02 -->
<!-- purpose: Weekly customer review summary from {your-review-platform}, App Store, and Slack -->

# Weekly Customer Reviews Summary

Generate a weekly summary of customer reviews from {your-review-platform}, Google Reviews, and the App Store, then save it and draft a Slack message to {your-pm-channel}.

## Instructions

### Step 1: Fetch {your-review-platform} reviews

1. Use WebFetch to pull the most recent reviews from `{your-review-platform-url}`
2. Extract: reviewer name, star rating, date, and full review text for every review visible
3. Note the overall star rating distribution if visible on the page

### Step 2: Fetch App Store reviews

1. Use WebFetch to pull reviews from `{your-app-store-url}`
2. Extract: reviewer name, star rating, date, title, and full review text
3. Only include reviews from the past week

### Step 3: Read Slack review channels

1. Load Slack tools using ToolSearch
2. Search for channels "reviews" and "app-reviews" using slack_search_channels to get their IDs
3. Read the past 7 days of messages from both channels using slack_read_channel with appropriate Unix timestamps for oldest/latest
4. Also search within both channels using slack_search_public with keywords like "star review", "{your-company-name}", "support", "easy", "recommend" to surface reviews where the text content is in the message body (many reviews are posted as rich attachments with empty text fields)
5. Extract any readable review content from Google Reviews (these tend to have visible text in the #reviews channel)

### Step 4: Categorise into themes

From ALL collected reviews across all sources, identify the key themes. For each theme provide:
- A descriptive name
- An estimated percentage of reviews falling into this category (use the overall {your-review-platform} star distribution to weight positive vs negative)
- Whether it is positive or negative sentiment
- 2-3 direct quotes from actual reviews

Common themes to look for (but don't limit to these):
- **Positive:** Easy/simple process, fair pricing, helpful staff, fast payment, better than alternatives
- **Negative:** Pricing issues, onboarding friction, customer support issues, delivery problems

### Step 5: Save the summary

Write the full summary as a markdown file to `insights/qual/` with the filename format `customer-reviews-summary-YYYY-MM-DD.md` (using today's date).

The file should include:
- Date range covered
- Total estimated review volume
- Rating distribution
- Each theme with: name, estimated %, sentiment, and 2-3 quotes
- A summary table of all themes
- Methodology & caveats section noting any data limitations

### Step 6: Draft Slack message

1. Load the Slack send message draft tool
2. Search for the {your-pm-channel} channel ID using slack_search_channels
3. Draft a concise version of the summary to {your-pm-channel} using slack_send_message_draft

The Slack message should use Slack mrkdwn formatting (single *asterisks* for bold, _underscores_ for italic, > for quotes).

**Slack formatting rules** (critical — the Slack API rejects invalid formatting):
- Do NOT use emoji shortcodes (`:star:`, `:chart:`, etc.) — these cause `invalid_blocks` errors in `slack_send_message`
- Do NOT use markdown tables — Slack mrkdwn does not support tables. Use bullet lists instead
- Use Unicode emoji or plain text markers for visual structure

Include:
- A header with the date range
- Total review volume and overall rating
- Each theme with estimated %, sentiment indicator, and one key quote
- A summary table
- A link to the full write-up file path

### Step 7: Notify the user

Tell the user the draft is ready for review in {your-pm-channel} and show them the file path of the full summary.

## Important Notes

- Only include customer reviews (not internal comments, Datadog alerts, or team discussions)
- Many Slack bot messages have empty text fields because reviews are posted as rich attachments -- use multiple search strategies to extract as much content as possible
- {your-review-platform} uses JavaScript pagination so only the first page of reviews may be accessible via WebFetch
- Be transparent about sample size limitations in the methodology section
- Percentage estimates should be informed by the overall {your-review-platform} star distribution, not just the small readable sample
