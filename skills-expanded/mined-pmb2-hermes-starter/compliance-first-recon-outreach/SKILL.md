---
name: compliance-first-recon-outreach
description: Legal recon and compliance-first outreach protocol for small business security assessments. Covers Phase 1 (public OSINT only pre-contract), Phase 2 (authorized scanning under contract), and Phase 3 (full pentest). Includes messaging frameworks, the upsell pattern, and email templates.
version: 1.1.0
author: Phantom (Cyber Lead)
license: MIT
metadata:
  hermes:
    tags: [compliance, osint, legal-recon, outreach, security-consulting]
    triggers:
      - "legal recon"
      - "compliance framework"
      - "outreach to businesses"
      - "security assessment outreach"
      - "how to contact businesses about vulnerabilities"
      - "recon without breaking laws"
      - "public osint only"
      - "upsell pattern security"
      - "phase 1 phase 2 phase 3"
      - "contract of engagement"
      - "proximity scan"
      - "find businesses near me"
      - "osm business discovery"
      - "website-landlord"
      - "no website business"
      - "gatekeeper script"
      - "ai threat pitch"
      - "how to sell security"
      - "in person sales flow"
      - "overpass api"
      - "business vulnerability scan"
      - "current exposure"
      - "light passive scan"
      - "live exposure"
      - "verify endpoint"
      - "subdomain check"
      - "api key exposure"
      - "small business pricing"
      - "owner operated"
      - "poc package"
      - "pitch security"
    related_skills:
      - ai-security-practice-builder
      - local-biz-scanner-workflow
      - osint-recon
      - business-voice-outreach
---

# Compliance-First Recon & Outreach Protocol

**Purpose:** Define and enforce the legal boundary between pre-engagement public OSINT and post-engagement authorized testing. Every outreach uses only what's publicly visible — zero scanning, zero probing, zero unauthorized access.

---

## THE GOLDEN RULE

**Before a signed contract of engagement:** Passive public data only. Anything a normal person with a web browser could find on their own. No automated requests. No active probing. No attempted access to non-public pages.

**After a signed contract of engagement:** Full authorized testing within the scope defined in the contract.

---

## THE THREE PHASES

### Phase 1: Free Teaser (Pre-Contract — Public OSINT Only)

**Always legal data sources:**
- **Shodan.io** — publicly indexed ports/services. Shodan's crawlers already collected it; you're searching their DB.
- **crt.sh** — Certificate Transparency logs. Every SSL cert ever issued is public by design.
- **DNS records (MX, TXT, A, etc.)** — public by internet infrastructure design.
- **WHOIS** — ICANN-required public domain registration data.
- **HTTP headers (curl -I)** — what a normal browser reveals visiting the homepage. Server type, CMS signatures.
- **SSL cert inspection** — expiry date, issuer, subject. Visible in any browser.
- **Website public pages** — contact info, team pages, technology mentions. Normal browsing.
- **Login pages returning HTTP 200** — the server chose to respond to that URL. Observable.
- **Social media** — LinkedIn, Facebook, Instagram public profiles.
- **Google/Bing search results** — indexed content, cached pages, job postings.
- **Job postings** — reveal tech stack ("WordPress developer", "AWS admin").
- **State business registrations** — LLC filings, officers, addresses (public record).
- **Google Maps / Street View** — public imagery of physical locations.
- **News articles** — company mentions, leadership changes, reported incidents.
- **OpenStreetMap Nominatim + Overpass API** — free, no-key geocoding and business discovery. Overpass QL queries find businesses by tag (shop, amenity, office) within a radius. No ToS issues — this is the project's public API.
- **Public DNS Passive Checks** — nslookup for SPF/DMARC/DKIM (TXT records), MX records, A/AAAA resolution. Zero queries sent to the target's servers.
- **HTTP GET requests** to public URLs — the server chose to respond. Same as a browser loading the page.
- **Subdomain enumeration via common prefixes** — guessing standard subdomains (vpn., rdp., owa., admin., okta., mail., sftp., remote., etc.) and checking if they resolve via DNS + single HTTP GET. Zero intrusion.
- **Page source analysis** — viewing HTML/JS the server sends to every visitor. Extract API endpoints, exposed API keys, third-party integrations, embedded config data.
- **Google API key verification** — testing an exposed key against Google's free Geocoding API. The key was made public by being in page source. Testing it is a standard API call with a publicly-disclosed key.
- **Email discovery via public procurement records** — state and local government procurement databases (NYSDOT contracts, NYC Comptroller vendor lists, SAM.gov, state contract repositories) often include vendor email addresses in CSV/PDF exports. Search `[company name]` + `[state].gov` or check contract award listings. These are public records, not scraped data. Format confirmation via website contact pages or LinkedIn.

