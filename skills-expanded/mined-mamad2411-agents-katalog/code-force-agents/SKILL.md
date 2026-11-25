# SheCare - Agent Operating Instructions

> Read this file before any code change. The full rule sets live in
> `backend_rules.md` (Python/FastAPI) and `frontend_rules.md` (React Native).
> This file distills the **non-negotiable invariants** that must hold on
> every commit. If a change violates any of these, it should be rejected
> in review.

---

## 0. Two rule sets, one product

| Domain | Authoritative rules | Stack |
|--------|---------------------|-------|
| Backend (`/backend`) | `backend_rules.md` | Python 3.11+, FastAPI, SQLAlchemy 2.x async, Alembic, Pydantic v2, Celery, Redis, PostgreSQL 15+ |
| Mobile (`/mobile`) | `frontend_rules.md` | React Native (TypeScript strict), React Navigation 7, Zustand, TanStack Query, Reanimated 3, react-hook-form + zod |

The bridge between them is `plans/30-mobile-api-contract.md`.

---

## 1. Backend invariants (from `backend_rules.md`)

### 1.1 Package by feature, NOT by layer

```
app/
  core/                  # config, database, security, event_bus, encryption, exceptions
  integrations/          # twilio, stream_chat, fcm, s3, huggingface
  modules/<feature>/     # one folder per feature, each self-contained
    routes.py            # thin: parse request, return response, delegate to service
    services.py          # business logic, DB queries, no HTTP types
    models.py            # SQLAlchemy models owned by THIS module
    schemas.py           # Pydantic Create / Update / Response / InDB
    dependencies.py      # FastAPI dependencies (get_current_user, get_service)
    tasks.py             # Celery tasks owned by THIS module
    exceptions.py        # ModuleNameError + NotFoundError / ValidationError / ConflictError
  tasks/                 # global_tasks only (cleanup, etc.)
  main.py                # FastAPI app factory
  lifespan.py            # startup / shutdown
tests/
  conftest.py
  modules/<feature>/test_*.py
```

**Forbidden:** `app/models/`, `app/routers/`, `app/services/` flat-by-layer layouts.
**Forbidden:** a module importing another module's `services` directly — emit an event on the event bus instead.

### 1.2 Routes are thin, services are HTTP-free

Routes parse, validate, call one service function, format response. No business logic in routes.
Services return domain objects or raise module-specific exceptions. Services NEVER see `Request` or `HTTPException`.

### 1.3 Dependency injection everywhere

External dependencies (DB session, Redis, Twilio, FCM, Stream, HuggingFace) are injected via FastAPI `Depends`. No global singletons imported from inside a module. Singletons live in `core/dependencies.py` and are registered via `lifespan`.

### 1.4 Database conventions

- UUID primary keys on all tables (except pure join tables).
- Module owns its tables; another module cannot read/write them directly. FK between modules is allowed; cross-module cascade delete is FORBIDDEN.
- Indexes, CHECK constraints, JSONB + GIN indexes live in the module's `models.py`.
- One Alembic migration per logical change, prefixed with module name (`cycle_add_symptoms_jsonb.py`).
- Migrations must be reversible (downgrade defined) unless destructive, in which case document it.
- Always run migrations BEFORE deploying the new code that depends on the schema (rule §17.3).
- Soft delete via `is_active` flag, not hard delete.

### 1.5 Configuration

- All config in `app/core/config.py` using Pydantic `BaseSettings` with nested classes per concern.
- No hardcoded URLs, secrets, or thresholds in modules.
- Secrets NEVER committed. Use env vars in dev, AWS Secrets Manager in prod.

### 1.6 Errors & exceptions

- Each module defines a base `ModuleNameError` plus specific subtypes.
- Routes catch only module exceptions and convert to HTTP. Global exception handler catches everything else.
- Celery tasks catch and log, then decide retry based on exception type.

### 1.7 API versioning

- All endpoints under `/api/v1/...`. New breaking features go to `/api/v2/`.
- Pydantic schemas are split: `*Create` (POST), `*Update` (PUT/PATCH, fields optional), `*Response` (GET, includes `id`, `created_at`), `*InDB` (internal, may hold sensitive fields). Never reuse one schema for both request and response.

### 1.8 Celery rules

- Tasks live in the owning module's `tasks.py`. Global tasks in `app/tasks/`.
- Tasks MUST be idempotent — running twice must not cause inconsistency. Use `task_id` based on business key, e.g. `f"analyze_journal_{journal_id}"`.
- Tasks MUST NOT call other tasks synchronously. Use `chain`, `chord`, or `send_task` with `apply_async`.
- Every task has `soft_time_limit` and `time_limit`.
- Dead-letter exchange for tasks that exhaust retries.

