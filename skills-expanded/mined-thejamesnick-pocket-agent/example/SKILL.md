---
name: example-skill
version: 1.0.0
description: An example skill to show the structure. Delete this and add your own.
---

# Example Skill

This is a placeholder to show you how skills are structured. Delete this folder and create your own.

## How Skills Work

A skill teaches your agent how to use a tool or API. It's just a markdown file with instructions.

## Structure

```
skills/
└── my-skill/
    ├── SKILL.md          ← Instructions (required)
    ├── package.json      ← Metadata (optional)
    └── scripts/          ← Helper scripts (optional)
```

## Example: A Weather Skill

```markdown
---
name: weather
version: 1.0.0
description: Get current weather for any location.
---

# Weather Skill

## How to Use

Fetch weather data from the OpenWeatherMap API:

\```bash
curl "https://api.openweathermap.org/data/2.5/weather?q=London&appid=$WEATHER_API_KEY"
\```

## Response Format
Returns temperature, humidity, conditions, etc.
```

## Finding Skills

- Check the OpenClaw community for published skills
- Build your own — it's just a SKILL.md teaching your agent how to use something
- Install third-party skills by cloning them into this folder
