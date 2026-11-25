---
name: local-power-mapping
description: Regional power player OSINT — identify wealthy, influential, and high-net-worth individuals in a specific geographic area for networking, partnership, or business development targeting. Covers the discovery phase (finding who matters) before any individual investigation begins.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [osint, power-mapping, influence, wealth, networking, business-development, regional-intelligence]
    triggers: [power-players, influential-people, wealthy-people-in, who-matters-in, power-map, regional-osint, local-movers-and-shakers]
    related_skills: [osint-recon, osint-person, osint-business, osint-property, land-acquisition-research]
---

# Local Power Mapping (Regional Influence OSINT)

Identify the wealthy, powerful, and influential people in a specific geographic area. This is the **discovery phase** — finding WHO the players are **before** you investigate any individual in depth. It answers: "Who in this area could help me advance my agenda, partner on deals, or open doors?"

## When to Use This Skill

You are asked to:
- "Who are the power players in [region]?"
- "Find wealthy/influential people near me I should network with"
- "Map the rich and powerful in [city/county]"
- "Who are the billionaires/multi-millionaires in [area]?"

## Prerequisites & Tool Reality

**Critical context as of 2026:** All major search engines (Google, Bing, DuckDuckGo) block automated curl/terminal requests with CAPTCHAs. You CANNOT rely on `web_search` or curl-based search engine scraping.

### Tools That Work
- **Wikipedia API** — reliable, no CAPTCHA. Use for verifying known individuals and finding notable residents of cities
- **Direct site access** — business journals, local news, Forbes lists (some may have paywalls)
- **Your training data** — the model has substantial knowledge of wealthy families, regional dynasties, and business empires. Use it as a starting point, then verify what you can
- **Browser (CDP connected)** — if available, use for targeted lookups on specific sites

### Tools That Do NOT Work
- curl-based search engine queries (Google, DDG, Bing all CAPTCHA)
- Most local news sites with paywalls (Times Union, BizJournals) — require subscription or human verification
- Wikipedia search API for specific wealth queries (returns poor results for "billionaire near X" type queries)

## Step-by-Step Methodology

### Phase 1: Structure the Region

Break the target area into logical tiers:

```
Tier 1: The target city/town itself (e.g., your city, NY)
Tier 2: The metro area core (e.g., Schenectady, Albany, Troy, Saratoga Springs)
Tier 3: The broader region / exurbs
Tier 4: Seasonal/second-home residents (if applicable — Saratoga race season, ski towns, etc.)
```

### Phase 2: Identify Wealth Categories

Power players typically fall into these buckets in any region:

1. **Family-Owned Business Dynasties** — multi-generational companies (retail, manufacturing, banking)
2. **Real Estate Barons** — commercial/residential developers, landowners
3. **Banking & Finance Families** — community/regional bank owners, credit union founders
4. **Healthcare Executives** — hospital CEOs, medical practice founders, pharma facility execs
5. **Tech / R&D Leaders** — major employer execs (GE, Regeneron, IBM, globalFoundries)
6. **Institutional Gatekeepers** — university presidents, chamber of commerce heads, foundation directors
7. **Political Power** — state senators, county executives, mayors (especially long-serving)
8. **Seasonal / Second-Home Wealth** — people who live elsewhere but have homes locally (racing season, ski season)
9. **Professional Services Kings** — top law firm partners, accounting firm heads, wealth managers
10. **Legacy Families** — old money from the area's industrial heyday

### Phase 3: Information Gathering (per category)

**For each candidate, collect:**
- Full name and family relationships
- Company/entity name and estimated worth
- Where they're based (specific town, neighborhood, or street)
- What technologies / business systems they run
- Personal interests, hobbies, memberships
- Charitable boards they sit on (goldmine for networking)
- Places they frequent (country clubs, restaurants, events, race tracks)
- Their business NEEDS (what do they buy? what land do they need? what services?)

### Phase 4: Verify What You Can

Use Wikipedia API to check named individuals:

```bash
# Wikipedia API — works reliably with curl
curl -sL -A "Mozilla/5.0" \
  "https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exintro=true&explaintext=true&titles=Trustco_Bank&format=json"
```

