---
name: linkedin-profile-optimizer-authority-builder
description: "Optimize LinkedIn profiles and build personal authority by analyzing profiles, rewriting headlines/bios for keyword optimization, and recommending content pillars. Use when the user needs LinkedIn positioning, credibility building, or personal branding without a strategist."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["OPENAI_API_KEY", "LINKEDIN_PROFILE_URL"],
        "bins": []
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"],
      "emoji": "🎯"
    }
  }
---

## Overview

The LinkedIn Profile Optimizer & Authority Builder is an AI-powered skill designed for solopreneurs, freelancers, consultants, and small business owners who want to build credibility and visibility on LinkedIn without hiring a brand strategist or copywriter.

This skill automates the entire LinkedIn positioning workflow:
- **Profile Analysis**: Scans your current LinkedIn headline, bio, and experience to identify gaps
- **Keyword Optimization**: Recommends SEO-friendly keywords for discoverability by recruiters, clients, and partners
- **Headline & Bio Rewriting**: Generates 3-5 compelling variations with different positioning angles
- **Content Pillar Strategy**: Suggests 4-6 content themes based on your industry, expertise, and market trends
- **Posting Cadence**: Recommends optimal posting frequency and content formats (articles, posts, videos)
- **Authority Positioning**: Identifies credibility gaps and recommends certifications, testimonials, or social proof additions

**Why This Matters**: LinkedIn's algorithm favors profiles with keyword-rich headlines and consistent content posting. Most solopreneurs leave $50K+ in opportunity on the table by having weak profiles. This skill closes that gap in minutes instead of weeks of strategy calls.

**Integrations**: Works with LinkedIn directly (via profile URL), exports to Google Docs for easy sharing, integrates with content calendars (Notion, Asana), and can post recommendations to Slack for team review.

---

## Quick Start

Try these prompts immediately:

### Prompt 1: Analyze & Optimize Your Current Profile
```
Analyze my LinkedIn profile and provide optimization recommendations.

My current LinkedIn headline is: "Marketing Manager at TechCorp"
My bio summary is: "Digital marketer with 5 years experience in B2B tech. 
I like helping companies grow their customer base."

Industry: B2B SaaS Marketing
Target audience: Marketing directors, founders needing growth strategy
Current pain points: Low profile views, few inbound inquiries
```

**What you'll get**: Profile audit, 5 keyword gaps, 3 headline variations, and bio rewrite suggestions.

---

### Prompt 2: Generate Content Pillar Strategy
```
Create a content pillar strategy for my LinkedIn profile.

My expertise: Email marketing automation, marketing operations, B2B demand generation
My industry: Marketing Technology / SaaS
Ideal clients: CMOs, marketing directors at $10M-$100M revenue companies
Current content gap: I rarely post
Target: Build authority as "go-to person for marketing ops"
```

**What you'll get**: 5-6 content themes, 20+ post ideas, optimal posting cadence, and format recommendations.

---

### Prompt 3: Build 90-Day Authority Plan
```
Build a 90-day LinkedIn authority plan for me.

Current profile strength: Medium (500 connections, 50 posts, some engagement)
Goal: Become recognized expert in customer retention strategies
Industry: SaaS, B2B
Time available: 4 hours/week
Preference: Mix of quick posts, long-form articles, and occasional video
```

**What you'll get**: Week-by-week content calendar, specific post templates, engagement tactics, and success metrics.

---

## Capabilities

### 1. Profile Analysis & Audit
- Scans LinkedIn headline, summary, experience sections, and skills
- Identifies missing keywords competitors are using
- Detects positioning conflicts (e.g., claiming expertise in two unrelated areas)
- Flags underutilized profile sections (recommendations, accomplishments)
- Scores profile completeness and SEO strength (0-100)

**Example Output**:
```
PROFILE AUDIT SCORE: 62/100

STRENGTHS:
✓ Professional photo present
✓ Experience section populated
✓ 420 connections (decent network)

GAPS:
✗ Headline lacks industry keywords ("SaaS," "growth," "B2B")
✗ Summary is vague (generic buzzwords: "passionate," "driven")
✗ No recent recommendations (last one: 18 months ago)
✗ Skills section not endorsed (limits algorithm visibility)

QUICK WINS:
1. Add 3-4 industry keywords to headline (+25% view increase)
2. Rewrite summary with specific metrics (-15% bounce rate)
3. Request 5 recommendations this month
```

### 2. AI-Powered Headline & Bio Generation
- Creates 5 headline variations targeting different positioning angles
- Includes keyword-rich bios that pass LinkedIn's algorithm
- Balances keyword optimization with human readability
- Includes call-to-action (CTA) strategies embedded in bio

**Example Output**:
```
ORIGINAL: "Marketing Manager at TechCorp"

VARIATION 1 (KEYWORD-HEAVY):
"B2B SaaS Marketing Manager | Demand Generation Specialist | 
LinkedIn Growth Strategist | HubSpot Certified"

VARIATION 2 (AUTHORITY-FOCUSED):
"Help SaaS Companies Grow to 7-Figures | Marketing Strategy & 
Demand Gen | Featured in Forbes/HubSpot"

VARIATION 3 (CLIENT-BENEFIT):
"Marketing Growth Expert for $5M-$50M SaaS Founders | 
3x Revenue Growth | Speaking at 15+ Conferences"

[...2 more variations...]

RECOMMENDED: Variation 2 (highest keyword match + authority signal)
```

