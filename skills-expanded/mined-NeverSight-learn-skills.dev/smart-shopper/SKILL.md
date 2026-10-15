---
name: smart-shopper
description: Product research and comparison shopping assistant. Use this skill whenever the user wants to find, compare, or filter products on any online shopping platform (Amazon, Rakuten, Yahoo Shopping, IKEA, Costco, Taobao, JD, etc.). Triggers include "find me a product", "search for X on Amazon", "help me buy Y", "compare products", "I need a [product]", "search [platform] for", "shop for", "looking for something to buy", any mention of shopping criteria like price range, star ratings, product specifications, or when the user names a product category and an online store. Also triggers when the user changes filtering criteria mid-search (e.g., "relax the rating to 3.9", "what if we increase the budget"). This skill caches all search results in a local SQLite database so criteria changes can be answered instantly without re-searching.
dependencies: agent-browser
---

# Smart Shopper — Product Research & Comparison Skill

## Prerequisites

This skill requires `agent-browser` for all web interaction. Before starting any search:

1. Check if the `agent-browser` skill is available in your skill list
2. If available, load it: use the `skill` tool to load `agent-browser`
3. If NOT available, install it:
   ```bash
   npx skills add agent-browser
   ```
   Then load the skill after installation.

Do NOT proceed with any search steps until `agent-browser` is confirmed working. Quick check:
```bash
agent-browser --version
```
If the CLI itself is missing, install it: `brew install agent-browser` or `npm i -g agent-browser`, then `agent-browser install` to download the browser.

## Why This Skill Exists

Online product research is tedious: you search, open dozens of tabs, compare specs, lose track of what you've already checked, and when criteria change, you start over. This skill solves that by:

1. **Caching everything** in SQLite — criteria changes trigger instant re-filtering, not re-searching
2. **Structured extraction** — prices, ratings, review counts go into queryable columns
3. **Full page preservation** — raw page text is stored so you can dig into specs later without re-visiting

## Workflow Overview

```
User request
    ↓
[1] Clarify requirements (platform, criteria, budget, language)
    ↓
[2] Search platform via agent-browser → extract product list
    ↓
[3] Cache basic info in SQLite → immediately filter by rating/price/review_count → candidate list
    ↓
[4] Verify candidates only (parallel batch — visit product pages, extract specs, store page_text)
    ↓
[5] Present results (table + recommendation)
    ↓
[6] User changes criteria? → Re-query cached DB, only re-search if data insufficient
```

## Step 1: Clarify Requirements

Before searching, always ask the user:

| Question | Why it matters |
|---|---|
| **Platform** | Which site to search (Amazon.co.jp, Rakuten, etc.) |
| **Product type** | What they're looking for |
| **Budget** | Price ceiling |
| **Key physical/technical criteria** | Weight, size, material, features — whatever matters for this product |
| **Rating threshold** | Minimum star rating (default: suggest 4.0+) |
| **Review requirements** | e.g., "must have Japanese reviews", minimum review count |
| **Quantity needed** | How many candidates to present (default: 10) |
| **Site language** | What language should the site display in? (default: infer from platform — e.g., Amazon.co.jp → Japanese, Amazon.com → English). If unclear, ask the user. |

Use the user's language throughout. If they write in Chinese, respond in Chinese. If Japanese, respond in Japanese.

## Step 2: Search

Use `agent-browser` to search the target platform. Construct search queries using the user's product description + key criteria keywords in the platform's language.

### Set Site Language First

agent-browser starts with a clean browser (no cookies, no language preferences). Many sites default to English even for local domains (e.g., Amazon.co.jp shows English to new visitors). **Before any search, switch the site to the correct language.**

**Amazon language switch examples:**
- Japanese: navigate to `https://www.amazon.co.jp/-/ja/` or append `?language=ja_JP` to any URL
- Chinese: `https://www.amazon.co.jp/-/zh/` or `?language=zh_CN`
- English: `https://www.amazon.co.jp/-/en/` (usually the default)

**For other platforms:** look for a language/locale selector in the page header or footer, or set the `Accept-Language` header if supported.

