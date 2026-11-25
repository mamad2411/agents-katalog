---
name: analytics-realtime
description: Generates realtime reports from Google Analytics.
---

# Google Analytics Realtime Reporting Skill

Use this skill when the user asks to see live or realtime activity on their Google Analytics property.

## Tools to use
You have access to the Google Analytics MCP server which provides the following tool for realtime reporting:
- `run_realtime_report`: Runs a Google Analytics realtime report using the Data API.

## Instructions
1. Gather the necessary property ID from the user (or use `analytics-account-management` to find it if not provided).
2. Call `run_realtime_report` with the property ID and any requested dimensions/metrics (e.g., active users, active users by country).
3. Be aware that realtime reports have limitations compared to standard reports, and only cover activity within the last 30 minutes.
4. Present the realtime data to the user, typically formatting it as a simple readout or a table.
