---
name: chat-app-utilities
description: "Adding admin monitoring, config CRUD, chat pipeline with Genie/KA sources, FastAPI router factories for Databricks Apps"
---

# Chat App Utilities

Full-stack library providing chat orchestration, admin/config FastAPI routers, and React monitoring components for Databricks Apps.

- **Source:** `https://github.com/databricks-field-eng/agent-chat-app-utilities.git`
- **Python:** `pip install chat-app-utilities[all]`
- **TypeScript:** `npm install @chat-app-utilities/react`

## When to Use

Use this package when you need:

- Chat orchestration with Genie and Knowledge Assistant sources
- Admin monitoring endpoints (cache stats, memory, chat logs, system diagnostics)
- Config CRUD endpoints (branding, presets, logo/font upload)
- Chat history endpoints (sessions, messages, scoped by dataset)
- Auth utilities for Lakebase PostgreSQL and Databricks WorkspaceClient
- React components for floating chat, monitoring tabs

This package provides the **backend routers** that power the **configurable-react-template** frontend (see that skill).

## Prerequisites

- Python 3.9+ (use `Optional[X]` not `X | None` for Databricks App compatibility)
- FastAPI backend on **port 8000**
- Lakebase PostgreSQL instance (for history, config, cache storage)
- Databricks workspace with serving endpoints

## Installation

**NOT published to PyPI or npm.** Install via vendoring or local file reference.

**Python — vendor into your app:**
```bash
# Clone into your project directory
git clone https://github.com/databricks-field-eng/agent-chat-app-utilities.git
# Then in requirements.txt or setup.py, reference the local path:
# -e ./chat-app-utilities[all]
```

**TypeScript — the React components are bundled in the same repo:**
```json
// package.json — use file: reference
{
  "dependencies": {
    "@chat-app-utilities/react": "file:../../chat-app-utilities/react"
  }
}
```

## 8-Phase Chat Orchestration Pipeline

The `ChatOrchestrator` processes each message through 8 phases:

1. **Deictic Resolution** -- Resolves pronouns and references ("that product", "the previous chart") using conversation context
2. **Cache Lookup** -- Checks `SemanticCache` (from **lakebase-semantic-cache**) for semantically similar prior answers
3. **Classification** -- `RegexClassifier` routes the query to relevant sources (Genie, KA, etc.)
4. **Fan-out** -- Invokes matching `DataSource` instances in parallel with configurable timeout
5. **Collection** -- Gathers results from all sources into a unified context block
6. **Memory Retrieval** -- If enabled, retrieves relevant memories from **agent-memory-service**
7. **FM Synthesis** -- Sends context + query to the foundation model endpoint for final answer
8. **Post-processing** -- Caches the result, stores conversation memory, appends tools-used badge

## Quick Start (Python Backend)

```python
from fastapi import FastAPI
from chat_app_utilities import ChatOrchestrator, RegexClassifier
from chat_app_utilities.pipeline.sources.genie import GenieSource
from chat_app_utilities.pipeline.sources.ka import KASource
from chat_app_utilities.history.router import create_history_router
from chat_app_utilities.admin import create_admin_router
from chat_app_utilities.config import create_config_router
from chat_app_utilities.auth.lakebase import get_workspace_client, get_db_cursor

app = FastAPI()

# Chat orchestrator
orchestrator = ChatOrchestrator(
    fm_endpoint="databricks-claude-sonnet-4-5",
    system_prompt_builder=lambda sources: "You are a helpful assistant.",
    sources=[
        GenieSource(name="genie", space_id_fn=lambda: "my-space-id"),
        KASource(name="ka", endpoint_fn=lambda: "my-ka-endpoint"),
    ],
    classifier=RegexClassifier(
        source_patterns={"genie": [r"price", r"sales", r"revenue"], "ka": [r"policy", r"document"]},
    ),
    workspace_client_fn=get_workspace_client,
)

@app.post("/api/chat")
async def chat(body: dict):
    from chat_app_utilities import ChatRequest
    request = ChatRequest(**body)
    return await orchestrator.chat(request)

# Mount routers
app.include_router(create_history_router(get_db_cursor=get_db_cursor), prefix="/api", tags=["history"])
app.include_router(create_admin_router(get_db_cursor=get_db_cursor), prefix="/api", tags=["admin"])
app.include_router(create_config_router(get_db_cursor=get_db_cursor, default_config={"company_name": "My Company", "color_primary": "#1B3139"}), prefix="/api", tags=["config"])
```

## Quick Start (React Frontend)

```tsx
import { FloatingChat, useChatState, createChatApi, createAdminApi } from "@chat-app-utilities/react";

const chatApi = createChatApi("/api");
const adminApi = createAdminApi("/api");

function App() {
  const chatState = useChatState({ api: chatApi, storageKey: "my-app" });
  return <FloatingChat chatState={chatState} visible={true} />;
}
```

## Key Classes

| Class | Purpose |
|---|---|
| `ChatOrchestrator` | 8-phase pipeline: deictic resolution, cache, classify, fan-out, collect, memory, FM, post-process |
| `RegexClassifier` | Pattern-based query routing to sources. Detects meta-questions and chitchat. |
| `DeicticResolver` | Resolves pronouns/references using FM |
| `GenieSource` | Databricks Genie Space data source |
| `KASource` | Databricks Knowledge Assistant data source |
| `DataSource` | Abstract base class for custom sources |

## Router Factories

