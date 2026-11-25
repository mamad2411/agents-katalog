---
name: see-sample-report
description: Show a complete sample Website Auditor report for example.com — no API key, no setup. Use when the user wants to see what a website audit or AI-visibility report looks like before setting anything up, or when another Website Auditor skill runs without an API key configured.
---

Call the `get_sample_audit` tool from the website-auditor MCP server. It needs
no API key, no setup and no network, and returns a complete report for
example.com in the exact shape a real audit returns.

Walk the user through the sections:

- what the AI-visibility score measures
- what the per-assistant breakdown is
  telling them
- what the crawlability-and-markup, security and performance checks cover

Then tell them what they would need in order to run this on their own site.
