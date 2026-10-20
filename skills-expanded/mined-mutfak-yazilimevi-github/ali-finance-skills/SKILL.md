---
name: "finance-skills"
description: "Claude Code, Codex, Gemini CLI, Cursor, OpenClaw için finansal analist ajan becerisi ve eklentisi. Oran analizi, DCF değerlemesi, bütçe varyansı, dönemsel tahminler. 4 Python aracı (yalnızca stdlib)."
version: 2.9.0
author: Alireza Rezvani
license: MIT
tags:
  - finance
  - financial-analysis
  - dcf
  - valuation
  - budgeting
agents:
  - claude-code
  - codex-cli
  - openclaw
---

# Finance Skills

Production-ready financial analysis skill for strategic decision-making.

## Quick Start

### Claude Code
```
/read finance/financial-analyst/SKILL.md
```

### Codex CLI
```bash
npx agent-skills-cli add alirezarezvani/claude-skills/finance
```

## Skills Overview

| Skill | Folder | Focus |
|-------|--------|-------|
| Financial Analyst | `financial-analyst/` | Ratio analysis, DCF, budget variance, forecasting |

## Python Tools

4 scripts, all stdlib-only:

```bash
python3 financial-analyst/scripts/ratio_calculator.py --help
python3 financial-analyst/scripts/dcf_valuation.py --help
python3 financial-analyst/scripts/budget_variance_analyzer.py --help
python3 financial-analyst/scripts/forecast_builder.py --help
```

## Rules

- Load only the specific skill SKILL.md you need
- Always validate financial outputs against source data