### 3. Content Pillar & Theme Strategy
- Analyzes your expertise and audience needs
- Suggests 4-6 evergreen content pillars
- Recommends content format mix (carousel posts, articles, videos, case studies)
- Provides 20+ specific post ideas ready to adapt

**Example Output**:
```
CONTENT PILLARS FOR YOUR PROFILE:

Pillar 1: "Email Marketing ROI" (30% of posts)
  └─ Why your email strategy is failing
  └─ 5-email sequences that convert
  └─ A/B testing frameworks

Pillar 2: "Marketing Operations" (25% of posts)
  └─ Tools that save 10 hours/week
  └─ Building a scalable martech stack
  └─ Automation workflows for teams

Pillar 3: "Founder Stories/Case Studies" (25% of posts)
  └─ "How we grew from 0 to 10K subscribers"
  └─ Client win stories (anonymized)
  └─ Behind-the-scenes founding lessons

Pillar 4: "Industry Trends/News" (20% of posts)
  └─ Weekly roundup of marketing news
  └─ React to LinkedIn algorithm changes
  └─ Thought leadership on emerging tech
```

### 4. Optimal Posting Cadence & Timing
- Recommends posting frequency (1x daily, 3x weekly, etc.)
- Suggests best days/times based on your industry and audience
- Provides format distribution (60% text, 20% articles, 20% video)
- Includes engagement acceleration tactics

**Example Output**:
```
RECOMMENDED POSTING CADENCE: 3-4 posts per week

OPTIMAL TIMING:
  Tuesday-Thursday, 8-10 AM ET (highest B2B engagement)
  Or 6-8 PM ET (when professionals browse casually)

FORMAT MIX:
  • 50% Quick insights (3-5 line posts with 1 image)
  • 30% Articles (1,200-1,500 word deep-dives)
  • 15% Carousels (educational swipe decks)
  • 5% Video (1-2 min tips or behind-the-scenes)

ENGAGEMENT MULTIPLIERS:
  1. Post, then engage with 10-15 related posts in your field (next 30 min)
  2. Reply to first 5-10 comments within 1 hour (boosts algorithm)
  3. Share others' content 2x per week (builds reciprocity)
```

### 5. Authority & Credibility Gap Analysis
- Identifies missing social proof elements (recommendations, certifications, speaking)
- Suggests specific certifications or badges to pursue
- Recommends how to highlight existing authority signals
- Provides templates for requesting testimonials

**Example Output**:
```
CREDIBILITY GAPS:

Gap 1: No Media Features (Medium risk)
  Action: Pitch yourself to 3 industry publications this month
  Template provided: "Expert Commentary Pitch Template"

Gap 2: Limited Speaking Experience (High risk)
  Action: Apply to 5 podcasts + 2 conference panels
  Resource: "How to Get Booked on High-Traffic Podcasts"

Gap 3: No LinkedIn Certifications (Medium risk)
  Action: Complete HubSpot Academy Marketing Cert (5 hours)
  Benefit: +18% profile views when displayed

QUICK WIN:
  Request 5 recommendations this week (template in exports)
  Each recommendation = +12% profile credibility score
```

---

## Configuration

### Environment Variables (Required)
```bash
# OpenAI API for AI analysis and writing
export OPENAI_API_KEY="sk-proj-..."

# Your LinkedIn profile URL (or extracted profile data)
export LINKEDIN_PROFILE_URL="https://linkedin.com/in/yourprofile"

# Optional: LinkedIn API key for direct integration (if available)
export LINKEDIN_API_KEY="your-api-key" # Optional
```

### Setup Instructions

1. **Get Your LinkedIn Profile Data**:
   - Copy your LinkedIn profile URL
   - Or manually paste your current headline + bio + summary text

2. **Provide Context**:
   - Industry/niche
   - Target audience (job titles, company size)
   - Business goals (build authority, get clients, find a job, etc.)
   - Time commitment (hours/week available for content)

3. **Choose Optimization Focus** (optional):
   - `full-audit`: Comprehensive profile + content strategy
   - `headline-only`: Quick headline rewrite
   - `content-pillars`: Just the content strategy
   - `authority-gaps`: Credibility & social proof recommendations

---

## Example Outputs

### Sample Profile Optimization Report

**PROFILE ANALYSIS FOR: Sarah Chen, Marketing Consultant**

