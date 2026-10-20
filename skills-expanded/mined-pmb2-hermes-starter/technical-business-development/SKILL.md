---
name: technical-business-development
description: "End-to-end technical business development workflow — investigate a company's platform, identify security/business gaps, build a working proof-of-concept, write business proposals, and package everything into a structured repository with documentation. Combines competitive intelligence, software development, and proposal writing into one lifecycle."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [business-development, competitive-intelligence, poc, proof-of-concept, security-proposal, platform-analysis, technical-due-diligence, api-reverse-engineering, headless-sdk]
    triggers:
      - investigate company
      - competitive intelligence
      - market feasibility
      - could we build
      - cost analysis research
      - venture research
      - technical due diligence
      - security proposal
      - platform analysis
      - build demonstration
      - business development report
      - poc with documentation
      - reverse engineer api
      - capture api traffic
      - headless api client
      - spa api mapping
    related_skills: [spike, github, project-documentation-standards, osint-business, writing-plans, web-app-qa]
---

# Technical Business Development

## Overview

This skill covers the end-to-end lifecycle of turning a technical investigation into a business opportunity: researching a company's platform, identifying security or market gaps, building a proof-of-concept that demonstrates both the capability and the risk, writing a business/security proposal, and packaging everything into a structured GitHub repository.

