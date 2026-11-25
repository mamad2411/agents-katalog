# Amazon Product Research Skill

Automated Amazon Best Sellers category analysis for e-commerce product research and selection decisions.

## Overview

This skill helps you:

- **Analyze entire categories** for market entry decisions
- **Find black horse products** (high potential, low competition)
- **Research competitors** and their strategies
- **Get AI-powered recommendations** for product selection

## Installation

### Using install.sh (Recommended)

```bash
chmod +x install.sh
./install.sh              # Auto-detect platform
./install.sh claude       # Claude Code
./install.sh copilot      # GitHub Copilot
./install.sh cursor       # Cursor
```

### Manual Installation

| Platform | Copy to |
|----------|---------|
| Claude Code | `~/.claude/skills/amazon-product-research-skill/` |
| GitHub Copilot | `.github/skills/amazon-product-research-skill/` |
| Cursor | `.cursor/rules/amazon-product-research-skill/` |
| Windsurf | `.windsurf/skills/amazon-product-research-skill/` |
| Cline | `.clinerules/amazon-product-research-skill/` |
| Codex CLI | `.codex/skills/amazon-product-research-skill/` |
| Gemini CLI | `.gemini/skills/amazon-product-research-skill/` |

## Prerequisites

1. **Apify Account** (Free tier available)
   - Sign up at https://apify.com
   - Get API token at https://console.apify.com/account/integrations

2. **OpenAI Account** (Optional, for AI analysis)
   - Sign up at https://platform.openai.com
   - Get API key at https://platform.openai.com/api-keys

3. **Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Set environment variables:

```bash
# Required
export APIFY_API_TOKEN="your_apify_token"

# Optional (for AI analysis)
export OPENAI_API_KEY="your_openai_key"
```

Add to your shell profile for persistence:

```bash
echo 'export APIFY_API_TOKEN="your_token"' >> ~/.bashrc
echo 'export OPENAI_API_KEY="your_key"' >> ~/.bashrc
source ~/.bashrc
```

## Usage

### Quick Start

```bash
# Analyze a category
/amazon-product-research Analyze https://www.amazon.com/Best-Sellers-Portable-Changing-Pads

# Find black horse products
/amazon-product-research Find black horses in electronics

# Get AI recommendations
/amazon-product-research Generate market entry report for baby products
```

### Command Line Usage

#### Complete Category Analysis

```bash
python3 scripts/analyze_category.py \
  --category-url "https://www.amazon.com/Best-Sellers-Electronics/zgbs/electronics" \
  --output-format markdown \
  --include-ai-analysis
```

#### Black Horse Discovery

```bash
python3 scripts/find_black_horses.py \
  --category-url "https://www.amazon.com/Best-Sellers-Electronics/zgbs/electronics" \
  --min-potential-score 1.0 \
  --max-reviews 100
```

#### Quick Scan

```bash
python3 scripts/quick_scan.py \
  --category-url "https://www.amazon.com/Best-Sellers-Cell-Phones/zgbs/wireless" \
  --limit 50
```

#### AI Opportunity Analysis

```bash
python3 scripts/ai_opportunity_analysis.py \
  --input-file analysis_result.json \
  --analysis-type comprehensive \
  --output report.md
```

## Available Scripts

| Script | Purpose | Documentation |
|--------|---------|---------------|
| `analyze_category.py` | Complete end-to-end analysis | [SKILL.md](SKILL.md) |
| `find_black_horses.py` | Find high-potential products | [SKILL.md](SKILL.md) |
| `ai_opportunity_analysis.py` | AI-powered recommendations | [SKILL.md](SKILL.md) |
| `quick_scan.py` | Fast category overview | [SKILL.md](SKILL.md) |
| `fetch_bestsellers.py` | Raw data collection | [SKILL.md](SKILL.md) |
| `calculate_metrics.py` | Metric calculations | [SKILL.md](SKILL.md) |

## Documentation

- **[SKILL.md](SKILL.md)** - Main skill documentation and workflows
- **[references/api-guide.md](references/api-guide.md)** - Apify API setup and troubleshooting
- **[references/analysis-methods.md](references/analysis-methods.md)** - Formulas and methodologies
- **[references/troubleshooting.md](references/troubleshooting.md)** - Common issues and solutions

## Key Metrics

### Potential Score

Formula: `(monthly_sales / (reviews + 1)) × (365 / (days_online + 1))`

Identifies high-growth, low-competition products.

### Monopoly Risk (CR5)

Top 5 brands' combined market share. Higher = more difficult to enter.

### Amazon Competition

Percentage of products sold directly by Amazon. Higher = more competition.

## Cost Estimation

Typical analysis costs (Apify):

- 50 products: ~$0.50 - $0.75
- 100 products: ~$1.00 - $1.50

Free tier includes $5/month credit.

## Troubleshooting

### Common Issues

1. **API Token Not Set**
   ```bash
   export APIFY_API_TOKEN="your_token"
   ```

2. **No Products Found**
   - Verify category URL is valid
   - Try different Amazon domain
   - Check internet connection

3. **Analysis Timeout**
   - Reduce `--max-items`
   - Check Apify console for run status

See [references/troubleshooting.md](references/troubleshooting.md) for detailed solutions.

## Support

- **Apify Support**: https://apify.com/contact
- **OpenAI Documentation**: https://platform.openai.com/docs
- **Skill Issues**: Check troubleshooting guide

## License

MIT License - See LICENSE file for details