### CRITICAL: Current Exposures vs. Historical Breaches

When the user asks for a "vulnerability scan" or "what's exposed", they want **CURRENT, LIVE, VERIFIABLE exposures** — not historical breach data.

**Bad:** "Company X was breached in 2023."
**Good:** "vpn.company.com is live right now — Cisco VPN. files.company.com returns 200 — IIS 10, not updated since 2018. Their ordering portal has 2 Google API keys in page source. One is unrestricted and works."

**How to verify a current exposure:**
1. DNS resolution — check if the domain resolves to an IP
2. HTTP GET — send a standard browser-like request, check the response / status code
3. Header analysis — server info, version strings, security headers, internal node names
4. Cookie analysis — session patterns, auth requirements

**Label every finding with verification status:**
- LIVE [200] — Endpoint responds, data accessible
- LIVE [302/301] — Endpoint exists, redirects. Still recon value
- LIVE [403] — Endpoint exists but blocked. Valuable intel
- LIVE [401] — Auth required. Exists
- DOWN [err] — No response

### Phase 2: Basic Assessment (Contract Signed)

Once a **Contract of Engagement** is signed:
- Authorized port scanning (nmap, masscan)
- Authorized vulnerability scanning (Nuclei, OpenVAS)
- Authorized directory enumeration (gobuster, ffuf)
- Credential testing on their systems
- SSL/TLS deep inspection
- CMS fingerprinting and plugin enumeration
- Email configuration review
- Subdomain enumeration via active methods

**Scope is defined in the contract. Stick to what's written.**

### Phase 3: Full Pentest (Extended Engagement)

With a full penetration testing contract:
- Everything in Phase 2
- Web application pentest (OWASP Top 10)
- API security testing
- Authenticated testing (with credentials)
- Social engineering (defined scope)
- Internal network assessment
- Source code review

---

## THE GRAY ZONE — What NOT To Do Pre-Engagement

| Activity | Why Risky | Alternative |
|----------|-----------|-------------|
| **Active port scanning (nmap, masscan)** | Thousands of unsolicited packets. May be "unauthorized access" under CFAA. | Use Shodan — already indexed. |
| **Directory brute-forcing (gobuster, dirb, ffuf)** | Many requests guessing hidden pages. Likely exceeds authorized access. | Check Google dork results. Shodan HTTP data. |
| **Vulnerability scanning (Nuclei, OpenVAS, Nikto)** | Actively probes for CVEs. Attempts to trigger exploits. CFAA violation. | Don't do. Wait for signed contract. |
| **Login attempts / password guessing** | Attempted unauthorized access. Clear CFAA violation. | Show them the login page exists. Offer to test under contract. |
| **Exploitation of any kind** | Gaining access = felony. | Never. Full stop. |
| **Automated crawling/scraping** | robots.txt violations, ToS breaches. | Manual browsing only. Reference third-party data. |
| **Social engineering calls** | Impersonation = fraud. | Call as yourself with your real business offer. |

### The "Publicly Indexed" Safe Harbor

Safe: **"I found your domain on Shodan showing port 80 open with an IIS server."**
Shodan crawled and published it. You're reading their index.

Safe: **"Your SSL certificate expired in 2022. I checked with crt.sh."**
Certificate Transparency logs are public infrastructure.

Safe: **"Your website has a /wp-admin page that loads for anyone."**
Your browser made a normal HTTP request to a publicly accessible URL the server chose to respond to.

**NOT safe:** "I scanned your network with nmap to see what ports are open."
You sent unsolicited probes to their server.

---

## OUTREACH MESSAGING — The "Teaser to Upsell" Arc

### The Core Pattern (Use Every Call)

**Step 1 — Intro + Credibility:**
> "Hi [Name], I'm the operator. I'm local — operate out of your city. I do security research for small businesses in the area."

