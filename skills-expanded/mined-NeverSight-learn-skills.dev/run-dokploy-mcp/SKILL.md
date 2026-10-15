---
name: run-dokploy-mcp
description: Deploy, manage, and monitor services on Dokploy via MCP tools. Use when deploying apps, checking logs, managing domains, updating environment variables, or inspecting container status on the Dokploy host.
---

# Dokploy MCP Integration

Manage Dokploy services exclusively through MCP tools (`mcp__dokploy__*`). Never call the Dokploy HTTP API directly — no `curl`, no `fetch`.

## Cardinal Rule: `project-all` Is Huge

`project-all` returns **140K+ characters** on most instances. It will blow the context window if read directly. Always use the Python extraction pattern.

### Finding Resource IDs

```bash
# Step 1: Call mcp__dokploy__project-all (output auto-saved to file by harness)
# Step 2: Extract with the helper script:
python3 .claude/skills/run-dokploy-mcp/extract.py <output-file> [filter-term]
```

Example:
```bash
python3 .claude/skills/run-dokploy-mcp/extract.py /tmp/result.txt my-project
# Output:
# Project: My Project (ID: abc-123)
#   Environment: production (ID: env-456)
#     Application: frontend | ID: app-789 | Status: running
#     Compose: supabase | ID: comp-012 | Status: running
#     Postgres: db | ID: pg-345
```

### Data Structure

```
projects[] > environments[] > {
  applications[], compose[],
  postgres[], mysql[], mariadb[],
  mongo[], redis[], libsql[]
}
```

ID fields: `projectId`, `environmentId`, `applicationId`, `composeId`, `postgresId`, etc.

## Common Operations

### Look Up a Specific Resource (when you have the ID)

```
mcp__dokploy__project-one(projectId: "...")
mcp__dokploy__compose-one(composeId: "...")
mcp__dokploy__application-one(applicationId: "...")
```

### Deploy

```
mcp__dokploy__application-deploy(applicationId: "...")
mcp__dokploy__compose-deploy(composeId: "...")
```

After deploying, check: `mcp__dokploy__deployment-queueList()`

### Read Logs

```
mcp__dokploy__application-readLogs(applicationId: "...", tail: 50, search: "error")
mcp__dokploy__compose-readLogs(composeId: "...", containerId: "...", tail: 50)
```

For compose logs, `containerId` is the Docker container name (e.g. `myapp-next-x7k2p-next-1`), not the compose ID.

### Update Environment Variables

```
# Application (newline-separated KEY=value, not JSON)
mcp__dokploy__application-saveEnvironment(
  applicationId: "...",
  env: "KEY=value\nKEY2=value2",
  buildArgs: null,
  buildSecrets: null,
  createEnvFile: true
)

# Compose
mcp__dokploy__compose-saveEnvironment(composeId: "...", env: "KEY=value\nKEY2=value2")
```

### Manage Domains

```
mcp__dokploy__domain-byApplicationId(applicationId: "...")
mcp__dokploy__domain-create(host: "example.it", port: 3000, https: true, certificateType: "letsencrypt", applicationId: "...")
mcp__dokploy__domain-update(domainId: "...", host: "new.example.it", https: true)
```

### Docker Containers

```
mcp__dokploy__docker-getContainers()                              # all containers on host
mcp__dokploy__docker-getContainersByAppLabel(appName: "...", type: "standalone")
mcp__dokploy__docker-restartContainer(containerId: "...")
```

`serverId` is optional — omit for the Dokploy host (most services).

## Update Patterns

### Application Update

```
mcp__dokploy__application-update(applicationId: "...", description: "New desc")
```

Only `applicationId` is required. Omitted fields stay unchanged. `appName` must match `^[a-zA-Z0-9._-]+$` (max 63 chars).

### Compose Update

```
mcp__dokploy__compose-update(
  composeId: "...",
  sourceType: "github",
  repository: "RepoName",
  owner: "OrgName",
  branch: "main",
  composePath: "docker-compose.yml",
  autoDeploy: true
)
```

Only `composeId` is required.

### Project Update

```
mcp__dokploy__project-update(projectId: "...", name: "ProjectName", description: "...")
```

**Must include `name`** even if only changing description.

## Anti-Patterns

| Don't | Why | Do This Instead |
|---|---|---|
| Read `project-all` output directly | 140K+ chars, blows context | Python extraction (`extract.py`) |
| Rely on `*-search` tools | Frequently return "not found" | `project-all` + filter |
| Forget `name` in project-update | Required in practice | Always include current `name` |
| Pass `serverId` everywhere | Most services use host | Only for remote servers |
| Confuse `composeId` / `containerId` | Different things | Compose logs need Docker container ID |
| Send bare "not found" to model | Model fixates on failure | Immediately try `project-all` fallback |

## Destructive Operations — Always Confirm First

These are irreversible:
- `application-delete`, `compose-delete`, `postgres-remove`
- `settings-cleanAll`, `settings-cleanDockerPrune`
- `server-remove`

## Deployment Status

```
mcp__dokploy__deployment-all(applicationId: "...")
mcp__dokploy__deployment-allByCompose(composeId: "...")
mcp__dokploy__deployment-queueList()
```

## Field Reference

| Concept | Field | Values/Notes |
|---|---|---|
| Source type | `sourceType` | `github`, `git`, `raw`, `docker`, `gitlab`, `bitbucket`, `gitea`, `drop` |
| Build type | `buildType` | `nixpacks`, `dockerfile`, `railpack`, `heroku_buildpacks`, `paketo_buildpacks`, `static` |
| Status | `applicationStatus` | `idle`, `running`, `done`, `error` |
| Server | `serverId` | `null` = Dokploy host |

## Troubleshooting

| Symptom | Fix |
|---|---|
| `project-all` output too large | Use `extract.py` — never read raw output |
| `compose-search` returns "not found" | Fall back to `project-all` + Python filter |
| Deploy queued but not running | Check `deployment-queueList()` for stuck items |
| Container crash-looping | `application-readLogs(tail: 50, search: "error")` |
| Port conflict between services | Check `docker-getContainers()` for conflicting published ports |
| Env vars not taking effect | Ensure `createEnvFile: true` and redeploy after saving |
| `compose-one` on Supabase returns 70K+ | Huge env block — extract specific fields with Python instead of reading full output |
