---
name: listing-writer
description: |
  Write compelling vintage clothing descriptions optimized for SEO and sales. Generate platform-specific titles, keyword-rich descriptions, and hashtag strategies.

  Triggers when user mentions:
  - "write listing description"
  - "SEO optimize this listing"
  - "create title for"
  - "description writer"
  - "hashtag suggestions"
---

# Listing Description Writer

Write listings that sell. SEO-optimized titles, compelling descriptions, and strategic keywords that get items found and sold faster.

---

## What It Does

Transforms basic item info into compelling listings:
- **SEO Titles** - Keyword-optimized for search
- **Compelling Descriptions** - Story + specs + urgency
- **Hashtag Strategy** - Platform-specific tags
- **Keyword Research** - What buyers are searching
- **Multi-Platform** - Adapted for Poshmark, eBay, Depop

---

## Inputs (from User Prompt)

| Input | Required | Description |
|-------|----------|-------------|
| `item` | ✅ Yes | Brand, type, style, color, size |
| `condition` | ✅ Yes | Grade + specific flaws |
| `platform` | ⚡ Highly Recommended | Poshmark, eBay, Depop |
| `era` | ❌ Optional | 70s, 80s, 90s, Y2K, etc. |
| `unique_features` | ❌ Optional | Special details that sell |

---

## SEO Title Formulas

### Poshmark Title (60 characters max)

**Formula:**
```
[Brand] [Item] [Style] [Color] [Size] [Era/Key Word]
```

**Examples:**
- "Vintage Levi's 501 Jeans Blue High Waist 28 90s"
- "Patagonia Better Sweater Fleece Green Medium"
- "90s Floral Midi Dress Vintage Grunge Small"

**Keyword Priority:**
1. Brand name (always first if known)
2. Item type (jeans, dress, jacket)
3. Style descriptor (high waist, oversized, cropped)
4. Color
5. Size
6. Era or trend (90s, Y2K, cottagecore)

---

### eBay Title (80 characters max)

**Formula:**
```
[Brand] [Gender] [Item] [Style] [Color] [Size] [Condition] [Keywords]
```

**Examples:**
- "Levi's 501 Women's Jeans High Waist Blue Size 28 Vintage 90s Denim"
- "Patagonia Men's Better Sweater Fleece Jacket Green Size M EUC"
- "Vintage 90s Floral Dress Women's Grunge Cottagecore Small EUC"

**eBay-Specific:**
- Include "Women's/Men's" (helps search)
- Use all 80 characters
- Include material (denim, wool, silk)
- Add "Vintage" if applicable

---

### Depop Title (Keep short, descriptive)

**Formula:**
```
✨ [Era] [Brand] [Item] ✨
```

**Examples:**
- "✨ 90s Vintage Levi's 501 ✨"
- "✨ Y2K Patagonia Fleece ✨"
- "✨ Vintage 70s Floral Dress ✨"

**Depop-Specific:**
- Emoji at start catches attention
- Hashtags go in description
- Keep it casual and aesthetic

---

## Description Templates

### Poshmark Description

```markdown
[Opening hook - style inspiration or vibe]

BRAND: [Brand name]
ITEM: [Item type]
SIZE: [Size on tag] - fits like [actual fit]
CONDITION: [Grade] - [specific details]

MEASUREMENTS (flat lay):
• Shoulder to shoulder: [X]"
• Armpit to armpit: [X]"
• Length: [X]"
• Sleeve: [X]" (if applicable)

[Unique features or details]

[Condition specifics/flaws if any]

[Call to action - bundle, offer, questions]

[Shipping info]

#poshmark #[brand] #[style] #[era] #[category]
```

**Example:**
```markdown
The perfect vintage Levi's for your 90s grunge look! 🖤

BRAND: Levi's
ITEM: 501 High Waist Jeans
SIZE: Tag 28 - fits like modern 27
CONDITION: Good vintage condition with authentic fade and wear

MEASUREMENTS (flat lay):
• Waist: 14"
• Rise: 11"
• Inseam: 30"
• Leg opening: 8"

Classic 90s orange tab Levi's with the perfect worn-in look. Medium wash with natural fading at thighs and knees. Single-stitch construction.

Minor pilling at inner thighs (see photo 4). No holes or stains. Priced accordingly.

Bundle 2+ items for 15% off! 
Smoke-free home. Ships next business day.

#poshmark #levis #vintage #90s #grunge #y2k #jeans #depop #depopfamous
```