**Step 2 — Public Source Lead-In (THE KEY CHANGE):**
> "I was looking at publicly available data on [Shodan / crt.sh / public DNS] and noticed [specific finding anyone could see]."

**Step 3 — Explain the Risk in Plain English:**
> "This means [concrete business impact]. For example, [real-world scenario]."

**Step 4 — Offer the Free Walkthrough:**
> "I can show you how to fix that specific issue. Takes about 20 minutes, no cost, no obligation."

**Step 5 — The Upsell:**
> "If I could find this much from public information alone, just imagine what a full authorized assessment under contract would uncover. That's when I can show you the things that aren't visible from the outside."

### The Key Differentiator Line
> *"If I could find this just from information that's already public, imagine what a real attacker with more resources could do. And if you want the full picture — the things you can't see from the outside — a contract of engagement would let me show you everything."*

### Documentation Rule
For every Phase 1 finding, document the **public source**:
```
Finding: SSL cert expired Sept 2022
Source: crt.sh (public Certificate Transparency log)
URL: https://crt.sh/?q=example.com
Date: 2026-06-19
```
This protects you if anyone questions the source. You can always point to the public data and say "I found this the same way any customer would see it."

## TARGET PRE-QUALIFICATION

Before pitching a business, verify they don't already have a security provider blocking your sale.

### Three Quick Checks
1. **Website footer** — "Designed by" / "Hosted by" = web developer, not security. Usually fine.
2. **HTTP security headers** — Cloudflare/Akamai = basic awareness but rarely dedicated security.
3. **Web search** — "[business] [city] IT support OR managed services OR IT provider". Empty results = greenlight.

### The Greenlight
Most small businesses (under 20 employees) have NEVER had a security assessment and have NO dedicated IT vendor. You would be the first person to ever show them this information. That's the competitive advantage.

### If They Do Have IT
> "I'm not looking to replace your IT company. I do a specific type of security assessment that most IT providers don't offer — finding exposed API keys, missing email authentication, and website vulnerabilities. When was the last time your IT provider checked your website for API key leaks?"

## PITCH STRUCTURE

Every pitch follows four steps, in order:

1. **Provable fact** — show them on your phone (screenshot, working API call, live admin page)
2. **Plain-language threat** — what it means in money/trust/compliance terms
3. **Cost of the alternative** — a local number they recognize
4. **The ask** — your price + deliverable + timeline

### Local Numbers That Close

| Number | Context | Industry |
|--------|---------|----------|
| $175,000 | Beacon Stone & Co. HIPAA fine (Latham CPA firm) | Accounting/Professional |
| $500,000 | Albany ENT penalty (NY AG settlement) | Healthcare/Medical |
| $2.25M | Albany ENT total (penalty + mandated security spend) | Healthcare |
| $150,000 | Average BEC/wire fraud loss | Title/Real Estate/Legal |
| $550,000 | Average data breach class action settlement | All |

### One-Sentence Hooks by Industry

| Target | Hook |
|--------|------|
| Medical/Dental | "Your patient portal is HIPAA-covered. I found [X]. Fines start at $10K." |
| Accounting | "Your industry is #1 BEC target. Your website has [Y]." |
| Law Firm | "Client trust accounts are targeted daily. Your email is spoofable." |
| Title/Real Estate | "Title companies are #1 for wire fraud. Your admin panel is exposed." |
| Restaurant | "Your ordering portal has exposed API keys anyone can use on your account." |

### The Comparison Close

> "I'm asking $[price]. [Local firm] got fined $[amount] because they never did what I'm offering you. [Price] is cheaper than one fraudulent wire transfer, cheaper than a HIPAA violation, cheaper than the legal fees from a breach notification. You fix what I find, you never pay the fine."

## WALKING ROUTE STRATEGY

Multi-tenant buildings are force multipliers. One walk-through = 5-6 pitches in 30 minutes.

### Route Pattern
```
START → Building #1 (same lot — AAA Title, Ste 112)
   5 pitches in 30 min
  → Walk 0.1 mi to Building #2
   3 pitches
  → Walk 0.3 mi to medical complex
   2-3 pitches
  → Walk 0.5 mi to office park
   2-3 pitches
  → Trophy client (larger, more budget, follow-up)
  → Back to car (1.5 mi round trip, 2-3 hours)
```

