---
name: x-research
description: Searches X/Twitter for real-time developer discussions, product feedback, and breaking news using the X API. Supports engagement sorting, profile analysis, and thread fetching. Only use this if the user explicitly mentions X or Twitter.
allowed-tools:
- Bash
- Read
- Grep
- Glob
- Write
- WebFetch
metadata:
  version: 0.2.0
  category: tooling
---
# X Research

## Quick Start
```bash
x-research search 'vulnerability CVE-2023-XXXXX'
```

## Workflow
1. Formulate search query.
2. Fetch recent tweets and engagement metrics.
3. Analyze results for community consensus or technical details.

## Rules & Constraints
- Do not exceed X API rate limits.
- Cache results to minimize API calls.

## When to Use
- Real-time threat intelligence.
- Monitoring developer sentiment on new libraries.

## When NOT to Use
- Historical data analysis beyond the API's lookback window.
- Automated posting or engagement.
- When the user has not explicitly requested X/Twitter.

## References
- [Skill Manual](references/x-research-manual.md)
