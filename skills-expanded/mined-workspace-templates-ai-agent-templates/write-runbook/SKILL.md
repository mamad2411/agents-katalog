---
name: write-runbook
description: Writes an on-call runbook for a service or alert, with first checks, exact commands, escalation and a safe way back.
disable-model-invocation: true
---

Write a runbook for: $ARGUMENTS (service name or alert name).

1. Gather facts from the repository: how the service is deployed, its dependencies (database, queue, third-party APIs), health endpoints, log locations, dashboards and alert rules (search for alert definitions and the alert name). Mark any fact you cannot find as "to be confirmed" and never invent hostnames or URLs.
2. Structure the page as: Purpose and impact (who notices when it breaks), Quick checks (first three minutes), Diagnosis by symptom, Fixes, Escalation, and After the incident.
3. For every check give the exact command in a code block, what healthy output looks like and what bad output looks like. Use read-only commands first (status, logs, metrics queries).
4. Put commands that change state, such as restart, scale, failover, rollback, in a separate list marked "Changes production", each with its risk and how to undo it.
5. Add who to page and when, using names from the repository's CODEOWNERS or docs when present.

Match the format of runbooks already in docs/. Show the draft and ask before saving it. Run none of the commands yourself.
