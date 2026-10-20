name: hyperlocal-market-analysis
description: >
  Hyperlocal market opportunity analysis for US service businesses using Census data (income, family
  composition, density, demographics) + competitor signals to rank zip codes by opportunity score,
  validate current strategy, and surface underserved high-value areas. Output: ranked opportunity
  map + strategic recommendations. Reusable for any local service business: events, home services,
  health, education, sports, childcare.
  TRIGGER for: "run market analysis for [city]", "which zip codes should we target", "validate our
  service area", "find underserved neighborhoods", "where should we expand", any request combining
  a geography with audience or revenue opportunity intent, or when user shares zip/Census data.
---

# Hyperlocal Market Analysis Skill

## Purpose
Transform raw US Census demographics + local context into an actionable, ranked opportunity map — telling the
business exactly *where* to focus marketing spend, sales outreach, and service expansion.

---

## Workflow Overview

```
Step 1: Intake — gather service area, business type, ICP, current strategy
Step 2: Data Collection — pull Census + supplemental public data per zip code
Step 3: Scoring — apply weighted opportunity score formula
Step 4: Gap Analysis — compare current targeting vs. highest-opportunity zips
Step 5: Output — ranked map + strategic recommendations
```

---

## Step 1: Intake Interview

Before running analysis, collect the following. Ask all at once in a single message.

**Required:**
- Business type / service (e.g., youth fencing academy, home cleaning, tutoring)
- City or metro area (or list of zip codes if known)
- Current primary service area (neighborhoods, zip codes, or radius)
- Ideal Customer Profile (ICP): household income tier, family type, age of decision-maker
- Current marketing channels and any known performance data

**Optional but valuable:**
- Known competitors and their locations / coverage areas
- Average revenue per client / LTV
- Current client zip code distribution (if available)
- Any zip codes the owner has "gut feel" about (good or bad)

If the user provides partial info, proceed with what's available and note assumptions.

---

## Step 2: Data Collection

### Primary Data Source: US Census Bureau
Use American Community Survey (ACS) 5-Year Estimates, Table-level data by ZIP Code Tabulation Area (ZCTA).

**Key tables to pull (by ZCTA / zip code):**

