# SakAI — Cursor project rules

## Project snapshot

- **What:** Ride-hailing monorepo (passenger/driver Flutter apps, Go+Gin backend, OpenAPI contract, Postgres+PostGIS, Redis, WebSockets).
- **Vibe:** Production-minded, Clean Architecture on backend and mobile, explicit API contract (`openapi/`), Dockerized infra, security/phase-gated roadmap (see `overview.md`).

## Skill library (read skills before deep work)

The JSON registry and skill bodies for this workspace live under:

`./~/.agent/skills.json` → each entry’s `path` resolves to `./~/.agent/<path>/SKILL.md`

(On your machine you may also keep a copy under `$HOME/.agents`; treat `./~/.agent` as the source bundled with this repo.)

**How to activate:** When your cursor or edits match a row below, open the listed `SKILL.md` with the Read tool (or equivalent) and follow it for that task.

---

## Skill Mapping

Map file paths (relative to repo root) and file types to skills. Use **primary** skills first; **secondary** are optional depth.

| Context | Primary skills | Secondary / supporting |
|--------|----------------|------------------------|
| `backend/**/*.go`, `backend/go.mod`, `backend/go.sum` | `golang-pro`, `backend-architect`, `ai-engineer` | `go-concurrency-patterns`, `backend-security-coder`, `backend-dev-guidelines`, `software-architecture`, `verification-before-completion` |
| `backend/**/delivery/ws/**`, WebSocket / realtime / PubSub logic in Go | `golang-pro`, `backend-architect`, `api-patterns` | `go-concurrency-patterns`, `backend-security-coder` |
| `migrations/**/*.sql`, SQL schema / PostGIS | `postgresql`, `postgres-best-practices`, `database-migration` | `database-migrations-sql-migrations`, `sql-pro`, `database-design` |
| `openapi/**`, `**/swagger.yaml`, REST contract design | `openapi-spec-generation`, `api-documentation`, `api-design-principles` | `api-patterns`, `api-security-best-practices` |
| `mobile/**/*.dart`, `mobile/**/pubspec.yaml` | `flutter-expert` | `software-architecture`, `testing-patterns`, `verification-before-completion` |
| `docker-compose.yml`, `**/Dockerfile*`, container tooling | `docker-expert` | `backend-architect` |
| `docs/**`, roadmap, architecture narratives | `writing-plans`, `00-andruia-consultant` | `20-andruia-niche-intelligence` (after niche is known) |
| `admin/**/*.{tsx,ts,jsx,js}` (when present) | `react-best-practices`, `typescript-pro` | `react-state-management`, `web-design-guidelines` |
| `**/*three*`, `**/*.glb`, `**/*.gltf`, Three.js / R3F stacks | `3d-web-experience` | `web-performance-optimization` |
| Security reviews, handlers, auth, API hardening | `backend-security-coder`, `api-security-best-practices`, `api-security-testing` | `code-review-excellence` |
| Debugging failing tests / unclear failures | `debugging-strategies`, `debugging-toolkit-smart-debug` | `testing-qa` |
| New features spanning backend + clients + contract | `full-stack-orchestration-full-stack-feature`, `writing-plans` | `openapi-spec-generation`, `golang-pro`, `flutter-expert` |

### Andru.ia (Spanish workflow) skills

| When | Skill ID | Path (under `./~/.agent/`) |
|------|-----------|-----------------------------|
| Kickoff, architecture diagnosis, roadmap in Spanish | `00-andruia-consultant` | `skills/00-andruia-consultant` |
| Authoring or extending **agent skills** in-repo | `10-andruia-skill-smith` | `skills/10-andruia-skill-smith` |
| Domain intelligence (mobility / ride-hailing regulations, UX) | `20-andruia-niche-intelligence` | `skills/20-andruia-niche-intelligence` |

---

## Global expectations

- Prefer existing Clean Architecture boundaries (`domain` / `usecase` / `repository` / `delivery`) and Flutter’s domain/data/presentation split.
- Keep OpenAPI and generated Dart clients aligned with `CONTRIBUTING.md`.
- For work guided by Andru.ia skills, follow **Estándar de Diamante** (see `.cursor/rules/estandar-diamante.mdc`).
