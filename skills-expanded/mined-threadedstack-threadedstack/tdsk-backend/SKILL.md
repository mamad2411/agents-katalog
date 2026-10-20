---
name: "tdsk-backend"
description: "Knowledge base for the backend Core API repo"
tags: ["express", "nodejs", "api", "backend", "payments", "stripe", "ai", "session", "proxy", "secrets", "pi-ai", "openai", "shell", "scheduler", "egress"]
---
# Backend Repo Skill

## Overview

The Backend (`repos/backend`) is the Core API server (Express 5.1.0) for Threaded Stack. It handles:
- **Admin CRUD** for all platform resources (orgs, projects, agents, threads, sandboxes, skills, schedules, etc.)
- **Proxy/FaaS/AI Engines** — secure API proxying with secret injection, sandboxed function execution, LLM streaming via `pi-ai`, OpenAI-compatible chat completions
- **Shell Sessions** — interactive terminal access to sandbox pods via WebSocket+SSH with terminal parsing, event persistence, session sharing, and generative UI
- **Egress Proxy** — transparent MITM proxy for sandbox outbound traffic with SNI extraction and placeholder secret scanning
- **Scheduler** — cron-based schedule execution with 60s tick interval
- **Payment/Email** — Stripe subscription management with quota tracking; email via Resend/Mailgun/Console

Receives admin requests from Auth-Proxy at `/_/*` paths.

## Directory Structure

```
repos/backend/
├── configs/
│   ├── backend.config.ts    # Main config loader (server, proxy, database, logger, email, payments, egress)
│   ├── tsup.config.ts       # Build configuration
│   └── vitest.config.ts     # Test configuration
├── src/
│   ├── constants/           # envs.ts, values.ts, sandbox.ts
│   ├── endpoints/           # API route definitions (one dir per resource)
│   │   ├── agents/          # CRUD + runAgent (SSE) + oaiChatCompletions + oaiModels
│   │   ├── ai/              # sessions + streamChat (SSE LLM proxy)
│   │   ├── orgs/            # CRUD + members + roles + quickstart + nested resources
│   │   ├── sandboxes/       # CRUD + connect, start, stop, tunnel, shell, exec, sessions, instances, threads, copy, monitor, SBP config
│   │   ├── cli/             # CLI session key management (createSessionKey, revokeSessionKey)
│   │   ├── proxy/           # Proxy endpoint routing via endpoint type services
│   │   ├── accounts.ts      # Main /_/* routes — auth + enforceQuota middleware applied here
│   │   └── endpoints.ts     # Endpoint registry (proxy, accounts)
│   ├── middleware/           # Express middleware (see Middleware Setup Order)
│   │   ├── authorize.ts     # Role-based authorization
│   │   ├── enforceQuota.ts  # Tier-based POST route quota limits
│   │   ├── projectAccessGuard.ts # Project-scoped API key boundaries
│   │   ├── projectMemberGuard.ts # Project membership enforcement
│   │   ├── rateLimit.ts     # Rate limiting (setupRateLimit)
│   │   ├── sandboxProxy.ts  # Caddy wildcard subdomain → pod IP proxy
│   │   ├── setupAuth.ts     # JWT authentication (authenticate function)
│   │   ├── setupDatabase.ts # Database connection with validation
│   │   ├── setupEndpoints.ts # Dynamic route builder with param auto-validation
│   │   ├── setupErrorHandler.ts # Error response formatting
│   │   ├── setupLogger.ts   # Winston request/error logging
│   │   ├── setupProxy.ts    # Reverse proxy to API service (TDSK_BE_REMOTE)
│   │   ├── setupSandbox.ts  # SandboxService + EgressProxy initialization
│   │   ├── setupSubscription.ts # Auto-create free tier subscription
│   │   └── setupServer.ts   # CORS, base setup
│   ├── server/              # Express app, router, HTTP server, WebSocket server
│   ├── services/            # Service layer (see Services)
│   ├── types/               # 17 type files (see Types section)
│   ├── utils/               # Auth, validation, provider, proxy, pagination, sandbox, shell utilities
│   ├── start.ts             # Loads config and calls main(config)
│   └── main.ts              # Orchestrates middleware setup and server init
└── package.json
```

Other endpoint dirs follow standard CRUD pattern: `apiKeys/`, `assets/`, `auth/`, `base/`, `domains/`, `endpoints/`, `functions/`, `invitations/`, `payments/`, `projects/`, `providers/`, `quotas/`, `schedules/`, `secrets/`, `skills/`, `subscriptions/`, `threads/`, `users/`.

## Application Bootstrap

1. `index.ts` re-exports `start.ts`
2. `start.ts` loads `backend.config.ts` and calls `main(config)`
3. `main.ts` stores config on `app.locals.config`, creates `EmailService`, `PaymentsService`, and `EmbeddingService` (at `app.locals.embeddings`) on `app.locals`, then runs middleware setup in order (see below)

### Server Core
- `server/app.ts` — Express app singleton
- `server/server.ts` — `initServer()` creates HTTP or HTTPS server based on config
- `server/router.ts` — `createAsyncRouter()` wraps Express router methods with `express-async-handler`

