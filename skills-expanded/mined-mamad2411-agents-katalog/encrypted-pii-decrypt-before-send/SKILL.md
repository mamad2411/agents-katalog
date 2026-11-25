---
tags: [backend, encrypted, pii, decrypt, before, send]
name: encrypted-pii-decrypt-before-send
description: Store user email/phone encrypted at rest; decrypt only inside the sender, never in cache/DTO/log boundaries
version: 1.0.0
source_project: lucida-notification
category: backend
trigger: any notification service whose user directory stores PII encrypted (GDPR/K-privacy) and which must deliver to plaintext recipient addresses
---

See `content.md`.
