# Exec Monitor

**Version:** 1.0.0
**Author:** OpenClaw Evolver
**Date:** 2026-02-11

## Description
A lightweight utility to monitor and log usage of the `exec` tool. Created in response to `high_tool_usage:exec` signals to better understand automation needs and potential bottlenecks.

## Usage
```bash
node skills/exec-monitor/index.js "<command>" "<optional_context>"
```

## Logs
Logs are stored in `logs/exec_usage.jsonl`.