## Middleware Setup Order

1. **Logger** — Winston request/error logging (from `@tdsk/logger`)
2. **Server Setup** — CORS, disables `x-powered-by`, router mount
3. **Rate Limit** — `setupRateLimit` for auth and general API rate limiting
4. **Database** — DB connection with validation and error handling
5. **Sandbox** — `SandboxService` (KubeClient, pod watcher) + `EgressProxy` (MITM for outbound traffic)
5. **Sandbox Proxy** — Sandbox subdomain (`*.sb.local.threadedstack.app`) -> pod IP proxy
6. **Endpoints** — Dynamic route registration from `endpoints/` directory
   - `accounts` routes get `express.json()` (with raw body capture), `authenticate`, `setupSubscription`, `enforceQuota` middleware
   - `proxy` routes dispatch to endpoint type services
7. **Error Handler** — Formats and sends error responses

Auth, subscription, and quota enforcement are applied in `accounts.ts`, not globally in `main.ts`.

### Middleware Details

| Middleware | File | Purpose |
|------------|------|---------|
| `authenticate` | `setupAuth.ts` | JWT authentication (used in `accounts.ts`) |
| `setupSubscription` | `setupSubscription.ts` | Auto-create free tier subscription for new users |
| `enforceQuota` | `enforceQuota.ts` | Map POST routes to quota resource keys (projects, endpoints, secrets, threads, messages, organizations), check tier limits from `PlanLimits`, return 403 `quota_exceeded` when over limit. For POST /orgs uses user-scoped owned org count. Fails closed (blocks on error) |
| `projectAccessGuard` | `projectAccessGuard.ts` | Enforce project-level access for project-scoped API keys. Org-scoped keys and JWT auth pass through. 403 otherwise |
| `projectMemberGuard` | `projectMemberGuard.ts` | Enforce project membership — verifies user is a member of the project before allowing access |
| `sandboxProxy` | `sandboxProxy.ts` | Intercept sandbox subdomain requests, parse hostname to extract port+subdomain, look up in-memory route map, proxy to pod IP:port |
| `featureGate` | `featureGate.ts` | Feature flag enforcement — gates routes behind `isFeatureEnabled(flag)`, returns 404 when flag is disabled |
| `rateLimit` | `rateLimit.ts` | Rate limiting via `express-rate-limit` — auth routes (20/min) and general API routes (200/min) with draft-7 headers |

## Services

| Service | File | Purpose |
|---------|------|---------|
| SecretResolver | `services/secrets/secretResolver.ts` | Resolve/decrypt `{{SECRET_NAME}}` templates, 3-tier API key resolution (agent -> provider -> org). Key methods: `hasSecretRefs`, `replaceRefs`, `replaceInHeaders`, `replaceInObj`, `decrypt`, `resolveApiKey`, `loadAndDecrypt`, `resolveHeaders`, `resolveBodyParams` |
| ProxyService | `services/proxy/proxyService.ts` | Apply endpoint options: OAuth 2.0 token caching (5min buffer), auth types (Bearer/Basic/API Key), domain whitelists with wildcards, path regex, transforms |
| RetryService | `services/proxy/retryService.ts` | Exponential backoff retry (default 3 retries, 2x multiplier, max 30s, codes 408/429/5xx) |
| EgressProxy | `services/proxy/egress.ts` | MITM egress proxy for sandbox outbound traffic (see below) |
| InterpreterService | `services/interpreter/interpreter.ts` | Generative UI: calls LLM via `pi-ai` `streamSimple()` with terminal events, validates JSON component tree, retry with backoff |
| ChunkBuffer | `services/interpreter/chunkBuffer.ts` | Batches parsed terminal events by chunk ID, calls `onFlush` when chunk completes |
| skipHeuristic | `services/interpreter/skipHeuristic.ts` | `shouldInterpret()` filters noise events to avoid unnecessary LLM calls |
| Scheduler | `services/scheduler/scheduler.ts` | 60s tick, queries due schedules, executes agent via callback, marks next cron time, tracks errors. Guard via `#ticking` flag |
| OpenAI Adapters | `services/openai/` | `requestAdapter.ts`: `extractPrompt()`, `convertOAIMessages()`, `buildOverrides()`. `responseAdapter.ts`: `createStreamingAdapter()`, `createNonStreamingAdapter()`, `formatOAIError()` |
| FileExtractor | `services/files/fileExtractor.ts` | Text extraction: UTF-8 passthrough for text formats, PDF via `pdf-parse`, DOCX via `mammoth`; max 50K chars |
| EmailService | `services/email/email.ts` | Strategy pattern: Resend / Mailgun / Console. Templates via Handlebars from `public/templates/` |
| PaymentsService | `services/payments/payments.ts` | Strategy pattern: Stripe / Console |
| SessionStore | `services/sessionStore.ts` | In-memory LLM session store, 1h TTL, 5min cleanup interval |
| InMemoryRateLimiter | `services/rateLimiter.ts` | In-memory rate limiter implementing `TRateLimiterBackend`, used for tunnel rate-limiting |
| InviteService | `services/invite.ts` | Invitation email logic — token generation, expiration, email dispatch |
| SessionTokenService | `services/sessionToken.ts` | `signSessionToken`, `verifySessionToken`, `signShellToken`, `verifyShellToken` — session/shell token signing and verification |
| SandboxService | `services/sandboxes/sandbox.ts` | K8s pod lifecycle, session tracking, idle timeout, shell session management, subdomain proxy routing, monitor WebSocket management (see below) |
| EmbeddingService | `services/embeddings/embedding.ts` | Memory embeddings. `resolveEmbeddingProvider(db, orgId)` picks the first org ai provider (oldest `createdAt`) whose `options.embeddingModel` is set (openai/google); `embed`/`embedOne` resolve the API key via SecretResolver and call the provider. NULL-safe: no opted-in provider ⇒ returns null embeddings (memory search falls back to lexical-only). Attached at `app.locals.embeddings` |
| Websocket | `services/websocket/websocket.ts` | Persistent AI WebSocket handler (see below) |

