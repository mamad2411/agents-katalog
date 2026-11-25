---
name: qa-answer-review-operation
description: >-
  Operation lens of qa-answer-review: check the run-time side of a prepared meeting answer —
  connectivity (VPN, firewall, hosts), file transfer / SFTP, sandbox and UAT access, API keys and
  auth, monitoring and error feedback, retry, support and cut-over. Use WHENEVER the work is
  "operation review of a prepared answer", "who hosts the SFTP server", "how will they know a
  push failed", "where is the sandbox", "ส่งไม่สำเร็จจะรู้ได้อย่างไร", or when qa-answer-review
  fans out its lenses. Read-only.
---

# Operation lens

Per row: **if the customer does exactly this tomorrow, does it reach us, and do both sides know
when it fails?**

## Check

1. **Connectivity.** Hosts and IPs per environment, VPN / firewall prerequisites, allow-lists. An
   answer that skips a network prerequisite → `ADJUST`.
2. **Channels that exist.** SFTP / file drop: grep the API repo and deployment packages for a
   listener; none = say so plainly. Excel / CSV import: the real import screen and its validate →
   confirm flow.
3. **Sandbox / UAT.** Which URL, which account, how a customer gets an API key. "There is a
   sandbox" needs the actual target.
4. **Failure feedback.** Response codes and bodies of the external endpoints, webhooks, queue
   status, notification paths. "Should have" when the code already has it → `ADJUST` to "has";
   when it doesn't → `OPEN`.
5. **Cut-over.** Interim → target channel: is there a duplicate guard when both run at once (the
   data lens has the keys)?

`N/A` for rows with no run-time content. Output contract and tone rules: `answer-review/SKILL.md` §1.
