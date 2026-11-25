---
name: vintage-authenticator
description: |
  Verify authenticity and spot fakes for vintage clothing brands. Analyze tags, stitching, materials, and construction details to determine if items are genuine vintage or reproductions.

  Triggers when user mentions:
  - "is this authentic" or "is this real"
  - "check if vintage or reproduction"
  - "authenticate this" or "spot fake"
  - "vintage tag identification"
  - "identify era or decade"
---

# Vintage Authenticator

Spot fakes and verify authenticity for vintage clothing. Analyzes photos, descriptions, and details to determine if items are genuine vintage or modern reproductions.

---

## What It Does

Helps vintage resellers avoid costly mistakes by:
- **Brand Authentication**: Verifying if designer pieces are genuine
- **Era Dating**: Identifying the decade based on tags, stitching, and materials
- **Reproduction Detection**: Spotting modern fakes and reproductions
- **Red Flag Identification**: Highlighting suspicious construction details

---

## Inputs (from User Prompt)

| Input | Required | Description |
|-------|----------|-------------|
| `brand` | ✅ Yes | Brand name (e.g., "Levi's", "Versace", "Chanel") |
| `description` | ✅ Yes | Item description, construction details, materials |
| `photos` | ⚡ Highly Recommended | Photos of tags, labels, stitching, hardware |
| `price` | ❌ Optional | Listed price (helps assess authenticity likelihood) |
| `seller_info` | ❌ Optional | Seller claims (e.g., "estate sale find", "thrifted") |

---

## Authentication Checklist by Brand

### Levi's Authentication

**Red Flags (Modern/Reproduction):**
- ❌ Care tags with QR codes or URLs
- ❌ "Made in China" on vintage styles (should be USA/Mexico/Japan for pre-2000s)
- ❌ Plastic buttons (vintage uses metal)
- ❌ Perfect, pristine condition on "vintage" items
- ❌ Modern care symbols on tags

**Green Flags (Authentic Vintage):**
- ✅ Big E red tab (pre-1971)
- ✅ Care tag with only text, no symbols (pre-1970s)
- ✅ "Made in USA" or specific mill codes
- ✅ Hidden rivets (pre-1966)
- ✅ Selvedge edge visible when cuffed
- ✅ Paper patch with care instructions

**Era Dating:**
- **1936-1966**: Hidden rivets, no care tags
- **1967-1971**: Care tags introduced, Big E tab
- **1971-1999**: Little e tab, varied care tags
- **2000+**: Modern care symbols, QR codes

---

### Designer Brands (Chanel, Versace, Gucci)

**Red Flags:**
- ❌ Misspelled labels or sloppy embroidery
- ❌ Plastic zippers (should be metal: YKK, Lampo, Riri)
- ❌ Synthetic linings in "vintage leather" bags
- ❌ No serial numbers or date codes
- ❌ Hardware that feels lightweight/cheap
- ❌ Glue visible in construction

**Green Flags:**
- ✅ Matching serial numbers on bag and card
- ✅ Quality hardware with brand engraving
- ✅ Even, precise stitching
- ✅ High-quality lining materials
- ✅ Authentic care cards/dust bags included

---

### Band T-Shirts

**Red Flags:**
- ❌ Double-stitched sleeves (modern)
- ❌ "Made in" tags with countries like China/Pakistan for "vintage"
- ❌ Modern font styles on tour dates
- ❌ Perfect, unworn condition with "vintage" claims
- ❌ Copyright dates after claimed era

**Green Flags:**
- ✅ Single-stitch construction (pre-1990s)
- ✅ Paper-thin, soft cotton from age
- ✅ Faded print consistent with era
- ✅ Tag style matches claimed decade (Screen Stars, Hanes, etc.)

---

## Era Dating Guide

### 1950s-1960s
- Union labels (ILGWU, ACTWU)
- No care tags
- "Made in USA" prominently displayed
- Metal zippers only
- Natural fibers only (no synthetics)

### 1970s
- Care tags introduced mid-decade
- Polyester blends become common
- Platform shoes, bell bottoms
- Bold patterns, earth tones

### 1980s
- "Made in Hong Kong/Taiwan/Korea"
- Bright neon colors
- Oversized silhouettes
- Brand tags with care symbols

### 1990s
- Grunge aesthetic
- Baggy jeans, flannel
- Sportswear brands
- Care tags with symbols standard

### 2000s+
- Fast fashion construction
- Care tags with QR codes/URLs
- Synthetic materials dominant
- "Made in China" on most items

---

## Authentication Workflow

### Step 1: Gather Information

Extract from user input:
- Brand name
- Claimed era/decade
- Material description
- Price point
- Seller claims

### Step 2: Analyze Photos (if provided)

**Tag Analysis:**
- Check for spelling errors
- Look for modern care symbols
- Verify font consistency with era
- Check for QR codes/URLs

