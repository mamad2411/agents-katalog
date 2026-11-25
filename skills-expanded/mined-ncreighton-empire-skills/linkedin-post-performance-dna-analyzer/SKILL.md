---
name: linkedin-post-performance-dna-analyzer
description: "Reverse-engineer LinkedIn engagement patterns from your top 100 posts to identify hook structures, emotional triggers, and CTAs. Use when the user needs to decode their personal posting formula, generate performance templates, or score new drafts before publishing."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {"openclaw":{"requires":{"env":["LINKEDIN_API_TOKEN","OPENAI_API_KEY"],"bins":["python3","curl"]},"os":["macos","linux","win32"],"files":["SKILL.md"],"emoji":"🧬"}}
---

## Overview

**LinkedIn Post Performance DNA Analyzer** decodes the hidden engagement formula in your personal LinkedIn content by reverse-engineering your top 100 posts. This skill identifies the specific patterns that drive YOUR audience engagement—hook structures, emotional trigger words, call-to-action patterns, optimal post length ranges, posting times, and content themes—then generates a personalized "DNA template" you can use to consistently replicate winning posts.

Instead of guessing what works, you'll have a data-backed blueprint of your unique engagement drivers. The skill then scores new draft posts against your personal DNA profile before you publish, flagging misalignments and suggesting improvements.

### Why This Matters

LinkedIn algorithm rewards consistency and authenticity. Generic content advice ("use power words," "post at 8am") fails because every creator's audience is different. This skill finds YOUR specific formula by analyzing thousands of data points from your actual posts, then helps you stay on-brand while maximizing reach and engagement.

**Perfect for:** Thought leaders, B2B marketers, personal brands, sales professionals, executive coaches, and content strategists who want to scale their LinkedIn presence with predictable, data-driven content.

### Integrations & APIs Used
- **LinkedIn API v2** (official post analytics endpoint)
- **OpenAI GPT-4** (pattern analysis and scoring)
- **Google Sheets** (optional export of DNA templates and scores)
- **Slack** (optional notifications of draft scores)

---

## Quick Start

Try these prompts to get started immediately:

### Example 1: Build Your DNA Profile
```
Analyze my LinkedIn DNA. Pull my top 100 posts using the LinkedIn API, 
then identify the engagement patterns (hooks, emotional language, CTAs, 
average length, optimal posting times). Generate a personalized DNA template 
showing my unique formula for success. Export as a PDF reference guide.
```

### Example 2: Score a New Draft
```
I wrote this LinkedIn post draft: "Just closed a $500K deal after 18 months 
of cold outreach. Here's what actually works: 1) Consistency beats perfection 
2) Your network is your net worth 3) Follow up 7x minimum. Who's applying this?"

Score this against my personal LinkedIn DNA profile. Rate it 1-10 against my 
engagement patterns. Suggest 3 edits to maximize performance.
```

### Example 3: Generate Weekly Content Ideas
```
Based on my LinkedIn DNA profile, generate 5 post ideas for next week that 
align with my top engagement drivers. For each idea, provide: the hook structure, 
emotional angle, recommended length, suggested CTA, and predicted engagement range.
```

### Example 4: Identify Your Content Gaps
```
Show me the engagement patterns in my top 100 LinkedIn posts. What themes or 
hooks am I underutilizing? Which posting times and post lengths drive the most 
engagement? Recommend 3 content experiments to test new DNA variations.
```

---

## Capabilities

### 1. **Reverse-Engineer Your LinkedIn DNA**
- Fetches your last 100 published LinkedIn posts via official LinkedIn API v2
- Analyzes engagement metrics: impressions, clicks, comments, shares, reposts
- Identifies hook patterns: questions, stories, data, contrasts, time-sensitive hooks
- Extracts emotional triggers: urgency, curiosity, FOMO, aspiration, relatability
- Maps CTA patterns: soft CTAs (questions), medium CTAs (invitations), hard CTAs (link/download)
- Calculates optimal content length ranges (50-150 words, 150-300 words, 300+ words)
- Identifies ideal posting times and days of week
- Tags content themes and topics with correlation to engagement
- Scores post type performance: carousel slides, document posts, video, text-only, polls

**Usage Example:**
```
Get my LinkedIn DNA baseline report showing all engagement patterns 
in my top 100 posts, including hook types, emotional language frequency, 
CTA effectiveness, and optimal posting windows.
```

### 2. **Generate Personalized DNA Templates**
- Creates a structured "Your LinkedIn DNA" document with your unique formula
- Templates include: 5 winning hook formulas, 10 high-performing CTAs, 
  emotional language patterns, recommended post structures, optimal posting calendar
- Provides before/after examples of posts that matched vs. didn't match your DNA
- Includes engagement benchmarks (your avg. impressions, comments, CTR vs. LinkedIn average)
- Exports templates to multiple formats: PDF, Google Sheets, Notion, Markdown

**Usage Example:**
```
Create my LinkedIn DNA template as a Notion database where I can browse 
my top hooks, CTAs, and themes. Include engagement score for each pattern 
so I can see what works best.
```

