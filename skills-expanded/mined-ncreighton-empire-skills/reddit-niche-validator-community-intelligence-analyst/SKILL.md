---
name: reddit-niche-validator-community-intelligence-analyst
description: "Analyze Reddit communities to identify underserved niches, map competitor mentions, extract pain points, and generate monthly intelligence reports. Use when the user needs niche validation, market research, audience insights, or competitive analysis before launching products."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET", "OPENAI_API_KEY"],
        "bins": ["python3", "curl"]
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"],
      "emoji": "🔍"
    }
  }
---

## Overview

The **Reddit Niche Validator & Community Intelligence Analyst** is a production-grade market research skill that transforms raw Reddit community data into actionable business intelligence. Instead of manually scrolling through thousands of posts, this skill systematically analyzes subreddit ecosystems to uncover:

- **Underserved niches** with high engagement but low competitive saturation
- **Competitor mention maps** showing who's winning mind-share in your target market
- **Problem statements** extracted directly from user discussions (the real pain points)
- **Sentiment trajectories** tracking how community sentiment evolves monthly
- **Audience demographics & growth patterns** for validated market sizing
- **Monthly intelligence reports** with scores, trends, and recommendations

This skill integrates with **Slack** (for report delivery), **Google Sheets** (for data export), **Zapier** (for workflow automation), and **WordPress** (for publishing research summaries). It's designed for:

- Product managers validating ideas before development
- Marketing agencies finding high-intent customer communities
- Founders identifying blue-ocean opportunities
- Content creators finding underserved audiences
- Researchers mapping community sentiment and growth

**Why it matters:** Reddit hosts 140M+ monthly active users discussing real problems in 140K+ active communities. This skill cuts through the noise, applying NLP sentiment analysis, semantic clustering, and trend detection to identify markets before they're saturated.

---

## Quick Start

### Example 1: Validate a SaaS Niche
```
Analyze these subreddits for underserved SaaS opportunities:
- r/freelance
- r/servicemanagers
- r/SmallBusiness

Focus on: recurring pain points, tool recommendations, budget discussion,
and competitor mentions. Generate a niche score (0-100) for each.
```

### Example 2: Competitive Landscape Mapping
```
Create a competitor mention matrix for the "productivity tools" niche:

Subreddits: r/productivity, r/getdisciplined, r/nootropics, r/studytips

For each subreddit, track mentions of: Notion, Obsidian, Roam Research, 
LogSeq, Asana, Monday.com

Show sentiment (positive/negative/neutral), frequency trend (last 90 days),
and user adoption patterns.
```

### Example 3: Extract Pain Points & Opportunities
```
Generate a problem statement report for the "AI tooling for creators" niche.

Search these communities: r/Creators, r/VideoEditing, r/AIwriters, 
r/graphic_design

Extract: Top 10 unresolved problems, sentiment around existing solutions,
willingness-to-pay signals, and community size/growth.

Format as a JSON report with severity scores.
```

### Example 4: Monthly Sentiment & Trend Analysis
```
Run a 90-day sentiment trajectory analysis on r/soloprepreneur

Track: Monthly mentions of "burnout", "work-life balance", "scaling",
"outsourcing", "tools"

Show trend direction, volume changes, and correlated discussion topics.
Include a seasonality analysis and forecast next quarter.
```

---

## Capabilities

### 1. **Subreddit Deep Dive Analysis**
- Scrapes up to 2,000 posts per subreddit (respecting Reddit API rate limits)
- Extracts title, body, comments, upvotes, posting date, author
- Applies NLP to identify discussion themes, sentiment, and entity extraction
- Returns: community size, growth rate, post frequency, engagement metrics

### 2. **Niche Scoring Engine**
- **Market Size Score:** Based on subscriber count, daily active users, post volume
- **Problem Clarity Score:** How explicitly users articulate problems (semantic analysis)
- **Competitive Saturation Score:** Tracks branded mentions vs. organic problem discussion
- **Growth Trajectory:** 30/90/180-day subscriber and engagement trends
- **Opportunity Score:** Composite metric (0-100) combining all factors
- Example output:
  ```json
  {
    "subreddit": "r/RemoteWorkers",
    "opportunity_score": 87,
    "market_size_score": 92,
    "problem_clarity": 89,
    "saturation_score": 34,
    "growth_momentum": 8.2%,
    "subscriber_count": 487203,
    "daily_active_users": 12400,
    "recommendation": "HIGH POTENTIAL - Underserved niche with strong engagement"
  }
  ```

### 3. **Competitor Mention Intelligence**
- Identifies brand mentions (exact match + fuzzy matching for misspellings)
- Maps sentiment: positive, negative, neutral, ambivalent
- Tracks feature requests and unmet needs customers mention
- Builds a "competitor perception matrix" showing strengths/weaknesses
- Monitors price sensitivity and contract churn signals

