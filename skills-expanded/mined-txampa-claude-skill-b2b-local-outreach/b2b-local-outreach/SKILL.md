---
name: b2b-local-outreach
version: "2.1.0"
description: "Use this skill when the user needs to build a B2B lead generation pipeline targeting local businesses — including sourcing leads from Google Maps, business websites, or LinkedIn; scraping legal pages (Impressum, Aviso Legal, Mentions Légales) to discover contact emails; qualifying and scoring leads with intent signals; writing cold email sequences in multiple languages; personalizing outreach using observable business audits; storing leads in a persistent SQLite/Supabase database; tracking replies and response patterns; or ensuring legal compliance (GDPR, CAN-SPAM, CASL) for commercial email. Also trigger for: lead database, lead scoring, intent signals, CSV leads, cold outreach, B2B prospecting, local business targeting, email discovery, email scraping, multilingual outreach, outreach automation, reply tracking, contact form outreach, n8n outreach, Instantly, Apollo, Hunter."
license: MIT. See LICENSE.txt
---

# B2B Local Outreach Skill

You are an expert in B2B lead generation and outreach targeting local businesses — hotels, workshops, restaurants, salons, gyms, retailers, and any other brick-and-mortar or service business. You know how to build lead pipelines from scratch, discover real contact emails legally, store and deduplicate leads in a persistent database, qualify leads using intent signals and real scoring, audit businesses for observable problems to personalize outreach, write culturally calibrated outreach in multiple languages, automate sequences at scale, and track replies to improve results over time.

---

## Pipeline Overview

Every B2B local outreach project follows this pipeline:

```
0. CHECK LAW     → Can you cold-email businesses in this country? (§6 gate) — if not, change channel
1. SOURCE        → Find businesses (Google Maps, directories, LinkedIn)
2. DISCOVER      → Find real contact email (legal pages, website, LinkedIn)
3. STORE         → Upsert into lead DB (SQLite / Supabase) — dedup by domain
4. ENRICH        → Capture intent signals (ads, job openings, activity, tech audit)
5. QUALIFY       → Score with weighted formula (intent + fit + maturity + revenue)
6. AUDIT         → Audit their website/social for observable problems to reference
7. PERSONALIZE   → Craft message using specific, verifiable detail from their business
8. SEQUENCE      → Send 3-email sequence + contact form fallback (only where §6 allows)
9. COMPLY        → Follow local law (LSSI, UWG, PECR, CAN-SPAM, CASL…)
10. TRACK        → Log replies, classify intent, adjust scoring
```

Step 0 runs first, before any scraping or copywriting. Spain, Germany and Italy do not allow cold email to
businesses without prior consent (§6): for leads there, the email and contact-form steps are skipped.

---

## 1. Lead Sources

### Google Maps
The most reliable source for local businesses worldwide.

**Manual approach:**
- Search: `[business type] in [city]`
- Export to CSV using tools like: Outscraper, PhantomBuster Google Maps Extractor, or Apify Google Maps Scraper
- Fields to capture: name, address, phone, website URL, rating, review count, category

**Google Places API (programmatic):**
```javascript
// Search businesses by type and location
GET https://maps.googleapis.com/maps/api/place/textsearch/json
  ?query=auto+repair+shop+Austin+TX
  &key=YOUR_API_KEY

// Get details for a specific place
GET https://maps.googleapis.com/maps/api/place/details/json
  ?place_id=PLACE_ID
  &fields=name,formatted_address,website,formatted_phone_number,rating,user_ratings_total
  &key=YOUR_API_KEY
```

**Key fields from Google Maps:**
| Field | Use |
|-------|-----|
| `website` | Entry point for email discovery |
| `rating` | Lead qualification signal |
| `user_ratings_total` | Business size/activity signal |
| `formatted_phone_number` | Fallback contact + country detection |
| `business_status` | Filter out closed businesses |

### Business Directories by Region
| Region | Directory |
|--------|-----------|
| Germany | gelbe-seiten.de, branchenbuch.de |
| Spain | paginasamarillas.es, yelp.es |
| France | pagesjaunes.fr, societe.com |
| Italy | paginegialle.it, kompass.com |
| UK | yell.com, checkatrade.com |
| US | yelp.com, yellowpages.com, thumbtack.com |
| Global | foursquare.com, tripadvisor.com (hospitality/F&B) |

### LinkedIn
Best for finding the decision maker's name and title before writing.

**Search pattern:**
- Search: `[Job Title] at [Company Name]` or `Owner [City] [Industry]`
- Common B2B local decision maker titles: Owner, Manager, Director, Founder, Geschäftsführer (DE), Gérant (FR), Propietario (ES)
- Use LinkedIn to confirm the decision maker's name even if you find email elsewhere

---

## 2. Email Discovery

### Strategy: Legal Pages First

Business legal/compliance pages are the best source of real contact emails because they are:
- **Required by law** in most countries — the business owner must put accurate contact info
- **Direct to the decision maker** — not a generic info@ address
- **Public by design** — no scraping restrictions apply to publicly required disclosures

### URL Patterns by Country

Try these paths in order. Append to the base domain:

**Germany — Impressum (legally required)**
```
/impressum
/impressum.html
/impressum/
/imprint
/imprint.html
/about/impressum
/de/impressum
```

**Spain — Aviso Legal**
```
/aviso-legal
/aviso_legal
/aviso-legal/
/legal
/legal.html
/politica-privacidad
/terminos-condiciones
```

**France — Mentions Légales**
```
/mentions-legales
/mentions_legales
/mentions-legales.html
/mentions-legales/
/cgv
/cgu
/legal
```

**Italy — Note Legali**
```
/note-legali
/note_legali
/privacy
/chi-siamo
/contatti
```

**UK & US — Privacy Policy / Contact**
```
/privacy-policy
/privacy
/contact
/about
/contact-us
/about-us
/terms
/legal
```

**Netherlands**
```
/disclaimer
/privacyverklaring
/over-ons
```

**Portugal / Brazil**
```
/aviso-legal
/politica-de-privacidade
/termos-de-uso
/contato
```

### Email Extraction

After fetching the page HTML, extract emails with this pattern:

