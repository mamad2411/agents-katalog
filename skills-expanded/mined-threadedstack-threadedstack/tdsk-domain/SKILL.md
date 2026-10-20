---
name: "tdsk-domain"
description: "Knowledge base for the shared types, models, and utilities repo"
tags: ["typescript", "types", "models", "domain", "shared", "utilities", "payments", "ai", "quotas", "subscriptions"]
---
# Domain Repo Skill

## Overview

The `@tdsk/domain` repo (`repos/domain`) is the shared foundation for the Threaded Stack monorepo.

- **29 type definition files** for Express APIs, auth, providers, AI/LLM configs, sandboxes, permissions, payments, GUI, shell events, sync, WebSocket, prefixes, and helpers
- **24 model classes** for core entities (all extend `Base` with `id`, `createdAt?`, `updatedAt?`)
- **Utility functions** for crypto (AES-256-GCM encryption, hashing, key derivation), permissions, time, async, data manipulation
- **API helpers** for Express routing, CORS, auth headers, and error handling via `Exception` class
- **Two export entry points**: `index.ts` (full, includes Node.js code) and `web.ts` (frontend-safe, excludes api/environment/services/crypto)

## Directory Structure

```
repos/domain/src/
├── api/           # Express utilities: adminPath, authHeaders, behindLBProxy, checkAuthHeader, inKube
├── constants/     # 11 constant files: featureFlags, gitProviders, gui, memory, parser, plans, prefixes, providerDomains, providers, sandbox, values
├── crypto/        # AES-256-GCM encryption/decryption, hashing, key generation
├── models/        # 23 domain model classes
├── services/      # Shared services (api/apiService.ts — ApiService base class)
├── types/         # 29 type definition files (includes prefixs.types.ts for entity ID prefixes)
├── utils/         # Permissions, payments, cleanSplit, isDomain, shortId, time, sandbox/slugify, providers/toProviderLinks, buildFallbackModel
├── error/         # Exception class with HTTP status codes
├── environment/   # loadEnvs, addToProcess
├── parser/        # Terminal output parser (AST nodes, GUI types)
├── index.ts       # Full barrel export (Node.js)
└── web.ts         # Web-safe barrel export (frontend)
```

Import alias: `@TDM/*` (e.g., `import { User } from '@TDM/models'`)

## Type Definitions

Types are in `src/types/`. Key files and their exports:

### Enums

| Enum | File | Purpose |
|------|------|---------|
| `EMsgType` | ai.types.ts | user, tool, system, action, assistant |
| `EAgentTool` | ai.types.ts | mkdir, listDir, readFile, shellExec, webSearch, writeFile, deleteFile, fileExists, memorySearch, memoryWrite |
| `EMemoryKind` | memory.types.ts | fact, insight, reflection, compaction, roadmap |
| `ELLMProviderBrand` | ai.types.ts | zai, openai, google, custom, anthropic |
| `EEndpointType` | epd.types.ts | proxy, faas, agent |
| `ESandboxType` | sandbox.types.ts | local, kubernetes |
| `EContainerState` | sandbox.types.ts | Failed, Pending, Running, Unknown, Succeeded |
| `ESBState` | sandbox.types.ts | Error, Running, Stopped, Starting |
| `ESandboxRuntime` | sandbox.types.ts | claude-code, codex, opencode, antigravity, openclaw, custom |
| `EApiKeyScope` | scopes.types.ts | read, write, admin |
| `EApiKeyExpire` | scopes.types.ts | d7, d30, d90, d180, y1, never |
| `EProvider` | provider.types.ts | ai, git, auth, storage |
| `EGitProvider` | git.types.ts | github, gitlab |
| `ERoleType` | permissions.types.ts | super, owner, admin, member, viewer |
| `EPermAction` | permissions.types.ts | create, read, update, delete, manage |
| `EPermResource` | permissions.types.ts | org, project, user, role, secret, apiKey, endpoint, provider, domain, function, agent, subscription, quota, invitation, thread, message, asset, memory |
| `EPermScope` | permissions.types.ts | global, org, project |
| `EFunLanguage` | functions.types.ts | python, typescript, javascript |
| `ESubscriptionTier` | payments.types.ts | free, basic, developer, pro |
| `ESubscriptionStatus` | payments.types.ts | active, canceled, past_due, incomplete |
| `EInviteStatus` | invitation.types.ts | pending, accepted, expired, revoked |
| `EHttpMethod` | http.types.ts | GET, POST, PUT, PATCH, DELETE, OPTIONS, HEAD |