### Building Priority
1. **Medical/dental office buildings** — HIPAA urgency, owner-operated, same-day yes
2. **Professional office buildings** — Lawyers, CPAs, title companies (fiduciary fear)
3. **Office parks** — Larger budgets but more gatekeepers
4. **Standalone retail** — Lower ticket, volume play

---

## EMAIL TEMPLATES

### Generic Template (Any Target)
```
Subject: Security finding on [company]'s website — public information

Hi [Name],

I'm a local security researcher operating out of your city. I was reviewing
publicly available data on local businesses and found something on [company]'s
website that I wanted to flag for you.

[Brief finding — 1-2 sentences. What I found, where I found it.]

Since this information is accessible to anyone who looks, I thought you should
know about it. I can walk through what I found and show you how to fix it —
no cost, no obligation. If after that you'd like a full authorized assessment
of your entire digital footprint, a contract of engagement would let me go much
deeper than what's visible from public data.

I'm local and can come by or do a quick call.

Best,
the operator
```

### Auto Dealer Template
```
Subject: Security finding on [domain] — public information

Hi [Name],

I'm a local security researcher operating out of your city. While doing a
routine check of publicly available data on local businesses, I noticed your
site has [finding]. Nothing I did required special access; [it was visible just
from public sources like Shodan / normal web browsing].

Since your dealership handles customer financing applications with financial
data, this is a significant exposure. [Specific risk in plain English.]

I can show you exactly what's exposed and how to lock it down — takes about
20 minutes, free, no obligation. If you'd then like a full authorized assessment
to find what's not visible from the outside, a contract of engagement would let
me go deeper.

I'm local — happy to stop by or hop on a call.

Best,
the operator
```

---

## HANDLING GATEKEEPERS (Receptionists, Employees, Phone Screens)

Every outreach goes through someone before reaching the decision-maker. Handle them right.

**General rule:** Be confident and specific. Don't ask permission — state the value.

### Four Gatekeeper Types

**Type 1: The Receptionist (Front desk, retail)**
> "Hey, I'm the operator. I found something on your company's website that [owner] needs to see. It's not a sales call — just a 2-minute heads-up."
*If they hesitate:* "You can stand right there while I show them — I'm not selling anything."

**Type 2: The Phone Screener (Calling in)**
> "This is the operator. I'm a local security researcher. I found a security issue with your website that I want to flag for [owner]. It's not a sales call — just a quick heads-up."
*If they offer to take a message:* "Just tell them the operator called about [specific finding — e.g., 'the expired SSL certificate']. That'll make sense to them."

**Type 3: Owner "Not Available"**
> "Totally understand. I'm in the area today and tomorrow. What's the best time to catch [owner]? Morning or after lunch?"
*Collects intel on when to return. Almost everyone answers.*

**Type 4: The Hostile/Defensive Gatekeeper**
> "Fair question. I found a security issue on your company's website. I'm trying to tell the owner before someone with worse intentions finds it. I'd rather be the guy who warned them than the guy who stayed silent."

### The In-Person Visit Flow

```
PARK → Walk in → Smile → Eye contact
  ↓
GREET → "Hey how's it going?" → Casual
  ↓
IDENTIFY → "Is [owner] around?" → Or "Who's the owner/manager?"
  ↓
PITCH → "I found something on your website..." → Curiosity gap
  ↓
SHOW → Pull out phone/laptop → Show the actual finding
  ↓
FIX → Offer to fix it right now for free → Build trust
  ↓
SELL → "That was the surface. Want me to check everything?"
  ↓
CLOSE → Contract signing → Schedule full assessment
```

### The AI Threat Close (After Showing The Finding)

> "If I could find this from public information alone, just imagine what a real attacker with more resources could do. And if you want the full picture — the things you can't see from the outside — a contract of engagement would let me show you everything."

---

## SMALL BUSINESS PRICING TIERS (Owner-Operator Targets)

When pitching locally-owned businesses (medical/dental practices, accounting firms, law firms, title companies, restaurants), use these tiers. The decision maker writes checks personally — no procurement.