Check city notable-people lists:
```bash
curl -sL -A "Mozilla/5.0" \
  "https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exintro=true&explaintext=true&titles=Schenectady,_New_York&format=json"
# Then grep the Notable People section from the extract
```

Check company Wikipedia pages for founder/officer info:
```bash
curl -sL -A "Mozilla/5.0" \
  "https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exintro=true&explaintext=true&titles=Stewart%27s_Shops&format=json"
```

### Phase 5: Cross-Reference & Compile

Look for connections, overlaps, and common threads:
- Same country club memberships
- Same charitable boards
- Same political donors
- Same business partnerships
- Family intermarriages

This reveals who is already connected to whom — and where YOU might fit in.

## Capital Region (NY) Pattern Example

The Capital Region of New York (Albany/Schenectady/Troy/Saratoga) has a predictable power structure:

**Level 1 ($1B+):** Galesi Group (real estate), Golub family (Price Chopper/Market 32), Dake family (Stewart's Shops)
**Level 2 ($500M-$1B):** McCormick family (Trustco Bank — note: based in your city, same town as the operator)
**Level 3 ($100M-$500M):** Kiernan family (Pioneer Bank), Barba (Albany Med), Regeneron facility execs, Margolis family
**Gatekeepers:** Chamber CEO, university presidents, hospital boards
**Seasonal:** Saratoga Race Course owners/trainers, hedge fund summer residents

**Common networking vectors:** Saratoga Race Course (July-September), chamber events, charity galas for Albany Med/SPAC/Saratoga Hospital, Wolferts Roost Country Club, Mohawk River Country Club

See `references/capital-region-ny-power-players.md` for the full dossier generated from a real session.

## Common Pitfalls

### Search Engine Blocking
- **PITFALL:** Trying to scrape Google/DuckDuckGo for "wealthy people in X" — this will fail with CAPTCHA every time.
- **SOLUTION:** Use Wikipedia API, direct site access, or your training data as a starting point.
- **WORKAROUND:** If you absolutely need search results, try Bing's mobile API or use a browser with a connected CDP session.

### Paywalled Local News
- **PITFALL:** Local business journals (Albany Business Review, Times Union) have paywalls that block automated access.
- **SOLUTION:** Check if the Wayback Machine has archived the article. Use the CDX API to find cached copies.
- **WORKAROUND:** The article snippet in search results often contains enough to identify the key names.

### Stale Data
- **PITFALL:** Business owners die, sell, or retire. Old Forbes lists from 5 years ago are misleading.
- **SOLUTION:** Cross-check with recent business activity. Check if the company is still family-operated. Search obituaries.
- **WORKAROUND:** Use Secretary of State business entity search to verify active status.

### Confusing Registered Agent with Actual Person
- **PITFALL:** Entity filings list the registered agent's address, not the actual business address.
- **SOLUTION:** Look for "Principal Address" vs "Registered Agent" on business filings.
- **WORKAROUND:** Property records reveal where business owners actually live/work.

## Cross-References

- `security/osint-recon` — Take identified individuals here for deep investigation
- `security/osint-person` — Enrich individual profiles once you have names
- `security/osint-business` — Trace corporate ownership of identified entities
- `security/osint-property` — Check identified individuals for property holdings
- `software-development/land-acquisition-research` — If the power mapping is for real estate purposes
- **`business-development/local-market-elite-networking`** — After identifying who the power players are, use this skill for the strategy/penetration phase: dual-track positioning, event calendars, club entry, and approach scripts. This skill is the "who" discovery; that skill is the "how" execution.

## Verification Checklist

- [ ] Region broken into logical tiers (target town, metro core, broader region, seasonal)
- [ ] At least one candidate identified in each wealth category (family business, real estate, banking, healthcare, tech, institutional, political)
- [ ] Each candidate has: full name, business, estimated worth range, location/neighborhood
- [ ] At least 2 sources support each significant claim
- [ ] Connections/overlaps mapped between candidates (same clubs, boards, charities)
- [ ] Networking vectors identified (events, clubs, venues where power players congregate)
- [ ] Written report organized by tier/priority for the user's specific goal
- [ ] Most actionable candidates flagged with specific approach recommendations
