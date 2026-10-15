---
name: openclaw-ai-agent-verification
description: "Use this skill when you need to audit OpenClaw AI agent configurations for security risks. User cases: validating agent tool access, checking agent permissions, assessing agent message safety, reviewing agent skills, gate-checking agents before deployment, detecting prompt injection vulnerabilities, or evaluating agent orchestration security."
license: MIT
metadata:
  author: Cybercentry
  version: "1.0.0"
---

# OpenClaw AI Agent Verification

Audit AI agent configurations for security risks via Cybercentry ACP. Returns Critical/High/Medium/Low risk level.

## Workflow

1. Install ACP CLI from https://github.com/Virtual-Protocol/openclaw-acp
2. Run `acp setup` (one-time only)
3. Run `acp browse "Cybercentry"` to find provider wallet
4. Run `acp job create <wallet> openclaw-ai-agent-verification --requirements '{"tool": {...}, "config": {...}}'`
5. Poll `acp job status <jobId>` until `COMPLETED`

## Requirements Schema

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `tool` | Object | No | Tool to validate (contains `name` and `args`) |
| `tool.name` | String | Yes | Tool name |
| `tool.args` | Object | Yes | Tool arguments |
| `config` | Object | Yes | Configuration (filename: openclaw.json or JSON content) |
| `skills` | String | No | Skills content (filename: SKILL.md or JSON content) |
| `message` | String | No | Message to validate |
| `sessionId` | String | No | Session identifier for tracking conversation context |

## Deliverables

| Field | Type | Format | Description |
|-------|------|--------|-------------|
| `report` | String | Plain | Security risk report |

## Gotchas

- `config` is required - pass the openclaw.json content or an empty object `{}`
- `tool.args` must be an object, even if empty - use `{}` not `null`
- Large skills content should be stringified JSON, not raw markdown
