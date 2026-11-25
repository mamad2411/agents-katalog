# Prompt 005: Add Missing Features from create-api-base Skill

**Date**: 2026-02-23
**Scope**: Implement 5 missing features to Azure FS REST API from the create-api-base skill
**Goal**: Close gaps in containerized deployment readiness, configuration visibility, and development experience

---

## Overview

The Azure FS REST API needs 5 specific features from the `create-api-base` skill to improve cloud deployment readiness and development experience. These features are driven by the deviation analysis at `docs/design/api-skill-deviation-analysis.md` and follow patterns established by the skill blueprint at `/Users/giorgosmarinos/.claude/skills/create-api-base/01-model-api-option.md`.

### Features to Implement

1. **Container-Aware Swagger URLs**: Auto-detect runtime environment (Azure App Service, Docker, Kubernetes) and generate correct server URLs in OpenAPI spec
2. **NODE_ENV Support**: Add environment-specific behavior and expose in health checks
3. **PortChecker Utility**: Pre-startup port availability checking with optional auto-selection
4. **Development Routes**: Secure endpoints for inspecting configuration in development mode
5. **Config Source Tracking**: Track where each config value originated for debugging and audit

---

## Phase 1: Investigation

### 1.1 Review Current State

**Location**: `/Users/giorgosmarinos/aiwork/agent-platform/azure-storage-tool/`

**Files to examine**:
- `src/api/server.ts` - Server startup, port listening, error handling
- `src/api/swagger/config.ts` - Current Swagger spec generation (static server URL)
- `src/config/config.loader.ts` - Configuration loading (file + env + CLI flags)
- `src/config/config.schema.ts` - Configuration validation and type definitions
- `.env.example` - Current environment variables (API section)
- `CLAUDE.md` - Tool documentation standards (review API tool documentation format)
- `docs/design/api-skill-deviation-analysis.md` - Detailed comparison with skill blueprint
- `docs/design/configuration-guide.md` - Current config documentation

**Objectives**:
- Understand current Swagger generation logic and identify where runtime detection should inject
- Map current config sources (file, env, CLI) and identify how to track origin
- Check if NODE_ENV is already loaded anywhere; identify where to inject environment-specific behavior
- Identify error handling on EADDRINUSE and where port checking should occur
- Review existing middleware and error handling patterns for development routes

### 1.2 Review Skill Blueprint

**Location**: `/Users/giorgosmarinos/.claude/skills/create-api-base/01-model-api-option.md`

**Key sections**:
- "Container & Cloud Environment (Optional - Auto-detected or manually set)" environment variables
- `createSwaggerSpec()` function signature and container detection logic (search for "getSwaggerServers" pattern)
- `PortChecker` utility class with `isPortAvailable()`, `findAvailablePort()`, `getProcessUsingPort()` methods
- `/api/dev/env` and `/api/dev/env/:key` development routes with NODE_ENV protection
- EnvironmentManager source tracking via `Map<string, string>` (if present in full skill)

**Objectives**:
- Extract exact implementation patterns for each feature
- Identify parameter signatures and return types
- Review error handling and validation patterns
- Understand environment variable naming and priority logic

### 1.3 Analysis Output

Document findings in a new file: `docs/design/feature-implementation-analysis.md`

**Structure**:
```
## 1. Container-Aware Swagger
### Current Implementation
### Skill Pattern
### Integration Points Required

## 2. NODE_ENV Support
### Current Implementation
### Skill Pattern
### Integration Points Required

## 3. PortChecker Utility
### Current Implementation
### Skill Pattern
### Integration Points Required

## 4. Development Routes
### Current Implementation
### Skill Pattern
### Integration Points Required

## 5. Config Source Tracking
### Current Implementation
### Skill Pattern
### Integration Points Required
```

---

## Phase 2: Planning & Design

### 2.1 Configuration Variables

Document all new/modified environment variables: `docs/design/new-config-variables.md`