```
CURRENT HEADLINE: "Helping B2B companies grow | Marketing strategist"
CURRENT BIO: "I'm passionate about marketing and helping businesses 
succeed. 10+ years experience."

ANALYSIS:
  ✗ Headline lacks specificity (which companies? what growth metrics?)
  ✗ Bio uses clichés ("passionate," "helping businesses")
  ✗ No keywords that match search intent
  ✗ Missing unique value proposition

RECOMMENDED HEADLINE:
"B2B SaaS Growth Strategist | $5M-$50M Revenue Scale | 
Marketing Operations Specialist"
  • +4 high-intent keywords
  • +2 credibility signals (specific revenue range)
  • Estimated +35% profile view increase

RECOMMENDED BIO:
"I help B2B SaaS companies scale from $5M to $50M revenue through 
integrated marketing operations and demand generation.

Specializations:
• Revenue-aligned marketing strategies
• MarTech stack optimization (HubSpot, Marketo, Salesloft)
• Demand generation (pipeline: $2M-$10M/year)

Recent wins: Helped 7 clients increase pipeline 40-60% in 6 months.

Let's talk growth → [Link to booking page]"

ESTIMATED IMPACT:
  • Profile views: +35-50%
  • Qualified inquiries: +60-80%
  • Connection requests: +25%
```

### Sample Content Calendar (30-Day Preview)

```
WEEK 1:
Mon: "3 email marketing metrics that actually matter" (quick post)
Wed: Article: "Why your marketing ops are costing you $50K/year"
Fri: Carousel: "5-step martech stack audit template"

WEEK 2:
Tue: "The #1 reason demand gen fails (and how to fix it)"
Thu: Client case study: "From 200 to 2,000 qualified leads/month"
Sat: "Weekly marketing ops roundup" (curated news)

WEEK 3:
Mon: Video: "30-sec demo of our favorite automation workflow"
Wed: Article: "Demand generation framework for B2B SaaS"
Fri: "Honest take: Is HubSpot worth the cost for early-stage companies?"

WEEK 4:
Tue: "5 questions to ask before hiring a marketing ops manager"
Thu: Podcast announcement: "I'm speaking at The Growth Pod!"
Sun: Month recap: "What I learned about SaaS marketing in September"
```

---

## Tips & Best Practices

### 1. Profile Optimization
- **Update sparingly but strategically**: Change headline/bio once every 6-12 months (too-frequent changes signal instability)
- **Use the 10% keyword rule**: Include 3-4 high-intent keywords in headline, but keep it readable for humans
- **Add a CTA**: "Open to: partnerships / speaking / consulting" tells LinkedIn's algorithm what you want
- **Complete all sections**: A 100% complete profile gets 40x more views than a 50% complete one

### 2. Content Pillars & Consistency
- **Choose 4-6 pillars, not 10+**: Depth beats breadth. Master 4 topics vs. scattered across 20
- **Batch-create content**: Spend 2 hours writing 8 posts instead of writing 1 post each day (saves 10 hours/month)
- **Use the 80/20 rule**: 80% educational/entertaining, 20% self-promotion
- **Repurpose ruthlessly**: One article = 8 LinkedIn posts, 1 email, 1 newsletter, 2 tweets

### 3. Engagement & Algorithm
- **Reply to comments within 1 hour**: First 30 min = 5x algorithm boost
- **Engage with similar accounts daily**: Spend 15 min liking/commenting on 15 related posts (builds reciprocal engagement)
- **Use hashtags strategically**: 3-5 hashtags per post, mix popular (#Marketing) + niche (#MarketingOps)
- **Hook in first 2 lines**: LinkedIn cuts off long posts—make the first sentence compelling

### 4. Authority Building
- **Request recommendations strategically**: Ask after a successful project, not randomly
- **Feature client wins (anonymized)**: "Helped a $20M SaaS grow pipeline 50%" (no naming names)
- **Speak or write elsewhere**: Cross-post articles to Medium, speak at webinars, publish on industry sites
- **Build in public**: Share your process, learnings, and failures—vulnerability builds trust

### 5. Measurement & Iteration
- **Track 3 metrics only**: Profile views, post impressions, engaged leads (don't obsess over follower count)
- **A/B test headlines**: Try 2 variations of the same topic, see which gets more engagement
- **Review monthly**: Every 30 days, analyze top-performing posts and double down on those themes
- **Adjust cadence if needed**: If posting 4x/week feels unsustainable, drop to 2-3x/week (consistency > frequency)

---

## Safety & Guardrails

### What This Skill Will NOT Do

- **Will NOT scrape LinkedIn data** (violates LinkedIn Terms of Service). You must manually provide your profile information
- **Will NOT generate false credentials or exaggerated claims** that could damage your reputation legally
- **Will NOT encourage deceptive practices**: All recommendations follow LinkedIn's guidelines and ethical marketing standards
- **Will NOT create spam or engagement-bait content**: Avoids clickbait, fake urgency, or manipulative tactics
- **Will NOT store your LinkedIn credentials or personal data** (all processing is stateless; no data persistence)

### Limitations & Boundaries

1. **LinkedIn Algorithm Volatility**: Recommendations are based on current best practices, but LinkedIn changes its algorithm frequently. What works today may need adjustment in 6 months.

2. **Individual Variation**: Results vary based on your network size, industry, and posting consistency. A 500-person network won't see the same results as a 50K network, even with perfect content.

3. **Authenticity Required**: This skill generates frameworks and content ideas, but YOUR voice and experiences must come through. Generic templates won't resonate—you must adapt and person