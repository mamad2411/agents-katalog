---
name: platform-optimizer
description: |
  Multi-platform listing strategy for vintage resellers. Determine best platform for each item, calculate fees, cross-post efficiently, and get platform-specific best practices.

  Triggers when user mentions:
  - "where should I sell this"
  - "cross-post to Poshmark and eBay"
  - "platform comparison"
  - "which platform is best"
  - "Poshmark vs eBay"
---

# Reselling Platform Optimizer

Strategic multi-platform selling. Determine where each item will sell fastest and for the most profit. Master cross-posting without the headaches.

---

## What It Does

Optimizes your listing strategy:
- **Platform Selector** - Best platform for each item type
- **Fee Comparison** - True cost across platforms
- **Cross-Posting Workflow** - Efficient multi-platform listing
- **Platform-Specific Tips** - Titles, tags, photos that work
- **Inventory Sync** - Prevent overselling

---

## Inputs (from User Prompt)

| Input | Required | Description |
|-------|----------|-------------|
| `item` | ✅ Yes | Item description, brand, style |
| `price_point` | ✅ Yes | Target sale price |
| `demographic` | ❌ Optional | Target buyer age/style |
| `current_platforms` | ❌ Optional | Where already listed |

---

## Platform Profiles

### Poshmark

**Best For:**
- Women's fashion (70% of users)
- Mid-range brands ($20-100)
- Social sellers who like engagement
- Trending/Gen Z styles
- Bundle-friendly items

**Demographics:**
- 80% female
- Ages 18-45 primarily
- US & Canada only
- Fashion-focused community

**Fee Structure:**
- Flat 20% on all sales
- Buyer pays $7.97 shipping
- No listing fees
- No final value fees beyond 20%

**Selling Style:**
- Social sharing required (self-shares)
- Posh Parties for visibility
- Following/follower dynamics
- Comment-driven negotiation
- Bundle discounts expected

**Listing Best Practices:**
- **Photos:** 8-12 photos, flat lay + modeled preferred
- **Title:** Brand + Item + Key descriptors (60 chars)
- **Description:** Detailed, measurements, flaws disclosed
- **Pricing:** Price 20-30% above expected (negotiation culture)
- **Sharing:** Self-share 2-3x daily minimum

**Time to Sell:**
- Fast movers: 7-14 days
- Average: 21-45 days
- Slow: 60+ days

---

### eBay

**Best For:**
- Men's clothing (strong market)
- Niche/vintage/collectible
- Higher price points ($50+)
- International buyers
- "Buy It Now" or auction

**Demographics:**
- 55% male, 45% female
- Ages 35-65+
- Global reach
- Collector community

**Fee Structure:**
- 13% final value fee (most categories)
- $0.30 per order
- Optional promoted listings (additional %)
- Shipping: Seller or buyer pays

**Selling Style:**
- Listing-focused (less social)
- Search algorithm driven
- Best Offer common
- Auction or fixed price
- Lower engagement required

**Listing Best Practices:**
- **Photos:** 12 photos max, white background preferred
- **Title:** Keyword-stuffed, 80 chars, SEO critical
- **Description:** HTML formatting, detailed specs
- **Pricing:** Competitive with sold comps
- **Item specifics:** Fill out ALL dropdowns (algorithm boost)

**Time to Sell:**
- Fast movers: 10-21 days
- Average: 30-60 days
- Slow: 90+ days

---

### Depop

**Best For:**
- Y2K, 90s, vintage streetwear
- Teens and Gen Z
- Trendy/tiktok viral items
- Graphic tees, baggy jeans
- Artistic/editorial photography

**Demographics:**
- 90% under 26
- Urban, fashion-forward
- UK/Europe strong, growing US
- Creative community

**Fee Structure:**
- 10% Depop fee
- 3.3% + $0.45 Stripe processing
- Total: ~13.3%
- Shipping: Arranged by seller

**Selling Style:**
- Photo aesthetic critical
- Modeled photos expected
- Instagram-like feed
- Following/follower culture
- DM negotiation

**Listing Best Practices:**
- **Photos:** 4 photos, editorial/modeled style
- **Title:** Short, descriptive, hashtags in description
- **Description:** Casual tone, measurements, style tags
- **Pricing:** Firm pricing more accepted
- **Engagement:** Like/follow similar sellers

