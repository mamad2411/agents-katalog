---
tags: [backend, byte, aware, sms, truncation, with]
name: byte-aware-sms-truncation-with-ellipsis
description: Truncate SMS message body to a byte budget (not char count) per charset, appending '...' without exceeding the budget
version: 1.0.0
source_project: lucida-notification
category: backend
trigger: writing to an SMS column / gateway with a hard byte limit where multibyte chars (Korean, emoji) overflow a naive char truncation
---

See `content.md`.