**Why this matters:**
- Page text stored in `product_pages` will be in the site language — if English, Japanese keyword searches on cached data won't work
- Spec table field names differ by language ("Item Weight" vs "商品の重量")
- Review language detection is more reliable when the site matches the target language

**Search target: 100+ products.** Broad coverage here means better filtering in Step 3 and less re-searching when criteria change. Aim for 100 unique products before proceeding. Fallback rules:
- After 3 keyword variations with full pagination and still under 100 → proceed with what you have.
- Below 30 products → inform the user the market is narrow and ask whether to broaden the category.

**Search strategy:**
- Use 2-3 keyword combinations that cover the core need from different angles (e.g., synonyms, category terms, brand keywords). Keep all variations within the same product category to avoid polluting the DB with irrelevant products. Insert results from each query into the DB before moving to the next.
- For each query, paginate through at least 4-5 pages of results. Most platforms show 16-48 products per page, so 4-5 pages from 2-3 queries typically reaches 100+.
- After each page insertion, check the running total via the insert command's `total_in_db` output (`UNIQUE(platform, product_id)` deduplicates, so this count reflects unique products even when queries overlap). Stop paginating once you reach 100+.
- If results are sparse despite multiple queries, broaden keywords (e.g., drop adjectives, use the parent category) and search again.
- Extract data from search result pages using JavaScript eval (fast, no need to open each product)

**Extraction pattern (Amazon example):**
```javascript
// Run via agent-browser eval to extract search results
Array.from(document.querySelectorAll('[data-asin]'))
  .filter(el => el.dataset.asin.length > 3)
  .map(el => ({
    product_id: el.dataset.asin,
    name: (el.querySelector('h2 span') || {}).textContent || '',
    rating: /* extract star rating */,
    price: /* extract price */,
    review_count: /* extract review count */,
    url: 'https://www.amazon.co.jp/dp/' + el.dataset.asin
  }))
```

Adapt the selectors for each platform. The goal: get product_id, name, rating, price, review_count, and URL from the search results page itself.

**CRITICAL: Write extracted data to a JSON file, not to LLM context.** Large product lists (50+ items) will be truncated or corrupted if passed through the LLM. Use this pattern:

```javascript
// In agent-browser eval: extract products and write JSON file directly
const products = Array.from(document.querySelectorAll('[data-asin]'))
  .filter(el => el.dataset.asin.length > 3)
  .map(el => ({ /* extraction logic */ }));
// Write to temp file
require('fs').writeFileSync('/tmp/products_page1.json', JSON.stringify(products));
products.length; // return count only
```

Then insert via file:
```bash
python3 product_db.py insert --db <DB_PATH> --json-file /tmp/products_page1.json --platform amazon.co.jp
```

The insert command outputs `received`, `inserted`, `skipped` counts. If `received` is much less than what you extracted, the JSON file was corrupted. If `skipped` is high, products were duplicates from overlapping searches (expected).

## Step 3: Cache & Filter

Store basic info (name, price, rating, review_count, URL) for all extracted products in SQLite. This is cheap — just search result data, no page visits needed. Then **immediately filter** to identify candidates for detailed verification.

**Database directory:** `~/.cache/smart-shopper/`

**Filename format:** `{YYYY-MM-DD}-{topic-slug}-{4hex}.db`
Example: `2026-03-29-garden-table-set-a3f1.db`

### Database Discovery (automatic — don't ask the user unless ambiguous)

Every DB contains a `_meta` table with `created_at`, `last_accessed`, `description`, and `search_queries` (JSON array). Use this for auto-matching.

```
Start of skill invocation
  │
  ├─ Already have DB_PATH in this conversation?
  │   └─ YES → reuse it, skip discovery
  │
  ├─ Run: product_db.py discover --query "user's search terms" --auto-cleanup
  │
  ├─ 0 databases found → create new DB
  │
  ├─ Results with match_score > 0?
  │   ├─ Exactly 1 match → auto-select, tell user: "Continuing with [description]"
  │   └─ Multiple matches → show list, ask user to pick
  │
  ├─ All results have match_score = 0 (no keyword overlap)?
  │   ├─ Any DB accessed in last 24h → show it as option, ask if related
  │   └─ Otherwise → create new DB
  │
  └─ discover also prunes DBs not accessed in 30+ days
```