### 4. **Pain Point & Question Extraction**
- Uses GPT-4 semantic analysis to extract recurring problems
- Groups similar issues using clustering (K-means on embeddings)
- Ranks by frequency, recency, and community consensus
- Identifies emerging problems (new discussions gaining traction)
- Example extraction:
  ```
  Top Pain Points in r/ContentCreators:
  
  1. "Inconsistent income/unstable revenue" — 2,847 mentions, 94% negative sentiment
  2. "Burnout from constant content pressure" — 1,923 mentions, trending up 34% MoM
  3. "Algorithm changes killing reach" — 1,654 mentions, sentiment declining
  4. "Lack of community management tools" — 892 mentions, high commercial intent
  5. "Creator-to-business collaboration barriers" — 567 mentions, rising trend
  ```

### 5. **Sentiment Trend Tracking**
- Aggregates sentiment scores at monthly intervals
- Detects inflection points (when sentiment shifts significantly)
- Correlates sentiment changes with external events/mentions
- Measures "problem urgency" (how frustrated users are)
- Generates trend forecasts using time-series analysis

### 6. **Monthly Intelligence Report Generation**
- Automated PDF/JSON export with visualizations
- Includes: market sizing, opportunity ranking, competitor matrix, problem mapping
- Sentiment heat maps and trend graphs
- Actionable recommendations per niche
- Integrates with Slack (automated delivery), Google Sheets (data sync)

---

## Configuration

### Required Environment Variables
```bash
# Reddit API Authentication
export REDDIT_CLIENT_ID="your_client_id"
export REDDIT_CLIENT_SECRET="your_client_secret"
export REDDIT_USER_AGENT="YourApp/1.0 by YourUsername"

# AI Analysis
export OPENAI_API_KEY="sk-your-api-key"
export OPENAI_MODEL="gpt-4"  # or gpt-3.5-turbo for cost optimization

# Optional: Cloud Export
export GOOGLE_SHEETS_API_KEY="your-sheets-key"
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."
export WORDPRESS_API_KEY="your-wordpress-token"  # for publishing reports
```

### Setup Instructions
1. **Create Reddit App:**
   - Visit https://reddit.com/prefs/apps
   - Create a "script" app (personal use)
   - Copy Client ID and Client Secret

2. **Install Dependencies:**
   ```bash
   pip install praw openai pandas numpy scikit-learn matplotlib slack-sdk gspread
   ```

3. **Authenticate:**
   - Store credentials in `.env` file (add to `.gitignore`)
   - Skill auto-loads on first run

4. **Configure Report Delivery:**
   - Add Slack webhook for daily/weekly digests
   - Link Google Sheets for collaborative analysis
   - Enable WordPress integration for public insights

---

## Example Outputs

### Output 1: Niche Opportunity Report (JSON)
```json
{
  "report_date": "2024-01-15",
  "analysis_period": "90_days",
  "subreddits_analyzed": 12,
  "top_opportunities": [
    {
      "rank": 1,
      "subreddit": "r/solopreneur",
      "opportunity_score": 91,
      "subscriber_count": 342100,
      "monthly_posts": 8934,
      "engagement_rate": 8.2,
      "top_problems": [
        "Client acquisition strategies",
        "Price setting for services",
        "Time management / burnout"
      ],
      "competitor_mentions": {
        "Notion": 127,
        "Zapier": 89,
        "Stripe": 76
      },
      "sentiment_trend": "stable_positive",
      "growth_rate_quarterly": "12.3%",
      "recommendation": "LAUNCH_READY"
    }
  ]
}
```

### Output 2: Sentiment Trajectory Chart (Text-Based)
```
r/RemoteWorkers — 90 Day Sentiment Analysis

Positive Sentiment Trend:
Month 1: ████████░░ 82%
Month 2: █████████░ 88%
Month 3: ██████████ 92%

Key Drivers:
- "Remote flexibility" mentions ↑ 34%
- "Timezone stress" mentions ↓ 28%
- "Salary negotiation" emerging (+156%)
```

### Output 3: Problem Ranking Table (Markdown)
```markdown
| Rank | Problem | Frequency | Sentiment | Trend | Commercial Intent |
|------|---------|-----------|-----------|-------|-------------------|
| 1 | Burnout/work-life balance | 2,847 | -0.82 | ↑↑ | High |
| 2 | Isolation/loneliness | 1,923 | -0.76 | ↑ | Medium |
| 3 | Finding quality contractors | 1,654 | -0.68 | ↑↑ | Very High |
| 4 | Tax/financial management | 1,203 | -0.54 | → | High |
| 5 | Imposter syndrome | 892 | -0.71 | → | Low |
```

---

## Tips & Best Practices

### 1. **Refine Your Subreddit Selection**
- Start with 5-10 highly relevant subreddits, not 50+ (depth > breadth)
- Use Reddit's search (`/r/topic`) to find niche communities aligned to your problem space
- Check sidebar descriptions to confirm topic alignment
- Avoid mega-communities (r/AskReddit, r/funny) — too broad, low signal

