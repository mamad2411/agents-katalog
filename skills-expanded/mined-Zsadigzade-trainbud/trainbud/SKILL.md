---
name: trainbud
description: >-
  Answer questions about the user's Garmin Connect data — workouts, sleep, heart rate,
  recovery, stress, VO2 max, body composition, and training load. Use when the user
  runs /trainbud:trainbud or asks about Garmin stats, fitness, recovery, or training.
disable-model-invocation: true
---

# TrainBud — talk to your Garmin data

Use TrainBud MCP tools when the `trainbud` server is connected. Do not guess fitness data.

## Before fetching data

If MCP tools are unavailable, tell the user to run **`/trainbud:trainbud-setup`**, set `GARMIN_EMAIL` / `GARMIN_PASSWORD`, restart Claude Code, and try again.

## MCP tools (15)

| Tool | Use for |
|------|---------|
| `get_latest_activity` | Most recent workout |
| `get_activities_range` | Activities between ISO dates |
| `get_sleep_data` | Sleep duration, stages, score |
| `get_heart_rate_trends` | Resting/max/average HR trends |
| `get_recovery_status` | Composite recovery score |
| `get_body_composition` | Weight, body fat, muscle trends |
| `get_stress_levels` | Daily stress averages |
| `get_vo2_max_trends` | VO2 max fitness trends |
| `get_training_insights` | Combined weekly summary |
| `get_findings` | What stands out against the user's **own** 28-day baselines |
| `get_week_review` | This week against last, load forecast, sleep debt, next race |
| `compare_workouts` | One workout against their own earlier efforts at that distance |
| `remember_context` | Record a goal, a race and its date, an injury, or a note |
| `get_user_context` | What is on record about the user, on any date |
| `log_subjective` | How a session felt — RPE, soreness, mood |

## How to respond

1. **Pick the right tool(s)** — prefer compound queries for training decisions.
2. **Sensible defaults** — 7 nights sleep, 30 days HR/VO2, today/yesterday for activities.
3. **Plain English** — friendly coach tone, not raw JSON.
4. **Honest about gaps** — body comp often empty.

## User intent → tools

| User asks… | Tools |
|------------|-------|
| Recent workouts | `get_latest_activity`, `get_activities_range` |
| Sleep | `get_sleep_data` |
| Recovered / train hard? | `get_recovery_status`, `get_sleep_data`, `get_stress_levels` |
| HR trend | `get_heart_rate_trends` |
| Weight / body comp | `get_body_composition` |
| Stress / overtraining | `get_stress_levels`, `get_training_insights` |
| VO2 max / fitness | `get_vo2_max_trends` |
| Weekly summary | `get_training_insights`, `get_week_review` |
| Anything unusual / how am I doing? | `get_findings` — prefer this over reading raw metrics |
| How did that session compare? | `compare_workouts` |
| Goals, races, injuries | `remember_context`, `get_user_context` |
| How a session felt | `log_subjective` |

## Example prompts

See [prompts.md](prompts.md). Natural language works too:

- "What did I do today?"
- "Am I recovered enough to train hard tomorrow?"

## Diagnostics

```bash
trainbud check
trainbud cache clear
```