```python
import re
import requests
from bs4 import BeautifulSoup

def find_emails_on_page(url):
    try:
        response = requests.get(url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (compatible; business-contact-finder/1.0)'
        })
        text = response.text

        # Extract all email-like strings
        raw_emails = re.findall(
            r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}',
            text
        )

        # Filter out false positives
        excluded_domains = ['example.com', 'domain.com', 'email.com',
                           'wixpress.com', 'sentry.io', 'cloudflare.com',
                           'googleapis.com', 'schema.org']
        excluded_patterns = ['noreply', 'no-reply', 'donotreply',
                            'webmaster', 'admin@wordpress']

        clean_emails = []
        for email in set(raw_emails):
            domain = email.split('@')[1].lower()
            local = email.split('@')[0].lower()

            if any(excl in domain for excl in excluded_domains):
                continue
            if any(pat in local for pat in excluded_patterns):
                continue
            if len(local) < 2:
                continue

            clean_emails.append(email.lower())

        return clean_emails
    except Exception as e:
        return []

def discover_contact_email(base_url, country_code='US'):
    """Try legal pages first, then fallback to contact/about"""

    patterns_by_country = {
        'DE': ['/impressum', '/impressum.html', '/imprint', '/about/impressum'],
        'ES': ['/aviso-legal', '/aviso_legal', '/legal', '/politica-privacidad'],
        'FR': ['/mentions-legales', '/mentions_legales', '/cgv', '/legal'],
        'IT': ['/note-legali', '/privacy', '/contatti'],
        'UK': ['/privacy-policy', '/contact', '/about'],
        'US': ['/contact', '/about', '/privacy-policy', '/contact-us'],
        'NL': ['/disclaimer', '/privacyverklaring', '/over-ons'],
    }

    fallback_paths = ['/contact', '/about', '/privacy-policy', '/terms', '/legal']
    paths = patterns_by_country.get(country_code.upper(), fallback_paths)

    # Also try root domain (footer emails)
    paths = [''] + paths + fallback_paths

    all_emails = []
    for path in paths:
        url = base_url.rstrip('/') + path
        emails = find_emails_on_page(url)
        all_emails.extend(emails)
        if emails:
            break  # Stop at first page with results

    return list(set(all_emails))
```

**Node.js version:**
```javascript
const axios = require('axios');

async function discoverEmail(baseUrl, countryCode = 'US') {
    const patterns = {
        DE: ['/impressum', '/impressum.html', '/imprint'],
        ES: ['/aviso-legal', '/aviso_legal', '/legal'],
        FR: ['/mentions-legales', '/mentions_legales', '/legal'],
        IT: ['/note-legali', '/privacy', '/contatti'],
        UK: ['/privacy-policy', '/contact', '/about'],
        US: ['/contact', '/about', '/privacy-policy'],
    };

    const emailRegex = /[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}/g;
    const excludedDomains = ['example.com', 'sentry.io', 'cloudflare.com', 'googleapis.com'];

    const paths = ['', ...(patterns[countryCode] || patterns['US']), '/contact', '/about'];

    for (const path of paths) {
        try {
            const { data } = await axios.get(baseUrl.replace(/\/$/, '') + path, {
                timeout: 8000,
                headers: { 'User-Agent': 'Mozilla/5.0' }
            });

            const found = [...data.matchAll(emailRegex)]
                .map(m => m[0].toLowerCase())
                .filter(e => !excludedDomains.some(d => e.includes(d)))
                .filter(e => !e.includes('noreply') && !e.includes('no-reply'));

            if (found.length > 0) return [...new Set(found)];
        } catch (e) { continue; }
    }

    return [];
}
```

### Email Prioritization

When multiple emails are found on a page, rank them:

1. **Highest priority:** Email matching owner/manager name (`stefan.muller@...`, `jean.dupont@...`)
2. **High:** Generic business email (`info@domainname.com`, `hola@domainname.com`)
3. **Medium:** Department email (`contact@...`, `hello@...`)
4. **Low/skip:** Generic platforms (`gmail.com`, `hotmail.com`, `yahoo.com`) — often personal, lower deliverability for B2B

---

## 3. Lead Database

Store leads in a persistent database instead of CSV. This eliminates duplicates across campaigns, enables incremental scoring, and builds a proprietary dataset that improves over time.

### SQLite (local) or Supabase (hosted)

Use SQLite for local-only pipelines. Use Supabase for multi-device or team access — same schema, just swap the connection string.

**schema.sql** (also available in `db/schema.sql`):

```sql
CREATE TABLE IF NOT EXISTS companies (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    domain        TEXT UNIQUE NOT NULL,
    name          TEXT NOT NULL,
    category      TEXT,
    address       TEXT,
    city          TEXT,
    country       TEXT,
    phone         TEXT,
    google_rating REAL,
    review_count  INTEGER,
    last_review_date TEXT,
    has_website   INTEGER DEFAULT 1,
    website_quality TEXT,       -- basic | medium | professional
    ssl           INTEGER,      -- 0 | 1
    mobile_friendly INTEGER,    -- 0 | 1
    meta_ads_active INTEGER,    -- 0 | 1 (checked via Meta Ads Library)
    job_openings  INTEGER,      -- 0 | 1 (signal of growth)
    last_google_activity TEXT,  -- date of last review / post
    linkedin_url  TEXT,
    created_at    TEXT DEFAULT (datetime('now')),
    updated_at    TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS leads (
    id                   INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id           INTEGER REFERENCES companies(id),
    email                TEXT NOT NULL,
    email_source         TEXT,  -- impressum | contact_page | footer | manual
    decision_maker_name  TEXT,
    decision_maker_title TEXT,
    score                INTEGER DEFAULT 0,
    status               TEXT DEFAULT 'new',
    personalization_note TEXT,
    created_at           TEXT DEFAULT (datetime('now')),
    UNIQUE(company_id, email)
);

CREATE TABLE IF NOT EXISTS outreach_log (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    lead_id      INTEGER REFERENCES leads(id),
    sent_at      TEXT DEFAULT (datetime('now')),
    sequence_step INTEGER,       -- 1 | 2 | 3
    channel      TEXT DEFAULT 'email',  -- email | contact_form
    subject      TEXT,
    body_preview TEXT
);

CREATE TABLE IF NOT EXISTS replies (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    lead_id      INTEGER REFERENCES leads(id),
    received_at  TEXT DEFAULT (datetime('now')),
    intent       TEXT,   -- interested | not_now | no | unsubscribe
    raw_text     TEXT,
    notes        TEXT
);

-- Status values: new → contacted → replied → meeting → won → lost → unsubscribed
-- Indexes for common queries
CREATE INDEX IF NOT EXISTS idx_leads_status ON leads(status);
CREATE INDEX IF NOT EXISTS idx_leads_score ON leads(score DESC);
CREATE INDEX IF NOT EXISTS idx_companies_domain ON companies(domain);
```

