---
name: verify-implementation
description: Sample verify-implementation registry for the ADHD demo monorepo
---

# Verify Implementation (Sample Monorepo)

## Dynamic Coverage Registry

<!-- REGISTRY:START -->
| check_id | trigger_patterns | verification_command | evidence | status | last_updated |
| --- | --- | --- | --- | --- | --- |
| backend-pytest | backend/** | cd backend && python3 -m pytest tests/ -v --tb=short | baseline | active | 2026-01-01 |
| frontend-build | frontend/** | cd frontend && npm run build 2>&1 || echo 'build check' | baseline | active | 2026-01-01 |
| frontend-typecheck | frontend/src/** | cd frontend && npm run typecheck 2>&1 || echo 'typecheck' | baseline | active | 2026-01-01 |
| stub-detector | backend/app/** | grep -rn "NotImplementedError\|raise NotImplemented" backend/app/ && echo "STUBS FOUND" || echo "No stubs" | baseline | active | 2026-01-01 |
| gap-detector | backend/**<br>frontend/** | grep -rn "TODO\|FIXME\|HACK" backend/ frontend/src/ && echo "GAPS FOUND" || echo "No gaps" | baseline | active | 2026-01-01 |
<!-- REGISTRY:END -->
