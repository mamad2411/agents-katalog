---
name: add-health-check
description: Adds liveness and readiness endpoints that test real dependencies with short timeouts, so orchestrators restart the right things.
disable-model-invocation: true
---

Add health endpoints to this service. Dependencies to include: $ARGUMENTS (detect them from config if empty).

1. Read the app entry point, config and client setup to list real dependencies: database, cache, queue, object storage, upstream APIs.
2. Add `GET /livez`: returns 200 with no dependency calls. It only proves the process responds.
3. Add `GET /readyz`: runs one cheap check per required dependency in parallel (for example `SELECT 1`, a cache PING), each with a 1 to 2 second timeout. Return 200 when all pass, otherwise 503 with JSON like {"status":"degraded","failed":["database"]}.
4. Mark optional dependencies as non-fatal so a flaky analytics API does not take the service out of rotation.
5. Never include secrets, hostnames, stack traces or version numbers in the body. Skip auth on these routes but do not expose them publicly if the platform supports an internal port.
6. Reuse existing connections; do not open a new pool per probe.
7. Add tests for all-healthy and one-dependency-down, then run them. Show the probe snippet for the deploy config and ask before editing it.
