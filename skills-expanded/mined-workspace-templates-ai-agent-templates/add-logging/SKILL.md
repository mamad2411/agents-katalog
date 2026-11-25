---
name: add-logging
description: Adds structured log lines to one flow at the points that help debugging, with levels, context fields and no sensitive data.
disable-model-invocation: true
---

Add structured logging to this flow: $ARGUMENTS

1. Find the project's logger (winston, pino, structlog, logging, slog, zap, log4j) and one well-logged file. Match its import, field names and level usage. If there is no logger, stop and ask before adding a dependency.
2. Trace the flow from entry to exit. Mark: start and end with duration, each external call, each branch that changes the outcome, retries, and every caught error.
3. Choose levels: debug for internals, info for business events, warn for recovered problems, error for failures with the cause attached.
4. Log fields, not sentences: request id, user id, order id, counts, elapsed ms. Reuse a correlation id if one exists.
5. Never log passwords, tokens, card numbers, full emails, request bodies or raw headers. Redact or log only an id.
6. No logging inside tight loops.

Show the diff plus a list of the lines added with their level. Run the tests. Ask before changing logger configuration.
