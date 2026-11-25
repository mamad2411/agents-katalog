---
name: property-contact-research
description: property-contact-research lets the user look up property owners, parcels, and contact information using paid APIs like BatchData, LandGlide, Rentcast, and free public web sources, covering the full workflow from an address to the owner's name, phone, email, and social signals so they can move from raw lead to direct outreach without switching between tools.
category: real-estate
---

# Property Contact Research

**Look up property owners, parcel data, and contact information using paid APIs or free public web sources.**

## What This Skill Does

This skill property-contact-research lets the user look up property owners, parcels, and contact information using paid APIs like BatchData, LandGlide, Rentcast, and free public web sources, covering the full workflow from an address to the owner's name, phone, email, and social signals so they can move from raw lead to direct outreach without switching between tools.

## Umbrella Sections

- **[§1 BatchData Skip Trace](#section-1-batchdata-skip-trace)** — Paid BatchData API: owner name, phones (with DNC/TCPA flags), emails, mailing addresses in one call
- **[§2 LandGlide Parcel Lookup](#section-2-landglide-parcel-lookup)** — ReportAll USA national parcel database: boundaries, ownership, assessed value, acreage, sale history
- **[§3 SDAT Maryland Property Search](#section-3-sdat-maryland-property-search)** — Official Maryland state property tax/assessment database
- **[§4 Rentcast Property Report](#section-4-rentcast-property-report)** — Market rent estimates, property valuations, tenant data
- **[§5 Free Public Skip Trace](#section-5-free-public-skip-trace)** — Web search method when no paid API access is available

---

## §1 BatchData Skip Trace

**Paid BatchData API — single call returns owner + phones + emails + addresses with DNC/TCPA flags.**

### Trigger
Use whenever Charles asks to skip trace, find contact info, or look up an owner's phone/email for a specific property address.

### API Details
- **Endpoint:** `POST https://api.batchdata.com/api/v3/property/skip-trace`
- **Auth:** Bearer token — API key stored in `~/.hermes/skills/property-contact-research/.env` as `BATCHDATA_API_KEY`
- **Content-Type:** `application/json`
- **Accept:** `application/json`
- **Sync vs Async:** Use sync endpoint (`/skip-trace`) for immediate results. Async (`/skip-trace/async`) requires a webhook and is for batch processing.

### Request Format
```json
{
  "requests": [
    {
      "propertyAddress": {
        "street": "<street address>",
        "city": "<city>",
        "state": "<2-letter state abbreviation>",
        "zip": "<5-digit ZIP>"
      }
    }
  ]
}
```

### Valid Address Combinations (pick one)
- `street + city + state + zip`
- `street + zip`
- `street + city + state`

### Response Structure
```json
{
  "status": { "code": 200, "text": "OK" },
  "result": {
    "data": [{
      "input": { "propertyAddress": {...}, "requestId": "..." },
      "property": {
        "id": "<uuid>",
        "address": { "fullAddress": "...", "county": "...", "zipPlus4": "..." },
        "mailingAddress": { ... },
        "owners": [{ "name": { "first": "", "last": "", "full": "" } }]
      },
      "persons": [{
        "propertyOwner": true,
        "name": { "first": "", "last": "", "middle": "", "full": "", "akas": [...] },
        "addresses": [{ "fullAddress": "", "rank": 1, "propertyMailingAddress": true/false }],
        "phones": [{ "rank": 1, "number": "...", "type": "Mobile|Land Line", "carrier": "...", "dnc": false, "tcpa": false, "reachable": true }],
        "emails": [{ "rank": 1, "email": "...", "tested": true }],
        "litigator": false,
        "deceased": false,
        "dob": "YYYY-MM-DD..."
      }],
      "meta": { "matched": true, "error": false }
    }],
    "meta": {
      "results": { "requestCount": 1, "matchCount": 1, "noMatchCount": 0, "errorCount": 0 },
      "requestId": "<ulid>"
    }
  }
}
```

### How to Run
```bash
curl -s -X POST "https://api.batchdata.com/api/v3/property/skip-trace" \
  -H "Authorization: Bearer $BATCHDATA_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "requests": [{
      "propertyAddress": {
        "street": "944 N Hill Rd",
        "city": "Baltimore",
        "state": "MD",
        "zip": "21218"
      }
    }]}' | python3 -c "
import json,sys
d=json.load(sys.stdin)
p=d['result']['data'][0]['persons'][0]
print('OWNER:', p['name']['full'])
print('DOB:', p.get('dob','')[:10])
print()
print('PHONES (DNC-free first):')
for ph in sorted(p['phones'], key=lambda x: x['dnc']):
    dnc='⚠ ON DNC' if ph['dnc'] else '✓'
    print(f\"  {dnc} {ph['number']} ({ph['type']}, {ph['carrier']})\")
print()
print('EMAILS:')
for e in p['emails']:
    print(f\"  {e['email']}\")
"
```

### API Key Setup
Store in `~/.hermes/skills/property-contact-research/.env`:
```
BATCHDATA_API_KEY=your_batchdata_api_key_here
```

### Output for Charles
Always present skip trace results in this format:
- **Owner name + DOB** if available
- **Phones** sorted: DNC-free first, with carrier and type. Flag TCPA-blacklisted
- **Emails** ranked
- **Other known addresses** for the owner
- **"No match"** if `matched: false`

### Pitfalls
- **Wrong base URL:** `api.batchdata.io` fails DNS, `batchdata.io/api/` gets Cloudflare 1010. Correct: `api.batchdata.com/api/v3/`
- **Python urllib blocked:** `execute_code` (urllib) fails with Cloudflare 1010 from this server IP. Always use `terminal` with `curl` — it bypasses the browser signature check.
- **If `matched: false`:** try different address formats ("N" vs "North", "St" vs "Street")
- **Phones with `dnc: true`:** do not call — Charles avoids DNC-listed numbers
- **Multiple owners:** present all persons returned, not just the first one
- **Account key:** Load `BATCHDATA_API_KEY` from the skill `.env`; never paste the live key into this file.

---

## §2 LandGlide Parcel Lookup

**ReportAll USA national parcel database — boundaries, ownership, assessed value, acreage, land use, sale history.**

### API Details
- **Base URL:** `https://reportallusa.com/api/`
- **Client Key:** `nBkKeHaA6m`
- **API Version:** `v=9` (current)
- **Rate Limit:** 20 requests/second
- **Docs:** https://reportallusa.com/solutions/overlay/documentation/

### Endpoints

#### Account / Quota Check
```
GET https://reportallusa.com/api/account?client=nBkKeHaA6m
```
Returns remaining quota and usage info.

#### Address Lookup (Most Common)
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

#### Parcel ID Lookup
```
GET https://reportallusa.com/api/parcels?client=nBkKeHaA6m&v=9&parcel_id=PARCEL_ID&region=REGION
```

#### Owner Name Lookup
```
GET https://reportallusa.com/api/parcels?client=nBkKeHaA6m&v=9&owner=Lastname%20Firstname&region=REGION
```
Supports `*` wildcard (e.g., `owner=Smith*&region=MD`)

#### Spatial Point Lookup
```
GET https://reportallusa.com/api/parcels?client=nBkKeHaA6m&v=9&spatial_intersect=LON+LAT&si_srid=4326
```

### Standard Filter Parameters
- `sale_price_min`, `sale_price_max`
- `mkt_val_tot_min`, `mkt_val_tot_max`
- `bldg_sqft_min`, `bldg_sqft_max`
- `acreage_min`, `acreage_max`
- `land_use_class` (Residential, Agricultural, Commercial, Industrial, etc.)
- `county_id`, `state`, `zip`

### Response Headers (Quota Tracking)
- `x-reportall-api-parcels-request-quota-used`
- `x-reportall-api-tiles-quota-remaining`

### Key Field Mappings (v9)
| v9 Field | Description |
|----------|-------------|
| `addr_full` | Full property address |
| `owner_name` | Owner of record |
| `owner_mailing_addr` | Mailing address |
| `mkt_val_tot` | Total market value |
| `mkt_val_land` | Land value |
| `mkt_val_bldg` | Building value |
| `sale_price` | Last sale price |
| `sale_date` | Last sale date |
| `bldg_sqft` | Building square footage |
| `acreage` | Acreage |
| `land_use_class` | Land use class |
| `year_built` | Year built |
| `zoning` | Zoning designation |
| `geom_as_wkt` | Parcel boundary in WKT format |
| `robust_id` | Unique parcel identifier |

### Usage Example
```bash
curl -s -D- "https://reportallusa.com/api/parcels?client=nBkKeHaA6m&v=9&address=109%20North%20Main%20Street&region=Baltimore" 2>&1
```

### Notes
- Always URL-encode addresses with spaces and special characters
- Rate limit is 20 req/sec — don't flood the API
- For MD properties, use SDAT (State Department of Assessments and Taxation) as the official state data source



---

## §4 Rentcast Property Report

**Market rent estimates, property valuations, and tenant data for US properties.**

### Trigger
Use when Charles wants market rent comparables or investment analysis for a property.

### How to Use
Use the `rentcast-property-report` skill (sub-agent delegation) for the full workflow.

---

## §5 Free Public Skip Trace

**Web search method using free public sources when no paid API is available.**

### When to Use
After you have an owner's name from LandGlide, SDAT, Rentcast, or public records and need to find phone/email/social profiles.

### Step 1: Normalize the Owner Name
LandGlide returns names like "STATON DERRELL" — convert to "Derrell Staton" for better search results. If you have a middle name/initial, use it too (e.g., "Derrell A Staton").

### Step 2: Run 3 Parallel Web Searches
```
Search 1 (Contact): "OWNER_NAME" CITY STATE phone email
Search 2 (Social):  "OWNER_NAME" ADDRESS STREET_NAME CITY social media
Search 3 (Records): "OWNER_NAME" CITY STATE property records contact
```
**Pro tip:** Uncommon last names get clean results. Common names ("Smith", "Johnson") need more specificity — add street name or business name.

### Step 3: Extract from Promising Results
For each promising URL, run `web_extract`:
```
web_extract(urls: [promising_url_1, promising_url_2, ...])
```

**Best sources (in order of usefulness):**
1. **RocketReach.com** — Phone numbers + emails. Partial numbers in snippet, full details need login.
2. **FMCSA / DOT carrier records** — If owner has trucking/logistics business, phone and email are FULLY visible. Goldmine.
3. **LinkedIn** — Professional profile with work history, sometimes email visible.
4. **Facebook** — Personal profile or business page, sometimes phone/email listed.
5. **State business registry** — LLC/Corp officer name and registered agent address are public.
6. **CyberBackgroundChecks / Spokeo / TruePeopleSearch** — Confirm name/phone/address match.
7. **Voter records** — Some states publish voter registration with address and sometimes DOB.
8. **Court records** — County clerk searches show lawsuits, liens, evictions — all public, often include phone numbers.

### Step 4: Cross-Reference and Verify
- Multiple sources show same phone = **confirmed**
- Source contradicts another = **unconfirmed** (flag it)
- Owner has business at different address = note both

### Step 5: Compile the Contact Card
```
OWNER FULL NAME, Age [if found]
Property: [address from records]

PHONE NUMBERS:
- (XXX) XXX-XXXX — confirmed active [source]
- (XXX) XXX-XXXX — unconfirmed [source]

EMAIL:
- name@domain.com — business [source]
- name@gmail.com — personal [source]

SOCIAL MEDIA:
- LinkedIn: linkedin.com/in/[profile]
- Facebook: facebook.com/[profile]

BUSINESS AFFILIATIONS:
- Company name, role, status (Active/Dissolved)
- DOT/EIN if applicable

ASSESSMENT:
[1-3 sentences: owner-occupied vs investor, equity position, motivators]
```

### Example: Derrell Staton — 944 N Hill Rd, Baltimore MD
**Search 1:** "Derrell Staton Baltimore MD phone email"
→ RocketReach: Director at Military Prep Center
→ FMCSA: DOT #3336094, phone (443) 418-8929

**Search 2:** "Derrell Staton Hill Road Baltimore social media"
→ LinkedIn: linkedin.com/in/derrell-staton-8596b8a1
→ Facebook: facebook.com/militaryprepcenter

**Search 3:** "Derrell Staton Baltimore property records contact"
→ CyberBackgroundChecks: Derrell A Staton, Age 45, Baltimore MD

**Result:** Confirmed phone (443) 418-8929 (FMCSA), business email derrell@militaryprepcenter.com, LinkedIn + Facebook, Military Prep Center Trucking LLC (DOT #3336094, Active).

### Notes
- This method is **FREE** — no paid database subscriptions needed
- It won't always find everything — common names or very private individuals may have limited results
- FMCSA/DOT business records are the single best free source when the owner has a trucking or logistics business
- Always verify the person found actually matches the property owner
- Do NOT fabricate phone numbers or emails — if you can't find it, say so
- This is public data only — all info is from publicly accessible records and profiles

---

## §6 SDAT Maryland Property Search

**Official Maryland state property tax/assessment database — browser automation workflow for ownership, assessed values, tax records.**

### Trigger
Use for any Maryland property lookup. SDAT (State Department of Assessments and Taxation) is the authoritative source for MD property data.

### URL
`https://sdat.dat.maryland.gov/RealProperty/Pages/default.aspx`

### Known Browser Automation Pitfalls
This is a legacy ASP.NET government form. It fights browser automation hard.

1. **Close the alert banner FIRST** — On page load there is a Tax Credit alert popup banner. Click Close before touching any form elements.
2. **Use keyboard navigation for dropdowns** — The county and search method dropdowns do NOT respond reliably to clicking option refs. Click the combobox, then `browser_press("ArrowDown")` repeatedly.
   - Baltimore City = 3 ArrowDown presses from -Select one-
   - Street Address = 1 ArrowDown press
3. **Do NOT use Enter to submit** — The page has a site-wide search bar. Pressing Enter submits the HEADER search bar, not the address form. Always click the "Next" button explicitly.
4. **The "Next" button is a form submit** — It must be clicked by its button ref, not via keyboard shortcuts.
5. **URL parameters don't work** — The form must be filled out interactively.
6. **Street number and street name are SEPARATE textboxes** — Verify refs with browser_snapshot before typing.
7. **The header search bar STEALS keystrokes** — Always browser_click() the target textbox IMMEDIATELY before browser_type().
8. **Session restart is your friend** — If the form gets into a bad state, do a full browser_navigate() back and start over.

### Step-by-Step Workflow
```
1. browser_navigate("https://sdat.dat.maryland.gov/RealProperty/Pages/default.aspx")
2. browser_snapshot() — find the Close button ref
3. browser_click(close_button_ref)
4. browser_click(county_combobox_ref)
5. browser_press("ArrowDown") × N  (3x for Baltimore City)
6. browser_click(search_method_combobox_ref)
7. browser_press("ArrowDown") × 1  (for Street Address)
8. browser_click(continue_button_ref)
9. browser_snapshot() — find street number + street name textbox refs
10. browser_click(street_number_ref) — click to focus first
11. browser_type(street_number_ref, "944")
12. browser_click(street_name_ref) — click to focus
13. browser_type(street_name_ref, "N HILL") — no suffix, no period
14. browser_click(next_button_ref) — DO NOT use Enter
15. browser_snapshot() — read results
```

### County Arrow-Down Count Reference
| County | Arrow presses |
|--------|--------------|
| ALLEGANY | 1 |
| ANNE ARUNDEL | 2 |
| BALTIMORE CITY | 3 |
| BALTIMORE COUNTY | 4 |
| CALVERT | 5 |

### What SDAT Shows
- Owner name and mailing address
- Property account identifier (parcel ID)
- Assessed value (land + improvements)
- Use code / property class
- Deed reference
- Sale price and date (most recent transfer)
- Tax credit status

### Alternative: MDLandRec
For deed/title documents, use MDLandRec (https://landrec.msa.maryland.gov) — REQUIRES login credentials. Ask Charles for credentials before attempting.

### Notes
- SDAT may be unavailable before 7:00 AM ET for maintenance
- Data is for informational purposes only
- Baltimore City and Baltimore County are separate entries

---

## §7 Rentcast Property Report

**Rentcast API — automated valuation models (AVM), market rent estimates, comparable sales/rentals, zip-code-level market statistics.**

### Trigger
Use when Charles wants market rent comparables or investment analysis for a US property.

### API Key
`fd06d33c1a0d480c8606b9e301ad7378`

### Command
```bash
python3 ~/.openclaw/workspace/skills/rentcast-property-report/scripts/generate_report.py \
  --api-key 'fd06d33c1a0d480c8606b9e301ad7378' \
  --address "123 Main St, Anytown, USA 12345"
```

### What It Returns
1. **Property Details** — structural attributes, features, tax history, owner info
2. **Value Estimate** — AVM market value + recent comparable sales
3. **Rent Estimate** — AVM market rent + comparable rental listings
4. **Market Statistics** — zip code-level data: median prices, days on market, inventory trends

### Output
JSON dump → format into a user-facing property investment report.

---

## §8 Home Depot Repair Estimator

**Image analysis + Home Depot pricing — contractor-style materials lists with dimension-based quantity calculations.**

### Trigger
Use when user sends a property image and asks for repair estimates, Home Depot pricing, or materials lists.

### Required User Input (ALWAYS ask first)
1. **Property Address** — full street address
2. **Room Dimensions** — Length × Width × Height in feet (e.g., "12 × 14 × 8")

### Workflow

#### Phase 1: Image Analysis
1. Locate image: `ls -lht /root/.hermes/image_cache/img_*.jpg | head -1`
2. Ask user for address and dimensions
3. Use `image` tool to analyze: room type, visible damage, missing/broken elements, repairs by trade

#### Phase 2: Flooring Decision (CRITICAL — ONE product only)
- **Bedroom / Living Room** → LVP or carpet
- **Kitchen / Bathroom** → Waterproof LVP or sheet vinyl (never carpet/laminate)
- **Basement** → Waterproof LVP with vapor barrier
- **Hallway / Entry** → LVP or tile
- **Unknown** → Default to LVP

ONLY recommend ONE product. State why. Move on.

#### Phase 3: Quantity Calculation
- Drywall: (Length + Width) × 2 × Height ÷ 32 sq ft per sheet
- Paint: Total wall sq ft ÷ 350 sq ft per gallon (primer + finish)
- Flooring: Length × Width (add 10% for waste)
- Ceiling tiles: Length × Width (round up to nearest case)

#### Phase 4: Compile Report
- Full product title, brand, model, price, link
- Quantity with justification
- "Why this product?" for each major item
- Grand total (materials only)

### Pricing Fallback Chain

**Tier 1: SerpApi Home Depot Search (BROKEN)**
- SerpApi account DELETED. Script returns `{"error": "This account has been deleted."}`

**Tier 2: web_search + web_extract (UNRELIABLE)**
- Firecrawl credits deplete → "Payment Required: Insufficient credits"

**Tier 3: Browser automation (BLOCKED)**
- Home Depot blocks headless browsers with "Error Page" — not viable without residential proxies

**Tier 4: Embedded Known Prices (RELIABLE FALLBACK)**
Verified April 2026 prices:
- USG Sheetrock 1/2" × 4×8 UltraLight: ~$16.61–$17.98/sheet
- BEHR Premium Plus 1 gal paint: ~$32/gal
- KILZ 2 All-Purpose Primer 1 gal: ~$22/gal
- Glidden Premium 1 gal: ~$26–$28/gal
- House of Fara 4-1/4" MDF Baseboard 8ft: ~$12.98/piece
- Kwikset Cove Passage Knob: ~$15 each
- Lifeproof 20-Mil LVP Flooring: ~$2.99/sq ft
- Grip-Rite 1-5/8" Drywall Screws 1 lb: ~$9.48
- FibaTape Mesh 150ft: ~$5.98

### Known Pitfalls
- **Home Depot blocks headless browsers** — not viable without residential proxies
- **Firecrawl credits deplete** — always have embedded price fallback
- **12-foot historic ceilings** — standard 8 ft assumptions are wrong for Baltimore rowhouses — verify ceiling height before calculating
- **Historic property lead paint** — assume pre-1978 Baltimore properties have lead paint. Include P100 respirators and lead test kits in estimates
- **Image path**: Telegram images land at `/root/.hermes/image_cache/img_*.jpg`


---

## §6 SDAT Maryland Property Search

**Official Maryland state property tax/assessment database — browser automation workflow for ownership, assessed values, tax records.**

### Trigger
Use for any Maryland property lookup. SDAT (State Department of Assessments and Taxation) is the authoritative source for MD property data.

### URL
`https://sdat.dat.maryland.gov/RealProperty/Pages/default.aspx`

### Known Browser Automation Pitfalls
This is a legacy ASP.NET government form. It fights browser automation hard.

1. **Close the alert banner FIRST** — On page load there is a Tax Credit alert popup banner. Click Close before touching any form elements.
2. **Use keyboard navigation for dropdowns** — The county and search method dropdowns do NOT respond reliably to clicking option refs. Click the combobox, then `browser_press("ArrowDown")` repeatedly.
   - Baltimore City = 3 ArrowDown presses from -Select one-
   - Street Address = 1 ArrowDown press
3. **Do NOT use Enter to submit** — The page has a site-wide search bar. Pressing Enter submits the HEADER search bar, not the address form. Always click the "Next" button explicitly.
4. **The "Next" button is a form submit** — It must be clicked by its button ref, not via keyboard shortcuts.
5. **URL parameters don't work** — The form must be filled out interactively.
6. **Street number and street name are SEPARATE textboxes** — Verify refs with browser_snapshot before typing.
7. **The header search bar STEALS keystrokes** — Always browser_click() the target textbox IMMEDIATELY before browser_type().
8. **Session restart is your friend** — If the form gets into a bad state, do a full browser_navigate() back and start over.

### Step-by-Step Workflow
```
1. browser_navigate("https://sdat.dat.maryland.gov/RealProperty/Pages/default.aspx")
2. browser_snapshot() — find the Close button ref
3. browser_click(close_button_ref)
4. browser_click(county_combobox_ref)
5. browser_press("ArrowDown") × N  (3x for Baltimore City)
6. browser_click(search_method_combobox_ref)
7. browser_press("ArrowDown") × 1  (for Street Address)
8. browser_click(continue_button_ref)
9. browser_snapshot() — find street number + street name textbox refs
10. browser_click(street_number_ref) — click to focus first
11. browser_type(street_number_ref, "944")
12. browser_click(street_name_ref) — click to focus
13. browser_type(street_name_ref, "N HILL") — no suffix, no period
14. browser_click(next_button_ref) — DO NOT use Enter
15. browser_snapshot() — read results
```

### County Arrow-Down Count Reference
| County | Arrow presses |
|--------|--------------|
| ALLEGANY | 1 |
| ANNE ARUNDEL | 2 |
| BALTIMORE CITY | 3 |
| BALTIMORE COUNTY | 4 |
| CALVERT | 5 |

### What SDAT Shows
- Owner name and mailing address
- Property account identifier (parcel ID)
- Assessed value (land + improvements)
- Use code / property class
- Deed reference
- Sale price and date (most recent transfer)
- Tax credit status

### Alternative: MDLandRec
For deed/title documents, use MDLandRec (https://landrec.msa.maryland.gov) — REQUIRES login credentials. Ask Charles for credentials before attempting.

### Notes
- SDAT may be unavailable before 7:00 AM ET for maintenance
- Data is for informational purposes only
- Baltimore City and Baltimore County are separate entries

---

## §7 Rentcast Property Report

**Rentcast API — automated valuation models (AVM), market rent estimates, comparable sales/rentals, zip-code-level market statistics.**

### Trigger
Use when Charles wants market rent comparables or investment analysis for a US property.

### API Key
`fd06d33c1a0d480c8606b9e301ad7378`

### Command
```bash
python3 ~/.openclaw/workspace/skills/rentcast-property-report/scripts/generate_report.py   --api-key 'fd06d33c1a0d480c8606b9e301ad7378'   --address "123 Main St, Anytown, USA 12345"
```

### What It Returns
1. **Property Details** — structural attributes, features, tax history, owner info
2. **Value Estimate** — AVM market value + recent comparable sales
3. **Rent Estimate** — AVM market rent + comparable rental listings
4. **Market Statistics** — zip code-level data: median prices, days on market, inventory trends

### Output
JSON dump → format into a user-facing property investment report.

---

## §8 Home Depot Repair Estimator

**Image analysis + Home Depot pricing — contractor-style materials lists with dimension-based quantity calculations.**

### Trigger
Use when user sends a property image and asks for repair estimates, Home Depot pricing, or materials lists.

### Required User Input (ALWAYS ask first)
1. **Property Address** — full street address
2. **Room Dimensions** — Length × Width × Height in feet (e.g., "12 × 14 × 8")

### Workflow

#### Phase 1: Image Analysis
1. Locate image: `ls -lht /root/.hermes/image_cache/img_*.jpg | head -1`
2. Ask user for address and dimensions
3. Use `image` tool to analyze: room type, visible damage, missing/broken elements, repairs by trade

#### Phase 2: Flooring Decision (CRITICAL — ONE product only)
- **Bedroom / Living Room** → LVP or carpet
- **Kitchen / Bathroom** → Waterproof LVP or sheet vinyl (never carpet/laminate)
- **Basement** → Waterproof LVP with vapor barrier
- **Hallway / Entry** → LVP or tile
- **Unknown** → Default to LVP

ONLY recommend ONE product. State why. Move on.

#### Phase 3: Quantity Calculation
- Drywall: (Length + Width) × 2 × Height ÷ 32 sq ft per sheet
- Paint: Total wall sq ft ÷ 350 sq ft per gallon (primer + finish)
- Flooring: Length × Width (add 10% for waste)
- Ceiling tiles: Length × Width (round up to nearest case)

#### Phase 4: Compile Report
- Full product title, brand, model, price, link
- Quantity with justification
- "Why this product?" for each major item
- Grand total (materials only)

### Pricing Fallback Chain

**Tier 1: SerpApi Home Depot Search (BROKEN)**
- SerpApi account DELETED. Script returns `{"error": "This account has been deleted."}`

**Tier 2: web_search + web_extract (UNRELIABLE)**
- Firecrawl credits deplete → "Payment Required: Insufficient credits"

**Tier 3: Browser automation (BLOCKED)**
- Home Depot blocks headless browsers with "Error Page" — not viable without residential proxies

**Tier 4: Embedded Known Prices (RELIABLE FALLBACK)**
Verified April 2026 prices:
- USG Sheetrock 1/2" × 4×8 UltraLight: ~$16.61–$17.98/sheet
- BEHR Premium Plus 1 gal paint: ~$32/gal
- KILZ 2 All-Purpose Primer 1 gal: ~$22/gal
- Glidden Premium 1 gal: ~$26–$28/gal
- House of Fara 4-1/4" MDF Baseboard 8ft: ~$12.98/piece
- Kwikset Cove Passage Knob: ~$15 each
- Lifeproof 20-Mil LVP Flooring: ~$2.99/sq ft
- Grip-Rite 1-5/8" Drywall Screws 1 lb: ~$9.48
- FibaTape Mesh 150ft: ~$5.98

### Known Pitfalls
- **Home Depot blocks headless browsers** — not viable without residential proxies
- **Firecrawl credits deplete** — always have embedded price fallback
- **12-foot historic ceilings** — standard 8 ft assumptions are wrong for Baltimore rowhouses — verify ceiling height before calculating
- **Historic property lead paint** — assume pre-1978 Baltimore properties have lead paint. Include P100 respirators and lead test kits in estimates
- **Image path**: Telegram images land at `/root/.hermes/image_cache/img_*.jpg`