### 2. **Set Appropriate Analysis Depth**
- **Light analysis:** Last 7 days of posts (daily monitoring, quick insights)
- **Standard analysis:** Last 90 days (quarterly planning, trend detection)
- **Deep analysis:** Last 365 days (founding research, historical shifts)
- Note: Deeper analysis takes longer due to API rate limits

### 3. **Interpret Opportunity Scores Contextually**
- **90-100:** Launch-ready niches with high demand, low saturation
- **75-89:** Strong opportunities, needs validation or differentiation
- **60-74:** Emerging interests, possible timing issue or niche appeal
- **Below 60:** Saturated, declining, or insufficient problem clarity

### 4. **Cross-Reference with External Data**
- Validate subreddit insights with Google Trends (search volume)
- Check Ahrefs/SEMrush for keyword difficulty and search volume
- Review ProductHunt and AppSumo for competing solutions
- Use Builtwith to identify tech stacks in use

### 5. **Automate Report Delivery**
```bash
# Run analysis every Sunday 8am, send to Slack
0 8 * * 0 /usr/bin/python3 /path/to/reddit-validator.py --schedule weekly --slack-notify
```

### 6. **Monitor Sentiment Shifts**
- Set alerts for sentiment drops >15% month-over-month (warning sign)
- Track emerging problem keywords (use GPT to identify new topics)
- Watch for influx of new members (could indicate trend timing)
- Monitor moderator discussions in private mod logs (if accessible)

### 7. **Combine with User Interview Validation**
- Use extracted pain points as interview guide questions
- Validate problem ranking with 10-15 real users
- Test willingness-to-pay signals from "how much would you pay?" discussions
- Don't launch solely based on Reddit sentiment — validate with surveys

---

## Safety & Guardrails

### What This Skill Will NOT Do
- **Violate Reddit's Terms of Service:** Does not mass-scrape, brigade, or manipulate voting
- **De-anonymize users:** Extracts themes/patterns only, never individual user tracking
- **Harass or target communities:** Respects community norms and doesn't engage in conflict
- **Bypass authentication:** Uses official Reddit API with proper credentials only
- **Store raw user data:** All processing is ephemeral; reports contain only aggregated insights

### API Rate Limiting & Ethical Boundaries
- Respects Reddit API rate limits (60 requests/minute for authenticated users)
- Implements exponential backoff for rate-limit errors
- Does not scrape comments from deleted/removed posts
- Excludes shadowbanned users and deleted accounts from analysis
- Does not generate reports on private/restricted subreddits

### Limitations
- **Reddit API access:** Requires valid API credentials; development apps have lower rate limits
- **Analysis latency:** Large analyses (10+ subreddits × 90 days) may take 15-30 minutes
- **NLP accuracy:** Sentiment analysis is 82-87% accurate; context-dependent cases may mis-classify
- **Real-time limitations:** Reports reflect historical data; real-time monitoring requires polling
- **Niche detection:** Works best for 50K+ subscriber communities; smaller communities may have insufficient data

### Responsible Use Guidelines
- Use findings to **validate**, not assume (Reddit ≠ market truth)
- Cross-reference with traditional market research (surveys, interviews)
- Disclose that insights come from Reddit when publishing findings
- Don't use sentiment analysis to mock or target communities
- Honor GDPR/privacy laws when exporting user-derived insights

---

## Troubleshooting

### Issue 1: "Invalid Reddit Credentials"
**Cause:** CLIENT_ID or CLIENT_SECRET incorrect or expired
**Solution:**
```bash
# Verify credentials at https://reddit.com/prefs/apps
# Re-generate if needed, update .env file
export REDDIT_CLIENT_ID="new_id_here"
export REDDIT_CLIENT_SECRET="new_secret_here"

# Test connection
python3 -c "import praw; reddit = praw.Reddit(client_id='...', client_secret='...'); print(reddit.user.me())"
```

### Issue 2: "Rate Limit Exceeded"
**Cause:** Too many API requests in short time
**Solution:**
- Reduce number of subreddits analyzed per run
- Increase analysis interval (run weekly instead of daily)
- Use cache for recent analyses (skip if run within 6 hours)
- Upgrade Reddit API app tier (personal → business if available)

### Issue 3: "Sentiment Analysis Timeout"
**Cause:** GPT-4 processing large datasets slowly
**Solution:**
```bash
# Option A: Use faster model
export OPENAI_MODEL="gpt-3.5-turbo"  # 3x faster, slightly less accurate

# Option B: Batch processing with delays
python3 reddit-validator.py --batch-size 50 --delay 2  # 2sec between batches

# Option C: Reduce analysis scope
# Analyze 500 posts instead of 2000
reddit-validator.py --max-posts 500
```

### Issue 4: "Subreddit Not Found or Private"
**Cause:** Typo, subreddit deleted, or access restricted
**Solution:**
```bash
# Check subreddit validity first
python3 -c "import praw; reddit = praw.Reddit(...); sub = reddit.subreddit('subreddit_name'); print(sub.display_name, sub.subscribers)"