---

### eBay Description

```markdown
[Keyword-rich opening paragraph]

Item Specifics:
• Brand: [Brand]
• Style: [Style]
• Size: [Size]
• Color: [Color]
• Material: [Material]
• Condition: [Condition]

Measurements:
[Detailed measurements]

Description:
[Item details, history, features]

Condition Notes:
[Specific flaws or wear]

Shipping:
[Shipping details]

Returns:
[Return policy]
```

**Example:**
```markdown
Vintage 1990s Levi's 501 High Waisted Blue Jeans Women's Size 28 Grunge Denim

These authentic vintage Levi's 501 jeans from the 1990s feature the iconic orange tab and high-waisted fit that's so on-trend right now. Perfect for creating that 90s grunge or Y2K aesthetic.

Item Specifics:
• Brand: Levi's
• Style: 501 High Waist Straight Leg
• Size: Tag 28 (see measurements)
• Color: Medium blue wash
• Material: 100% cotton denim
• Era: 1990s
• Condition: Good pre-owned vintage condition

Measurements (taken flat, approximate):
• Waist: 14 inches (28" circumference)
• Front rise: 11 inches
• Inseam: 30 inches
• Leg opening: 8 inches

The jeans show authentic vintage wear including natural fading at stress points, which is characteristic of genuine vintage Levi's. Single-stitch construction confirms 90s era.

Condition Notes:
• Light pilling at inner thigh area
• Natural vintage fade and whiskering
• No holes, tears, or stains
• All original hardware intact

These jeans have that perfectly broken-in feel that takes years to achieve. The high waist and straight leg silhouette is flattering and versatile.

Ships within 1 business day via USPS Priority Mail. Smoke-free home.

Returns accepted within 30 days if item is not as described.
```

---

### Depop Description

```markdown
✨ [Vibe statement] ✨

[Size/measurements in casual format]
[Condition in casual terms]
[Unique details with emojis]

[Call to action]

Tags: #[tag] #[tag] #[tag]
```

**Example:**
```markdown
✨ your new favorite 90s jeans ✨

size 28 but fits more like 27! 
worn vintage condition with that perfect broken-in feel 🖤
high waist + straight leg = chef's kiss

measurements:
waist: 14" flat
inseam: 30"
rise: 11"

authentic 90s orange tab Levi's 
natural fade and some pilling (gives character tbh)
no holes or stains!

DM for questions or more pics 💌
bundle to save!

Tags: #vintage #levis #90s #grunge #y2k #depop #jeans #aesthetic #thrifted
```

---

## Hashtag Strategy

### Poshmark Hashtags (5 allowed)

**Tier 1 - Always Use:**
- #poshmark
- #[brand name]
- #[item category]

**Tier 2 - Trend/Style:**
- #vintage
- #90s / #y2k / #70s / #80s
- #grunge / #cottagecore / #streetwear
- #depop (cross-platform discovery)

**Tier 3 - Size/Demo:**
- #size[number]
- #plussize / #petite (if applicable)

