---
name: infra-runbook-build
description: 'Create evidence-based runbooks for operational tasks using supported project interfaces. Use when documentation for an operational workflow is requested. RU: ранбук, инструкция по эксплуатации.'
disable-model-invocation: true
---

# Operator runbooks

Use when the user requests documentation for an operational workflow. Identify the target system, audience, applicable project conventions and authorized documentation scope. Inspect the actual supported commands, configuration schema, running behavior and existing documentation to the extent permitted; distinguish a planned procedure, observed runtime and source-only inference.

Document prerequisites, safe operation sequence, expected observable results, failure interpretation, relevant authorization, rollback and escalation boundaries. Use placeholders or parameters for environment-specific paths, credentials, hosts and names; do not expose secrets or imply that example values identify the user's environment. Avoid inventing commands, services, tools, APIs or universal infrastructure assumptions.

Validate command syntax or examples through the supported project interface when authorized and practical, without running live mutations solely to prove documentation. Cite the actual evidence and state which procedure was not exercised. Preserve unrelated documents and generated artifacts.