### 3. **Score New Drafts Against Your DNA**
- Analyzes draft posts against your personalized DNA profile
- Scores on 1-10 scale with breakdown: hook strength, emotional alignment, CTA effectiveness, length appropriateness, timing match
- Flags misalignments ("Your hook uses questions 80% of the time, but this draft has no hook")
- Suggests specific edits to improve DNA alignment
- Provides predicted engagement range based on DNA match score
- Optional Slack integration for instant draft scoring

**Usage Example:**
```
Score this draft against my DNA and suggest edits: "Excited to announce 
I'm joining a new startup! Can't wait to share more soon." Predict engagement 
if I publish tomorrow at 9am EST.
```

### 4. **Generate Content Ideas Aligned to DNA**
- Creates 5-10 weekly content ideas that match your DNA patterns
- Each idea includes: hook structure, emotional angle, recommended length, CTA formula, predicted engagement
- Allows filtering by content theme, post type, or engagement goal
- Provides swipe files of similar high-performing posts as inspiration
- Generates full post outlines ready for personalization

**Usage Example:**
```
Generate 5 LinkedIn post ideas for next week that match my DNA. 
I want to focus on sales and leadership themes. For each, show the 
hook structure, length recommendation, and engagement prediction.
```

### 5. **Identify Untapped Engagement Opportunities**
- Analyzes gaps in your content strategy
- Shows themes you rarely use but that performed well when you did
- Identifies underutilized hook types and CTAs
- Recommends content experiments based on top performer patterns
- Suggests new angles on your most successful themes

**Usage Example:**
```
What's my LinkedIn DNA missing? Show me engagement opportunities 
I haven't fully explored yet. Recommend 3 content experiments to test 
new DNA variations and expand my reach.
```

---

## Configuration

### Required Environment Variables

Set these before using the skill:

```bash
# LinkedIn API Authentication
export LINKEDIN_API_TOKEN="urn:li:digitalmediaAsset:xyz123..."

# OpenAI for pattern analysis
export OPENAI_API_KEY="sk-proj-..."

# Optional: Slack integration for draft scoring notifications
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."

# Optional: Google Sheets export
export GOOGLE_SHEETS_API_KEY="AIzaSy..."
```

### Configuration Options

The skill accepts these optional parameters:

```yaml
analysis:
  post_count: 100                    # Number of posts to analyze (default: 100, max: 500)
  engagement_metric: "combined"      # "combined", "impressions", "engagement_rate", "shares"
  date_range: "last_6_months"        # "last_3_months", "last_6_months", "all_time"

dna_report:
  format: "pdf"                      # "pdf", "sheets", "notion", "markdown"
  include_benchmarks: true           # Compare your metrics to LinkedIn averages
  export_destination: "email"        # "email", "slack", "gdrive", "local"

scoring:
  prediction_model: "conservative"   # "conservative", "balanced", "aggressive"
  include_suggestions: true          # Provide edit suggestions for low-scoring drafts
  notify_channel: "slack"            # "slack", "email", "none"
```

### Setup Instructions

1. **Generate LinkedIn API Token:**
   - Go to linkedin.com/developers
   - Create an app and request access to Official LinkedIn API (Post Introspection)
   - Generate a User Access Token with scope: `w_member_social`

2. **Get OpenAI API Key:**
   - Visit platform.openai.com/api-keys
   - Create a new secret key with `gpt-4` and `text-embedding-3-large` access

3. **Optional Slack Setup:**
   - Create an Incoming Webhook: api.slack.com/messaging/webhooks
   - Copy webhook URL to `SLACK_WEBHOOK_URL`

4. **Authenticate:**
   ```bash
   source ~/.openclaw/env
   openclaw skill install linkedin-post-performance-dna-analyzer
   ```

---

## Example Outputs

### Output 1: LinkedIn DNA Profile Report

