---
name: site-audit
description: This skill should be used when the user invokes /site-audit with a URL. It crawls the target website and produces a quality audit report covering broken links, spelling errors, console errors, and visual issues.
---

# Site Audit

**Role:** Thorough website quality auditor.

**Objective:** Crawl the provided URL and all reachable same-domain pages using Chrome browser navigation, checking for broken links, spelling/grammar errors, console errors, and visual issues. Produce a structured report of all findings.

## Input

The user provides a target URL as an argument to /site-audit. Example: `/site-audit https://example.com`

If no URL is provided, ask the user for one. Validate that the input is a valid URL (starts with http:// or https://).

## Execution

**Phase 1: URL Validation & Browser Setup**

1. Extract the URL from the user's command
2. Validate it starts with http:// or https://
3. Set up Chrome browser tab:
   - Call `tabs_context_mcp` to get existing tab group (with `createIfEmpty: true`)
   - Call `tabs_create_mcp` to create one dedicated tab for the entire audit
   - Store the returned tab ID for all subsequent operations
4. Navigate to the seed URL to verify it loads
5. Confirm the target domain with the user

**Phase 2: Chrome-Based Crawl**

After URL validation, begin the breadth-first crawl using Chrome navigation.

**Initialization:**

1. Parse the seed URL to extract protocol, domain (hostname), and path
2. Initialize crawl state:
   - `queue`: List containing only the seed URL (normalized)
   - `visited`: Empty set for tracking crawled URLs
   - `page_count`: 0
   - `max_pages`: 20 (crawl limit — keeps audit focused)
   - `broken_links`: Empty list for recording dead links with source info
   - `seed_hostname`: Extracted hostname from seed URL (for same-domain checks)
   - `link_sources`: Map of {target_url: source_page} for dead link tracking
   - `broken_links_count`: 0
   - `spelling_issues_count`: 0
3. Create `.audit-data/` directory and initialize JSONL files:
   ```bash
   mkdir -p .audit-data
   touch .audit-data/findings-broken-links.jsonl
   touch .audit-data/findings-spelling.jsonl
   ```
4. Reference @references/URL_RULES.md for URL normalization rules
5. Reference @references/CHECKS.md for content analysis and broken link detection rules
6. Display initialization summary to user:
   - Seed URL (normalized)
   - Domain to crawl
   - Max pages limit
   - Chrome tab ID being used
   - Findings will be written to `.audit-data/` directory

**Crawl Loop:**

Execute the following steps in order, looping until termination:

1. **Termination check** — If queue is empty OR page_count >= max_pages, exit loop and proceed to Phase 3

2. **Dequeue** — Remove first URL from queue front (FIFO / breadth-first)

3. **Duplicate check** — If URL already in visited set, skip to step 1 (continue loop)

4. **Mark visited** — Add current URL to visited set, increment page_count

5. **Navigate in Chrome** — Navigate the Chrome tab to the current URL:
   - Use the `navigate` tool with the stored tab ID
   - Wait 3 seconds for page load

6. **Check for 404/error page** — Reference @references/CHECKS.md for detection rules:
   - Read the page title using tabs context (check tab title in tool response)
   - Use `get_page_text` to get page content
   - A page is broken if ANY of these are true:
     - Tab title contains "404", "not found" (case-insensitive), or starts with "undefined"
     - Page text content starts with "404" or contains "page you're looking for wasn't found" or similar 404 patterns
   - **If page is broken:**
     - Get source page from `link_sources` map (use current URL as key)
     - If source not found, use "(seed)" as source
     - Record finding:
       ```bash
       echo '{"type":"broken_link","page":"[source_page]","target":"[current_url]","error":"404","timestamp":"[iso8601_timestamp]"}' >> .audit-data/findings-broken-links.jsonl
       ```
     - Increment `broken_links_count`
     - Skip to step 11 (loop back) — no links to extract from 404 page

7. **Extract links from DOM** — Execute JavaScript on the Chrome tab to get all actual link hrefs:
   ```javascript
   (function() {
     const links = Array.from(document.querySelectorAll('a[href]'))
       .map(a => ({ href: a.href, text: a.textContent.trim().substring(0, 50) }))
       .filter(l => l.href && !l.href.startsWith('javascript:') && !l.href.startsWith('mailto:') && !l.href.startsWith('tel:'));
     return JSON.stringify(links);
   })()
   ```
   This extracts the **actual resolved href** values from the DOM, not guessed URLs.

8. **Classify and route** — For each extracted link:
   - Reference @references/URL_RULES.md for normalization and classification rules
   - **Skip check:** If URL matches any skip rule (mailto:, .pdf, .jpg, etc.), discard it
   - **Same-domain check:** Extract hostname, compare with seed_hostname using strict matching (www. is significant)
   - **If same-domain AND not already in visited set:** Add to queue, record in `link_sources` map: `link_sources[normalized_url] = current_page_url`
   - **If external:** Skip (external link verification is out of scope)

9. **Analyze content** — Reference @references/CHECKS.md for detailed rules:
   - Use the page text already extracted in step 6 (from `get_page_text`)
   - **Spelling/Grammar Check:**
     - Apply filtering rules to exclude non-prose content
     - Identify HIGH confidence spelling errors only
     - For each error found, write finding to JSONL:
       ```bash
       echo '{"type":"spelling","page":"[current_url]","word":"[misspelled]","suggestion":"[correction]","context":"[snippet]","timestamp":"[iso8601]"}' >> .audit-data/findings-spelling.jsonl
       ```
     - Increment `spelling_issues_count`

10. **State update** — After processing each page, output:
    ```
    Page [page_count]/[max_pages]: [current_url] - [issues_found_this_page] issues
    Queue: [queue_length] URLs remaining
    ```

11. **Loop back** — Return to step 1 (termination check)

**After crawl completion:**

- Report total pages crawled
- Report queue status (exhausted or hit page limit)
- Report total findings: broken links and spelling issues
- Proceed to Phase 3

**Notes:**
- ALL link discovery uses JavaScript on the actual DOM — never construct or guess URLs
- Broken link detection happens by navigating to the URL in Chrome and checking the result
- The `a.href` property in JavaScript returns the fully resolved absolute URL (browser handles relative URL resolution)
- Use the same Chrome tab for the entire crawl (navigate between pages)
- If JavaScript execution is blocked on a page, fall back to `get_page_text` and extract visible link text, but do NOT attempt to construct URLs from link text

**Phase 3: External Link Verification** (to be implemented)
- Placeholder: Report that external link verification is not yet implemented

**Phase 4: UI Checks**

After crawl completion, perform Chrome-based runtime checks on all visited pages to detect console errors, broken resources, and visual issues.

**Initialization:**

1. Reference @references/UI_CHECKS.md for console filtering and resource classification rules
2. Get the visited pages list from Phase 2 crawl context (the `visited` set)
3. Reuse the same Chrome tab from Phase 2 (no need to create a new one)
4. Initialize JSONL findings files:
   ```bash
   touch .audit-data/findings-console-errors.jsonl
   touch .audit-data/findings-broken-resources.jsonl
   touch .audit-data/findings-visual-issues.jsonl
   ```
5. Initialize counters:
   - `page_check_count`: 0
   - `console_errors_count`: 0
   - `broken_resources_count`: 0
   - `visual_issues_count`: 0
   - `total_pages`: length of visited set

**UI Check Loop:**

Execute the following steps in order for each URL in visited pages:

1. **Progress check** — If page_check_count >= total_pages, exit loop and proceed to completion

2. **Navigate** — Navigate the Chrome tab to the current URL

3. **Wait** — Wait 3 seconds for page load (scripts, resources, async content)

4. **Console error check** — Reference @references/UI_CHECKS.md for filtering rules:
   - Call `read_console_messages` with `{"tabId": tab_id, "onlyErrors": true, "clear": true}`
   - Filter out messages from `chrome-extension://` URLs
   - Filter out favicon 404 messages
   - For each remaining error message:
     - Write finding to JSONL:
       ```bash
       echo '{"type":"console_error","page":"[url]","level":"[level]","message":"[msg]","timestamp":"[iso8601]"}' >> .audit-data/findings-console-errors.jsonl
       ```
     - Increment `console_errors_count`

5. **Broken resource check** — Reference @references/UI_CHECKS.md for classification rules:
   - Call `read_network_requests` with `{"tabId": tab_id, "clear": true}`
   - Filter for failed requests: status >= 400 or status == 0
   - Filter out `chrome-extension://` requests
   - For each broken resource:
     - Write finding to JSONL
     - Increment `broken_resources_count`

6. **Visual layout check** — Reference @references/UI_CHECKS.md for JavaScript snippets:
   - Execute combined layout check JavaScript
   - Write each finding to JSONL
   - Increment `visual_issues_count`

7. **State update** — After processing each page, increment page_check_count and output progress

8. **Loop back** — Return to step 1 (progress check)

**After UI check completion:**
- Report total pages checked
- Report total findings
- Proceed to Phase 5

**Notes:**
- Single tab reuse: same tab used throughout Phase 2 and Phase 4
- Clear console and network state between pages using `clear: true`
- Reference @references/UI_CHECKS.md for all filtering, classification, and visual check details

**Phase 5: Report**

After UI checks complete, generate the structured markdown report.

**Report Generation:**

1. **Reference rules** — Reference @references/REPORT.md for format specification

2. **Generate filename** — `audit-{domain}-{date}.md` (domain with dots replaced by hyphens)

3. **Read all JSONL findings** — Read each findings file, parse JSON, group by type

4. **Build report** — Following @references/REPORT.md format:
   - Run metadata header (seed URL, pages crawled, duration, timestamp)
   - Summary counts table
   - Conditional TOC (if 50+ findings)
   - Finding type sections with markdown tables
   - Page index sorted by total findings

5. **Write report file** — Use the Write tool to save to working directory root

**After report generation:**
- Report file path to user
- Report total findings count and breakdown by type
- Audit is complete

## Current Status

All phases are implemented. After validating the URL, the skill will:
1. Set up a Chrome browser tab
2. Navigate to pages using Chrome (real browser navigation)
3. Extract links from the actual DOM using JavaScript (real `href` attributes)
4. Detect broken links by navigating to them and checking for 404 page indicators
5. Analyze page text for spelling errors using `get_page_text`
6. Check each page for console errors, broken resources, and visual issues
7. Generate structured markdown report

External link verification (Phase 3) is coming in future updates.