### Key Interfaces & Types

- **Express**: `TApp` (typed Express app with locals), `TRequest` (extended with `user`), `TResponse` (typed locals), `TRouter`, `TResLocals` — in `server.types.ts`
- **AI/LLM**: `TLLMAdapterConfig` (model, apiKey, provider, systemPrompt, temperature, maxTokens, headers, bodyParams), `ILLMAdapter` (provider, stream method), `TAIMessage` (role + TMessageContent[]), `TStreamEvent` (union: text, tool_call_start/args, tool_result, tool_execution_update, error, done), `TLLMToolDef` (name, description, inputSchema), `TAgentRunRequest`, `TAgentEnvironment`, `TAgentConfigFields` — in `ai.types.ts`
- **Agent**: `TAgentTool`, `TAgentProject`, `TAgentProvider`, `TAgentFunction` — in `agent.types.ts`
- **API**: `TApiRequest`, `TApiResponse`, `TApiServiceConfig` — in `api.types.ts`
- **Endpoint**: `TEndpointOpts<T>` (discriminated union: TProxyEndpointConfig, TFaaSEndpointConfig, TAgentEndpointConfig) — in `epd.types.ts`, `endpoint.types.ts`
- **Feature Flags**: `TFeatureFlag`, `TFeatureFlagConfig` — in `featureFlag.types.ts`
- **Git**: `EGitProvider`, git provider/repo types — in `git.types.ts`
- **GUI**: `TGUINode`, `TGUITree`, GUI component tree types for generative UI — in `gui.types.ts`
- **Headers**: Auth header types — in `headers.types.ts`
- **Sandbox**: `ISandbox` (reset, close, mkdir, readFile, deleteFile, listDir, fileExists, writeFile, exec, evaluate), `ISandboxProvider`, `TSandboxConfig`, `TKubeSandboxConfig` (image, args, gitRepo, workdir, sshEnabled, runtimes, initScript, etc.), `TSandboxSession`, `TSandboxConnectResponse`, `TContainerMeta`, `TRouteEntry`, `TRouteMapEntry`, `TSandboxRuntimeId` — in `sandbox.types.ts`
- **Schedule**: `TScheduleConfig`, cron-based agent execution types — in `schedule.types.ts`
- **Secret**: Secret-related types — in `secret.types.ts`
- **Shell Events**: Shell event types for WebSocket communication — in `shellEvent.types.ts`
- **Skill**: Skill definition types — in `skill.types.ts`
- **Memory**: `EMemoryKind`, `TMemoryKind`, `TMemory` (orgId, agentId, kind, text, importance, embedding?, lastAccessedAt), `TMemorySearchOpts`, `TMemoryWriteInput` — in `memory.types.ts`
- **Sync**: `TSyncConfig`, `TSyncRule`, `TSyncMode`, Mutagen file sync configuration types — in `sync.types.ts`
- **Parser**: Terminal parser types — in `parser.types.ts`
- **WebSocket**: WebSocket message types — in `ws.types.ts`
- **Quickstart**: `TProviderTemplate` (id, name, baseUrl, models, defaultModel, apiKeyPattern), `TQuickstartRequest`, `TQuickstartResponse`
- **Scopes**: `TKeyHash` (key, hash, prefix) — in `scopes.types.ts`
- **Functions**: `TFunctionParam`, `TFunctionRequest`, `TFunctionContext`, `TFunctionResponse`, `TFunctionExecResult` — in `functions.types.ts`
- **Helpers**: `TAnyCB`, `TValueOf<T>`, `TAnyObj`, `TKeyLike` — in `helpers.types.ts`
- **Organization**: Org-related types — in `organization.types.ts`
- **Invitation**: Invitation-related types — in `invitation.types.ts`
- **Payments**: Subscription/payment types — in `payments.types.ts`
- **Permissions**: Role/permission types — in `permissions.types.ts`
- **HTTP**: HTTP method enum and types — in `http.types.ts`

## Models