All routers auto-create their tables on first access (`CREATE TABLE IF NOT EXISTS`). No manual table creation needed.

| Factory | Endpoints | Auto-created Tables |
|---|---|---|
| `create_history_router()` | `GET /chat/history/{id}`, `PUT /chat/history`, `DELETE /chat/history/{id}`, `GET /chat/sessions` | `chat_history` |
| `create_admin_router()` | `/admin/cache/*`, `/admin/memory/*`, `/admin/system`, `/admin/chat/*`, `/admin/install-pgvector`, `/admin/cache/invalidate`, `/admin/cache/clear`, `/admin/cache/cleanup` | — |
| `create_config_router()` | `GET /config`, `PATCH /config`, `POST /config/logo`, `POST /config/font`, `POST /config/reset`, `GET /config/presets`, `POST /config/presets` | `demo_config`, `demo_presets` |

**Note:** `create_admin_router` system diagnostics and pgvector install work even without `semantic_cache` installed — they fall back to `get_db_cursor` for PG operations.

## Auth Utilities

```python
from chat_app_utilities.auth.lakebase import get_workspace_client, get_db_cursor, get_pg_connection

# Singleton WorkspaceClient with Databricks unified auth
ws = get_workspace_client()

# Context manager for database cursor (requires LAKEBASE_ENDPOINT env var)
with get_db_cursor() as cursor:
    cursor.execute("SELECT 1")

# Raw psycopg2 connection with health check + reconnect
conn = get_pg_connection()
```

### Lakebase API Path Distinction

The auth module supports **autoscaling Lakebase** (`/api/2.0/postgres/` API) via the `LAKEBASE_ENDPOINT` env var. Regular (non-autoscaling) Lakebase instances use `/api/2.0/database/` API and are configured via the `LAKEBASE_INSTANCE` env var instead. When `LAKEBASE_INSTANCE` is set, the auth module resolves the connection dynamically using `GET /api/2.0/database/instances/{name}` for the `read_write_dns` host and `POST /api/2.0/database/credentials` for OAuth-based credentials. Use one or the other, not both.

### Lakebase Bootstrap Requirements

Fresh Lakebase instances don't give the app's service principal permission to create tables. Before the app can work:

1. **Workspace owner must run** (once, via SQL console or psql):
   ```sql
   GRANT CREATE ON SCHEMA public TO PUBLIC;
   GRANT ALL ON ALL TABLES IN SCHEMA public TO PUBLIC;
   ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO PUBLIC;
   ```

2. **Tables are auto-created** by `create_config_router()` and `create_history_router()` on first access. No manual table creation needed.

### Lakebase Resource PATCH API Quirk

When attaching Lakebase as a resource via `PATCH /api/2.0/apps/{name}`, the resource `name` field **cannot match** the Lakebase instance name. Use a different name (e.g., `"my-app-lakebase"` instead of `"my-app-db"`).

## React Components

| Component | Purpose |
|---|---|
| `FloatingChat` | Collapsible chat widget with session management |
| `ChatMessage` | Single message bubble with markdown rendering |
| `MentionDropdown` | @-mention autocomplete dropdown |
| `MentionChips` | Attached mention chips display |

## React Hooks

| Hook | Returns |
|---|---|
| `useChatState({ api, storageKey })` | `ChatState` -- messages, sessions, send function, input state |
| `useMentionState({ items, onSelect })` | `MentionState` -- dropdown state, keyboard handlers |

## TypeScript API Factories

| Factory | Returns |
|---|---|
| `createChatApi(baseUrl)` | `sendMessage`, `loadHistory`, `saveHistory`, `clearHistory`, `listSessions` |
| `createAdminApi(baseUrl)` | Methods matching template `*TabApi` interfaces: `getStats`, `getEntries`, `getEntryDetail`, `getEvents`, `deleteEntry`, `getCacheConfig`, `updateCacheConfig`, `invalidateCache`, `clearCache`, `cleanupExpired`, `getDiagnostics`, `installPgvector`, `getSessions`, `getSessionDetail`, plus `search`/`deleteEntry` for memory |

**Recommended pattern:** Instead of using `createAdminApi()`, build per-plugin API objects in `apiFactories.ts` that directly satisfy each `*TabApi` interface. This avoids key collision between `CacheTabApi.getEntries` and `MemoryTabApi.getEntries` when flat-merging.

## CSS Theming

React components use CSS custom properties for theming, with Databricks defaults:

```css
--color-primary: #1B3139;
--color-accent: #FF3621;
--color-success: #00984A;
--color-warning: #EB7B30;
--color-danger: #DF002C;
--color-light-bg: #F9F7F4;
```

These are set automatically when used with the **configurable-react-template** `BrandingProvider`.

## Guardrails

- NEVER delete existing Databricks Apps or shared resources without explicit user confirmation.
- NEVER use `X | None` syntax -- use `Optional[X]` for Python 3.9 compatibility.
- NEVER hardcode Lakebase PGHOST -- resolve dynamically via the credentials API.
- ALWAYS use port 8000 for the FastAPI server (Databricks App proxy requirement).
- ALWAYS run `GRANT CREATE ON SCHEMA public TO PUBLIC` on fresh Lakebase instances before the app can create tables.
- The `resources:` block in `app.yaml` is NOT read by `databricks apps deploy` — must use `PATCH /api/2.0/apps/{name}` with `resources` array to attach resources.
- Lakebase resource name in PATCH cannot match the instance name — use a different identifier.
