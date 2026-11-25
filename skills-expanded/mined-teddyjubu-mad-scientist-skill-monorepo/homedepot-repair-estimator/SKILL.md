---

name: homedepot-repair-estimator
description: homedepot-repair-estimator lets the user turn property photos plus basic room measurements into a contractor-style repair estimate that recommends specific Home Depot materials, calculates likely quantities, shows pricing, explains why each product was chosen, totals the material cost, and packages the result into a usable report for rehabs, buy-box decisions, or seller conversations.

---
## What This Skill Does

This skill homedepot-repair-estimator lets the user turn property photos plus basic room measurements into a contractor-style repair estimate that recommends specific Home Depot materials, calculates likely quantities, shows pricing, explains why each product was chosen, totals the material cost, and packages the result into a usable report for rehabs, buy-box decisions, or seller conversations.

## Current Notion Routing Override

This skill has older examples that mention `Welcome to Notion` or legacy parent pages. Those are superseded. For any new Notion output, use the current `notion-cli` skill, active workspace `Charles Blair’s Space`, parent/migration root `36325ada250d81b08171fa8170e25c82`, then run Publisher Agent validation and send only the published `finalLink` on `bush-gas-a9e.notion.site`.


**Analyze property images, identify needed repairs, and generate contractor-style material estimates with Home Depot pricing.**

## Trigger
Use when the user:
- Sends a property image and asks for repair estimates
- Mentions "Home Depot materials" or "Home Depot estimate"
- Wants pricing for property repairs
- Asks "what materials do I need to fix this room?"
- Says "run the Home Depot estimator"
- Sends any interior property photo (basement, room, garage, etc.)

## Critical Setup Details
- **SerpApi Key**: Stored in `.secrets/serpapi.env`
- **Notion Integration**: Connected via Zapier MCP (already authenticated)
- **Notion Parent Page**: Charles Blair’s Space migration root (user manually organizes later)
- **Image Location**: `/data/.openclaw/media/inbound/` (Telegram images auto-saved here)
- **Report Storage**: `estimates/estimate-YYYY-MM-DD-[address-slug].md`
- **Search Script**: `scripts/search_homedepot.sh` (uses SerpApi Home Depot engine)

## Workflow

### Phase 1: Image Analysis
1. **Locate the image**
   - Check `/data/.openclaw/media/inbound/` for most recent image: `ls -lht /data/.openclaw/media/inbound/*.jpg | head -1`
   - If user sent via Telegram, image will be there automatically

2. **Ask for property details**
   - Before analyzing, ask the user:
     - "What is the property address?"
     - "What are the room dimensions? (Length x Width x Height in feet)"
   - If user doesn't know exact dimensions, ask them to estimate or provide square footage
   - Store address and dimensions for report and Notion page

3. **Analyze the property image**
   - Use `image` tool to analyze the photo
   - Prompt: "Analyze this property image in detail. Identify: (1) Room type, (2) Visible damage or issues (walls, floors, ceiling, fixtures, paint condition), (3) Missing or broken elements, (4) Required repairs categorized by trade (painting, flooring, drywall, electrical, plumbing, HVAC). Be specific about quantities and materials needed."

### Phase 2: Room Type → Flooring Decision (CRITICAL — DO NOT SKIP)
**Use the image analysis to identify the room type, then pick ONE appropriate flooring type:**
- **Bedroom / Living Room** → LVP or carpet (LVP for rentals/flips, carpet for higher-end bedrooms)
- **Kitchen / Bathroom** → Waterproof LVP or sheet vinyl (never carpet or laminate)
- **Basement** → Waterproof LVP with vapor barrier underlayment
- **Hallway / Entry** → LVP or tile (high traffic, durability first)
- **Dining Room** → Laminate or hardwood-look LVP
- **Unknown / Multi-purpose** → Default to LVP (works in any room)

**ONLY recommend ONE flooring product** — not a menu. Pick the best fit, state why, and move on. Never give comparison tables or multiple options. Charles wants one answer, not a catalog.

3. **Extract repair categories**
   - Parse the analysis into material categories (e.g., "drywall repair", "interior paint", "flooring replacement", "light fixtures")

4. **Search Home Depot for each category**
   - Use the search script: `scripts/search_homedepot.sh "<search_term>"`
   - For each major repair category, search Home Depot
   - **Focus on top-rated, popular, contractor-grade products**
   - Search returns top 5 products sorted by popularity/top sellers

5. **Select BEST product for each category**
   - **Choose the #1 recommended product** (typically first result - highest rated/most popular)
   - **Clearly state WHY it's recommended:**
     - "Top seller for [application]"
     - "Contractor favorite - proven durability"
     - "Best value per square foot"
     - "Moisture-resistant formula for basements"
   - **Include full product details:**
     - Complete product name with size/specs
     - Brand name (e.g., "USG Sheetrock", "Behr Premium Plus", "TrafficMASTER")
     - Model number
     - Unit price
     - Product link