**Strategy:**
- Use trending hashtags during relevant Posh Parties
- Mix broad (#vintage) and specific (#levis501)
- Research what successful sellers use

---

### eBay Keywords

**Don't use hashtags** - eBay uses item specifics and title keywords instead.

**Key Fields to Fill:**
- Brand
- Style
- Size Type (Regular, Petite, Plus)
- Size
- Color
- Material
- Pattern
- Department (Women's, Men's)
- Occasion
- Features (Pockets, Lined, etc.)

---

### Depop Hashtags (Unlimited, use 10-15)

**Essential Tags:**
- #vintage
- #[brand]
- #[item type]
- #[era] (90s, y2k, 70s, etc.)
- #[style] (grunge, cottagecore, streetwear)

**Discovery Tags:**
- #depop
- #depopfamous
- #thrifted
- #aesthetic
- #[color]
- #[size]

**Trending Tags (2024-2025):**
- #coquette
- #blokecore
- #gorpcore
- #oldmoney
- #tomatoGirl
- #eclecticgrandpa

---

## SEO Keyword Research

### High-Value Keywords by Category

**Vintage Denim:**
- Vintage Levi's
- 501 jeans
- High waisted jeans
- 90s denim
- Mom jeans
- Straight leg
- Orange tab

**Vintage Outerwear:**
- Vintage Patagonia
- Retro-X fleece
- Vintage North Face
- 90s windbreaker
- Vintage barn coat
- Chore coat

**Vintage Dresses:**
- 90s slip dress
- Cottagecore dress
- Vintage floral
- Grunge dress
- Midi dress
- Prairie dress
- 70s boho

**Vintage Tops:**
- Band tee
- Vintage t-shirt
- 90s button up
- Grunge flannel
- Silk blouse
- Vintage sweater

**Y2K/Trending:**
- Y2K top
- Low rise jeans
- Velour tracksuit
- Baby tee
- Cargo pants
- Butterfly top

---

## Copywriting Best Practices

### Opening Hooks That Work

**Vibe/Emotion:**
- "The perfect [item] for your [aesthetic] look"
- "Channel your inner [decade/era]"
- "That [adjective] vintage [item] you've been searching for"

**Scarcity/Urgency:**
- "Hard to find"
- "Rare vintage"
- "One of a kind"
- "Don't sleep on this"

**Problem/Solution:**
- "Finally, vintage jeans that actually fit"
- "The cozy sweater you've been looking for"

### Power Words

- Authentic
- Vintage
- Rare
- Perfect
- Cozy
- Flattering
- Versatile
- Timeless
- Unique
- Statement

### Words to Avoid

- "Nice" (too vague)
- "Good" (use specific condition terms)
- "Thing" (be specific)
- "Stuff" (unprofessional)
- "Pretty" (overused)

---

## Output Format

### Listing Package

```markdown
## 📝 Listing Package: [Item Name]

---

### 🏷️ TITLES BY PLATFORM

**Poshmark (60 chars):**
"[Title]"

**eBay (80 chars):**
"[Title]"

**Depop:**
"[Title]"

---

### 📄 DESCRIPTIONS

**Poshmark:**
```
[Full description]
```

**eBay:**
```
[Full description]
```

**Depop:**
```
[Full description]
```

---

### 🏷️ HASHTAGS

**Poshmark (choose 5):**
[Hashtag list]

**Depop (10-15):**
[Hashtag list]

---

### 🔍 SEO KEYWORDS

**Primary:** [Main keywords]
**Secondary:** [Supporting keywords]
**Long-tail:** [Specific phrases]

---

### 💡 PRO TIPS

- [Platform-specific tip 1]
- [Platform-specific tip 2]
- [Platform-specific tip 3]
```

---

## Examples

### Example 1: Vintage Sweater

**User prompt:**
```
@listing-writer Help me write a listing for this vintage wool Pendleton cardigan. Size M, excellent condition, earth tones, 1970s.
```

**Expected output:**
- Poshmark title: "Vintage Pendleton Cardigan Wool Earth Tone 70s Medium"
- eBay title: "Vintage 1970s Pendleton Cardigan Sweater Wool Earth Tone Women's Size M EUC"
- Depop title: "✨ 70s Vintage Pendleton Cardigan ✨"
- Descriptions tailored to each platform's tone
- Hashtags: #vintage #pendleton #70s #boho #wool #cardigan

### Example 2: Band T-Shirt

**User prompt:**
```
@listing-writer Write me a fire description for this 1992 Nirvana tee. Single-stitch, paper thin, some fading. Authentic vintage.
```

**Expected output:**
- Emphasize authenticity markers (single-stitch, 1992)
- Highlight vintage wear as positive
- Use grunge aesthetic language
- Price guidance: $80-150
- Keywords: grunge, 90s, band tee, vintage nirvana

### Example 3: Y2K Item

**User prompt:**
```
@listing-writer Y2K low rise jeans, light wash, flared. Size 26. Good condition.
```

**Expected output:**
- Depop-focused (Y2K trend strongest there)
- Use trending language: "that girl" aesthetic
- Emojis and casual tone for Depop
- More professional for Poshmark/eBay

---

## Common Gotchas & Solutions

| Issue | Solution |
|-------|----------|
| Title too long | Prioritize brand + item + size |
| Boring descriptions | Add style context and emotion |
| Wrong tone | Match platform culture |
| Missing keywords | Research sold listings first |
| Overusing hashtags | Quality over quantity |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | Feb 2026 | Initial release - Title formulas, description templates, hashtag strategy |