### 1.9 Event-driven cross-module communication

```
event_bus.emit("period_started", user_id=...)
# subscriber in another module:
@event_bus.subscribe("period_started")
def on_period_started(user_id): ...
```

Subscribers are defined in the subscriber's module, not the emitter's. For async work, the subscriber enqueues a Celery task.

### 1.10 Testing

- `tests/modules/<feature>/test_*.py` mirrors the module layout.
- `conftest.py` per module.
- Mock external services (Twilio, FCM, Stream) at the module boundary with `pytest-mock`. Do NOT mock internal service functions — use a real instance against a test DB.
- 80% coverage target enforced in CI.

### 1.11 Logging & observability

- Structured JSON logs (structlog) with `request_id` and `user_id` (when authenticated).
- Per-module logger: `logging.getLogger("app.modules.<feature>")`.
- Levels: INFO for request start/end (no body), DEBUG for SQL / external request/response, WARNING for rate-limit hits, ERROR for exceptions and permanent external failures.

### 1.12 Security

- Row-level permission: never trust `user_id` from request body. Always use `current_user.id` from auth.
- Encryption / decryption of sensitive fields (journal content, medical notes) happens in the SERVICE LAYER, not in routes or models. Use the shared `encryption_service` from `core/`.
- Rate limiting via `@rate_limit(limit=100, window=60)` decorator per endpoint, configured per-module in `dependencies.py`.

### 1.13 Module pluggability

- Each module may expose `init_module(app, event_bus)` for routes + subscribers + lifespan hooks, called from `app/main.py`.
- Commenting out a module's import must not break the rest of the app. Use `try/except ImportError` for optional dependencies.

### 1.14 Code quality gates

- `black` for formatting, `isort` for imports, `ruff` for linting, `mypy --strict` for types.
- Max line length 100.
- Type hints on every function argument and return.
- CI fails on any module importing another module's service directly — enforced by `import-linter`.

### 1.15 External service clients

- Each external API wrapped in a client class in `app/integrations/` (`TwilioClient`, `FCMClient`, `StreamClient`, `S3Client`, `HuggingFaceClient`).
- Clients own retry, circuit breaker, and timeout. The rest of the code only uses the client.

---

## 2. Frontend invariants (from `frontend_rules.md`)

### 2.1 Navigation

- Hybrid: bottom tabs for primary modules (Wellness, Cycle, Pregnancy, Safety, Profile), native stack for nested screens, separate auth stack for unauthenticated.
- `src/screens/<feature>/...` mirrors backend modules.
- Predefined param types in TypeScript for compile-time safety.
- Navigation state in Zustand only for deep linking / restoring after kill — NOT for transient UI state.

### 2.2 State management (three layers, three tools)

| What | Tool |
|------|------|
| Global app state (auth, profile, feature flags) | Zustand |
| Server state (fetch / cache / background refresh) | TanStack Query (React Query) — NEVER put API responses in Zustand |
| Persistent local (preferences, drafts, cached predictions) | AsyncStorage **encrypted with `react-native-encrypted-storage`** |
| Transient UI (modal open, form input) | `useState` / `useReducer` inside the component |
| Offline actions queue | Custom hook backed by AsyncStorage; sync when connection resumes |

### 2.3 Styling

- Pick ONE: `styled-components` OR NativeWind (Tailwind for RN). Do not mix.
- Central `theme/` folder: colors, typography, spacing (4-px grid: 4/8/12/16/24/32/48), border-radius (sm/md/lg/xl), shadows, dark mode tokens.
- Light + dark mode via `useColorScheme` with NO layout shifts.
- NO inline styles in components. NO hardcoded colors / spacing. Reuse theme values.
- Semantic color names (`color.primary`), not literal (`color.blue500`).

### 2.4 Component design

- Shared library in `src/components/ui/`: Button, Card, Input, Modal, BottomSheet, Toast, Loader, EmptyState, Calendar, MoodPicker, SymptomGrid.
- Atomic design: atoms (Button/Text/Icon), molecules (FormField), organisms (PeriodLogCard), templates (ScreenLayout).
- Every component must be accessible, responsive, and reusable.
- Touch targets ≥ 44 × 44 pt (Apple HIG).

### 2.5 Forms

