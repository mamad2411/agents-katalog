---
name: ai-community-sentiment-engagement-analyst
description: "Analyze community sentiment across Discord, Slack, Reddit & forums to identify engagement opportunities, pain points, and influencers. Use when the user needs weekly opportunity reports, collaboration insights, or community growth strategies."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {"openclaw":{"requires":{"env":["DISCORD_TOKEN","SLACK_BOT_TOKEN","REDDIT_CLIENT_ID","REDDIT_CLIENT_SECRET","OPENAI_API_KEY","GOOGLE_SEARCH_API_KEY"],"bins":["python3","curl"]},"os":["macos","linux","win32"],"files":["SKILL.md"],"emoji":"📊"}}
---

## Overview

The **AI Community Sentiment & Engagement Opportunity Analyst** is a comprehensive community intelligence tool that automatically monitors your target communities across Discord servers, Slack workspaces, Reddit subreddits, and niche forums to surface actionable insights. This skill transforms raw community conversations into strategic opportunities by:

- **Sentiment Analysis**: Real-time classification of discussions as positive, neutral, or negative
- **Influencer Identification**: Flags high-engagement members, thought leaders, and potential brand advocates
- **Pain Point Detection**: Extracts recurring problems, feature requests, and unmet needs from organic conversations
- **Collaboration Mapping**: Identifies cross-community partnership opportunities and co-marketing angles
- **Engagement Hook Generation**: Produces conversation starters and content ideas tailored to community interests
- **Weekly Opportunity Reports**: Delivers structured, actionable insights with specific next steps

**Perfect for**: SaaS founders, community managers, product teams, marketing leaders, and agencies managing multiple client communities. Integrates with Slack (for delivery), Google Sheets (for reporting), and native APIs for Discord, Reddit, and forum platforms.

---

## Quick Start

Try these example prompts immediately:

```
Analyze the #product-feedback channel in my Discord server (ID: 123456789) 
for the past 7 days. Identify the top 3 pain points mentioned, sentiment 
distribution, and list the 5 most engaged members. Generate 3 conversation 
starters based on unmet needs.
```

```
Generate a weekly community opportunity report for r/nodejs, r/python, and 
r/webdev. Include: sentiment breakdown, emerging trends, top 5 influencers 
by engagement, and 5 collaboration ideas with complementary communities. 
Format as a Slack message ready to share with my team.
```

```
Monitor my Slack workspace (#general, #feature-requests, #support) and flag 
any discussions mentioning "competitor X" or "pain point Y". Score sentiment, 
identify who mentioned it, and suggest 3 engagement hooks to convert concerns 
into product feedback.
```

```
Scan the following forum communities [list URLs] for mentions of "AI", "automation", 
or "workflow". Create a CSV with: poster name, sentiment score (1-10), post URL, 
key quote, and recommended response strategy.
```

---

## Capabilities

### 1. Multi-Platform Community Monitoring
- **Discord**: Real-time channel monitoring, thread analysis, emoji reaction sentiment
- **Slack**: Workspace-wide scanning, thread depth analysis, reaction tracking
- **Reddit**: Subreddit monitoring, comment thread analysis, post scoring
- **Niche Forums**: Web scraping + API integration for platforms like Discourse, Circle, Mighty Networks
- **Custom Communities**: Support for any platform with API access (Telegram, Facebook Groups, LinkedIn groups)

### 2. Advanced Sentiment Analysis
Powered by OpenAI's GPT-4 with context-aware classification:
- Extracts emotional tone, intent, and urgency from raw text
- Detects sarcasm, frustration, enthusiasm, and neutral inquiry
- Scores sentiment on 0-100 scale with confidence metrics
- Identifies emotional triggers and pain points within conversations
- Tracks sentiment trends over time (weekly/monthly comparisons)

