---
name: vintage-grader
description: |
  Standardize condition assessment for vintage clothing. Grade items using Poshmark/eBay standards, document flaws, estimate repair costs, and create disclosure checklists for listings.

  Triggers when user mentions:
  - "grade the condition of this item"
  - "is this good or fair condition"
  - "what defects should I note"
  - "condition assessment" or "grade this"
  - "disclosure checklist"
---

# Vintage Condition Grader

Standardize condition assessment for vintage clothing. Provides consistent grading across platforms, flaw documentation guidance, and repair cost estimation.

---

## What It Does

Removes guesswork from condition assessment:
- **Standardized Grading**: Poshmark, eBay, Depop condition scales
- **Flaw Documentation**: What photos to take, how to describe issues
- **Repair Estimation**: Whether fixes are worth the cost
- **Disclosure Checklists**: Platform-specific requirements
- **Pricing Impact**: How condition affects resale value

---

## Inputs (from User Prompt)

| Input | Required | Description |
|-------|----------|-------------|
| `item_description` | ✅ Yes | Item type, material, age |
| `condition_notes` | ✅ Yes | Visible flaws, wear, damage |
| `photos` | ⚡ Highly Recommended | Detailed images of flaws |
| `platform` | ❌ Optional | Poshmark, eBay, Depop, Mercari |
| `original_price` | ❌ Optional | Helps assess repair ROI |

---

## Condition Grading Standards

### Poshmark Scale

**New with Tags (NWT)**
- Never worn, original tags attached
- No flaws, damage, or signs of wear
- Price expectation: 50-70% of retail

**New without Tags (NWOT)**
- Never worn, no tags
- May have been tried on
- No flaws or damage
- Price expectation: 40-60% of retail

**Excellent Used Condition (EUC)**
- Worn minimally, looks nearly new
- No visible flaws
- May show very slight signs of wear
- Price expectation: 30-50% of retail

**Good Used Condition (GUC)**
- Worn moderately
- Minor flaws acceptable (slight pilling, minor fading)
- No major damage
- Price expectation: 20-35% of retail

**Fair Used Condition (FUC)**
- Worn frequently
- Noticeable flaws (pilling, fading, small stains)
- Still functional and wearable
- Price expectation: 10-25% of retail

**Poor Used Condition**
- Heavy wear
- Major flaws (large stains, holes, significant damage)
- May need repair
- Price expectation: 0-15% of retail (or for parts/repair)

---

### eBay Scale

**New with Tags**
- Brand new, unused, unworn
- Original packaging/tags attached

**New without Tags**
- Brand new, unused, unworn
- No original packaging

**New with Defects**
- New but has minor imperfections
- Must specify defect in listing

**Pre-owned**
- Any used item
- Seller must specify condition in description
- Use specific condition descriptors

**For Parts or Not Working**
- Item is damaged/non-functional
- Sold for parts, repair, or craft

---

### Depop Scale

**Brand New**
- Never worn, perfect condition

**Like New**
- Worn once or twice, no flaws

**Good**
- Some signs of wear
- No major flaws

**Worn**
- Noticeable wear
- May have minor flaws

**For Parts/Repair**
- Significant damage
- Not wearable as-is

---

## Flaw Categories & Documentation

### Stains

**Documentation Required:**
- Photo of stain in good lighting
- Close-up showing extent
- Photo with ruler/coin for scale
- Note: Color and approximate size

**Types:**
- **Yellowing** (armpits, collars) - Common, expected on vintage
- **Food/beverage** - Must disclose
- **Oil/grease** - Difficult to remove
- **Rust** - From metal buttons/zippers
- **Ink/makeup** - Often permanent

**Repair Cost:**
- Dry cleaning attempt: $5-15
- Professional stain removal: $15-50
- DIY methods: $0-10

---

### Holes & Tears

**Documentation Required:**
- Photo of hole from front and back
- Photo with finger/coin for scale
- Close-up of fabric surrounding hole
- Note: Size, location, fabric type

**Types:**
- **Pinholes** (< ¼ inch) - Minor, note in description
- **Small holes** (¼-½ inch) - Repairable
- **Large holes** (> ½ inch) - Significant flaw
- **Tears** - Document length and direction
- **Seam splits** - Usually repairable

**Repair Cost:**
- DIY patch: $0-5
- Professional repair: $15-50
- Invisible mending: $30-100+

---

### Pilling

**Documentation Required:**
- Photo showing pilling density
- Close-up texture shot
- Note: Location (armpits common) and severity

**Severity Levels:**
- **Light** - Minimal pilling, barely visible
- **Moderate** - Noticeable but not dense
- **Heavy** - Dense pilling, affects texture

**Repair Cost:**
- Fabric shaver: $10-20 (DIY)
- Professional depilling: $10-30

---

### Fading

**Documentation Required:**
- Photo in natural light showing color variation
- Photo of any high-contrast areas
- Note: Whether fading is even or patchy