**Time to Sell:**
- Fast movers: 3-10 days
- Average: 14-30 days
- Slow: 45+ days

---

### Mercari

**Best For:**
- Casual sellers
- General merchandise
- Quick flips
- Bundle sales
- "Decluttering" mindset

**Demographics:**
- Mixed gender
- Ages 25-45
- US only
- Convenience-focused

**Fee Structure:**
- 10% selling fee
- 2.9% + $0.30 payment processing
- Total: ~12.9%
- Shipping: Multiple options

**Selling Style:**
- Simple, quick listing
- Less social engagement
- "Make an offer" culture
- Automatic price drops

**Listing Best Practices:**
- **Photos:** Up to 12, casual acceptable
- **Title:** Descriptive but simple
- **Description:** Bullet points work well
- **Pricing:** Competitive, room for offers

**Time to Sell:**
- Fast movers: 14-21 days
- Average: 30-45 days
- Slow: 60+ days

---

### Facebook Marketplace

**Best For:**
- Local sales
- Heavy/large items
- Quick cash
- No fees (mostly)
- Negotiation

**Demographics:**
- All ages, local
- Casual buyers
- Budget-conscious

**Fee Structure:**
- Free for local pickup
- 5% for shipped items (or $0.40 minimum)
- No listing fees

**Selling Style:**
- Local pickup preferred
- Cash transactions
- Meet in public places
- Quick turnover

**Listing Best Practices:**
- **Photos:** 1-10 photos, real-life settings
- **Title:** Simple, searchable
- **Description:** Brief, condition noted
- **Pricing:** Expect 20-30% negotiation

**Time to Sell:**
- Fast movers: 1-7 days
- Average: 7-14 days
- Slow: 30+ days

---

## Platform Selection Matrix

| Item Type | Best Primary | Secondary | Avoid |
|-----------|--------------|-----------|-------|
| Y2K/Gen Z fashion | Depop | Poshmark | eBay |
| Vintage band tees | Depop | eBay | Mercari |
| 90s streetwear | Depop | Poshmark | Mercari |
| Women's designer | Poshmark | eBay | Depop |
| Men's workwear | eBay | Poshmark | Depop |
| Vintage Levi's | Depop | Poshmark | eBay |
| Patagonia/North Face | Poshmark | eBay | Depop |
| Wool coats | Poshmark | eBay | Mercari |
| Collectible vintage | eBay | - | Poshmark |
| $10-20 items | Poshmark | Mercari | eBay |
| $100+ items | eBay | Poshmark | Depop |
| Local only | Facebook | - | All others |

---

## Cross-Posting Strategy

### Workflow

**Step 1: Primary Platform**
List on best platform first
- Best photos
- Full description
- Optimal pricing

**Step 2: Secondary Platform (24-48 hours later)**
Cross-post if no sale
- Adjust photos for platform style
- Tweak description tone
- Slightly different pricing (avoid exact match)

**Step 3: Third Platform (1 week later)**
If still available
- Consider price drop
- Evaluate if worth effort

### Inventory Management

**Critical:** Track where items are listed

**Methods:**
1. **Spreadsheet:** Item | Poshmark | eBay | Depop | Status
2. **Crosslisting tool:** Use service like List Perfectly
3. **Manual check:** Daily review of all platforms

**When Item Sells:**
1. Mark sold on that platform IMMEDIATELY
2. Delete from other platforms within 1 hour
3. Update inventory tracker

### Pricing Strategy

**Avoid Exact Matches:**
- Poshmark: $45
- eBay: $47  
- Depop: $42

**Account for Fees:**
- List higher on high-fee platforms
- Or accept lower net on convenient platforms

---

## Platform-Specific Optimization

### Poshmark Optimization

**Title Formula:**
```
[Brand] [Item Type] [Style] [Color] [Size] [Key Feature]
Example: "J.Crew Wool Coat Camel Button Front Size M Vintage"
```

