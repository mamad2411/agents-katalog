# Project Skill Router

This file is the skill dispatcher for the repository.

## Skill Catalog (Call Only When Needed)
- `docs/skills/frontend-skill.md`: UI architecture, component composition, accessibility, frontend performance.
- `docs/skills/backend-skill.md`: service boundaries, API/domain flow, persistence and queue integration.
- `docs/skills/python-skill.md`: Python implementation, validation, API handlers, data and ML pipeline jobs.
- `docs/skills/rust-skill.md`: high-throughput pipelines, low-latency processors, memory-safe hot paths.
- `docs/skills/gateway-skill.md`: API Gateway, auth, routing policy, rate limiting, request shaping.
- `docs/skills/devops-skill.md`: deployment, CI/CD, observability, incident response, SLO operations.

## Invocation Policy
1. Default to no skill.
2. Call exactly one primary skill for focused tasks.
3. Call extra skill(s) only when the task crosses clear technical boundaries.
4. For mixed tasks, apply skills in this order:
   - `gateway` -> `backend` -> `python` or `rust` -> `devops` -> `frontend`

## Non-Negotiable Rules
- Keep code and docs production-ready and testable.
- Never hardcode environment or infrastructure values.
- Every decision point must include reason and measurable condition.
- Any signal/decision function must return:
  - TypeScript: `{ pass: boolean; reason: string; note?: string }`
  - Rust: `SignalResult { pass, reason, note }`

## Project North Star
- `docs/README.md`
- `docs/project-north-star.md`