- `react-hook-form` + `zod` for every form. Schemas live in `src/validation/` and are SHARED with the backend's Pydantic schemas when possible.
- Auto-save journal drafts to encrypted AsyncStorage every 30 s; show "Draft saved" toast.
- Use native date pickers (`@react-native-community/datetimepicker`).
- Validate on BOTH sides. Frontend validation gives instant feedback.

### 2.6 Animations

- Reanimated 3 for everything complex. Avoid the legacy `Animated` API.
- Micro-interactions: button press scale to 0.96, list swipe actions, pull-to-refresh with haptics, tab cross-fade.
- Skeleton placeholders for every async fetch (`react-native-skeleton-placeholder`).
- Lottie for breathing visual, pregnancy milestones — pre-load.
- Honor `useReducedMotion`.

### 2.7 Performance

- `FlatList` (not `ScrollView`) for > 5 items. Use `getItemLayout`, `initialNumToRender={7}`, `maxToRenderPerBatch={10}`.
- Memoize hot components (`React.memo`, `useMemo`, `useCallback`). No inline functions in render.
- Hermes engine (default RN 0.70+).
- Lazy load screens with `React.lazy` + `Suspense`.
- `FlashList` for very long lists (chat messages).
- `react-native-fast-image` for images, WebP, proper dimensions.
- Keep state as local as possible.

### 2.8 Gestures & sensors

- `react-native-gesture-handler` for all custom gestures.
- SOS double-click power button via `react-native-power-button` (or floating-action-button fallback for older devices).
- Request sensor / GPS permission AT THE MOMENT OF USE, not at app start.
- Vibration guides for breathing exercises.

### 2.9 Error handling

- `react-native-toast-message` for non-critical feedback (platform-correct position).
- Critical errors (SOS failed) → modal with retry + manual emergency-call action.
- Global error boundary with friendly fallback + Restart button.
- Sentry only AFTER user consent.

### 2.10 Accessibility

- `accessibilityLabel`, `accessibilityRole`, `accessibilityHint` on every interactive element.
- Dynamic type / font scaling supported. Use `react-native-size-matters` for spacing; allow text to scale with system.
- Contrast ratio ≥ 4.5:1 normal, 3:1 large.
- `accessibilityLiveRegion` to announce important changes ("SOS activated").

### 2.11 Offline & network

- `persistQueryClient` + AsyncStorage for cached API responses; serve stale-while-revalidate.
- `@react-native-community/netinfo` for connectivity. Show offline banner.
- Offline action queue: journal entries, mood logs, period logs. Sync last-write-wins on reconnect.
- SOS: try API; if offline, keep retrying locally AND offer native SMS as last resort.

### 2.12 Push notifications

- Request permission AFTER login, not at app open.
- Foreground: in-app toast (not system banner).
- Deep-link from notification to relevant screen.
- Android 8+ channels, iOS critical alerts for SOS.

### 2.13 Security (client side)

- Auth tokens + encryption keys in `react-native-encrypted-storage`. NEVER plain AsyncStorage.
- Biometric (FaceID / Fingerprint) to unlock sensitive sections (health records).
- Clear in-memory state on `AppState === 'background'` for high-sensitivity mode.
- Never log journal content, GPS, or PII to console.

### 2.14 Testing

- Jest unit tests for utils, validation, state stores.
- React Native Testing Library for components (focus on user interaction, not implementation).
- Maestro or Detox for E2E: login → log period → trigger SOS.
- CI runs both iOS and Android simulators.

### 2.15 Dev environment

- TypeScript strict. No `any`. Define interfaces for all props and state.
- ESLint (`@react-native-community/eslint-config`) + Prettier, pre-commit hook.
- Absolute imports via `babel-plugin-module-resolver` (`src/...`).
- Min SDK 24, target 33 (Android); iOS 14+.

---

## 3. Project-level invariants (apply to BOTH backend and mobile)

1. **API contract lives in `plans/30-mobile-api-contract.md`.** Any change to request/response shape must update that file in the same PR. Mobile cannot break on a backend change — the contract is the source of truth.
2. **Response envelope:** success `{ "data": ..., "message": "ok" }`, error `{ "error": { "code": "RESOURCE_NOT_FOUND", "details": "..." } }`. Mobile parses both forms.
3. **Pagination:** cursor for user-facing lists (journals, logs), offset for admin lists. Mobile MUST handle both.
4. **Auth header:** `Authorization: Bearer <access_token>`. Refresh in request body. Mobile persists the refresh token in encrypted storage; backend stores hashed.
5. **Idempotency:** SOS and any future payment mutation MUST accept an `Idempotency-Key` header and dedupe.
6. **Rate limit response:** HTTP 429 with `Retry-After` header. Mobile shows a toast and backs off.
7. **ETag support** for offline: backend emits `ETag`; mobile sends `If-None-Match` for cheap revalidation.
8. **Privacy:** journal content and medical notes are EITHER client-side encrypted (server cannot read) OR server-side encrypted with per-user key — never plaintext at rest. The encryption boundary lives in the backend's `core/encryption.py` and is called from the SERVICE LAYER only.
9. **Feature flags** live in a small JSON file on the backend (or Redis for hot flags). Mobile fetches its flag set on launch via `/api/v1/features`.
10. **Errors from the backend must be Sentry-tagged with `request_id` and `user_id`.** Mobile sends the same `request_id` (in the `X-Request-ID` header) so traces link across the network.