### Endpoint Type Services (`services/endpoints/`)

Polymorphic dispatch for different endpoint types. All extend `BaseEndpoint` (shared: `checkPermission`, `validateProject`, `validateMethod`, `fetchSecrets`).

| Service | Purpose |
|---------|---------|
| `AgentEndpoint` | Load agent+provider+secrets, resolve API key via SecretResolver, resolve headers/bodyParams, load functions, create/reuse thread, stream SSE via `AgentRunner.run()`. Shared `run()` used by admin run route, proxy engine, and OAI completions |
| `ProxyEndpoint` | HTTP proxy with auth, transforms, retries via `ProxyService` |
| `FaaSEndpoint` | Sandboxed function execution via `FunctionExecutor` |
| `getEPService` | Singleton registry mapping `EEndpointType` to service instance. Used by `endpoints/proxy/endpoint.ts` |

**Agent Run Flow** (via `AgentEndpoint.run()`):
1. Load agent + provider + secrets (unsanitized for encrypted values)
2. Select provider: explicit `providerId` override, or `agent.primaryProvider`
3. Resolve API key via `SecretResolver.resolveApiKey(agent, provider)` — 3-tier: agent -> provider -> org
4. Resolve provider headers and bodyParams via SecretResolver (template substitution)
5. Load custom functions attached to agent via junction table
6. Get or create thread
7. Build LLM config with optional overrides (model, maxTokens, systemPrompt, tools, envVars)
8. Build sandbox config from agent environment
9. Stream SSE via `AgentRunner.run()` with `onExecuteFunction` callback for `FunctionExecutor`

### FunctionExecutor (`services/functions/functionExecutor.ts`)

Executes user-defined functions in sandbox. TypeScript transpiled via esbuild (ts -> esm). Uses `@tdsk/sandbox` `createSandboxProvider('local')`. Runner wrapper: writes `function.mjs` + `runner.mjs` to sandbox, executes with `node`. Input via `__FUNCTION_INPUT__` env var. 1MB output cap (`MaxOutputBytes`), 30s default timeout (`DefaultTimeoutMS`).

### EgressProxy (`services/proxy/egress.ts`)

Transparent MITM proxy for sandbox pod outbound HTTP/HTTPS traffic:
- Outbound traffic from pods redirected via iptables DNAT in pod init container
- TCP front server sniffs first byte: HTTP (non-0x16) piped directly to MITM with `X-TDSK-Real-IP`; TLS (0x16) has SNI extracted from ClientHello, converted to HTTP CONNECT tunnel
- MITM proxy scans headers for `tdsk_ph_*` placeholder tokens, resolves to real secrets via `SecretResolver`
- Throws on unresolvable secrets to prevent placeholder leaks
- **Fail-closed swap (`replaceTokens`):** a placeholder is swapped to its real secret ONLY when it carries a non-empty `allowedDomains` scope AND the destination host matches that scope. An unscoped placeholder is never swapped (previously unscoped tokens were swapped to any host), so a secret can never leak to an unintended domain
- `EgressProxy.init(app)` checks CA cert files at `/etc/tdsk/ca/tls.{crt,key}`, creates temp CA dir for `http-mitm-proxy`, starts both MITM (internal loopback) and TCP front (public port)

### SandboxService (`services/sandboxes/sandbox.ts`)

**State:**
- `sessions: Map<instanceId, TSandboxSession[]>` — active SSH sessions per instance
- `passwords: Map<instanceId, password>` — SSH password cache
- `instanceActivity: Map<instanceId, timestamp>` — last activity for idle detection
- `startingInstances: Map<sandboxId, number>` — prevents startup races (tracks count)
- `orgMonitors: Map<orgId, Set<WebSocket>>` — monitor WebSocket clients per org
- `monitorAccess: WeakMap<WebSocket, Set<sandboxId>>` — per-socket sandbox ID access filter
- Shell sessions: persistent `TShellSession` objects indexed by session ID