| Tier | Price | What They Get | Decision Timeline |
|------|-------|---------------|-------------------|
| **Surface Scan (S)** | **$750** | Passive OSINT: exposed API keys, security headers, email security (SPF/DMARC), subdomain enumeration, leakage check. One-page report. | Same-day |
| **Standard Assessment (M)** | **$2,500** | Surface scan + POS integration review + employee phishing simulation + written report with remediation steps. | 1-2 days |
| **Annual Protection (A)** | **$1,500/yr** | Quarterly re-scan + dark web monitoring + incident response phone support. | 1 week |

### Why These Prices Work

- **$750** is "dinner out money" for a business owner — they can decide without thinking
- **$2,500** is "one client refund" — the cost of fixing one mistake
- **$1,500/yr** is "insurance premium" thinking — easy renewal
- Enterprise competitors (CrowdStrike, Rapid7) start at $50K+ — you win on accessibility
- Local MSPs don't do this kind of recon — you win on specificity

### Comparing to Enterprise Pricing

| Enterprise (Fortune 500) | Small Biz (Owner-Op) |
|-------------------------|----------------------|
| $7,500-$65,000 | $750-$2,500 |
| VPN/RDP/Okta/SSO exposure | API key/header/email exposure |
| Regulatory compliance (HIPAA, SEC) | "This code could cost you money" |
| Procurement, legal review | Owner decides same-day |
| 2-4 week engagement | 1-2 day engagement |

---

### Ticket Sizing by Vulnerability Finding

Map what you found to the price you quote. The vulnerability type determines the urgency, which determines what they'll pay:

| Finding | Urgency | Min Ticket | Example Pitch |
|---------|---------|-----------|---------------|
| **Exposed WP admin** (`/wp-admin` returns 200) | Critical — anyone can try to log in | $2,500 | "Your admin panel is publicly accessible. Anyone can try to guess your password right now." |
| **Google API key in page source** (verified working) | High — active financial exposure | $1,500 | "Your Google API key works. Anyone who views your page source can use it on your account." |
| **No SPF record** (email spoofable) | High — phishing/BEC risk | $1,500 | "Anyone can send emails from your domain. Your customers will think it's you." |
| **Missing HSTS + CSP + XFO** (no security headers) | Moderate — customer protection missing | $750 | "Your website has zero security headers. Customer sessions aren't protected." |
| **Server version disclosure** (nginx/Apache version in headers) | Moderate — reconnaissance target | $750 | "Your server tells attackers exactly what version you're running and what exploits to try." |
| **Dev/staging environment exposed** | High — weaker security, test data | $2,500 | "Your development environment is publicly accessible. These are frequently less secure than production." |
| **VPN/RDP/Okta gateway exposed** | Critical — direct network access | $3,500 | "Your [VPN/RDP/Okta] is internet-facing. This is how ransomware starts." |
| **No website, no domain** (walk-in only) | Low — can't prove digitally | $2,500 | "[Industry] firms with client data are targeted daily. Let me check what's exposed." |

**The rule:** If you found something critical (WP admin, VPN, API key), price HIGHER. If you only found missing headers or version disclosure, price LOWER. Don't pitch a $3,500 scan for a missing HTTP header. Don't pitch a $750 scan for an exposed VPN.

The vulnerability determines the urgency. The urgency determines the price. The price determines whether they say yes today or "let me think about it."

## POC PACKAGE STRUCTURE

When you need to demonstrate a vulnerability to win a client, structure the POC as:

### The 3-Part POC

**POC #1: Something They Can See (Visual)**
- An exposed API key in their page source
- A missing security header screenshot
- Their login page loading on your phone

**POC #2: Something You Can Prove (Working)**
- Verify the exposed key actually works (Google Geocoding API test)
- Show the nslookup returning no SPF record
- Show version disclosure in HTTP headers

**POC #3: Something They Should Fear (Impact)**
- "Anyone who finds this key can make API calls on your account"
- "Anyone can send emails appearing to be you — no SPF means no protection"
- "Customer sessions have no encryption enforcement — anyone on the same WiFi can intercept"

### The 5-Minute Demo Flow

```
1. Open their website/portal in browser
2. View page source, find the vulnerability
3. Copy the exposed key/data
4. Paste into a live API call that proves it works
5. Show the verified result (JSON with "status": "OK")
6. "This is what I found publicly. This is what you're paying for. $750 and I find the rest."
```