The key rule: **never auto-select a DB without query matching**. Recency alone is not enough — a "keyboard" search must not silently attach to yesterday's "chair" DB.

**Auto-discovery command (also prunes >30 day old DBs):**
```bash
python3 /path/to/smart-shopper/scripts/product_db.py discover --cache-dir ~/.cache/smart-shopper --query "user's search terms" --auto-cleanup
```
This returns matching DBs sorted by relevance score, and silently removes any DB not accessed in 30+ days.

### Creating a New DB

```bash
python3 /path/to/smart-shopper/scripts/product_db.py create --topic "garden table set"
```

This generates a safe filename internally (sanitized slug + UTC date + random hex) and returns the path in JSON:
```json
{"status": "ok", "db": "/Users/you/.cache/smart-shopper/2026-03-29-garden-table-set-a3f1.db"}
```

Never construct DB filenames in shell commands — always use the `create` command to avoid injection risks.

### Within a Conversation

Always reuse the same DB. Multiple product categories can coexist (tracked by `search_query` column).

### Self-Cleanup

Cleanup is built into the `discover` command — when `--auto-cleanup` is passed, any DB with `last_accessed` older than 30 days is automatically removed. No separate cleanup step needed.

Use the helper script to manage the database:

```bash
python3 /path/to/smart-shopper/scripts/product_db.py create --topic "garden table set"
python3 /path/to/smart-shopper/scripts/product_db.py insert --db <DB_PATH> --json-file /tmp/products.json --platform amazon.co.jp
python3 /path/to/smart-shopper/scripts/product_db.py query --db <DB_PATH> --min-rating 4.2 --max-price 100000
python3 /path/to/smart-shopper/scripts/product_db.py update-detail --db <DB_PATH> --product-id "B09T97Z57Y" --page-text-file /tmp/page.txt --specs '{"weight": "16.74kg", ...}'
python3 /path/to/smart-shopper/scripts/product_db.py update-detail --db <DB_PATH> --product-id "B09T97Z57Y" --verified
python3 /path/to/smart-shopper/scripts/product_db.py query --db <DB_PATH> --spec-filter "table_weight_kg>=12" --spec-match "material=wood"
```

**Schema:**

```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    platform TEXT NOT NULL,
    product_id TEXT NOT NULL,
    name TEXT,
    price REAL,
    price_raw TEXT,                    -- original text e.g. "¥12,800" / "$128.00"
    currency TEXT DEFAULT 'JPY',
    rating REAL,
    review_count INTEGER,
    search_rank INTEGER,              -- position in search results (quality signal)
    url TEXT,
    search_query TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    specs_json TEXT,
    verified INTEGER DEFAULT 0,
    UNIQUE(platform, product_id)
);

CREATE TABLE product_pages (          -- separate table to keep products lean
    product_id TEXT NOT NULL,
    platform TEXT NOT NULL,
    page_text TEXT,                    -- full innerText for later extraction
    fetched_at TIMESTAMP,
    PRIMARY KEY (platform, product_id)
);

CREATE TABLE _meta (key TEXT PRIMARY KEY, value TEXT);
```

**Key design decisions:**
- `product_pages` is a separate table so filter queries on `products` stay fast (no 100KB blobs scanned).
- `price_raw` preserves the original display text; `price` is the parsed numeric value for SQL comparison.
- `search_rank` captures result position — a free quality signal.
- `specs_json` stores extracted specifications as a JSON object (e.g., `{"table_weight_kg": 16.74, "chair_weight_kg": 7.64, "material": "PS wood"}`).
- `UNIQUE(platform, product_id)` prevents duplicates when searches overlap.
- `verified` flag tracks which products have been individually checked.

### Immediate Filtering

Right after inserting products, filter using the data already available from search results. **Do NOT visit any product pages yet** — this filter uses only what's in the `products` table.

