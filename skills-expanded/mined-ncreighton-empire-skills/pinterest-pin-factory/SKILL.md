---
name: pinterest-pin-factory
description: "Generate SEO-optimized Pinterest pins from articles with descriptions, images, and scheduling. Use when the user needs social automation, content repurposing, or bulk pin creation for traffic growth."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["PINTEREST_ACCESS_TOKEN", "OPENAI_API_KEY", "UNSPLASH_API_KEY"],
        "bins": []
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"],
      "emoji": "📌"
    }
  }
---

# Pinterest Pin Factory

## Overview

Pinterest Pin Factory automates the creation of SEO-optimized Pinterest pins directly from your blog articles, web content, or product descriptions. This skill eliminates manual pin design and copywriting by generating multiple pin variations, descriptions, hashtags, and scheduling recommendations—all tailored for maximum Pinterest engagement and traffic.

**Why It Matters:**
- Pinterest drives 33% of social referral traffic to content sites
- Users spend 3x longer on Pinterest than other social platforms
- Bulk pin creation typically requires $500–$2,000/month in design tools or freelancers
- This skill automates the entire workflow in seconds

**Integrations & Compatibility:**
- **WordPress**: Extract article content via REST API
- **Medium, Substack, Dev.to**: Parse RSS feeds for content
- **Slack**: Receive pin notifications and approval workflows
- **Google Sheets**: Bulk import URLs, export pin data
- **Zapier/Make**: Connect to 5,000+ apps for automated workflows
- **Pinterest Business API**: Direct pin scheduling (with authentication)
- **Unsplash/Pexels**: Automatic image selection or custom image uploads

---

## Quick Start

Try these example prompts immediately:

### Example 1: Generate Pins from a Blog Article
```
Generate 5 Pinterest pins from this article:
Title: "10 Proven Strategies for Remote Team Productivity"
URL: https://example.com/remote-productivity
Category: Business/Productivity
Target Audience: Remote managers and entrepreneurs

I want:
- 5 pin variations with different hooks
- SEO-optimized descriptions (150 chars max)
- Relevant hashtags (10-15 per pin)
- Scheduling recommendations (best posting times)
- Image style suggestions (minimal, infographic, quote-overlay, etc.)
```

### Example 2: Bulk Pin Creation from RSS Feed
```
Create Pinterest pins from my latest 10 blog posts.
RSS Feed: https://myblog.com/feed.xml
Blog Niche: Sustainable Living
Brand Colors: #2D5016, #F4E4C1
Pin Dimensions: 1000x1500px (vertical)

For each article:
1. Extract title and first 200 words
2. Generate 3 pin variations (educational, inspirational, how-to)
3. Write descriptions with internal link CTAs
4. Suggest optimal posting schedule (Monday-Friday, 9am-3pm EST)
5. Format as CSV for bulk upload to Pinterest
```

### Example 3: Product-to-Pin Conversion
```
Convert my Shopify product into Pinterest pins:
Product: "Organic Bamboo Toothbrush Set"
Price: $24.99
Description: Eco-friendly, biodegradable, comes in 5 colors
Target Keywords: sustainable toothbrush, eco-friendly oral care, zero-waste bathroom

Generate:
- 4 pin designs (lifestyle, product-focused, benefit-driven, social proof)
- Rich pin descriptions with affiliate link
- Trending hashtags for eco-conscious audience
- A/B testing recommendations (text overlay vs. minimal design)
```

---

## Capabilities

### 1. **Intelligent Content Extraction**
- Parse article URLs, RSS feeds, or raw text
- Extract headlines, body copy, key insights, and metadata
- Identify primary topic and secondary themes for better targeting
- Support for 50+ content platforms (WordPress, Medium, Substack, Wix, etc.)

### 2. **Multi-Variation Pin Generation**
- Create 3–10 pin variations per article automatically
- Different hooks: educational, inspirational, how-to, listicle, social proof, trending format
- Customize tone (professional, casual, playful, urgent)
- A/B testing recommendations for optimal performance

### 3. **SEO-Optimized Descriptions**
- Generate 150-character descriptions with primary keywords
- Include CTAs: "Learn more," "Shop now," "Read full post"
- Pinterest algorithm optimization: keyword placement, readability, engagement triggers
- Multi-language support (English, Spanish, French, German, Portuguese)