**Must include**:
- `NODE_ENV` (required, values: development/production/staging)
- `PUBLIC_URL` (optional, override for Swagger server URL)
- `DOCKER_HOST_URL` (optional, auto-detected or manual)
- `K8S_SERVICE_HOST` (auto-set by Kubernetes)
- `K8S_SERVICE_PORT` (auto-set by Kubernetes)
- `WEBSITE_HOSTNAME` (auto-set by Azure App Service)
- `WEBSITE_SITE_NAME` (auto-set by Azure App Service)
- `SWAGGER_ADDITIONAL_SERVERS` (optional, comma-separated)
- `ENABLE_SERVER_VARIABLES` (optional boolean, defaults to false)
- `AUTO_SELECT_PORT` (optional boolean, defaults to false)

**Per variable, document**:
- Purpose and valid values
- Default behavior if omitted
- Priority in multi-source scenarios
- Whether it's required or optional
- Recommended storage method (env, config file, or either)
- Expiration or refresh requirements (none for these, but document if added later)

### 2.2 Architecture Design

Create: `docs/design/feature-architecture.md`

**Sections**:

#### 2.2.1 Container-Aware Swagger URLs

**Current state**: `createSwaggerSpec(apiConfig)` generates static `servers: [{ url: 'http://...' }]`

**Desired state**:
- Function signature: `createSwaggerSpec(apiConfig, runtimeContext?: RuntimeContext)` where `RuntimeContext` includes detected environment
- Auto-detection order:
  1. Check `PUBLIC_URL` (if set, use as primary server)
  2. Check `WEBSITE_HOSTNAME` (Azure App Service)
  3. Check `K8S_SERVICE_HOST` + `K8S_SERVICE_PORT` (Kubernetes)
  4. Check `DOCKER_HOST_URL` (Docker)
  5. Fall back to config `host` + `port`
- Support `SWAGGER_ADDITIONAL_SERVERS` (comma-separated URLs, added to servers array)
- Conditional server variables: if `ENABLE_SERVER_VARIABLES=true`, add variable definitions for baseUrl substitution
- Integration: Call detection logic in `startServer()` after port is finalized (or auto-selected), pass result to Swagger re-mount

**New files**:
- `src/utils/swagger-server-detector.ts` - Exports `detectRuntimeEnvironment()` function and `RuntimeContext` type

#### 2.2.2 NODE_ENV Support

**Current state**: NODE_ENV not referenced; no environment-specific behavior

**Desired state**:
- Load `NODE_ENV` as required env var in `config.loader.ts` (throw if missing)
- Store in `ResolvedConfig` as `env: string` field
- Use in:
  - Health check: Include `environment` in response (e.g., `{ status: 'healthy', environment: 'development' }`)
  - Error handler: Only include stack traces in logs when `NODE_ENV === 'development'`
  - Development routes: Only mount when `NODE_ENV === 'development'`
- No impact on exit codes (already fine)

**Modifications**:
- `src/config/config.types.ts` - Add `env: string` to `ApiResolvedConfig`
- `src/config/config.schema.ts` - Load and validate `NODE_ENV` (required, enum: development/production/staging)
- `src/api/routes/health.routes.ts` - Include env in health response
- `src/api/middleware/error-handler.middleware.ts` - Conditional stack trace logging based on env

#### 2.2.3 PortChecker Utility

**Current state**: Error handling on `EADDRINUSE` fails with error message

**Desired state**:
- New class `PortChecker` in `src/utils/port-checker.ts` with:
  - `async isPortAvailable(port: number): Promise<boolean>` - Check if port is available
  - `async findAvailablePort(startPort: number): Promise<number>` - Find next available port (try up to 100 ports ahead)
  - `async getProcessUsingPort(port: number): Promise<string | null>` - Use `lsof` (macOS/Linux) or `netstat` (Windows) to identify process using port
- Integration in `startServer()`:
  - Before `server.listen()`, check if port is available
  - If not available and `AUTO_SELECT_PORT=true`, find next available port, log it, and use auto-selected port
  - If not available and `AUTO_SELECT_PORT=false`, throw descriptive error (show which process is using port if possible)
  - If port was auto-selected, re-mount Swagger with correct actual port (if Swagger was already created)
- Error message should be helpful: "Port 3000 is in use by process ID 12345 (node). Set AUTO_SELECT_PORT=true to auto-select or choose a different port."

**New files**:
- `src/utils/port-checker.ts` - Exports `PortChecker` class

#### 2.2.4 Development Routes