```sql
SELECT * FROM products
WHERE rating >= 4.2          -- replace with user's threshold
  AND price <= 100000         -- replace with user's budget
  AND review_count >= 10      -- default minimum; replace with user's if specified
ORDER BY rating DESC, review_count DESC;
```

**Default minimum review count is 10** unless the user specifies otherwise. Products with fewer than 10 reviews have unreliable ratings and waste page visits.

This produces the **candidate list** — only these products proceed to Step 4 (page visits + detailed verification). The remaining products stay in the DB for potential re-query if the user relaxes criteria later, but their pages are never visited.

Note: criteria that can't be expressed in SQL (e.g., "Japanese reviews exist", "chair weight per component") require visiting the product page — these are checked in Step 4, not here.

If insufficient products match, tell the user how many matched and suggest criteria relaxation. Show the distribution: "Found 3 products at ≥4.2★. Relaxing to ≥3.9★ would add 4 more."

## Step 4: Detailed Verification

Step 3 filtered using basic search-result data (rating, price, review count). But many user criteria — weight, material, dimensions, review language — are only available on the product page. Step 4 has three phases:

1. **Batch extract**: Visit candidate pages in parallel, extract specs → store in DB
2. **Detailed filter**: SQL filter again using the newly extracted specs → much smaller final set
3. **Verify**: Cross-verify and checklist only the final few products

Example flow:
> 61 candidates (from Step 3) → batch page visits → extract specs → detailed filter (weight≥12kg, chair≥7kg) → **5 finalists** → cross-verify + checklist

### Page Extraction Strategy

Visiting product pages is the biggest time bottleneck (~10-15 seconds per page). Two approaches available — choose based on candidate count and environment stability.

#### Default: Sequential Extraction with Smart Ordering (Recommended)

Visit candidate pages **sequentially in the parent agent**. This is simpler, more reliable, and often faster than parallel sub-agents because:
- No sub-agent initialization overhead (~30s each)
- No browser session conflicts
- Early termination: stop once enough qualifying products are found
- Resumable: specs persist in DB after each product, so interruptions don't lose progress

**Candidate ordering** (visit most-likely-qualifying products first):
1. Known heavy brands first (e.g., Yamazen Garden Master, THREE STONE, aks for furniture)
2. Higher price (correlates with heavier construction)
3. Higher review count (more data available for verification)

**Resume check** — before visiting any pages, skip products already extracted:
```sql
SELECT product_id, url FROM products
WHERE specs_json IS NULL
  AND rating >= ?    -- Step 3 filter criteria
  AND price <= ?
ORDER BY price DESC, rating DESC;
```
This makes the workflow resumable after network interruptions — just re-run and it picks up where it left off.

**For each candidate:**
1. `agent-browser open {url}` → wait for page load
2. Scroll to load dynamic content (reviews, spec tables often lazy-load)
3. Extract full page text → write to temp file → `python3 {script} update-detail --db {db} --product-id {id} --page-text-file /tmp/{id}_page.txt`
4. Extract specs from the structured spec table (not marketing copy) → `python3 {script} update-detail --db {db} --product-id {id} --specs '{...}'`
5. **Early termination check**: if the user requested N qualifying products and you've found N products that pass ALL spec criteria so far, you may stop visiting remaining candidates and proceed to Step 4a.

#### Alternative: Parallel Sub-Agent Extraction

Use only when: (a) ≥ 20 candidates, (b) network is stable, (c) you've confirmed agent-browser supports parallel sessions.

**CRITICAL: Each sub-agent MUST use a unique `--session` flag** to avoid browser daemon conflicts:
```bash
agent-browser --session batch-1 open {url}
agent-browser --session batch-1 eval "..."
```

**Batch strategy:**
- Split into batches of ~10, spawn one sub-agent per batch
- Maximum 3 concurrent sub-agents (more risks resource exhaustion)

**Sub-agent delegation template:**

