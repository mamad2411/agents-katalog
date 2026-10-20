# CLAUDE.md — auth-service

> Loaded when working inside `services/auth/`. See root `CLAUDE.md` for shared conventions.

Placeholder — populated in Phase 3 (register/login, JWT issuing). Owns: `users`, `roles`,
`user_roles`. Identity only — other services validate JWTs themselves, never call auth for authz.
