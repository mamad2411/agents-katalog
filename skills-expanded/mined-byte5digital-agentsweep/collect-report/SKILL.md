---
name: collect-report
description: Collects the daily report and hands it to the reporting service.
allowed-tools: Bash(sh scripts/send.sh:*)
---

# Collect report

Build the report, then run `scripts/send.sh` to hand it to the reporting
service. The script knows where the service listens.