### Dedup by domain

Always upsert by `domain` — never create two records for the same website.

```python
from urllib.parse import urlparse

def extract_domain(url):
    try:
        parsed = urlparse(url if url.startswith('http') else f'https://{url}')
        return parsed.netloc.replace('www.', '').lower()
    except:
        return None

def upsert_company(conn, data):
    domain = extract_domain(data['website'])
    if not domain:
        return None
    conn.execute("""
        INSERT INTO companies (domain, name, category, city, country,
            google_rating, review_count, last_review_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(domain) DO UPDATE SET
            name=excluded.name,
            google_rating=excluded.google_rating,
            review_count=excluded.review_count,
            last_review_date=excluded.last_review_date,
            updated_at=datetime('now')
    """, (domain, data['name'], data.get('category'), data.get('city'),
          data.get('country'), data.get('rating'), data.get('reviews'),
          data.get('last_review_date')))
    conn.commit()
    return conn.execute("SELECT id FROM companies WHERE domain=?", (domain,)).fetchone()[0]

def upsert_lead(conn, company_id, email, source, decision_maker=None, score=0):
    conn.execute("""
        INSERT INTO leads (company_id, email, email_source, decision_maker_name, score)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(company_id, email) DO UPDATE SET
            email_source=excluded.email_source,
            decision_maker_name=COALESCE(excluded.decision_maker_name, decision_maker_name),
            score=excluded.score
    """, (company_id, email.lower(), source, decision_maker, score))
    conn.commit()
```

### Key queries

```sql
-- Leads ready to contact, not yet touched
SELECT l.*, c.name, c.city, c.domain
FROM leads l JOIN companies c ON l.company_id = c.id
WHERE l.status = 'new' AND l.score >= 70
ORDER BY l.score DESC;

-- Replies to classify today
SELECT l.email, c.name, r.raw_text, r.received_at
FROM replies r JOIN leads l ON r.lead_id = l.id
JOIN companies c ON l.company_id = c.id
WHERE r.intent IS NULL
ORDER BY r.received_at DESC;

-- Campaign performance snapshot
SELECT status, COUNT(*) as n, AVG(score) as avg_score
FROM leads GROUP BY status;

-- Re-engagement candidates (no reply, 90+ days ago)
SELECT l.*, c.name, c.domain
FROM leads l JOIN companies c ON l.company_id = c.id
JOIN outreach_log o ON o.lead_id = l.id
WHERE l.status = 'no_response'
AND o.sent_at < datetime('now', '-90 days')
AND o.sequence_step = 3;
```

---

## 4. Lead Qualification & Scoring

### Scoring Model v2 — Weighted Formula (0–100)

The v1 score was proxy-based (reviews = size). v2 scores on **intent** — signals that the business is likely to buy now.

```
Score = (revenue_proxy * 0.30) + (digital_maturity * 0.20) + (intent_signals * 0.30) + (icp_fit * 0.20)
```

Each component is scored 0–100 and then weighted.

---

**Revenue Proxy (0–100)** — estimates business size/activity

| Signal | Points |
|--------|--------|
| Review count 200+ | 100 |
| Review count 100–199 | 75 |
| Review count 50–99 | 50 |
| Review count 20–49 | 25 |
| Review count < 20 | 0 |
| Bonus: Google Rating ≥ 4.5 | +15 (capped at 100) |

---

**Digital Maturity (0–100)** — how digitally active they are (observable without login)

