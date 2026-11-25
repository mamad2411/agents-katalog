---
name: opencode-analyzer
description: Analyze OpenCode token usage and estimate costs on OpenRouter
version: 1.0.0
author: Dustin Chadwick (@ShaggyD)
tags: [opencode, costs, analysis, productivity]
---

# opencode-analyzer

OpenCode cost analyzer with detailed daily, weekly, and monthly breakdowns. Shows what you actually spent vs what it would cost on OpenRouter, plus same-token model comparisons.

## Problem

OpenCode costs add up fast and the CLI doesn't tell you what you're actually spending. Free models hide real costs behind a "free" label, and without tracking you won't notice budget drift until the bill comes.

## Built

A cost analysis tool that queries your local OpenCode SQLite database and breaks down usage by day, week, and month. Shows top models by spending, projects cost comparisons against OpenRouter equivalents, and provides same-token repricing across comparable model tiers.

## Outcome

You see budget drift before it becomes a surprise bill. Daily and weekly summaries catch unusual spending patterns early, and the OpenRouter comparison helps you decide whether switching providers would save money.

**SCOPE:** This skill covers **OpenCode** cost analysis only. OpenCode and OpenAI Codex CLI are separate tools with separate cost databases. Do NOT use this to analyze Codex CLI costs — see `references/codex-cli-monitoring.md`.

## What It Does

Queries your local OpenCode SQLite database to show:
- Daily, weekly, and monthly spending
- Average costs per day/week/month
- Cost projections
- Top models by spending
- OpenRouter cost equivalents for free models
- Same-token repricing across comparable model tiers

## Installation

```bash
# Copy to your skills directory
cp -r skills/opencode-analyzer ~/.config/opencode/skills/

# Or create symlink to command
ln -s ~/.config/opencode/skills/opencode-analyzer/opencode-cost ~/.local/bin/opencode-cost
```

Optional plugin sources are stored in `plugins/`.

## Plugin behavior (optional)

When enabled in a compatible OpenCode runtime, the plugin layer is intended to:

- Surface quick spend context inside OpenCode (today, yesterday, 7d, 30d)
- Use actual costs for paid usage and OpenRouter estimates for free-model usage
- Show rolling averages and a short top-model cost list

If your runtime does not expose plugin sidebar UI, use the command path (`opencode-cost` and `/cost-report`), which is the primary supported workflow for this skill.

## Usage

```bash
# Show complete cost breakdown
opencode-cost
```

## What It Shows

```
💰 OPENCODE COST BREAKDOWN

📅 SPENDING BY PERIOD
────────────────────────────────────────────────────────────
Today:                         $3.80
Yesterday:                     $2.19
Last 7 Days:                  $16.68
Last 30 Days:                 $16.89
All Time:                      $81.83

📊 AVERAGES
────────────────────────────────────────────────────────────
Daily Average (30d):           $0.60
Weekly Average (30d):          $4.20
Monthly Average (30d):        $18.17
Daily Avg (active):            $3.07

🔮 PROJECTION
────────────────────────────────────────────────────────────
Projected (7d run-rate):     $107.70

📈 ACTIVITY
────────────────────────────────────────────────────────────
Active Days (Week):                  5
Active Days (Month):                 6
Total Active Days:                  27
Calendar Span Days:               104

🔥 TOP MODELS (Last 30 Days)
────────────────────────────────────────────────────────────
MODEL                              COST % OF TOTAL
kimi-k2.5-free                   $7.26      40.0%
gpt-5.3-codex                    $5.14      30.0%
moonshotai/kimi-k2.5             $1.58       9.0%
```

## Sections Explained

### 📅 Spending by Period
- **Today**: Current day's spending
- **Yesterday**: Previous day's spending  
- **Last 7 Days**: Week total
- **Last 30 Days**: Month total
- **All Time**: Complete history

### 📊 Averages
- **Daily/Weekly/Monthly (30d)**: Rolling averages based on the last 30 calendar days
- **Daily Avg (active)**: Average per active day across all-time usage

