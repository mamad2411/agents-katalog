---
name: security-privacy-review
description: 'Review secret handling, redaction, no-read and privacy claims across application boundaries. Use for credential loading, sensitive-data redaction or "secrets never reach logs" claims. RU: приватность, секреты в логах.'
license: MIT
disable-model-invocation: true
---

# Privacy boundary review

Use for an authorized review of credential loading, sensitive-data redaction, or claims that source bodies, identifiers or secrets do not cross persistence, logs, responses, telemetry, filesystem or transport boundaries. Define the allowed scope first and distinguish **no body read**, **no disclosure**, and **no mutation**: evidence of one is not proof of the others.

Trace each representation before and after normalization, hooks, hashing, storage and output. For telemetry include logs, spans, events, metric labels and every exporter separately. Redaction must happen before any forbidden boundary; sanitizing a final log cannot undo earlier exposure. Review exact configured sinks and use synthetic sentinels, keeping secret values and raw payloads out of command output, reports and delegated work.

For dotenv and credential source precedence use [configuration sources](references/configuration-sources.md); for runtime and no-read proof use [privacy evidence](references/privacy-evidence.md); for a source-only credential inventory use [source evidence](references/source-evidence.md). This review does not authorize reading secret stores, testing live credentials, changing accounts or modifying code.
