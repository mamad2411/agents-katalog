# OpenClaw — AI Capability Manifest

## Identity

OpenClaw is an infrastructure generation platform that produces production-ready Docker Compose stacks from a list of services, skill packs, and configuration options. It supports 95+ Docker services, 10+ presets, and 10+ skill packs covering AI, automation, monitoring, media, security, and more.

## Connection Methods

### MCP Server (Recommended for AI Agents)

```json
{
  "mcpServers": {
    "better-openclaw": {
      "command": "npx",
      "args": ["-y", "@better-openclaw/mcp"]
    }
  }
}
```

Transport: stdio. Compatible with Claude Desktop, Cursor, Claude Code, and any MCP client.

### REST API

Base URL: `http://localhost:3456/api/v1`

OpenAPI spec: `GET /openapi.json`
Swagger docs: `GET /docs`

### CLI

```bash
npx create-better-openclaw generate --preset researcher
```

---

## Available Tools

### Discovery Tools

#### `list-services`
List all available Docker services. Optionally filter by category or maturity.
- **Input**: `{ category?: string, maturity?: "stable" | "beta" | "experimental" }`
- **Output**: Array of `{ id, name, description, category, maturity, tags }`

#### `get-service`
Get the complete definition of a service by ID.
- **Input**: `{ id: string }`
- **Output**: Full `ServiceDefinition` (image, ports, env vars, volumes, dependencies, healthcheck, resource limits)

#### `search-services`
Keyword search across service names, descriptions, tags, and categories.
- **Input**: `{ query: string, limit?: number }`
- **Output**: Scored results `{ id, name, description, category, score }`

#### `suggest-services`
Suggest services from a natural language description of what to build.
- **Input**: `{ description: string, limit?: number }`
- **Output**: Scored suggestions with match reasons

#### `list-presets`
List all curated presets (service bundles for common use cases).
- **Input**: `{}`
- **Output**: Array of `{ id, name, description, services[], estimatedMemoryMB }`

#### `get-preset`
Get preset details with fully resolved dependency tree.
- **Input**: `{ id: string }`
- **Output**: Preset definition + resolved service list with transitive dependencies

#### `list-skill-packs`
List skill packs, optionally filtered by service compatibility.
- **Input**: `{ serviceIds?: string[] }`
- **Output**: Array of `{ id, name, description, requiredServices[], skills[], tags }`

### Composition Tools

#### `resolve-dependencies`
Resolve service dependencies, detect conflicts, and estimate memory.
- **Input**: `{ services: string[], skillPacks?: string[], proxy?, gpu?, platform?, monitoring? }`
- **Output**: `{ isValid, services[], addedDependencies[], errors[], warnings[], estimatedMemoryMB }`

#### `validate-stack`
Full validation pipeline: resolve -> compose -> validate (ports, volumes, YAML, DAG).
- **Input**: `{ services: string[], skillPacks?, proxy?, domain?, gpu?, platform?, monitoring? }`
- **Output**: `{ valid, errors[], warnings[], serviceCount, estimatedMemoryMB }`

#### `generate-stack`
Generate a complete Docker Compose stack. Returns all files as a JSON map.
- **Input**: `{ projectName: string, services: string[], skillPacks?, proxy?, domain?, gpu?, platform?, monitoring?, generateSecrets? }`
- **Output**: `{ files: { [filename]: content }, metadata, fileList }`

---

## Data Model

### Service IDs
Kebab-case identifiers. Examples: `postgresql`, `redis`, `n8n`, `ollama`, `caddy`, `grafana`, `qdrant`, `meilisearch`

### Service Categories
`ai`, `ai-platform`, `analytics`, `automation`, `browser`, `coding-agent`, `communication`, `database`, `desktop`, `dev-tools`, `knowledge`, `media`, `monitoring`, `proxy`, `search`, `security`, `social-media`, `storage`, `streaming`, `vector-db`

### Presets
`minimal`, `creator`, `researcher`, `devops`, `full`, `content-creator`, `ai-playground`, `ai-powerhouse`, `coding-team`, `lasuite-meet`

### Skill Packs
`video-creator`, `research-agent`, `social-media`, `dev-ops`, `knowledge-base`, `local-ai`, `content-creator`, `ai-playground`, `coding-team`, `knowledge-hub`

### GenerationInput Shape
```json
{
  "projectName": "my-stack",
  "services": ["postgresql", "redis", "n8n"],
  "skillPacks": ["dev-ops"],
  "proxy": "none | caddy | traefik",
  "domain": "example.com",
  "gpu": false,
  "platform": "linux/amd64 | linux/arm64",
  "monitoring": false,
  "generateSecrets": true
}
```

---

## MCP Resources

| URI | Description |
|-----|-------------|
| `openclaw://services` | Full service catalog with summaries |
| `openclaw://presets` | All preset definitions |
| `openclaw://skills` | All skill pack definitions |

---

## Example Agent Workflows

### 1. User wants a research stack

```
1. list-presets → find "researcher" preset
2. get-preset({ id: "researcher" }) → see resolved services and memory estimate
3. generate-stack({ projectName: "my-research", services: [...preset.services], proxy: "caddy", domain: "research.local" })
4. Return docker-compose.yml and .env to user
```

### 2. User asks "what can I use for AI?"

```
1. list-services({ category: "ai" }) → get all AI services
2. list-services({ category: "ai-platform" }) → get AI platform services
3. list-skill-packs() → find AI-related skill packs
4. suggest-services({ description: "AI chatbot with document search" }) → get recommendations
5. Present options to user with descriptions and memory estimates
```

### 3. User wants to add monitoring to their services

```
1. resolve-dependencies({ services: ["redis", "postgresql", "n8n"], monitoring: true })
   → see which monitoring services get auto-added (grafana, prometheus)
2. validate-stack({ services: [...resolved], monitoring: true })
   → verify no conflicts
3. generate-stack({ projectName: "my-app", services: [...], monitoring: true })
```

### 4. Build a custom stack from scratch

```
1. suggest-services({ description: "video processing with notifications and storage" })
   → get suggested services
2. resolve-dependencies({ services: ["ffmpeg", "minio", "ntfy"] })
   → check dependencies, get memory estimate
3. validate-stack({ services: [...resolved] })
   → verify everything works together
4. generate-stack({ projectName: "video-pipeline", services: [...], generateSecrets: true })
   → get all deployment files
```

---

## Output Files

A generated stack typically includes:
- `docker-compose.yml` — Main compose file
- `docker-compose.*.yml` — Profile-specific compose files (ai, monitoring, tools, etc.)
- `.env` / `.env.example` — Environment variables with generated secrets
- `README.md` — Setup instructions
- `scripts/` — Helper scripts (start, stop, backup, etc.)
- `Caddyfile` or `traefik/` — Reverse proxy configuration (if proxy selected)
- `grafana/` / `prometheus/` — Monitoring configs (if monitoring enabled)
- `init-db.sql` — PostgreSQL initialization (if PostgreSQL used)
- `skills/` — Skill documentation with connection details
