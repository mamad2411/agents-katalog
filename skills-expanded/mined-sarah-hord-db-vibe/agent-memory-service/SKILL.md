---
name: agent-memory-service
description: "Persistent memory for AI agents, MCP memory service, cross-conversation agent memory on Databricks"
---

# Agent Memory Service

Persistent, searchable memory for AI agents deployed as a Databricks App with MCP SSE transport, Lakebase PostgreSQL storage, and async Delta sync.

- **Source:** `https://github.com/databricks-field-eng/lakebase-agent-memory-service.git`

## When to Use

Use this service when you need:

- Persistent memory that survives across agent conversations
- Searchable memory with semantic similarity (pgvector)
- Row-level access control per user/owner
- MCP-compatible memory tools for any AI agent
- Unity Catalog registration for governance and audit

## Architecture

```
Agent/Client  -->  MCP SSE  -->  Databricks App (FastAPI, port 8000)
                                      |
                                      v
                                 Lakebase PostgreSQL (pgvector)
                                      |
                                      v
                                 Delta Sync (async to Unity Catalog)
```

- **Transport:** MCP over Server-Sent Events (SSE) at `/sse`
- **Storage:** Lakebase PostgreSQL with pgvector for semantic search
- **Identity:** X-Forwarded-Email > X-Forwarded-User (UUID) > project-only scope
- **Access control:** Row-level filtering by `owner_email`, soft-delete

## Prerequisites

- Databricks workspace with Apps enabled
- Lakebase PostgreSQL instance with pgvector extension
- A Databricks LLM serving endpoint (for summarization tool)
- Terraform (optional, for infrastructure provisioning)

## MCP Tools (5)

| Tool | Description |
|---|---|
| `store_memory_tool` | Store a new memory with type, content, and optional tags |
| `search_memories_tool` | Semantic search across memories by query string |
| `get_memories_tool` | List memories with optional type and date filters |
| `delete_memory_tool` | Soft-delete a memory by ID |
| `summarize_conversation_tool` | Summarize a conversation and store as memory |

### Memory Types

| Type | Purpose |
|---|---|
| `conversation_summary` | Auto-generated summaries of past conversations |
| `project_fact` | Facts about projects, architectures, decisions |
| `user_preference` | User preferences, coding style, tool choices |

## Quick Start: Deploying the Service

### 1. Clone and configure

```bash
git clone https://github.com/databricks-field-eng/lakebase-agent-memory-service.git
cd dbx-agentic-memory-as-a-service
```

### 2. Set environment variables

```bash
# Required -- one of these connection methods
ENDPOINT_NAME=my-lakebase-endpoint        # Autoscaling endpoint
# OR
LAKEBASE_INSTANCE=my-lakebase-instance    # Provisioned instance
# OR
PGHOST=... PGUSER=... PGPASSWORD=...     # Direct connection

# Required
DATABRICKS_HOST=https://my-workspace.cloud.databricks.com
LLM_ENDPOINT=databricks-claude-sonnet-4-6   # For summarization
```

### 3. Configure app.yaml

```yaml
command: ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "8000"]
resources:
  - name: my-lakebase
    database:
      instance: my-lakebase-instance
      permission: CAN_CONNECT_AND_CREATE
```

### 4. Deploy

```bash
databricks apps deploy agent-memory --source-code-path=/Workspace/path/to/app
```

### 5. Register in Unity Catalog

Create an HTTP connection with `is_mcp_connection: true` and `base_path: /sse` pointing to the app URL.

## Library API

For programmatic access (e.g., from another Python service):

```python
from mcp_memory import configure, init_schema, store_memory, search_memories

# Configure connection
configure(endpoint_name="my-lakebase-endpoint")

# Initialize schema (run once)
init_schema()

# Store a memory
memory_id = store_memory(
    conversation_id="conv-001",
    project_id="my-project",
    memory_type="user_preference",
    content="User prefers dark mode and uses Vim keybindings",
    owner_email="user@example.com",
    tags={"source": "conversation", "confidence": "high"},
)

# Search memories
results = search_memories(
    project_id="my-project",
    query_text="What editor preferences does the user have?",
    owner_email="user@example.com",
    limit=5,
)
for memory in results:
    print(f"[{memory['similarity']:.2f}] {memory['content']}")
```

## Identity Resolution

The service resolves user identity from HTTP headers in this priority:

1. **X-Forwarded-Email** -- Preferred. Set by the Databricks App proxy for browser-authenticated users.
2. **X-Forwarded-User** -- Fallback. Contains UUID, less human-readable.
3. **Project-only scope** -- If no user identity is available, memories are scoped to the project only.

All memory operations are filtered by the resolved identity, providing row-level access control.

## Infrastructure (Terraform)

The repo includes Terraform modules for provisioning:

| File | Purpose |
|---|---|
| `terraform/main.tf` | App definition, service principal |
| `terraform/variables.tf` | Configurable inputs (instance name, workspace URL, etc.) |
| `terraform/lakebase.tf` | Lakebase instance and database |
| `terraform/uc_connection.tf` | Unity Catalog HTTP connection for MCP |
| `terraform/app.tf` | Databricks App resource definition |
| `terraform/outputs.tf` | Terraform output values |
| `terraform/uc_audit.tf` | Audit logging configuration |

```bash
cd terraform
terraform init
terraform plan -var="workspace_url=https://my-workspace.cloud.databricks.com"
terraform apply
```

## Integration with ChatOrchestrator

The memory service integrates with **chat-app-utilities** `ChatOrchestrator` via the `memory_project_fn` parameter:

```python
from chat_app_utilities import ChatOrchestrator

orchestrator = ChatOrchestrator(
    fm_endpoint="databricks-claude-sonnet-4-6",
    system_prompt_builder=lambda s: "You are helpful.",
    memory_project_fn=lambda: f"my-app-{get_current_user()}",
    workspace_client_fn=get_workspace_client,
)
```

When `memory_project_fn` is set, the orchestrator:
- **Phase 6:** Retrieves relevant memories and injects them into the FM context
- **Phase 8:** Stores conversation summaries as new memories

## Monitoring

Add the `memoryPlugin()` to the **configurable-react-template** admin panel:

```tsx
import { AdminPage, memoryPlugin } from "@configurable-react-client/template";

<AdminPage
  plugins={[memoryPlugin()]}
  configApi={configApi}
  onBack={handleBack}
/>
```

This provides a UI for browsing, searching, and deleting stored memories.

See `references/api-reference.md` for complete tool signatures and API details.

## Guardrails

- NEVER delete existing Databricks Apps or shared resources without explicit user confirmation.
- NEVER hardcode PGHOST -- resolve dynamically via endpoint name or instance name.
- NEVER expose memory content across users -- always scope by owner_email.
- ALWAYS use `CAN_CONNECT_AND_CREATE` permission for the Lakebase resource.
- ALWAYS use port 8000 (Databricks App proxy requirement).
