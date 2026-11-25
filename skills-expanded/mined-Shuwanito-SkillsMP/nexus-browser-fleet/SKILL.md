---
name: nexus-browser-fleet
description: "Headless browser fleet orchestration and management. Use when you need to coordinate multiple headless browser instances for automated web auditing, scraping, or testing at scale using tools like Pinchtab. Detects and corrects unstable fleets that fail audit coverage."
license: proprietary
compatibility: "NEXUS Ecosystem 1.0"
metadata:
  department: automation
  autonomy_level: competent
  nexus_version: "1.0"
  version: "1.0.0"
  author: "NEXUS AI Corp"
allowed-tools:
  - web-search
  - web-fetch
  - memory-read
  - memory-write
---

# Fleet Navigator

## Capabilities
- Headless browser fleet management and orchestration
- Automated web scraping at scale
- Browser automation pipelines using tools like Pinchtab
- Fleet stability monitoring and audit coverage validation
- Detection and correction of unstable browser fleets

## Workflow
1. Receive request for headless browser orchestration task
2. Assess fleet requirements (number of instances, target sites, audit scope)
3. Configure and deploy headless browser fleet
4. Monitor fleet stability and coverage metrics
5. Detect and remediate unstable instances that fail audit coverage
6. Report results and store findings in shared memory

## Guidelines
- Never modify target application code directly
- All proposals require peer review
- Ensure all browser fleets maintain full audit coverage before reporting completion
- Validate scraping results for completeness and accuracy
- Monitor resource consumption to prevent fleet instability
