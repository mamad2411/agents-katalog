---
name: roadguard-postman
description: Use when a RoadGuard API is added, changed, removed, or prepared for manual or collection-run testing.
---

# RoadGuard Postman workflow

Use this skill with endpoint delivery whenever an API contract changes. Read `AGENTS.md`, `planning/V2/TASK_LIFECYCLE.md`, the assigned task/Source evidence, directly changed controller/DTO/auth policy and immediate dependency, actual DbInitializer/seed and existing Postman artifacts.

## Required workflow

Follow `IMPLEMENT -> UPDATE_POSTMAN -> REVIEW_FIX -> VERIFY -> REPORT`. Postman is part of completion for any change to method, route, request/response schema, auth, headers, stable errors, or direct setup dependency. Keep `Controller -> IService -> IRepository` unchanged.

1. Compare the running/source contract with the existing collection. Do not create requests for planning-only APIs or infer undocumented behavior.
2. Prefer `docs/postman/RoadGuardSystem-V2.postman_collection.json`; preserve request names/IDs, folders, scripts and variables outside the task. Add or update the matching request, description, examples and dependency order.
3. Keep environment configuration in `docs/postman/RoadGuard.local.postman_environment.json`. Commit placeholders only; never copy SQL credentials, JWTs, refresh tokens or real passwords into JSON, logs or documentation.
4. Describe every request: purpose, allowed role, setup/input, expected status/body/errors, and whether it changes data. Separate independent requests from ordered scenarios and blocked/manual steps.
5. Use seeded accounts only after checking the actual Development `DbInitializer`/seed. Store each role's token separately. Capture IDs/row versions only after a successful response. Do not reset shared seed accounts or silently overwrite user variables.
6. Write meaningful assertions for status, content type/payload, stable error codes, authorization and idempotency where the contract supports them. Do not claim Postman proves SQL rollback or concurrency without backend evidence.
7. Validate JSON, v2.1 schema fields, duplicate request names/IDs, unresolved variables, URLs, headers, bodies and dependency references. If runtime execution is unavailable, report `NOT_RUN` or `BLOCKED` with the reason.

After `roadguard-review-autofix` changes an API contract, re-run this update for affected requests before reporting completion. Record static/runtime Postman evidence separately in task completion history and update `verificationStatus` honestly. Do not ask the user to repeat “add Postman” for a normal API task; ask only for a missing contract, business decision or required permission.
