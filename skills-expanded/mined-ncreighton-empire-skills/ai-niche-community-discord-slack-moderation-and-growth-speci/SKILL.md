---
name: ai-niche-community-discord-slack-moderation-and-growth-specialist
description: "Automate Discord/Slack moderation, toxicity filtering, and community growth with AI-powered member scoring, FAQ auto-responses, viral moment detection, and weekly health reports. Use when the user needs spam prevention, community engagement analytics, member retention strategies, or automated moderation workflows."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {"openclaw":{"requires":{"env":["DISCORD_BOT_TOKEN","SLACK_BOT_TOKEN","OPENAI_API_KEY","PERSPECTIVE_API_KEY"],"bins":["python3","curl"]},"os":["macos","linux","win32"],"files":["SKILL.md"],"emoji":"🛡️"}}
---

## Overview

The **AI Niche Community Discord/Slack Moderation and Growth Specialist** is a production-ready automation system designed to manage, moderate, and grow engaged niche communities across Discord and Slack. This skill combines real-time moderation (spam detection, toxicity filtering, automated warnings), member intelligence (high-value member identification, retention scoring), and growth analytics (viral moment detection, sentiment-driven content recommendations, weekly health reports).

### Why This Matters

Community managers spend 30-40% of their time on repetitive moderation tasks and manual member engagement tracking. This skill eliminates that overhead while providing data-driven insights to grow community quality and retention. It integrates with:

- **Discord API** — native bot integration for real-time message monitoring
- **Slack API** — workspace moderation and member analytics
- **Google Perspective API** — toxicity and spam classification
- **OpenAI GPT-4** — contextual FAQ responses and sentiment analysis
- **PostgreSQL/Firebase** — member scoring and historical analytics

---

## Quick Start

Try these prompts immediately to see the skill in action:

### Example 1: Set Up Automated Moderation Rules
```
"Set up moderation for my Discord server. Flag messages with toxicity score >0.7, 
auto-delete spam patterns (repeated emojis, links >5 per message), and send warnings 
to members with >3 violations in 24 hours. Whitelist #announcements and #dev channels 
from spam filters."
```

### Example 2: Identify High-Value Members
```
"Analyze my Slack workspace and generate a member score for everyone based on: 
message quality (not just frequency), helpful responses given to others, 
participation in threads, and emoji reactions received. Rank top 20 members 
and suggest who to feature in our weekly newsletter."
```

### Example 3: Generate Weekly Community Health Report
```
"Create a weekly community health report for my Discord server showing: 
total messages, new members joined, member retention rate, toxicity incidents, 
top discussion topics by sentiment, and engagement trends. Include recommendations 
for content topics based on conversation sentiment."
```

### Example 4: Detect Viral Moments
```
"Monitor my Discord for viral moments: identify threads with >50 reactions, 
messages that sparked high engagement, and sentiment shifts. When detected, 
pin the message, notify community managers, and suggest follow-up content topics."
```

### Example 5: Auto-Respond to FAQs
```
"Train the FAQ responder on our community guidelines, pricing, onboarding process, 
and common technical questions. When members ask similar questions, auto-respond 
with contextual answers and escalate complex issues to moderators."
```

---

## Capabilities