**Hashtags:**
- Use all 5 party hashtags
- Add brand hashtags
- Add style hashtags (#vintage, #y2k, #streetwear)

**Sharing Strategy:**
- Morning: 8-10 AM (commute time)
- Lunch: 12-1 PM
- Evening: 8-10 PM (peak activity)

---

### eBay Optimization

**Title Formula:**
```
[Brand] [Item Type] [Style] [Color] [Size] [Condition] [Keywords]
Example: "J.Crew Women's Wool Coat Camel Single Breasted Size Medium EUC Vintage Style"
```

**Item Specifics:**
- Fill out ALL dropdowns
- Brand, size, color, material, style
- Pattern, occasion, department

**Best Practices:**
- Free shipping (baked into price)
- 30-day returns (trust signal)
- Immediate payment required
- Promoted listings for slow movers

---

### Depop Optimization

**Photo Style:**
- Modeled or editorial flat lay
- Natural light
- Aesthetic background
- Show fit/drape

**Description Style:**
```
✨ Vintage [Brand] [Item] ✨

Size: [Size]
Measurements: [Chest/Waist/Length]
Condition: [Grade + details]

DM for questions! 💌

Tags: #vintage #[brand] #[style] #[era]
```

---

## Output Format

### Platform Recommendation Report

```markdown
## 🎯 Platform Optimizer Report

### Item: [Item Description]
**Target Price:** $[X]
**Target Buyer:** [Demographic]

---

### 🏆 Recommended Strategy

**Primary Platform:** [Platform]
**Why:** [Reasoning]

**Secondary Platform:** [Platform]  
**Cross-post timing:** [When]

**Platform to Avoid:** [Platform]
**Why:** [Reasoning]

---

### 💰 Fee Comparison

| Platform | Sale Price | Fees | You Keep | Net Profit |
|----------|------------|------|----------|------------|
| Poshmark | $[X] | $[X] (20%) | $[X] | $[X] |
| eBay | $[X] | $[X] (13%) | $[X] | $[X] |
| Depop | $[X] | $[X] (13.3%) | $[X] | $[X] |
| Mercari | $[X] | $[X] (12.9%) | $[X] | $[X] |

**Best Net Profit:** [Platform] ($[X])

---

### 📋 Platform-Specific Recommendations

**[Primary Platform]:**
- **Title:** "[Suggested title]"
- **Photos:** [Number and style]
- **Pricing:** $[X]
- **Key tactics:** [Specific tips]

**[Secondary Platform]:**
- **Adjustments:** [What to change]
- **Timing:** [When to list]

---

### ⚡ Quick-Start Actions

1. [First action]
2. [Second action]  
3. [Third action]

---

### 📊 Platform Cheat Sheet

| Factor | Best Platform |
|--------|---------------|
| Fastest sale | [Platform] |
| Highest profit | [Platform] |
| Lowest effort | [Platform] |
| Best for this item | [Platform] |
```

---

## Examples

### Example 1: Y2K Jeans

**User prompt:**
```
@platform-optimizer Where should I sell these Y2K low-rise jeans? Targeting $35
```

**Expected output:**
- Primary: Depop (Gen Z audience, trending)
- Secondary: Poshmark (broader reach)
- Avoid: eBay (wrong demographic)
- Depop listing: Editorial photos, casual description
- Poshmark listing: Detailed measurements, professional photos

### Example 2: Vintage Wool Coat

**User prompt:**
```
@platform-optimizer Men's vintage wool coat, J.Crew, excellent condition. Want $85.
```

**Expected output:**
- Primary: eBay (men's market, higher prices)
- Secondary: Poshmark (can work but slower)
- eBay: Fill all item specifics, 12 photos
- Consider: Price at $90 on eBay, $85 on Poshmark

### Example 3: Band T-Shirt

**User prompt:**
```
@platform-optimizer 1994 Nirvana tee, single-stitch, authentic vintage. What's the play?
```

**Expected output:**
- Primary: Depop (vintage band tees hot)
- Secondary: eBay (collector market)
- Depop: Modeled photo, grunge aesthetic
- eBay: Detailed era authentication info
- Price: $120+ (authentic vintage)

---

## Common Gotchas & Solutions

| Issue | Solution |
|-------|----------|
| Overselling | Use spreadsheet or crosslisting tool |
| Different photo styles | Maintain photo library, edit per platform |
| Price matching | Vary prices by 5-10% across platforms |
| Platform fatigue | Start with 1-2 platforms, expand later |
| Fee confusion | Track actual net, not gross sales |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | Feb 2026 | Initial release - Platform profiles, selection matrix, cross-posting workflow |