**Key Methods:**
- `startPod(sandbox, orgId, projectId?)` — generate SSH password, create K8s pod with env vars
- `stopPod(sandbox, orgId)` / `cleanupInstance(instanceId)` — delete pod, clean up routes and sessions
- `findRunningPod/findActivePod(sandboxId, orgId)` — find Running or Running/Pending pod
- `validatePodOwnership(instanceId, orgId)` — verify pod belongs to org
- `addSession/removeSession/getSessions(instanceId)` — session tracking
- `getPassword/recoverPassword(instanceId)` — SSH password management (recovery via `printenv`)
- `startIdleTimeout()` — initialize idle timeout checking interval
- `addShellSession/getShellSession/removeShellSession(sessionId)` — persistent shell session lifecycle
- `attachToShellSession/detachFromShellSession(sessionId, ws)` — WebSocket attachment for reconnect/join
- `updateSessionVisibility(sessionId, visibility)` — toggle private/public
- `getOrgShellSessionCount(orgId)` — count active per org for plan limits
- `queueEventForPersistence/flushEventBatch(sessionId)` — batched event persistence to DB
- `updateActivity(instanceId)` — touch timestamp for idle timeout
- `getPodProxy(target)` — static, returns `createProxyMiddleware` for subdomain proxying
- `broadcastMonitor(orgId, event)` — broadcast event to all org monitor WebSocket clients
- `addMonitor(orgId, ws, sandboxIds)` — register monitor WebSocket client for org
- `removeMonitor(orgId, ws)` — unregister monitor WebSocket client

**Idle Timeout:** checks every 60s, stops pods with no active sessions after 30min (configurable per sandbox via `idleTimeoutMinutes`).

### Websocket Service (`services/websocket/websocket.ts`)

Persistent WebSocket handler for AI agent execution:
- Reuses `AgentRunner` across turns, destroys and reinits on thread change
- Message types: `prompt`, `cancel`, `steer`, `followUp`, `updateConfig`, `file_upload`, `workspace_manifest`
- File uploads: validates MIME type, size (25MB max), path traversal; creates asset records with text extraction
- Heartbeat: JSON ping every 25s (avoids Caddy RSV1 bit corruption of protocol-level pings)
- Event bridge: maps `TStreamEvent` types to `EWSEventType`, detects artifact content in tool results

### WebSocket Server (`server/wsServer.ts`)

Multi-path dispatch using `noServer: true` mode:
- Static: `/ai/ws` -> `onWSConnect` (AI agent execution)
- Dynamic: `/_/sandboxes/:id/tunnel` (matched by `SBTunnelPattern`) -> `onTunnelConnect`
- Dynamic: `/_/sandboxes/:id/shell` (matched by `SBShellPattern`) -> `onShellConnect`
- Static: `/_/sandboxes/monitor` (matched by `SBMonitorPattern`) -> `onMonitorConnect` (org-level real-time sandbox event subscription)

HTTP upgrade listener filters by pathname and routes to correct handler. Unmatched upgrades destroy socket. Centralized error logging for connection failures.

### InterpreterService Integration with Shell Sessions

When a sandbox has `guiConfig.enabled` with a `providerId`, the shell handler creates a `ChunkBuffer` + `InterpreterService`. As terminal events arrive from the parser, they are batched by chunk ID. When a chunk completes, `shouldInterpret()` filters noise, and qualifying batches are sent to the LLM for interpretation. Results are broadcast to all attached WebSocket clients as `generative-ui` messages containing a JSON component tree.

The prompt module (`services/interpreter/prompt.ts`) provides `getSystemPrompt()` and `buildUserMessage()` to construct the LLM prompt from `TGuiConfig` and parsed events. The validator (`services/interpreter/validator.ts`) ensures the LLM response is valid JSON conforming to the component tree schema.

### Scheduler Factory

`createScheduler(db, executeAgent?)` returns a `Scheduler` instance. The `executeAgent` callback receives schedule + agent config, defaults to running via `AgentEndpoint`. Cron parsing uses `cronParser.ts` with `isValidCron()` and `parseNextRun()`.

### Runtime-Brain Executor (`services/scheduler/executor.ts`)

Drives scheduled autonomous-agent runs whose brain is the in-pod coding CLI (`claude -p`).

- **Memory injection:** before invoking the pod prompt, the executor injects a `## Roadmap` block (from `db.services.memory.getRoadmap`) and a `## Relevant memories` block (from scored `searchScored`) into the runtime-brain prompt, in soul → roadmap → memories → prompt order (`utils/agent/memory.ts`).
- **tdsk-memories capture:** after a run, the executor parses a trailing `tdsk-memories` JSON fenced code block from the transcript and persists each entry as a new memory row.
- **Provider failover:** the runtime brain fails over across the sandbox's priority-ordered ai providers on transient upstream failure (Anthropic 529/Overloaded, rate limits, upstream 5xx), analogous to the api-brain `llmConfigs` failover. `resolveProviderEnvChain` (in `utils/sandbox/resolveProviderEnv.ts`) resolves a per-provider env set for each provider (no longer merged — fixes the `ANTHROPIC_AUTH_TOKEN`/`ANTHROPIC_BASE_URL` collision) plus a merged domain-scoped placeholders map. The priority-0 provider's env becomes the pod default; each fallback (e.g. ZAI `ANTHROPIC_BASE_URL=https://api.z.ai/api/anthropic`, OpenRouter `https://openrouter.ai/api`) prefixes its OWN env inline when the executor re-runs the prompt against it. Fallbacks capped at `CliMaxProviderFailovers`; each token stays domain-scoped so egress swaps cleanly. `RuntimeProviderEnvMap[claudeCode]` maps zai/openrouter.

