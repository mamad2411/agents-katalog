---
name: browser-automation
description: Browser automation via agent-browser CLI (Vercel Labs). Headless Chrome navigation, snapshots, clicks, fills, screenshots, eval, and batch flows for web research, UI testing, and QA.
version: 1.4.0
author: Dustin Chadwick (@ShaggyD)
tags: [browser, automation, agent-browser, chrome, web-scraping, testing]
license: MIT
---

# Browser Automation

Usage of `agent-browser` CLI for headless browser automation tasks.

## Problem

Standard headless browsers get blocked by Cloudflare, LinkedIn, Akamai, and similar WAFs immediately. The automation flags in Chrome are easy to detect. navigator.webdriver is set, plugins are empty, languages are wrong. Most sites check these signals before even loading your page.

## Built

A skill combining [agent-browser CLI (Vercel Labs)](https://github.com/vercel/agent-browser) with a stealth Chrome extension that patches browser fingerprint vectors at document_start. Uses specific Chrome flags (`--disable-blink-features=AutomationControlled`, real user agent, consistent viewport) plus the extension to patch navigator.webdriver, plugins, languages, and permissions API before any page scripts run.

## Outcome

Gets through WAFs that normally stop automated browsing cold. Confirmed working against Cloudflare, LinkedIn, Indeed, AI model pricing pages, SaaS documentation portals, and e-commerce product pages. Also includes batch flow patterns for multi-step automation sequences.

## Priority (workflow rule)

**Always try agent-browser FIRST** for any web scraping or page-interaction task — before curl and before the built-in Hermes browser tools (browser_navigate, etc.). The built-in browser is for simple page reads only (no Cloudflare/Akamai). agent-browser with proper flags (see Cloudflare bypass below) has bypassed WAF-protected sites across multiple domains including AI model pricing pages, SaaS documentation portals, e-commerce product pages, and job aggregators — all of which blocked curl and the Hermes browser outright. See `references/waf-protected-site-scraping.md` for concrete eval patterns used across domains.

## Installation

```bash
npm install -g agent-browser
```

Verify: `agent-browser --version`

## Quick Start

```bash
# Open a page
agent-browser --args "--no-sandbox,--disable-gpu,--disable-dev-shm-usage" open https://example.com

# Interactive snapshot (shows elements with refs)
agent-browser snapshot -i

# Click by ref
agent-browser click @e2

# Fill a form field
agent-browser fill @e3 "user@example.com"

# Take a screenshot
agent-browser screenshot --full

# Eval JavaScript
agent-browser eval "document.title"

# Batch multi-step
agent-browser batch '[["open","https://example.com"],["snapshot","-i"]]'
```

## Container/VM Sandbox Workaround

In containerized or VM environments (Docker, Codespaces, WSL), Chrome crashes immediately with:
```
No usable sandbox! If you want to live dangerously, try using --no-sandbox.
```

Always pass these Chrome args for container/VM environments:
```bash
--args "--no-sandbox,--disable-gpu,--disable-dev-shm-usage"
```

This goes BEFORE the command, not after:
```bash
# CORRECT:
agent-browser --args "--no-sandbox,--disable-gpu,--disable-dev-shm-usage" open https://example.com

# WRONG (will be ignored if a daemon is already running):
agent-browser open --args "--no-sandbox" https://example.com
```

Comma-separate multiple args. The `--args` flag uses commas or newlines as delimiters.

If a previous failed attempt left a daemon running, close it first:
```bash
agent-browser close
```

## Common Patterns

| Task | Command |
|------|---------|
| Open + snapshot | `open <url> && snapshot -i` |
| Click and wait | `click @e1 && wait 2000 && snapshot -i` |
| Fill + submit | `fill @e1 "user" && fill @e2 "pass" && click @e3` |
| Screenshot | `screenshot --full` (or `--annotate` for labeled vision output) |
| Download file | `download @e5 /tmp/report.pdf` |
| Get page text | `get text @e1` |
| Keyboard input | `keyboard type "hello world"` |
| Page JavaScript | `eval "document.title"` |
| Batch flow | `batch '[["cmd","arg"],["cmd","arg"]]'` |
| Debug | `doctor` (diagnostics) or `doctor --fix` (repairs) |

## Session Management

- Browser persists as a daemon between commands — chain with `&&`
- Close with `agent-browser close`
- Reuse Chrome profile: `--profile Default open gmail.com`
- Named session for multi-step: `--session-name myapp open ...`
- Connect to running Chrome via CDP: `--cdp 9222 snapshot`

## Pitfalls

- **Daemon collision**: If a previous invocation crashed mid-flight, you'll get "daemon already running". Always `close` before retrying with different args.
- **`--args` position**: Must go BEFORE the command (before `open`, `snapshot`, etc.), not after.
- **No sandbox in containers**: This is the most common failure. Always include `--no-sandbox` in container/VM environments.
- **First run**: `agent-browser` auto-downloads Chrome on first launch if not found. This can take a moment.
- **`--json` response wrapper**: When using `--json`, agent-browser wraps output in `{"success":true,"data":...,"error":null}`. The actual result is nested inside `data`. For eval, the result is at `data.result`. Always unwrap the outer wrapper before accessing response fields.
- **Oversized pages**: Large snapshots auto-spill to files. Check `details.fullOutputPath` for the full content.
- **Cloudflare / WAF bypass — maximum stealth combo (proven on multiple WAF-protected domains):**

  The stealth extension at `extensions/stealth-extension/` (repo root) patches `navigator.webdriver`, plugins array, languages, and permissions before any page scripts run. Combined with Chrome flags and a real UA, this has bypassed Cloudflare on all job aggregators tested.

  ```bash
  # Resolve extension path from skill location (../../extensions/stealth-extension/)
  SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"  # browser/browser-automation/
  EXT_DIR="$(cd "$SKILL_DIR/../../extensions/stealth-extension" && pwd)"

  agent-browser close --all
  agent-browser \
    --args "--no-sandbox,--disable-gpu,--disable-dev-shm-usage,--disable-blink-features=AutomationControlled,--no-first-run,--no-default-browser-check" \
    --user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36" \
    --extension "$EXT_DIR" \
    open https://example.com
  ```

   Then set a realistic viewport and verify stealth:
  ```bash
  agent-browser set viewport 1920 1080
  agent-browser eval "JSON.stringify({webdriver: navigator.webdriver, plugins: navigator.plugins.length, languages: navigator.languages})"
  # Expected: {"webdriver":false,"plugins":5,"languages":["en-US","en"]}
  agent-browser eval "document.body.innerText"   # full page content
  ```

  **What each piece does:**
  - `--disable-blink-features=AutomationControlled` — removes Chrome's automation flag
  - `--user-agent` — realistic Chrome 125 UA (update version periodically)
  - `--extension` — loads a content script that patches detection vectors at `document_start`
  - `--no-first-run` / `--no-default-browser-check` — avoids Chrome's first-run dialogs that give away automation
  - `set viewport` — realistic screen dimensions (headless default is smaller)

  **LinkedIn job search (no login required):** LinkedIn serves job search results to unauthenticated users when the stealth combo is active. Verified on `linkedin.com/jobs/search/` — returns full job cards with titles, companies, locations, and direct apply links. No sign-in wall, no CAPTCHA.

  ```bash
  agent-browser close --all
  EXT_DIR="$(cd "$(dirname "$0")/../../extensions/stealth-extension" && pwd)"
  agent-browser \
    --args "--no-sandbox,--disable-gpu,--disable-dev-shm-usage,--disable-blink-features=AutomationControlled,--no-first-run,--no-default-browser-check" \
    --user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36" \
    --extension "$EXT_DIR" \
    open "https://www.linkedin.com/jobs/search/?keywords=KEYWORDS&location=LOCATION&f_TPR=r604800"
  ```

  LinkedIn uses dynamic/obfuscated CSS class names that change per session, so avoid targeting specific class names. Use the multi-selector fallback pattern for extraction:

  ```javascript
  // Multi-selector extraction for dynamic-class-name pages (LinkedIn, etc.)
  const jobs = Array.from(document.querySelectorAll(
    '.job-card-container, .base-card, .job-search-card, li[class*="jobs-search-results__list-item"]'
  ));
  JSON.stringify(jobs.map((j, i) => {
    const titleEl = j.querySelector(
      '.job-card-list__title, .base-search-card__title, .job-card-container__link, ' +
      'h3, a[data-anonymize="job-title"]'
    );
    const companyEl = j.querySelector(
      '.job-card-container__company-name, .base-search-card__subtitle, ' +
      '.job-card-container__primary-description, .base-search-card__info h4 a'
    );
    const linkEl = titleEl?.tagName === 'A' ? titleEl : titleEl?.querySelector('a');
    return {
      title: titleEl?.innerText.trim() || 'N/A',
      company: companyEl?.innerText.trim() || 'N/A',
      location: j.querySelector(
        '.job-card-container__metadata-item, .base-search-card__metadata, ' +
        '.job-card-container__secondary-description'
      )?.innerText.trim() || 'N/A',
      time: j.querySelector('.job-card-container__listed-state, time, .job-search-card__listed-time')
            ?.innerText.trim() || '',
      link: linkEl?.href || (j.querySelector('a[href*="/jobs/view"]')?.href ?? '')
    };
  }));
  ```

  **Key insight:** Pass multiple CSS selectors comma-separated and query them all — LinkedIn renames classes per session but keeps semantic attribute patterns stable (data-anonymize, href*=/jobs/view). Always fall back to document.body.innerText when structured extraction returns 0 items.

  **Job detail extraction (employment type + salary):** LinkedIn search result cards do NOT display employment type or salary range. To get these, click into individual job cards and extract from the detail panel. After clicking a job link, query document.querySelector("main").innerText and filter for lines containing Employment type, Salary, Part-time, Full-time, or $. The detail panel updates in-place after each click.

  **If still blocked:** try `--headed` on a desktop to see what Cloudflare shows, then add more patches to the `stealth.js` content script.

- **WAF & CAPTCHA bot detection — fallback chain (if above fails):**
  1. **Python `urllib.request` with realistic browser headers** — different TLS fingerprint sometimes escapes detection.
  2. **Google search snippet extraction** — use `web_search("site:target.com ...", limit=50)` for aggregate data from indexed snippets. See `references/search-snippet-extraction.md`.
  3. **Employer-direct career portals** — job aggregators blocked? Hit the employer's own ATS (BambooHR, Paylocity, Workday, ADP). They rarely block. See `references/employer-direct-job-scraping.md`.

## MCP Server Alternative

The `stealth-browser-mcp` skill (`../stealth-browser-mcp/`) exposes the same stealth browser capabilities as **native agent tools** via an MCP server. Instead of CLI commands, the agent calls dedicated tools (`navigate`, `snapshot`, `click`, `eval`). The MCP server bundles the stealth extension inline — no external skill dependency.

Use browser-automation when you want CLI instructions. Use stealth-browser-mcp when you want tool-based integration with Hermes' tool system.

## References

- `references/waf-protected-site-scraping.md` — Concrete agent-browser patterns for extracting data from Cloudflare/Akamai-protected sites using the stealth extension: general extraction approach, real-world use cases (AI pricing, SaaS docs, e-commerce, web app E2E), and employer-direct ATS fallback.
- `references/content-editing-feedback-loop.md` — Edit → screenshot → deliver → iterate workflow for collaborative web content editing with the user.
- `references/structured-data-extraction.md` — Extracting pricing tables, spec sheets, and structured data from JS-rendered pages via eval + text parsing. Covers OpenAI, Anthropic, DeepSeek, and Kimi/Moonshot.
- `references/search-snippet-extraction.md` — Google search snippet fallback for sites behind CAPTCHA that still have indexed content.
- `references/linkedin-job-scraping.md` — LinkedIn job search extraction: no-login access, multi-selector JSON extraction for dynamic class names, page pagination, and fallback strategies.