**Current state**: No development-specific endpoints

**Desired state**:
- Mount only if `NODE_ENV === 'development'`
- Two endpoints:
  - `GET /api/dev/env` - List all env variables with config source and masking
  - `GET /api/dev/env/:key` - Get single env variable with source
- Both return 403 if accessed outside development mode
- Response format: `{ success: true, data: { variableName, value, source, isMasked }, metadata: { ... } }`
- Source values: ".env file", "Environment variable", ".azure-fs.json", "CLI flag", "Auto-detected"
- Sensitive masking: Hide values for keys containing SECRET, PASSWORD, TOKEN, KEY, PRIVATE, CREDENTIAL, CONNECTION_STRING, SAS_TOKEN
- Implementation note: This requires config source tracking (feature 5 below) to work properly

**New files**:
- `src/api/routes/dev.routes.ts` - Dev route registration
- `src/api/controllers/dev.controller.ts` - Dev endpoint handlers

#### 2.2.5 Config Source Tracking

**Current state**: Config values merged from three sources (file, env, CLI) but origin lost after merge

**Desired state**:
- Extend `config.loader.ts` to maintain `Map<string, { source: string, value: any, isMasked?: boolean }>`
- When loading config from each source, annotate with source:
  - Config file: source = ".azure-fs.json"
  - Environment variables: source = "Environment variable"
  - CLI flags: source = "CLI flag"
  - Auto-detected (e.g., K8S_SERVICE_HOST): source = "Auto-detected"
  - Computed/defaults for non-fallback cases: source = "Computed"
- Expose via:
  - `ResolvedConfig.sources: Map<string, string>` (or similar)
  - `config show` command: Include source in output (e.g., `AZURE_FS_API_PORT: 3000 (source: CLI flag)`)
  - Dev routes: Include source for each variable
- Do not create fallback values - if missing and required, throw error (already enforced, but note this)

**Modifications**:
- `src/config/config.loader.ts` - Track source during loading, expose via `resolvedConfig.sources` or similar
- `src/config/config.types.ts` - Add sources field to `ResolvedConfig` and `ApiResolvedConfig`
- `src/commands/config.commands.ts` - Display source in `config show` output

### 2.3 Integration Points

Document in `docs/design/feature-integration-plan.md`:

**Startup Sequence (impacts timing)**:
1. Load configuration (all sources)
2. Create express app (includes middleware, routes, Swagger with static spec)
3. Create HTTP server from app
4. Check port availability (PortChecker)
5. If needed, auto-select port (PortChecker)
6. Detect runtime environment (SwaggerServerDetector)
7. Re-mount Swagger spec with correct server URLs
8. Bind server to resolved port
9. Log startup info including actual port, environment, detected runtime

**Validation**: All new env vars must be validated in `config.schema.ts` before use

**Error handling**: All new features should throw `ConfigError` or `AppError` with clear messages

### 2.4 Testing Strategy

Document in `docs/design/feature-testing-plan.md`:

**Unit tests needed**:
- `PortChecker.isPortAvailable()` with mocked port binding
- `PortChecker.findAvailablePort()` with controlled port availability
- `SwaggerServerDetector.detectRuntimeEnvironment()` with various env var combinations
- Config loader source tracking with multiple source combinations
- Development route authorization (403 outside dev mode)
- Sensitive value masking for various key patterns

**Integration tests needed**:
- Server startup with auto-selected port
- Server startup with unavailable port (failure case)
- Swagger spec generation with different runtime contexts
- Full config show output with sources
- Development routes returning correct source information

**Manual testing checklist**:
- Start server with `AUTO_SELECT_PORT=true` when port is in use
- Start server in Docker and verify Swagger shows correct container URL
- Start server in Kubernetes and verify Swagger shows correct K8s URL
- Start server in Azure App Service and verify Swagger shows correct Azure URL
- Call `/api/dev/env` in development and verify source tracking
- Call `/api/dev/env` in production and verify 403 response
- Use `config show --json` and verify source annotations

---

## Phase 3: Implementation

### 3.1 Feature 1: PortChecker Utility

**File**: `/Users/giorgosmarinos/aiwork/agent-platform/azure-storage-tool/src/utils/port-checker.ts`

