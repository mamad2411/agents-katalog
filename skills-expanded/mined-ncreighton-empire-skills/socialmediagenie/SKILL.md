---
name: socialmediagenie
description: "Generate engaging social media posts, captions, and visual content strategies across platforms. Use when the user needs Instagram content, TikTok scripts, LinkedIn posts, or multi-platform campaigns with AI-powered tone customization."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["OPENAI_API_KEY", "ANTHROPIC_API_KEY"],
        "bins": []
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"],
      "emoji": "✨"
    }
  }
---

## Overview

**SocialMediaGenie** automates social media content creation for businesses, agencies, and creators who need high-quality, platform-optimized posts without the time investment. This skill generates engaging captions, hashtag strategies, content calendars, and visual direction in seconds—eliminating writer's block and ensuring brand consistency across Instagram, TikTok, LinkedIn, Twitter, Facebook, and YouTube.

### Why It Matters

Social media content creation is the #1 time drain for small businesses and agencies. Posting consistently across 5+ platforms while maintaining brand voice is exhausting. SocialMediaGenie solves this by:

- **Generating platform-specific content** (Instagram Reels captions differ from LinkedIn thought leadership)
- **Maintaining brand voice** across all posts through customizable tone profiles
- **Creating content calendars** with themes, hashtags, and posting schedules
- **Integrating with WordPress, Buffer, Hootsuite, and Slack** for seamless workflow
- **Producing visual briefs** for designers and video creators
- **Scaling content production** from 5 posts/week to 50+ without quality loss

Perfect for: SaaS companies, e-commerce brands, personal brands, agencies, nonprofits, and creators.

---

## Quick Start

### Example 1: Generate Instagram Content Series

```
Create 5 Instagram carousel post captions for a sustainable fashion brand targeting eco-conscious millennials. 
Topics: sustainable fabric sourcing, behind-the-scenes manufacturing, customer testimonials, seasonal trends, and care tips.
Tone: conversational, inspiring, with 15-20 relevant hashtags per post.
Include call-to-action for each post.
```

**What you'll get:** 5 complete carousel captions with hashtags, CTAs, and emoji suggestions—ready to copy/paste into Instagram.

### Example 2: LinkedIn Thought Leadership Thread

```
Write a 5-part LinkedIn thread about AI adoption in small businesses.
Target audience: founders and CEOs with 10-100 employees.
Tone: authoritative but approachable, include 1-2 statistics per post.
End with a soft CTA (link to resource or poll).
Include engagement hooks for each post.
```

**What you'll get:** 5 LinkedIn posts designed for maximum engagement, with built-in discussion starters.

### Example 3: TikTok Content Calendar (2 Weeks)

```
Generate a 2-week TikTok content calendar for a fitness coaching brand.
Content mix: 40% educational (workout tips), 30% entertaining (trending sounds), 20% testimonials, 10% behind-the-scenes.
Include video concepts, trending audio suggestions, hashtag strategies, and posting times.
Target audience: women 18-35 interested in fitness.
```

**What you'll get:** 14 video concepts with scripts, trending audio links, hashtags, and optimal posting times.

### Example 4: Multi-Platform Campaign Brief

```
Create a 4-week content campaign for a new SaaS product launch.
Platforms: Instagram, LinkedIn, Twitter, TikTok, YouTube.
Tone: professional yet approachable, emphasize ROI and efficiency.
Include 5 posts per platform, visual direction for designers, and a content calendar with posting schedule.
```

**What you'll get:** 20+ platform-specific posts + visual briefs + calendar + hashtag strategy.

---

## Capabilities

### 1. Platform-Specific Content Generation
- **Instagram**: Captions (feed posts, Reels, Stories), hashtag strategies, carousel concepts
- **TikTok**: Video scripts, trending audio suggestions, hook strategies, hashtag optimization
- **LinkedIn**: Thought leadership posts, industry insights, company updates, job postings
- **Twitter/X**: Threads, hot takes, news commentary, engagement bait, quote tweets
- **Facebook**: Community posts, event promotions, customer stories, group discussions
- **YouTube**: Video titles, descriptions, SEO-optimized tags, thumbnail concepts

### 2. Tone & Brand Voice Customization
Define your brand voice once, apply it to all content:
- Professional / Casual / Humorous / Inspirational / Educational / Provocative
- Adjust vocabulary, emoji usage, formality level, and personality
- Maintain consistency across 50+ posts automatically

### 3. Content Calendar Generation
- Multi-week planning with themes and topics
- Optimal posting times per platform (based on audience timezone)
- Content mix ratios (educational, promotional, entertaining, engagement)
- Seasonal adjustments and holiday tie-ins
- CSV/JSON export for Buffer, Hootsuite, or Sprout Social

### 4. Hashtag & SEO Strategy
- Trending hashtag research (Instagram, TikTok, Twitter)
- Mix of high-volume and niche hashtags
- Hashtag performance predictions
- Competitor hashtag analysis
- Seasonal hashtag calendars

