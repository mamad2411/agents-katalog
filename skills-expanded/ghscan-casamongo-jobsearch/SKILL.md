---
name: fintech-gtm-job-search
description: Reference criteria, company/role definitions, output schema, and search strategies for GTM leadership job search across wealth tech, investment tech, asset management tech, and personal financial management tech
---

# GTM Leadership Job Search — Skill Reference

## Candidate Profile

- **Background:** Fintech professional with direct wealth management and financial services industry experience
- **Target seniority:** Director-level and above (Director, Senior Director, VP, SVP, Head of, C-suite)
- **Target function:** Go-to-market, revenue, and commercial leadership
- **Compensation floor:** $200K+ total compensation (base + bonus/equity). If comp is not listed, still include the role but note "Not disclosed"
- **Location:** Open to anywhere in the US (remote, hybrid, or on-site). Include international roles ONLY if they explicitly allow working from the United States

---

## Role Criteria

### INCLUDE — roles in these functional areas:
- Sales / Enterprise Sales / Revenue (e.g., Head of Sales, CRO, VP Revenue)
- Partnerships / Strategic Alliances / Channel (e.g., Senior Director of Partnerships, Head of Strategic Alliances)
- Business Development / Expansion (e.g., VP Business Development, Head of Market Expansion)
- Go-to-Market / GTM Strategy (e.g., GTM Lead, Head of GTM)
- Client / Relationship Management at a leadership level (e.g., Head of Client Success, VP Client Relations)
- Consulting / Advisory leadership tied to commercial outcomes (e.g., Head of Wealth Consulting, Director Advisory Services)
- General Manager / P&L leadership with commercial focus
- Any other revenue-generating or market-facing leadership role that fits the spirit of the above

### EXCLUDE — do NOT return:
- Engineering, Product, Design, Data Science, or other purely technical leadership roles
- Marketing roles UNLESS the title explicitly combines marketing with GTM/revenue responsibility (e.g., "VP Marketing & GTM" is okay; "Head of Content Marketing" is not)
- Operations, Compliance, Legal, Finance, HR, or other back-office leadership

> Use the examples above as **thematic guidance, not an exhaustive list**. Apply judgment — if a role is clearly revenue/growth-facing leadership at a qualifying company, include it even if the title doesn't match the examples verbatim.

---

## Company Criteria

### Industry Focus — Financial Technology (Fintech) with Wealth & Investment Focus

The company must be a **fintech company** or a **technology company with a wealth management, investment, or financial services vertical**. Target these segments:

#### Wealth Technology (WealthTech)
- Wealthtech SaaS platforms (portfolio management, financial planning, rebalancing, reporting)
- Digital wealth / robo-advisory platforms
- Advisor technology platforms (CRM, client portal, practice management for advisors)
- RIAs and hybrid advisor platforms (registered investment advisors with a tech-forward model)

#### Investment Technology
- Investment management platforms with technology at the core
- Alternative investment / private markets platforms (serving wealth channels, institutional, or both)
- Trading technology / execution platforms
- Fund administration and portfolio analytics technology
- ESG / impact investing technology platforms

#### Asset Management Technology
- Technology platforms serving asset managers (portfolio construction, risk, reporting)
- Index / ETF technology providers
- Institutional investment technology
- Multi-asset class platforms

#### Personal Financial Management (PFM) Tech
- Personal finance / financial wellness platforms
- Retirement tech platforms (401k, retirement planning, decumulation)
- Embedded wealth / banking-as-a-service where wealth management is a primary vertical
- Financial data aggregation platforms serving wealth/investment use cases

#### Adjacent — Include if strong wealth/investment connection:
- Regtech platforms serving wealth management or investment firms
- Data & analytics companies with financial services / wealth vertical
- Software / technology companies with a dedicated FinTech or Financial Services vertical
- Compliance technology for RIAs, broker-dealers, or asset managers

### Company Size & Stage
- **Include all company sizes and stages** — startups (Seed through Growth), private companies, and public companies
- **Prioritize by relevance and momentum** — companies actively hiring for GTM leadership signal growth
- Within results, sort by perceived relevance rather than stage

### Company Exclusions
- Pure insurance tech (unless it has a meaningful wealth management or investment product line)
- Pure banking/payments fintech with no wealth management or investment focus
- Crypto-only companies (unless they have a wealth management or investment platform)
- Pure lending / mortgage tech (unless investment-adjacent)

### Known Companies Watchlist (non-exhaustive, organized by segment)

