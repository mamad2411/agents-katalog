---
name: bargain-finder
description: |
  Find local marketplace bargains via browser tools and send top deals to Telegram.

  Use when user mentions:
  - "find deals on Facebook Marketplace"
  - "search Craigslist for bargains"
  - "find local deals" or "marketplace deals"
  - "bargain finder" or "deal finder"
---

# Bargain Finder

Find the best local bargains on Facebook Marketplace and Craigslist using browser automation. Returns a curated list of top 3–5 deals with mini-reports explaining why each is a great bargain.

---

## Purpose

Automated deal discovery for local marketplace listings. Scans Facebook Marketplace and Craigslist, applies intelligent filtering, and delivers a concise summary of the best bargains to Telegram.

---

## Default Location

**Search Center:** 957 Hayes St, San Francisco, CA (94117)  
**Default Radius:** 5 miles

---

## Prerequisites

1. **Chrome with OpenCode Browser Extension** — Browser automation requires the extension installed and running
2. **Telegram Configured** — Telegram bot token and chat ID must be set up (see telegram skill)

---

## Inputs (from User Prompt)

| Input | Required | Description |
|-------|----------|-------------|
| `items` | ✅ Yes | List of items to search for (e.g., "yamaha receiver", "coffee table", "dining chairs") |
| `brand preferences` | ❌ Optional | Specific brands to prioritize or filter for |
| `max price` | ❌ Optional | Maximum price cap per item |
| `condition notes` | ❌ Optional | Preferred condition (new, like new, good, etc.) |

### Default Excluded Keywords

Listings containing these terms are auto-excluded:
- broken
- for parts
- repair
- not working

---

## Bargain Scoring Logic

### 1. Distance First (Primary Rank)

| Distance | Score | Notes |
|----------|-------|-------|
| 0–1 mile | ⭐⭐⭐ Always best | Top priority regardless of price |
| 1–3 miles | ⭐⭐ Acceptable | Good if price is competitive |
| 3–5 miles | ⭐ Only if insanely cheap | Must be ~50% below typical price |

### 2. Price vs Typical

1. Glance at first 8–10 results to estimate typical market price
2. Flag listings priced significantly below the median
3. For 3–5 mile distance: only keep if ~50% or less of typical price

### 3. Condition Quality

- ✅ Clear, well-lit photos
- ✅ Detailed description
- ✅ No damage language ("scratch", "dent", "crack")
- ✅ Complete sets (not missing pieces)

### 4. Urgency Signals (Tie-breakers)

Boost score if listing includes:
- "moving"
- "must go"
- "today"
- "pickup only"
- "OBO" (or best offer)
- "ASAP"

---

## Workflow (Browser Tools Only)

### Step 1: Build Search URLs

For each item in the user's list, construct:

**Facebook Marketplace:**
```
https://www.facebook.com/marketplace/sanfrancisco/search?query=<URL_ENCODED_ITEM>
```

**Craigslist:**
```
https://sfbay.craigslist.org/search/sss?query=<URL_ENCODED_ITEM>&search_distance=5&postal=94117
```

### Step 2: Apply Filters

1. Set radius to 5 miles
2. Sort by closest first (if available)
3. If UI resets location, set back to 957 Hayes St
4. Apply any user-specified filters (price max, condition)

### Step 3: Collect Candidate Listings

For each item, scan first page and open promising listings:

**Capture per listing:**
- Title
- Price
- Distance (from search center)
- Condition notes
- Direct link
- Urgency signals

**Exclude if:**
- Contains excluded keywords (broken, for parts, repair, not working)
- No photos
- No price listed
- Distance unknown AND price not obviously insane

### Step 4: Rank and Select Top 3–5

Ranking algorithm:
1. **Distance bucket** (highest weight)
2. **Price vs typical** (median comparison)
3. **Condition quality** (photo/description assessment)
4. **Urgency signals** (tie-breaker)

