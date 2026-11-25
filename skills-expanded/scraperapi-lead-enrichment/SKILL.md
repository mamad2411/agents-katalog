---
name: scraperapi-lead-enrichment
description: >-
  Use this skill whenever the user wants to enrich a contact or company and build a profile. Trigger on: "enrich this lead", "find info about [person or company]", "build a contact card for X", "I have this LinkedIn URL, find more about them", "find the email for [person] at [company]", "research this contact", "I have an email, can you find more details". Accepts any seed input — a name, company name, LinkedIn URL, email address, domain, or any combination. Executes ScraperAPI calls directly to search Google and fetch web pages, then synthesizes all findings into a structured contact card covering person fields (name, title, email, phone, LinkedIn, location, social) and company fields (domain, revenue, funding, employee count, founded year, HQ, tech stack, key investors, recent news, competitors).

  Note: Transmits user-supplied queries, URLs, and content to ScraperAPI.
metadata:
  openclaw:
    requires:
      env:
        - SCRAPERAPI_API_KEY
    emoji: "🧲"
    homepage: https://docs.scraperapi.com/
---

# Lead Enrichment

Given any seed information about a person or company, call ScraperAPI directly to search the web and fetch relevant pages, then synthesize everything into a structured contact card.

**You — Claude — execute the API calls** using the ScraperAPI MCP tools. Do not generate code for the user; run the searches yourself and report findings as you go.

---

## Phase 1 — Analyze the Seed

Before running any searches, state clearly what you already know and what you're looking for. Categorize the seed:

| Seed type | Information gaps to fill |
|-----------|--------------------------|
| Person name (+ optional company) | Title, email, phone, location, company details |
| Company name | Website, description, size, funding, contact info |
| Profile URL (LinkedIn, Crunchbase, etc.) | Fetch directly; then fill remaining gaps |
| Email address | Owner name, company, company details |
| Domain / website | Company info, key contacts, funding |

Announce before searching: *"Starting with: [what I have]. Will search for: [what's missing]."*

---

## Phase 2 — Discovery Searches

Run searches by *what you're looking for*, not by which site to target. Google will surface whatever sources exist — company website, Crunchbase, Wikipedia, news, directories, LinkedIn, G2, etc. Collect all promising URLs from `organic_results[].link` and carry them into Phase 3.

**Search tool:** Call `mcp__ScraperAPI__google_search` with `query`, `num: 10`, and `countryCode: "us"`. Read snippets carefully — they often contain the data you need without an extra fetch.

### 2a. Person name as seed

1. **Profile and context**
   Query: `"PERSON_NAME"+"COMPANY_NAME"`
   Surfaces: personal website, bios, speaker profiles, press mentions, social profiles, company team pages.

2. **Contact info**
   Query: `"PERSON_NAME"+"COMPANY_NAME"+contact+email`
   Surfaces: email addresses, contact pages, directory listings.

Then run 2b with the company name.

### 2b. Company name as seed (or company found in 2a)

1. **Company overview**
   Query: `"COMPANY_NAME"`
   Surfaces: official website, Wikipedia, Crunchbase, AngelList, G2, Glassdoor, LinkedIn — whatever exists publicly.

2. **Financials and size**
   Query: `"COMPANY_NAME"+funding+revenue+employees`
   Surfaces: Crunchbase, news articles, press releases, industry databases.

3. **Contact info**
   Query: `"COMPANY_NAME"+contact+email+phone`
   Surfaces: contact pages, email formats, phone directories.

4. **Recent news**
   Call `mcp__ScraperAPI__google_news` with `query: "COMPANY_NAME"` and `num: 5`.
   Extract `news_results[].title`, `news_results[].date`, `news_results[].link`. Keep the 3 most recent.

### 2c. Email address as seed

1. Extract the domain (everything after `@`).
2. Search for associated profiles: `"EMAIL_ADDRESS"`
3. Run 2b with the domain as the company seed.

### 2d. Direct URL as seed

Skip Phase 2 — go directly to Phase 3 with the provided URL.

---

## Phase 3 — Fetch Source Pages

