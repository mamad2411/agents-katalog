---
name: onflou-spring-conv-code
description: Use when implementing, reviewing, refactoring, or planning Spring backend code for Onflou projects and the user asks about code convention, layer boundaries, package structure, Controller/Service/Mapper roles, DTO/model naming, DB/MyBatis rules, response format, exception handling, logs, security, or backend quality standards. Loads the Onflou Spring convention resources from MCP before changing or judging backend code.
---

# Purpose

Apply Onflou Spring backend code conventions consistently before backend implementation, review, refactor, or planning.

# MCP-First Rule

Read convention resources from `agent_mcp` first. Local files are fallback/runtime mirrors only.

# Required Knowledge

Read only the resources relevant to the task:

- Spring code convention: `ai-workspace/70-knowledge/company/onflou/internal/SPRING_BACKEND_STANDARD_v1.0/SPRING BACKEND STANDARD (v1.0)/Policy/코드 컨벤션.md`
- Spring layer/package guide: `ai-workspace/70-knowledge/company/onflou/internal/SPRING_BACKEND_STANDARD_v1.0/SPRING BACKEND STANDARD (v1.0)/Guide/레이어 & 패키지 구조 가이드.md`
- Spring REST API guide: `ai-workspace/70-knowledge/company/onflou/internal/SPRING_BACKEND_STANDARD_v1.0/SPRING BACKEND STANDARD (v1.0)/Guide/REST API 가이드.md`
- Spring DB naming guide: `ai-workspace/70-knowledge/company/onflou/internal/SPRING_BACKEND_STANDARD_v1.0/SPRING BACKEND STANDARD (v1.0)/Guide/DB 네이밍 규칙.md`
- Spring DB policy: `ai-workspace/70-knowledge/company/onflou/internal/SPRING_BACKEND_STANDARD_v1.0/SPRING BACKEND STANDARD (v1.0)/Policy/DB 정책.md`
- Spring CRUD query policy: `ai-workspace/70-knowledge/company/onflou/internal/SPRING_BACKEND_STANDARD_v1.0/SPRING BACKEND STANDARD (v1.0)/Policy/CRUD 쿼리 정책.md`
- Spring response format policy: `ai-workspace/70-knowledge/company/onflou/internal/SPRING_BACKEND_STANDARD_v1.0/SPRING BACKEND STANDARD (v1.0)/Policy/응답 포멧 정책.md`
- Spring exception policy: `ai-workspace/70-knowledge/company/onflou/internal/SPRING_BACKEND_STANDARD_v1.0/SPRING BACKEND STANDARD (v1.0)/Policy/예외 처리 정책.md`
- Spring log policy: `ai-workspace/70-knowledge/company/onflou/internal/SPRING_BACKEND_STANDARD_v1.0/SPRING BACKEND STANDARD (v1.0)/Policy/로그 정책.md`
- Spring security policy: `ai-workspace/70-knowledge/company/onflou/internal/SPRING_BACKEND_STANDARD_v1.0/SPRING BACKEND STANDARD (v1.0)/Policy/보안 정책.md`

# Workflow

1. Identify whether the task is implementation, review, refactor, or planning.
2. Read the smallest relevant MCP convention resources before touching backend code.
3. Check existing project patterns and preserve them when they do not conflict with Onflou conventions.
4. Enforce one-way layer flow: `Controller -> Service -> Mapper`.
5. Keep Controller thin: request handling, validation, service call, response only.
6. Keep business logic in Service; put CUD flows in transactions and read flows in read-only transactions when appropriate.
7. Keep Mapper/MyBatis focused on SQL execution only; no business logic in mapper interfaces or XML.
8. Keep DTO and Model separate; use `XxxRequest`, `XxxResponse`, and model names with clear domain meaning.
9. Keep packages lowercase and domain-oriented; keep `global` common-only and `infra` external-integration-only.
10. Use global exception handling for response conversion; do not scatter try/catch or swallow exceptions.
11. Review DB naming, CRUD query shape, response format, log policy, and security policy when the task touches those surfaces.
12. Document convention conflicts or missing business rules in MCP-backed shared state when they affect the decision.

# Quick Checks

- No Controller -> Mapper direct call.
- No business logic in Controller or Mapper.
- No DTO/Model naming mix such as `VO`, `Entity`, or vague `Data` unless existing project convention requires it.
- No wildcard imports.
- CUD transaction boundary is explicit.
- Response and exception handling follow the project/global pattern.
- Logs avoid sensitive data and follow policy.

# Output

- Backend implementation/review guidance aligned with Onflou Spring conventions.
- Exact convention resources consulted.
- Verification notes and remaining risk.
