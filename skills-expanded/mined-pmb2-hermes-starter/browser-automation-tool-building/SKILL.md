---
name: browser-automation-tool-building
description: Build interactive browser automation tools for authenticated web platforms with anti-bot protection (Cloudflare, PerimeterX). Covers undetected-playwright, stealth injection, session persistence, human-like behavior simulation, modular CLI architecture, and per-platform automation modules.
version: 2.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [browser-automation, web-automation, stealth, anti-bot, playwright, CLI-tools]
    triggers:
      - "build browser automation for * platform"
      - "automate * site"
      - "build tool for fiverr/upwork/freelance platform"
      - "bypass bot detection *"
      - "create automation suite for *"
      - "browser automation tool"
      - "create account on * platform"
      - "scan for matching jobs *"
      - "auto apply to jobs *"
      - "post gig on fiverr/upwork *"
      - "monitor freelance jobs *"
      - "match skills to jobs *"
    related_skills: [web-scraping-scrapling, test-driven-development, systematic-debugging, web-app-qa]
---

# Browser Automation Tool Building

Class-level skill for building interactive browser automation tools targeting web platforms protected by anti-bot systems (Cloudflare, PerimeterX, reCAPTCHA, DataDome).

## Architecture Pattern

```
project/
├── main.py              # CLI entry point (argparse, 1 command per operation)
├── config.py            # Credential management, session/cookie paths
├── browser.py           # Stealth browser engine (undetected-playwright wrapper)
├── platforms/
│   ├── platform_a/__init__.py   # Platform-specific automation class
│   └── platform_b/__init__.py   # Platform-specific automation class
└── utils/               # Helpers (stealth, humanize, storage)
```

## Phase 1: Research

Before writing any code:

1. **Check for official API** — Many platforms have REST/GraphQL APIs (Upwork has one, Fiverr doesn't). An API-based approach is always preferable when available.
2. **Check GitHub for existing tools** — Search `github.com/search?q=<platform>+automation+python` for prior art.
3. **Test the bot protection level** — curl the site. If you get a Cloudflare challenge page or PerimeterX "human touch" page, the site has serious anti-bot protection.
4. **Decide the approach**:
   - API available → use requests/httpx with OAuth (most reliable)
   - Anti-bot but read-only → use `cloudscraper` or Scrapling
   - Anti-bot + interactive (login, messaging, orders) → use `undetected-playwright`

## Phase 2: Stealth Browser Engine

Build a wrapper around `undetected-playwright` (NOT raw Playwright):

### Package requirements
```
playwright>=1.40
undetected-playwright>=0.3.0
```

### Stealth injection script (critical)
Inject via `context.add_init_script()` before any navigation:
```python
# Hide webdriver
Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
# Fake plugins (Chrome has 5)
Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
# Set languages
Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
# Fake chrome.runtime
window.chrome = { runtime: {} };
# Override permissions query
const originalQuery = window.navigator.permissions.query;
window.navigator.permissions.query = (parameters) => (
    parameters.name === 'notifications' ?
    Promise.resolve({state: Notification.permission}) :
    originalQuery(parameters)
);
```

### Browser launch args
```python
args = [
    "--disable-blink-features=AutomationControlled",
    "--disable-features=IsolateOrigins,site-per-process",
    "--no-sandbox",
    "--disable-setuid-sandbox",
    "--disable-infobars",
    "--disable-dev-shm-usage",
    "--no-first-run",
    "--no-default-browser-check",
]
```

### Browser smoke test (required before platform code)
```python
from browser import StealthBrowser
b = StealthBrowser(headless=True, platform="test")
page = b.launch()
page.goto("https://httpbin.org/headers", wait_until="networkidle", timeout=15000)
assert page.evaluate("navigator.webdriver") is None  # stealth must work
b.save_session()
b.close()
```

Failure at this stage means the stealth configuration is wrong — do NOT proceed to platform code until this passes.

### Lightweight alternative: cloudscraper
For read-only operations that don't need login (public job listings, public profiles), `cloudscraper` (v1.2.71+) can bypass basic Cloudflare protection without launching a full browser:
```python
import cloudscraper
scraper = cloudscraper.create_scraper()
response = scraper.get("https://example.com/search")
```
Use this for quick data checks during development. Fall back to full browser for any operation requiring login/interaction.

### Randomize fingerprints per session
- **Viewport**: pick randomly from common sizes (1920x1080, 1440x900, 1536x864, 1366x768)
- **User agent**: rotate from a list of real Chrome user agents
- **Geolocation**: set to a plausible location matching the timezone/locale

### Human-like behavior
```python
# Typing: variable delays per keystroke
TYPING_SPEED = {"fast": (10, 30), "normal": (30, 80), "slow": (80, 200)}

# Random pauses between actions
ACTION_PAUSE = (1.0, 3.0)
```

Key methods every stealth browser wrapper needs:
- `human_type(element, text, speed)` — fills field with per-character delays
- `human_scroll(direction, amount)` — smooth scrolling in steps
- `random_pause(min, max)` — random sleep between actions
- `wait_for_navigation()` — waits for networkidle + random pause

## Phase 3: Session Persistence

This is the key to making automation work on protected platforms:

```python
# Save after login
def save_session(self):
    cookies = self.context.cookies()
    with open(cookie_path, "w") as f:
        json.dump(cookies, f)

    storage = self.page.evaluate("JSON.stringify(localStorage)")
    with open(session_path, "w") as f:
        json.dump({"localStorage": json.loads(storage)}, f)

# Load before navigation
def load_session(self):
    if cookie_path.exists():
        cookies = json.load(open(cookie_path))
        self.context.add_cookies(cookies)
    if session_path.exists():
        state = json.load(open(session_path))
        for key, value in state["localStorage"].items():
            page.evaluate(f"localStorage.setItem('{key}', '{value}')")
```

**Login flow**: First run opens visible browser → user solves any CAPTCHA manually → cookies persist → subsequent headless runs reuse session.

## Phase 4: Per-Platform Automation Modules

Each platform gets its own module with:

1. **Data classes** defining the domain model (e.g., `FiverrGig`, `UpworkJob`)
2. **Automation class** with methods for every operation:
   - `start()` — launch browser, check login state
   - `login()` — authenticate with credentials
   - `search_*()` / `research_*()` — scrape listings
   - `get_*_details()` — scrape individual item details
   - `send_message()` — compose and send in-platform messages
   - `get_messages()` — read inbox
   - `get_orders()` / `get_contracts()` — active work items
   - Platform-specific actions (proposals, gig management)
   - `close()` — save session and clean up

3. **Selectors** — each platform has unique CSS selectors. Store them as module-level constants or dicts for easy updating when the platform changes its UI.

## Phase 5: CLI Interface

Use `argparse` with one subcommand per operation type:

```bash
python main.py research --platform fiverr --query "AI" --pages 3
python main.py login --platform upwork
python main.py analyze --platform both --terms "AI,cybersecurity"
python main.py messages --platform fiverr
python main.py send --platform fiverr --recipient user123 --message "Hello"
python main.py proposal --job-url https://upwork.com/... --cover-letter "..."
```

Include batch mode (`--batch` or `batch` subcommand) that reads operations from a JSON config file for scheduled/automated runs.

## Phase 6: Analysis Features

Build aggregation functions that make the raw scrape data valuable:
- **Price analysis**: min/max/avg per search term
- **Top sellers/clients**: frequency counters
- **Skills/tags in demand**: Counter-based aggregation across all results
- **Client sources**: geographic distribution
- **Trend detection**: compare results across time (requires persistent storage)

## Phase 7: Account Creation Workflow (Guided)

When automating platforms that require accounts, build a guided creation flow:

### Architecture
```python
class AccountCreator:
    def __init__(self, headless=False):
        self.profile_mgr = ProfileManager()
    
    def create_platform_account(self, email=None, password=None):
        # 1. Generate credentials if not provided
        # 2. Create local profile entry
        # 3. Launch browser to signup page
        # 4. Fill form fields (email, password, display_name, etc.)
        # 5. Submit form
        # 6. Wait for user to solve CAPTCHA (with progress indicator)
        # 7. Save session on successful redirect away from signup
```

### Key patterns
- **Generate strong credentials**: `secrets.choice(string.ascii_letters + string.digits + "!@#$%^&*")` for length 16
- **Fill forms defensively**: Try multiple selector patterns per field since signup forms vary
- **CAPTCHA wait loop**: Monitor URL changes + login state detection. Wait up to 120s with periodic status reports. Print progress every 20s so the user knows it's still working.
- **Session save on success**: Save cookies immediately after login state confirmed
- **Profile metadata**: Store email, password, skills, hourly rate, created/last-used timestamps in account.json

### Form-filling strategy
```python
fields = {
    'input[name="email"]': email, 'input[type="email"]': email,       # fallback
    'input[name="password"]': password, 'input[type="password"]': password,
    'input[name="username"]': display_name, 'input[name="fullname"]': display_name,
}
for selector, value in fields.items():
    el = page.query_selector(selector)
    if el and el.is_visible():
        el.fill(value)
```

## Phase 8: Smart Matching & Scoring Engine

Build a capability-matching layer that scores listings against known skills:

### Capability matrix
```python
CAPABILITIES = [
    "AI automation", "machine learning", "LLM", "GPT", "chatbot",
    "Python", "automation script", "web scraping", "API integration",
    "cybersecurity", "data analysis", "workflow automation",
    # ... 40-60 domain-specific entries
]
EASY_WIN_KEYWORDS = [
    "python script", "data extraction", "automation",
    "csv", "excel automation", "template",
]
```

### Scoring algorithm (0-100)
```python
def score_job(title, description="", skills=None):
    text = f"{title} {description}".lower()
    score = 0    
    for skill in self.capabilities:
        if skill.lower() in text:
            matched_skills.append(skill); score += 15
    for kw, bonus in capability_bonuses.items():
        if kw in text: score += bonus  # python+20, ai+20, gpt+25
    for kw in easy_wins:
        if kw in text: score += 10
    # Normalize: min(score, 100)
    return MatchedJob(score=min(100, score), is_easy_win=(easy_matches>=2), ...)
```

### MatchedJob dataclass
```python
@dataclass
class MatchedJob:
    platform: str; title: str; url: str; description: str
    budget: str; budget_max: float; match_score: int   # 0-100
    match_reasons: list; is_easy_win: bool; skills_matched: list
```

### Filter-and-rank pipeline
```python
def filter_and_rank(jobs, default_platform=""):
    scored = []
    for job in jobs:
        # Handle both dataclass objects and plain dicts
        title = getattr(job, 'title', '') or job.get('title', '')
        description = getattr(job, 'description_snippet', '') or job.get('description', '') or ''
        skills = getattr(job, 'skills_required', []) or job.get('skills', [])
        platform = getattr(job, 'platform', '') or job.get('platform', '') or default_platform
        
        matched = self.score_job(title, description, skills, platform)
    scored = [s for s in scored if s.match_score >= 30]  # relevance floor
    scored.sort(key=lambda x: (-x.match_score, x.is_easy_win))
    return scored
```

## Phase 9: AI-Powered Content Generation

Use the matching engine to generate platform-specific content:

### Proposal/cover letter generation
```python
def generate_proposal(matched_job, freelancer_name=""):
    skills_context = f"I specialize in {', '.join(matched_job.skills_matched[:3])}"
    easy_win = " I can complete this efficiently." if matched_job.is_easy_win else ""
    budget = f" within your budget of ${matched_job.budget_max:.0f}" if matched_job.budget_max > 0 else ""
    # Template: greeting → skills match → offer → CTA → signature
    return f"Hi,\n\nI read your posting... {skills_context}... {easy_win}...{budget}..."
```

### Gig/service listing generation
```python
GIG_TEMPLATES = {
    "AI Automation": {
        "title_prefix": "I will build custom AI automation for your business",
        "highlights": ["AI chatbot dev", "Process automation", ...],
        "price_ranges": {"basic": $50, "standard": $150, "premium": $500},
    },
}
```

## Phase 10: Continuous Monitoring Pattern

Set up cron-based scanning that runs autonomously:

### Core components
```python
class JobMonitor:
    def __init__(self):
        self.seen_jobs = set()        # deduplication across runs
        self.report_dir = Path("reports/")
    
    def scan_run(self, search_terms, platforms=("upwork",)):
        # For each platform x search term: search + score
        # Deduplicate against seen_jobs set
        # Generate structured JSON report
        # Print top matches with scores, easy-win flags, URLs
    
    def setup_cron(self, interval_hours=4):
        # Install crontab entry
        cron_cmd = f"0 */{interval_hours} * * * cd ~/project && python -c '...'"
        # Check existing crontab, append if not already present
```

### Deduplication
```python
job_key = f"{platform}:{title}:{url}"
if job_key not in self.seen_jobs:
    self.seen_jobs.add(job_key)
    # process new match
```

### Reports directory
Save each scan as `reports/scan_{timestamp}.json` with:
- total_new_matches, easy_wins, high_value counts
- by_platform breakdown, top_skills_in_demand
- top_matches with scores/reasons/URLs
- easy_win_opportunities list

## Phase 11: Profile Management & Multiple Accounts

```python
class ProfileManager:
    PROFILES_DIR = Path("~/.project/profiles")
    
    def create_profile(self, platform, email, password, **kwargs):
        profile_dir = self.PROFILES_DIR / platform / email_hash
        account = Account(platform, email, password, ...)
        self._save_account(account)
        return account
    
    def get_browser(self, account, headless=False):
        return StealthBrowser(headless=headless,
                              profile=account.email.split("@")[0],
                              platform=account.platform)
```

Account metadata (`account.json`): platform, email, password, display_name, skills, hourly_rate, created_date, last_used, is_active.

## Phase 12: CLI Extensions

Beyond basic research/login commands, a full suite includes:

```bash
# Account management
create-account --platform fiverr     # guided creation
login --platform upwork              # establish session

# Job matching & application
scan --terms "AI,Python,automation"  # search + score + generate proposals
apply                                 # batch-submit saved proposals

# Gig posting
post-gig --query "AI Automation" --message premium  # create + publish

# Continuous monitoring
monitor                               # run one scan now
monitor-setup --pages 4               # install cron job (every 4h)

# Batch operations
batch --job-url batch_config.json     # run ops from JSON file
```

Batch config JSON format:
```json
{
  "operations": [
    {"name": "Research AI", "type": "research", "platform": "upwork", "query": "AI", "pages": 2},
    {"name": "Send proposal", "type": "proposal", "job_url": "...", "cover_letter": "..."}
  ]
}
```

## Pitfalls

- **Full headless triggers detection** — Always do first login in non-headless mode (headless=False) to solve CAPTCHAs. Only use `--headless` after session cookies are established.
- **Hardcoded selectors break** — Platforms redesign their UI frequently. Store selectors in dicts at the top of each module; update them when scraping breaks.
- **Rate limiting** — Add 2-5 second random delays between actions. Fast automation on protected platforms triggers block pages.
- **Session expiry** — Cookies expire (typically 24h-30d). The first command each day may need to re-login. Detect login state before each operation and fall back to login flow.
- **2FA/Security questions** — Fiverr uses TOTP, Upwork uses security questions. Handle both in the login flow with fallback paths.
- **PerimeterX "human touch"** — This is Fiverr's main protection. Session cookies from a real login bypass it. Without cookies, even undetected-playwright triggers this page reliably.
- **Cloudflare challenges** — Upwork uses Cloudflare. Session persistence is the only reliable bypass. `cloudscraper` works for simple GET requests but not for interactive sessions.
- **Test early, test small** — Before building the full suite, verify the browser can navigate to the platform and detect login state. A failing launch wastes hours of platform-specific code.
- **Terminal timeout kills browser sessions** — Account creation with CAPTCHA wait loops can exceed the terminal tool's 300s timeout. Use `execute_code` with a Python script file (not inline bash) for operations that need >60s of wait time. The browser closes when the Python process exits, losing the partially-created session.
- **Account creation timeout recovery** — If the account creation process times out or is interrupted, the profile directory still exists. Re-run the creation command for the same email — it will attempt signup again. Session cookies are only saved after successful login detection, so re-running from scratch is safe.

## Reference Files

- `references/platform-automation-research.md` — Research findings on Fiverr/Upwork anti-bot protection, key URLs, session cookie format, price parsing patterns, and library recommendations.

## Verification

```python
# Quick smoke test
from browser import StealthBrowser
b = StealthBrowser(headless=True, platform="test")
page = b.launch()
page.goto("https://httpbin.org/headers")
assert page.evaluate("navigator.webdriver") is None  # stealth check
b.save_session()
b.close()
```