### 5. Visual Direction & Design Briefs
- Color palette suggestions aligned with brand
- Typography and layout recommendations
- Video editing style guides
- Thumbnail concepts for YouTube/TikTok
- Image composition tips for designers

### 6. Engagement Optimization
- Hook-based copy that stops scrolls
- Strategic CTA placement and messaging
- Question-based engagement prompts
- Poll and quiz concepts
- Comment-baiting strategies (ethical)

### 7. Analytics-Informed Content
- Content performance predictions
- A/B testing suggestions
- Audience sentiment analysis
- Competitor content benchmarking
- Trending topic integration

---

## Configuration

### Environment Variables (Required)

```bash
# OpenAI API key for GPT-4 content generation
OPENAI_API_KEY=sk-your-key-here

# Anthropic API key for Claude-based tone analysis
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### Brand Profile Setup

Before generating content, define your brand once:

```json
{
  "brand_name": "EcoThread",
  "industry": "sustainable fashion",
  "target_audience": "eco-conscious millennials, 25-40, urban",
  "brand_voice": "conversational, inspiring, authentic",
  "tone_keywords": ["warm", "educational", "optimistic"],
  "values": ["sustainability", "transparency", "quality"],
  "emoji_usage": "moderate",
  "hashtag_style": "mix of trending and niche",
  "posting_timezone": "America/New_York",
  "content_pillars": [
    "Sustainable sourcing",
    "Customer stories",
    "Behind-the-scenes",
    "Care & longevity",
    "Industry insights"
  ]
}
```

### Integration Setup

**Slack Integration:**
```
/socialmediagenie generate instagram 5 posts for sustainable fashion
```

**WordPress Integration:**
Schedule generated posts directly to WordPress social media plugins (Jetpack, Social Snap).

**Buffer/Hootsuite:**
Export calendar as CSV for direct import into scheduling tools.

**Google Sheets:**
Auto-populate content calendar into shared team spreadsheet.

---

## Example Outputs

### Instagram Carousel Post (Generated)

```
📱 Post 1 of 5: Sustainable Fabric Sourcing

Caption:
"Ever wonder where your clothes actually come from? 🌱 

We partner with certified organic cotton farms in India and deadstock fabric suppliers to minimize waste. Each garment tells a story of sustainability—from soil to closet.

Our goal? Zero waste by 2025. We're at 73% right now. 🎯

Swipe to see our supply chain! ➡️

#SustainableFashion #EthicalStyle #OrganicCotton #TransparencyMatters #EcoFashion #SlowFashion #SustainableStyle #FashionWithPurpose #GreenLiving #ConsciousConsumer #EcoThread #FashionIndustry #TextileWaste #SustainableSourcing"

Hashtags: 14
Emoji: 3
CTA: Swipe engagement
Best Posting Time: Tuesday 10:30 AM EST
Estimated Reach: 8,400-12,100 (based on account size)
```

### TikTok Video Script (Generated)

```
🎬 Video Concept: "How We Upcycle Fashion Waste"

Hook (0-3 sec): 
"Wait, this is made from trash? 🤔"

Main Content (3-20 sec):
- Show pile of fabric scraps
- Time-lapse of sorting by color
- Sewing/assembly process
- Final product reveal
- Model wearing finished piece

Trending Audio: 
"Levitating" by Dua Lipa (9.2M uses, trending in Fashion niche)

Hashtags:
#FashionHaul #SustainableFashion #UpcycledFashion #DIY #FashionTok #EcoFriendly #ZeroWaste #BeforeAndAfter

Optimal Posting Time: Thursday 6:00 PM EST
Expected Views: 15,000-45,000 (trending audio + hook)
```

### LinkedIn Thought Leadership Post (Generated)

```
🔗 LinkedIn Post: "The Hidden Cost of Fast Fashion (And Why Your Supply Chain Matters)"

Caption:
The fashion industry produces 92 million tons of textile waste annually. But here's what most leaders miss: your supply chain IS your brand story.

We spent 18 months mapping ours. What we found:
• 63% of our fabric came from suppliers with zero sustainability practices
• Our carbon footprint per garment: 8.2 kg CO2 (industry average: 6.5 kg)
• Our customers had NO idea

So we rebuilt it.

Today, 100% of our cotton is certified organic, 73% of our materials are deadstock/upcycled, and we publish our supply chain publicly.

The result? 
→ Customer loyalty increased 340%
→ Wholesale partnerships tripled
→ Media coverage: Forbes, Vogue, Business Insider

The brands winning in 2024 aren't hiding their supply chains—they're weaponizing them.

What's your biggest supply chain challenge? Drop it in the comments. 👇

#Sustainability #SupplyChain #EthicalBusiness #Leadership #Fashion #SocialImpact #Transparency

