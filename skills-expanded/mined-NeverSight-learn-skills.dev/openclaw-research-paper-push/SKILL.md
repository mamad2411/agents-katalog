---
name: openclaw-research-paper-push-skill
description: Schedule automated research paper alerts from OpenAlex with daily Chinese summaries using OpenClaw cron
triggers:
  - set up automated paper alerts for my research topics
  - monitor new publications in neuroimaging journals
  - create a daily digest of Alzheimer's research papers
  - schedule OpenAlex paper notifications
  - track new papers on dynamic functional connectivity
  - get daily summaries of research papers in Chinese
  - set up cron job for academic paper monitoring
  - subscribe to journal alerts for fMRI studies
---

# OpenClaw Research Paper Push Skill

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

An OpenClaw AgentSkill that creates scheduled research paper alerts using OpenAlex API and OpenClaw's cron functionality. Monitors journals, conferences, and topics, then generates concise daily Chinese summaries of newly published papers.

## What it does

- **Scheduled monitoring**: Create cron-based subscriptions for research topics and venues
- **OpenAlex integration**: Query real academic papers without API key requirements
- **Smart filtering**: Match papers by research topics, journal names, or conferences
- **Deduplication**: Track papers by DOI, OpenAlex ID, or title to avoid duplicates
- **State management**: Persist `last_checked` timestamps locally
- **Chinese summaries**: Generate daily digests with title, authors, venue, date, link, matched topics, and relevance scores

## Installation

This is an OpenClaw AgentSkill. Install via ClawHub:

```bash
clawhub install research-paper-push
```

Or clone the repository:

```bash
git clone https://github.com/ZJunCher/openclaw-research-paper-push-skill.git
cd openclaw-research-paper-push-skill
```

## Requirements

- OpenClaw with AgentSkill and cron support
- Python 3.x
- Internet access for OpenAlex API
- Optional: `curl` for environments without Python HTTPS support
- Optional: Set `OPENALEX_MAILTO` environment variable for polite API usage

```bash
export OPENALEX_MAILTO="your-email@example.com"
```

## Core script

All functionality is in `scripts/manage_papers.py`. Available commands:

- `add` - Create a new subscription
- `list` - Show all subscriptions
- `update` - Modify an existing subscription
- `remove` - Delete a subscription
- `test` - Run a test query against OpenAlex
- `run` - Execute a saved subscription immediately

## Creating subscriptions

### Basic subscription

```bash
python scripts/manage_papers.py add \
  --to "<recipient-id>" \
  --time "09:00" \
  --timezone "Asia/Shanghai" \
  --journals "NeuroImage,Medical Image Analysis,IEEE TMI" \
  --topics "Alzheimer,MCI,dynamic functional connectivity"
```

### Multi-topic subscription

```bash
python scripts/manage_papers.py add \
  --to "<recipient-id>" \
  --time "08:30" \
  --timezone "UTC" \
  --journals "Nature Neuroscience,Human Brain Mapping,Cerebral Cortex" \
  --topics "graph neural network,rs-fMRI,fMRI,brain networks,neuroimaging"
```

### Parameters

- `--to`: Recipient identifier for OpenClaw notification
- `--time`: Daily execution time (HH:MM format)
- `--timezone`: Timezone for scheduling (e.g., "Asia/Shanghai", "America/New_York", "UTC")
- `--journals`: Comma-separated journal/venue names (partial matching supported)
- `--topics`: Comma-separated research topics for filtering

## Managing subscriptions

### List all subscriptions

```bash
python scripts/manage_papers.py list
```

Output shows subscription ID, recipient, schedule, journals, and topics.

### Update a subscription

```bash
python scripts/manage_papers.py update \
  --id "1" \
  --time "10:00" \
  --journals "NeuroImage,Brain" \
  --topics "Alzheimer,connectivity,fMRI"
```

### Remove a subscription

```bash
python scripts/manage_papers.py remove --id "1"
```

## Testing queries

Before creating a subscription, test your filters:

```bash
python scripts/manage_papers.py test \
  --since "2026-01-01" \
  --limit 10 \
  --journals "NeuroImage,Human Brain Mapping" \
  --topics "Alzheimer,MCI,dynamic functional connectivity,rs-fMRI"
```

### Test parameters

- `--since`: Start date for paper search (YYYY-MM-DD format)
- `--limit`: Maximum number of results to return
- `--journals`: Same as subscription
- `--topics`: Same as subscription

The test command performs a real OpenAlex query and shows how many papers match your criteria.

## Running subscriptions manually

Execute a saved subscription on demand:

```bash
python scripts/manage_papers.py run --id "1" --limit 10
```

This is useful for:
- Testing subscription output before scheduling
- Backfilling papers since last check
- Debugging filter criteria

## OpenAlex query patterns

The skill queries OpenAlex with:

```python
# Date-based filtering
from_publication_date = "YYYY-MM-DD"

# Full-text search for topics
search = "Alzheimer OR MCI OR dynamic functional connectivity"

# Venue filtering
filter = "primary_location.source.display_name:NeuroImage OR primary_location.source.display_name:Medical Image Analysis"

# Sorting by publication date (newest first)
sort = "publication_date:desc"

# Pagination
per_page = 100
```