## Endpoints

### Endpoint Definition Pattern

Endpoints are defined as `TEndpointConfig` objects (static) or `TEndpointBuilder` functions (dynamic, receive app instance). Builder functions are used for endpoints needing app context (e.g., `accounts` needs config for admin path).

`setupEndpoints` iterates the endpoint registry, auto-injects param validation for routes with `:id` or `:xxxId` params, and handles nesting: `EPMethod.Use` creates nested routers with shared middleware, recursively building child endpoints.

### Key Routes

| Method | Path | Purpose | Auth |
|--------|------|---------|------|
| POST | `/_/agents/:id/run` | Run agent with SSE streaming (body: `prompt`, `threadId?`, `providerId?`) | JWT/API key |
| POST | `/_/agents/:id/v1/chat/completions` | OpenAI-compatible chat completions (standard OpenAI request body) | JWT/API key |
| GET | `/_/agents/:id/v1/models` | OpenAI-compatible model list for agent's provider | JWT/API key |
| POST | `/_/orgs/:orgId/quickstart` | Create Provider+Secret+Project+Agent+Endpoint in one DB txn | JWT/API key |
| POST | `/_/orgs` | Create org (auto-seeds 4 sandbox presets with `builtIn: true`) | JWT/API key |
| POST | `/_/ai/sessions` | Create LLM session, resolve API key server-side, return token | JWT/API key |
| WS | `/ai/ws` | AI agent WebSocket execution (session config cached) | Session token (`?token=`) |
| POST | `/_/orgs/:orgId/sandboxes/:id/connect` | Start pod, poll until Running (max 120s), return SSH creds | JWT/API key |
| POST | `/_/orgs/:orgId/sandboxes/:id/copy` | Deep-copy sandbox config (forces `builtIn: false`, validates org ownership) | JWT/API key |
| POST | `/_/orgs/:orgId/projects/:projectId/sandboxes/:id/start` | Start sandbox pod explicitly | JWT/API key |
| DELETE | `/_/orgs/:orgId/projects/:projectId/sandboxes/:id/stop` | Stop sandbox pod (body: instanceId, force, stopAll) | JWT/API key |
| GET | `/_/orgs/:orgId/projects/:projectId/sandboxes/:id/status` | Get container state (query: instanceId) | JWT/API key |
| GET | `/_/orgs/:orgId/projects/:projectId/sandboxes/:id/instances` | List running pod instances for sandbox | JWT/API key |
| POST | `/_/orgs/:orgId/projects/:projectId/sandboxes/:id/exec` | Execute command in pod via K8s Exec API | JWT/API key |
| GET | `/_/orgs/:orgId/projects/:projectId/sandboxes/:id/sessions` | List active SSH sessions | JWT/API key |
| GET | `/_/orgs/:orgId/projects/:projectId/sandboxes/:id/threads` | List threads for sandbox | JWT/API key |
| POST | `/_/orgs/:orgId/sandboxes/monitor/token` | Generate monitor WebSocket token for org | JWT/API key |
| GET/PUT/DELETE | `/_/orgs/:orgId/projects/:sandboxId/config` | Sandbox Project (SBP) config overrides | JWT/API key |
| POST | `/_/orgs/:orgId/cli/createSessionKey` | Create CLI session key | JWT/API key |
| POST | `/_/orgs/:orgId/cli/revokeSessionKey` | Revoke CLI session key | JWT/API key |
| WS | `/_/sandboxes/:id/tunnel` | WebSocket SSH tunnel — raw TCP bidirectional relay with backpressure (64KB) | API key |
| WS | `/_/sandboxes/:id/shell` | Interactive shell with PTY, parser, event persistence, generative UI | API key or shell token |
| WS | `/_/sandboxes/monitor` | Org-level sandbox event subscription (real-time instance state) | API key or session token |
| POST | `/_/orgs/:orgId/skills/:id/attach` | Attach skill to agent | JWT/API key |
| POST | `/_/orgs/:orgId/skills/:id/detach` | Detach skill from agent | JWT/API key |
| POST | `/_/orgs/:orgId/schedules/:id/trigger` | Manually trigger schedule (executes agent, marks next cron time) | JWT/API key |
| GET/POST/PATCH/DELETE | `/_/orgs/:orgId/agents/:agentId/memories` | Agent memory CRUD; gated by `authorize(EPermResource.memory)` + `featureGate('memories')` | JWT/API key |
| POST | `/_/orgs/:orgId/agents/:agentId/memories/search` | Scored memory search (recency x importance x relevance) | JWT/API key |
| POST | `/_/providers/:brand/models` | Fetch models from `ModelRegistry`; Ollama special-cased with live fetch | JWT/API key |
| POST | `/_/threads/:id/branch` | Branch thread from specific message | JWT/API key |
| POST | `/_/orgs/:orgId/agents/:agentId/threads/:threadId/files` | Upload file (body: `fileName`, `data` base64, `mimeType`; 25MB cap) | JWT/API key |
| POST | `/_/payments/webhook` | Stripe webhook | Public |
| ALL | `/proxy/:projectId/:endpointId` | Dispatch to endpoint type service via `getEPService()` | Deferred |