**Implementation checklist**:
- [ ] Create `PortChecker` class
- [ ] Implement `isPortAvailable(port)` using `net.createServer()`
- [ ] Implement `findAvailablePort(startPort)` with 100-port scan limit
- [ ] Implement `getProcessUsingPort(port)` using `child_process.exec('lsof')` or `netstat` with OS detection
- [ ] Add error handling and logging
- [ ] Export as singleton or factory
- [ ] Write unit tests (if test framework in place)

**Integration**:
- Import in `src/api/server.ts`
- Call `portChecker.isPortAvailable(port)` before `server.listen()`
- Handle auto-selection logic
- Update error messages with process info

### 3.2 Feature 2: NODE_ENV Support

**File modifications**:
- [ ] `src/config/config.types.ts` - Add `env: string` field to `ApiResolvedConfig`
- [ ] `src/config/config.schema.ts` - Load NODE_ENV as required env var with validation
- [ ] `src/config/config.loader.ts` - Extract NODE_ENV in config loading
- [ ] `src/api/routes/health.routes.ts` - Include environment in health check response
- [ ] `src/api/middleware/error-handler.middleware.ts` - Conditional stack trace logging based on NODE_ENV

**Checklist**:
- [ ] NODE_ENV required in config validation
- [ ] Valid values: development, production, staging
- [ ] Error message clear if missing
- [ ] Health response format: `{ status: 'healthy', environment: 'development', ... }`
- [ ] Stack traces only in dev logs (not in error response body)
- [ ] Update .env.example with NODE_ENV

### 3.3 Feature 3: Config Source Tracking

**File modifications**:
- [ ] `src/config/config.loader.ts` - Implement source tracking Map during loading
- [ ] `src/config/config.types.ts` - Add `sources: Map<string, string>` to `ResolvedConfig` and `ApiResolvedConfig`
- [ ] `src/commands/config.commands.ts` - Include source in `config show` output
- [ ] `.env.example` and docs - Document source tracking behavior

**Implementation approach**:
```typescript
// Inside resolveConfig()
const sources = new Map<string, string>();
// As each source is loaded:
// - From file: sources.set('AZURE_STORAGE_ACCOUNT_URL', '.azure-fs.json')
// - From env: sources.set('AZURE_STORAGE_ACCOUNT_URL', 'Environment variable')
// - From CLI: sources.set('AZURE_STORAGE_ACCOUNT_URL', 'CLI flag')
// Return both config and sources
```

**Checklist**:
- [ ] Source tracking integrated into all three loaders (file, env, CLI)
- [ ] CLI flags override with proper source annotation
- [ ] `config show --json` includes sources
- [ ] `config show` (human-readable) includes sources or separate section
- [ ] No performance degradation from tracking

### 3.4 Feature 4: Container-Aware Swagger URLs

**New file**: `/Users/giorgosmarinos/aiwork/agent-platform/azure-storage-tool/src/utils/swagger-server-detector.ts`

**Exports**:
```typescript
type RuntimeContext = {
  detectedAt: string; // timestamp
  primaryServer: { url: string; description?: string };
  additionalServers: Array<{ url: string; description?: string; variables?: {} }>;
  runtimeEnvironment: 'azure-app-service' | 'kubernetes' | 'docker' | 'local';
};

function detectRuntimeEnvironment(apiConfig: ApiConfig): RuntimeContext;
```

**Detection order** (in `detectRuntimeEnvironment()`):
1. If `PUBLIC_URL` set: use as primary
2. Else if `WEBSITE_HOSTNAME` set: construct Azure App Service URL, set runtime to 'azure-app-service'
3. Else if `K8S_SERVICE_HOST` + `K8S_SERVICE_PORT` set: construct K8s URL, check `USE_HTTPS`, set runtime to 'kubernetes'
4. Else if `DOCKER_HOST_URL` set: use directly, set runtime to 'docker'
5. Else: use config host + port, set runtime to 'local'

