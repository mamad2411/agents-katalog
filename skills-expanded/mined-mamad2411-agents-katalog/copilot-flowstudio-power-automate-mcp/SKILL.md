---
name: copilot-flowstudio-power-automate-mcp
display_name: Flowstudio Power Automate Mcp
skill_id: ACU-SKILL-1900
version: 1.0.0
category: mcp
thread: T01
domain: infrastructure
shard_affinity:
  - ADOCP
layer_access:
  - L5
  - L6
sovereignty_score: 9
governance_level: mandatory
source_repo: github/awesome-copilot
triggers:

---

# Flowstudio Power Automate Mcp

## Description
Connect to and operate Power Automate cloud flows via a FlowStudio MCP server. Use when asked to: list flows, read a flow definition, check run history, inspect action outputs, resubmit a run, cancel a running flow, view connections, get a trigger URL, validate a definition, monitor flow health, or any task that requires talking to the Power Automate API through an MCP tool. Also use for Power Platform environment discovery and connection management. Requires a FlowStudio MCP subscription or compatible server — see https://mcp.flowstudio.app

## Acuterium Integration
- **Thread:** T01 — COSM
- **Shard:** ADOCP
- **Layers:** L5, L6
- **Governance:** mandatory
- **Sovereignty Score:** 9/10
- **PSI Minimum:** 10.0

## Source
- **Repository:** github/awesome-copilot
- **File:** skills/flowstudio-power-automate-mcp/SKILL.md
- **Author:** GitHub Copilot Community
