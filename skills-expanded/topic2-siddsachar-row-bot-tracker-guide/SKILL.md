---
name: tracker_guide
display_name: Tracker Guide
icon: "📊"
description: Guidance for habit and activity tracking tools.
tools:
  - tracker
tags: []
---
HABIT / ACTIVITY TRACKING:
- You have a habit tracker for logging recurring activities: medications,
  symptoms, habits, health events (periods, headaches, exercise, mood, etc.).
- When a user mentions something that matches an existing tracker — e.g.
  'I have a headache' when Headache is tracked — ask: 'Want me to log that?'
  before logging.  Never log silently.
- Use tracker_log to record entries, tracker_query for history/stats/trends.
- tracker_query exports CSV files that you can pass to create_chart for
  visualisations (bar charts of frequency, line charts of values over time).
- Tracker CSV: tracker_query auto-exports CSV files — pass the
  returned path directly to send or attach tools.
