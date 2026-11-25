---
name: job-scraper-pipeline
description: Automated ML/AI job scraping, deduplication, and gatekeeper scoring pipeline. Scrapes AI company career pages on Greenhouse, AshbyHQ, and Lever, avoids duplicates, and scores jobs 0-100 against profile keywords, classifying tier-1/2/3.
triggers:
  - cron job: job scraper and gatekeeper pipeline
  - scrape AI/ML jobs
  - job hunt queue management
---

# Job Scraper + Gatekeeper Pipeline

Automated job scraping, deduplication, and gatekeeper scoring for ML/AI job hunting.

## When to Use
- Cron job that scrapes AI company career pages on Greenhouse, AshbyHQ, and Lever
- Runs on a schedule (e.g. every 15m, 6h, or daily)
- Appends new jobs to the queue file
- Scores pending jobs against profile keywords

## Configuration

All PII, paths, and scoring keywords live in `profile.yaml` at the repo root. Copy `profile.yaml.example` to `profile.yaml` and edit. Keys this skill reads:

- `paths.queue` — queue JSON location (default `~/hermes-merchant/state/queue/jobs.json`)
- `paths.scraper_log` — log file
- `scoring.required_keywords`, `scoring.adjacent_roles`, `scoring.reject_keywords`, `scoring.ai_companies`, `scoring.tiers`

Minimal loader (Python):

```python
import yaml, os
from pathlib import Path

cfg = yaml.safe_load(Path("profile.yaml").read_text())
queue_path = Path(os.path.expanduser(cfg["paths"]["queue"]))
queue_path.parent.mkdir(parents=True, exist_ok=True)
```

## Scraping Strategy

### Sources — What Works / What Doesn't

| Source | Method | Status | Notes |
|--------|--------|--------|-------|
| Naukri.com | browser_navigate | Blocked | Search results require JS rendering; homepage loads but listings aren't accessible. |
| Indeed.com | browser_navigate | Blocked by Cloudflare | "Additional Verification Required"; cannot bypass without residential proxies. |
| **Together AI** | Browser → `https://job-boards.greenhouse.io/togetherai` | Works | Greenhouse format — use the JS snippet below to extract all jobs. |
| **Cohere** | Browser → `https://jobs.ashbyhq.com/cohere` | Works (~100+ roles) | AshbyHQ — largest pipeline source. Departments include Agentic Platform, Modeling, Applied-ML, Inference, Model Serving. |
| Baseten | Browser → `https://jobs.ashbyhq.com/baseten` | Works | AshbyHQ. Many roles previously bounced on email — prefer web form. |
| **Modal Labs** | Browser → `https://www.modal.com/careers` | Works (~24 roles) | AshbyHQ embedded on page — scroll to see listings. |
| **Cerebras** | Browser → `https://www.cerebras.ai/join-us` → click ML dept | Works | Greenhouse-based, limited ML roles. |
| **Mistral AI** | Browser → `https://jobs.lever.co/mistral` | Works | Lever ATS — do NOT add query params; go direct and filter in-page. |
| LangChain | Browser → `https://jobs.ashbyhq.com/langchain` | Works | AshbyHQ; iframe on their own careers page — go direct. |
| **Pinecone** | Browser → `https://www.pinecone.io/careers` | Works | AshbyHQ-hosted, JS console extraction works. |
| **Groq** | Browser → `https://www.groq.com/careers/` | Moved | All engineering roles now on an external ATS (Gem.com). |
| Hugging Face | Browser → `https://huggingface.co/jobs` | Login-gated | Requires auth to view. |
| **Anthropic** | Browser → `https://job-boards.greenhouse.io/anthropic` | Works partially | Greenhouse — some listings require a second fetch. |
| Qdrant | Browser | Blocked | `careers.qdrant.tech` resolves to a private network. |

### ATS Platform Taxonomy

Three ATS platforms dominate AI company career pages. Each wants a different scraping approach:

| ATS | URL Pattern | Best Method |
|-----|-------------|-------------|
| **Greenhouse** | `job-boards.greenhouse.io/{company}` | `browser_navigate` → `browser_console` JS snippet |
| **AshbyHQ** | `jobs.ashbyhq.com/{company}` | `browser_navigate` → `browser_snapshot` |
| **Lever** | `jobs.lever.co/{company}` | `browser_navigate` → `browser_snapshot` (no query params) |

Known Greenhouse: Anthropic, Together AI, Cerebras.
Known AshbyHQ: Cohere, Baseten, LangChain, Modal, Pinecone.
Known Lever: Mistral AI.

### Greenhouse Job Extraction

Many AI companies host on Greenhouse at `https://job-boards.greenhouse.io/{company}`.

JavaScript snippet to extract ALL job links from a Greenhouse page (run via `browser_console`):

```javascript
"use strict"; (() => {
  const links = document.querySelectorAll('a[href*="/jobs/"]');
  const seen = new Set();
  return Array.from(links)
    .filter(l => l.href && !seen.has(l.href) && seen.add(l.href))
    .map(l => l.href + '\t' + l.textContent.trim())
    .join('\n');
})()
```

Returns a newline-separated list of `URL\tJob Title` pairs. Greenhouse pages load all jobs on one page — no pagination.

### web_extract is unreliable for job scraping

