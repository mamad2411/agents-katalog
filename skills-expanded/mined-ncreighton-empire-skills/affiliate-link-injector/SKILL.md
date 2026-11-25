---
name: affiliate-link-injector
description: "Scan content for product mentions and auto-insert compliant affiliate links with FTC disclosures. Use when the user needs to monetize blog posts, reviews, or guides while maintaining legal compliance."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {"openclaw":{"requires":{"env":["AFFILIATE_API_KEY","AMAZON_ASSOCIATES_ID","FTC_DISCLOSURE_TEXT"],"bins":["curl","jq"]},"os":["macos","linux","win32"],"files":["SKILL.md"],"emoji":"🔗"}}
---

## Overview

The **Affiliate Link Injector** automates the process of identifying product mentions in your content and inserting properly formatted affiliate links while maintaining FTC compliance. This skill scans text for product references, matches them against your affiliate networks (Amazon Associates, ShareASale, Awin, CJ Affiliate, etc.), and injects tracked links with legally required disclosures.

### Why This Matters

- **Revenue Acceleration**: Convert existing content into income streams without rewriting
- **FTC Compliance**: Automatically adds required disclosures to protect your brand and avoid legal penalties
- **Time Savings**: Process 50+ pages of content in minutes instead of hours of manual link insertion
- **Consistency**: Ensures uniform disclosure formatting and link structure across all content
- **Network Integration**: Works with WordPress, Medium, Ghost, Substack, and custom platforms

### Primary Use Cases

1. **Blog Monetization**: Inject affiliate links into product reviews, roundups, and how-to guides
2. **Content Repurposing**: Convert old non-monetized posts into affiliate-linked versions
3. **Bulk Processing**: Process entire content libraries (100+ articles) systematically
4. **Multi-Network Management**: Handle links across Amazon, ShareASale, Awin, and other networks simultaneously

---

## Quick Start

### Example 1: Scan Blog Post and Generate Affiliate Links

```
Scan this blog post for product mentions and inject Amazon affiliate links with FTC disclosure:

"The best productivity laptops for remote workers in 2024. The MacBook Pro 16-inch remains 
the gold standard with its M3 Max chip and exceptional display. For Windows users, the Dell 
XPS 15 offers similar performance at a lower price point. Budget-conscious creators should 
consider the Lenovo ThinkPad X1 Carbon, which delivers reliable performance for under $1000."

Use my Amazon Associates ID: 12345-6789 and add a disclosure at the top of the content.
```

### Example 2: Process Product Review with Multiple Networks

```
Convert this product review to include affiliate links from both Amazon and ShareASale:

"I've tested the Dyson V15 Detect vacuum for 3 months. It's the most powerful cordless 
vacuum on the market, with a laser that reveals hidden dust. The Shark Navigator is a 
solid budget alternative at half the price. For pet owners, the Bissell Pet Hair Eraser 
is specifically engineered for animal fur."

Add FTC disclosure and return JSON with all affiliate links, networks, and commission rates.
```

### Example 3: Bulk Content Library Processing

```
Process my entire blog content library (50 articles) and inject affiliate links for:
- Amazon Associates (ID: my-id-123)
- ShareASale (merchant IDs: 45678, 45679)
- Awin (account: 9876543)

Return a CSV report with: article_title, product_mentioned, affiliate_link, network, 
estimated_commission_percentage. Add FTC disclosure to each article automatically.
```

---

## Capabilities

### 1. Product Mention Detection
- **NLP-powered scanning**: Identifies product names, brands, and model numbers in natural language
- **Context awareness**: Distinguishes between mentioned products and casual brand references
- **Synonym matching**: Recognizes alternative product names ("MacBook" = "Apple MacBook Pro")
- **Model number parsing**: Extracts specific product versions and SKUs

### 2. Affiliate Link Generation
- **Multi-network support**: Amazon Associates, ShareASale, Awin, CJ Affiliate, Impact, Rakuten
- **Smart routing**: Automatically routes products to the network offering highest commission
- **UTM parameter injection**: Adds custom tracking parameters for analytics
- **Short URL generation**: Creates clean, trackable links using bit.ly or custom domains
- **Batch API calls**: Processes 100+ products simultaneously with rate limiting

### 3. FTC Compliance Automation
- **Disclosure templates**: Pre-written, legally reviewed disclosure language
- **Placement optimization**: Positions disclosures prominently (top of content, before links)
- **Multiple formats**: Supports text, HTML, Markdown, and rich text formats
- **Regulatory updates**: Stays current with FTC Endorsement Guides (updated quarterly)
- **Multi-language support**: Generates compliant disclosures in 12+ languages

### 4. Content Integration
- **WordPress integration**: Direct post/page editing via REST API
- **Markdown processing**: Preserves formatting while injecting links
- **HTML handling**: Cleans and validates HTML output
- **JSON output**: Returns structured data for custom integrations
- **CSV export**: Bulk reporting for content audits

### 5. Analytics & Reporting
- **Link performance tracking**: Monitor clicks, conversions, and earnings per link
- **Content ROI calculation**: Estimates revenue potential by article
- **Network comparison**: Shows which networks perform best for your audience
- **Compliance audit log**: Records all disclosures added for legal protection

