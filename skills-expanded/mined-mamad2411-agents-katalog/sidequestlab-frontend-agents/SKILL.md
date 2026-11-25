# AGENTS — Private App (Angular)

`frontend/` is the private Angular app, including the login entry and guarded MemoQuiz routes. Public website pages belong in `apps/public-site/`.

## Generated OpenAPI client (critical)

- The OpenAPI TS client lives in: `frontend/src/app/api/**`
- NEVER edit it manually.
- If API changes require regen:
  - `cd frontend && npm run generate:api`
  - Then validate with: `ALLOW_GENERATED_API_CHANGES=1 ./scripts/check.sh`

## Coding conventions

- Keep existing UX unless asked.
- UI must use Angular Material components by default. Do not introduce other UI libraries unless explicitly requested.
- Target: Angular (project version), use modern control flow (@if/@for) and inject().
- Add minimal `loading` + `errorMessage` when wiring to API.
- Avoid wide refactors; touch only the screen/slice requested.

## Commands (reference)

- `cd frontend && npm run lint`
- `cd frontend && npm run build`
- (optional) `cd frontend && npm test -- --watch=false`
- Final gate remains: `./scripts/check.sh` (repo root)
