---
name: openclawforge-ai-agent-creator
description: >
  Use when creating new AI agents for the OpenClaw AI company, designing agent specifications,
  defining skills and capabilities, or managing the agent lifecycle.
---

# OpenClaw Agent Creator - OpenClaw AI Agent Lifecycle Management

## Overview
Designs, creates, configures, and manages the lifecycle of all AI agents within the OpenClaw AI company. Handles agent specification, skill definition, database registration (on `srv1628373.hstgr.cloud`), and integration with the broader OpenClaw ecosystem. Works closely with the SQLite Manager for database operations and the Model Assigner for model configuration.

## Capabilities
- **Agent Specification**: Comprehensive agent role definition and capability planning
- **Skill Architecture**: Design of skill sets with proper routing and integration logic
- **Agent Registration**: Coordinates with SQLite Manager to register new agents in the `agents` table on the VPS database
- **API Key Setup**: Works with SQLite Manager to register API keys in `agent_api_keys` table on the VPS database
- **Lifecycle Management**: Agent updates, status changes, decommissioning, and knowledge transfer

## When to Use
- When creating new agents for the OpenClaw AI company
- When defining or updating agent capabilities and skills
- When setting up agent reporting structure (reports_to)
- When an agent's role or responsibilities need to change
- When decommissioning an agent and transferring its knowledge

## Platform Context
- **VPS Hostname**: `srv1628373.hstgr.cloud`
- **Database**: SQLite on the VPS (managed by SQLite Manager)
- See `infrastructure/vps-infrastructure.md` for detailed knowledge