All 24 models extend `Base { id, createdAt?, updatedAt? }` (except Certificate and Plan). Key fields and methods for each:

- **Agent** -- name, orgId, model, maxTokens, description, tools, systemPrompt, active, secrets[], projects[], providers[], functions[], envVars, environment. Computed: `primaryProvider`. Methods: `sanitize()`
- **ApiKey** -- key, name, orgId, userId, projectId, keyHash, scopes, active, keyPrefix, rateLimit, expiresAt, lastUsedAt. Methods: `hasScope()`, `isExpired()`, `isValid()`, `getRateLimit()`, `sanitize()`
- **Asset** -- name, type, url, content, orgId, userId, threadId, projectId, messageId, providerId, meta
- **Certificate** -- does NOT extend Base. Fields: parent, name, isFile, value, modified
- **Domain** -- domain, orgId/projectId (exclusive arc), verified, verifiedAt, sslEnabled, sslPrivateKey, sslCertificate, sslExpiresAt, certificates[]. Computed: `certificate`
- **Endpoint** -- type, path, name, projectId, method, public, options, headers. Subclasses: ProxyEndpoint, FaaSEndpoint, AgentEndpoint
- **Function** -- name, content, projectId, endpointId, description, agentIds, branch, inputSchema, defaultArgs, dependencies, language
- **Invitation** -- email, orgId, token, userId, invitedBy, revokedBy, roleType, status, expiresAt, acceptedAt, revokedAt. Methods: `sanitize()`, `isPending()`, `isExpired()`, `isAccepted()`, `isRevoked()`, `daysUntilExpiration()`
- **Invoice** -- userId, stripeInvoiceId, amount, currency, status, invoiceUrl, period
- **Memory** -- text, orgId, agentId, kind (TMemoryKind, default fact), importance (default 5), lastAccessedAt, embedding (number[] | null), meta
- **Message** -- type (TMsgType), content (TMessageContent[]), threadId, projectId, orgId, meta
- **Organization** -- name (required), ownerId (required), description
- **Plan** -- does NOT extend Base. Fields: id, name, description, recurring, metadata (auto-converted via `rawPlanToMeta()`)
- **Project** -- name, orgId, gitUrl, description, branch (default 'main'), meta
- **Provider** -- name, orgId, type, brand, options, headers, bodyParams, secretId
- **Quota** -- orgId, period, projects, members, endpoints, threads, messages, functionCalls, runtime, orgSecrets, projectSecrets, organizations, price, retention
- **Role** -- name, type (ERoleType), userId, orgId, projectId. Methods: `hasMinRole()`, `isAdmin()`, `isOwner()`, `isSuperAdmin()`
- **Sandbox** -- name, orgId, userId, projectId, config (TKubeSandboxConfig), builtIn, runtime
- **Schedule** -- agentId, orgId, cronExpression, prompt, enabled, lastRunAt, nextRunAt, error
- **Secret** -- name, value, description, hashKey, encryptedValue, orgId/agentId/projectId/providerId (exclusive arc). Methods: `sanitize()`
- **Skill** -- name, description, instructions, triggerKeywords, tools, alwaysActive, orgId
- **Subscription** -- tier, status, userId, stripeCustomerId, stripeSubscriptionId, stripePriceId, seats, currentPeriodEnd, currentPeriodStart, cancelAtPeriodEnd
- **Thread** -- name, userId, orgId, agentId, projectId, providerId, public, parentThreadId, branchMessageId, meta
- **User** -- first, last, name, email, image, banned, banReason, emailVerified, role, provider. Computed: `displayName`

## Constants

8 constant files in `src/constants/`:

- **providers.ts** -- `ProviderTemplates`: `Record<ELLMProviderBrand, TProviderTemplate>` with model lists, base URLs, API key patterns for anthropic, openai, google, zai, custom
- **providerDomains.ts** -- Provider domain mappings for URL resolution
- **values.ts** -- `ApiKeyPrefix` (`tdsk_`), `AuthHeaders` (`X-User-Id`, `X-User-Role`, `X-User-Email`), `RoleHierarchy` (`[viewer, member, admin, owner, super]`), `PermissionMatrix` (role-to-permission mapping for 17 resource types)
- **sandbox.ts** -- `SandboxRuntimeConfigs` (`Record<TSandboxRuntimeId, { command, args, runtimeCommand }>`), `SandboxPresets` (full seed configs per runtime, used by backend to seed default sandboxes on org creation), `SBImagePresets` (image preset buttons: Claude Code, Codex, OpenCode)
- **featureFlags.ts** -- Feature flag definitions for toggling platform features (includes the `memories` flag gating the agent memory layer)
- **memory.ts** -- memory-layer constants: `MemoryRecencyDecay` (0.995), `MemorySearchTopK` (8), `MemoryMaxTextChars` (4000), `MemoryMaxImportance` (10), `MemoryMinImportance` (1), `MemoryEmbeddingDimensions` (1536), `MemoriesBlockFence` (`tdsk-memories`), `MemoryInjectMaxChars` (6000)
- **gui.ts** -- GUI-related constants for generative UI
- **parser.ts** -- Terminal parser constants
- **plans.ts** -- Subscription plan tier definitions and metadata

## Crypto Functions

All in `src/crypto/crypto.ts`. Requires `TDSK_MASTER_KEY` env (hex-encoded, min 64 hex chars).

- `deriveKey(ref_id)` -- HKDF-SHA256 key derivation from user ID + master key
- `encryptValue(derivedKey, plaintext)` -- AES-256-GCM encrypt (12-byte IV, 16-byte auth tag)
- `decryptValue(derivedKey, ciphertext, iv, authTag)` -- decrypt
- `encodeEncrypted(iv, authTag, encrypted)` -- base64 encode for storage
- `bufferToBytea(buffer)` / `byteaToBuffer(byteaString)` -- PostgreSQL bytea conversion
- `createHashKey(name)` -- truncated SHA-256 hash (16 hex chars) for secret name lookup
- `hashKey(key)` -- SHA-256 hash for API key storage/validation
- `generateApiKey()` -- generate new API key with `tdsk_` prefix, returns `{ key, hash, prefix }`

## Permissions Functions

All in `src/utils/permissions/permissions.ts`:

- `getRoleLevel(role)` -- viewer=0 through super=4
- `hasMinRole(userRole, requiredRole)` -- check minimum role level
- `canPerform(userRole, action, resource)` -- main permission check
- `canAccessSecretValue(userRole)` -- requires admin+
- `isSuperAdmin(userRole)`
- `getHighestRole(roles)`
- `canManageRole(managerRole, targetRole)` -- must be strictly higher
- `getAllowedActions(userRole, resource)`
- `isValidRoleType(role)`

## Other Utilities

- `shortId()` -- generate short unique ID
- `isDomain(domain)` -- validate domain name format
- `splitBy(str, sep)` / `cleanSplit(str, sep)` -- string splitting
- `timestamp()` -- `Date.now()`
- `nextFrame(callback)` -- schedule on next animation frame
- `throttleCBLast(callback, delay)` -- throttle with last call guarantee

## API Helpers

In `src/api/`: `adminPath(config)` (default `/_`), `setAuthHeaders(pxReq, req)`, `fromAuthHeaders(req)`, `checkAuthHeader(authHeader)` (extract Bearer token), `behindLBProxy()`, `inKube()`

## Error Handling

`Exception` extends `Error` with `status` (HTTP code), `code?`, `details?` (array), `__isAuthError?`. Static method: `Exception.throw(status, message, code?, details?)`.

## Integration Points

- **Backend** -- full `index.ts`: TApp, TRequest, adminPath, authHeaders, Exception, loadEnvs, canPerform, hashKey, generateApiKey
- **Proxy** -- full `index.ts`: checkAuthHeader, behindLBProxy, inKube, hashKey, encryption
- **Admin** -- `web.ts` only: Exception, model classes, ProviderTemplates, constants
- **Agent** -- full `index.ts`: TLLMAdapterConfig, ILLMAdapter, TStreamEvent, model classes
- **TSA** -- full `index.ts`: AI types, model classes
- **Sandbox** -- sandbox types: ISandbox, ISandboxProvider, TSandboxConfig, TKubeSandboxConfig, ESandboxRuntime, SandboxRuntimeConfigs, SandboxPresets
- **Database** -- model classes for ORM type definitions

## Build & Test

```bash
cd repos/domain
pnpm test     # Vitest
# No build script -- TypeScript source consumed directly via aliases
```
