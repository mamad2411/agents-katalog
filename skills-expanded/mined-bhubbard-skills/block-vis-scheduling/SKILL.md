---
name: block-vis-scheduling
description: Configuring Date and Time scheduling for blocks. Use when setting up temporary promotions, seasonal content, or recurring weekly visibility.
---

# Block Visibility: Scheduling

The Date & Time visibility control allows users to automate when a block appears or disappears from the site.

## Available Scheduling Options
- **Start / End Date**: The block will only show between specific dates and times.
- **Seasonal**: Year-agnostic scheduling (e.g., "Every year between Dec 1 and Dec 25").
- **Day of Week**: Show the block only on specific days (e.g., "Only show on Weekends").
- **Time of Day**: Show the block only during specific hours (e.g., "Show lunch menu from 11:00 AM to 2:00 PM").

## Troubleshooting Timezones
If a scheduled block appears or disappears at the wrong time:
1. Check the WordPress global timezone settings (`Settings > General`). Block Visibility relies on the site's configured timezone, NOT the visitor's local browser timezone.
2. If using page caching, the cache must be purged when the schedule triggers, otherwise the old state (hidden or visible) will continue to be served from the cache. The plugin attempts to handle cache purging automatically for popular caching plugins, but edge cases exist.