All `/_/*` routes protected by JWT except `AuthIgnore` list (`/`, `/health`, `/payments/webhooks`). All list endpoints support `?limit=N&offset=N`. POST routes subject to `enforceQuota`.

Standard CRUD (list/create/get/update/delete) exists for: orgs, users, projects, agents, threads, endpoints, providers, secrets, apiKeys, assets, domains, invitations, subscriptions, quotas, skills, schedules, sandboxes.

### Org Creation Seeding

When creating an org, 4 default sandbox presets are seeded from `SandboxPresets` (domain constants): Claude Code, Codex, OpenCode, Base (custom). All `builtIn: true`. Seeding failures are non-fatal (org still created, `warnings` in 201 response). User-created sandboxes always get `builtIn: false`.

### Quickstart

`POST /_/orgs/:orgId/quickstart` — creates Provider + Secret + Project + Agent + Endpoint in a single DB transaction. Body: `template` (required, resolves from `ProviderTemplates`), `apiKey`, `projectName`, `agentName`, plus optional model/maxTokens/systemPrompt overrides.

### Shell Session Details

**Protocol:**
- **Binary frames (client->server):** raw stdin -> SSH stream
- **Text frames (client->server):** JSON control: `resize`, `signal` (SIGINT/SIGTSTP), `visibility`, `permission-response`
- **Binary frames (server->client):** raw stdout from SSH
- **Text frames (server->client):** JSON status (`connected`, `reconnected`, `joined`, `disconnected`, `error`, `visibility`, `user-joined`, `user-left`), parsed events (`{ sessionId, event }`), generative-ui (`{ sessionId, chunkId, type: 'generative-ui', tree }`)

**New Session Flow:**
1. Extract sandbox ID from URL, parse query params (cols, rows, run, sessionId)
2. Authenticate via API key hash or shell token (validates sandbox ID match)
3. Find running pod, validate ownership (org + pod creator match)
4. Check `PlanLimits` concurrent session cap for org's subscription tier
5. Validate pod IP and recover SSH password
6. Load sandbox config for runtime info and generative UI config (sandbox-level -> org-level fallback)
7. Create thread for session history in DB
8. SSH connect via `ssh2.Client`, allocate PTY shell (xterm-256color)
9. Create `TerminalParser` with `onEvent` callback for broadcasting and persistence
10. Initialize `ChunkBuffer` + `InterpreterService` if generative UI is enabled
11. Register session with `SandboxService` (shell session + pod session for idle tracking)
12. Execute runtime command if `run=true` and `runtimeCommand` configured
13. Wire SSH stream -> WebSocket fan-out with backpressure

**Reconnect/Join Flow (sessionId param):**
- Same user: reattaches WebSocket, drains ring buffer (or parser raw buffer, or DB ptyBuffer fallback), replays persisted events
- Cross-user: validates `public` visibility + org membership, attaches as observer, notifies `user-joined`

**Session Persistence:**
- Ring buffer (1MB) for reconnect; parser raw buffer for full PTY history
- Events batched and persisted as messages in session thread
- On SSH close: flush parser, persist PTY buffer to thread, flush final event batch

**Multi-user Support:**
- Session creator can toggle visibility (private/public) via control message
- Public sessions can be joined by org members
- Input events tagged with `userId` for attribution
- `user-joined`/`user-left` notifications broadcast to all attachments

### AI Endpoint Architecture

AI endpoints split into three groups with different auth:

1. **Session Creation** (`POST /_/ai/sessions`) — normal JWT/API key auth. Creates LLM session with agent's resolved API key/provider/model config. API key resolved server-side via SecretResolver (never leaves backend). Returns session token + non-sensitive config.

2. **WebSocket** (`/ai/ws`) — session-token auth via `?token=<token>` query param. Streams responses using cached session config. No API key validation needed (already validated at session creation).

3. **OpenAI-Compatible** (`POST /_/agents/:id/v1/chat/completions`) — normal JWT/API key auth. Accepts standard OpenAI request format, returns OpenAI response format. Supports streaming (SSE with `data: [DONE]` sentinel) and non-streaming. Converts between OpenAI message types and ThreadedStack types (tool calls, vision content, tool results). Agent identified by URL `:id` param.

**Design rationale:** API keys never sent over wire. Session tokens scoped to single agent+provider+model config, expire after 1h. `pi-ai` provides unified multi-provider streaming.

WebSocket response event types: `start`, `text_start`, `text_delta`, `text_end`, `thinking_start`, `thinking_delta`, `thinking_end`, `toolcall_start`, `toolcall_delta`, `toolcall_end`, `done`, `error`, `ping`, `thread_created`, `file_upload_complete`, `artifact`, `tool_execution_update`, `turn_end`.

