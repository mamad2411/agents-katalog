---
name: pagerangers-seo
description: "Use when working with ANY PageRangers or SEO ranking operation — keyword analysis, SERP data, search volume, competition metrics, ranking positions, KPIs, or keyword opportunities via PageRangers API."
license: "(MIT AND CC-BY-SA-4.0). See LICENSE-MIT and LICENSE-CC-BY-SA-4.0"
compatibility: "Requires python3, uv. PageRangers API credentials."
metadata:
  author: Netresearch DTT GmbH
  version: "1.1.0"
  repository: https://github.com/netresearch/pagerangers-skill
allowed-tools: Bash(python3:*) Bash(uv:*) Read
---

# PageRangers SEO

Query the PageRangers Monitoring API for SEO insights directly from your AI assistant.

## Commands

| Command | Description |
|---------|-------------|
| `keyword <term>` | Analyze a keyword (SERP, volume, competition) |
| `rankings` | List current keyword rankings |
| `kpis` | Get project KPIs (ranking index, top 10/100) |
| `prospects` | Find high-opportunity keywords |

## Quick Start

```bash
# 1. Create credentials file (see references/setup.md for details)
cat > ~/.env.pagerangers << 'EOF'
PAGERANGERS_API_TOKEN=your_api_key_here
PAGERANGERS_PROJECT_HASH=your_project_hash_here
EOF

# 2. Run commands (global flags like --json go BEFORE the subcommand)
python3 scripts/pagerangers.py --json keyword "SEO Analyse" --top 5
python3 scripts/pagerangers.py --json rankings --limit 10
python3 scripts/pagerangers.py --json kpis
python3 scripts/pagerangers.py --json prospects --limit 10
```

## Usage Examples

### Keyword Analysis

```bash
python3 scripts/pagerangers.py --json keyword "online marketing" --top 10
```

Returns: keyword, search volume, competition (low/medium/high), top URLs, related keywords.

### Project Rankings

```bash
python3 scripts/pagerangers.py --json rankings --limit 20
```

Returns: keyword, position, ranking URL.

### Project KPIs

```bash
python3 scripts/pagerangers.py --json kpis
```

Returns: ranking index, top 10 count, top 100 count, average position.

### Keyword Opportunities

```bash
python3 scripts/pagerangers.py --json prospects --limit 10
```

Returns: keywords with best ranking potential.

## References

| Topic | Reference |
|-------|-----------|
| API documentation | `references/pagerangers-api.md` |
| Endpoint configuration | `references/pagerangers-api.json` |
| Setup and credentials | `references/setup.md` |
| Error handling | `references/error-handling.md` |
| Module distinction (Monitoring vs Explorer) | `references/module-distinction.md` |
| API costs and credits | `references/api-costs.md` |
| CLI implementation | `scripts/pagerangers.py` |