---

## 4. When you are unsure

- Open the per-topic plan in `plans/` first.
- If the plan is silent, open the matching section in `backend_rules.md` or `frontend_rules.md`.
- If both are silent, write an ADR (Architecture Decision Record) under `/backend/docs/adr/NNNN-title.md` and reference it in the PR.
- Do NOT introduce a pattern that violates the modularity rules above just to ship faster.

---

## 5. Quick "is this change allowed?" checklist

Before you open a PR, walk this list:

**Backend**
- [ ] Did you create a new module folder under `app/modules/<feature>/`?
- [ ] Are routes thin, business logic in services?
- [ ] Are models / schemas / tasks in the owning module, not in a shared `models/` or `tasks/`?
- [ ] Are Pydantic schemas split into Create / Update / Response / InDB?
- [ ] Is the new endpoint under `/api/v1/...`?
- [ ] Is encryption / decryption done in the service, not the route or model?
- [ ] Are Celery tasks idempotent + have time limits?
- [ ] Is row-level permission enforced via `current_user.id`, not request body?
- [ ] Is there a test file under `tests/modules/<feature>/`?
- [ ] Did you run `ruff`, `mypy`, `pytest` locally?

**Mobile**
- [ ] Did you put the new screen under `src/screens/<feature>/`?
- [ ] Are server reads going through React Query (NOT Zustand)?
- [ ] Is persistent data in encrypted storage (NOT plain AsyncStorage)?
- [ ] Are forms using `react-hook-form` + `zod`?
- [ ] Is the component using theme tokens (NOT hardcoded colors / spacing)?
- [ ] Is the list a `FlatList` with `getItemLayout` if length > 5?
- [ ] Are touch targets ≥ 44 × 44?
- [ ] Are `accessibilityLabel` / `accessibilityRole` set on interactive elements?
- [ ] Is sensitive data NOT logged?
- [ ] Did you update the API contract doc if the request/response shape changed?

If any checkbox is unchecked, fix it before opening the PR.

---

## 6. Android Build invariants

### 6.1 NDK toolchain patch (`c++_shared`)
- `android-legacy.toolchain.cmake` at line 366 must contain:
  `list(APPEND ANDROID_CXX_STANDARD_LIBRARIES "-lc++_shared")`
  in the `c++_shared` STL case. This is a **global NDK patch** (not per-package).
- Without this, JNI library loading fails silently at runtime on some devices.

### 6.2 expo-av source build
- **Root cause (proven by ELF analysis):** the `publication` block in
  `expo-av/expo-module.config.json` makes the build consume a **prebuilt AAR**
  compiled against OLD JSI headers. Its `libexpo-av.so` references
  `asObject(fb::jsi::Runtime&)`, but RN 0.86's `libjsi.so` only exports
  `asObject(IRuntime&)` → `dlopen` fails at `AVManager.<clinit>`.
- **The fix is the source build**, not the CMakeLists change: remove the
  `publication` block from `expo-av/expo-module.config.json` so Gradle compiles
  expo-av against the app's own RN JSI headers. `libjsi.so` DOES ship in the
  APK and the source-built `libexpo-av.so` is ABI-consistent.
- `patches/expo-av+16.0.8.patch` captures ALL changes: config `publication`
  removal, `local-maven-repo/` AAR deletion, `CMakeLists.txt` link fix, and
  `ViewUtils.kt` / `FullscreenVideoPlayer.java` SDK 57 API migrations.
- The patch must be **regenerated with `npx patch-package expo-av`** whenever a
  new manual node_modules edit is made — a manual edit NOT captured in the
  patch is silently lost on `npm ci` (this was the actual EAS failure).

### 6.3 Fresh build after `npm ci`
After `npm ci`, re-apply patches with `npx patch-package` before Android build.
NDK toolchain patch must be re-applied manually if NDK is reinstalled or updated.
