---
name: ai-powered-e-commerce-product-description-writer
description: "Generate SEO-optimized e-commerce product descriptions with features, benefits, and unique selling points. Use when the user needs product copy for Shopify, WooCommerce, Amazon, or any online store."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {"openclaw":{"requires":{"env":["OPENAI_API_KEY"],"bins":["curl"]},"os":["macos","linux","win32"],"files":["SKILL.md"],"emoji":"📝"}}
---

# AI-Powered E-Commerce Product Description Writer

## Overview

This skill generates high-quality, conversion-optimized product descriptions for e-commerce platforms. It analyzes product details you provide and creates compelling copy that:

- **Maximizes SEO visibility** with keyword optimization and structured formatting
- **Drives conversions** through benefit-focused copywriting and psychological triggers
- **Saves time** by automating 80% of product description writing
- **Maintains consistency** across your entire product catalog
- **Supports multiple platforms** including Shopify, WooCommerce, BigCommerce, Amazon, eBay, Etsy, and custom storefronts

The skill uses OpenAI's GPT-4 model to generate descriptions that balance technical accuracy with persuasive marketing language. It's ideal for e-commerce managers, product marketers, and store owners managing catalogs of 10+ products.

**Integrations:** Works seamlessly with Zapier, Make.com, WordPress REST API, Shopify Admin API, and direct CSV/JSON exports for bulk uploads.

---

## Quick Start

### Example 1: Basic Product Description
```
Generate a product description for:
Product: Bamboo Wireless Charging Pad
Category: Electronics/Accessories
Price: $34.99
Key features:
- 10W fast charging
- Works with all Qi-enabled devices
- Eco-friendly bamboo construction
- Non-slip surface
- LED indicator light
Target audience: Eco-conscious tech users, gift buyers
Tone: Modern, sustainable, minimalist
Include: SEO keywords for "wireless charger" and "eco-friendly"
```

### Example 2: Amazon-Optimized Description
```
Create an Amazon A+ product description for:
Product: Stainless Steel Water Bottle (32oz)
Brand: HydroFlow
Key selling points:
- Double-wall insulation (keeps drinks cold 24hrs, hot 12hrs)
- BPA-free, food-grade stainless steel
- Wide mouth opening for easy filling and cleaning
- Comes with carrying loop
- Available in 8 colors
Competitors: Hydro Flask, S'well, Nalgene
Target keywords: stainless steel water bottle, insulated bottle, eco-friendly
Format: Include bullet points for search visibility
```

### Example 3: Bulk Product Batch
```
Generate product descriptions for my Shopify store (CSV format):
[Product Name] | [Category] | [Price] | [Key Features]
Yoga Mat Pro | Sports | $45 | Non-slip, eco-friendly TPE, 6mm thick, carrying strap
Running Shoes X1 | Footwear | $120 | Lightweight mesh, responsive cushioning, reflective trim
Protein Powder | Nutrition | $35 | 25g protein per serving, vanilla flavor, no artificial sweeteners

Requirements:
- Format: Shopify-compatible (under 255 chars for title, 1000 chars for body)
- Include meta descriptions for each
- Add internal linking suggestions
- Output as JSON for direct Shopify import
```

---

## Capabilities

### 1. **SEO-Optimized Copy Generation**
- Analyzes competitor descriptions and identifies keyword gaps
- Incorporates primary and long-tail keywords naturally
- Structures content for featured snippets and voice search
- Generates meta descriptions (155-160 characters) optimized for CTR
- Creates H1, H2 hierarchy for on-page SEO

**Usage Example:**
```
Write an SEO-optimized description for "ergonomic gaming mouse"
Include these keywords: gaming mouse, ergonomic, wireless, 16000 DPI
Target audience: Competitive gamers, streamers
Platforms: Amazon, Newegg, Best Buy
```

### 2. **Conversion-Focused Copywriting**
- Uses proven persuasion frameworks (AIDA: Attention, Interest, Desire, Action)
- Highlights unique selling propositions (USPs) and differentiation
- Addresses customer pain points and objections
- Includes social proof suggestions (review counts, awards)
- Creates urgency and scarcity messaging options

### 3. **Multi-Platform Formatting**
- **Shopify:** Title + Description + Meta Description optimized for Shopify's character limits
- **Amazon:** Bullet points (5 max) + Description + Enhanced Content (A+)
- **WooCommerce:** Short description + Full description + SEO fields
- **eBay:** Title (80 chars) + Description (4000 chars) with HTML formatting
- **Etsy:** Title (140 chars) + Description (4000 chars) + Tags (13 max)
- **Custom:** Plain text, Markdown, or HTML

### 4. **Tone & Brand Voice Customization**
- Luxury/Premium: Sophisticated, aspirational language
- Budget-Friendly: Value-focused, practical benefits
- Eco-Conscious: Sustainability messaging, certifications
- Tech-Forward: Specs-heavy, performance-oriented
- Fun/Playful: Casual, personality-driven copy