- `web_extract` frequently fails with `409 BILLING_ERROR` on job-heavy targets (Naukri, Indeed, Anthropic, Cohere, Mistral, Together AI, Groq, LangChain, Baseten).
- `web_search` is the working fallback — it returns titles, descriptions, and listing URLs from search-engine indexes. Use it to discover individual job-listing URLs.
- **Parallel `web_search` calls hit 409** — always run sequentially.
- **Fallback chain when `web_extract` fails:**
  1. `web_search` first (sequentially) to discover URLs.
  2. If `web_extract` fails (409/504), use search-result snippets as job data — they contain title, company, and location.
  3. For career pages, use `browser_navigate` directly to the ATS URL.

### Indeed / Naukri

- **Indeed**: blocked by Cloudflare. `site:indeed.com` `web_search` queries sometimes return snippet data with enough info (title, company, location) to score.
- **Naukri**: some LLM/GenAI index pages (e.g. `naukri.com/llm-engineer-jobs-16`) extract successfully via `web_extract`; search pages don't.

## Gatekeeper Scoring

Load thresholds and keyword lists from `profile.yaml`:

```python
tiers = cfg["scoring"]["tiers"]
required = cfg["scoring"]["required_keywords"]
adjacent = cfg["scoring"]["adjacent_roles"]
reject   = cfg["scoring"]["reject_keywords"]
ai_cos   = set(cfg["scoring"]["ai_companies"])
```

### Tier Thresholds

- **Tier 1**: `score >= tiers.tier_1` (default 75) → tailor resume, apply immediately.
- **Tier 2**: `tiers.tier_2 <= score < tiers.tier_1` → generic or light tailoring.
- **Tier 3**: below `tiers.tier_2` → skip unless specifically interested.

### Scoring Logic

```python
def score_job(title, location="", source="", cfg=None):
    text = f"{title} {location}".lower()
    score = 0
    matched = []

    core_roles = [
        "machine learning engineer", "ml engineer", "ai engineer",
        "generative ai engineer", "rag engineer", "llm engineer",
    ]
    for role in core_roles:
        if role in text:
            score += 40
            matched.append(role)

    for kw in cfg["scoring"]["required_keywords"]:
        if kw.lower() in text:
            score += 10
            matched.append(kw)

    for adj in cfg["scoring"]["adjacent_roles"]:
        if adj.lower() in text:
            score += 10

    high_value = [
        "llm", "rag", "generative ai", "genai", "agentic", "nlp",
        "deep learning", "fine-tuning", "rlhf", "multimodal",
        "foundation model", "transformer", "post-training",
        "model serving", "vector db", "embeddings",
    ]
    for hw in high_value:
        if hw in text:
            score += 5

    company_key = source.lower().strip()
    if company_key in {c.lower() for c in cfg["scoring"]["ai_companies"]}:
        has_ai  = any(kw.lower() in text for kw in cfg["scoring"]["required_keywords"])
        has_adj = any(adj.lower() in text for adj in cfg["scoring"]["adjacent_roles"])
        if not has_ai and has_adj:
            score += 15
        elif has_ai or has_adj:
            score += 5

    for rk in cfg["scoring"]["reject_keywords"]:
        if rk.lower() in text:
            score -= 15

    score = max(0, min(100, score))
    t = cfg["scoring"]["tiers"]
    tier = "tier-1" if score >= t["tier_1"] else ("tier-2" if score >= t["tier_2"] else "tier-3")
    return score, tier, matched
```

### AI companies use generic SWE titles

Cohere, Baseten, Modal, and friends use generic titles like "Member of Technical Staff", "Forward Deployed Engineer", or "Agentic Platform". These score low without the AI-company context bonus because the title doesn't contain explicit ML keywords.

Roles like "Forward Deployed Engineer, Agentic Platform" (Cohere) score 0 by title alone. Include `agentic`, `post-training`, `inference`, `forward deployed`, `prompt specialist`, `applied researcher`, `research engineer`, `ml researcher`, `ai researcher`, `reinforcement learning`, `rlhf`, and `agent` in either `adjacent_roles` or `required_keywords` to catch them.

### Reject keyword false positives

"Research Engineer" contains "engineer" but is NOT a reject. Reject logic should only trigger on exact matches like "java developer" or "react developer" — not any string containing "developer".

## Job Data Shape

```json
{
  "url": "https://jobs.ashbyhq.com/cohere/...",
  "source": "cohere",
  "title": "Forward Deployed Engineer, Agentic Platform",
  "company": "Cohere",
  "location": "Toronto; New York",
  "experience": "Not specified",
  "score": 35,
  "tier": "tier-2",
  "matched_keywords": [],
  "scraped_at": "2026-04-19T17:35:45+00:00",
  "status": "pending"
}
```

## Status Values

- `pending` — in queue, not yet applied.
- `applied` — successfully applied via web form.
- `applied_email` — applied via email.
- `failed` — application attempt failed; include `failure_reason` and `manual_apply_url`.
- `blocked` — known blocker (visa, experience mismatch, etc.).

## Deduplication

Before appending, compute `existing_urls = {j["url"] for j in queue}` and skip URLs already present.

## Known Gotchas

- **f-string + dict access**: `f"score={j['score']}"` with nested dict access confuses older Python parsers. Use string concatenation or `.format()`.
- **Tuple unpacking**: if `score_job` returns `(score, tier, matched)`, unpack all three at every call site.
- **Parallel web calls**: `web_search` / `web_extract` in parallel reliably hits `409 BILLING_ERROR`. Run sequentially.
- **LangChain Ashby**: the jobs board is iframed on the careers page. Go direct to `https://jobs.ashbyhq.com/langchain` — don't try to scrape the embed.
- **Mistral Lever**: times out in browser without residential proxies on some networks. Mark blocked and move on.
