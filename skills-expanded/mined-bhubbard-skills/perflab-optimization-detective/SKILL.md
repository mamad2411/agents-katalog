---
name: perflab-optimization-detective
description: Guidance on Optimization Detective. Use when troubleshooting dependencies for Embed Optimizer or Image Prioritizer, or understanding its URL metric data.
---

# Performance Lab: Optimization Detective

Optimization Detective is a foundational dependency module. It does not provide direct optimizations itself, but rather analyzes the frontend to inform other modules.

## How it works
It gathers data about the page structure (like identifying the LCP element or finding embeds) and stores this telemetry data so that other modules (like Image Prioritizer and Embed Optimizer) can act upon it.

## Troubleshooting
If dependent modules (Embed Optimizer, Image Prioritizer) are not working, ensure Optimization Detective is active and successfully completing its analysis runs. It may require a few page loads to gather accurate data.