### 3. Influencer & Advocate Identification
- **Engagement Scoring**: Combines post frequency, reply depth, reaction count, and follower metrics
- **Authority Detection**: Identifies domain expertise through keyword matching and response quality
- **Advocacy Potential**: Flags users showing strong positive sentiment + high engagement
- **Network Mapping**: Shows connections between key community members
- **Growth Trajectory**: Identifies rising voices gaining momentum in community

### 4. Pain Point & Opportunity Extraction
- **Automated Theme Clustering**: Groups similar complaints/requests using NLP
- **Frequency Analysis**: Ranks pain points by mention count and community impact
- **Solution Mapping**: Suggests product features or content that addresses each pain point
- **Competitive Intelligence**: Flags mentions of competitors and sentiment around alternatives
- **Feature Request Synthesis**: Consolidates fragmented feature requests into coherent product ideas

### 5. Engagement Hook Generation
Produces conversation starters tailored to community culture:
- Question-based hooks that invite participation
- Content ideas addressing identified pain points
- Collaboration proposals with complementary communities
- Product announcement angles based on community priorities
- Educational content ideas that provide immediate value

### 6. Weekly Opportunity Reports
Structured, actionable reports delivered to Slack or email:
- Executive summary (top 3 insights)
- Sentiment breakdown with trend analysis
- Top 10 influencers with engagement scores
- Emerging themes and trending topics
- Top 5 pain points with solution recommendations
- 5-10 specific engagement hooks with timing suggestions
- Collaboration opportunities with external communities
- Competitive intelligence summary
- Recommended actions with owner assignment

---

## Configuration

### Required Environment Variables

```bash
# Discord
DISCORD_TOKEN=your_bot_token_here
DISCORD_GUILD_IDS=123456789,987654321  # comma-separated

# Slack
SLACK_BOT_TOKEN=xoxb-your-token
SLACK_SIGNING_SECRET=your-signing-secret

# Reddit
REDDIT_CLIENT_ID=your-client-id
REDDIT_CLIENT_SECRET=your-client-secret
REDDIT_USERNAME=your-username
REDDIT_PASSWORD=your-password

# OpenAI (for sentiment analysis & report generation)
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4  # or gpt-3.5-turbo for cost optimization

# Google (for search & Sheets export)
GOOGLE_SEARCH_API_KEY=your-key
GOOGLE_SHEETS_API_KEY=your-key
GOOGLE_SHEETS_ID=your-spreadsheet-id

# Optional
WEBHOOK_URL=https://your-domain.com/webhook  # for real-time alerts
REPORT_SCHEDULE=weekly  # daily, weekly, monthly
REPORT_TIMEZONE=America/New_York
```

### Setup Instructions

