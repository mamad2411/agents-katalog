---
name: whatsapp-router
description: Classify and route WhatsApp messages with consent, privacy, and escalation boundaries.
category: utilities
aliases:
- whatsapp
- route
- classify
triggers:
- Route this WhatsApp message
- Categorize WhatsApp message
- Process WhatsApp input
keywords:
- whatsapp
- message
- route
- classify
- triage
dependencies:
- optional:whatsapp-api
risk: high
version: 1.0.0
source: custom
enabled: true
capabilities:
- whatsapp-router
- utilities
inputs:
- task
- context
outputs:
- result
- report
lifecycle: enabled
author: Mr-Nobody-Anonymous
tags:
- classify
- message
- route
- router
- utilities
- whatsapp
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# Whatsapp Router

## Purpose
Classify incoming WhatsApp messages and route them to appropriate handlers based
on content type, sender, and intent. The skill ensures proper consent verification
and privacy boundaries are maintained.

## When to Use
- Processing incoming WhatsApp messages for automation
- Routing messages to appropriate handlers or skills
- Classifying message intent (question, command, escalation)

## When NOT to Use
- Responding directly without user consent
- Storing message content without permission
- Processing messages from unknown senders

## Capabilities
- Message classification (command, question, notification, spam)
- Intent detection
- Sender verification
- Privacy-filtering (redact sensitive content)
- Routing to appropriate handlers
- Escalation detection for human review

## Inputs
- `message` (required) — message content
- `sender` (required) — sender identifier
- `timestamp` (required) — message timestamp
- `context` (optional) — conversation history

## Workflow
1. **Verify** — Check sender consent and authorization
2. **Classify** — Determine message type and intent
3. **Filter** — Apply privacy filters to content
4. **Route** — Direct to appropriate handler or skill
5. **Escalate** — Flag for human review if needed
6. **Respond** — Generate appropriate response (if authorized)

## Tools
- WhatsApp Business API
- Message classification model

## Examples
Example usage:
```bash
# Invoke via skills CLI
python scripts/skills/skills.py route "Route this WhatsApp message"
```

## Safety
- NEVER process messages without verified consent
- Always filter sensitive content before routing
- Escalate ambiguous or concerning messages to human review
- Never store raw messages without consent
- Respect blocking and opt-out requests immediately

## Source
Auto-generated from openclawskills.net description.

## Notes
Maintained as part of canonical utilities category.