6. **Compile materials list**
   - Extract: **full product title**, brand, model, price, link
   - **Calculate accurate quantities using provided room dimensions:**
     - Drywall: (Length + Width) × 2 × Height ÷ 32 sq ft per sheet
     - Paint: Total wall sq ft ÷ 350 sq ft per gallon (primer + finish)
     - Flooring: Length × Width (add 10% for waste)
     - Ceiling tiles: Length × Width (round up to nearest case)
   - Group by repair category with quantity justification
   - **Add "Why this product?" note for each major item**

### Phase 3: Report Generation
6. **Format the estimate**
   - Use template from `references/estimate_template.md`
   - Include:
     - Property condition summary
     - Repair categories with materials
     - Product details (title, brand, price, link)
     - Estimated total cost per category
     - Grand total
     - Notes on labor (not included in materials pricing)

7. **Create Notion page**
   - Use `mcporter call zapier` to create page via existing MCP connection
   - Page title: "[Property Address] - [Property Type] - $[Total Cost]"
   - Parent page: "Home Depot Property Details" (MCP will find/create automatically)
   - Properties include: Address, Date, Property Type, Dimensions, Total Cost
   - Include: condition summary, materials breakdown, total cost

8. **Deliver the report**
   - Save to workspace as markdown: `estimates/estimate-YYYY-MM-DD.md`
   - Reply with formatted estimate + Notion page link to user via Telegram

## Tools
- `image`: Analyze property photos
- `exec`: Run Home Depot search script, call MCP for Notion
- `write`: Save estimate reports
- `mcporter`: Create Notion pages via Zapier MCP

## API Details
- **SerpApi Key**: Stored in `.secrets/serpapi.env`
- **Endpoint**: `https://serpapi.com/search?engine=home_depot`
- **Search script**: `scripts/search_homedepot.sh`

## Example Invocation
**User sends image of damaged bedroom and says:**
> "What materials do I need to fix this up? Give me Home Depot pricing."

**Agent workflow:**
1. Finds image in `/data/.openclaw/media/inbound/`
2. **Asks user**: 
   - "What is the property address?"
   - "What are the room dimensions? (Length x Width x Height in feet)"
3. **User responds**: 
   - "123 Main St, Baltimore, MD 21201"
   - "12 x 14 x 8"
4. Analyzes image → identifies: hole in drywall, peeling paint, damaged baseboards, missing light fixture
5. Calculates quantities:
   - Walls: (12+14)×2×8 = 416 sq ft → 13 sheets drywall
   - Paint: 416 sq ft ÷ 350 = 2 gallons primer + 2 gallons finish
   - Baseboards: (12+14)×2 = 52 linear feet
6. Searches Home Depot for: "drywall sheets", "interior white paint", "baseboards", "ceiling light fixture"
7. Compiles products with accurate quantities and pricing
8. Generates contractor estimate report with dimension-based calculations
9. Creates Notion page: "123 Main St - Bedroom - $487"
10. Delivers markdown report + Notion link via Telegram

---

## Quick Reference

### How User Triggers Skill
- Send property image via Telegram
- Say "Home Depot estimate" or "run the Home Depot estimator"
- Ask "what materials do I need?"

### Required From User
1. Property address (full street address)
2. Room dimensions (Length x Width x Height in feet)

### What Skill Delivers
- ✅ Detailed materials list with specific product names, brands, models
- ✅ Home Depot pricing with product links
- ✅ Quantity calculations based on dimensions
- ✅ "Why this product?" recommendations for each category
- ✅ Total cost breakdown (materials only)
- ✅ Notion page created automatically under Charles Blair’s Space migration root
- ✅ Local markdown report saved to `estimates/`

### Key Files
- **Skill**: `/data/.openclaw/workspace/skills/homedepot-repair-estimator/SKILL.md`
- **Search Script**: `scripts/search_homedepot.sh`
- **Template**: `references/estimate_template.md`
- **Notion Integration**: `references/notion_integration.md`
- **API Key**: `.secrets/serpapi.env`

### Notion Details
- **Parent Page**: Charles Blair’s Space migration root
- **Page Format**: "[Address] - [Room Type] - $[Cost]"
- **Icon**: 🏠
- **User Action**: Manually move pages to "Property Estimate HD" folder after creation

### Important Notes
- Estimates include materials only (no labor)
- Products recommended are top-rated/contractor-grade
- Quantities calculated from user-provided dimensions
- All products available at Home Depot with direct links
- Prices subject to change - verify before purchasing

