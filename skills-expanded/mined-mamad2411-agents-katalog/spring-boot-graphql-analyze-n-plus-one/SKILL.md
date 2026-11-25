---
name: spring-boot-graphql-analyze-n-plus-one
description: Analyze GraphQL N+1 query problems, DataLoader batching, caching, and downstream query amplification. Use for Spring Boot graphql design, implementation review, or runtime diagnosis.
---

# Analyze N Plus One

1. Read the service repository, `.digital-platform-ai/` metadata, environment context, and relevant service instructions.
2. Inspect framework configuration, code, contracts, tests, dependencies, and runtime wiring before drawing conclusions.
3. Gather runtime evidence from logs, traces, metrics, request IDs, model/tool telemetry, database/cache state, or downstream services when diagnostic.
4. Identify the first confirmed divergence from expected behavior.
5. Separate Spring framework behavior from provider/platform-specific behavior and route those concerns to the owning technology skill.
6. Preserve API/schema/session/business contracts unless redesign is explicitly requested.
7. Protect sensitive prompts, tokens, credentials, session data, and user information.
8. Do not mutate production resources unless explicitly authorized.

## Output
- Scope
- Code/Configuration Findings
- Runtime Evidence
- Root Cause or Design Assessment
- Recommended Action
- Remaining Unknowns
