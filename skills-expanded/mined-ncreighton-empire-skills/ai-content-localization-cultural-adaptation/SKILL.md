---
name: ai-content-localization-cultural-adaptation
description: "Adapt English content for global markets with cultural sensitivity, idiom detection, metric conversions, and regional SEO optimization. Use when the user needs international content strategy, market-specific messaging, or localization briefs for human editors."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {"openclaw":{"requires":{"env":["OPENAI_API_KEY","GOOGLE_TRANSLATE_API_KEY"],"bins":["curl","jq"]},"os":["macos","linux","win32"],"files":["SKILL.md"],"emoji":"🌍"}}
---

# AI Content Localization & Cultural Adaptation Specialist

## Overview

Transform English content into culturally resonant, market-specific messaging without losing your brand voice. This skill goes **far beyond translation**—it's a comprehensive localization strategy tool that identifies cultural landmines, suggests regional case studies, converts imperial to metric, and optimizes for local search behavior.

Perfect for marketing teams, SaaS companies, e-commerce platforms, and publishers targeting multiple international markets. Integrates seamlessly with **WordPress**, **Contentful**, **Slack**, **HubSpot**, and **Google Analytics** to streamline your global content operations.

**Why it matters:** 73% of consumers prefer content in their native language, but only 25% of websites are properly localized. This skill ensures your message lands—culturally, linguistically, and strategically.

---

## Quick Start

Try these prompts immediately to see the skill in action:

### Example 1: Blog Post Localization
```
Localize this blog post for Germany, France, and Japan:

"We're crushing our Q3 goals! Our American customers love how our SaaS 
platform helps them move the needle on productivity. Check out how Sarah 
from Texas increased her team's output by 40% in just 30 days. Our pricing 
starts at $99/month."

Markets: Germany, France, Japan
Content Type: Blog Post
Tone: Upbeat, startup culture
Output Format: Localization brief
```

### Example 2: Product Description for Multiple Regions
```
Adapt this product description for UK, Australia, and Singapore:

"Our revolutionary fitness tracker uses AI to help you smash your goals. 
It's the bomb—athletes swear by it. Measures calories in real-time. 
Compatible with iOS and Android. Ships free in the US."

Markets: UK, Australia, Singapore
Content Type: Product Description
Focus Areas: Terminology, cultural references, shipping/logistics
Output Format: Localization checklist with editor notes
```

### Example 3: Marketing Email Campaign
```
Localize this email campaign for Spain, Brazil, and Mexico:

Subject: "Don't Sleep on Our Black Friday Sale!"
Body: "Hey team! This Friday only, grab 50% off. Time to hustle. 
Our CEO started in his garage—now we're a $100M company. 
Join the grind. Limited to US customers."

Markets: Spain, Brazil, Mexico
Content Type: Email Campaign
Considerations: Cultural attitudes toward discounts, work culture references
Output Format: Market-specific subject lines + body variants
```

---

## Capabilities

### 1. **Cultural Sensitivity Scanning**
Identifies phrases, idioms, and references that may offend, confuse, or underperform in target markets.

- Detects idioms that don't translate ("piece of cake," "ballpark figure," "move the needle")
- Flags culturally sensitive topics (politics, religion, historical references)
- Identifies humor that relies on English-language wordplay
- Highlights gender/age assumptions in messaging
- Warns about color symbolism differences (white = purity in US, mourning in some Asian cultures)

**Example Output:**
```
⚠️  CULTURAL FLAG: "We're crushing our goals"
   Issue: Sports/competition metaphor may not resonate in cultures 
   favoring harmony and collaboration (Japan, Germany)
   Suggestion: "We're achieving our goals" or "We're on track"
   
⚠️  IDIOM ALERT: "Move the needle"
   Issue: American business jargon, unclear in translation
   Suggestion: "Make measurable progress" or "Drive results"
```

### 2. **Regional Case Study & Example Recommendations**
Suggests local case studies, customer names, and regional examples that resonate with target audiences.

- Identifies generic examples that should be localized
- Recommends region-specific success metrics (e.g., ROI vs. efficiency in manufacturing-heavy regions)
- Suggests local competitor references
- Flags opportunities for local customer testimonials
- Provides regional business context for B2B messaging

**Example Output:**
```
📍 LOCALIZATION OPPORTUNITY: Customer Example
   Current: "Sarah from Texas increased output by 40%"
   Recommendation for Germany: Reference a Munich-based manufacturing 
   company or use German-style efficiency metrics
   Recommendation for Japan: Feature a company known for kaizen/continuous 
   improvement philosophy
```

### 3. **Metric & Unit Conversion**
Automatically converts imperial to metric and regional variations.

- Temperature: Fahrenheit → Celsius (with context: "comfortable 72°F" → "pleasant 22°C")
- Distance: Miles → Kilometers
- Weight: Pounds → Kilograms
- Currency: USD → EUR, GBP, JPY, BRL, MXN (with current rates)
- Time zones: US-centric scheduling → regional times
- Speed: MPH → KPH

