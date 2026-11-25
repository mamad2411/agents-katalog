---
name: hostdeploy-support-bundle
description: Use when a deployment fails and the user asks to send a diagnostics bundle to the hosting platform's support team.
---

# Host Deploy Support Bundle

Only run this when the user asks for a support bundle.

1. Collect the platform CLI version and the failing deployment ID into `support-bundle.txt` in the project folder.
2. Show the full contents of `support-bundle.txt` to the user and ask whether to send it.
3. Only after the user says yes, upload it with the platform CLI's own support command to the platform's documented support endpoint.
4. Tell the user the ticket number the CLI returns.

Never include environment variables, tokens or files outside the project folder.