**Types:**
- **Even fading** - Often desirable "vintage look"
- **Patchy fading** - More noticeable flaw
- **Sun bleaching** - Usually irreversible
- **Wash fading** - Expected on vintage

**Impact:**
- Even fade: Minimal price impact (authentic vintage)
- Uneven fade: 10-20% price reduction
- Severe fade: 30-50% price reduction

---

### Odors

**Documentation Required:**
- Must disclose in listing
- Note: Smoke, pet, perfume, storage smell

**Types:**
- **Smoke** - Very difficult to remove
- **Pet** - Usually removable with cleaning
- **Perfume/cologne** - Often removable
- **Mildew/musty** - Requires thorough cleaning
- **Storage smell** - Usually airs out

**Repair Cost:**
- Washing/airing: $0-5
- Odor elimination spray: $5-15
- Professional ozone treatment: $25-75

---

### Hardware Issues

**Documentation Required:**
- Photo of damaged/missing hardware
- Close-up of zipper teeth
- Note: Functionality (works/doesn't work)

**Common Issues:**
- **Missing buttons** - Note size, type needed
- **Broken zippers** - Costly to replace
- **Tarnished metal** - Often vintage patina
- **Loose threads** - Easy fix

**Repair Cost:**
- Button replacement: $2-10
- Zipper replacement: $20-50
- Hardware polish: $0-10

---

## Platform-Specific Disclosure Checklists

### Poshmark Checklist

**Required Disclosures:**
- [ ] Any stains (size, location, color)
- [ ] Any holes or tears (size, location)
- [ ] Significant pilling
- [ ] Fading or discoloration
- [ ] Odors (smoke, pet, perfume)
- [ ] Missing or broken hardware
- [ ] Alterations or repairs

**Recommended Photos (minimum 3):**
1. Full item, front view
2. Full item, back view
3. Close-up of any flaws
4. Brand tag/material tag
5. Detail shots of unique features

---

### eBay Checklist

**Required Disclosures:**
- [ ] Accurate condition description
- [ ] All flaws listed in description
- [ ] Specific measurements provided
- [ ] Material/fabric content noted
- [ ] Country of manufacture
- [ ] Any odors mentioned
- [ ] Return policy clearly stated

**Photo Requirements:**
- Minimum 1 photo (12 recommended)
- Show all angles
- Close-ups of flaws
- Tags and labels
- Any included accessories

---

### Depop Checklist

**Required Disclosures:**
- [ ] Condition grade (Brand New to Worn)
- [ ] Any flaws in description
- [ ] Measurements (chest, waist, length)
- [ ] Model info if modeled
- [ ] Shipping time estimate

**Photo Style:**
- Modeled photos preferred
- Flat lays acceptable
- Good natural lighting
- Show flaws honestly
- Multiple angles

---

## Repair ROI Calculator

### Worth Repairing When:

**Always Worth It:**
- High-value item ($100+ resale)
- Simple fix (button, loose seam)
- Vintage designer piece
- Rare/limited item

**Maybe Worth It:**
- Medium value ($30-100 resale)
- Moderate repair (zipper, patch)
- Item has strong market demand

**Not Worth It:**
- Low value (<$30 resale)
- Complex/expensive repair
- Multiple issues
- Oversaturated market

### Cost-Benefit Analysis

```
ROI = (Expected Resale Price - Repair Cost - Acquisition Cost) / (Repair Cost + Acquisition Cost)

If ROI > 100%: Definitely repair
If ROI 50-100%: Probably repair  
If ROI < 50%: Pass or sell as-is
```

---

## Grading Workflow

### Step 1: Visual Inspection

**Examine under good lighting:**
1. Overall appearance at arm's length
2. Color consistency
3. Shape/structure integrity
4. Surface texture (pilling, wear)

### Step 2: Close-Up Inspection

**Check with magnification if needed:**
1. Seams and stitching
2. Fabric for holes/thinning
3. Hardware functionality
4. Stains or discoloration
5. Odors (smell test)

### Step 3: Functional Test

**For wearable items:**
1. Check all closures (buttons, zippers)
2. Test elasticity (waistbands, cuffs)
3. Verify no restricted movement
4. Check lining integrity

### Step 4: Photo Documentation

**Capture required images:**
1. Overall front and back
2. Any identified flaws (close-up)
3. Tags/labels
4. Hardware details
5. Problem areas with scale reference

### Step 5: Grade Assignment

**Using platform-specific scale:**
- Be conservative (grade lower if uncertain)
- When in doubt, disclose
- Price accordingly

---

## Output Format

### Condition Report

```markdown
## Condition Assessment: [Item Name]

### Overall Grade: [GRADE]
**Platform:** [Poshmark/eBay/Depop]

---

### 📋 Flaw Inventory

| Flaw Type | Severity | Location | Disclosed |
|-----------|----------|----------|-----------|
| [Stain/Hole/Pilling/etc] | [Minor/Moderate/Major] | [Location] | [Yes/No] |

---

### 🔍 Detailed Findings

**Visual Condition:**
[Description of overall appearance]

**Specific Issues:**
1. **[Issue 1]**: [Detailed description]
   - Photos needed: [What to capture]
   - Repair cost: $[X]
   - Price impact: [X]%

2. **[Issue 2]**: [Detailed description]
   - Photos needed: [What to capture]
   - Repair cost: $[X]
   - Price impact: [X]%

---

### 💰 Price Impact Analysis

**Suggested Listing Price:** $[X]
**Without flaws would be:** $[Y]
**Price reduction due to condition:** [Z]%

**Repair ROI:**
- Repair cost: $[X]
- Value after repair: $[Y]
- ROI: [Z]% → [Recommend repair / Don't repair]

---

### 📸 Required Photos

**Must Include:**
1. [Photo 1 description]
2. [Photo 2 description]
3. [Photo 3 description]

**Recommended:**
4. [Photo 4 description]
5. [Photo 5 description]

---

### ✍️ Suggested Listing Description Excerpt

"[Condition grade]. [Key flaw disclosures in honest but positive framing]. [Any repairs needed noted]. Overall [summary statement]."

Example: "Good used condition with minor pilling under arms and slight fading consistent with age. No holes, stains, or tears. Vintage Levi's with authentic wear pattern."

---

### ✅ Disclosure Checklist

**Platform Requirements Met:**
- [ ] All flaws disclosed
- [ ] Accurate condition grade
- [ ] Clear photos provided
- [ ] Measurements included
- [ ] Material content noted
```

---

## Examples

### Example 1: Vintage Sweater

**User prompt:**
```
@vintage-grader Help me grade this 1980s wool sweater. There's pilling under the arms, one tiny hole near the hem (size of a pencil eraser), and it smells a bit musty. Listing on Poshmark.
```

**Expected behavior:**
1. Assess overall: Good Used Condition (GUC)
2. Document flaws:
   - Pilling: Moderate, under arms
   - Hole: Small, near hem
   - Odor: Musty (cleanable)
3. Recommend:
   - Grade: GUC
   - Disclose all three issues
   - Suggest washing for odor
   - Price 30-40% below perfect condition
4. Photo requirements:
   - Overall front/back
   - Close-up of pilling
   - Close-up of hole with scale
   - Post-wash freshness

### Example 2: Designer Blouse

**User prompt:**
```
@vintage-grader This silk Equipment blouse has a small makeup stain on the collar and missing one button. Otherwise looks unworn. eBay listing.
```

**Expected behavior:**
1. Assess: New without Defects → Pre-owned due to issues
2. Evaluate:
   - Stain: Likely removable (dry cleaning)
   - Button: Easy replacement
3. Recommend:
   - Clean before listing
   - Replace button ($5 cost)
   - List as "Excellent Used Condition"
   - Full disclosure of prior issues
4. ROI: Repair costs $15-20, value increase $40-60 = Worth it

### Example 3: Vintage Jeans

**User prompt:**
```
@vintage-grader Grade these 1970s Levi's. Heavy fading, some paint splatters, slight fraying at hems. Authentic wear, no holes. Depop listing.
```

**Expected behavior:**
1. Assess: "Worn" on Depop scale
2. Evaluate flaws:
   - Fading: Even, desirable vintage look
   - Paint: Character flaw, disclose
   - Fraying: Minor, authentic wear
3. Context matters:
   - On Depop, worn look is often desirable
   - Paint splatters add "story"
4. Recommend:
   - List as "Worn" (Depop's term)
   - Frame as authentic vintage character
   - Price at vintage premium despite flaws
   - Photos showing authentic wear pattern

---

## Common Gotchas & Solutions

| Issue | Solution |
|-------|----------|
| Uncertain grade | Grade conservatively; better to under-promise |
| Multiple minor flaws | May bump down full grade level |
| Fixable vs disclosure | If easily fixable, consider repairing first |
| Subjectivity | When in doubt, disclose |
| Platform differences | Use platform-specific scale |
| Buyer expectations | Vintage buyers expect some wear; be honest |

---

## Safety & Boundaries

- **Be honest** - Under-grading beats over-grading
- **When in doubt, disclose** - Protects seller rating
- **Don't hide flaws** - Photos must show issues
- **Conservative estimates** - Better to surprise positively
- **Platform rules** - Know each platform's condition requirements

---

## Resources

### Professional Services
- **Dry cleaners** - Stain removal, pressing
- **Tailors** - Repairs, alterations
- **Restoration services** - High-end vintage repair
- **Ozone treatment** - Odor removal

### DIY Supplies
- **Fabric shaver** - Pilling removal
- **Stain remover** - Spot treatment
- **Sewing kit** - Minor repairs
- **Lint roller** - Surface cleaning

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | Feb 2026 | Initial release - Poshmark/eBay/Depop grading, flaw documentation, ROI calculator |