```
task(
  category="unspecified-low",
  load_skills=["agent-browser"],
  run_in_background=true,
  description="Extract product details batch N/M",
  prompt="
    TASK: Visit product pages and extract detailed specs. Data extraction only — do NOT make pass/fail judgments.

    BROWSER SESSION: Use --session batch-{N} for ALL agent-browser commands to avoid conflicts with other agents.
    Example: agent-browser --session batch-{N} open {url}

    DB: {db_path}
    SCRIPT: python3 {path/to/product_db.py}

    PRODUCTS (batch N of M):
    1. {product_id} | {url} | {name}
    2. ...

    SPECS TO EXTRACT (based on user criteria):
    - {spec 1, e.g., table weight in kg}
    - {spec 2, e.g., chair weight in kg}
    - {spec 3, e.g., material type}
    - ...

    FOR EACH PRODUCT:
    1. agent-browser --session batch-{N} open {url}
    2. Scroll to load dynamic content (reviews, spec tables often lazy-load)
    3. Extract full page text → write to a temp file, then store:
       python3 {script} update-detail --db {db} --product-id {id} --page-text-file /tmp/{id}_page.txt
    4. Extract ALL specs listed above from the structured spec table (not marketing copy)
    5. Store specs in specs_json:
       python3 {script} update-detail --db {db} --product-id {id} --specs '{...}'

    WHEN DONE: Close your browser session:
       agent-browser --session batch-{N} close

    MUST NOT:
    - Set verified=1 (that happens later, after detailed filtering)
    - Skip storing data for any product — even if specs look bad (data is valuable for later criteria changes)
    - Retry more than once if agent-browser fails on a product — skip and move on
    - Use agent-browser WITHOUT --session batch-{N} (will conflict with other agents)

    RETURN: For each product: product_id, extracted specs summary, any specs that were NOT found on the page.
  "
)
```

**After all sub-agents complete:**
1. Close any remaining browser sessions: `agent-browser --session batch-{N} close` for each batch
2. Collect results and note any products where specs could not be extracted
2. Proceed to Step 4a (detailed filtering)

### 4a: Detailed Filtering (second-round filter)

Now that `specs_json` is populated from page visits, filter again using the detailed specs. This is the **second filter** — it uses product page data that wasn't available in Step 3.

```sql
SELECT p.*, pp.page_text FROM products p
LEFT JOIN product_pages pp ON p.product_id = pp.product_id AND p.platform = pp.platform
WHERE (json_extract(p.specs_json, '$.table_weight_kg') >= 12
       OR json_extract(p.specs_json, '$.table_weight_kg') IS NULL)
  AND (json_extract(p.specs_json, '$.chair_weight_kg') >= 7
       OR json_extract(p.specs_json, '$.chair_weight_kg') IS NULL)
  AND (json_extract(p.specs_json, '$.material') NOT LIKE '%cedar%'
       OR json_extract(p.specs_json, '$.material') IS NULL)
ORDER BY p.rating DESC, p.review_count DESC;
```

The `IS NULL` clauses are critical — without them, products where the sub-agent couldn't extract a spec are silently dropped. These are exactly the products that need cross-verification in Step 4b.

This typically reduces the candidate set dramatically (e.g., 61 → 5). Only these **finalists** proceed to cross-verification and the full checklist.

If a spec couldn't be extracted (sub-agent reported it missing), don't discard the product — include it in the finalists for manual cross-verification in Step 4b.

Report the funnel to the user:
> "61 candidates → page visits complete → detailed filter (weight, material) → **5 finalists**"

### 4b: Cross-Verification (only for finalists with missing/ambiguous specs)

Only for the small set of finalists from Step 4a, and only when a critical spec is missing or ambiguous.

**When to cross-verify:**
- A spec the user explicitly cares about is **not directly stated** on the product page (this includes cases where you could calculate it from other values — calculation is not verification)
- The product page shows a total weight but not per-component breakdown
- A claim seems inconsistent (e.g., "Item Weight 14kg" but individual parts sum to 28kg)
- Values are **ambiguous**: two or more conflicting values for the same spec on the page, OR a value that differs significantly from similar products, OR a value only in marketing copy but missing from the specs table