1. **Create Discord Bot**: Visit [Discord Developer Portal](https://discord.com/developers/applications), create app, enable "Message Content Intent", copy token
2. **Create Slack App**: Go to [Slack API](https://api.slack.com/apps), create app, add "chat:write" and "channels:history" scopes
3. **Reddit API**: Register at [Reddit Apps](https://www.reddit.com/prefs/apps), create "script" type app
4. **OpenAI API**: Obtain key from [platform.openai.com](https://platform.openai.com)
5. **Google APIs**: Enable Sheets & Search APIs in [Google Cloud Console](https://console.cloud.google.com)
6. **Deploy**: Use environment variables in your deployment platform (Vercel, Heroku, AWS Lambda, etc.)

### Configuration Options

```yaml
monitoring:
  channels:
    discord:
      - guild_id: "123456789"
        include_channels: ["#general", "#product", "#feedback"]
        exclude_channels: ["#off-topic"]
    slack:
      - workspace_id: "T123ABC"
        include_channels: ["#announcements", "#feature-requests"]
    reddit:
      - subreddits: ["nodejs", "python", "webdev"]
        min_upvotes: 5  # only analyze posts with 5+ upvotes
    forums:
      - url: "https://forum.example.com"
        categories: ["feature-requests", "bugs"]

analysis:
  sentiment_threshold: 0.6  # flag items with strong sentiment
  influencer_min_engagement: 10  # minimum interactions to be flagged
  pain_point_min_frequency: 3  # mention count threshold
  
reporting:
  format: "slack"  # slack, email, google_sheets, markdown
  frequency: "weekly"  # daily, weekly, monthly
  recipients:
    slack: "#community-insights"
    email: ["team@example.com"]
  include_sections:
    - sentiment_analysis
    - influencers
    - pain_points
    - engagement_hooks
    - collaboration_opportunities
```

---

## Example Outputs

### Sentiment Analysis Report

```
Community: r/nodejs
Period: Jan 1-7, 2025
Total Posts Analyzed: 247

SENTIMENT BREAKDOWN:
├─ Positive (60%): 148 posts
├─ Neutral (30%): 74 posts
└─ Negative (10%): 25 posts

TOP NEGATIVE THEMES:
1. "TypeScript learning curve" (8 mentions, avg sentiment: 2.1/10)
2. "Dependency management complexity" (6 mentions, avg sentiment: 3.4/10)
3. "Performance issues with large projects" (5 mentions, avg sentiment: 2.8/10)

TREND: Sentiment up 12% week-over-week. Community enthusiasm about Node.js 21 release.
```

### Influencer Identification

```
TOP 5 COMMUNITY VOICES (by engagement + authority):

1. @nodejs_guru (Score: 94/100)
   └─ Posts: 12 | Avg Replies: 8.3 | Positive Sentiment: 85%
   └─ Expertise: Framework architecture, best practices
   └─ Advocacy Level: HIGH | Recommendation: Feature them in newsletter

2. @debugging_expert (Score: 87/100)
   └─ Posts: 18 | Avg Replies: 6.2 | Positive Sentiment: 79%
   └─ Expertise: Debugging, performance optimization
   └─ Advocacy Level: MEDIUM | Recommendation: Invite to beta program

3. @newbie_helper (Score: 82/100)
   └─ Posts: 25 | Avg Replies: 4.1 | Positive Sentiment: 71%
   └─ Expertise: Onboarding, documentation clarity
   └─ Advocacy Level: MEDIUM | Recommendation: Collaborate on tutorial content
```

### Engagement Hooks

```
CONVERSATION STARTERS (Ready to Use):

1. "We noticed several discussions about TypeScript setup complexity. 
   What's your biggest pain point when configuring TS in Node.js projects? 
   We're building a resource guide and want to address the real blockers."
   └─ Best Time: Tuesday 2 PM EST | Channel: #nodejs-help

2. "Saw the thread about dependency management. Do you use workspaces, 
   monorepos, or something else? Curious how the community is solving this."
   └─ Best Time: Wednesday 10 AM EST | Channel: #nodejs-general

3. "Performance optimization is a hot topic lately. What's the #1 bottleneck 
   you've hit in production? We're collecting real-world challenges for our 
   next content series."
   └─ Best Time: Thursday 1 PM EST | Channel: #nodejs-performance
```

### Weekly Opportunity Report (Slack Format)

```
📊 COMMUNITY INSIGHTS REPORT — Week of Jan 1-7

🎯 TOP 3 OPPORTUNITIES
1. TypeScript adoption friction → Create "TS setup guide" (14 mentions, 8.2/10 urgency)
2. Dependency management pain → Host "monorepo best practices" webinar (11 mentions)
3. Performance optimization interest → Publish "Node.js profiling guide" (9 mentions)

😊 SENTIMENT: 60% Positive | 30% Neutral | 10% Negative ⬆️ +12% vs last week

👥 RISING VOICES
• @nodejs_guru (94/100) — Framework expert, high influence
• @debugging_expert (87/100) — Performance focus, helpful community member
• @newbie_helper (82/100) — Great for onboarding content collaboration

🤝 COLLABORATION IDEAS
1. Partner with @debugging_expert on performance optimization content
2. Feature @nodejs_guru's insights in monthly newsletter
3. Invite @newbie_helper to review documentation clarity

💬 READY-TO-USE ENGAGEMENT HOOKS
→ "We noticed TypeScript setup frustration. What's your biggest pain point?"
→ "How are you solving dependency management at scale?"
→ "What's the #1 performance bottleneck you've hit in production?"

⚡ RECOMMENDED ACTIONS
[ ] Schedule 15-min call with @nodejs_guru (assign: @manager)
[ ] Draft "TS setup guide" outline (assign: @content-team)
[ ] Plan monorepo webinar (assign: @product-manager)
```

---

## Tips & Best Practices

### 1. Maximize Influencer Relationships
- **Prioritize High-Authority Voices**: Focus engagement efforts on users scoring 85+
- **Segment by Advocacy Level**: HIGH = beta access; MEDIUM = exclusive content; LOW = nurture track
- **Track Engagement History**: Note what content/topics each influencer responds to best
- **Create VIP Channels**: Give top influencers exclusive access to early releases or feedback groups

### 2. Act on Pain Points Quickly
- **Weekly Review**: Set aside 30 minutes every Monday to review new pain points
- **Prioritize by Frequency + Sentiment**: Focus on issues mentioned 5+ times with negative sentiment
- **Close the Loop**: When you address a pain point, announce it in the community with attribution
- **Create Content Roadmap**: Use pain points to inform your content calendar (blogs, videos, guides)

### 3. Optimize Engagement Hooks
- **Test Timing**: Experiment with post times; track which hours get highest response rates
- **Use Community Language**: Mirror the terminology and tone from actual community discussions
- **Ask Open-Ended Questions**: "What's your biggest challenge?" beats "Do you like feature X?"
- **Follow Up**: If someone responds, continue the conversation; build relationships, don't just extract data

### 4. Build Collaboration Partnerships
- **Map Community Overlaps**: Identify communities with 30%+ audience overlap for co-marketing
- **Create Win-Win Proposals**: Offer value (guest posts, exclusive access, revenue share) not just promotion
- **Cross-Promote Strategically**: Share partner content in your communities when genuinely relevant
- **Track Collaboration ROI**: Measure traffic, signups, and sentiment impact from partnerships

### 5. Refine Your Monitoring Scope
- **Start Narrow**: Begin with 2-3 core communities, then expand
- **Exclude Noise**: Blacklist off-topic channels and low-signal forums early
- **Adjust Thresholds**: If reports are too noisy, increase minimum engagement scores
- **Seasonal Adjustments**: Some communities are more active at certain times; plan accordingly

### 6. Protect Community Trust
- **Never Spam**: Only engage when you have genuine value to add
- **Disclose Affiliation**: Be transparent about your company's involvement
- **Respect Community Rules**: Follow each community's guidelines on self-promotion
- **Add Value First**: Spend 80% of time helping, 20% on promotion
- **Don't Manipulate Sentiment**: Never astroturf or use fake accounts to artificially boost perception

---

## Safety & Guardrails

### What This Skill Will NOT Do

✋ **Does NOT**:
- Scrape private/non-public communities without explicit permission
- Bypass authentication or violate terms of service of any platform
- Create fake accounts or engage in inauthentic behavior
- Store personal data longer than 30 days (GDPR/CCPA compliance)
- Automate posts without human review and approval
- Manipulate voting systems or artificially inflate engagement metrics
- Share community data with third parties without consent
- Impersonate community members or misrepresent your company

### Ethical Boundaries

1. **Transparency**: Always disclose your company's involvement in communities
2. **Consent**: Only monitor communities you have permission to access
3. **Privacy**: Aggregate insights at the theme level; don't expose individual member data
4. **Authenticity**: All engagement must be genuine and add real value
5. **Respect**: Honor each community's culture, rules, and norms
6. **Data Security**: Encrypt API keys, use secure storage, rotate credentials quarterly

### Limitations

- **Platform Changes**: API changes may temporarily break monitoring; check status page weekly
- **Sentiment Accuracy**: AI sentiment analysis is 85-90%