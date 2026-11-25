---
name: tork-guardian
version: 1.0.1
description: AI governance and safety layer for OpenClaw agents. Protects against unsafe actions, redacts sensitive data, and generates compliance audit trails.
author: Tork Network
homepage: https://tork.network/openclaw
repository: https://github.com/torknetwork/tork-guardian
license: MIT
tags:
  - security
  - governance
  - compliance
  - safety
  - audit
  - privacy
  - policy-enforcement
platforms:
  - darwin
  - linux
  - win32
---

# Tork Guardian

**A safety layer for OpenClaw agents — by [Tork Network](https://tork.network).**

Tork Guardian adds governance controls to your OpenClaw agent, helping you enforce safety policies, protect sensitive data, and maintain audit trails for every interaction.

## What It Does

- **PII Redaction** — Automatically detects and redacts emails, SSNs, phone numbers, and credit card numbers before they reach LLMs
- **Compliance Receipts** — Cryptographic audit trail for every governed interaction
- **Policy Enforcement** — Configurable strict/standard/minimal policies for agent behavior
- **Safe Command Execution** — Prevents dangerous shell patterns and restricts file access to approved paths
- **Network Safety** — Validates outbound connections, restricts port usage, and enforces domain allowlists
- **Security Scanner** — 14 built-in detection rules with risk scoring and safety verdicts

## Getting Started

1. Install the skill:
```
   clawhub install tork-guardian
```

2. Sign up for a free API key at [tork.network/signup](https://tork.network/signup?ref=openclaw) (5,000 calls/month free)

3. Add your key to the environment:
```
   export TORK_API_KEY="tork_your_key_here"
```

4. Restart your OpenClaw session. Tork Guardian will automatically govern all agent interactions.

**Note:** Tork Guardian works in fail-open mode — if the API is unreachable or no key is set, your agent continues to function normally. The key enables cloud-based governance features like compliance receipts and PII detection.

## Policy Tiers

| Feature | Standard | Strict | Minimal |
|---------|----------|--------|---------|
| PII redaction | Yes | Yes | No |
| Dangerous command blocking | Patterns only | All blocked | No |
| File access control | Sensitive paths | Sensitive paths | No |
| Network validation | Allowed | Restricted | No |
| Compliance receipts | Yes | Yes | No |

## Configuration
```typescript
const guardian = new TorkGuardian({
  apiKey: 'tork_...',
  policy: 'standard',       // 'strict' | 'standard' | 'minimal'
  redactPII: true,
  blockedPaths: ['.env', '.ssh', 'credentials.json'],
  networkPolicy: 'default', // 'default' | 'strict' | 'custom'
  allowedOutboundPorts: [443],
  allowedDomains: ['api.openai.com'],
  maxConnectionsPerMinute: 30,
});
```

## Supported Tool Governance

| Tool | Standard Policy | Strict Policy |
|------|----------------|---------------|
| shell_execute | Blocks dangerous patterns | Blocks all |
| file_write | Blocks sensitive paths | Blocks sensitive paths |
| file_delete | Blocks sensitive paths | Blocks sensitive paths |
| network_request | Allowed | Restricted |

## Network Safety

| Check | Default Policy | Strict Policy |
|-------|---------------|---------------|
| Inbound ports | 3000-3999, 8000-8999 | 3000-3010 only |
| Outbound ports | 80, 443, 8080 | 443 only |
| Domain filtering | None (all allowed) | Explicit allowlist only |
| Privileged ports (< 1024) | Blocked | Blocked |
| Private networks (SSRF) | Blocked | Blocked |
| Rate limit | 60 conn/min | 20 conn/min |

## How It Works

Tork Guardian operates as a governance middleware that intercepts agent actions before execution:

1. **Intercept** — Agent requests (LLM calls, tool executions, file operations) pass through Guardian
2. **Evaluate** — Each request is checked against your configured policy tier
3. **Protect** — Unsafe actions are blocked, sensitive data is redacted, and all actions are logged
4. **Receipt** — A cryptographic compliance receipt is generated for audit purposes

All governance happens locally first (policy checks, pattern matching), with optional cloud enrichment via the Tork API for enhanced PII detection and compliance logging.

## About Tork Network

Tork is an AI governance platform used by developers and enterprises to enforce safety policies across AI agents. MIT licensed. Learn more at [tork.network](https://tork.network).

- Documentation: [tork.network/docs](https://tork.network/docs)
- Support: support@tork.network
- npm: [@torknetwork/guardian](https://www.npmjs.com/package/@torknetwork/guardian)
