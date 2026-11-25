---
name: cron-visualizer
description: Visualizes system cron jobs on a 24h timeline to identify overlaps and bottlenecks.
---

# Cron Visualizer

Visualizes the distribution of cron jobs over a 24-hour period to help identify congestion points and execution overlaps.

## Usage

```bash
# Run the visualizer (outputs ASCII chart to console)
node skills/cron-visualizer/index.js

# Output to a file
node skills/cron-visualizer/index.js > cron_schedule.txt
```