### 4. **Hashtag & Keyword Strategy**
- 10–15 relevant hashtags per pin based on niche and trending topics
- Mix of high-volume (#productivity) and long-tail (#remote-team-management) tags
- Avoid hashtag saturation (< 5M posts per hashtag)
- Seasonal and trending keyword suggestions

### 5. **Image Recommendations**
- Suggest 5 design styles: minimal, infographic, quote-overlay, lifestyle, carousel
- Integration with Unsplash/Pexels for free image sourcing
- Custom image upload support (JPG, PNG, WebP)
- Image optimization: compression, dimensions (1000x1500px standard)
- Color palette analysis matching brand guidelines

### 6. **Scheduling Intelligence**
- Optimal posting times based on audience timezone and niche
- Bulk scheduling recommendations (Monday–Friday, 9am–3pm typically best)
- Frequency suggestions (3–5 pins/day per board for growth)
- Seasonal posting calendar (holiday, seasonal content)

### 7. **Bulk Operations**
- Process 50–500 URLs in a single request
- CSV/JSON export for Pinterest bulk upload tool
- Batch scheduling across multiple boards
- Progress tracking and error reporting

---

## Configuration

### Environment Variables (Required)

```bash
# Pinterest Business API
export PINTEREST_ACCESS_TOKEN="your_pinterest_token_here"
export PINTEREST_BUSINESS_ACCOUNT_ID="your_account_id"

# AI & Content Generation
export OPENAI_API_KEY="sk-your-key-here"
export OPENAI_MODEL="gpt-4-turbo"  # or gpt-3.5-turbo for cost savings

# Image Sourcing
export UNSPLASH_API_KEY="your_unsplash_key"
export PEXELS_API_KEY="your_pexels_key"  # Optional fallback

# Optional: WordPress Integration
export WORDPRESS_API_KEY="your_wp_key"
export WORDPRESS_SITE_URL="https://yourblog.com"

# Optional: Slack Notifications
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
```

### Configuration Options

```yaml
pin_generation:
  variations_per_article: 5           # 1-10 pins per article
  description_length: 150             # characters (max 500 for Pinterest)
  hashtag_count: 12                   # per pin (recommended: 10-15)
  include_emoji: true                 # emoji in descriptions
  tone: "professional"                # professional, casual, playful, urgent
  
image_settings:
  preferred_source: "unsplash"        # unsplash, pexels, custom_upload
  dimensions: "1000x1500"             # Pinterest vertical standard
  include_text_overlay: true
  brand_colors: ["#2D5016", "#F4E4C1"]
  
scheduling:
  auto_schedule: false                # requires Pinterest API
  optimal_times: true                 # analyze best posting times
  timezone: "EST"                     # your timezone
  frequency: 3                        # pins per day per board
  
seo:
  include_keywords: true
  keyword_density: 2-3                # percentage
  include_internal_links: true
  rich_pin_format: "article"          # article, product, recipe, etc.
  
export_format: "csv"                  # csv, json, pinterest_bulk
```

---

## Example Outputs

### Output 1: Single Pin Generation (JSON)

```json
{
  "pin_id": "pinterest-pin-001",
  "article_title": "10 Proven Strategies for Remote Team Productivity",
  "variations": [
    {
      "variation_number": 1,
      "hook": "educational",
      "pin_description": "Boost remote team productivity with these 10 science-backed strategies. From async communication to focus time blocks—proven methods for distributed teams. Read the full guide →",
      "hashtags": "#RemoteWork #ProductivityTips #TeamManagement #AsyncWork #LeadershipTips #DistributedTeams #WorkFromHome #Productivity #Management #BusinessGrowth",
      "design_style": "infographic",
      "image_suggestions": [
        "Dashboard/metrics visual",
        "Team collaboration graphic",
        "Time management chart"
      ],
      "cta": "Read full post",
      "internal_link": "https://example.com/remote-productivity"
    },
    {
      "variation_number": 2,
      "hook": "inspirational",
      "pin_description": "Remote teams don't have to be disconnected teams. Discover the culture-building strategies that turned scattered groups into high-performing units.",
      "hashtags": "#RemoteTeam #TeamCulture #LeadershipDevelopment #CompanyGrowth #DistributedWorkforce #EmployeeEngagement #WorkplaceWellness #ProductivityHacks #RemoteLeadership",
      "design_style": "quote-overlay",
      "image_suggestions": [
        "Team video call screenshot",
        "Celebration/success moment",
        "Diverse team collaboration"
      ],
      "cta": "Learn more",
      "internal_link": "https://example.com/remote-productivity"
    }
  ],
  "scheduling_recommendations": {
    "best_days": ["Tuesday", "Wednesday", "Thursday"],
    "best_times": ["9:00 AM", "2:00 PM"],
    "timezone": "EST",
    "frequency": "2-3 pins per day",
    "board_recommendations": [
      "Business Tips",
      "Leadership",
      "Remote Work"
    ]
  },
  "seo_analysis": {
    "primary_keywords": ["remote work", "team productivity", "remote management"],
    "keyword_density": "2.1%",
    "readability_score": 8.5,
    "engagement_triggers": 4,
    "estimated_reach": "15,000-25,000 impressions"
  }
}
```

### Output 2: Bulk CSV Export

```csv
Pin_Title,Description,Hashtags,Design_Style,Image_Source,CTA,Internal_Link,Optimal_Day,Optimal_Time,Board
"Remote Productivity Tips","Boost remote team productivity with 10 science-backed strategies. Read the full guide →","#RemoteWork #ProductivityTips #TeamManagement #AsyncWork #LeadershipTips #DistributedTeams #WorkFromHome #Productivity #Management #BusinessGrowth","infographic","unsplash:team-meeting","Read full post","https://example.com/remote-productivity","Tuesday","9:00 AM","Business Tips"
"Remote Team Culture","Build disconnect-proof remote teams with proven culture strategies. Learn more →","#RemoteTeam #TeamCulture #LeadershipDevelopment #CompanyGrowth #DistributedWorkforce #EmployeeEngagement #WorkplaceWellness #ProductivityHacks #RemoteLeadership","quote-overlay","unsplash:team-collaboration","Learn more","https://example.com/remote-productivity","Wednesday","2:00 PM","Leadership"
```

### Output 3: Slack Notification

```
📌 Pinterest Pin Factory - Batch Complete

✅ Generated 15 pins from 3 articles
📊 Estimated reach: 45,000-75,000 impressions
⏱️ Processing time: 2 min 34 sec

📁 Exports ready:
  • CSV for bulk upload: pinterest_pins_batch_001.csv
  • JSON data: pinterest_pins_batch_001.json
  • Board assignments: 5 boards

🎯 Next steps:
  1. Review descriptions in CSV
  2. Upload to Pinterest Business Account
  3. Schedule posts for Tuesday-Thursday, 9am-3pm
  4. Monitor performance in 7 days

👉 [View Full Report] [Download CSV] [Schedule Now]
```

---

## Tips & Best Practices

### 1. **Maximize Engagement**
- Create 5–10 variations per article (test different hooks and designs)
- Use power words: "Proven," "Science-backed," "Complete Guide," "Never," "Always"
- Include numbers in descriptions (10 strategies, 5 steps, 3 minutes)
- A/B test text overlay vs. minimal design (minimal typically wins for traffic)

### 2. **Optimize for Pinterest Algorithm**
- Post consistently (3–5 pins/day per board) to build momentum
- Use 10–15 relevant hashtags (avoid hashtag saturation)
- Include internal links in descriptions to drive traffic
- Rich pins (article, product) get 40% more engagement than standard pins
- Keyword placement: primary keyword in first 50 characters of description

### 3. **Niche-Specific Strategies**
- **B2B/Business**: Focus on "how-to," listicles, data-driven insights
- **E-commerce**: Product pins + lifestyle imagery, include pricing, urgency CTAs
- **Lifestyle/Wellness**: Inspirational hooks, before/after, transformations
- **DIY/Crafts**: Step-by-step infographics, materials lists, difficulty ratings

### 4. **Image Best Practices**
- Vertical pins (1000x1500px) get 35% more clicks than horizontal
- Text-heavy pins outperform minimalist designs for B2B
- Brand colors should appear in 30% of pins (consistency = recognition)
- Faces/people increase engagement by 25% (use diverse representations)
- High contrast text overlays (dark text on light background, vice versa)

### 5. **Board Organization**
- Create 5–10 boards organized by topic/audience segment
- Pin 30% original content, 70% curated/repurposed content
- Use descriptive board names with keywords (e.g., "Remote Work Strategies" not "Work Tips")
- Add board descriptions with keywords for discoverability

### 6. **Seasonal & Trending Content**
- Schedule holiday-related pins 3–4 weeks in advance
- Monitor Pinterest Trends tool for rising keywords in your niche
- Create evergreen content (productivity, learning, wellness) alongside timely pins
- Capitalize on back-to-school, New Year, Q1/Q3 planning seasons

### 7. **Drive Measurable Results**
- Use UTM parameters in links: `?utm_source=pinterest&utm_medium=pin&utm_campaign=remote-work`
- Set up Pinterest conversion tracking (pixel) on your website
- Monitor top-performing pins (saves, clicks, outbound clicks)
- Analyze monthly: What topics, designs, and posting times drive traffic?

---

## Safety & Guardrails

### What This Skill WILL NOT Do

❌ **Copyright Violations**: This skill will not generate pins that use copyrighted images without attribution or license. Always provide original images or properly licensed assets.

❌ **Misleading Content**: Will not create sensationalized descriptions, false claims, or "clickbait" that misrepresents article content. Generated descriptions must accurately reflect the linked content.

❌ **Spam or Manipulation**: Will not help with pin stuffing, hashtag manipulation, or artificial engagement tactics. Bulk operations must comply with Pinterest Terms of Service.

❌ **Unauthorized Scheduling**: Will not schedule pins to accounts without explicit API authentication. Requires valid `PINTEREST_ACCESS_TOKEN` with proper permissions.

❌ **Sensitive Content**: Will not generate pins for adult, violent, hateful, or discriminatory content. Respects Pinterest Community Guidelines.

### Boundaries & Limitations

⚠️ **Rate Limits**: OpenAI API calls limited by your subscription tier (typically 3,500 requests/minute for GPT-4). Bulk operations may require staggered processing.

⚠️ **Image Attribution**: Unsplash/Pexels images are free to use but require attribution per license. Custom images must be your own or properly licensed.

⚠️ **Pinterest API**: Rich pin scheduling requires Pinterest Business Account with API access. Not all features available on free/personal accounts.

⚠️ **Content Quality**: AI-generated descriptions are starting points—always review for