## Required User Input
**ALWAYS ask for these TWO pieces of information before starting:**
1. **Property Address** - Full street address (e.g., "1929 State Street, Baltimore, MD 21216")
2. **Room Dimensions** - Length x Width x Height in feet (e.g., "15 by 25 by 8")

If user doesn't know exact dimensions, ask for estimates or square footage.

## Product Recommendations
- **Recommend specific products by name** - include full product title, brand, model number
- **Explain WHY each product is recommended** (top seller, contractor grade, best value, etc.)
- Search returns top-rated/popular products - use #1 result as primary recommendation
- Add "Recommended Product" section before pricing table for each category
- Include "Why this product?" reasoning for every major material

## Output Requirements
- **Notion Page**: Create automatically under Charles Blair’s Space migration root parent via Zapier MCP
- **Page Title Format**: "[Address] - [Property Type] - $[Cost Range]"
- **Local Report**: Save markdown to `estimates/estimate-YYYY-MM-DD-[address-slug].md`
- **Include**: Full product names, brands, models, quantity calculations, cost breakdown
- **Materials only** - no labor costs in totals (labor shown as reference)

## Notes
- Always verify image exists before analysis: `ls -lht /data/.openclaw/media/inbound/*.jpg | head -1` or check `/root/.hermes/image_cache/img_*.jpg` for Telegram images
- Calculate quantities using provided dimensions (formulas in Phase 2)
- Include product links for easy ordering
- Zapier MCP connection already configured - no setup needed
- User can manually move Notion pages to "Property Estimate HD" folder after creation

## IMPORTANT: Pricing Fallback Chain (April 2026)

### Tier 1: SerpApi Home Depot Search (BROKEN)
- **The SerpApi account embedded in `scripts/search_homedepot.sh` is DELETED.** The script returns `{"error": "This account has been deleted."}` — it cannot be used.

### Tier 2: web_search + web_extract (UNRELIABLE)
- **Firecrawl web_search credits deplete** — returns `"Payment Required: Failed to search. Insufficient credits"` when quota is exhausted. This happened April 8, 2026.
- `web_extract` on Home Depot product pages also fails when credits are gone.
- **When this works**: `web_search(query="Home Depot <product name/brand> price")` pulls snippet prices, then `web_extract` for full product specs.

### Tier 3: Browser automation (BLOCKED)
- `browser_navigate` to homedepot.com returns "Error Page" — Home Depot aggressively blocks headless browsers even with stealth mode.
- Individual product pages (e.g., `/p/USG-Sheetrock-5-8-in-x-4-ft-x-8-ft-...`) also block with "Error Page".
- **Not viable without residential proxies** (Browserbase proxy support required).

### Tier 4: Embedded Known Prices (RELIABLE — USE WHEN TIERS 1-3 FAIL)
- **Known prices verified April 2026:**
  - USG Sheetrock 1/2" × 4×8 UltraLight: ~$16.61–$17.98/sheet
  - BEHR Premium Plus 1 gal paint: ~$32/gal
  - KILZ 2 All-Purpose Primer 1 gal: ~$22/gal
  - Glidden Premium 1 gal: ~$26–$28/gal
  - House of Fara 4-1/4" MDF Baseboard 8ft: ~$12.98/piece
  - Kwikset Cove Passage Knob: ~$15 each
  - Lifeproof/20-Mil LVP Flooring: ~$2.99/sq ft ($53.76/case of 18 sq ft)
  - Grip-Rite 1-5/8" Drywall Screws 1 lb: ~$9.48
  - FibaTape Mesh 150ft: ~$5.98
- **Image path**: Telegram images land at `/root/.hermes/image_cache/img_*.jpg` (NOT `/data/.openclaw/media/inbound/` — that was the old OpenClaw path)

## Known Pitfalls
- **Home Depot blocks headless browsers** — `browser_navigate` to any homedepot.com URL returns "Error Page" even with stealth features enabled. Browser-based price scraping is **not viable** without residential proxies (Browserbase proxy addon required).
- **Firecrawl credits deplete quickly** — `web_search` and `web_extract` both fail with "Payment Required" when the API quota is exhausted. Always have a fallback plan to use embedded known prices.
- **12-foot historic ceilings** — standard height assumptions (8 ft) are wildly wrong for Baltimore rowhouses. Always verify ceiling height — it affects drywall sheet counts (standard sheets are 8 ft tall, so 12 ft ceilings require horizontal seams or special-order 12 ft panels), paint quantities, and wall area calculations significantly.
- **Historic property lead paint** — assume lead paint is present in any pre-1978 Baltimore rowhouse until tested. Include P100 respirators and lead test kits in estimates.