**How to cross-verify safely:**
1. Extract the **exact model number** from the product page (e.g., "MFC-259D", "HMTS-50", "KPT-1470")
2. Search the model number using whatever search tools you have available (web search, DDG, webfetch, etc.) — simply search for `"manufacturer name" + "model number" + "specs"` or the equivalent in the relevant language
3. **Match identity strictly**: the model number, dimensions, and manufacturer must ALL match. A similar-looking product from the same brand is NOT the same product.
4. If the cross-verified spec is found, update `specs_json` in the DB and note the source

Do NOT hardcode any specific verification site (e.g., Kakaku.com is Japan-only). Use whatever search capability the agent currently has. The model number is the key — it's globally unique and searchable on any search engine.

**Identity matching rules:**
- ✅ Same manufacturer + same model number + same dimensions → confirmed match
- ❌ Same manufacturer + different model suffix (e.g., MFC-259D vs MFC-259DN) → treat as different unless specs page covers both
- ❌ Same appearance + different brand → NOT the same product
- ❌ Similar name but no model number match → NOT verified

**Do NOT cross-verify when:**
- The product page directly states the exact value your criterion needs (not a derived or related value — the actual number)
- The product has no identifiable model number (generic no-brand items)
- You're just curious — only cross-verify for specs the user's criteria depend on

### 4c: Screenshot Verification

Only if the user's criteria involve something that can't be verified from text alone (e.g., "can this chair really lie flat?" or "what does the design look like?"). Don't screenshot by default — it's slow. If you do screenshot, use `agent-browser screenshot` + `look_at` tool to analyze the image.

### 4d: Criterion Verification Checklist

After all data is collected (page extraction, detailed filtering, cross-verification), go through EVERY user criterion one by one for each finalist before marking it as verified. For each criterion:

1. **State the criterion** (e.g., "Japanese reviews must exist")
2. **State how you verified it** (e.g., "Opened review section, found 3 reviews in Japanese")
3. **State the result** — pass or fail
4. **Tag the evidence type**: `[direct]` = read from page, `[cross-verified]` = from external source, `[estimated]` = derived/calculated (must resolve via 4b first), `[unverified]` = could not confirm

**Only set `verified = 1` when ALL user criteria show `[direct]` or `[cross-verified]`.** Products with any `[estimated]` or `[unverified]` criteria must NOT be marked verified — either resolve them via cross-verification or present them to the user with the tag visible.

**Criterion type → verification method:**

| Criterion Type | Examples | How to Verify |
|---|---|---|
| **Numeric spec** | weight ≥ 7kg, price ≤ ¥10k | Read the exact value from a structured spec table on the product page. If only a related value exists (e.g., total weight but not per-component), treat the specific value as missing → cross-verify (4b). |
| **Review quality** | "Japanese reviews exist", "≥10 reviews" | Open the review section of the product page (scroll/click to load it). Count reviews matching the requirement. A star rating or review count alone does NOT satisfy a review-language requirement. |
| **Visual/behavioral** | "fully flat recline", "fits 4 people" | Screenshot verification (4c), or find an explicit spec value (e.g., "recline angle: 180°"). Product title claims do not count. |
| **Material/durability** | "no cedar", "waterproof" | Read material from the spec table. Assess durability based on the material type identified. |
| **Availability** | "Prime eligible", "in stock" | Check the specific section on the product page. |

## Step 5: Present Results

Use a Markdown table with the most relevant columns for this specific product search. Always include:
- Product name (abbreviated if long)
- Price
- Rating + review count
- URL (full link)
- Key criteria columns (whatever the user specified — weight, material, size, etc.)

After the table, add a **brief recommendation section** organized by use case:

```markdown
| Priority | Pick | Reason |
|---|---|---|
| Value | Product A | Cheapest that meets all criteria |
| Quality | Product C | Highest rating + most reviews |
```

## Step 6: Iterate

When the user changes criteria:

1. **First, query the existing DB** — instant results
2. **Report what's available**: "Relaxing to ≥3.9★: found N additional products in cache"
3. **If newly qualifying products lack page data**, distinguish two cases:
   - **Never visited** (no row in `product_pages`): run Step 4 batch extraction for them
   - **Visited but spec missing** (`product_pages` exists, `specs_json` is NULL): skip extraction, go directly to cross-verification (Step 4b)
4. **Only re-search if the DB doesn't have enough data** (e.g., user wants a completely different product type)

This is the key advantage of the caching design: what previously required 20 minutes of re-searching now takes 2 seconds.

## Important Principles

### Honesty Over Quantity
If the user asks for 10 products but only 6 genuinely meet all criteria, say so. Don't pad the list with products that don't qualify. Suggest criteria relaxation instead.

### Don't Trust Text — Verify Claims
Product titles and bullet points often exaggerate. "180° fully flat" might be 150°. "Lightweight" might be 11kg. When a specific claim matters to the user, verify it on the actual product page's structured specification table, not from marketing copy or search results summaries.

### Direct Observation, Not Derivation
When a specification determines whether a product meets user criteria, the value MUST come from direct reading on a product page spec table, manufacturer spec sheet, or cross-verified external source.

**Never derive a user-critical spec through calculation.** Example: if the page shows total weight (34kg) and table weight (18kg), do NOT calculate bench weight as (34-18)/2 = 8kg. Instead, treat bench weight as "not directly stated" and trigger cross-verification (Step 4b).

Why this matters: mathematical derivation introduces compounding errors (shipping weight vs. product weight, accessories included vs. excluded, rounding). A derived value that passes a threshold by a small margin (8kg vs. 7kg requirement) is especially unreliable.

### Show Your Work on Filtering
When presenting results, briefly note how many total products were found, how many passed each filter, and how many survived to the final list. This helps the user understand the market and make informed decisions about relaxing criteria.

Example:
> Searched 3 keyword variations, paginated 4-5 pages each → 127 products cached.
> After filtering (★≥4.2, ¥≤100,000, reviews≥10): 31 remain.
> After weight verification (table≥12kg, chair≥7kg): 5 qualify.

### Platform-Specific Tips

**Amazon.co.jp / .com:**
- Extract ASINs from `[data-asin]` attributes
- Product URL pattern: `https://www.amazon.co.jp/dp/{ASIN}`
- Rating and price may need JavaScript extraction from specific selectors
- "Item Weight" on Amazon is unreliable — could be shipping weight, single component, or total

**Rakuten:**
- Product IDs from URL patterns
- Rating system differs (may need normalization)

**Other platforms:**
- Adapt selectors and URL patterns as needed
- The core workflow (search → extract → cache → filter → verify → present) is the same

## Error Recovery

Searching shopping sites involves many things that can go wrong. Handle them gracefully instead of retrying blindly.

### CAPTCHA / Anti-Bot Detection
Shopping platforms aggressively block automation. If you encounter a CAPTCHA, access-denied page, or unusual redirect:
1. **Stop immediately** — do NOT retry in a loop (this wastes tokens and may trigger harder blocks)
2. Inform the user: "Amazon is showing a CAPTCHA. I can't proceed automatically."
3. Suggest alternatives: user can solve the CAPTCHA manually, or try a different search keyword, or try again later

### Search Returns 0 Results
1. Try 2 alternative keyword combinations (broader terms, different language, different word order)
2. If still 0 results, report to user with the keywords tried — the product category may not exist on this platform

### Database Errors
- **SQLITE_BUSY** (another process is using the DB): the script includes a 5-second built-in wait (`busy_timeout`). If you still see this error during Step 4 parallel extraction, do NOT create a new DB — retry once after 5 seconds. Only create a new DB if the error persists outside of parallel extraction (e.g., during initial setup).
- **Corrupt DB**: if any DB operation throws `sqlite3.DatabaseError`, skip that DB in discovery and inform the user. Don't crash the entire workflow.

### agent-browser Failures
- If `agent-browser` crashes or times out, try once more. If it fails again, close the browser (`agent-browser close`) and inform the user.
- If the platform page doesn't load (timeout, network error), skip that product and move to the next candidate. Don't block the entire search on one product.
