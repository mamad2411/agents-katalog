---
name: geo-brand-mentions
description: "Brand authority scan across the platforms AI models lean on for entity recognition (YouTube, Reddit, Wikipedia and Wikidata, LinkedIn, and others), producing a weighted Brand Authority Score (0-100), sentiment, and per-platform recommendations. Use when the user asks whether AI assistants know or recommend a brand, or wants off-site authority work that improves AI citations."
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
  - Write
---

# Brand Mention Scanner Skill

## Core Insight

Brand mentions correlate ~3x more strongly with AI visibility than traditional backlinks (Ahrefs, Dec 2025, 75K brands). **Unlinked brand mentions** predict AI citation better than Domain Rating or backlink count, and **the platform matters enormously** — a YouTube/Reddit mention outweighs a DR 70 dofollow link, because AI training data and retrieval disproportionately index high-engagement platforms.

This inverts traditional SEO: the signals that matter most for AI visibility (YouTube, Reddit) are nearly irrelevant in classic SEO, and vice versa.

---

## Composite Brand Authority Score

### Scoring Formula

| Platform | Weight | Rationale |
|---|---|---|
| YouTube Presence | 25% | Strongest correlation with AI citation (0.737) |
| Reddit Presence | 25% | Second strongest; critical for product recommendations |
| Wikipedia / Wikidata | 20% | Entity recognition foundation; AI training data cornerstone |
| LinkedIn Authority | 15% | Professional authority signals; B2B relevance |
| Other Platforms | 15% | Supplementary: Quora, GitHub, news, forums, podcasts |

**Formula:**
```
Brand_Authority_Score = (YouTube * 0.25) + (Reddit * 0.25) + (Wikipedia * 0.20) + (LinkedIn * 0.15) + (Other * 0.15)
```

### Score Interpretation

| Score Range | Rating | Interpretation |
|---|---|---|
| 85-100 | Dominant | Well-recognized entity across AI platforms. Highly likely to be cited and recommended. |
| 70-84 | Strong | Solid cross-platform presence. AI likely recognizes and cites for relevant queries. |
| 50-69 | Moderate | Presence on some platforms but gaps exist. AI citation is inconsistent. |
| 30-49 | Weak | Limited platform presence. AI may not recognize as a distinct entity. |
| 0-29 | Minimal | Negligible presence. AI unlikely to cite or recommend. |

For per-platform 0-100 rubrics, why each platform matters, and what to check on each — see **`platforms.md`**.

---

## Analysis Procedure

### Step 1: Identify Brand Information

Gather from the user or the website:
- **Brand name** (exact spelling + official variants)
- **Founder/CEO name(s)**
- **Domain URL**
- **Industry/category**
- **Key products or services** (top 3)
- **Key competitors** (for comparison context)

### Step 2: Platform Scanning

For each platform, use WebFetch to search and assess presence.

**YouTube Check:**
1. Search: `[brand name] site:youtube.com`
2. Check: `youtube.com/@[brand-name]` or `youtube.com/c/[brand-name]` for official channel
3. Search: `"[brand name]" site:youtube.com` (exact match for mentions in descriptions)
4. Note: Channel subscriber count, video count, latest upload date, third-party mention count

**Reddit Check:**
1. Search: `[brand name] site:reddit.com`
2. Search: `"[brand name]" site:reddit.com` (exact match)
3. Check: `reddit.com/r/[brand-name]` for official subreddit
4. Check: `reddit.com/user/[brand-name]` for official account
5. Note: Thread count, dominant subreddits, sentiment (positive/negative/neutral), recommendation frequency

**Wikipedia Check (IMPORTANT — use BOTH methods to avoid false negatives):**

**Method 1 — Python API check (MOST RELIABLE, do this FIRST):**
```bash
python3 -c "
import requests, json
from urllib.parse import quote_plus
brand = '[Brand_Name]'
# Check Wikipedia API directly
api_url = f'https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={quote_plus(brand)}&format=json'
r = requests.get(api_url, headers={'User-Agent': 'GEO-Audit/1.0'}, timeout=15)
data = r.json()
results = data.get('query', {}).get('search', [])
if results and brand.lower() in results[0].get('title', '').lower():
    print(f'WIKIPEDIA PAGE EXISTS: {results[0][\"title\"]}')
    print(f'URL: https://en.wikipedia.org/wiki/{results[0][\"title\"].replace(\" \", \"_\")}')
else:
    print('No direct Wikipedia page found')
# Check Wikidata
wd_url = f'https://www.wikidata.org/w/api.php?action=wbsearchentities&search={quote_plus(brand)}&language=en&format=json'
r2 = requests.get(wd_url, headers={'User-Agent': 'GEO-Audit/1.0'}, timeout=15)
wd = r2.json()
entities = wd.get('search', [])
if entities:
    print(f'WIKIDATA ENTRY: {entities[0].get(\"id\", \"\")} — {entities[0].get(\"description\", \"\")}')
"
```

**Method 2 — Direct URL check (backup verification):**
1. WebFetch: `https://en.wikipedia.org/wiki/[Brand_Name]` — check if page loads (not redirect to search)
2. WebFetch: `https://en.wikipedia.org/wiki/[Founder_Name]` for founder article

**Method 3 — Search (least reliable, supplemental only):**
1. Search: `[brand name] site:wikipedia.org`
2. Search: `[brand name] site:wikidata.org`

**CRITICAL:** Web search alone is NOT reliable for determining Wikipedia presence. ALWAYS run the Python API check first. If the API says a page exists, it exists — do not override with a search result that fails to find it.

5. Note: Article existence, quality, edit history, Wikidata completeness

**LinkedIn Check:**
1. Search: `[brand name] site:linkedin.com`
2. Check: `linkedin.com/company/[brand-name]` for company page
3. Note: Follower count, post frequency, employee count listed, engagement levels

**Other Platforms:**
1. Search: `[brand name] site:quora.com`
2. Search: `[brand name] site:stackoverflow.com` (if technical brand)
3. Search: `[brand name] site:github.com` (if technical brand)
4. Search: `[brand name] site:news.ycombinator.com` (Hacker News)
5. Search: `"[brand name]"` broadly for news mentions (filter to last 6 months)
6. Note: Presence/absence and quality of mentions on each platform

### Step 3: Sentiment Assessment

For Reddit and discussion platforms, assess sentiment from the most recent and most prominent mentions. Use the sentiment indicator table in `platforms.md` (Positive / Neutral / Negative / Mixed).

### Step 4: Competitive Comparison (Optional)

If competitors are identified, do a quick scan of their platform presence for context. A brand with "moderate" Reddit presence in an industry where competitors have zero Reddit presence is relatively strong — context calibrates the score.

### Step 5: Score Calculation

1. Score each platform (0-100) using the rubrics in `platforms.md`.
2. Apply weights to compute the composite Brand Authority Score.
3. Identify the strongest and weakest platforms.
4. Generate specific, actionable recommendations for the weakest platforms — use the platform-specific quick-wins list in `platforms.md`.

---

## Output

Write a file named `GEO-BRAND-MENTIONS.md` using the exact template in **`templates.md`** (report header, platform breakdown table, per-platform detail blocks, recommendations by horizon, optional competitive table, key takeaway).