**Construction Analysis:**
- Stitching quality (even vs sloppy)
- Hardware type (metal vs plastic)
- Lining material
- Seam construction

**Wear Patterns:**
- Does wear match claimed age?
- Fading consistent with era?
- Fabric thinning in high-friction areas?

### Step 3: Cross-Reference Red/Green Flags

For the specific brand:
- Check against known authentication markers
- Identify any red flags
- Note any green flags
- Assess overall authenticity likelihood

### Step 4: Deliver Verdict

**Confidence Levels:**
- **"Likely Authentic"** (80%+ confidence) - Multiple green flags, no red flags
- **"Probably Authentic"** (60-79% confidence) - Some green flags, minor concerns
- **"Uncertain"** (40-59% confidence) - Mixed signals, need more info
- **"Probably Reproduction"** (20-39% confidence) - Red flags present
- **"Likely Fake"** (0-19% confidence) - Multiple red flags

---

## Output Format

### Authentication Report

```markdown
## Authentication Report: [Brand] [Item Type]

### Verdict: [LIKELY AUTHENTIC / UNCERTAIN / LIKELY FAKE]
**Confidence:** [X]%

### Claimed Era: [Decade]
### Assessed Era: [Decade] (if determinable)

---

### ✅ Green Flags (Authenticity Indicators)
- [Specific authentic detail 1]
- [Specific authentic detail 2]
- [Specific authentic detail 3]

### ⚠️ Red Flags (Concern Indicators)
- [Specific concern 1]
- [Specific concern 2]

### 📋 Detailed Analysis

**Tags & Labels:**
[Analysis of label authenticity]

**Construction:**
[Analysis of stitching, hardware, materials]

**Wear Patterns:**
[Analysis of age-appropriate wear]

---

### 💡 Recommendations

**If buying:**
- [Specific advice for purchase decision]

**If listing:**
- [Specific advice for accurate listing]

**Additional verification:**
- [What else to check/ask for]
```

---

## Examples

### Example 1: Levi's Jeans

**User prompt:**
```
@vintage-authenticator Help me check these Levi's. The tag says "Made in USA 501" and has a red tab with a small e. Care tag has washing symbols. Single-stitched hem. Asking $85 at estate sale.
```

**Expected behavior:**
1. Identify brand: Levi's
2. Note small e tab (post-1971)
3. Note care symbols present (post-1970s)
4. Note "Made in USA" (positive)
5. Assess likely 1980s-1990s era
6. Price point reasonable for authentic vintage
7. Verdict: "Probably Authentic" with 75% confidence

### Example 2: Chanel Bag Suspicion

**User prompt:**
```
@vintage-authenticator This Chanel bag is $200 on Facebook Marketplace. The quilting looks uneven and the CC logo seems off-center. Seller says it's "vintage from the 90s." No serial number card.
```

**Expected behavior:**
1. Flag extremely low price for vintage Chanel
2. Note uneven quilting (red flag)
3. Note off-center logo (red flag)
4. Note missing serial card (red flag)
5. Verdict: "Likely Fake" with 15% confidence
6. Advise against purchase

### Example 3: Band T-Shirt

**User prompt:**
```
@vintage-authenticator Is this a real 1987 Guns N' Roses tour shirt? Single-stitched, paper thin, tag says "Screen Stars." Print is cracked but graphic looks sharp.
```

**Expected behavior:**
1. Identify positive markers: single-stitch, Screen Stars tag, paper thin fabric
2. Note cracked print consistent with age
3. Verify 1987 tour existed
4. Cross-reference Screen Stars tag style with era
5. Verdict: "Likely Authentic" with 85% confidence

---

## Common Gotchas & Solutions

| Issue | Solution |
|-------|----------|
| Poor photo quality | Request clearer photos of tags, labels, hardware |
| Missing key details | Ask for specific photos (interior tags, stitching close-ups) |
| Conflicting signals | Weigh red vs green flags; when uncertain, say so |
| Reproduction vs authentic vintage | Explain difference; some repros are legitimate vintage-style, not claiming to be actual vintage |
| Price too good to be true | Flag as red flag - authentic vintage designer rarely underpriced |
| "Vintage style" vs "Vintage" | Clarify with seller if item is actually old or just vintage-inspired |

---

## Safety & Boundaries

- **This is guidance, not guarantee** - Always verify before high-value purchases
- **No legal authentication** - Cannot provide certificates of authenticity
- **Educational purpose** - Use as learning tool, not sole decision-maker
- **When in doubt, pass** - Better to skip than buy a fake

---

## Resources

### Reference Databases
- **The Vintage Fashion Guild** - Label database and authentication guides
- **Levi's Archive** - Official brand history and dating guides
- **Real Authentication** - Professional authentication service comparison

### Tag Dating Resources
- Union label history (ILGWU dates)
- Care symbol introduction timeline
- Brand-specific tag evolution

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | Feb 2026 | Initial release - Levi's, designer brands, band tees |