| Signal | Points |
|--------|--------|
| Own domain email (not gmail/hotmail) | 30 |
| SSL certificate (https://) | 20 |
| Mobile-friendly website | 20 |
| Professional CMS (not Wix/free builder) | 15 |
| Online booking or e-commerce present | 15 |

Check SSL: `curl -sI https://domain.com | head -1`
Check mobile: Google Mobile-Friendly Test (free, public URL)
Detect Wix/Squarespace: `view-source:` and look for `wixsite.com`, `squarespace.com` in scripts

---

**Intent Signals (0–100)** — signs they're actively investing in growth right now

| Signal | Points | How to check |
|--------|--------|--------------|
| Active Meta ads (last 30 days) | 40 | facebook.com/ads/library → search by business name |
| Job openings posted | 25 | LinkedIn Jobs or Google "site:linkedin.com/jobs [company name]" |
| Google Business post < 30 days | 20 | Visible in Google Maps sidebar |
| Recent Google review < 14 days | 15 | Check review dates in Maps |

Meta Ads Library is public, no login required: `https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ALL&q=BUSINESS_NAME`

---

**ICP Fit (0–100)** — how well they match your ideal customer profile (customize per campaign)

| Signal | Points |
|--------|--------|
| Decision maker name found (LinkedIn/Impressum) | 35 |
| LinkedIn company presence | 25 |
| Vertical matches campaign target exactly | 25 |
| City/district matches target area | 15 |

---

**Score thresholds:**
- **70–100:** Priority A — audit their site, personalize manually, send first
- **40–69:** Priority B — semi-personalized, batch send
- **0–39:** Priority C — skip or save for future re-engagement

**Scoring function:**

```python
def calculate_score(lead):
    revenue = min(100, (
        (100 if lead['reviews'] >= 200 else
         75 if lead['reviews'] >= 100 else
         50 if lead['reviews'] >= 50 else
         25 if lead['reviews'] >= 20 else 0) +
        (15 if lead.get('rating', 0) >= 4.5 else 0)
    ))
    maturity = (
        (30 if lead.get('domain_email') else 0) +
        (20 if lead.get('ssl') else 0) +
        (20 if lead.get('mobile_friendly') else 0) +
        (15 if lead.get('professional_cms') else 0) +
        (15 if lead.get('has_booking') else 0)
    )
    intent = (
        (40 if lead.get('meta_ads_active') else 0) +
        (25 if lead.get('job_openings') else 0) +
        (20 if lead.get('google_post_recent') else 0) +
        (15 if lead.get('recent_review') else 0)
    )
    icp = (
        (35 if lead.get('decision_maker_name') else 0) +
        (25 if lead.get('linkedin_url') else 0) +
        (25 if lead.get('vertical_match') else 0) +
        (15 if lead.get('city_match') else 0)
    )
    return round(revenue * 0.30 + maturity * 0.20 + intent * 0.30 + icp * 0.20)
```

### Disqualification Signals
- `business_status: CLOSED_PERMANENTLY`
- Rating < 3.0 (struggling business, low budget)
- No website (hard to reach, likely very small)
- Last Google review > 12 months ago (inactive)
- Review count < 5 (too new or very small)

### Vertical-Specific Qualification

**Hotels / Hospitality:**
- Priority: 3+ stars, own domain email, 100+ reviews
- Skip: hostels with shared dorms only (low margin), Airbnb-only operators
- Best signals: conference facilities mention, corporate rates page, fleet/transport mention

**Auto Workshops:**
- Priority: Has fleet service, mentions "empresas" / "fleets" / "Flottenkunden"
- Skip: single-person operations, no website
- Best signals: brand partnerships (authorized dealer), multiple bays visible in photos

**Restaurants / F&B:**
- Priority: Private dining / events section, catering mention, 200+ reviews
- Skip: Fast food franchises (decisions made centrally), food trucks
- Best signals: corporate lunch menu, group booking form

**Beauty & Wellness (salons, spas):**
- Priority: Multiple staff, online booking system, gift vouchers
- Skip: Home-based single operators
- Best signals: corporate wellness packages, multi-location

**Fitness (gyms, studios):**
- Priority: Corporate membership option, group classes, equipment brand partnerships
- Skip: Solo personal trainers working from parks
- Best signals: HR/corporate wellness page, B2B pricing visible

**Retail:**
- Priority: Multi-brand boutique, specialty store with own brand, online + physical
- Skip: Franchises with central purchasing, discount stores
- Best signals: local brand, own products, community engagement

---

## 5. Vertical Intelligence

For each vertical: decision maker, core pain, buying trigger, best angle, objections.

---

### Hospitality (Hotels, B&Bs, Aparthotels)

**Decision maker:** General Manager, Owner, Operations Manager
**Core pains:** Guest experience differentiation, upsell revenue, corporate client acquisition
**Buying triggers:** New season starting, refurbishment, TripAdvisor score drop, new competitor opened nearby
**Best angle:** Guest experience upgrade, new amenity, corporate package inclusion
**Objections:** "We already have a supplier", "Not in the budget", "Guests don't ask for this"
**Best contact time:** Tuesday–Thursday, 10am–12pm local time. Avoid peak season (summer for beach, winter for ski).

**Hook examples:**
- "Hotels in [city] that offer [product] as an amenity see a 12% increase in positive reviews mentioning activities"
- "Your guests arriving by [transport hub] often need [product] for their stay"

---

### Automotive (Workshops, Garages, Fleet Services)

**Decision maker:** Owner, Workshop Manager, Fleet Manager
**Core pains:** Technician downtime, parts margin, customer retention, fleet contracts
**Buying triggers:** Fleet tender season (Q4/Q1), new model year, regulation changes
**Best angle:** Efficiency gain, margin improvement, fleet client acquisition
**Objections:** "We have preferred suppliers", "Cash flow is tight", "Not relevant to our customers"
**Best contact time:** Monday–Wednesday, 8–10am (before workshop gets busy)

**Hook examples:**
- "Fleet managers at [type] companies in [city] are adding [product] to their driver packages"
- "We work with [X] workshops in [region] who resell [product] as an add-on service"

---

### Food & Beverage (Restaurants, Cafés, Catering)

**Decision maker:** Owner, Restaurant Manager, Events Manager
**Core pains:** Slow lunch covers, event differentiation, corporate catering contracts
**Buying triggers:** Summer terrace opening, private dining launch, new events menu
**Best angle:** Guest experience, event differentiation, corporate catering add-on
**Objections:** "Not core to what we do", "Our customers don't ask for this", "Too expensive"
**Best contact time:** Tuesday–Thursday, 2:30–4pm (post-lunch, pre-dinner prep)

---

### Beauty & Wellness (Salons, Spas, Barbershops)

**Decision maker:** Owner, Salon Manager
**Core pains:** Client retention, ticket average, corporate wellness contracts
**Buying triggers:** Valentine's Day, summer, bridal season, corporate wellness trends
**Best angle:** Gift voucher upsell, corporate package, experience differentiation
**Objections:** "Our clients don't come for that", "We have a full menu already"
**Best contact time:** Monday or Tuesday, 10am–12pm (quietest days for salons)

---

### Fitness (Gyms, Yoga Studios, CrossFit)

**Decision maker:** Owner, General Manager, Head of Corporate Sales
**Core pains:** Corporate membership sales, member retention, off-peak utilization
**Buying triggers:** January (New Year), September (back to routine), corporate wellness budget cycles (Q3)
**Best angle:** Corporate wellness partnership, member benefit add-on
**Objections:** "We already have enough members", "Our members are very specific"
**Best contact time:** Early morning (6–8am) or mid-morning (10–11am), Monday or Wednesday

---

### Retail (Boutiques, Specialty Shops)

**Decision maker:** Owner, Buyer, Store Manager
**Core pains:** Foot traffic, average basket, online competition
**Buying triggers:** New collection season, local events, store refurbishment
**Best angle:** Complementary product, bundle opportunity, local collaboration
**Objections:** "We're very curated", "Not our style", "We buy from specific brands only"
**Best contact time:** Tuesday–Thursday, 11am–1pm (post-opening, pre-lunch rush)

---

## 6. Legal Compliance by Country

This is non-negotiable, and it comes **before** writing any copy: in some countries you may not send a
cold email to a business at all, no matter how relevant it is or how easy the opt-out.

> Not legal advice. This section summarises the rules as of November 2026 so the skill stops before
> doing something unlawful. For a real campaign, check the current law or ask a lawyer in that country.

### Two different laws, and GDPR is not the one that decides

1. **Data protection (GDPR in the EU/UK).** Covers collecting and storing the contact data. Legitimate
   interest (Art. 6(1)(f)) can work here for business contacts.
2. **The e-marketing rule** (EU ePrivacy Directive Art. 13, implemented by each country: LSSI, UWG,
   CPCE, PECR, Codice privacy…). Decides whether you may **send** the unsolicited email at all.

Passing (1) does not get you through (2). For businesses, the ePrivacy Directive lets each member state
choose, so the answer changes country by country. That is why there is no single "EU rule".

### Country gate: can you cold-email a business without prior consent?

| Country | Law | Cold email to a business without consent? | Notes |
|---|---|---|---|
| 🇪🇸 Spain | LSSI-CE art. 21 | ❌ **No** | Commercial email that was not requested or expressly authorised is prohibited. No B2B exception: the only one is an existing customer relationship, for products similar to what they bought, with an easy opt-out (art. 21.2). Also covers "equivalent electronic means". |
| 🇩🇪 Germany | UWG §7(2) Nr. 2 | ❌ **No** | Email advertising needs **prior express consent**, also between businesses. The B2B relaxation (presumed consent) exists only for phone calls (§7(2) Nr. 1). Exception §7(3): existing customer, your own similar products, opt-out offered at collection and in every email. An Impressum address is not consent. |
| 🇮🇹 Italy | Codice privacy art. 130 | ❌ **Treat as no** | The Garante applies prior consent to legal persons too, and has ruled that an unsubscribe link does not make the send lawful. Some lawyers argue B2B should be opt-out; the regulator does not. |
| 🇫🇷 France | CPCE L.34-5 (CNIL guidance) | ✅ Yes, with conditions | Allowed when the subject relates to the recipient's profession (CNIL example: software pitched to an IT director). Identify yourself, offer an easy opt-out, and the person must have been told their address may be used for prospecting. |
| 🇬🇧 UK | PECR reg. 22–23 | ✅ To companies · ❌ to sole traders and some partnerships | Corporate subscribers (limited companies, LLPs) can be emailed with sender identity and an opt-out. Sole traders and non-LLP partnerships count as individuals: consent needed. UK GDPR still applies to named employees. |
| 🇺🇸 US | CAN-SPAM | ✅ Yes | No prior consent. Physical postal address, working opt-out honoured within 10 business days, no deceptive subject or headers. |
| 🇨🇦 Canada | CASL | ⚠️ Only with implied consent | Implied consent exists when the address is conspicuously published, there is no statement refusing unsolicited messages, and your message is relevant to the person's business role. Keep a record of where and when you found the address. |
| Anywhere else | — | ❓ Unknown → **stop** | Do not assume GDPR legitimate interest is enough. Check that country's ePrivacy / anti-spam law first. |

### What the skill must do with the gate

- **❌ or ❓ country:** do not write, schedule or send a cold email sequence. Tell the user why, cite the
  law from the table, and offer a channel that is not email: a postal letter, a visit, an event, a
  referral or a LinkedIn connection request. Check the national rules for phone and post too: they differ.
- **Contact forms are not a way around a ❌.** A sales pitch typed into a website form reaches the same
  inbox and falls under the same rule (Spain's art. 21 names "equivalent electronic means" explicitly).
- **Existing customers** (they bought from you before) are the exception in Spain and Germany: similar
  products only, opt-out in every message.
- **✅ country:** build the sequence and include everything below.

**Required in every email that does go out:**
```
To unsubscribe from further emails, reply with "unsubscribe" or click here: [link]
[Your company name] · [Address] · [Country]
```

### Country Compliance Checklist (generate per campaign)

```
[ ] Identified target country for every lead
[ ] Country passes the gate (✅ in the table) — ❌ or ❓ means no cold email, no contact form
[ ] Verified email is a business/professional address
[ ] Email is relevant to recipient's business activity
[ ] Unsubscribe link / instruction included
[ ] Physical sender address included
[ ] Subject line is accurate (not clickbait)
[ ] Suppression list checked before send
[ ] For the UK: recipient is a company or LLP, not a sole trader
[ ] For Canada: implied consent basis recorded (where and when the address was published)
```

Sources: [LSSI art. 21 (BOE)](https://www.boe.es/buscar/act.php?id=BOE-A-2002-13758#a21) ·
[UWG §7](https://www.gesetze-im-internet.de/uwg_2004/__7.html) ·
[CNIL: prospection par courrier électronique](https://www.cnil.fr/fr/la-prospection-commerciale-par-courrier-electronique)

---

## 7. Cultural Calibration for Outreach

The same message written for the US will fail in Germany. Adjust tone by market:

| Market | Tone | Length | Formality | Avoid |
|--------|------|--------|-----------|-------|
| USA | Direct, energetic, benefit-first | Short (3–5 sentences) | Semi-formal | Passive voice, excessive hedging |
| Germany | Precise, factual, respect for time | Medium (5–7 sentences) | Formal (Sie) | Hype, exaggeration, vague claims |
| France | Context-first, relationship-aware | Medium-long | Semi-formal (Vous) | Being too direct too fast |
| Spain | Warm, relationship-first | Medium | Semi-formal (usted for cold) | Being too cold or transactional |
| Italy | Personal, expressive | Medium | Formal first contact | Generic templates |
| UK | Polite understatement, indirect | Short-medium | Professional | Aggressive CTAs, pressure |
| Japan | Extremely formal, context-rich | Long | Very formal | Any directness at first contact |

### Formality by Language (Cold Email)

| Language | Formal address | Informal (follow-ups only) |
|----------|---------------|---------------------------|
| German | Sie / Sehr geehrte/r | Du (only if they switch first) |
| French | Vous / Madame, Monsieur | tu (never in cold) |
| Spanish | Usted | tú (follow-up if warm) |
| Italian | Lei | tu (follow-up if warm) |
| English | Hi [Name] | (already informal) |

---

## 8. Email Templates by Vertical + Language

### Template Structure (Universal)

```
Subject: [Specific hook referencing their business / city / situation]

Hi [First Name],

[Opening: one sentence that shows you know their business — the "observable signal"]

[Value proposition: what you offer and why it's relevant to them specifically — 2 sentences max]

[Social proof: one line — X businesses in [city/region] already use this]

[CTA: one clear, low-commitment ask]

[Opt-out line]
[Signature with company + address]
```

### Hospitality — English

**Email 1 (Cold):**
```
Subject: Bike rentals for [Hotel Name] guests — [City] season

Hi [Name],

I noticed [Hotel Name] is well-positioned near [specific area / landmark / bike route] —
a detail that more hotels in [City] are starting to capitalize on.

We supply bike fleets and e-bikes to hotels across [region] as a guest amenity —
typically included in the room rate or as a paid add-on. Setup takes a day,
no upfront investment required.

[Hotel/property nearby] started offering this last [season] and saw a 15%
increase in activity-related reviews on TripAdvisor.

Would a 10-minute call this week make sense to see if it fits what you're building?

To opt out of further emails, reply "unsubscribe".
[Name] · [Company] · [Address]
```

**Email 2 (Follow-up, Day 4–5):**
```
Subject: Re: Bike rentals for [Hotel Name] guests

Hi [Name],

Following up briefly — I know this may not be the right moment, but wanted to
share one thing: we offer a pilot program for [season] with no commitment
beyond the trial period.

Happy to share what that looks like if it's useful.

[Name]
```

**Email 3 (Breakup, Day 10–12):**
```
Subject: Closing the loop — [Hotel Name]

Hi [Name],

I'll stop following up after this — I know your inbox is busy.

If bike rentals or guest activity amenities ever become relevant for [Hotel Name],
feel free to reach out. We're at [email].

Wishing you a strong [upcoming season].

[Name]
```

---

### Hospitality — German (Hotels)

> Germany fails the §6 gate: use this only with prior consent or for existing customers. For Austria or
> Switzerland, check their law first.

**Email 1:**
```
Subject: Fahrradverleih für Ihre Hotelgäste – [Stadt]

Sehr geehrte/r [Nachname],

ich bin auf das [Hotel Name] aufmerksam geworden, da Ihr Haus in unmittelbarer
Nähe von [Sehenswürdigkeit / Radweg / Stadtzentrum] liegt.

Wir statten Hotels in [Region] mit Leihfahrrädern und E-Bikes aus –
als Gästeservice oder buchbares Zusatzangebot. Die Einrichtung erfolgt ohne
Vorabinvestition Ihrerseits.

Wäre ein kurzes Gespräch diese Woche für Sie sinnvoll?

Mit freundlichen Grüßen,
[Name] · [Unternehmen] · [Adresse]

Wenn Sie keine weiteren E-Mails erhalten möchten, antworten Sie bitte mit "Abmelden".
```

---

### Hospitality — French

**Email 1:**
```
Objet : Location de vélos pour les clients de [Nom de l'hôtel] – [Ville]

Bonjour [Prénom/Madame/Monsieur],

Je me permets de vous contacter car [Nom de l'hôtel] est idéalement situé
à proximité de [lieu / piste cyclable / centre-ville].

Nous équipons des hôtels en [région] avec des vélos et vélos électriques
en location – comme service inclus ou en option payante pour les clients.
La mise en place ne nécessite aucun investissement initial de votre part.

Seriez-vous disponible pour un bref échange cette semaine ?

Cordialement,
[Nom] · [Société] · [Adresse]

Pour ne plus recevoir d'e-mails de notre part, répondez "désabonnement".
```

---

### Hospitality — Spanish

> Spain fails the §6 gate: use this only with prior consent or for existing customers. For Spanish-speaking
> countries outside Spain, check their law first.

**Email 1:**
```
Asunto: Alquiler de bicicletas para los huéspedes de [Nombre del hotel] – [Ciudad]

Estimado/a [Nombre],

Me pongo en contacto porque [Nombre del hotel] está muy bien ubicado
cerca de [zona / carril bici / centro], algo que muchos hoteles de [Ciudad]
están aprovechando para diferenciarse.

Ofrecemos flotas de bicicletas y e-bikes para hoteles en [región] como servicio
para huéspedes — incluido en la tarifa o como extra. Sin inversión inicial por vuestra parte.

¿Tendría sentido una llamada breve esta semana?

Un saludo,
[Nombre] · [Empresa] · [Dirección]

Si no desea recibir más correos, responda "baja".
```

---

### Automotive — English

**Email 1:**
```
Subject: Fleet bikes for [Workshop Name] — staff and corporate clients

Hi [Name],

[Workshop Name] caught my attention — you appear to be one of the larger
independent workshops in [City], which typically means a mix of walk-in
and fleet/corporate clients.

We supply utility bikes and e-bikes to automotive businesses and fleet
managers across [region] — both as staff transport and as part of corporate
mobility packages they offer to their own clients.

Three workshops in [City] added this last year as a managed mobility service.
Happy to share how they structured it.

Worth a quick call?

[Name] · [Company] · [Address]
To unsubscribe: reply "unsubscribe"
```

---

### F&B — English

**Email 1:**
```
Subject: Guest activity add-on for [Restaurant Name] — [City]

Hi [Name],

I came across [Restaurant Name] while researching the best dining experiences
near [area / waterfront / city center] — clearly a spot that invests in the
full guest experience.

We work with restaurants and food venues that offer activity packages to
corporate groups and private dining clients — bike tours, scenic routes,
experience bundles. It typically lifts event booking value by 20–30%.

Would this kind of add-on be relevant to what you do with private events?

[Name] · [Company] · [Address]
Unsubscribe: reply "unsubscribe"
```

---

## 9. Personalization at Scale

### The Observable Signal Technique

Never open with "I was browsing your website and..." — it sounds like every other template.

Instead, use one specific, verifiable detail that proves you looked. For Priority A leads, go further: audit their business for visible problems and reference the problem directly in your opening.

---

### Business Audit Checklist (Priority A leads only)

Run this before writing the email. Takes 3–5 minutes per lead. Spend time here — it's what converts.

**Website — view-source or browser DevTools:**
- [ ] `<title>` tag: empty, generic ("Home"), or keyword-rich?
- [ ] `<meta name="description">`: missing = quick SEO win you can mention
- [ ] Single H1 on the page? Multiple H1s = problem to reference
- [ ] Contact form: fill it and submit. 404 or broken response?
- [ ] Primary CTA button: does it have an action, or is it dead?
- [ ] Mobile: count checkout/booking steps vs. industry standard

**SEO — visible without tools (view-source):**
- [ ] Title tag missing or duplicated across pages
- [ ] Meta description missing (shows generic text in Google results)
- [ ] No structured data (no `<script type="application/ld+json">`)
- [ ] Images with `alt=""` or no alt attribute

**Social activity — public profiles:**
- [ ] Last Instagram/Facebook post date (check their Google Business links)
- [ ] Last post > 3 months = social abandonment signal
- [ ] No social links at all on website

**Google Business:**
- [ ] Profile photo quality (blurry/old photos = they haven't updated)
- [ ] Business description present or empty
- [ ] Last owner reply to reviews (never replied = bad signal)
- [ ] Category accuracy (wrong category = missing search traffic)

**Pricing/positioning:**
- [ ] Is pricing visible on the website?
- [ ] Pricing hidden = transactional friction (can mention)
- [ ] No testimonials/social proof section

---

### Turning an audit into a personalized opener

**The formula:**
```
"[Business name] + [specific observable problem] + [cost of that problem to them]"
```

**Examples (strong):**
- "I noticed [Workshop Name]'s contact form returns a 404 on mobile — anyone trying to reach you from their phone is hitting a dead end."
- "[Hotel Name]'s Google Business description is empty — you're getting traffic from Maps but the listing isn't converting."
- "Vuestro formulario de reservas en [Restaurant Name] tiene 4 pasos en móvil — la media del sector está en 2."
- "[Salon Name]'s last Instagram post was 4 months ago — corporate wellness buyers check social before reaching out."
- "Your checkout page has no SSL indicator on Safari mobile — that yellow warning is killing conversions."

**Examples (weak — avoid):**
- "I came across your business and wanted to reach out."
- "I love what you're doing at [Business Name]."
- "I noticed you have great reviews on Google."

---

**Good observable signals (when no problem found):**
- Nearby landmark / street / neighbourhood visible on Google Maps
- Recent Google review mentioning something specific
- A page on their website (events page, corporate page, seasonal menu)
- Their rating vs. local average ("4.9★ with 340 reviews puts you in the top 3% of [category] in [city]")
- A badge or certification visible on their website

**Formula:**
```
"[Business name] + [specific observable detail] + [why that makes your offer relevant]"
```

### CSV-Based Personalization at Scale

```python
import csv

def generate_email(template, lead):
    """Fill template with lead data"""
    return template.format(
        first_name=lead['decision_maker_name'].split()[0] if lead['decision_maker_name'] else 'there',
        business_name=lead['business_name'],
        city=lead['city'],
        signal=lead['personalization_signal'],  # manually added for Priority A leads
        rating=lead['google_rating'],
        review_count=lead['review_count']
    )

# Add personalization_signal column to CSV for top leads
# Leave blank for Priority C leads — use generic version
```

### Anti-Template Checklist

Before sending, verify each email:
- [ ] First line mentions something specific about their business (not generic)
- [ ] Business name appears naturally in first 2 sentences
- [ ] City/location referenced at least once
- [ ] CTA is a question, not a command ("Would it make sense?" not "Book a call")
- [ ] Email is under 150 words (unless follow-up relationship warrants more)
- [ ] No hype words: "amazing", "revolutionary", "game-changing", "excited to share"
- [ ] Subject line is specific, not clever clickbait

---

## 10. Email Sequence Structure

### Timing

```
Day 0  → Email 1 (Cold introduction)
Day 4  → Email 2 (Different angle, shorter)
Day 10 → Email 3 (Breakup — closes the loop)
```

After Email 3: move to status `no_response`. Re-engage in 90 days with a new trigger (new product, new season, new local event).

### Email 2 — The "Different Angle" Rule

Email 2 should NOT repeat Email 1. Change the angle entirely:
- Email 1: Guest experience / revenue angle
- Email 2: Operational / ease of setup angle
- OR Email 2: Social proof / what competitors are doing

### Email 3 — Breakup Email

The breakup email often gets the highest reply rate because:
- It signals you will stop contacting them (relief)
- It leaves door open for future
- It's the most human of the three

Always end with: "If this ever becomes relevant, feel free to reach back out. No hard feelings either way."

---

## 11. Outreach Automation Stack

### n8n Pipeline (DB-backed)

```
[Trigger: Cron every morning / manual]
    ↓
[SQLite / Supabase: SELECT leads WHERE status='new' AND score>=40 ORDER BY score DESC]
    ↓
[For each lead:]
    ↓
[HTTP Request: POST to email provider API (Instantly / Brevo / Mailgun)]
    ↓
[SQLite: UPDATE leads SET status='contacted' WHERE id=lead_id]
[SQLite: INSERT INTO outreach_log (lead_id, sequence_step=1, channel='email')]
    ↓
[Wait 4 days (n8n Wait node)]
    ↓
[Check: SELECT status FROM leads WHERE id=lead_id → still 'contacted'?]
    ↓
[Send Email 2 → INSERT outreach_log sequence_step=2]
    ↓
[Wait 6 days]
    ↓
[Send Email 3 (breakup) → INSERT outreach_log sequence_step=3]
[UPDATE leads SET status='no_response']
```

**n8n + Supabase node:** Use the HTTP Request node with Supabase REST API to query/update rows. Supabase exposes a PostgREST endpoint at `https://[project-id].supabase.co/rest/v1/`.

**n8n + SQLite:** Use the Execute Command node to run a Python script that queries the local DB.

### Email Sending Tools

| Tool | Best for | Notes |
|------|----------|-------|
| Instantly.ai | High volume cold email | Built-in warm-up, sequences, analytics |
| Apollo.io | Prospecting + email | Also finds emails (paid) |
| Brevo (ex-Sendinblue) | EU-compliant sending | GDPR-friendly, good EU deliverability |
| Mailgun | API-based sending | For n8n/custom integrations |
| Hunter.io | Email discovery | Finds emails from domain |
| lemlist | Personalized sequences | Image/video personalization |

### Domain & Deliverability

Never use your main domain for cold outreach. Use a subdomain or separate domain:
```
Main:    yourcompany.com       ← protect this
Outreach: outreach.yourcompany.com OR yourcompany-sales.com
```

Warm up new domains for 3–4 weeks before sending at scale. Use tools like Mailreach or Instantly's built-in warm-up.

---

## 12. Contact Form Channel

Contact forms are an underused outreach channel. They bypass spam filters, reach whoever monitors the website, and have no deliverability issues. Use as a fallback when email isn't found, or as a parallel channel for Priority A leads.

**Same law as email.** Only use this channel in countries that pass the §6 gate. In Spain, Germany and Italy a sales pitch through a contact form needs the same prior consent as an email: it is not a workaround.

### Discovery

```python
CONTACT_FORM_PATHS = [
    '/contact', '/contacto', '/kontakt', '/contatti', '/contact-us',
    '/about', '/get-in-touch', '/reach-us', '/anfrage', '/demande'
]

def find_contact_form(base_url):
    """Return first URL that contains a <form> element"""
    import requests
    from bs4 import BeautifulSoup

    for path in CONTACT_FORM_PATHS:
        try:
            r = requests.get(base_url.rstrip('/') + path, timeout=8,
                             headers={'User-Agent': 'Mozilla/5.0'})
            if '<form' in r.text.lower():
                return base_url.rstrip('/') + path
        except:
            continue
    return None
```

### Message format for contact forms

Contact form messages must be shorter than emails — forms are read in a different context.

```
Subject (if field exists): Quick question about [specific thing on their site]

Hi [Name if known, otherwise skip],

[One-sentence observable signal about their business or a specific problem you spotted]

[One sentence on what you offer and why it's relevant to them]

[Low-friction CTA — not "book a call", more like "would it be worth 5 minutes?"]

[Name] · [Company] · [Email for reply]
```

### Logging

```python
# After submitting a contact form, log it in outreach_log
conn.execute("""
    INSERT INTO outreach_log (lead_id, sequence_step, channel, body_preview)
    VALUES (?, 1, 'contact_form', ?)
""", (lead_id, message_preview))
```

---

## 13. Reply Tracking & Classification

Tracking replies is what turns this into an improving system. Log every reply, classify intent with an LLM, and use the data to refine scoring and messaging.

### Classify replies with Claude

```python
import anthropic

def classify_reply(reply_text):
    client = anthropic.Anthropic()
    result = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=50,
        messages=[{
            "role": "user",
            "content": f"""Classify this cold email reply into exactly one of: interested | not_now | no | unsubscribe

Reply: {reply_text}

Respond with only the classification word."""
        }]
    )
    return result.content[0].text.strip().lower()
```

### Log and update on reply

```python
def handle_reply(conn, lead_id, raw_text):
    intent = classify_reply(raw_text)
    conn.execute("""
        INSERT INTO replies (lead_id, raw_text, intent)
        VALUES (?, ?, ?)
    """, (lead_id, raw_text, intent))
    status_map = {
        'interested': 'replied',
        'not_now': 'replied',
        'no': 'lost',
        'unsubscribe': 'unsubscribed'
    }
    conn.execute("UPDATE leads SET status=? WHERE id=?",
                 (status_map.get(intent, 'replied'), lead_id))
    conn.commit()
    return intent
```

### Daily review query

Run this every morning:

```sql
-- Leads that replied as "interested" — call them today
SELECT l.email, c.name, c.city, c.domain, r.raw_text
FROM replies r JOIN leads l ON r.lead_id = l.id
JOIN companies c ON l.company_id = c.id
WHERE r.intent = 'interested'
AND DATE(r.received_at) >= DATE('now', '-3 days')
ORDER BY r.received_at DESC;

-- Leads that said "not now" — re-engage in 60 days
SELECT l.*, c.name, r.received_at
FROM replies r JOIN leads l ON r.lead_id = l.id
JOIN companies c ON l.company_id = c.id
WHERE r.intent = 'not_now'
AND DATE(r.received_at) <= DATE('now', '-60 days');
```

### Learning loop

After 50+ replies, analyze patterns:

```sql
-- Which verticals reply most?
SELECT c.category, r.intent, COUNT(*) as n
FROM replies r JOIN leads l ON r.lead_id = l.id
JOIN companies c ON l.company_id = c.id
GROUP BY c.category, r.intent ORDER BY n DESC;

-- Does score correlate with replies?
SELECT
  CASE WHEN l.score >= 70 THEN 'A' WHEN l.score >= 40 THEN 'B' ELSE 'C' END as tier,
  COUNT(*) as total_leads,
  SUM(CASE WHEN l.status IN ('replied','meeting','won') THEN 1 ELSE 0 END) as replied
FROM leads l GROUP BY tier;
```

Use these results to adjust scoring weights and disqualification thresholds.

---

## 14. Campaign Checklist

Before launching any B2B outreach campaign:

```
DATABASE
[ ] schema.sql applied (SQLite or Supabase)
[ ] Leads imported via upsert_company / upsert_lead (no duplicates)
[ ] Unsubscribed leads from prior campaigns already in DB with status='unsubscribed'
[ ] Suppression check: WHERE status != 'unsubscribed'

ENRICHMENT & SCORING
[ ] Intent signals checked for all leads (Meta Ads Library, job openings, activity date)
[ ] All leads scored with v2 formula
[ ] Priority A leads (score ≥ 70): business audit completed, personalization_note filled
[ ] Disqualified leads removed (score < 20, closed businesses)

LEGAL
[ ] Country identified for each lead
[ ] Country passes the §6 gate — Spain, Germany, Italy and unknown countries: no cold email, no contact form
[ ] Compliance requirements met for that country
[ ] Opt-out mechanism tested and working
[ ] Physical sender address in email footer

COPY
[ ] Subject lines reviewed (specific, not clickbait)
[ ] Priority A: opener references specific audit finding or observable signal
[ ] Priority B: opener references city/vertical/rating
[ ] No hype words: "amazing", "revolutionary", "game-changing"
[ ] CTA is a question, not a command
[ ] Contact form URLs found for leads without email

TECHNICAL
[ ] Sending domain is NOT main domain
[ ] Domain warmed up if new (3–4 weeks minimum)
[ ] Sequence timing set correctly (Day 0 / 4 / 10)
[ ] Tracking enabled (opens, replies)
[ ] Reply inbox monitored — classify replies within 24h

LAUNCH
[ ] Test send to yourself first
[ ] Start with Priority A leads only (top 20%)
[ ] Review reply rate after first 50 sends before scaling
[ ] Log first replies in DB → check classification is correct
```

---

## Common Mistakes

**Treating GDPR legitimate interest as permission to send** — GDPR covers storing the contact data. Whether you may send the email is decided by each country's e-marketing law, and Spain, Germany and Italy say no without prior consent, B2B included (§6).

**Using main domain for cold outreach** — damages your deliverability permanently if spam complaints accumulate.

**Sending all 3 emails with same angle** — If Email 1 didn't work, repeating it twice more won't either. Change the angle.

**Generic opening line** — "I came across your business and wanted to reach out" is the most recognizable template opener. Everyone uses it. Start with the observable signal instead.

**Emailing info@ addresses only** — info@ goes to whoever is monitoring that inbox (often not the owner). If you find a direct email from Impressum/legal pages, use that.

**Ignoring review timing** — A business with 50 reviews all from 3 years ago is very different from one with 50 reviews in the last 6 months. Check recency, not just count.

**Translating English emails literally into other languages** — German emails translated from English sound unnatural. Write in the target language's native register from scratch.

**Skipping the lead DB and working from CSV** — You'll re-scrape the same leads, lose unsubscribe history, and have no visibility on performance. The DB is the foundation of everything else.

**Scoring only on review count** — Review count is a proxy for size, not intent. A 200-review business that's been quiet for 18 months is a worse lead than a 40-review business running Meta ads and hiring. Always weight intent signals.

**Generic audit opener** — "I noticed your website could be improved" is as generic as "I love your website." Reference the specific problem: the broken form URL, the empty H1, the 4-month-old last post. The more specific, the higher the reply rate.

**Not classifying replies** — If you send 200 emails and don't log what happened, you learn nothing. Even logging manually into the DB after 2 weeks gives you enough signal to improve your next campaign's targeting and messaging.