---

## Configuration

### Required Environment Variables

```bash
# Your unique API key from the Affiliate Link Injector service
export AFFILIATE_API_KEY="sk_live_abc123xyz789"

# Amazon Associates ID (format: name-20)
export AMAZON_ASSOCIATES_ID="mysite-20"

# Your FTC disclosure text (customize per brand)
export FTC_DISCLOSURE_TEXT="This page contains affiliate links. I earn a commission if you make a purchase at no additional cost to you."

# Optional: API keys for additional networks
export SHARESALE_API_KEY="your_sharesale_key"
export AWIN_API_KEY="your_awin_key"
export CJ_AFFILIATE_KEY="your_cj_key"
```

### Setup Instructions

1. **Obtain API credentials**:
   - Sign up at [affiliate-link-injector.io](https://affiliate-link-injector.io)
   - Generate API key in dashboard → Settings → API Keys
   - Copy your Amazon Associates ID from [amazon.com/associates](https://amazon.com/associates)

2. **Configure environment variables**:
   ```bash
   # Add to your .env file or shell profile
   source ~/.affiliate-config
   ```

3. **Authenticate with affiliate networks**:
   - Connect Amazon Associates account (OAuth)
   - Add ShareASale merchant IDs
   - Link Awin account credentials
   - Configure CJ Affiliate commission rates

4. **Test the connection**:
   ```
   Test the skill with a simple 2-sentence product mention to verify all API connections are working.
   ```

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `disclosure_position` | string | "top" | Where to place FTC disclosure: "top", "inline", "footer" |
| `link_format` | string | "markdown" | Output format: "markdown", "html", "plain_text" |
| `auto_shorten_urls` | boolean | true | Create short links for tracking |
| `min_commission_rate` | number | 0.5 | Minimum commission % to include link |
| `exclude_brands` | array | [] | Brand names to skip (e.g., competitors) |
| `preferred_networks` | array | ["amazon"] | Priority order for network selection |

---

## Example Outputs

### Input Content
```
"The best portable coffee makers for travel. The Aeropress Go is lightweight and 
makes excellent espresso. For simplicity, the Melitta Pour Over is hard to beat. 
The Nespresso Vertuo Plus offers convenience if you want automatic brewing."
```

### Output (Markdown)
```markdown
**Disclosure**: This page contains affiliate links. I earn a commission 
if you make a purchase at no additional cost to you.

The best portable coffee makers for travel. The [Aeropress Go](https://amazon.com/dp/B07GYWVYBX?tag=mysite-20) 
is lightweight and makes excellent espresso. For simplicity, the [Melitta Pour Over](https://amazon.com/dp/B00FCHBZEA?tag=mysite-20) 
is hard to beat. The [Nespresso Vertuo Plus](https://amazon.com/dp/B07GYWVYBX?tag=mysite-20) 
offers convenience if you want automatic brewing.
```

### Output (JSON Report)
```json
{
  "content_id": "article_12345",
  "total_products_found": 3,
  "total_links_injected": 3,
  "disclosure_added": true,
  "links": [
    {
      "product": "Aeropress Go",
      "affiliate_url": "https://amazon.com/dp/B07GYWVYBX?tag=mysite-20",
      "network": "amazon",
      "commission_rate": 4.5,
      "estimated_monthly_earnings": 12.50
    },
    {
      "product": "Melitta Pour Over",
      "affiliate_url": "https://amazon.com/dp/B00FCHBZEA?tag=mysite-20",
      "network": "amazon",
      "commission_rate": 4.5,
      "estimated_monthly_earnings": 8.75
    },
    {
      "product": "Nespresso Vertuo Plus",
      "affiliate_url": "https://amazon.com/dp/B07GYWVYBX?tag=mysite-20",
      "network": "amazon",
      "commission_rate": 4.5,
      "estimated_monthly_earnings": 15.25
    }
  ],
  "total_estimated_monthly_earnings": 36.50,
  "compliance_status": "compliant",
  "processed_at": "2024-01-15T10:30:00Z"
}
```

### Output (CSV Report)
```csv
article_title,product_mentioned,affiliate_link,network,commission_rate,estimated_monthly_earnings
Best Portable Coffee Makers,Aeropress Go,https://amazon.com/dp/B07GYWVYBX?tag=mysite-20,amazon,4.5%,$12.50
Best Portable Coffee Makers,Melitta Pour Over,https://amazon.com/dp/B00FCHBZEA?tag=mysite-20,amazon,4.5%,$8.75
Best Portable Coffee Makers,Nespresso Vertuo Plus,https://amazon.com/dp/B07GYWVYBX?tag=mysite-20,amazon,4.5%,$15.25
```

---

## Tips & Best Practices

### 1. Maximize Commission Rates
- **Network selection**: Configure preferred networks by commission rate
- **Product research**: Some products pay 10%+ on ShareASale vs. 4.5% on Amazon
- **Seasonal optimization**: Adjust preferred networks during high-commission periods
- **Example**: Set CJ Affiliate as primary for electronics (higher rates), Amazon as fallback

### 2. Maintain Content Quality
- **Authenticity first**: Only link to products you genuinely recommend
- **Avoid over-linking**: Limit to 2-3 links per 500 words for readability
- **Contextual placement**: Insert links naturally within sentences, not as afterthoughts
- **Disclosure transparency**: Use clear, honest disclosure language that builds trust

### 3. Optimize Disclosure Placement
- **Top of content**: Place primary disclosure before first link (highest visibility)
- **Inline disclosures**: Use for product roundups with multiple links
- **Footer disclosures**: Acceptable for consistent, recurring affiliate content
- **A/B testing**: Test disclosure wording to find highest conversion rates

### 4. Leverage Analytics
- **Track link performance**: Monitor clicks and conversions by product
- **Identify top performers**: Focus content on high-converting product categories
- **Monitor seasonal trends**: Adjust content strategy based on commission fluctuations
- **Calculate content ROI**: Measure earnings per article to prioritize future content

### 5. Scale Efficiently
- **Batch processing**: Process 50+ articles in single request for speed
- **Content templates**: Create reusable structures for consistent link placement
- **Automation workflows**: Integrate with WordPress cron jobs for automatic updates
- **Quality control**: Review first 5 articles manually before full automation

### 6. Compliance Excellence
- **Regular audits**: Review all content quarterly for compliance
- **Update disclosures**: Refresh language when FTC guidelines change
- **Document everything**: Keep records of all affiliate relationships
- **Train team members**: Ensure all contributors understand FTC requirements

---

## Safety & Guardrails

### What This Skill Will NOT Do

❌ **Insert links to products you don't recommend** — The skill requires human approval of product selections; it doesn't force links into content

❌ **Hide affiliate relationships** — All links include FTC-compliant disclosures; cloaking is explicitly prevented

❌ **Violate affiliate network terms** — The skill validates all links against network policies before injection

❌ **Create misleading content** — Links are only inserted for genuine product mentions, not fabricated recommendations

❌ **Bypass editorial guidelines** — The skill respects your content standards and doesn't auto-approve all detected products

### Compliance Boundaries

- **FTC Endorsement Guides**: All disclosures comply with current FTC regulations (updated quarterly)
- **Network TOS**: Respects affiliate network terms (no cloaking, no incentivized clicks, no misleading claims)
- **Geographic restrictions**: Handles region-specific disclosure requirements (EU GDPR, CCPA, etc.)
- **Content restrictions**: Won't inject links into prohibited categories (weapons, illegal products, adult content)

### Limitations

- **Detection accuracy**: 85-95% accuracy for product mentions; manual review recommended for critical content
- **Network coverage**: Supports 15+ major affiliate networks; niche programs require manual setup
- **Language support**: Best performance in English; other languages available but with lower accuracy
- **Real-time updates**: Commission rates updated daily; may lag 24 hours behind network changes

---

## Troubleshooting

### Common Issues & Solutions

**Q: "API key not recognized" error**
- **Solution**: Verify `AFFILIATE_API_KEY` environment variable is set correctly
- **Check**: Run `echo $AFFILIATE_API_KEY` to confirm the value
- **Reset**: Generate new API key in dashboard if key is expired (90-day rotation)

**Q: Links are being inserted for products I don't recommend**
- **Solution**: Use `exclude_brands` configuration to blacklist specific brands
- **Example**: `exclude_brands: ["competitor-brand", "low-quality-product"]`
- **Manual review**: Enable `require_approval` mode to review each link before insertion

**Q: FTC disclosure not appearing in output**
- **Solution**: Verify `FTC_DISCLOSURE_TEXT` environment variable is set
- **Check**: Ensure `disclosure_position` is set to "top" or "inline"
- **Validate**: Test with simple 2-sentence content to isolate the issue

**Q: Amazon Associates links returning 404 errors**
- **Solution**: Verify `AMAZON_ASSOCIATES_ID` format is correct (should be "name-20")
- **Check**: Confirm product ASIN is valid by visiting Amazon product page
- **Update**: Re-authenticate Amazon account if token has expired

**Q: Processing is slow for large content libraries**
- **Solution**: Enable batch processing mode (processes 100 articles in parallel)
- **Optimize**: Reduce `min_commission_rate` threshold to include more products
- **Schedule**: Run bulk jobs during off-peak hours to avoid rate limiting

**Q: Commission rates are lower than expected**
- **Solution**: Check `preferred_networks` configuration; some networks pay more for specific categories
- **Research**: Compare rates across networks for your product category
- **Example**: Electronics often pay 10%+ on ShareASale vs. 4.5% on Amazon

**Q: Affiliate links work but don't track conversions**
- **Solution**: Verify UTM parameters are being added correctly
- **Check**: Test link in incognito browser to ensure cookies are tracking
- **Validate**: Confirm affiliate account is properly connected to network

**Q: Content formatting is broken after link injection**
- **Solution**: Specify correct `link_format` (markdown, html, or plain_text)
- **Check**: Review output format matches your platform (WordPress, Ghost, etc.)
- **Validate**: Test on single article before processing entire library

### FAQ

**Q: Can I use this with WordPress?**
A: Yes! The