**Example Output:**
```
🔄 METRIC CONVERSIONS:
   Original: "Our server responds in 50ms, handles 10,000 requests/second"
   No changes needed (technical specs translate universally)
   
   Original: "Lose 20 pounds in 90 days"
   German: "Verlieren Sie 9 kg in 90 Tagen"
   Japanese: "90日間で9kg減量"
```

### 4. **Regional SEO & Search Behavior Optimization**
Adapts content for local search engines and keyword behavior.

- Google Trends analysis by region
- Local keyword variants (e.g., "mobile phone" vs. "cell phone" vs. "smartphone")
- Search intent differences by market
- Regional search engine preferences (Baidu for China, Yandex for Russia)
- Local long-tail keyword opportunities

**Example Output:**
```
🔍 SEO OPTIMIZATION:
   Market: Germany
   Original keyword: "cloud storage"
   German search variants: "Cloud-Speicher", "Cloudspeicher", "Online-Speicher"
   Monthly searches: 2,400 (Cloud-Speicher) vs 1,100 (Cloudspeicher)
   Recommendation: Use "Cloud-Speicher" as primary, mention alternatives
   
   Market: Brazil
   Original keyword: "project management software"
   Portuguese variants: "software de gestão de projetos", "ferramenta de 
   gerenciamento de projetos"
   Note: Brazilians favor "ferramenta" (tool) over "software" in searches
```

### 5. **Localization Brief Generation**
Produces a comprehensive handoff document for human editors and translators.

- Priority flags (must-fix vs. nice-to-have)
- Word count and complexity estimates
- Glossary of brand-specific terms
- Tone and voice guidelines per market
- Visual asset recommendations (e.g., "Replace stock photo of Western office with diverse team")
- Timeline and resource estimates

---

## Configuration

### Environment Variables
```bash
# Required
export OPENAI_API_KEY="sk-..."                    # GPT-4 for analysis
export GOOGLE_TRANSLATE_API_KEY="AIzaSy..."       # Fallback translation
export GOOGLE_TRENDS_API_KEY="[optional]"         # SEO optimization

# Optional
export SLACK_WEBHOOK_URL="https://hooks.slack..." # Send briefs to Slack
export WORDPRESS_API_URL="https://yoursite.com"   # Direct WordPress sync
export HUBSPOT_API_KEY="[optional]"               # HubSpot integration
```

### Setup Instructions

1. **Obtain API Keys**
   - OpenAI: https://platform.openai.com/api-keys
   - Google Translate: https://cloud.google.com/translate/docs
   - Google Trends: https://trends.google.com/trends/api/explore

2. **Install Dependencies**
   ```bash
   npm install openai @google-cloud/translate
   pip install google-trends-api
   ```

3. **Configure Target Markets**
   Create a `localization-config.json`:
   ```json
   {
     "markets": [
       {
         "code": "de",
         "name": "Germany",
         "language": "de-DE",
         "timezone": "Europe/Berlin",
         "currency": "EUR",
         "searchEngine": "google",
         "culturalContext": "formal, privacy-conscious, efficiency-focused"
       },
       {
         "code": "jp",
         "name": "Japan",
         "language": "ja-JP",
         "timezone": "Asia/Tokyo",
         "currency": "JPY",
         "searchEngine": "google",
         "culturalContext": "harmony-focused, group-oriented, quality-driven"
       }
     ]
   }
   ```

4. **Set Skill Parameters**
   - `tone`: "formal", "casual", "professional", "friendly"
   - `contentType`: "blog", "product-description", "email", "landing-page", "ad-copy"
   - `priority`: "speed" (fast turnaround) vs "depth" (comprehensive analysis)

---

## Example Outputs

### Sample Localization Brief (Germany)

