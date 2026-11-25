---
name: enonic-webhook-integrator
description: Sets up Enonic XP event listeners, webhook configurations, and external system integrations triggered by content lifecycle events. Covers lib-event listener registration, node event filtering, outbound webhook configuration via com.enonic.xp.webhooks.cfg, custom HTTP service controllers for inbound webhooks, task-based async processing with lib-task, and outbound HTTP calls with lib-httpClient. Use when listening for content publish/create/update/delete events, configuring outbound webhooks, building HTTP service endpoints for inbound webhooks, or triggering async processing on content changes. Do not use for content querying, frontend component development, non-Enonic event systems, or GitHub webhook configuration.
license: MIT
metadata:
  author: webmaxru
  version: "1.3"
---

# Enonic Webhook Integrator

## Procedures

**Step 1: Detect the Enonic XP project**
1. Execute `node scripts/find-enonic-targets.mjs .` to locate Enonic XP project roots in the workspace.
2. If the script returns an empty array, stop and explain that no Enonic XP project was found.
3. If multiple projects are found, ask which project should receive the integration.
4. Identify the application key from `gradle.properties` (`appName`) or `build.gradle`.

**Step 2: Determine integration direction**
1. Classify the task as one of: *outbound event listener* (XP reacts to internal events and calls an external system), *outbound webhook config* (XP sends webhook payloads via built-in config), *inbound webhook endpoint* (XP receives payloads from an external system), or *mixed* (combination).
2. Read `references/event-reference.md` to identify the correct event types, listener patterns, and filtering strategies.
3. Read `references/webhook-reference.md` when the task involves outbound webhook configuration or inbound HTTP service endpoints.

**Step 3: Implement outbound event listener (if applicable)**
1. Read `assets/event-listener.template.ts` as a starting scaffold.
2. Register the event listener in the application's `main.ts` (or `main.js`) controller using lib-event's `listener()` function.
3. Use the `type` parameter with a pattern matching the target node events (e.g., `node.pushed`, `node.created`, `node.updated`, `node.deleted`).
4. Filter events by path within the callback by checking `event.data.nodes[].path` to restrict processing to the intended content tree.
5. When the listener must call an external HTTP endpoint, use lib-httpClient's `request()` function inside the callback or delegate to a background task.
6. For long-running processing, delegate work from the event callback to a background task using lib-task's `executeFunction()` to avoid blocking the event thread.
7. Read `references/examples.md` for complete integration patterns including CDN invalidation, search reindexing, and notification dispatch.

**Step 4: Configure outbound webhooks (if applicable)**
1. Read `references/webhook-reference.md` for the `com.enonic.xp.webhooks.cfg` configuration format.
2. Create or update the file at `XP_HOME/config/com.enonic.xp.webhooks.cfg` with webhook entries specifying the target URL and event types.
3. Validate that the configured event types match the intended content lifecycle events.
4. Use HTTPS URLs for webhook targets.
5. **Never write actual secret values into configuration files or source code.** Use descriptive placeholder tokens (e.g., `REPLACE_WITH_CDN_SECRET`) and instruct the operator to substitute real credentials out-of-band. Secrets must be managed by the operator through secure deployment pipelines, environment variables, or secret management tools—not committed to files.

**Step 5: Implement inbound webhook endpoint (if applicable)**
1. Read `assets/http-service.template.ts` as a starting scaffold.
2. Create an HTTP service controller at `src/main/resources/services/<serviceName>/<serviceName>.ts`.
3. Export a `post(req)` function that parses the incoming JSON payload from `req.body`.
4. Reject payloads exceeding a reasonable size limit (e.g., 1 MB) before parsing.
5. Validate the inbound payload by checking required fields, authentication headers, or HMAC signatures before processing.
6. Sanitize all string fields from the external payload before using them in content operations: trim whitespace, enforce maximum lengths, strip or escape HTML/script content, and reject values containing path traversal sequences (`..`, `/`, `\`).
7. Use an allowlist of expected field names rather than passing the raw payload object to content APIs.
8. Return appropriate HTTP status codes: `200` for success, `400` for malformed payloads, `401` for authentication failures, `413` for oversized payloads, `500` for unexpected errors.
9. When inbound payloads trigger content creation or modification, use lib-content or lib-node APIs within a context run to ensure proper permissions. Never pass unsanitized external values as content names, paths, or keys.

**Step 6: Wire async processing with lib-task (if applicable)**
1. When event handling or webhook processing requires heavy or time-consuming work, wrap it in `executeFunction()` from lib-task.
2. Report progress from long-running tasks using `progress()` to allow monitoring.
3. Read `references/event-reference.md` for the task event lifecycle (`task.submitted`, `task.updated`, `task.finished`, `task.failed`).

**Step 7: Validate the integration**
1. Execute `node scripts/find-enonic-targets.mjs .` to confirm the project still resolves correctly.
2. Verify that the event listener registration is in the application's `main.ts` or `main.js` file, which runs at application startup.
3. Confirm that outbound HTTP calls use HTTPS and include error handling for network failures and non-2xx responses.
4. Confirm that no actual secret values, API keys, or credentials appear in generated source code or configuration files—only placeholder tokens.
5. Confirm that inbound webhook endpoints sanitize and allowlist all fields from external payloads before passing them to content APIs.
6. If a webhook config file was created, confirm the event type patterns match the intended triggers.
7. Run the workspace build to verify no compilation errors.
8. Read `references/troubleshooting.md` when events do not fire, webhook deliveries fail, or inbound requests are rejected.

## Error Handling
* If `node scripts/find-enonic-targets.mjs .` finds no projects, confirm that `build.gradle` references `com.enonic.xp` plugins or that a `src/main/resources/site/` directory exists.
* If events do not fire after registering a listener, read `references/troubleshooting.md` to check listener registration location, event type patterns, and cluster vs. local event scope.
* If outbound HTTP calls fail, verify the target URL, network access from the XP instance, and that the operator has substituted placeholder tokens with real credentials.
* If inbound webhook requests return 404, confirm the service controller path follows `services/<name>/<name>.ts` and the application is deployed.
* If background tasks fail silently, check task state using `taskLib.list()` and inspect logs for errors within the task function.
