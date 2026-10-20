# Quick Capture — Agent Guide

Quick Capture is a Turborepo monorepo for capturing notes (camera, voice, manual entry) and turning them into todos via AI extraction and a review step before save.

**Before writing mobile code:** Read the versioned Expo docs at https://docs.expo.dev/versions/v56.0.0/ — this project uses **Expo SDK 56**.

## Project overview

| Package | Path | Purpose |
| --- | --- | --- |
| `@quick-capture/mobile` | `apps/mobile/` | Expo React Native app (Expo Router) |
| `@quick-capture/api` | `apps/api/` | Hono TypeScript API (Railway in prod) |
| `@quick-capture/shared` | `packages/shared/` | Shared types + Zod schemas |
| `@quick-capture/typescript-config` | `packages/typescript-config/` | Shared tsconfig bases |
| Native (future) | `native/watch/`, `native/wear/` | Apple Watch / Wear OS companions |

**Roadmap:** [PLAN.md](./PLAN.md)  
**Architecture:** [docs/architecture.md](./docs/architecture.md)  
**Monorepo commands:** [docs/monorepo.md](./docs/monorepo.md)  
**Feature specs:** [docs/features/](./docs/features/)

## Commands (run from repo root)

```bash
npm install                  # Install all workspaces
npm run dev:mobile           # Expo dev server
npm run dev:api              # API at http://localhost:3000
npm run dev                  # Mobile + API in parallel
npm run build                # Build shared + api (turbo cache)
npm run typecheck            # Typecheck all packages
npm test                     # Unit tests (all workspaces)
npm run docker:dev           # Full stack in Docker (main checkout)
npm run worktree:bootstrap   # Linked worktree: Neon branch + .env.worktree
npm run worktree:create      # New linked worktree: git worktree add + bootstrap
npm run docker:dev:worktree  # Docker stack for current worktree
```

Copy `.env.example` to `.env` for local env vars. Mobile env uses `EXPO_PUBLIC_*` prefix.

**Parallel worktrees:** Always `cd` into the linked worktree before `worktree:bootstrap` or `docker:dev:worktree`. Main checkout uses `npm run docker:dev`. See [docs/features/worktree-dev.md](./docs/features/worktree-dev.md).

## Core product flows

1. **Manual todo** — Todos tab → Add → modal → save locally
2. **Camera capture** — Capture tab → photo → AI extract → review modal → save
3. **Voice capture** (planned) — mic button → record → transcribe + extract → review → save
4. **Cloud sync** (planned) — Neon Auth + sync todos/captures when logged in

All AI-generated todos go through **review before save**. Never skip the review step for capture flows.

## Code conventions

### Monorepo boundaries

- **Routes only** in `apps/mobile/app/` — no components, hooks, or utils co-located there
- **Shared types/schemas** live in `packages/shared/` — update Zod + TypeScript together
- **Mobile imports:** `@/` → `apps/mobile/*`; cross-package → `@quick-capture/shared`
- **Native watch/wear** code goes in `native/`, not npm workspaces

### Mobile (`apps/mobile`)

- Kebab-case filenames (`capture-camera.tsx`, `add-todo-form.tsx`)
- Use `PlatformColor` for system-aware styling; `contentInsetAdjustmentBehavior="automatic"` on scroll lists
- `expo-camera`, `expo-audio` (not legacy `expo-av`); `expo-sqlite` for local persistence
- `TodoSource`: `manual` | `capture` | `voice` | `watch` (defined in shared)
- Metro monorepo config: `apps/mobile/metro.config.js` — rebuild shared before testing workspace imports:
  `npm run build --workspace=@quick-capture/shared`

### API (`apps/api`)

- Hono + ESM (`"type": "module"`)
- Validate request bodies with Zod schemas from `@quick-capture/shared`
- Auth via **Neon Auth** (email/password, Google, GitHub); JWT verification in Hono — see [docs/features/auth.md](./docs/features/auth.md)

### When adding a feature

1. Check [PLAN.md](./PLAN.md) for phase and priority
2. Read or create `docs/features/<feature>.md`
3. Add types/schemas to `packages/shared` if used by mobile + API
4. Update PLAN.md when shipping

## Key files

| Area | Files |
| --- | --- |
| Todo state | `apps/mobile/hooks/use-todos.ts`, `apps/mobile/utils/db.ts`, `todo-repository.ts`, `todo-store.ts` |
| AI extraction | `apps/mobile/services/ai-extract-todos.ts` |
| Review modal | `apps/mobile/app/review-todos.tsx` |
| Shared types | `packages/shared/src/todo.ts`, `api-schemas.ts` |
| API entry | `apps/api/src/index.ts` |
| Tab layout | `apps/mobile/app/(tabs)/_layout.tsx` |

## Testing changes

```bash
npm run typecheck                                    # All packages
npm test                                             # Unit tests — see docs/features/unit-testing.md
npm run build --workspace=@quick-capture/shared      # After shared changes
curl http://localhost:3000/health                    # API health
```

Run Expo from root via `npm run dev:mobile` or from `apps/mobile/` with `npx expo start`. Try **Expo Go** first; use dev client / EAS only when native modules require it.

## Recommended skills

Use these **existing skills** (install or enable in Cursor) when working in the matching area:

### Mobile / Expo (use frequently)

| Skill | When to use |
| --- | --- |
| `building-native-ui` | Expo Router, tabs, camera, storage, styling, navigation patterns |
| `vercel-react-native-skills` | React Native performance, lists, gestures |
| `expo-dev-client` | Custom native builds, TestFlight dev clients |
| `expo-deployment` | EAS Build, store submission |
| `expo-cicd-workflows` | CI/CD for Expo |
| `upgrading-expo` | SDK upgrades |