```
═══════════════════════════════════════════════════════════════
YOUR LINKEDIN DNA PROFILE
═══════════════════════════════════════════════════════════════

ENGAGEMENT ANALYSIS (Top 100 Posts, Last 6 Months)
─────────────────────────────────────────────────────────────
Average Impressions:        4,847 (vs LinkedIn avg: 1,200)
Average Engagement Rate:    2.3% (vs LinkedIn avg: 0.6%)
Average Comments:           12 (vs LinkedIn avg: 3)
Average Shares:             4 (vs LinkedIn avg: 1)
Top Post Performance:       18,234 impressions | 8.4% engagement rate

HOOK DNA (Top 5 Winning Patterns)
─────────────────────────────────────────────────────────────
1. QUESTION HOOKS (45% of top posts)
   Example: "What's the #1 reason your cold outreach fails?"
   Avg Engagement: 3.8% | Avg Comments: 18

2. STORY HOOKS (28% of top posts)
   Example: "I spent 18 months cold outreach before I found..."
   Avg Engagement: 2.1% | Avg Comments: 8

3. CONTRARIAN HOOKS (18% of top posts)
   Example: "Your network advice is wrong. Here's why..."
   Avg Engagement: 4.2% | Avg Comments: 22

4. DATA HOOKS (7% of top posts)
   Example: "Study: 87% of salespeople ignore this..."
   Avg Engagement: 1.9% | Avg Comments: 5

5. TIME-SENSITIVE HOOKS (2% of top posts)
   Example: "Only 48 hours left: Here's what I learned..."
   Avg Engagement: 5.1% | Avg Comments: 31

EMOTIONAL TRIGGER DNA
─────────────────────────────────────────────────────────────
Primary Triggers (highest correlation to engagement):
✓ Vulnerability/Authenticity (+82% engagement lift)
✓ Curiosity/Mystery (+71% engagement lift)
✓ Urgency/FOMO (+65% engagement lift)
✓ Aspiration/Inspiration (+58% engagement lift)
✓ Relatability/Struggle (+54% engagement lift)

CALL-TO-ACTION DNA (Top 5 Patterns)
─────────────────────────────────────────────────────────────
1. SOFT CTA - Question Engagement (52% of top posts)
   Example: "What's working for you?"
   Avg Engagement: 3.4% | Highest comment volume

2. MEDIUM CTA - Invitation (32% of top posts)
   Example: "Save this for later / Drop a comment if..."
   Avg Engagement: 2.1% | High share rate

3. HARD CTA - Resource Link (12% of top posts)
   Example: "Read the full analysis here → [link]"
   Avg Engagement: 1.8% | Highest click-through rate

4. COLLABORATIVE CTA (3% of top posts)
   Example: "Tag someone who needs to see this"
   Avg Engagement: 4.7% | High share + comment combo

5. NO CTA (1% of top posts)
   Avg Engagement: 0.9% | Not recommended pattern

OPTIMAL POST LENGTH DNA
─────────────────────────────────────────────────────────────
50-150 words:      2.1% avg engagement | 35% of top posts
150-300 words:     3.4% avg engagement | 48% of top posts ⭐ OPTIMAL
300+ words:        1.8% avg engagement | 17% of top posts

POSTING TIME DNA
─────────────────────────────────────────────────────────────
Highest engagement times:
• Tuesday 8-10am EST     (3.8% avg engagement)
• Wednesday 1-3pm EST    (3.5% avg engagement)
• Thursday 9-11am EST    (3.3% avg engagement)

Lowest engagement times:
• Friday 5-7pm EST       (0.9% avg engagement)
• Saturday/Sunday        (1.1% avg engagement)

CONTENT THEME DNA
─────────────────────────────────────────────────────────────
1. Sales/Cold Outreach (34% of posts) → 3.1% avg engagement ⭐
2. Leadership/Team Building (28% of posts) → 2.8% avg engagement
3. Career Transitions (16% of posts) → 2.2% avg engagement
4. Industry Insights (14% of posts) → 1.9% avg engagement
5. Personal Wins (8% of posts) → 4.1% avg engagement ⭐ HIGHEST

YOUR DNA FORMULA SUMMARY
─────────────────────────────────────────────────────────────
Use QUESTION HOOKS (80% of the time) + VULNERABILITY/AUTHENTICITY
+ CURIOSITY TRIGGER + 150-300 word length + SOFT CTA (question engagement)
+ Post on Tuesday-Thursday mornings EST + Focus on Sales/Personal themes

This formula drives 3.4% avg engagement vs your 2.3% baseline.
```

### Output 2: Draft Scoring Report

```
═══════════════════════════════════════════════════════════════
LINKEDIN DRAFT SCORING ANALYSIS
═══════════════════════════════════════════════════════════════

DRAFT TEXT:
"Just closed a $500K deal after 18 months of cold outreach. 
Here's what actually works: 1) Consistency beats perfection 
2) Your network is your net worth 3) Follow up 7x minimum. 
Who's applying this?"

DNA MATCH SCORE: 8.2/10 ⭐ STRONG ALIGNMENT
─────────────────────────────────────────────────────────────

COMPONENT BREAKDOWN:

Hook Analysis: 7/10
✓ Uses STORY HOOK (matches your 28% top pattern)
✓ Leads with achievement/vulnerability
✗ Could strengthen with upfront hook line
Suggestion: Start with "After 18 months of cold outreach, 
I finally cracked the code..." to create more immediate curiosity.

Emotional Triggers: 9/10
✓ VULNERABILITY: "18 months" shows struggle/persistence
✓ ASPIRATION: $500K deal is aspirational
✓ RELATABILITY: Cold outreach struggle is relatable
Perfect alignment with your top emotional drivers.

CTA Analysis: 8/10
✓ Uses SOFT CTA (question): "Who's applying this?"
✓ Matches your highest-performing CTA pattern
✓ Invites engagement and comment responses
Very strong here. This will drive high comment volume.

Post Length: 8.5/10
Word Count: 82 words (including headline)
Your optimal range: 150-300 words
Suggestion: Expand with personal story or specific numbers
to reach 180-220 word range for maximum engagement.

Content Theme: 9/10
✓ Personal Win + Sales/Outreach hybrid
✓ Matches your top 2 performing themes
Highly aligned with your audience expectations.

Posting Time Recommendation: Tuesday 8-10am EST
Predicted Engagement: 3.6-4.1% (vs your 2.3% baseline)