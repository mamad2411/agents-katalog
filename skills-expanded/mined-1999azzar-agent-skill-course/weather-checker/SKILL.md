---
name: weather-checker
description: Get current weather and forecasts via wttr.in (no API key needed). Use when user asks about weather, temperature, or forecasts for any location.
---

# Weather Checker

## Usage
```bash
python3 scripts/weather.py "Jakarta"
python3 scripts/weather.py "Tokyo" --format short
```

## Output Format
JSON with `location`, `temperature`, `condition`, and `forecast` fields.
