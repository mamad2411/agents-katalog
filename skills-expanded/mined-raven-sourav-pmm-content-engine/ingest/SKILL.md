# Skill: Ingest New Content

## Trigger
User provides new posts, writer content, URLs, or newsletter URLs to add to the system.

## Process

### For new user posts
1. Read the .docx or text content
2. Analyze for voice patterns, new mental models, topic evolution
3. Update `data/brain/pmm_brain.json` voice profile if needed
4. Store in ChromaDB for gap map retrieval

### For new reference writer content
1. Read the .docx, URL, or text content
2. Analyze for mental models, argumentation patterns, thinking process
3. Update the PMM Brain's synthesized models if new patterns found
4. Store in ChromaDB for gap map retrieval

### For newsletter/blog URLs
1. Fetch and read the content via WebFetch
2. Extract writer identity, key themes, mental models, unique perspectives
3. Add to `newsletter_insights` section of the Brain
4. Note any new emerging beliefs for the value landscape

### For newsletter scraping (Substack / Beehiiv)

When user provides a newsletter URL for scraping (e.g., "scrape this newsletter", "ingest posts from https://..."):

1. **Scrape** — Run the newsletter scraper to pull posts:
   ```bash
   python3 -m src.ingestion.newsletter_scraper \
     --url "https://newsletter-url.com" \
     --days 90 --full-content
   ```
   This auto-detects the platform (Substack or Beehiiv), scrapes posts,
   stores them in SQLite + ChromaDB, and saves raw JSON to `data/scraped/`.

2. **Generate brain brief** — Get the synthesis brief:
   ```bash
   python3 -m src.ingestion.newsletter_scraper \
     --url "https://newsletter-url.com" \
     --days 90 --full-content --output brain-brief
   ```

3. **Synthesize into Brain** — Read the brain brief and update `data/brain/pmm_brain.json`:
   - `newsletter_insights`: Add/update entry with focus, key_frameworks, key_data_points, contrarian_insights, useful_for
   - `evidence_bank`: Extract concrete stats, benchmarks, data points
   - `pmm_value_landscape`: Note contested or emerging beliefs
   - `synthesized_mental_models`: Extract new mental models or frameworks
   - `topic_depth_layers`: Add practitioner wisdom, common mistakes, key debates

4. **Verify** — Confirm what was added to each Brain section.

#### CLI flags
| Flag | Description |
|------|-------------|
| `--url` | Newsletter URL (required) |
| `--name` | Source name (auto-detected from author if omitted) |
| `--days N` | Only scrape last N days |
| `--max-posts N` | Limit total posts |
| `--keywords "a,b"` | Filter by keywords |
| `--full-content` | Fetch full post bodies (slower, richer for synthesis) |
| `--no-store` | Skip SQLite/ChromaDB storage, just preview |
| `--output` | `summary` (default), `json`, or `brain-brief` |

#### Supported platforms
- **Substack** — uses public `/api/v1/archive` JSON endpoint
- **Beehiiv** — uses hidden `/posts` JSON endpoint
- Both work with custom domains (auto-detected)

### For visual illustrations
1. Read images to understand visual style
2. Update visual signature in voice profile if patterns have evolved

## Data Flow

```
Newsletter URL
  → newsletter_scraper.py (detect platform → scrape → filter)
  → data/scraped/{source}_{timestamp}.json (audit trail)
  → SQLite posts table + ChromaDB embeddings (retrieval)
  → Brain synthesis brief (for Claude analysis)
  → pmm_brain.json updates (newsletter_insights, evidence_bank, etc.)
```

## Output
Confirm what was ingested and what changed in the Brain.
