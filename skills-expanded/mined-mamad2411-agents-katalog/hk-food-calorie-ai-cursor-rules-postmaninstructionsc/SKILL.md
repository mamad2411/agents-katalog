---
description: "Use when editing Postman collections, environments, globals, or fixture scripts."
globs: "postman/**"
alwaysApply: false
---

# Postman Workflow Rules

- Read `postman/README.md` first before changing requests, environment values, globals, or fixture setup scripts.
- Keep request paths and payload fields aligned with deployed edge-function contracts.
- If fixture object paths or setup commands change, update both `postman/setup-local-fixtures.sh` and `postman/README.md` in the same task.
- Prefer using `environments/Local Supabase.environment.yaml` variables (`baseUrl`, `userId`, `date`, `recordId`) rather than hardcoded values.
