---
name: multi-agent-governance
description: "Use this skill when building, managing, or auditing multi-agent AI systems. Provides governance patterns for behavioral enforcement, drift detection, audit trails, role management, and accountability across autonomous AI agents. Compatible with any orchestration framework."
license: Apache-2.0
metadata:
  author: palyan-family-ai
  version: "1.0.0"
  homepage: https://www.npmjs.com/package/@anthropic-ai/mcp-nervous-system
  repository: https://github.com/anthropics/mcp-nervous-system
---

# Multi-Agent Governance

Governance patterns for multi-agent AI systems. When you have multiple autonomous AI agents operating together, you need accountability, behavioral enforcement, and drift detection - just like human organizations.

## Core Principles

1. **Single source of truth** - One config file defines all agent roles. Every agent reads from it. No parallel systems.
2. **Behavioral enforcement** - Rules are not suggestions. Guardrails are enforced through preflight checks, violation logging, and automated audits.
3. **Drift detection** - Systems drift from their intended state over time. Automated drift audits catch configuration mismatches, version inconsistencies, and role conflicts before they cause failures.
4. **Tamper-proof audit trails** - Every action, every change, every decision is logged in append-only logs that can be verified for integrity.
5. **File-based memory** - Agent memory lives in files on disk, not in cloud databases. This enables air-gapped deployment, full auditability, and zero vendor dependency.

## Governance Patterns

### Role Management
Define roles in a single JSON file that all agents reference:
```json
{
  "agent-name": {
    "role": "Operations Manager",
    "scope": ["dispatch", "monitoring", "reporting"],
    "access": "admin",
    "model": "claude-opus-4-6"
  }
}
```
Every agent reads from this file at startup. Changes propagate automatically.

### Preflight Checks
Before any agent modifies a file:
1. Check if the file is on the protected list
2. If protected: log the attempt, report to admin, and STOP
3. If allowed: create backup, make change, syntax check, restart affected process

### Drift Audit Scopes
Run periodic audits across these dimensions:
- **roles** - Do running agents match their role definitions?
- **versions** - Are all agents on the correct model version?
- **files** - Have any protected files been modified?
- **processes** - Are all expected processes running?
- **config** - Do config files match expected state?

### Session Management
Every agent session should:
1. Read the current system state before acting
2. Write progress as it goes (no silent failures)
3. Update handoff documentation before ending
4. Run a drift audit on affected areas

### Permission Protocol
Two categories of changes:
- **DATA** (values, content, configuration): Agent can act with general authorization
- **LOGIC** (how something decides, classifies, responds): Agent PROPOSES and WAITS for human approval

When in doubt, it is LOGIC. Ask the human.

## Implementation

### Using the Nervous System MCP
The Nervous System is a Model Context Protocol server that implements these governance patterns with 19+ tools:

```bash
npm install -g @anthropic-ai/mcp-nervous-system
```

Tools include: drift_audit, security_audit, auto_propagate, session_close, preflight_check, violation_logging, and more.

### DIY Implementation
If building your own governance layer:
1. Create a roles config file (JSON) as single source of truth
2. Create a protected files list that agents check before editing
3. Implement append-only logging for all agent actions
4. Schedule periodic drift audits (compare expected vs actual state)
5. Build a violation log that captures unauthorized changes

## Anti-Patterns
- Letting agents self-modify their own rules
- Multiple sources of truth for the same data
- Silent failures (agent encounters error but does not report it)
- Manual fixes without adding automated detection
- Hardcoding values that should come from config

## Resources
- [Nervous System MCP on npm](https://www.npmjs.com/package/@anthropic-ai/mcp-nervous-system)
- [Agent Skills Specification](https://agentskills.io/specification)
- [Model Context Protocol](https://modelcontextprotocol.io)