**Two-track pattern:** Many engagements naturally split into:
- **Track 1 (The Product):** Build the system itself (the thing you're creating)
- **Track 2 (The Pitch):** Package the findings as a security/business solution to sell back to the target company

Track 1 proves it's possible. Track 2 sells the mitigation.

## When to Use

Load this skill when:
- The user says "investigate [company] and tell me how it works"
- The user wants to identify security gaps in a platform and propose solutions
- The user wants a POC built AND a business proposal written
- The user says "document everything and commit to a repo"
- The user wants competitive intelligence on a technology platform

Do NOT use for:
- Pure OSINT research without a technical deliverable (use `osint-business` or `osint-recon`)
- A quick throwaway experiment to validate an idea (use `spike`)
- General documentation authoring without a business angle (use `project-documentation-standards`)

## Workflow

### Phase 0: Market Feasibility (Pre-Investigation)

Run this phase when you have a raw product idea and need to validate whether it's worth building before targeting specific companies.

**When to use:** The user says "could we build [idea]" or asks about market viability, competitors, or costs for a concept.

1. **Define the idea in one sentence** — what are you building, for whom, and why?
2. **Competitive landscape scan:**
   - Search for existing products/services doing the exact thing
   - Search for adjacent solutions (partial overlap)
   - Identify what nobody is doing (the gap / your wedge)
   - Document each competitor: what they do, pricing, weaknesses
3. **FOSS / open-source inventory:**
   - Search for open-source projects that could serve as building blocks
   - Note each tool's: purpose, GitHub stars, license, GPU requirements, current readiness
   - Highlight which tools solve a "hard part" (e.g. NoPoSplat for pose-free 3DGS from sparse photos)
4. **Cost analysis (unit economics):**
   - Break every component into line-item costs (API calls, AI credits, GPU time, hosting)
   - Calculate per-unit cost (per house, per lead, per generation)
   - Compare across pricing tiers if relevant
   - Identify the "volume play" tier (cheapest option that still delivers value)
5. **Package findings into a structured repo:**
   - `README.md` — overview, pricing tiers table
   - `docs/RESEARCH.md` — competitive landscape
   - `docs/COST_ANALYSIS.md` — unit economics
   - `docs/FOSS_INVENTORY.md` — open-source tool catalog
   - `docs/ARCHITECTURE.md` — proposed pipeline design
   - `docs/COMPETITOR_ANALYSIS.md` — head-to-head comparison
   - `.gitignore` — relevant build artifacts
   - Commit and push to a fresh private repo

**Key questions to answer before Phase 1:**
- Does a working path exist from idea to deliverable? (technical feasibility)
- What does it cost to produce one unit? (marginal cost)
- What could we sell it for? (market price signal from competitors)
- What FOSS tools remove the need to build from scratch? (acceleration leverage)

**Output:** A private GitHub repo with all research docs. This is the evidence for whether to proceed to Phase 1 (target a specific company) or pivot.

**Example phase-0 case studies in `references/`:**
- `zillow-tour-pipeline-feasibility.md` — real estate virtual tour pipeline with cost analysis, competitor landscape, and FOSS tool inventory

### Phase 1: Investigate

1. **Surface website:** curl the marketing/brochure site to understand what the company claims
2. **Find the real app:** Look for login portals, customer-facing SPAs, or web apps. These reveal the actual tech stack
3. **Reverse-engineer the tech stack:**
   - Check HTML for build artifacts (Next.js `_next/static/`, Angular `main.*.js`, ASP.NET `__VIEWSTATE`)
   - Check for CDN providers (Cloudinary, Akamai, Cloudflare)
   - Check monitoring tags (New Relic NRUM, Google Analytics, Sentry)
   - Check CMS platforms (Builder.io, Contentful, WordPress)
   - Check meta tags for framework identification
4. **Document routes and auth flow:**
   - Map all observed URL routes
   - Understand auth mechanism (SPA in-memory token? Cookie? JWT?)
   - Note session persistence behavior (does page reload kill auth?)
5. **Identify the real app vs marketing site:**
   - Marketing/brochure sites often run a different stack than the actual product
   - Look for the consumer portal, not just the landing page

**Tools:** `terminal` (curl), `browser_navigate` / Chrome DevTools MCP tools

### Phase 2: Access & Explore

When the user provides credentials or you need to log in:

1. **Navigate to the login page** using the app's URL
2. **Fill credentials** using browser automation (fill_form or individual fill calls)
3. **Handle post-login modals** (TOS acceptance, onboarding, chat widgets)
   - The TOS modal often has an ACCEPT button that can be clicked
   - Chat assist modals need to be dismissed
4. **Map the authenticated app:**
   - Dashboard structure
   - Available products/services
   - Navigation routes
   - Key business features (messaging, payments, calling, etc.)
5. **Test session persistence:** Navigate between routes within the SPA vs full page reloads
   - SPA in-memory auth: navigating via URL fragment changes keeps session
   - Full page navigation via browser URL bar kills session

**Important:** Angular SPAs typically store auth tokens in memory only. A full page reload (changing URL in the address bar) destroys the session. Always navigate by clicking links within the SPA. If session is lost, re-authenticate by filling credentials again.

**Tools:** `mcp_chrome_devtools_mcp_navigate_page`, `mcp_chrome_devtools_mcp_fill_form`, `mcp_chrome_devtools_mcp_click`, `mcp_chrome_devtools_mcp_take_snapshot`, `mcp_chrome_devtools_mcp_evaluate_script`

### Phase 2.5: API Reverse Engineering

Once you have an authenticated session in the browser, the next step is to capture the actual API traffic so you can build a headless client. This is the critical step that moves you from "browser automation required" to "pure API calls, no browser needed."

**Setup:**
1. Ensure the target SPA tab is selected in Chrome DevTools
2. The DevTools MCP server passively records all network requests since the last navigation
3. Use `mcp_chrome_devtools_mcp_list_network_requests` to see all requests

**Capturing API traffic:**

1. **Perform actions** that trigger API calls (login, navigate, read inbox, send form, etc.)
2. **List all network requests** to identify the API calls:
   ```
   mcp_chrome_devtools_mcp_list_network_requests(pageSize=100)
   ```
3. **Filter for API calls** — look for:
   - POST requests to authentication endpoints
   - RESTful patterns (`/api/v1/`, `/services/`, `/ffws/`, etc.)
   - XHR/Fetch requests (not CSS, JS, font, or image loads)
   - Status 200 responses with JSON bodies
4. **Examine request details** for key endpoints:
   ```
   mcp_chrome_devtools_mcp_get_network_request(reqid=<id>)
   ```
   This returns: request headers, request body, response headers, response body

**Key things to extract from each API call:**

- **Full URL** + HTTP method
- **Request body format** (JSON structure, field names, data types)
- **Authentication headers** — these are the keys to headless access
- **Response body structure** — what data comes back
- **Response headers** — tokens, IDs, expiry timestamps
- **Cookie behavior** — session cookies, load balancer affinity

**Authentication mechanisms to look for:**
- JWT Bearer tokens in `Authorization` header
- Custom token headers like `TokenId`, `ContactId`
- Device IDs (`X-DeviceId`)
- Client version headers (`MobileAppVersion`, `DeviceType`)
- Response headers that set auth state (`tokenid`, `contactid`, `tokenexpirationtimestamp`)
- Cookie-based session tracking (HAProxy, load balancer stickiness)

**Infrastructure discovery:**

Check `config/env.json` (or similar config endpoints) for:
- Backend API base URLs (the actual API host, not just the SPA host)
- Authentication type (OPENID_CONNECT, API key, etc.)
- Cloud infrastructure (AWS AppSync, region, GraphQL endpoints)
- Third-party integrations (anti-fraud, analytics, chat widgets)
- CSP headers (Content-Security-Policy reveals all allowed domains)

**SPA navigation trick (critical):**

Angular SPAs store auth tokens in JavaScript memory only. A full page reload destroys the session. To navigate within an authenticated SPA without losing the session:

```javascript
// Use this in the browser console via evaluate_script:
// This changes only the hash fragment, staying within the SPA
window.location.hash = '#/products/emessage/inbox';
```

This calls `mcp_chrome_devtools_mcp_evaluate_script` with that function and preserves the in-memory auth state.

**Building the headless API client:**

Once you've mapped the API surface, build a Python SDK:

```python
class TargetAPIClient:
    """
    Headless API client for [target platform].
    Uses the same REST API as the Angular SPA.
    """
    
    BASE_URL = "https://app.example.com"
    
    def __init__(self):
        self.session = requests.Session()
        self.device_id = str(uuid.uuid4())
        
    def authenticate(self, email, password):
        """POST /api/auth endpoint"""
        # 1. Send credentials
        # 2. Extract JWT/token from response headers
        # 3. Store in session headers for future requests
        # 4. Return auth result with IDs and expiry
        
    def _auth_headers(self):
        """Build common headers for authenticated requests."""
        return {
            "TokenId": self.token_id,
            "ContactId": str(self.contact_id),
            "Authorization": f"Bearer {self.id_token}",
            "X-DeviceId": self.device_id,
        }
```

**Required methods for a complete SDK:**
- `authenticate()` — login + JWT extraction
- `_auth_headers()` — common header builder
- Business methods for each API endpoint discovered
- `get_inbox()`, `send_message()`, `get_balance()` etc.

**Document the API surface** in `docs/api-reference.md`:
- Every endpoint with method, URL, request/response format
- Auth flow step-by-step
- Identifiers (user IDs, account IDs, device IDs)
- Infrastructure details (AWS region, GraphQL endpoints, etc.)
- Rate limits, timeouts, session expiry

**Important:** The browser session that was used for capture stays authenticated and can be used for further discovery. Don't close it until you're done mapping.

### Phase 3: Document Findings

Create structured documentation:

1. **Platform Analysis Doc** (`docs/platform-analysis.md`):
   - Corporate structure (parent company, subsidiaries)
   - Tech stacks for each surface
   - Routes/endpoints mapped
   - Auth flow documented
   - Account details (sanitize credentials)
   - Security observations
   - API surface (documented or inferred)
   - Screenshots where helpful

2. **Architecture Doc** (`docs/architecture.md`):
   - System architecture diagram (ASCII or mermaid)
   - Module descriptions
   - Data flow
   - Security considerations

3. **Security Report / Business Proposal** (`docs/security-report.md`):
   - **Executive Summary** — one-page elevator pitch
   - **Security Gap** — what's vulnerable and why it matters
     - Current monitoring architecture
     - Vulnerabilities table
     - Known incidents proving the gap
   - **Solution** — what you propose to build/sell
     - Architecture diagram
     - Core detection capabilities
     - Technical implementation plan
     - Integration points
   - **Market Analysis** — TAM, competition, regulatory tailwind
   - **Business Model** — pricing, go-to-market, pilot pathway
   - **Competitive Moat** — what makes this defensible
   - **Risks & Mitigations**
   - **Call to Action** — what to do next

**Format:** Markdown files (.md), well-structured with headings, tables, and code blocks where appropriate.

### Phase 4: Build the Proof-of-Concept

Structure the POC as a Python package with clear modules:

```
src/
├── __init__.py
├── main.py              # Entry point with CLI + demo mode
├── config.py             # Environment-based configuration
├── name_bridge.py        # Integration layer for target platform
├── llm_agent.py          # LLM integration for intelligence
├── safety_filter.py      # Content safety / detection engine
└── name_pipeline.py      # Orchestration pipeline
```

**Pattern for each module:**
- Clear class definitions with dataclasses for data types
- Environment-based configuration (never hardcode credentials)
- Logging throughout
- Graceful degradation when dependencies are missing
- Docstrings on all public methods

**Demo mode:** Always include a standalone demo that runs without credentials or live dependencies. This is your proof-of-concept that anyone can run.

**Key principle:** The POC serves double duty:
1. It demonstrates the capability you're building
2. It proves the security gap exists (if you can do it, so can bad actors)

### Phase 5: Package & Publish

1. **Create the GitHub repo:**
   ```bash
   gh repo create <repo-name> --public --description "..." --clone
   ```
   Or use `mkdir && git init && gh repo create` from inside the directory.

2. **Organize the repo structure:**
   ```
   repo/
   ├── README.md              # Elevator pitch, structure, status
   ├── requirements.txt       # Python dependencies
   ├── .gitignore
   ├── .env.example           # Configuration template (no real credentials)
   ├── docs/
   │   ├── architecture.md
   │   ├── platform-analysis.md
   │   └── security-report.md
   ├── research/
   │   └── sources.md         # Citations
   └── src/
       ├── __init__.py
       ├── main.py
       ├── config.py
       └── ... (POC modules)
   ```

3. **Add .gitignore:** session/, logs/, .env, *.log, *.jsonl, __pycache__/, *.pyc

4. **Commit with descriptive messages:**
   ```
   Initial commit: [project name] platform analysis and security report
   
   - Platform analysis: Reverse-engineered [target] tech stack
   - Security report: [solution] proposal with market analysis
   - Sources: cited references
   - README: Project overview and structure
   ```

5. **Push:**
   ```bash
   git remote add origin https://github.com/user/repo.git
   git push -u origin main
   ```

**Tools:** `gh repo create`, `git add/commit/push`, `write_file`, `terminal`

## Two-Track Strategy (Critical Pattern)

Many engagements naturally produce TWO products:

| Track | Description | Example |
|-------|-------------|---------|
| **Track 1: The Product** | The system itself — automated messaging, LLM agent, monitoring tool | "JailAI: An automated inmate communication system" |
| **Track 2: The Pitch** | The security/mitigation solution sold back to the target | "AI threat detection for Securus/JPay" |

**Order matters:** Build Track 1 first (the POC). Use the working POC as evidence/exhibit for Track 2 (the pitch). This mirrors a classic security research pattern: "we found the vulnerability, here's the exploit, and here's how you fix it."

## Content Safety Screening (Dual-Use Design)

When building a system that processes user/inmate messages, include a safety filter with layered detection:

| Layer | Technology | Purpose |
|-------|------------|---------|
| 1. Regex patterns | Fast pattern matching | Catch known threats instantly |
| 2. Coded language | Phrase/slang matching | Detect euphemisms and coded terms |
| 3. LLM classification | Semantic analysis | Catch novel patterns and context-dependent threats |
| 4. Policy rules | Configurable lists | Facility/company-specific content rules |

The safety filter serves dual purposes:
- Screens your own system's messages (safety/compliance)
- Demonstrates the detection capability you'd sell (the pitch)

## User Preferences (the operator)

When working for the operator:
- Everything is documented, committed, and pushed to GitHub
- Reports go in .MD files
- Deliver working code, not plans
- Voice messages may have transcription errors -- use context to deduce meaning
- Two-track strategy: product first, pitch second
- No em dashes (M-dashes) in any writing

## Pitfalls

1. **Lost SPA sessions:** Navigating to a hash URL via full page navigation kills Angular in-memory auth. Always navigate within the SPA by clicking links. If session is lost, re-authenticate.

2. **Credentials in code:** Never commit real credentials to the repo. Use environment variables and a .env.example template.

3. **Marketing vs product:** The marketing website is often a different tech stack than the actual product. Don't confuse them. The real app is at the login portal URL.

4. **TOS acceptance:** Some apps require accepting Terms of Service on first login. This modal needs to be found and clicked programmatically.

5. **Report-only without POC:** Don't write a security proposal without a working demonstration. The POC is the evidence that makes the pitch credible.

6. **Over-reliance on regex detection:** Regex-based detection has high false-positive and false-negative rates. Use it as a first pass, not the only layer. The demo should explicitly show both what regex catches AND what it misses to make the case for LLM-based semantic analysis.

7. **Skipping sources:** Every business/security proposal needs cited sources (FCC docs, market reports, news articles). Keep a `research/sources.md` file with full citations.

8. **Missing the config/env.json:** Many SPAs expose a configuration endpoint that reveals the entire backend infrastructure (API hosts, AWS regions, GraphQL endpoints, anti-fraud providers). Always check `GET /config/env.json` (or similar) during the API discovery phase.

9. **Not checking response headers:** Critical auth state (JWT tokens, user IDs, session expiry) often lives in RESPONSE HEADERS, not the response body. Use `get_network_request` to examine headers — the body alone is insufficient.

10. **Assuming one auth mechanism doesn't mean the only one:** Securus uses a triple combo: JWT Bearer token (Authorization header) + tokenid header + contactid header + X-DeviceId. Missing any one of these causes 401 errors. Always reconstruct the full header set from the captured requests.

11. **Not persisting the browser session:** The browser tab with the authenticated SPA is your map — you can keep using it for discovery while building the headless client. Don't close it until you're fully done mapping. The CDP network log continues recording.

## Verification Checklist

- [ ] Platform analysis documents the marketing site AND the real app
- [ ] Auth flow is documented with session persistence behavior
- [ ] All credentials use environment variables, not hardcoded values
- [ ] Repo has README, .gitignore, requirements.txt, .env.example
- [ ] POC has a demo mode that runs without live credentials
- [ ] Security proposal has: executive summary, gap analysis, solution, market analysis, business model
- [ ] Research sources are cited
- [ ] Everything committed and pushed to GitHub
- [ ] Two-track strategy is documented if applicable
