# Control API Agent Rules

Validate and bound every input before domain execution. Keep route contracts centralized in `src/route-contracts.mjs`; do not scatter body, path, query, or response schemas through handlers.

Keep errors sanitized, use correlation-aware events, enforce workspace scope, and never turn an external request directly into a model or tool side effect. Boundary validation and OAF-008 authentication/authorization are distinct layers; protected route handlers must not run before both have succeeded.

Boundary order is request limits, route matching, path/query/header/body validation, correlation ID, credential extraction, authentication, workspace resolution, contextual policy evaluation, CSRF where applicable, domain handler, policy/audit event recording, response validation.

Route handlers must not call role maps directly. Build trusted policy inputs from the authenticated principal and current membership only; never accept role, environment, or policy fields from request bodies.

When adding a route, update the runtime registry, OpenAPI, protocol schemas or examples when the wire contract changes, and adversarial tests proving invalid requests do not invoke stores, workflows, tools, models, artifacts, or migrations.