### 🔮 Projection
- **Projected (7d run-rate)**: Based on last 7 days active-day run rate × 30

### 🧪 Model Comparison (Same 7d Tokens)
- Uses your exact last 7 days input/output token totals
- Pulls current trending models from OpenRouter rankings
- Reprices those same tokens across comparable model tiers
- Shows 7-day repriced cost and 30-day run-rate per model
- Helps compare options without changing usage volume

### ☁️ AWS vs OpenRouter (30d from 7d usage)
- Uses your exact last 7 days tokens and projects to 30 days
- Compares AWS us-east on-demand rates vs OpenRouter model rates
- Includes Claude Sonnet/Opus 4.6 (and Long Context on AWS), DeepSeek, Kimi, GLM, Qwen, and Minimax
- Rounds displayed values up to the nearest cent for budget planning
- Adds `ZDR` column (whether model has at least one OpenRouter ZDR endpoint)
- Adds `MM` column (whether the model supports non-text inputs)

### 📈 Activity
- Active days plus total calendar span since first usage

### 🔥 Top Models
- Most expensive models (by cost, not tokens)
- Shows cost and percentage of monthly total

## Cost Calculation

**Paid models**: Uses actual cost from OpenCode  
**Free models**: Uses OpenRouter pricing:

| Model | Input | Output |
|-------|-------|--------|
| GLM 4.6 | $0.30/M | $2.55/M |
| Kimi K2.5 | $0.50/M | $2.40/M |
| Gemini 2.5 Flash | $0.30/M | $2.50/M |
| GPT-5.3 Codex | $1.25/M | $10.00/M |
| MiniMax M2.5 | $0.15/M | $0.60/M |
| Claude Opus | $5.00/M | $25.00/M |
| Qwen | $0.40/M | $2.40/M |

Comparison table dynamically selects current OpenRouter trending models in value, balanced, and premium classes. If live fetch fails, it falls back to a stable default set.

## Database Location

Auto-detects from:
- `~/.local/share/opencode/opencode.db` (default)
- `~/Library/Application Support/opencode/opencode.db` (macOS)

## Requirements

- sqlite3 (usually pre-installed)
- bc (for calculations, usually pre-installed)

## Examples

```bash
# Default breakdown
opencode-cost

# Use specific database
opencode-cost --db /path/to/opencode.db
```

## Troubleshooting

### Database not found
```bash
# Find your database
find ~ -name "opencode.db" 2>/dev/null

# Specify path
opencode-cost --db /path/to/opencode.db
```

### Permission denied
```bash
chmod 644 ~/.local/share/opencode/opencode.db
```

### sqlite3 not found
```bash
# macOS
brew install sqlite

# Ubuntu/Debian
sudo apt-get install sqlite3
```

## Notes

- Negative values (refunds/adjustments) are excluded
- Free models show OpenRouter equivalent cost
- Projections based on recent 7-day average
- Only counts days you actually used OpenCode

## Related

- [OpenCode](https://github.com/opencode-ai/opencode) - AI coding agent
- [OpenRouter](https://openrouter.ai) - Unified API for LLMs
- `references/codex-cli-monitoring.md` — Cost monitoring for **OpenAI Codex CLI** (separate tool from OpenCode)

## Pitfalls

- **OpenCode vs Codex CLI**: This skill is for **OpenCode** only. OpenAI Codex CLI uses a completely separate session storage (`~/.codex/sessions/`) and model pricing. Do NOT use `opencode-cost` to check Codex usage — use the codex-usage-monitor.py script instead (see `references/codex-cli-monitoring.md`).
- **Database detection**: If `opencode-cost` can't find the database, run `find ~ -name "opencode.db" 2>/dev/null` and pass with `--db`.
- **Free models show estimates**: Free-tier OpenCode models are repriced at OpenRouter rates. Actual cost was $0, but the estimate shows what a paid equivalent would cost.
- **Session files cleared**: If you clear OpenCode session databases, historical data resets. The script only sees what's in the DB.