### 1. Real-Time Moderation & Spam Detection
- **Toxicity Filtering**: Uses Google Perspective API to score messages for toxicity, profanity, and personal attacks (0-1 scale)
- **Spam Detection**: Identifies repeated links, excessive emojis, all-caps messages, and coordinated spam patterns
- **Automated Warnings**: Issues progressive warnings (1st: DM warning, 2nd: mute 1 hour, 3rd: escalate to mods)
- **Custom Rules**: Define channel-specific rules (e.g., stricter moderation in #general, relaxed in #off-topic)
- **Whitelist/Blacklist**: Exclude trusted members or channels from certain filters

**Usage Example:**
```
Configure moderation thresholds:
- Toxicity threshold: 0.7 (flag if score >0.7)
- Spam link limit: 3 links per message
- Caps lock threshold: 70% of message
- Repeated emoji limit: 5 consecutive
- Action: Auto-delete + warning on first offense
```

### 2. Member Intelligence & Retention Scoring
- **Member Value Score**: Composite metric based on:
  - Message quality (sentiment, helpfulness, citations)
  - Community contribution (answers given, threads started)
  - Engagement consistency (days active, response time)
  - Network influence (followers, reactions received)
- **Retention Risk Scoring**: Identifies members likely to churn (declining activity, negative sentiment)
- **High-Value Member Alerts**: Notifies admins when VIP members are at risk
- **Cohort Analysis**: Groups members by activity level and engagement type

**Usage Example:**
```
Member John_Dev scores:
- Message Quality: 8.5/10 (helpful, technical)
- Contribution: 9.2/10 (answered 47 questions, started 12 threads)
- Consistency: 7.8/10 (active 5/7 days)
- Influence: 8.9/10 (avg 12 reactions per message)
- Overall Score: 8.6/10 (VIP tier)
- Retention Risk: Low (stable engagement)
- Recommendation: Feature in monthly spotlight, invite to leadership council
```

### 3. Automated FAQ Responses
- **Intent Recognition**: Understands questions even with different wording
- **Contextual Answers**: Pulls from knowledge base and recent discussions
- **Escalation Logic**: Routes complex questions to human moderators
- **Learning**: Improves responses based on member feedback and mod corrections
- **Multi-Language Support**: Responds in member's detected language

**Usage Example:**
```
Member asks: "How do I get started with your product?"
Bot responds: "Welcome! Here's our onboarding guide: [link]. 
Key steps: (1) Create account, (2) Connect your first data source, 
(3) Run your first analysis. Stuck? Reply with 'help' or ask in #support."
```

### 4. Viral Moment Detection & Content Recommendations
- **Engagement Surge Detection**: Identifies threads with unusual activity spikes
- **Sentiment Trend Analysis**: Detects when conversations shift positive/negative
- **Topic Extraction**: Pulls trending discussion topics from viral threads
- **Content Recommendations**: Suggests follow-up topics based on sentiment and engagement
- **Viral Amplification**: Auto-pins messages, notifies mods, suggests discussion starters

**Usage Example:**
```
Viral Moment Detected:
- Thread: "New feature announcement" (47 reactions, 23 replies in 2 hours)
- Sentiment: 92% positive
- Topics: Feature request, use cases, integration
- Action: Pinned message, notified #announcements
- Recommendation: Host a live demo session, create tutorial video
```

### 5. Weekly Community Health Reports
- **Engagement Metrics**: DAU, MAU, message volume, reply rates
- **Member Lifecycle**: New members, churned members, reactivated members
- **Content Performance**: Top threads, most-discussed topics, sentiment trends
- **Moderation Summary**: Violations, warnings issued, banned members
- **Health Score**: Overall community vitality (0-100 scale)
- **Actionable Recommendations**: Specific steps to improve retention and engagement

**Usage Example:**
```
WEEKLY COMMUNITY HEALTH REPORT (Jan 15-21)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Engagement
- Messages: 2,847 (+12% vs last week)
- Active Members: 287 (↑8)
- Avg Reply Time: 2.3 hours
- Thread Participation: 64% (↑3%)

👥 Member Lifecycle
- New Members: 34
- Churned (7d inactive): 8
- Reactivated: 12
- Health Score: 78/100 (↑2 points)

🔥 Top Topics (by engagement)
1. Feature requests (234 messages, 89% positive)
2. Use cases (156 messages, 94% positive)
3. Integrations (98 messages, 76% positive)

⚠️ Moderation
- Toxicity Flags: 3 (all handled)
- Spam Removed: 12 messages
- Warnings Issued: 2
- Bans: 0

💡 Recommendations
1. Host live demo on top feature request
2. Create integration guide for #3 trending topic
3. Spotlight 5 high-value members (retention)
4. Schedule AMAs with product team
```

---

## Configuration

### Environment Variables (Required)

```bash
# Discord Integration
DISCORD_BOT_TOKEN=your_discord_bot_token_here
DISCORD_GUILD_ID=your_server_id_here

# Slack Integration
SLACK_BOT_TOKEN=xoxb-your-slack-bot-token
SLACK_SIGNING_SECRET=your_slack_signing_secret

# AI & Moderation APIs
OPENAI_API_KEY=sk-your-openai-key
PERSPECTIVE_API_KEY=your-google-perspective-api-key

# Database (for member scoring & history)
DATABASE_URL=postgresql://user:password@localhost/community_db
# OR Firebase
FIREBASE_PROJECT_ID=your-firebase-project
FIREBASE_PRIVATE_KEY=your-firebase-key

# Optional: Analytics
MIXPANEL_TOKEN=your-mixpanel-token
```

### Setup Instructions

1. **Create Discord Bot** (if using Discord):
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Create new application → Bot → Copy token
   - Enable intents: Message Content, Guild Members
   - Invite to server with permissions: Manage Messages, Moderate Members, Send Messages

2. **Create Slack App** (if using Slack):
   - Go to [Slack API Dashboard](https://api.slack.com/apps)
   - Create new app → Install to workspace
   - Enable events: message.channels, member_joined_channel
   - Set permissions: chat:write, users:read, conversations:read

3. **Configure Moderation Rules**:
   ```yaml
   moderation:
     toxicity_threshold: 0.7
     spam_filters:
       - repeated_links: 3
       - excessive_caps: 70%
       - emoji_spam: 5
     auto_actions:
       first_violation: "dm_warning"
       second_violation: "mute_1h"
       third_violation: "escalate_to_mods"
     whitelisted_channels: ["#announcements", "#dev"]
   ```

4. **Train FAQ System**:
   - Upload knowledge base (markdown or PDF)
   - Provide 10-20 example Q&A pairs
   - Define escalation keywords for human review

---

## Example Outputs

### Moderation Alert
```
🚨 MODERATION ALERT
Member: @SpamBot_123
Message: "CHECK THIS OUT!!! FREE MONEY!!! CLICK LINK 👉 bit.ly/xxx [emoji spam]"
Toxicity Score: 0.82 (FLAGGED)
Spam Score: 0.91 (FLAGGED)
Action: Message deleted, member warned (1/3)
Reason: Toxicity (0.82 > 0.7 threshold) + Spam (links + emoji spam)
```

### Member Spotlight Report
```
⭐ TOP 5 MEMBERS THIS WEEK
1. @Sarah_Dev (Score: 9.1/10)
   - Answered 23 questions
   - 156 reactions received
   - Helped 18 unique members

2. @Alex_Designer (Score: 8.7/10)
   - Started 8 high-quality threads
   - 98% positive sentiment
   - Mentored 3 new members

[... 3 more members ...]

🎯 Retention Risk Alert
@OldMember_42 (formerly Score: 8.9/10)
- Activity ↓ 78% (was 45 msg/week, now 10)
- Last message: 6 days ago
- Sentiment: Neutral → Negative
- Recommendation: Reach out personally, invite to special event
```

### FAQ Response Example
```
User: "What's the pricing for enterprise?"
Bot: "Great question! Our Enterprise plan includes:
     • Unlimited users & API calls
     • Dedicated support (1h response time)
     • Custom integrations
     • SLA guarantee

     Pricing starts at $5K/month (custom quotes available).
     
     Schedule a demo: [calendly link]
     Or chat with our sales team in #sales-inquiries"
```

---

## Tips & Best Practices

### 1. **Moderation Calibration**
- Start with toxicity threshold at 0.75 (conservative), lower to 0.65 after 2 weeks of tuning
- Monitor false positives weekly; adjust spam filters based on actual violations
- Use "mute" before "ban" to give members a second chance
- Review escalated messages manually to improve AI accuracy

### 2. **Member Engagement Strategy**
- Spotlight top 5 members weekly in #announcements (increases retention by ~15%)
- Proactively reach out to members with retention risk scores >0.6
- Create "member tiers" (Contributor, Expert, Leader) based on scores
- Invite high-value members to leadership council or beta testing

### 3. **Content Strategy**
- Review viral moment recommendations daily; prioritize trending topics
- Host AMAs on top 3 trending discussion topics monthly
- Create tutorials/guides for frequently asked questions
- Use sentiment trends to pivot community focus (if negative, increase recognition events)

### 4. **FAQ Training**
- Start with 20-30 Q&A pairs; add 5-10 new ones weekly based on real questions
- Test FAQ bot in #test-channel before production deployment
- Review bot responses daily for first 2 weeks; adjust as needed
- Create escalation tags for questions requiring human judgment

### 5. **Analytics & Reporting**
- Share weekly health reports with community leads (builds transparency)
- Track week-over-week trends; investigate sudden drops in engagement
- Use member cohort analysis to identify at-risk groups early
- Set health score targets (e.g., "maintain 75+ score") and track progress

---

## Safety & Guardrails

### What This Skill Will NOT Do

- **No Surveillance**: Does not track private DMs or read deleted messages
- **No Discriminatory Moderation**: Will not flag messages based on protected characteristics (race, religion, gender, disability)
- **No False Bans**: Requires human confirmation before permanent bans
- **No Spam Escalation**: Will not auto-ban without mod review; uses graduated warnings
- **No Data Sharing**: Member data stays in your database; never shared with 3rd parties
- **No Impersonation**: Bot always identifies itself; never pretends to be human
- **No Automated Decisions on Account Deletion**: Requires human mod approval

### Boundaries & Limitations

1. **Moderation Bias**: AI toxicity detection (Google Perspective API) can have cultural/linguistic bias. Always review flagged content manually.
2. **Context Blindness**: Bot may miss sarcasm, inside jokes, or context-dependent toxicity. Pair with human judgment.
3. **Escalation Overload**: In communities >10K members, may generate high false-positive rates; recommend manual tuning.
4. **FAQ Hallucination**: GPT-4 may generate plausible-sounding but inaccurate answers. Always review FAQ responses before production.
5. **Member Scoring Opacity**: Composite scores can be hard to interpret; provide detailed breakdowns to members if challenged.
6. **Rate Limits**: Discord API allows ~50 requests/sec; Slack allows ~20 requests/sec. In high-traffic communities, may experience lag.

### Privacy Compliance

- **GDPR**: Supports data export/deletion on request
- **CCPA**: Complies with California privacy rights
- **Discord/Slack ToS**: Fully compliant with platform policies
- **Data Retention**: Configurable (default: 90 days for moderation logs, 1 year for member scores)

---

## Troubleshooting

### Common Issues & Solutions

**Q: Bot is not responding to commands in Discord**
- A: Check that bot has "Send Messages" and "Read Message History" permissions in the channel
- Verify DISCORD_BOT