### POC Documentation Rules
- Screenshot every finding with timestamps
- Save the curl command that produced the result
- Note the verification method (curl, browser, nslookup, etc.)
- Include the raw response data

---

## PROXIMITY-BASED TARGET SELECTION

When working a geographic area, prioritize targets by decision-maker accessibility and compliance pressure, not by size.

### Decision Speed Tiers by Ownership Structure

How fast a target can say yes is determined by their ownership structure, not their industry:

| Structure | Decision Timeline | Example | Strategy |
|-----------|------------------|---------|----------|
| **Solo practitioner** | Same-day, on the spot | Single dentist, one-CPA shop, solo lawyer | Ask for the check. They are the owner. |
| **2-3 partner firm** | 1-3 days, one partner call | Small law firm, dental group, 2-partner CPA | Pitch the partner you reach. They'll call the other. |
| **5+ partner firm** | 1-2 weeks, partnership meeting | Multi-physician practice, mid-size law firm | Send email first, follow up. Needs board/partner vote. |
| **LLC with managing member** | Same-day (if managing member present) | Title agency, real estate brokerage | Ask for the managing member specifically. |
| **Corporate/branch** | Procurement, legal review — weeks | National chain, public company | Skip. Not worth the time for small ticket. |

Pitch the solo practitioners and 2-3 partner firms first. You get a same-day yes or a 3-day follow-up. Everything else is secondary.

### Tier 1: Owner-Operated Professional Services (Fastest Yes)

These are businesses where the person you pitch IS the check writer:
- **Medical/Dental practices** (HIPAA = regulatory urgency, owner = doctor deciding same-day)
- **Accounting firms** (handle money, BEC fear, partner-owned)
- **Law firms** (client confidentiality, trust accounts, partner-owned)
- **Title/Real Estate companies** (wire fraud = their biggest fear, owner-operated)
- **Small CPA firms** (solo practitioner = instant decision)

**Pitch angle for each:**

| Type | Hook | Price |
|------|------|-------|
| Medical/Dental | "HIPAA requires you to protect patient data. I found [X] in 5 minutes." | $2,500-$3,500 |
| Accounting | "Your industry is #1 for wire fraud. Your client portal has [Y]." | $2,500-$3,500 |
| Law | "Client trust accounts are targeted daily. Your email is spoofable." | $2,500-$3,500 |
| Title | "Title companies are the #1 BEC target. Let me show you what's visible." | $2,500-$5,000 |

### Special Category: Fiduciary Duty Targets (Highest Ticket, Fastest Compliance Fear)

Law firms, financial advisors, CPAs, title companies, and real estate professionals have **fiduciary obligations** that create urgency no other target type has:

| Target | Fiduciary Duty | The Specific Fear | Est. Ticket |
|--------|---------------|-------------------|-------------|
| **Real estate law firm** | Client trust/IOLTA accounts, wire transfers | "Your client's down payment gets stolen through a BEC email" | $3,500-$5,000 |
| **Elder law / trust firm** | Trust administration, fiduciary duty to beneficiaries | "Grandma's trust gets drained because someone spoofed your email" | $3,500-$5,000 |
| **Banking/financial law** | Client funds, regulatory compliance | "Banking regulators find you exposed client data" | $3,500-$5,000 |
| **Independent financial advisor** | Fiduciary standard (SEC/RIA), client investment assets | "Client investment accounts accessed through compromised email" | $3,500-$5,000 |
| **CPA firm** | Tax returns (SSNs), client financial data, IRS compliance | "SSNs of every client you've ever served get leaked" | $2,500-$3,500 |
| **Title company** | Closing funds, wire transfers | "Buyer loses $150K down payment to wire fraud" | $2,500-$5,000 |

**Why they buy faster than medical/dental:** Medical practices face HIPAA fines, but lawyers and financial advisors face **personal liability, disbarment, and professional ruin.** A solo lawyer who loses client trust funds doesn't get fined — they lose their license to practice. That urgency closes deals.

**The fiduciary pitch opener:**
> *"You have a [fiduciary duty / ethical obligation] to protect your clients' assets. I found [specific exposure] on your systems. If this was found by someone with malicious intent instead of me, [specific harm] would happen — and you'd be personally liable."*

### No-Digital-Presence Law Firms & Fiduciaries

