---

name: landglide-lookup
description: landglide-lookup lets the user search a property by address, parcel number, owner name, or GPS coordinates and pull parcel-level intelligence like owner details, assessed value, sale history, acreage, zoning, flood-zone clues, and building facts, then pair that with skip-trace style research so they can understand both the land and the person behind it before making a move.
category: openclaw-imports

---
**Query the national parcel database by address, parcel ID, owner name, or GPS coordinates. Returns parcel boundaries, ownership info, assessed values, acreage, land use, and more.**

## What This Skill Does

This skill landglide-lookup lets the user search a property by address, parcel number, owner name, or GPS coordinates and pull parcel-level intelligence like owner details, assessed value, sale history, acreage, zoning, flood-zone clues, and building facts, then pair that with skip-trace style research so they can understand both the land and the person behind it before making a move.

## API Details
- **Base URL:** `https://reportallusa.com/api/`
- **Client Key:** `nBkKeHaA6m`
- **API Version:** `v=9` (current)
- **Rate Limit:** 20 requests/second
- **Docs:** https://reportallusa.com/solutions/overlay/documentation/

## Endpoints

### 1. Account / Quota Check
```
GET https://reportallusa.com/api/account?client=nBkKeHaA6m
```
Returns remaining quota and usage info. Always check this first if troubleshooting.

### 2. Address Lookup (Most Common)
```
GET https://reportallusa.com/api/parcels?client=nBkKeHaA6m&v=9&address=STREET_ADDRESS&region=REGION
```
- `address`: Street address (no state needed if region is provided)
- `region`: County name, State abbreviation, or ZIP code
- Returns: parcel boundary (WKT), owner info, assessed value, sale data, acreage, building info

**Examples:**
- `address=109 North Main Street&region=Baltimore`
- `address=1600 Pennsylvania Ave&region=DC`
- `address=500 Main St&region=MD`
- `address=123 Elm St&region=21201`

### 3. Parcel ID Lookup
```
GET https://reportallusa.com/api/parcels?client=nBkKeHaA6m&v=9&parcel_id=PARCEL_ID&region=REGION
```

### 4. Owner Name Lookup
```
GET https://reportallusa.com/api/parcels?client=nBkKeHaA6m&v=9&owner=Lastname%20Firstname&region=REGION
```
- Supports `*` wildcard (e.g., `owner=Smith*&region=MD`)
- Returns all parcels matching the owner name

### 5. Spatial Point Lookup
```
GET https://reportallusa.com/api/parcels?client=nBkKeHaA6m&v=9&spatial_intersect=LON+LAT&si_srid=4326
```

### 6. Spatial Polygon Lookup
```
GET https://reportallusa.com/api/parcels?client=nBkKeHaA6m&v=9&spatial_intersect=WKT_POLYGON&si_srid=4326
```

### 7. Generate Auth Token
```
GET https://reportallusa.com/api/auth?client=nBkKeHaA6m&timestamp=EPOCH
```

## Standard Filter Parameters
Add these to any parcels query:
- `sale_price_min`, `sale_price_max`
- `mkt_val_tot_min`, `mkt_val_tot_max`
- `bldg_sqft_min`, `bldg_sqft_max`
- `acreage_min`, `acreage_max`
- `land_use_class` (Residential, Agricultural, Commercial, Industrial, etc.)
- `county_id`, `state`, `zip`

## Response Headers (Quota Tracking)
- `x-reportall-api-parcels-request-quota-used` — parcels quota consumed
- `x-reportall-api-tiles-quota-remaining` — tiles remaining
- Quota periods: `alltime`, `month`, `day`, `hour`

## Key Field Mappings (v9)
| v9 Field | Description |
|----------|-------------|
| `addr_full` | Full property address |
| `addr_city` | City |
| `addr_state` | State |
| `addr_zip` | ZIP code |
| `owner_name` | Owner of record |
| `owner_mailing_addr` | Mailing address |
| `mkt_val_tot` | Total market value |
| `mkt_val_land` | Land value |
| `mkt_val_bldg` | Building value |
| `sale_price` | Last sale price |
| `sale_date` | Last sale date |
| `bldg_sqft` | Building square footage |
| `lot_sqft` | Lot square footage |
| `acreage` | Acreage |
| `land_use_code` | Land use classification code |
| `land_use_class` | Land use class (Residential, etc.) |
| `year_built` | Year built |
| `zoning` | Zoning designation |
| `geom_as_wkt` | Parcel boundary in WKT format |
| `robust_id` | Unique parcel identifier (persistent) |
| `county_id` | County identifier |

