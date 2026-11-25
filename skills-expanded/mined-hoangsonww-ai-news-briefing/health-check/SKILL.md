---
name: health-check
description: Run the system health check to verify the AI News Briefing setup and configuration.
---

# Health Check Skill

Run the system health check script located in the `scripts/` directory to verify the installation, dependencies, and configuration.

To do this, execute `bash scripts/health-check.sh` on macOS/Linux or `powershell -ExecutionPolicy Bypass -File scripts\health-check.ps1` on Windows.
Parse the output and summarize any warnings or errors for the user. If everything is healthy, report that the system is fully operational.