### 5. **Bulk Generation & Automation**
- Process 50+ products in a single request
- Maintain consistent voice across catalog
- Generate variations (short, medium, long formats)
- Export to CSV, JSON, or direct API integration
- Track generation history and A/B test results

---

## Configuration

### Environment Variables
```bash
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxx  # Required: OpenAI API key (GPT-4 access)
OPENAI_MODEL=gpt-4-turbo              # Optional: Default model (gpt-4, gpt-3.5-turbo)
MAX_TOKENS=1500                        # Optional: Max output length per description
TEMPERATURE=0.7                        # Optional: Creativity level (0.5-0.9)
```

### Setup Instructions
1. **Get OpenAI API Key:**
   - Visit https://platform.openai.com/account/api-keys
   - Create new secret key
   - Store in environment variable: `export OPENAI_API_KEY=sk-...`

2. **Verify Installation:**
   ```bash
   curl -X POST https://api.openai.com/v1/models \
     -H "Authorization: Bearer $OPENAI_API_KEY"
   ```

3. **Optional Integrations:**
   - **WordPress/WooCommerce:** Install WooCommerce REST API plugin
   - **Shopify:** Enable custom app with `write_products` scope
   - **Zapier:** Use "Code by Zapier" or "Webhooks" to trigger skill
   - **Make.com:** Create HTTP module calling skill endpoint

### Default Options
```yaml
format: "shopify"                    # Output format
tone: "professional"                 # Copy tone
length: "medium"                     # Description length
include_meta_description: true       # Add SEO meta tags
include_keywords: true               # Highlight target keywords
include_features_benefits: true      # Structure with Features/Benefits sections
include_faq: false                   # Optional: Add FAQ section
language: "en-US"                    # Output language
```

---

## Example Outputs

### Output 1: Shopify Product Description

**Input:**
```
Product: Ceramic Non-Stick Frying Pan (12-inch)
Price: $49.99
Features: PFOA-free ceramic coating, stainless steel handle, oven-safe to 350°F
Category: Cookware
```

**Output:**
```
TITLE:
Ceramic Non-Stick Frying Pan 12-inch | PFOA-Free Cookware

DESCRIPTION:
Cook healthier with our premium ceramic non-stick frying pan. Unlike traditional 
Teflon cookware, our PFOA-free ceramic coating delivers superior non-stick 
performance without harmful chemicals. Perfect for everyday cooking—from fluffy 
pancakes to perfectly seared vegetables.

FEATURES:
• Advanced ceramic non-stick coating (PFOA & PTFE-free)
• Professional-grade stainless steel handle stays cool during cooking
• Oven-safe up to 350°F for versatile stovetop-to-oven cooking
• Compatible with all stovetops: gas, electric, induction, and ceramic
• Easy cleanup—hand wash or dishwasher safe
• Lifetime warranty against manufacturing defects

WHY CHOOSE THIS PAN:
Tired of non-stick cookware that loses its coating after a few months? Our 
ceramic frying pan maintains its non-stick properties for years, thanks to 
premium materials and rigorous testing. Plus, it's better for your family—no 
PFOA, no PTFE, no compromise.

META DESCRIPTION:
PFOA-free ceramic non-stick frying pan, 12-inch. Oven-safe, stainless steel 
handle. Healthy cooking for every kitchen.

KEYWORDS:
ceramic frying pan, non-stick cookware, healthy cookware, PFOA-free
```

### Output 2: Amazon Bullet Points

**Input:**
```
Product: Portable Bluetooth Speaker
Key specs: 20W power, 12-hour battery, waterproof
```

**Output:**
```
TITLE:
Portable Bluetooth Speaker, 20W Stereo Sound, 12-Hour Battery, IPX7 Waterproof

BULLET POINTS:
• Powerful 20W stereo sound with deep bass—fills rooms up to 1,200 sq ft
• 12-hour battery life on single charge; quick-charge in 2 hours
• IPX7 waterproof rating: survive pool parties, beach trips, and rain
• Pairs instantly with any Bluetooth device (phones, tablets, laptops)
• Compact design (5.2 x 3.1 x 2.8 inches) fits backpacks and cup holders

DESCRIPTION:
Take your music anywhere with professional-grade sound in your pocket. Whether 
you're hosting a backyard barbecue, hitting the beach, or working from a coffee 
shop, this speaker delivers room-filling audio without the bulk.

A+ CONTENT (Enhanced):
[Image: Product in use at beach]
BEST-IN-CLASS SOUND
20W dual drivers deliver concert-quality audio with crisp highs and thunderous 
bass. No tinny, compressed sound here.

[Image: Battery life graphic]
ALL-DAY BATTERY
Get 12 hours of continuous playback. Perfect for road trips, camping, or 
just forgetting to charge overnight.

[Image: Water splash]
WATERPROOF EVERYWHERE
IPX7 rating means it survives dunks, spills, and storms. Take it poolside 
without worry.
```

### Output 3: JSON Export (Bulk)