### Backend / infra (Phase 3+)

| Skill | When to use |
| --- | --- |
| Vercel `auth` plugin skill | Better Auth / OAuth patterns (Neon Auth is Better Auth–based) |
| Vercel `vercel-functions` / `runtime-cache` | If adding edge/serverless endpoints |
| `deploy-on-aws` `deploy` skill | Alternative hosting; primary target is **Railway + Neon** |

### Quality / workflow

| Skill | When to use |
| --- | --- |
| `quick-capture-worktree` | Creating linked worktrees, parallel Docker stacks, `worktree:bootstrap` |
| `create-skill` | Adding project-specific skills below |
| `split-to-prs` | Large changes spanning mobile + api + shared |
| `review-bugbot` | PR review before merge |
| `review-security` | Auth, API keys, OAuth, upload endpoints |
| `gh-fix-ci` | Fixing GitHub Actions failures |

### Wearables (Phase 5)

| Skill | When to use |
| --- | --- |
| `building-native-ui` (media + storage refs) | Audio recording patterns |
| `@bacons/apple-targets` docs | Apple Watch SwiftUI companion in `native/watch/` |

**Note:** Nothing CMF Watch Pro does **not** support third-party watch apps — use Android phone shortcuts instead (see planned `docs/features/cmf-watch-android-shortcuts.md`).

## Suggested project skills to create

Create these under `.cursor/skills/` in this repo so all contributors get the same context:

| Skill name | Purpose |
| --- | --- |
| `quick-capture-feature` | Read PLAN.md + `docs/features/` before implementing; update specs when done |
| `quick-capture-shared` | How to add types + Zod schemas in `packages/shared` and rebuild |
| `quick-capture-capture-flow` | Camera/voice → AI service → review modal → `useTodos` pipeline |
| `quick-capture-api` | Hono route patterns, shared validation, Neon Auth JWT middleware + Drizzle |
| `quick-capture-monorepo` | Turbo filters, workspace deps, Metro gotchas |
| `quick-capture-worktree` | Git worktrees, Neon branch per checkout, `docker:dev:worktree` |

Use the `create-skill` skill to scaffold these. Each should link to the relevant `docs/features/*.md` spec.

## Do not

- Put components or business logic inside `apps/mobile/app/` (routes only)
- Commit `.env` or API keys; use `.env.example` as template
- Skip review modal for AI-extracted todos
- Use `AsyncStorage` or legacy `expo-av` — use `expo-sqlite` and `expo-audio`
- Edit `.cursor/plans/*.plan.md` unless explicitly asked — update [PLAN.md](./PLAN.md) and `docs/` instead
- Assume Wear OS apps run on Nothing CMF Watch (proprietary OS, no app store)

## Current priority

**Phase 1:** Voice capture — see [docs/features/voice-capture.md](./docs/features/voice-capture.md)

**Phase 3 (next major):** Neon Auth + todo sync in Neon Postgres; API JWT auth in Hono — see [docs/features/auth.md](./docs/features/auth.md).

## Cursor Cloud specific instructions

The startup update script runs `npm install` and builds `@quick-capture/shared`. Standard commands live in the **Commands** section above; the notes below are non-obvious caveats for this headless Linux VM.

- **Build `packages/shared` before running any dev server.** Turbo's `dev` task has no `^build` dependency, so `npm run dev:api` / `dev:web` import `@quick-capture/shared` from its compiled `dist/` and fail if it was never built. The update script handles the first build; after editing `packages/shared` rebuild it with `npm run build --workspace=@quick-capture/shared`.
- **API runs standalone with `.env` copied from `.env.example`.** It boots fine with no DB/auth/AI keys. Expected behavior without secrets: `GET /api` reports `sync:false, auth:false`; `/api/todos` (and other sync routes) return `503 Database is not configured`; `/api/ai/extract/*` return a `400` provider-key error. These are not bugs — they are gated features. Set `DATABASE_URL`, `NEON_AUTH_URL` (API JWKS), and `OPENAI_API_KEY`/`MINIMAX_API_KEY` to enable them.
- **Mobile app cannot be exercised headlessly in this VM.** `npm run dev:mobile` (Metro) starts, but: (1) Expo **web** crashes at runtime because the app uses `PlatformColor`, which `react-native-web` does not implement (`PlatformColor is not a function`); (2) there is **no Android SDK and no `/dev/kvm`**, so an emulator cannot run. Verifying mobile UI requires a physical device via Expo Go / an EAS dev build. Use the API + shared schemas to validate logic from the VM.
- **Web companion (`npm run dev:web`) needs TLS certs and Neon Auth for its real flow.** The `dev` script uses `--experimental-https` and reads `apps/web/certificates/localhost-key.pem` + `localhost.pem`, which are gitignored and absent on a fresh VM — generate them per [docs/docker-dev.md](./docs/docker-dev.md) (one-time `openssl`/mkcert), or run plain HTTP with `npm run dev:docker:http --workspace=@quick-capture/web`. Every app route is auth-gated: without `NEON_AUTH_BASE_URL` + `NEON_AUTH_COOKIE_SECRET` the middleware redirects to `/auth/sign-in` and there is no guest/offline todo mode (todos are 100% API-backed). The sign-in page itself renders without secrets, which is enough to confirm the frontend builds/serves.
- **Docker is not installed in this VM.** Run services natively via the npm scripts above; `docker:dev`/`docker:dev:worktree` (whisper.cpp STT, migrate) are unavailable here.