From the URLs collected in Phase 2, select the most information-dense sources to fetch. Don't fetch everything — pick based on the gaps remaining in your contact card and the expected yield of each source.

### 3a. Source evaluation guide

| Source type | Typical yield | Fetch cost |
|-------------|--------------|------------|
| Company website (`/`, `/about`, `/contact`, `/team`) | Description, address, phone, email, social links, team members, tech signals | 1 credit/page |
| Crunchbase (`crunchbase.com/organization/...`) | Funding rounds, investors, employee range, founded year | ~10 credits (needs `render=true`) |
| Wikipedia (`en.wikipedia.org/wiki/...`) | Founded year, public financials, acquisitions, executive history | 1 credit |
| AngelList / Wellfound (`wellfound.com/company/...`) | Funding, investors, tech stack, open roles | ~10 credits (needs `render=true`) |
| LinkedIn person (`linkedin.com/in/...`) | Name, title, location, current company, education | ~10 credits (needs `render=true&premium=true`) |
| LinkedIn company (`linkedin.com/company/...`) | Employee count, industry, HQ, founded year | ~10 credits (needs `render=true&premium=true`) |
| News article / press release | Funding amounts, key hires, product launches | 1 credit |
| G2 / Capterra (`g2.com/products/...`) | Product category, company size range, competitors | 1 credit |
| GitHub org (`github.com/ORG`) | Tech stack, open source projects, activity | 1 credit |
| Job posting | Tech stack requirements, team growth signals | 1 credit |
| Glassdoor (`glassdoor.com/...`) | Employee count, HQ, culture signals | ~10 credits (needs `render=true`) |

Prefer cheap standard fetches (1 credit) over JS-rendered ones (10 credits) whenever the page is a static HTML site. Reserve `render=true` for pages that are known to require JavaScript (LinkedIn, Crunchbase, and SPA-style sites).

### 3b. Fetch pages

For each selected URL, call `mcp__ScraperAPI__scrape` with the appropriate options:

- **Standard HTML page** (news, Wikipedia, company sites, G2, GitHub): `url`, `outputFormat: "markdown"`
- **JS-rendered page** (LinkedIn, Crunchbase, React/SPA sites): `url`, `outputFormat: "markdown"`, `render: true`, `premium: true`

For a company website, always fetch homepage + `/about` + `/contact` as three separate calls — they frequently contain different data. Extract every relevant field before moving to the next URL.

---

## Phase 4 — Synthesize

Fill in the contact card from all gathered data. For each field:
- Mark **✓** if confirmed in 2+ independent sources or from a structured endpoint
- Mark **~** if found in one source with supporting context
- Mark **?** if a single unverified mention
- Leave blank (`—`) if not found after reasonable search

See `references/contact-card-schema.md` for field definitions.

Use the template in `assets/contact-card-template.md` to present the output.

---

## Phase 5 — Gap Report

After the contact card, list any high-priority fields still empty and explain briefly why they weren't found. Suggest one concrete follow-up per gap, for example:
- Email not found → "Try Hunter.io (`hunter.io`) or Apollo (`app.apollo.io`) with the company domain"
- Revenue not found → "Check SimilarWeb or Owler for traffic-based revenue estimates"
- Phone not found → "Search `"COMPANY NAME" phone inurl:contact` or check the company's `/contact` page"
- Funding not found → "No Crunchbase page found; the company may be bootstrapped or pre-launch"
- Profile URL not found → "No public profile surfaced; the person may use a pseudonym or have low public presence"

---

## Stop Conditions

Stop searching when any of the following is true:
- All high-priority fields are filled (name, title, company, and at least two of: email, phone, location, profile URL)
- You have made **8 or more API calls** without finding new data
- 3 or more consecutive tool calls returned errors or empty results

Do not loop past these limits. Announce when you've hit a stop condition.

---

## Error Handling

| Error type | What to do |
|------------|-----------|
| MCP tool returns an error or empty result | Retry once with `premium: true` added (for scrape calls). Skip on second failure. |
| "No results" or empty `organic_results` | Try a slightly rephrased query. Count as one call. |
| Tool call fails entirely | Note the failure, skip the URL, and continue with remaining sources. |

Count failed tool calls against the 8-call stop condition.