Selection rules:
- Prioritize 0–1 mile listings
- Include 1–3 mile if price is good
- Only include 3–5 mile if "insanely cheap" (~50% below typical)

### Step 5: Send Telegram Summary

Format as Markdown message with 2–4 lines per deal.

---

## Telegram Output Format

```markdown
*Daily Bargains (SF 957 Hayes St)* 🛍️

1) $120 — Yamaha receiver + speakers (0.8 mi) [FB link]
   Why it's a deal: ~50% below typical; clean photos, complete set.
   Condition: described as "like new," no damage language.
   Notes: pickup today, seller says "must go."

2) $80 — Solid wood coffee table (2.2 mi) [CL link]
   Why it's a deal: price below similar listings nearby.
   Condition: solid wood, minor scuffs only.
   Notes: moving sale, quick pickup.

3) $45 — Set of 4 dining chairs (1.1 mi) [FB link]
   Why it's a deal: under $12/chair, similar sets go for $100+.
   Condition: "gently used," photos show minimal wear.
   Notes: OBO, seller responsive.

_Searched: yamaha receiver, coffee table, dining chairs_
```

---

## Daily Scheduler Prompt Template

Use this with the scheduler to run daily at 9 AM:

```yaml
---
schedule: "0 9 * * *"
---

@bargain-finder
Find top 3–5 deals near 957 Hayes St, San Francisco. Use browser tools only.
Search Facebook Marketplace and Craigslist for: <items list>.
Apply distance rule (1–3–5 miles), exclude broken listings, and send a short report per deal with why it is great.
Send results via Telegram.
```

---

## Common Gotchas & Solutions

| Issue | Solution |
|-------|----------|
| Facebook requires login | Ensure Chrome has an authenticated Facebook session before running |
| Filters reset on query switch | Re-check radius and location after each new search |
| Listing lacks distance | Skip unless price is obviously insane (e.g., $10 for a couch) |
| Price not shown | Skip — can't evaluate without price |
| Photos unclear or missing | Skip — condition assessment requires photos |
| "For parts" in title | Auto-exclude via keyword filter |
| Multiple items in one listing | Evaluate each item individually; if it's a bundle, price-per-item should be great |
| Telegram not sending | Verify bot token and chat ID are configured correctly |

---

## Examples

### Example 1: Basic Search

**User prompt:**
```
@bargain-finder find deals for yamaha receiver, coffee table, and dining chairs
```

**Expected behavior:**
1. Search Facebook Marketplace for all three items
2. Search Craigslist for all three items
3. Collect 10–20 candidate listings
4. Rank by distance and price
5. Send top 3–5 deals to Telegram with explanations

### Example 2: With Constraints

**User prompt:**
```
@bargain-finder find guitar amps under $200, prefer Fender or Marshall
```

**Expected behavior:**
1. Search for "guitar amp", "Fender amp", "Marshall amp"
2. Apply max price filter ($200)
3. Prioritize Fender and Marshall brands
4. Return best deals within 5 miles

### Example 3: Condition-Specific

**User prompt:**
```
@bargain-finder look for like-new or new office chairs, ergonomic preferred
```

**Expected behavior:**
1. Search for "office chair", "ergonomic chair", "desk chair"
2. Filter for "like new" or "new" condition
3. Prioritize ergonomic in title/description
4. Report top finds

---

## Cleanup (CRITICAL)

After completing the search and sending Telegram summary:

1. **Close all opened tabs** — `browser_browser_release()`
2. **Release browser lock** — ensures other skills can use browser

Never leave browser locked after completion.

---

## Safety & Boundaries

- **Never share seller personal info** publicly (names, exact addresses)
- **Respect platform TOS** — don't scrape aggressively, add delays between requests
- **No automated purchasing** — this skill finds deals, doesn't buy them
- **Verify listings manually** before meeting sellers — this is a discovery tool, not a guarantee

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | Feb 2026 | Initial release — Facebook Marketplace + Craigslist support |
