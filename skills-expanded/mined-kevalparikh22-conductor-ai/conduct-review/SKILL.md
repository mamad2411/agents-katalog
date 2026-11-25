---
name: conduct-review
description: "Second-opinion review of the branch by a worker LLM; the controller triages findings"
argument-hint: "[--plan <file>] [--base <ref>] [focus text]"
disable-model-invocation: true
allowed-tools: "Read, Bash(conductor-ai run review:*), Bash(git diff:*), Bash(git log:*)"
---

Run in the background: `conductor-ai run review the arguments the user gave`

Then read the report and triage every finding: open the cited lines and mark each one **real**, **false positive** or **unsure**. Don't pass on unchecked claims. Show the user only the real and unsure findings (severity, `file:line`, one-line problem), plus the reviewer's verdict and yours. Offer to fix them: small ones yourself, larger ones with `conductor-ai run fix`.