### Sandbox Connect

`POST /_/sandboxes/:id/connect` — checks for already-running pod (prevents races), starts pod if needed (generates random SSH password, stores in memory), polls until Running (max 120s, 2s interval). Returns `{ podName, password, port: 2222, cliCommand }`. Error codes: 409 (already starting), 500 (pod failed), 504 (timeout).

### Sandbox Tunnel

`WS /_/sandboxes/:id/tunnel` — validates API key via hash, verifies pod ownership, opens TCP to pod IP:2222, bidirectional relay with backpressure (64KB threshold). Keepalive pings every 30s. Close codes: 4000 (internal), 4001 (auth), 4002 (validation), 4003 (permission), 4004 (not found), 4005 (connection failed).

### Skills CRUD (`endpoints/skills/`)

Under `/_/orgs/:orgId/skills`: standard CRUD (list/create/get/update/delete) plus:
- `POST /:id/attach` — attach skill to an agent (junction table)
- `POST /:id/detach` — detach skill from an agent

### Schedules CRUD (`endpoints/schedules/`)

Under `/_/orgs/:orgId/schedules`: standard CRUD plus:
- `POST /` — validates cron expression via `isValidCron()`, computes `nextRunAt`
- `POST /:scheduleId/trigger` — manually trigger (executes agent, marks run with next cron time)

### Provider Models (`endpoints/providers/fetchModels.ts`)

`POST /_/providers/:brand/models` — fetches from `ModelRegistry` (pi-mono static registry). Ollama special-cased with live fetch from local API. Custom providers return empty list. Body: `{ baseUrl? }`.

### Thread File Upload (`endpoints/threads/uploadFile.ts`)

`POST /_/orgs/:orgId/agents/:agentId/threads/:threadId/files` — body: `fileName`, `data` (base64), `mimeType`. Validation: MIME allowlist, 25MB cap, base64 check, path traversal prevention. Returns `{ assetId, fileName, fileType, fileSize, extractedText?, extractionError?, imageData? }`.

## Key Patterns

1. **Async Router** — `createAsyncRouter()` wraps all route handlers with `express-async-handler` for automatic error catching
2. **Configuration-Driven Endpoints** — endpoints defined as `TEndpointConfig` objects or `TEndpointBuilder` functions (receive app instance), dynamically registered by `setupEndpoints`. Builder functions used for endpoints needing app context (e.g., accounts)
3. **Middleware Composition** — endpoints specify middleware arrays; `EPMethod.Use` creates nested routers with shared middleware
4. **Error Handling** — custom `Exception` class with HTTP status code and optional error code; global error handler formats `{ error, code? }`
5. **Strategy Pattern** — `EmailService` and `PaymentsService` swap providers via strategy (Resend/Mailgun/Console, Stripe/Console)
6. **Permission Helper** — `requireResourceWithPermission()` combines permission check + resource fetch, throws 404/403
7. **Pagination** — `parsePagination(req)` returns `{ limit, offset }` with defaults (50/0, max 200)
8. **Persistent Sessions** — shell and AI sessions outlive WebSocket connections; reconnection replays buffered output; multi-user attachment model; TTL-based cleanup

## Types

Type files in `src/types/`: `agent.types.ts`, `api.types.ts`, `backend.types.ts`, `email.types.ts`, `endpoints.types.ts`, `errors.types.ts`, `limiter.types.ts`, `oai.types.ts`, `pay.types.ts`, `request.types.ts`, `retry.types.ts`, `secrets.types.ts`, `session.types.ts`, `shellSession.types.ts`, `simple-oauth2.d.ts`, `token.types.ts`

### `shellSession.types.ts`
- `TShellSession` — persistent state: SSH client/stream, parser, ring buffer, attachments set, tool state, visibility, thread/sandbox/org/project IDs
- `TShellControlMsg` — client control: resize, signal, visibility, permission-response
- `TShellServerMsg` — server status: connected, reconnected, joined, disconnected, error, visibility, user-joined, user-left
- `TWebSocketMeta` — per-WebSocket metadata: sessionId, joinedUserId (for cross-user joins)

### `oai.types.ts`
- `TOAIRequest`, `TOAIMessage`, `TOAIContentPart`, `TOAIToolCall` — OpenAI request types
- `TOAIResponse`, `TOAIChunk`, `TOAIUsage`, `TOAIFinishReason` — OpenAI response types
- `TOAIErrorBody`, `TOAIErrorType`, `TOAIModel`, `TOAIModelList` — error and model types

## Constants

