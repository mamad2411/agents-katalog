---
name: portfolio-integration-auditor
description: "Guidelines for enforcing Contract-Driven Parallel Execution between frontend and backend agents."
---
# Portfolio Integration Auditor

To prevent bottlenecking, Frontend and Backend development should occur in parallel, governed by a strict API contract.

## Standard Operating Procedure

1. **The Contract:** Before any implementation begins, the Orchestrator must define a strict API contract (e.g., shared TypeScript types, OpenAPI schema, or a mock JSON payload) outlining exactly how the Frontend and Backend will communicate.
2. **Parallel Deployment:** The Orchestrator invokes both a Frontend sub-agent and a Backend sub-agent simultaneously.
3. **Model Selection:** Use the `flash` model tier for standard CRUD backend routes and basic React UI consumption, optimizing for speed and efficiency.
4. **Validation:** An Integration Auditor agent (or the Orchestrator) must verify that the Next.js BFF data fetching logic perfectly matches the FastAPI response schema before finalizing the feature.