| Metric | ACS Table | Notes |
|---|---|---|
| Median Household Income | B19013 | Core demand signal |
| Per Capita Income | B19301 | Complements median for skew detection |
| Households with children under 18 | B11005 | Key for youth/family services |
| Population density | B01003 + land area | High density = higher reach efficiency |
| Educational attainment (Bachelor's+) | B15003 | Proxy for affluence and service receptivity |
| Owner-occupied housing | B25003 | Proxy for stability and disposable income |
| Median home value | B25077 | Wealth indicator |
| Age distribution | B01001 | Match to ICP age brackets |
| Commute / work from home | B08301 | Local spend propensity signal |

### How to Access Data (no API key required):
1. **Census Data Explorer**: https://data.census.gov — search by zip code or table ID
2. **Census Reporter**: https://censusreporter.org — faster UX, zip-level profiles
3. **FFIEC Geocoding / Census Tract tool**: https://geomap.ffiec.gov — for precise tract lookup
4. **Opportunity Atlas** (Harvard/Census): https://opportunityatlas.org — income mobility overlays

Codex should:
- Use `web_search` and `web_fetch` to pull publicly available Census data for each relevant zip in the service area
- Cross-reference with Census Reporter profile pages: `https://censusreporter.org/profiles/86000US[ZIPCODE]-[ZIPCODE]/`
- When live data isn't accessible, use Codex's training knowledge of Census ACS estimates and note the vintage year

### Supplemental Public Data Sources:

| Data Type | Source |
|---|---|
| School ratings by zip | GreatSchools.org, NCES |
| Crime index | NeighborhoodScout, SpotCrime |
| Business density (competitors) | Google Maps search, Yelp category search |
| Real estate price trends | Zillow Research (downloadable CSVs) |
| Walkability / transit | Walk Score API (free tier) |

---

## Step 3: Opportunity Scoring Model

Score each zip code on a **0–100 scale** using weighted factors. Weights are defaults — adjust based on
business type (see reference file for weight presets by business category).

### Default Scoring Formula

```
Opportunity Score = 
  (Income Score × 0.30) +
  (Family/ICP Match Score × 0.25) +
  (Density Score × 0.15) +
  (Education Score × 0.10) +
  (Competitor Gap Score × 0.15) +
  (Proximity Score × 0.05)
```

### Scoring Each Dimension (0–10 scale, then normalize):

**Income Score**
- Pull median HH income for zip
- Score relative to metro median: >2× metro median = 10, 1.5–2× = 8, 1–1.5× = 6, 0.75–1× = 4, <0.75× = 2

**Family/ICP Match Score**
- % households with children under 18 (for youth services) or relevant age bracket
- >30% = 10, 20–30% = 7, 10–20% = 5, <10% = 2

**Density Score**
- Population per sq mi: >10,000 = 10, 5,000–10,000 = 7, 2,000–5,000 = 5, <2,000 = 3

**Education Score**
- % adults with Bachelor's or higher: >50% = 10, 35–50% = 7, 20–35% = 5, <20% = 3

**Competitor Gap Score**
- Search for "[business type] [zip code]" on Google Maps; count results within 5mi
- 0 direct competitors = 10, 1–2 = 7, 3–5 = 4, 6+ = 1

**Proximity Score**
- Distance from client's current operational hub / home base
- <5 mi = 10, 5–15 mi = 6, 15–30 mi = 3, >30 mi = 1

---

## Step 4: Gap Analysis

Compare the **ranked zip code scores** against the client's **current targeting**:

1. **Coverage Audit**: Are the client's top-performing or most-marketed zips in the top quartile of scores?
2. **Missed Opportunity Zones**: Which high-score zips are currently unserved or under-marketed?
3. **Low-ROI Zones**: Which currently targeted zips score in the bottom half? Flag for de-prioritization.
4. **Audience Mismatch Test**: Does the ICP the client *thinks* they serve match who actually lives in their current footprint?

Present as a 2×2 if helpful:

```
               HIGH SCORE         LOW SCORE
Currently    | ✅ Core Zone     | ⚠️ Audit for ROI |
Serving      |                  |                   |
─────────────|──────────────────|───────────────────|
Not          | 🎯 Expand Here   | ⬛ Deprioritize   |
Serving      |                  |                   |
```

---

## Step 5: Output Format

Always produce the following sections in this order:

### 1. Executive Summary (3–5 bullet points)
- Market size of total addressable households in ICP range
- Top 3 opportunity zip codes
- Key strategic finding (e.g., "current marketing underserves highest-income corridor by 40%")

### 2. Ranked Opportunity Table

| Rank | Zip Code | Neighborhood | Opp Score | Med HH Income | % Families w/ Kids | Competitor Gap | Notes |
|------|----------|--------------|-----------|---------------|---------------------|----------------|-------|
| 1    | XXXXX    | Name         | 87        | $XXX,XXX      | XX%                 | Low            | ...   |

### 3. Strategic Recommendations
- Minimum 3, maximum 7 recommendations
- Each tagged with: [QUICK WIN], [MEDIUM TERM], or [LONG TERM]
- Each includes the *why* (data backing the recommendation)
- Each includes cross-functional impact note (marketing, ops, staffing, pricing)

### 4. Current Strategy Validation
- "Your current service area scores X on average — here's what that means"
- Flag any significant mismatches between stated ICP and zip demographics

### 5. Data Confidence Note
- State which data is from live web pull vs. Codex training knowledge
- Flag any zips where data was unavailable or estimated
- Recommend a field validation step if confidence is mixed

---

## Adapting Weights by Business Type

Read `/references/weight-presets.md` when the business category matches one of:
- Youth sports / recreation
- Home services (cleaning, landscaping, HVAC)
- Health & wellness
- Private education / tutoring
- Event services (catering, photography, entertainment)
- Personal services (salon, fitness, coaching)

---

## Handling Missing Data

- If zip-level data is unavailable, aggregate to county or Census tract and note the limitation
- If the user cannot share client zip distribution, ask for 3 representative client addresses
- If competitor data is unavailable via web search, ask the user to provide known competitors
- Never fabricate Census figures — state "estimate based on adjacent zip / county average" when extrapolating

---

## Example Trigger Phrases

- "Run market analysis for [city]"
- "Which zip codes in [metro] should we focus on?"
- "Are we targeting the right neighborhoods?"
- "Find me high-income areas near [location] that [business type] isn't serving"
- "Validate our service area for [business]"
- "Where should [business] expand next?"
- "Build me an opportunity map for [city/region]"