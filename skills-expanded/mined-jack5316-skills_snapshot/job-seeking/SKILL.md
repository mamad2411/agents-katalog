---
name: job-seeking
description: Aggregate latest job listings from V2EX 酷工作 and RemoteOK for China job search. Use when user asks for job digest, job listings, 招聘, 找工作, or /job-seeking.
---

# Job Seeking Skill (/job-seeking)

Grab the latest job-related information from multiple platforms and curate into an Obsidian digest. Optimized for job seeking in China.

## Sources

| Platform | Focus | API |
|----------|-------|-----|
| **V2EX 酷工作** | Tech community job postings (China) | Free public API |
| **RemoteOK** | Global remote jobs (includes China-remote) | Free public API |

## Quick Start

```bash
python3 _scripts/job_seeking.py
```

## Options

- `--v2ex-only`: Fetch only V2EX 酷工作
- `--remoteok-only`: Fetch only RemoteOK
- `--keywords Python 北京`: Filter by keywords (overrides job_keywords.txt)
- `--limit-v2ex N`: Max V2EX jobs (default: 25)
- `--limit-remoteok N`: Max RemoteOK jobs (default: 15)
- `--no-save`: Print only, do not save to vault
- `--no-ai`: Skip AI digest, raw listing only

## Configuration

Edit `_scripts/job_keywords.txt` to filter jobs by keywords (one per line):

```
# Examples
Python
北京
Shanghai
后端
AI
远程
```

Leave empty to show all listings.

## Examples

```bash
# Full digest (V2EX + RemoteOK)
python3 _scripts/job_seeking.py

# China tech only
python3 _scripts/job_seeking.py --keywords Python 北京 上海

# V2EX only (most China-relevant)
python3 _scripts/job_seeking.py --v2ex-only

# Preview without saving
python3 _scripts/job_seeking.py --no-save
```

## Output

- **Saved note**: `Sources/Job Digest - YYYY-MM-DD.md`
- **Content**: Raw listings table + AI-curated digest (categories, China-relevant highlights, actionable notes)
- **Tags**: `source/jobs`, `job-seeking`, `china`

## Extending

To add more platforms (e.g., Lagou, 51job, BOSS直聘), you would need:
- API access or scraping logic
- Rate limiting and respectful request delays
- Update `job_seeking.py` with new fetch functions