**WealthTech:** Addepar, Orion, Envestnet, Betterment, Wealthfront, Riskalyze/Nitrogen, Advyzon, Pontera, Farther, Vanilla, Savvy Wealth, LifeYield, Conquest Planning, Jump, InvestCloud, Altruist, RightCapital, Dynasty Financial, Hightower

**Investment Tech:** iCapital, CAIS, YieldStreet, Carta, Forge Global, Republic, Moonfare, AngelList, Vise, Tegus, AlphaSense

**Asset Management Tech:** SEI, Morningstar, BlackRock (Aladdin), FactSet, MSCI, Clearwater Analytics, Enfusion, Arcesium

**PFM / Retirement Tech:** Pershing/BNY, Empower, Guideline, Human Interest, Vestwell, Capitalize, Magnifi

**Adjacent / Data / Regtech:** Broadridge, FIS, SS&C, Compliance.ai, ComplySci, RIA in a Box, Risklick, Aumni

---

## Output Schema

Return results as structured JSON with these fields:

```json
[
  {
    "company": "Company Name",
    "stage": "Series C / Growth / Public",
    "title": "Exact Role Title",
    "url": "Direct URL to job posting",
    "location": "City, State / Remote (US) / Hybrid — City",
    "compensation": "Salary range or Not disclosed",
    "datePosted": "YYYY-MM-DD or approximate",
    "source": "LinkedIn / Greenhouse / Company site / etc.",
    "isNew": true,
    "segment": "WealthTech / InvestmentTech / AssetMgmtTech / PFMTech / Adjacent"
  }
]
```

### Field Definitions
- **company:** Full legal/brand name
- **stage:** Seed / Series A / B / C / D / Growth / Public — if unknown, write "Unknown (Private)" or "Public"
- **title:** Exact title as listed
- **url:** Direct URL to the job posting (not a search results page)
- **location:** City + state, or "Remote (US)" or "Hybrid — City"
- **compensation:** As listed on the posting. If not disclosed, write "Not disclosed"
- **datePosted:** When the role was listed. Flag roles posted within the last 14 days as isNew: true
- **source:** Where you found the listing
- **isNew:** true if posted within last 14 days
- **segment:** Which industry segment the company falls into

---

## Search Strategy

### Sources
1. **LinkedIn Jobs** — search by title keywords + industry filters
2. **Wellfound (AngelList Talent)** — startup-focused roles
3. **Lever & Greenhouse hosted job boards** — search `jobs.lever.co` and `boards.greenhouse.io`
4. **Company career pages directly** — for known companies listed above
5. **Indeed / Glassdoor** — as supplemental sources
6. **Google search** — for roles that may only appear on niche boards or company sites

### Example Search Queries
Starting points — adapt and expand as needed:

**Broad GTM Leadership:**
- `"Head of Sales" OR "VP Sales" fintech wealth management`
- `"Chief Revenue Officer" fintech OR wealthtech OR "investment technology"`
- `"VP GTM" OR "Head of GTM" fintech wealth OR investment OR "asset management"`
- `"Head of Business Development" financial technology`
- `"Director Partnerships" OR "Head of Partnerships" fintech wealth`

**Segment-Specific:**
- `"VP Sales" OR "Head of Sales" "portfolio management" OR "financial planning" OR "investment platform"`
- `"Director" OR "VP" "alternative investments" OR "private markets" sales partnerships`
- `"Head of Sales" "retirement" OR "401k" technology platform`
- `"VP Business Development" "asset management" technology`
- `"CRO" OR "Chief Revenue Officer" "wealth management" OR "investment management" technology`

**Job Board Specific:**
- `site:jobs.lever.co "wealth" OR "investment" OR "fintech" director OR VP OR head sales OR partnerships OR revenue`
- `site:boards.greenhouse.io "wealth management" OR "investment" OR "financial advisor" sales OR partnerships`

**Company-Targeted:**
- `Addepar OR Orion OR Envestnet OR iCapital OR CAIS careers sales director VP`
- `Altruist OR Pontera OR Betterment OR Wealthfront OR Carta open roles sales partnerships director`
- `SEI OR Morningstar OR FactSet OR Clearwater careers "VP" OR "Director" OR "Head" sales revenue partnerships`

### Keyword Variations
Use multiple variations across searches: "Head of," "VP," "Director," "Senior Director," "Chief," "GTM," "Revenue," "Sales," "Partnerships," "Business Development," "Client," "Consulting," "Wealth," "Investment," "Advisory," "RIA," "Financial Advisor," "Asset Management," "Fintech"