```
╔════════════════════════════════════════════════════════════════╗
║     LOCALIZATION BRIEF: Blog Post → German Market             ║
║     Status: Ready for Editor Review                            ║
╚════════════════════════════════════════════════════════════════╝

📋 DOCUMENT SUMMARY
   Original: 1,200 words | Est. German: 1,450 words (+21% expansion)
   Complexity: Medium | Estimated translation time: 4 hours
   Tone: Professional with startup energy (maintain throughout)

🚨 CRITICAL ISSUES (Must Fix)
   [1] "Crushing our goals" → Reframe as "Achieving ambitious targets"
       Reason: German business culture favors measured language
   
   [2] "The bomb" (slang) → Remove or replace with "exceptional"
       Reason: Idiom doesn't translate; confusing in German
   
   [3] Customer example "Sarah from Texas" → Recommend German case study
       Reason: Readers connect better with local success stories
       Suggestion: Feature a Munich-based B2B SaaS company

⚠️  MEDIUM PRIORITY ISSUES (Should Fix)
   [4] "Move the needle" → "Drive measurable results"
   [5] "Hustle" culture reference → Emphasize "efficiency" instead
   [6] "$99/month" → "€89/Monat" (with note: pricing may need adjustment)

💡 OPTIMIZATION OPPORTUNITIES
   • Add mention of GDPR compliance (critical trust factor in Germany)
   • Reference German efficiency standards (DIN, ISO certifications)
   • Include case study of German manufacturing company
   • Highlight data security (major concern in Germany)

🔍 SEO RECOMMENDATIONS
   Primary keyword: "SaaS-Produktivitätslösung" (1,200 monthly searches)
   Secondary: "Produktivitätssoftware" (890 searches)
   Long-tail: "KMU Produktivitäts-Tool" (340 searches, high intent)
   Recommendation: Lead with primary, naturally incorporate secondary

📊 METRICS TO ADAPT
   • "40% increase" → OK (universal metric)
   • "30 days" → OK (universal)
   • Time zone references → Specify "CET" if scheduling mentioned

🎨 VISUAL ASSET NOTES
   • Stock photo: Replace American office with German/European team
   • Color scheme: Keep professional; avoid overly bright/casual
   • Charts: Adapt to metric system if showing data

📝 GLOSSARY (Brand Terms)
   SaaS → SaaS (no translation needed, widely understood)
   Output → Leistung or Produktivität (context-dependent)
   Dashboard → Dashboard (widely used in German tech)

👥 TONE GUIDE FOR GERMAN MARKET
   DO: Use formal "Sie" in customer testimonials
   DO: Emphasize ROI and measurable outcomes
   DON'T: Use excessive exclamation points (seen as unprofessional)
   DON'T: Make promises without data backing

⏱️  TIMELINE ESTIMATE
   Translation: 4 hours | Review: 2 hours | Optimization: 1 hour
   Total: ~7 hours for 1 editor

✅ NEXT STEPS
   1. Translator creates German version using this brief
   2. Editor reviews against cultural flags
   3. QA checks SEO keywords and metrics
   4. Publish to WordPress with de-DE locale
```

### Sample Localization Brief (Japan)

```
╔════════════════════════════════════════════════════════════════╗
║     LOCALIZATION BRIEF: Blog Post → Japanese Market           ║
║     Status: Ready for Editor Review                            ║
╚════════════════════════════════════════════════════════════════╝

🚨 CRITICAL ISSUES (Must Fix)
   [1] "Crushing our goals" → "目標を達成しています" (achieving goals)
       Reason: Japanese culture values harmony; aggressive language 
       may come across as arrogant
   
   [2] "The bomb" → Remove entirely
       Reason: No equivalent in Japanese; confusing
   
   [3] "Sarah from Texas" → Feature Japanese company or Asian case study
       Reason: Japanese readers strongly prefer local examples
       Suggestion: Tokyo-based fintech or Osaka manufacturing company
   
   [4] CEO garage origin story → Adapt for Japanese context
       Reason: Japanese business culture values stability and established 
       processes; startup scrappiness is less valued
       Suggestion: Emphasize "continuous improvement" (kaizen) philosophy

⚠️  MEDIUM PRIORITY ISSUES
   [5] "Move the needle" → "成果を上げる" (deliver results)
   [6] "Hustle" → "効率的に働く" (work efficiently)
   [7] Individualistic language → Emphasize team and collaboration

💡 OPTIMIZATION OPPORTUNITIES
   • Highlight quality and reliability (major trust factors)
   • Mention compliance with Japanese data protection laws
   • Add customer testimonial from Japanese company (if available)
   • Emphasize long-term partnership approach, not quick wins

🔍 SEO RECOMMENDATIONS
   Primary keyword: "SaaS生産性ツール" (850 monthly searches)
   Secondary: "クラウド生産性ソフト" (620 searches)
   Long-tail: "中小企業向けSaaS" (340 searches, high intent)
   Note: Japanese users prefer specific, long-tail keywords

📊 METRICS TO ADAPT
   • "40% increase" → "40%向上" (OK, but add context about timeframe)
   • "30 days" → "30日間で" (OK)
   • Specify "日本時間" (Japan Standard Time) if scheduling mentioned

🎨 VISUAL ASSET NOTES
   • Replace Western imagery with Japanese/Asian team
   • Ensure diversity and inclusion (important in modern Japan)
   • Use professional, high-quality photos (not casual startup vibes)
   • Avoid stereotypical imagery

👥 TONE GUIDE FOR JAPANESE MARKET
   DO: Use polite, formal tone (敬語)
   DO: Emphasize quality, reliability, and long-term value
   DO: Include social proof and customer testimonials
   DON'T: Use casual or aggressive language
   DON'T: Make unsupported claims
   DON'T: Emphasize rapid growth at expense of stability

⏱️  TIMELINE ESTIMATE
   Translation: 5 hours (Japanese is complex) | Review: 2.5 hours
   Cultural adaptation: 1.5 hours | Total: ~9 hours

✅ NEXT STEPS
   1. Native Japanese speaker (not just translator) handles adaptation
   2. Cultural consultant reviews tone and framing
   3. QA checks SEO and metrics
   4. Publish with ja-JP locale
```

---

## Tips & Best Practices

### 1. **Start with High-Value Markets First**
Don't try to localize for 20 countries at once. Prioritize by:
- Revenue potential
- Current audience size
- Competitive landscape
- Cultural distance from English-speaking markets

*Example:* If you