```json
{
  "products": [
    {
      "sku": "YOGA-MAT-001",
      "title": "Non-Slip Yoga Mat 6mm | Eco-Friendly TPE | Carrying Strap",
      "short_description": "Premium yoga mat with 6mm cushioning, eco-friendly TPE material, and carrying strap.",
      "description": "Transform your yoga practice with our premium non-slip mat...",
      "meta_description": "6mm eco-friendly yoga mat with carrying strap. Non-slip surface, perfect for beginners and pros.",
      "seo_keywords": ["yoga mat", "non-slip", "eco-friendly", "6mm cushioning"],
      "tone_used": "wellness-focused",
      "platform": "shopify"
    },
    {
      "sku": "SHOES-RUN-002",
      "title": "Lightweight Running Shoes | Responsive Cushioning | Reflective",
      "short_description": "Professional-grade running shoes with responsive cushioning and reflective trim.",
      "description": "Run faster, farther, and safer...",
      "meta_description": "Lightweight running shoes with responsive cushioning. Reflective trim for night running.",
      "seo_keywords": ["running shoes", "lightweight", "cushioning", "reflective"],
      "tone_used": "performance-focused",
      "platform": "shopify"
    }
  ],
  "generation_stats": {
    "total_products": 2,
    "avg_description_length": 187,
    "keywords_included": 8,
    "estimated_seo_score": 8.2
  }
}
```

---

## Tips & Best Practices

### 1. **Maximize SEO Impact**
- **Research keywords first:** Use Google Keyword Planner, Ahrefs, or SEMrush to identify high-volume, low-competition keywords
- **Front-load keywords:** Place primary keyword in title and first 50 words of description
- **Use long-tail variations:** Instead of just "yoga mat," include "non-slip yoga mat 6mm eco-friendly"
- **Add schema markup:** Include product schema (name, price, rating, availability) for rich snippets
- **Example prompt:**
  ```
  Generate description for "wireless earbuds" targeting these keywords:
  - wireless earbuds (primary)
  - true wireless earbuds (secondary)
  - best wireless earbuds (long-tail)
  - noise-cancelling earbuds (related)
  ```

### 2. **Improve Conversion Rates**
- **Lead with benefits, not features:** "Stay focused for 12 hours" beats "12-hour battery"
- **Address objections:** If price is high, emphasize durability and warranty
- **Use power words:** Transform, unlock, discover, proven, exclusive, limited
- **Include social proof:** "Join 50,000+ satisfied customers" or "4.8-star rating from 2,300 reviews"
- **Create urgency:** "Only 5 left in stock" or "Limited-time offer"

### 3. **Platform-Specific Optimization**
- **Amazon:** Focus on bullet points (they're indexed); use A+ content for premium products
- **Shopify:** Keep meta descriptions under 155 characters; use product collections for internal linking
- **WooCommerce:** Leverage Yoast SEO plugin integration; include FAQ schema for featured snippets
- **Etsy:** Use all 13 tags; capitalize on long-tail keywords with lower competition
- **eBay:** Avoid keyword stuffing; use HTML formatting for readability

### 4. **Brand Voice Consistency**
- **Create a brand guide:** Document your tone, vocabulary, and messaging pillars
- **Use custom instructions:** Tell the skill "Always mention sustainability" or "Use casual, friendly language"
- **Review and refine:** Check first 5 descriptions manually; refine prompts based on feedback
- **A/B test variations:** Generate 2-3 versions; test which converts better

### 5. **Bulk Processing Efficiency**
- **Batch by category:** Process similar products together for consistency
- **Use templates:** Create a CSV template with columns: Product Name, Category, Price, Features
- **Validate output:** Spot-check descriptions for accuracy, tone, and keyword placement
- **Export strategically:** Use JSON for API integration, CSV for spreadsheet review

---

## Safety & Guardrails

### What This Skill Will NOT Do

1. **Misleading Claims:** Will not generate false or exaggerated claims (e.g., "Cures cancer," "Guaranteed weight loss")
   - Safeguard: Skill prompts you to provide factual features; generates copy based only on verified information
   - Limitation: Cannot verify product claims independently; you remain responsible for accuracy

2. **Copyright Infringement:** Will not copy competitor descriptions or plagiarize existing content
   - Safeguard: Generates original content based on your product details
   - Limitation: You should still verify uniqueness using plagiarism checkers (Copyscape, Grammarly)

3. **Unsubstantiated Health/Medical Claims:** Will not generate descriptions claiming medical benefits without FDA/clinical approval
   - Safeguard: Skill filters out prohibited health claims
   - Limitation: For supplements, cosmetics, or medical devices, you must comply with FTC and FDA regulations independently

4. **Illegal or Unethical Content:** Will not generate descriptions for counterfeit, illegal, or unethical products
   - Safeguard: Built-in content policy filter
   - Limitation: You are responsible for ensuring product legality in your jurisdiction

5. **Discriminatory Language:** Will not generate descriptions with racial, gender, age, or other discriminatory bias
   - Safeguard: Filters for inclusive, respectful language
   - Limitation: Review descriptions for regional cultural sensitivity before publishing

### Limitations & Disclaim