Some law firms and financial advisors intentionally maintain NO public website. They rely on referrals and reputation. These are still viable targets — you just need a different approach.

**How to detect them:** State business registration filings, LinkedIn profiles, Bar association listings, directory listings (Yellow Pages, Justia, SuperLawyers).

**The walk-in pitch:**
> *"I couldn't find a website for your firm — which tells me you run on reputation and referrals. But your email is still the primary way clients send you sensitive information and funds. I checked your domain and found [no SPF / no DMARC / exposed mail server]. For a firm handling client trust accounts, that's a real risk. $2,500 and I'll map your entire digital footprint."*

**PITFALL: Virtual/registered-agent entities.** Some LLCs (especially title agencies and investment vehicles) use a law firm's address as their registered agent. There is no standalone office, no signage, and no front door. The law firm hosting the entity IS the real target. Walk into their suite and say: *"I was looking for [entity name] and saw it's registered at this address — figured you'd be the ones to talk to."*

### Tier 2: Local Retail/Restaurants (Volume Play)

- Online ordering systems (Toast, Mealeo, Clover integrations)
- POS systems handling card data
- Exposed API keys in page source (Google Maps, Stripe, etc.)
- $750 quick scan entry point

### Tier 3: Corporates (Wait for Introductions)

- NYSUT, Plug Power, government — gatekeepers, procurement, legal
- Pay more ($35K-$65K) but take months to close
- Build relationships for later; don't lead with these

### Walking Route Strategy

```
START → Tier 1 building (5-6 businesses in one multi-tenant building)
         ↓
         Tier 1 building #2 (0.3 mi — another multi-tenant)
         ↓
         Tier 2 locations (0.5 mi — restaurants with online ordering)
         ↓
         BACK to car (1.5 mi round trip, 2-3 hours, $15K-$35K potential)
```

**Key rule:** multi-tenant buildings are gold. One walk-through = 5-6 pitches. Hit all suites in one building before moving to the next.

**PITFALL: Virtual entities and no-physical-storefront targets.** Some registered businesses use a law firm or accounting firm's address as their registered agent — there is no standalone office, no signage, and no front door to walk through. The entity exists in state filings only. 

**How to detect:** The business registry lists the law firm's suite number as the principal address. No website. No phone number from search. No Yelp/Google Maps listing.

**The pivot:** The law firm (or professional practice) hosting the entity IS the real target. Walk into their suite and pitch them directly. They're typically the ones making the business decisions for the entity anyway. "I was looking for [entity name] and saw it's registered at this address — figured you'd be the ones to talk to."

**Price mapping by target type:**

| Target Type | Price | Why |
|-------------|-------|-----|
| Retail/Restaurant (online ordering) | $750-$1,500 | Low data sensitivity, POC-driven, volume play |
| Solo professional (CPA, dentist, chiropractor) | $1,500-$2,500 | Owner decides same-day, compliance pressure |
| Partnership/group practice (dental group, law firm, medical) | $2,500-$5,000 | Multiple partners = higher liability consciousness |
| Trophy (already breached, under consent order) | $7,500-$17,500 | They KNOW they need help, have compliance budget |

Pre-scan methodology using OpenStreetMap to find businesses near a location, filter out chains, and run passive OSINT on each.

### Workflow

```
1. GEOCODE location → lat/lng via Nominatim (free, no key)
2. QUERY Overpass API for shop/amenity/office within radius
3. FILTER known chains from ~60-name blocklist
4. FILTER corporate redirect domains (stores.brand.com, etc.)
5. For each business with a domain: passive OSINT checks
   (DNS, HTTP/HTTPS, SSL cert, WP login, admin paths, DMARC)
6. For each business WITHOUT a domain: flag as website-landlord opportunity
7. Generate report: vulnerabilities + website opportunities + CSV export
```

### Running The Scanner

```bash
# Full scan with vuln checks (from land-agent repo)
python scripts/proximity_scan.py --location "your city, NY" --radius 5000 --niches "general" --export-csv

# Lightweight version (business discovery only)
python scripts/proximity_scan_osm.py
```