Engagement Hooks: 2 questions, 1 controversial stat, 1 CTA
Predicted Engagement Rate: 6.2% (vs. LinkedIn average 1.8%)
```

### Content Calendar (2-Week Sample)

| Date | Platform | Content Type | Topic | Hashtags | Posting Time | Status |
|------|----------|--------------|-------|----------|--------------|--------|
| Mon 1/15 | Instagram | Carousel | Sustainable Sourcing | #EcoThread #SustainableFashion | 10:30 AM | Draft |
| Tue 1/16 | TikTok | Video Script | Upcycling Process | #FashionTok #ZeroWaste | 6:00 PM | Draft |
| Wed 1/17 | LinkedIn | Thought Leadership | Supply Chain Transparency | #Leadership #Sustainability | 9:00 AM | Draft |
| Thu 1/18 | Twitter | Thread | Fashion Industry Stats | #Fashion #Sustainability | 2:00 PM | Draft |
| Fri 1/19 | Instagram | Story Series | Customer Testimonial | #CustomerLove #EcoThread | 7:00 PM | Draft |

---

## Tips & Best Practices

### 1. Define Your Content Pillars First
Before generating 100 posts, identify 5-7 core topics your brand owns:
- For SaaS: Product updates, industry insights, customer stories, thought leadership, behind-the-scenes
- For e-commerce: Product features, customer testimonials, behind-the-scenes, care tips, industry trends
- For personal brand: Expertise sharing, daily lessons, personal stories, hot takes, Q&A

**Pro tip:** SocialMediaGenie generates better content when you specify pillars. It prevents repetition and keeps your feed intentional.

### 2. Use Platform-Specific Prompts
Instagram captions ≠ LinkedIn posts. Be explicit:
```
Create an Instagram caption (max 150 words, 8-12 hashtags, casual tone)
vs.
Create a LinkedIn post (max 1,300 characters, professional tone, 1 stat, 1 CTA)
```

### 3. A/B Test Your Tone
Generate the same post in 2-3 tones (professional, casual, humorous) and test which resonates:
```
Rewrite this LinkedIn post in 3 versions:
1. Authoritative (expert voice)
2. Conversational (friend talking)
3. Provocative (contrarian take)
```

### 4. Batch Content Creation
Don't generate 1 post at a time. Create 2-4 weeks of content in one session:
- Faster workflow
- Consistent quality
- Easier to spot themes/repetition
- Better for scheduling tools

### 5. Customize Hashtag Mix
Balance hashtag types:
- 30% high-volume (1M+ posts): reach, but harder to rank
- 50% mid-volume (100K-1M posts): sweet spot
- 20% niche (under 100K): your target audience

SocialMediaGenie calculates this automatically if you specify "balanced" hashtag strategy.

### 6. Leverage Trending Topics
Ask SocialMediaGenie to tie posts to trending topics:
```
Create 3 Instagram posts about [your product] that reference trending topics this week 
(check Twitter, TikTok, Google Trends).
```

### 7. Schedule for Your Audience's Timezone
Optimal posting times vary by platform AND audience:
- Instagram: 10-11 AM, 7-9 PM (EST)
- TikTok: 6-10 PM (EST)
- LinkedIn: 8-10 AM, 12 PM (EST)
- Twitter: 9 AM, 5 PM (EST)

SocialMediaGenie adjusts times based on your audience timezone (set in brand profile).

### 8. Use Visual Briefs for Design Handoff
Generate visual direction for your designer:
```
Create a visual brief for 4 Instagram carousel posts about sustainable sourcing.
Include: color palette, typography style, layout suggestions, and mood board references.
```

---

## Safety & Guardrails

### What SocialMediaGenie Will NOT Do

1. **Generate Misinformation or False Claims**
   - Will not create posts with unverified statistics or misleading claims
   - Requests must include sources for claims (e.g., "According to UN Fashion Report...")
   - Limitation: Verify all stats before posting—SocialMediaGenie cites sources but doesn't fact-check in real-time

2. **Create Engagement Manipulation Content**
   - Will not generate "like-bait" or misleading CTAs ("Tag someone who...")
   - Will not create artificial controversy or inflammatory posts designed to manipulate
   - Limitation: Ethical engagement strategies only

3. **Impersonate or Misrepresent Brands**
   - Will not generate content pretending to be another brand or person
   - Will not create deepfake video scripts or deceptive visual descriptions
   - Limitation: All content must be authentic to your brand

4. **Violate Platform Terms of Service**
   - Will not generate spam, bot-like content, or mass-follow tactics
   - Will not create posts designed to evade platform algorithms artificially
   - Limitation: Content follows Instagram, TikTok, LinkedIn, Twitter native guidelines

5. **Generate Illegal or Harmful Content**
   - Will not create posts promoting illegal activities, hate speech, or discrimination
   - Will not generate content that harasses, bullies, or defames individuals
   - Limitation: Content must comply with local laws and platform policies

6. **Bypass Copyright or Intellectual Property**
   - Will not generate content using copyrighted material without permission
   - Will not suggest using others' content without attribution
   - Limitation: Always credit sources, music, and inspiration

### Best Practices for Responsible Use

- **Review before posting:** Always review generated content for accuracy and brand fit
- **Disclose AI usage:** Consider transparency about AI-assisted content (growing audience expectation)
- **Monitor comments:** Engage authentically with comments—don't use bots for replies
- **Fact-check statistics:** Verify all claims, especially for healthcare, finance