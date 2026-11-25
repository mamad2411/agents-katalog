---
name: logging-best-practices
description: Adds structured log lines with levels, correlation IDs and no personal data where they help. Use it when a service is hard to debug from its logs.
---

# Logging best practices

Log decisions and failures, not every step. Every line must help someone answer "what happened to this request?"

## Steps

1. Find the logger already in use (`grep -rn "logger\|logging\|pino\|winston\|slog" src`). Reuse it. Do not add a second library.
2. Locate the points that matter: request entry and exit, calls to other services and databases, retries, fallbacks, state changes, and every catch block.
3. Make sure a correlation ID exists. Read it from an incoming header such as `x-request-id` or create one at the edge, then attach it to the logger context so every line carries it.
4. Write each entry as structured key-value data with a short event name (`payment.declined`), not an interpolated sentence. Put variable data in fields.
5. Pick levels deliberately: ERROR only when someone should act, WARN for handled surprises, INFO for business events, DEBUG for detail that is off in production.
6. Log an error once, where it is handled, with the exception and stack. Do not log and rethrow at every layer.

## Never log

Passwords, tokens, API keys, session cookies, full card or national ID numbers, email addresses, or whole request bodies. Log an internal user ID or a masked value instead.

## Report

List the files changed, the events added with their levels, and any place where you found personal data already being logged.
