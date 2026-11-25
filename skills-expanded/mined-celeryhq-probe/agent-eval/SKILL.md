---
name: agent-eval
description: Use when probing AI agents — reads eval config YAML, orchestrates browser interaction, verification, and report generation for web-based AI agent evaluation
---

# Agent Eval — Orchestrator

## Overview

Probes an AI agent end-to-end from a YAML config. Drives a real browser, interacts like a user, judges the output across multiple dimensions, and generates an HTML report with screenshots and optional video.

## Prerequisites

- `playwright-cli` installed (`playwright-cli --version`)
- Chrome/Chromium available

## Config Format

```yaml
suite: "Suite Name"

target:
  url: "https://app.example.com"
  credentials:                   # secrets — use {{env:VAR}} to pull from .env
    email: "{{env:AGENT_TARGET_EMAIL}}"
    password: "{{env:AGENT_TARGET_PASSWORD}}"
  auth:                          # login steps — run once per suite
    - "Type '{{email}}' in the email field"
    - "Type '{{password}}' in the password field"
  setup:                         # fresh conversation — run before each scenario
    - "Start a new conversation"
scenarios:
  - name: "Scenario Name"
    steps:
      - "Natural language action steps"
    verify:
      - type: ai-judge
        check: "Natural language assertion"
```

**Substitution:** `{{env:VAR}}` resolves from environment. `{{key}}` resolves from credentials.

## Execution

### 1. Parse + Classify

Read the YAML. Resolve credentials. Classify each scenario:

- **Parallel:** 1-3 simple steps, no multi-turn interaction (routing probes, single Q&A)
- **Sequential:** 3+ steps with forms, approvals, multi-turn flows

The agent decides — no YAML flag needed. Look at the steps: if they reference "approve", "fill form", "click Next", or depend on previous output → sequential.

### 2. Auth Once

Log in once at the start. Save browser state for parallel sessions to reuse.

### 3. Run Scenarios

- **Sequential:** Same browser session, fresh conversation per scenario via setup steps
- **Parallel:** Dispatch subagents with their own named browser sessions, shared auth state

### 4. Per Scenario

For each scenario:
1. Run setup steps (fresh conversation)
2. Run scenario steps — screenshot after each action, record video if enabled
3. Run verify blocks — capture page state, evaluate each check
4. For AI-evaluated checks (ai-judge, compliance, visual, brand): read screenshot + page text, judge against the check

### 5. Report

Generate HTML report with:
- AI Analysis per scenario (top of each section — the highlight)
- Verification results with explanations
- Step-by-step screenshots (expandable)
- Pass/fail/warning summary

Open report automatically when done.

## Key Behaviors

- Auth runs ONCE per suite — browser stays open across scenarios
- Each scenario gets a FRESH conversation via setup steps
- Screenshot after EVERY action
- Record video per scenario when enabled
- If a step fails: capture error screenshot, mark remaining verifies as "error", continue to next scenario
- Always produce a report, even if partial
- Auto-classify parallel vs sequential — no manual flags
