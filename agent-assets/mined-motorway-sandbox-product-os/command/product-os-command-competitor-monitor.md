<!-- owner: shared | audience: all-pms | last-updated: 2026-03 -->
<!-- purpose: On-demand competitor news search and analysis -->

You are running an on-demand competitor monitor. This is an interactive session — present findings and ask for direction.

## Task

Search the web for competitor and market news relevant to {Your Company}, save structured results, and present a summary.

## Step 1: Search

Run the following 9 web searches (run as many in parallel as possible):

<!-- SETUP: Replace the searches below with your actual competitors and market.
     Add 4-6 competitor-specific searches and 2-3 thematic searches. -->

**Competitor-specific:**
1. "{Competitor 1}" news — last 7 days
2. "{Competitor 2}" news — last 7 days
3. "{Competitor 3}" news — last 7 days
4. "{Competitor 4}" news — last 7 days

**Thematic:**
5. {your industry} market trends — last 7 days
6. {your industry} AI startups — last 7 days
7. {your industry} funding OR investment — last 7 days

For each search, review the top results. Use WebFetch to read any articles that look significant (new product launches, funding rounds, executive changes, market shifts, regulatory changes, technology moves).

## Step 2: Evaluate

For each piece of news found, assess:
- **Significance**: High / Medium / Low
  - High: direct competitive threat, major funding/M&A, product launch that overlaps with {Your Company}, regulatory change affecting the market
  - Medium: notable but indirect — market trend, executive hire, geographic expansion
  - Low: routine coverage, minor updates, no clear implication for {Your Company}
- **{Your Company} implication**: 1–2 sentences on what this means for {Your Company}'s strategy, positioning, or priorities

Discard Low-significance items unless 3+ Low items together suggest a pattern worth noting.

## Step 3: Check for duplicates

Read the existing per-competitor tracking files to avoid repeating news already logged:
- insights/market/competitors/{competitor-1}.md
- insights/market/competitors/{competitor-2}.md
- insights/market/competitors/{competitor-3}.md

Also check recent digest files in insights/market/competitors/weekly-digests/ (use Glob to find the most recent one, if any).

Skip any news items that are already recorded.

## Step 4: Present findings

Present the results in a clear summary:

### Key Signals
- {high-significance findings, bulleted}

### By Competitor
For each competitor with news, show:
- **{Competitor}**: {headline} — {1-2 sentence summary}. Significance: {H/M/L}. *{Your Company} implication: {implication}*. [Source]({url})

### Market Themes
- {theme}: {summary}

## Step 5: Ask what to do next

After presenting findings, ask the user:

> What would you like to do?
> 1. **Save digest** — Save to `insights/market/competitors/weekly-digests/` and update per-competitor files
> 2. **Dig deeper** — Investigate a specific competitor or signal in more detail
> 3. **Adjust scope** — Change time window, add/remove competitors, focus on specific themes
> 4. **Send Slack summary** — Send a concise summary DM to {YOUR_NAME} on Slack
> 5. **Save and send** — Do both 1 and 4

If the user chooses to save, create the digest file and update per-competitor files following the same format as the automated version:
- Digest at: `insights/market/competitors/weekly-digests/competitor-digest-{YYYY-MM-DD}.md`
- Per-competitor files: prepend new week entry after "## News Log" heading

If the user chooses to send on Slack, use the same concise format as the automated version (max ~15 lines).

## Important

- Use UK date format (6 March, not March 6)
- Use UK English throughout
- Run web searches in parallel where possible
- Do not fabricate or speculate about news — only report what you find with sources
- Each finding must have a working source URL
- Flag confidence level if a source seems unreliable or a claim is unverified