**Chain filtering:** ~60 chain names (Subway, Dunkin, McDonald's, CVS, T-Mobile, etc.) are auto-skipped. Corporate domains (tools.usps.com, stores.hannaford.com) also blocked.

**Outputs:** Text report, CSV export, website opportunities list with website-landlord build commands.

**Compliance:** OpenStreetMap APIs are public and permit automated querying. Domain checks are passive (Phase 1). No scanning, no ToS violations.

---

## WEBSITE-LANDLORD INTEGRATION (No-Website Businesses)

Businesses found without a domain become website-landlord candidates for auto-generated Hugo static sites.

### Targeting Rules

- **Good targets:** Independent retail, restaurants, auto shops, salons, medical practices, plumbers, electricians, contractors
- **Skip:** Schools, government, police, libraries, municipal buildings, churches, utility companies
- **Edge case:** Local bank branches — talk to manager about a local landing page

### Build Commands

Run from the website-landlord repo (`${USER_HOME}/Documents/github/website-landlord/`):
```
website-landlord build-site --niche "alcohol" --location "your city, NY" --business-name "Personal Wine Cellar"
```

---

## PITFALLS
2. **Don't use active scanning tools before a contract.** Use Shodan's existing index instead of running nmap.
3. **Document every finding's source.** If challenged, you need to show "here's the public URL I checked."
4. **Don't try to log in to anything.** Showing someone their login page exists = fine. Trying default creds = CFAA risk.
5. **Lead with the source, not the vulnerability.** "I found this on Shodan" sounds like research. "Your site is hackable" sounds like a threat.
6. **Always offer the free walkthrough before pitching the contract.** Build trust first.
7. **State-specific computer crime laws vary.** NY has Penal Law § 156.00. Know your state's law. The safest position: don't touch their systems at all pre-engagement.
8. **Screenshot your public sources.** If you ever need to prove you got data from Shodan/crt.sh/DNS, screenshots with timestamps are your best evidence.
9. **PITFALL (context interpretation):** When the client in the #cyber channel mentions getting a "discounted order" or "something similar to [previous client]" from a target, interpret this as a legitimate security assessment POC — not fraud or theft. In security consulting, "order" means a service engagement, and "similar to Manhattan" means replicating the same security assessment methodology. Clarify with a question before assuming the worst — the misunderstanding creates friction and wastes time.
10. **PITFALL: Pre-qualify targets before pitching.** Check if the target already has an IT vendor or MSP before walking in. Website footer references ("designed by", "hosted by") and HTTP security headers (Cloudflare, Akamai) indicate existing vendor relationships. Most small businesses have NONE — you're the first person to ever show them this information. Pre-qualification tells you if you're competing with an incumbent.
11. **PITFALL: Current live exposures vs. historical breach data.** These are two different deliverables. "What's exposed" means current, verifiable, active endpoints — VPN gateways returning 200, admin panels accessible RIGHT NOW, API keys that work today. Historical breaches support the narrative but do NOT answer "what is exposed now." Label every finding with verification status (LIVE [200], LIVE [302], DOWN [err]). Delivering breach history when they asked for live exposures means you redo the work.

## VERIFICATION CHECKLIST

- [ ] Every finding's source documented (Shodan / crt.sh / DNS / HTTP headers / browser)
- [ ] No active scanning performed
- [ ] No login attempts made
- [ ] No automated crawling/scraping
- [ ] All pitches lead with the public source
- [ ] Every pitch includes the upsell line
- [ ] Compliance Framework is accessible alongside outreach materials

---

## RELATED REFERENCES

For the full sales playbook (AI threat pitch, gatekeeper scripts, in-person flow, close techniques), see `ai-security-practice-builder` skill's `references/sales-playbook.md`.

For the complete passive scanning methodology (HTTP headers, subdomain enumeration, API key verification, SPF/DMARC, response classification), see `references/passive-scan-methodology.md` in this skill.

For the complete business setup, pipeline, and media PR strategy, see the `ai-security-practice-builder` umbrella skill.

## Trophy Target Outreach

For targets that already know they have a security problem (previously breached, under consent order, fined by regulators), see `references/trophy-target-outreach.md` for the decision-maker identification, email format discovery, multi-recipient strategy, follow-up cadence, and email template.

## Worked Example

For a complete worked example of a proximity sweep using this methodology (17 targets across 4 tiers, Latham NY corridor, including pre-qualification checks, live passive exposure verification, per-target pitch creation, and walking route strategy), see `references/latham-sweep-worked-example.md` in this skill.
