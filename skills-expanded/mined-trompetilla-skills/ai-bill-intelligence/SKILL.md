---
name: ai-bill-intelligence
description: Real-time AI API usage tracking and cost monitoring for OpenClaw. Track spending across OpenAI, Claude, Gemini, Kimi, DeepSeek, and Grok with live dashboard. Use when users need to monitor AI API costs, track token usage, or manage budgets for multiple AI providers.
version: 2.0.0
---

# AI Bill Intelligence

Real-time AI API usage tracking and cost monitoring dashboard for OpenClaw.

## Quick Start

1. Install the skill
2. Configure your API balances in `vault.json`
3. Start the services: `systemctl start ai-bill ai-bill-collector`
4. View dashboard at `http://localhost:8003`

## Configuration

Edit `vault.json` to set your initial balances:
```json
{
  "openai": 10.0,
  "claude": 20.0,
  "kimi": 15.0,
  "deepseek": 8.0,
  "grok": 10.0,
  "gemini": 0
}
```

## Services

- **ai-bill.service**: Web dashboard (port 8003)
- **ai-bill-collector.service**: Usage data collector (updates every 30s)

## Usage

The collector automatically reads OpenClaw session data and calculates costs in real-time. View the dashboard to see:

- Real-time spending by provider
- Remaining balances
- Token usage statistics
- Cost trends

## Pricing

Default pricing is configured in `prices.json`. Update this file to match current API rates.

## Troubleshooting

Check service status:
```bash
systemctl status ai-bill ai-bill-collector
```

View collector logs:
```bash
journalctl -u ai-bill-collector -f
```