## Data storage

Local subscription state is stored in:

```
data/
  subscriptions.json   # All subscription configs
  paper_history.json   # Deduplication tracking
  last_checked.json    # Timestamp state
```

**Important**: Do not commit `data/*.json` files to version control. Add to `.gitignore`:

```gitignore
data/*.json
```

## Common patterns

### Monitoring specific research areas

```bash
# AD/MCI neuroimaging
python scripts/manage_papers.py add \
  --to "<recipient-id>" \
  --time "09:00" \
  --timezone "Asia/Shanghai" \
  --journals "NeuroImage,Alzheimer's & Dementia,Brain" \
  --topics "Alzheimer,mild cognitive impairment,amyloid,tau,neurodegeneration"

# Graph neural networks for brain analysis
python scripts/manage_papers.py add \
  --to "<recipient-id>" \
  --time "09:00" \
  --timezone "Asia/Shanghai" \
  --journals "Medical Image Analysis,IEEE TPAMI,NeuroImage" \
  --topics "graph neural network,brain network,connectome,graph learning"
```

### Conference paper tracking

```bash
python scripts/manage_papers.py add \
  --to "<recipient-id>" \
  --time "09:00" \
  --timezone "America/New_York" \
  --journals "MICCAI,CVPR,NeurIPS,ICCV" \
  --topics "medical image analysis,brain segmentation,registration"
```

### Weekly digest pattern

For less frequent updates, use the `run` command via external cron:

```bash
# In system crontab: Run every Monday at 9 AM
0 9 * * 1 cd /path/to/skill && python scripts/manage_papers.py run --id "1" --limit 50
```

## Output format

The skill generates Chinese summaries with:

- **标题** (Title): Paper title
- **作者** (Authors): Author list
- **期刊/会议** (Venue): Publication venue
- **发表日期** (Date): Publication date
- **链接** (Link): DOI or OpenAlex URL
- **匹配主题** (Matched topics): Which subscription topics matched
- **相关度** (Relevance): Match count or score

Example output structure:

```
### 论文1
- 标题: Dynamic Functional Connectivity in Alzheimer's Disease
- 作者: Zhang A, Li B, Wang C
- 期刊: NeuroImage
- 发表日期: 2026-05-10
- 链接: https://doi.org/10.1016/...
- 匹配主题: Alzheimer, dynamic functional connectivity
- 相关度: 2/5
```

## Troubleshooting

### No papers returned

- **Check date range**: OpenAlex may have indexing delays. Use `--since` a few days earlier.
- **Verify journal names**: Use exact or partial names as they appear in OpenAlex (e.g., "NeuroImage" not "Neuroimage").
- **Broaden topics**: Try fewer or more general search terms.

### HTTPS/SSL errors

If running in embedded Python without HTTPS:

```bash
# The script falls back to curl automatically
# Ensure curl is available:
which curl
```

### Rate limiting

OpenAlex is generous but set polite headers:

```bash
export OPENALEX_MAILTO="your-email@example.com"
```

The script automatically adds a User-Agent and respects rate limits.

### Duplicate papers

The skill tracks papers by:
1. DOI (primary)
2. OpenAlex ID (secondary)
3. Title hash (fallback)

If duplicates appear, check `data/paper_history.json` for state corruption.

### Subscription not running

Verify OpenClaw cron is active:

```bash
# Check OpenClaw cron status
openclaw cron status

# Manually trigger
python scripts/manage_papers.py run --id "1"
```

## Advanced usage

### Custom date ranges

```bash
# Last 7 days
python scripts/manage_papers.py test \
  --since "$(date -d '7 days ago' +%Y-%m-%d)" \
  --limit 20 \
  --journals "Nature,Science" \
  --topics "neuroimaging"
```

### Combining multiple subscriptions

Create separate subscriptions for different research areas:

```bash
# Subscription 1: Alzheimer's research
python scripts/manage_papers.py add --to "<recipient-1>" --time "09:00" --journals "..." --topics "Alzheimer,MCI"

# Subscription 2: Deep learning methods
python scripts/manage_papers.py add --to "<recipient-2>" --time "10:00" --journals "..." --topics "deep learning,CNN,transformer"
```

### Filtering by publication type

OpenAlex returns all types by default. For articles only, the script focuses on papers with DOIs and publication dates.

## Integration with OpenClaw workflows

This skill is designed for OpenClaw's AgentSkill ecosystem. Once installed:

1. OpenClaw cron manager schedules subscriptions
2. At scheduled time, the skill queries OpenAlex
3. Results are filtered and deduplicated
4. Chinese summary is generated
5. Notification is sent to recipient via OpenClaw messaging

## Contributing

Repository: https://github.com/ZJunCher/openclaw-research-paper-push-skill

Report issues or suggest improvements via GitHub Issues.

## License

MIT-0 — Free to use, modify, and distribute.