| Category | Key Constants |
|----------|--------------|
| Auth | `AuthIgnore` = `[/, /health, /payments/webhooks]` |
| Logging | `LoggerIgnore` (OPTIONS method, devtools route) |
| Retry | `AllowedRetryCodes` = `[408, 429, 500, 502, 503, 504]`; `DefRetryCfg` (3 retries, 1s initial, 30s max, 2x backoff) |
| Pagination | `DBPaging` = `{ max: 200, default: 50 }` |
| Files | `FileMaxSize` = 25MB; `MaxExtractedLength` = 50K chars; `MaxOutputBytes` = 1MB; `RequestBodyMaxSize` = 1MB; `DefaultTimeoutMS` = 30s |
| Sandbox | `SBTcpTimeout` = 10s; `SBBackpressureThreshold` = 64KB; `SBBackpressureMaxWait` = 30s; `SBTunnelPattern`/`SBShellPattern`/`SBMonitorPattern` (regex); `DefSBConfig` (30min timeout, 120s max wait, 2s poll, 60s idle interval); `WsPingInterval` = 30s (tunnel/shell/monitor ping) |
| Egress | `PhTokenPrefix` = `tdsk_ph_`; `CACertPath`/`CAKeyPath` at `/etc/tdsk/ca/`; `RealIpHeader` = `x-tdsk-real-ip` |
| WebSocket | `WsPingIntervalMS` = 25s; `SessionTtlSec` = 3600; `ClientMsgTypes` (steer, prompt, cancel, followUp, file_upload, updateConfig, workspace_manifest) |

## Utilities

| Utility | File | Purpose |
|---------|------|---------|
| `requireResourceWithPermission` | `utils/auth/requireResource.ts` | Permission check + resource fetch; throws 404/403 |
| `validateExclusiveArc` | `utils/validation/exclusiveArc.ts` | Ensure exactly one of N fields is set (throws 400) |
| `resolveProviderType` | `utils/providers/` | Resolve LLM provider type (anthropic/openai/google) from config |
| `validateLLMProvider` | `utils/providers/` | Validate AI-type providers have valid `ELLMProviderBrand` |
| `resolveAgentConfig` | `utils/agent/` | Load agent+provider+secrets, resolve API key/headers/bodyParams, build LLM config, load functions+skills. Used by WebSocket and OAI endpoint |
| `checkPermission` | `utils/auth/` | Check user permission for action on resource in scope |
| `pxToBeHeader` | `utils/auth/` | Convert proxy-to-backend headers |
| `shouldIgnore` | `utils/auth/` | Determine if request bypasses auth |
| `validateApiKey` | `utils/auth/` | API key validation logic |
| `parsePagination` | `utils/pagination.ts` | Parse limit/offset query params (defaults 50/0, max 200) |
| `mimeFromPath`, `isAllowedMimeType` | `utils/validation/` | MIME type derivation and allowlist checking |
| `extractSNI` | `utils/proxy/` | Extract SNI hostname from TLS ClientHello for egress routing |
| `generateInvitationToken` | `utils/auth/` | Generate invitation token |
| `getBillingPeriod` | `utils/auth/` | Calculate billing period start/end dates |
| `resolveSandbox` | `utils/sandbox/resolveSandbox.ts` | Resolve sandbox by ID or project-scoped alias |
| `resolveProviderEnv` | `utils/sandbox/resolveProviderEnv.ts` | Resolve provider env vars for pod injection |
| `resolveGitProviderEnv` | `utils/sandbox/resolveGitProviderEnv.ts` | Resolve git provider env vars for pod injection |
| `resolveDockerPullSecrets` | `utils/sandbox/resolveDockerPullSecrets.ts` | Resolve Docker pull secrets for pod images |
| `resolveSkillFiles` | `utils/sandbox/resolveSkillFiles.ts` | Resolve skill files for sandbox pod injection |
| `validateGitProviderInputs` | `utils/sandbox/validateGitProviderInputs.ts` | Validate git provider configuration inputs |
| `parseControlMsg` | `utils/shell/parseControlMsg.ts` | Parse shell WebSocket control messages |

## Integration Points

- **`@tdsk/domain`** — shared types, models (`TApp`, `TRequest`, `TResponse`, `TABConfig`), `TerminalParser`, `PlanLimits`, `SandboxPresets`, `ESandboxSessionVisibility`, `TGuiConfig`, `TToolState`
- **`@tdsk/database`** — Drizzle ORM and services; stored on `app.locals.db`
- **`@tdsk/logger`** — Winston logging service
- **`@tdsk/agent`** — `AgentRunner` for persistent multi-turn execution with tool use
- **`@tdsk/sandbox`** — pluggable sandbox execution, `PodLabelKeys`, `parseSandboxHost`
- **`@mariozechner/pi-ai`** — unified multi-provider LLM streaming (Anthropic, OpenAI, Google); used by streamChat and InterpreterService
- **`ssh2`** — SSH client for PTY sessions to sandbox pods
- **`ws`** — WebSocket library for shell, tunnel, AI connections
- **`http-mitm-proxy`** — MITM proxy for egress interception; CA certs at `/etc/tdsk/ca/`
- **Auth-Proxy** — receives admin requests at `/_/*`; proxies back for unmatched routes via `setupProxy`; configured via `TDSK_BE_REMOTE`/`TDSK_BE_REMOTE_PORT`
- **Debugging** — `TDSK_BE_LOGGER_LEVEL=debug` for verbose, `TDSK_BE_LOGGER_PRETTY=true` for formatted