**Additional servers**:
- Parse `SWAGGER_ADDITIONAL_SERVERS` (comma-separated) and add each
- If `ENABLE_SERVER_VARIABLES=true`, add variable definitions (e.g., `{basePath: {default: '/api/v1'}}`

**Checklist**:
- [ ] Detect Azure App Service via WEBSITE_HOSTNAME
- [ ] Detect Kubernetes via K8S_SERVICE_HOST/PORT
- [ ] Detect Docker via DOCKER_HOST_URL
- [ ] Fall back to localhost:port for local development
- [ ] Parse SWAGGER_ADDITIONAL_SERVERS correctly
- [ ] Handle ENABLE_SERVER_VARIABLES for dynamic URLs
- [ ] Return complete RuntimeContext with all metadata
- [ ] Handle edge cases (malformed URLs, missing parts)

**Integration in Swagger config**:
- [ ] Modify `createSwaggerSpec()` signature to accept optional `RuntimeContext`
- [ ] If context provided, use detected servers instead of static localhost
- [ ] Otherwise, compute context from config
- [ ] Re-mount Swagger in `startServer()` after port finalization

### 3.5 Feature 5: Development Routes

**New route file**: `/Users/giorgosmarinos/aiwork/agent-platform/azure-storage-tool/src/api/routes/dev.routes.ts`

**New controller**: `/Users/giorgosmarinos/aiwork/agent-platform/azure-storage-tool/src/api/controllers/dev.controller.ts`

**Endpoints**:

```
GET /api/dev/env (only if NODE_ENV === 'development')
  Response: {
    success: true,
    data: [
      {
        variable: "AZURE_STORAGE_ACCOUNT_URL",
        value: "https://myaccount.blob.core.windows.net",
        source: "Environment variable",
        isMasked: false
      },
      {
        variable: "AZURE_STORAGE_CONNECTION_STRING",
        value: "[MASKED]",
        source: "Environment variable",
        isMasked: true
      }
    ],
    metadata: { timestamp, durationMs }
  }

GET /api/dev/env/:key (only if NODE_ENV === 'development')
  Response: {
    success: true,
    data: {
      variable: "AZURE_STORAGE_ACCOUNT_URL",
      value: "https://myaccount.blob.core.windows.net",
      source: "Environment variable",
      isMasked: false
    },
    metadata: { timestamp, durationMs }
  }

If NODE_ENV !== 'development':
  GET /api/dev/env -> { success: false, error: { code: 'FORBIDDEN', message: 'Development routes only available in development mode' }, metadata: { timestamp } }
```

**Sensitive patterns to mask**:
- Keys: SECRET, PASSWORD, TOKEN, KEY, PRIVATE, CREDENTIAL, CONNECTION_STRING, SAS_TOKEN (case-insensitive)
- Value: replaced with "[MASKED]"

**Checklist**:
- [ ] Routes not mounted if NODE_ENV !== 'development'
- [ ] 403 returned if accessed outside development
- [ ] Environment variables with sources listed correctly
- [ ] Sensitive values masked correctly
- [ ] Individual variable endpoint works
- [ ] Response envelope correct
- [ ] Performance acceptable (no expensive operations)

---

## Phase 4: Documentation & Updates

### 4.1 Update Existing Documentation Files

**File**: `/Users/giorgosmarinos/aiwork/agent-platform/azure-storage-tool/docs/design/configuration-guide.md`

**Update sections**:
- Add NODE_ENV as required variable with explanation
- Add container detection variables (PUBLIC_URL, DOCKER_HOST_URL, etc.)
- Add AUTO_SELECT_PORT and explain port conflict behavior
- Add source tracking explanation with example
- Update configuration priority section if changed
- Add reference to development routes and when to use them

**File**: `/Users/giorgosmarinos/aiwork/agent-platform/azure-storage-tool/docs/design/project-functions.md`

**Add**:
- Describe container-aware Swagger URL generation feature
- Describe PORT_CHECKER behavior and AUTO_SELECT_PORT option
- Describe development routes and their security model
- Describe config source tracking and audit capability
- Cross-reference to configuration-guide.md

**File**: `/Users/giorgosmarinos/aiwork/agent-platform/azure-storage-tool/docs/design/project-design.md`

**Update architecture section**:
- Add PortChecker utility class diagram/description
- Add SwaggerServerDetector utility class diagram/description
- Add RuntimeContext data structure description
- Update middleware chain to note runtime detection timing
- Add note about config source tracking implementation

**File**: `/Users/giorgosmarinos/aiwork/agent-platform/azure-storage-tool/CLAUDE.md`

**Update REST API tool documentation section**:
- Update `<azure-fs-api>` tool documentation with NODE_ENV requirement
- Update startup behavior description to mention auto port selection
- Update environment variables table with new vars (NODE_ENV, PUBLIC_URL, AUTO_SELECT_PORT, etc.)
- Add description of development routes under REST API section
- Update configuration priority if changed

**File**: `/Users/giorgosmarinos/aiwork/agent-platform/azure-storage-tool/.env.example`

**Add**:
- NODE_ENV=development
- PUBLIC_URL (commented, optional)
- DOCKER_HOST_URL (commented, optional)
- K8S_SERVICE_HOST (commented, explained as auto-set)
- K8S_SERVICE_PORT (commented, explained as auto-set)
- WEBSITE_HOSTNAME (commented, explained as auto-set)
- WEBSITE_SITE_NAME (commented, explained as auto-set)
- SWAGGER_ADDITIONAL_SERVERS (commented, optional)
- ENABLE_SERVER_VARIABLES (commented, optional)
- AUTO_SELECT_PORT=false
- Section comment explaining container environment detection

### 4.2 Create New Documentation Files

**File**: `/Users/giorgosmarinos/aiwork/agent-platform/azure-storage-tool/docs/reference/container-deployment-guide.md`

**Content**:
- Explanation of container-aware Swagger URL detection
- Examples for each runtime:
  - Azure App Service (WEBSITE_HOSTNAME auto-set)
  - Docker (set DOCKER_HOST_URL or PUBLIC_URL)
  - Kubernetes (K8S_SERVICE_HOST/PORT auto-set)
  - Local development (http://localhost:PORT)
- How to verify correct Swagger URL in each environment
- Troubleshooting section

**File**: `/Users/giorgosmarinos/aiwork/agent-platform/azure-storage-tool/docs/reference/development-endpoints.md`

**Content**:
- Purpose of /api/dev/env endpoints
- How to enable (NODE_ENV=development)
- Security implications and when safe to use
- Example requests and responses
- Sensitive variable masking rules
- Use cases (debugging, configuration validation, etc.)

### 4.3 Update Issues & Pending Items

**File**: `/Users/giorgosmarinos/aiwork/agent-platform/azure-storage-tool/Issues - Pending Items.md`

**Add to completed items section**:
- "Feature 1: PortChecker utility implemented and integrated" ✓
- "Feature 2: NODE_ENV support added with environment-specific behavior" ✓
- "Feature 3: Config source tracking implemented across all loaders" ✓
- "Feature 4: Container-aware Swagger URLs with runtime detection" ✓
- "Feature 5: Development routes for config inspection" ✓

**Check existing items**:
- Remove any related pending items (e.g., "Add PORT_CHECKER")
- Review and update "API implementation alignment with skill" if present

---

## Phase 5: Testing & Validation

### 5.1 Manual Test Cases

**Test 1: NODE_ENV validation**
```bash
# Should fail with clear error
unset NODE_ENV && npm run api

# Should succeed
NODE_ENV=development npm run api
```

**Test 2: PortChecker with unavailable port**
```bash
# Terminal 1
PORT=3000 npm run api

# Terminal 2 (should auto-select to 3001 or fail with process info)
PORT=3000 AUTO_SELECT_PORT=true npm run api
```

**Test 3: Container-aware Swagger URLs**
```bash
# Docker simulation
DOCKER_HOST_URL=http://host.docker.internal:3000 npm run api
# Check /api/docs.json and verify server.url is correct

# Kubernetes simulation
K8S_SERVICE_HOST=api-service.default.svc.cluster.local K8S_SERVICE_PORT=3000 npm run api
# Check /api/docs.json and verify server.url is correct

# Azure App Service simulation
WEBSITE_HOSTNAME=myapi.azurewebsites.net npm run api
# Check /api/docs.json and verify server.url is correct
```

**Test 4: Development routes in development mode**
```bash
NODE_ENV=development npm run api
# Success
curl http://localhost:3000/api/dev/env
# Success
curl http://localhost:3000/api/dev/env/AZURE_STORAGE_ACCOUNT_URL
```

**Test 5: Development routes blocked in production**
```bash
NODE_ENV=production npm run api
# Should return 403
curl http://localhost:3000/api/dev/env
# Expected response: { success: false, error: { code: 'FORBIDDEN', ... } }
```

**Test 6: Config source tracking**
```bash
# Via config file
azure-fs config show --json
# Should include source: ".azure-fs.json"

# Via CLI flag
azure-fs config show -a https://myaccount.blob.core.windows.net --json
# Should include source: "CLI flag" for the account URL

# Via environment
AZURE_STORAGE_ACCOUNT_URL=https://myaccount.blob.core.windows.net azure-fs config show --json
# Should include source: "Environment variable"
```

**Test 7: Sensitive value masking**
```bash
NODE_ENV=development npm run api
curl http://localhost:3000/api/dev/env | jq '.data[] | select(.variable | contains("CONNECTION_STRING"))'
# Should show isMasked: true, value: "[MASKED]"
```

### 5.2 Validation Checklist

- [ ] All new environment variables documented in .env.example
- [ ] NODE_ENV is required and validated
- [ ] PortChecker returns correct availability status
- [ ] Auto port selection works with SWAGGER_ADDITIONAL_SERVERS parsing
- [ ] Development routes return 403 in production
- [ ] Sensitive values are masked correctly
- [ ] Config source tracking shows correct origin
- [ ] Swagger spec generation includes detected servers
- [ ] Health check includes environment field
- [ ] All exit codes unchanged (no new ones needed)
- [ ] No fallback defaults for config values
- [ ] Error messages are clear and actionable

### 5.3 Code Review Checklist

- [ ] No console.log() statements (use Logger)
- [ ] All errors inherit from AzureFsError or AppError
- [ ] TypeScript strict mode compliance
- [ ] No unused imports or variables
- [ ] Error handling for all edge cases (missing env vars, malformed URLs, etc.)
- [ ] Response envelopes follow standard format
- [ ] CORS headers configured correctly
- [ ] Logger injection consistent with existing patterns
- [ ] No hardcoded ports, hosts, or secrets

---

## Phase 6: Deliverables

### 6.1 Code Deliverables

New files:
- `src/utils/port-checker.ts` - PortChecker class
- `src/utils/swagger-server-detector.ts` - RuntimeContext type and detection function
- `src/api/routes/dev.routes.ts` - Development route registration
- `src/api/controllers/dev.controller.ts` - Development endpoint handlers

Modified files:
- `src/config/config.loader.ts` - Add source tracking
- `src/config/config.types.ts` - Add fields for env, sources
- `src/config/config.schema.ts` - Validate NODE_ENV
- `src/api/server.ts` - Integrate PortChecker, RuntimeContext detection
- `src/api/swagger/config.ts` - Use RuntimeContext for servers
- `src/api/routes/health.routes.ts` - Include environment in response
- `src/api/middleware/error-handler.middleware.ts` - Conditional stack traces
- `src/api/routes/index.ts` - Register dev routes conditionally
- `src/commands/config.commands.ts` - Include sources in output
- `.env.example` - Add new variables

### 6.2 Documentation Deliverables

New files:
- `docs/design/feature-implementation-analysis.md` - Investigation findings
- `docs/design/new-config-variables.md` - Environment variable reference
- `docs/design/feature-architecture.md` - Design and integration details
- `docs/design/feature-testing-plan.md` - Testing strategy
- `docs/reference/container-deployment-guide.md` - Runtime environment guide
- `docs/reference/development-endpoints.md` - Dev routes reference

Updated files:
- `docs/design/configuration-guide.md` - Add new variables and source tracking
- `docs/design/project-functions.md` - Describe new features
- `docs/design/project-design.md` - Update architecture
- `CLAUDE.md` - Update REST API tool documentation
- `Issues - Pending Items.md` - Mark completed items

### 6.3 Validation Outputs

- Test results showing all manual test cases passing
- TypeScript compilation successful (`npm run build`)
- No ESLint warnings (if configured)
- Response envelope samples for each new endpoint
- Swagger spec samples for different runtime environments

---

## Success Criteria

Implementation is complete when:

1. **PortChecker**:
   - [x] Detects port availability
   - [x] Auto-selects available port when AUTO_SELECT_PORT=true
   - [x] Fails with helpful error (showing process using port) when port in use and AUTO_SELECT_PORT=false
   - [x] Integrated before server.listen()

2. **NODE_ENV Support**:
   - [x] Required environment variable
   - [x] Validated to be one of: development, production, staging
   - [x] Included in health check response
   - [x] Used to control error stack trace visibility and development routes

3. **Config Source Tracking**:
   - [x] Tracks origin of each config value
   - [x] Exposed in config show command
   - [x] Exposed in development routes
   - [x] Works across file, env, and CLI sources

4. **Container-Aware Swagger**:
   - [x] Detects and uses correct server URL for Azure App Service
   - [x] Detects and uses correct server URL for Kubernetes
   - [x] Detects and uses correct server URL for Docker
   - [x] Supports PUBLIC_URL override
   - [x] Supports SWAGGER_ADDITIONAL_SERVERS
   - [x] Supports ENABLE_SERVER_VARIABLES for dynamic paths

5. **Development Routes**:
   - [x] GET /api/dev/env returns all env vars with sources and masking
   - [x] GET /api/dev/env/:key returns single var with source and masking
   - [x] Both return 403 outside development mode
   - [x] Sensitive values (SECRET, PASSWORD, TOKEN, etc.) are masked

6. **Documentation**:
   - [x] All new environment variables documented
   - [x] Configuration guide updated
   - [x] Project functions document updated
   - [x] Project design updated
   - [x] CLAUDE.md tool documentation updated
   - [x] Container deployment guide created
   - [x] Development endpoints reference created
   - [x] Issues/pending items updated

7. **Quality**:
   - [x] No TypeScript errors
   - [x] All error cases handled
   - [x] Consistent with existing code patterns
   - [x] All tests passing (manual or automated)
   - [x] No fallback defaults for configuration
   - [x] Clear, actionable error messages

---

## Execution Order

Implement in this order (dependencies matter):

1. ✓ Phase 1: Investigation & Analysis
2. ✓ Phase 2: Planning & Design (all documents)
3. **Phase 3: Implementation**
   - Step 1: NODE_ENV support (simplest, needed for dev routes protection)
   - Step 2: PortChecker utility (can be tested independently)
   - Step 3: Config source tracking (foundation for dev routes and config show)
   - Step 4: Container-aware Swagger (builds on port resolution)
   - Step 5: Development routes (depends on config source tracking)
4. **Phase 4: Documentation & Updates** (as each feature completes)
5. **Phase 5: Testing & Validation** (full integration testing)
6. **Phase 6: Final Review** (code review, docs review, git commit)

---

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| PortChecker fails on Windows | Implement `getProcessUsingPort()` with both `lsof` and `netstat` with OS detection |
| Config source tracking causes performance issues | Use simple Map instead of complex tracking; measure startup time |
| Development routes leak sensitive info | Double-check masking patterns, test with various secret names |
| Container-aware Swagger breaks existing deployments | Make all new env vars optional with sensible fallbacks to localhost:port |
| NODE_ENV missing breaks startup | Clear error message and update .env.example prominently |

---

## References

- **Skill Blueprint**: `/Users/giorgosmarinos/.claude/skills/create-api-base/01-model-api-option.md`
- **Deviation Analysis**: `docs/design/api-skill-deviation-analysis.md`
- **Current API Code**: `src/api/`
- **Current Config Code**: `src/config/`
- **Project CLAUDE.md**: Tool documentation format and standards
- **Global CLAUDE.md**: `/Users/giorgosmarinos/.claude/CLAUDE.md` (project instructions)

---

## Implementation Notes

- Use the existing Logger utility for all logging (no console.log)
- Follow existing error handling patterns (AzureFsError subclasses)
- Maintain response envelope consistency (`buildResponse()` helper)
- Keep PortChecker and SwaggerServerDetector as utility functions/classes (no dependencies on domain logic)
- All environment variable loading happens in `config.loader.ts`
- Development routes controller should use factory pattern like other controllers
- No synchronous I/O in hot paths (especially port checking should be async)
- Test locally before considering container environments