## Usage Examples

### Example 1: Look up a property by address
**User says:** "Look up 109 North Main Street in Baltimore, MD using LandGlide."

**Agent workflow:**
1. URL-encode the query:
   ```bash
   curl -s -D- "https://reportallusa.com/api/parcels?client=nBkKeHaA6m&v=9&address=109%20North%20Main%20Street&region=Baltimore" 2>&1
   ```
2. Parse the JSON response
3. Extract and present key fields: address, owner, market value, sale price, acreage, sqft, zoning, year built
4. Include parcel boundary if relevant (WKT format)

### Example 2: Quick quota check
**User says:** "How many LandGlide lookups do we have left?"

**Agent workflow:**
```bash
curl -s -D- "https://reportallusa.com/api/account?client=nBkKeHaA6m" 2>&1
```
Report the quota headers.

### Example 3: Find all parcels by owner
**User says:** "Find all properties owned by Smith in Maryland."

**Agent workflow:**
```bash
curl -s "https://reportallusa.com/api/parcels?client=nBkKeHaA6m&v=9&owner=Smith*&region=MD" 2>&1 | jq '.parcels[] | {address, market_value, acreage}'
```

## Important Notes
- Always URL-encode addresses with spaces and special characters
- Use `POST` instead of `GET` for very long query strings (>2KB)
- The response returns a list of parcels — even single-address queries may return an array
- Always check quota headers to monitor usage
- Rate limit is 20 req/sec — don't flood the API
- For MD properties, SDAT (State Department of Assessments and Taxation) is the official state data source; LandGlide provides national parcel GIS data
- If a lookup returns no results, try a simpler query: just house number + street name, or try the ZIP as region instead of city

---

## Phase 2: Owner Skip Tracing (After Parcel Lookup)

When the user wants to skip trace the property owner after the LandGlide lookup, follow this workflow:

### Step 1: Extract Owner Name
Take the `owner` field from the LandGlide results (e.g., "STATON DERRELL").

### Step 2: Multi-Prong Web Search (3 parallel searches)
Run these web searches simultaneously:

```
Search 1: "\"OWNER_NAME\" CITY STATE phone email"
Search 2: "\"OWNER_NAME\" ADDRESS STREET CITY social media"  
Search 3: "\"OWNER_NAME\" CITY STATE property records contact"
```

### Step 3: Extract from Results
For each promising result, use web_extract to pull contact details. Focus on:
- **RocketReach.com** — phone numbers and emails (requires login for full details, but snippet often shows partials)
- **FMCSA / DOT records** — if owner has a trucking business, full phone and email are visible (e.g., newbizbot.ai)
- **LinkedIn** — professional profiles with work history (linkedin.com/in/[profile])
- **Facebook** — personal or business pages
- **CyberBackgroundChecks / Spokeo** — confirm name/phone/address match
- **Business registries** — state corporation filings with officer contact info

### Step 4: Compile Contact Card
Format findings as:
- Owner full name (including middle name if found)
- Age (if available)
- Confirmed phone numbers (mark which are confirmed vs partial)
- Confirmed emails (mark business vs personal)
- Social media links
- Business affiliations
- Brief assessment (owner-occupied vs investor, equity position since purchase)

### Step 5: Real-World Example

**Owner:** STATON DERRELL from 944 N HILL Rd, BALTIMORE MD

Skip trace returned:
- Full name: Derrell Antoine Staton, Age 45
- Phone: (443) 418-8929 (confirmed active from FMCSA DOT registration)
- Email: derrell@militaryprepcenter.com (confirmed business email)
- Business: Military Prep Center Trucking LLC, DOT #3336094, Active
- Previous employer: The Pasha Group (1999-2017)
- LinkedIn: linkedin.com/in/derrell-staton-8596b8a1
- Facebook: facebook.com/militaryprepcenter

**Assessment:** Business owner, logistics industry. Owner-occupying since 2006 purchase at $149,900. Current market value $135,400 — property hasn't appreciated significantly. May be candidate if there are other motivations.
