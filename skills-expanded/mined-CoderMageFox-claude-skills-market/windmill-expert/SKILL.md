---
name: windmill-expert
description: Comprehensive Windmill workflow platform expert. Use when building scripts, flows, apps, or managing resources in Windmill. Covers TypeScript/Python/Go/Bash scripting, multi-step workflows, UI apps, schedules, webhooks, and API integration.
---

# Windmill Expert Skill

Complete guide for building internal tools, workflows, and automation with Windmill.

---

## What is Windmill?

Windmill is an **open-source developer platform** for building:
- **Scripts**: TypeScript, Python, Go, Bash, SQL, GraphQL
- **Flows**: Multi-step workflows with branching, loops, error handling
- **Apps**: Low-code UI builder with data binding
- **Schedules**: Cron-based automation
- **Webhooks**: HTTP endpoints for external triggers

**Key Features**:
- Auto-generated UIs from script parameters
- Resource management (DB connections, API keys)
- Version control and audit logs
- Approval flows and human-in-the-loop
- Enterprise SSO and RBAC

---

## Quick Reference

### Core Concepts

| Concept | Description | Path Format |
|---------|-------------|-------------|
| **Script** | Single executable unit | `f/folder/script_name` |
| **Flow** | Multi-step workflow | `f/folder/flow_name` |
| **App** | UI application | `f/folder/app_name` |
| **Resource** | Credentials/configs | `f/folder/resource_name` |
| **Variable** | Key-value storage | `f/folder/variable_name` |
| **Schedule** | Cron trigger | `schedule_name` |

### Path Conventions
```
u/username/script_name    # User scripts (private)
f/folder/script_name      # Folder scripts (shared)
g/group/script_name       # Group scripts
```

### Supported Languages
| Language | File Extension | Use Case |
|----------|---------------|----------|
| TypeScript | `.ts` | General purpose, APIs |
| Python | `.py` | Data processing, ML |
| Go | `.go` | Performance critical |
| Bash | `.sh` | System operations |
| SQL | `.sql` | Database queries |
| GraphQL | `.graphql` | GraphQL APIs |

---

## Detailed Guides

For comprehensive guidance on each topic:

- **[scripts.md](scripts.md)** - Script development in all languages
- **[flows.md](flows.md)** - Multi-step workflow design
- **[apps.md](apps.md)** - UI application building
- **[api_reference.md](api_reference.md)** - REST API documentation
- **[resources.md](resources.md)** - Resource and variable management

---

## Common Patterns

### Pattern 1: Database Query Script
```typescript
import * as wmill from "windmill-client";
import { Client } from "pg";

export async function main(query: string) {
  const db = await wmill.getResource("f/databases/postgres");
  const client = new Client(db);
  await client.connect();
  const result = await client.query(query);
  await client.end();
  return result.rows;
}
```

### Pattern 2: API Integration Script
```python
import wmill
import requests

def main(endpoint: str, method: str = "GET"):
    api_key = wmill.get_variable("f/secrets/api_key")
    base_url = wmill.get_variable("f/config/base_url")

    response = requests.request(
        method,
        f"{base_url}/{endpoint}",
        headers={"Authorization": f"Bearer {api_key}"}
    )
    return response.json()
```

### Pattern 3: ETL Flow
```
Extract (Script A) → Transform (Script B) → Load (Script C)
     ↓                    ↓                    ↓
  results.a           results.b            results.c
```

### Pattern 4: Approval Workflow
```
Request → Approval Step → [Approved] → Execute
                       → [Rejected] → Notify
```

---

## Best Practices

### ✅ Do
- Use Resources for credentials (encrypted at rest)
- Use Variables for configuration
- Add proper error handling in scripts
- Use typed parameters for auto-generated UIs
- Test scripts before adding to flows
- Use meaningful path names

### ❌ Don't
- Hardcode credentials in scripts
- Skip error handling
- Create overly complex single scripts
- Ignore type annotations
- Mix concerns in one script

---

## Integration with Infrastructure

Your Windmill instance:
- **URL**: http://100.85.134.23:8080
- **Location**: avalon-nuc (NUC server)
- **Access**: Via Tailscale network

---

## Related Skills

- **n8n-workflow-patterns** - Alternative workflow platform
- **n8n-mcp-tools-expert** - n8n MCP integration

---

## Summary

**Key Points**:
1. Scripts are the building blocks (TS/Python/Go/Bash)
2. Flows orchestrate multiple scripts
3. Apps provide UI for scripts/flows
4. Resources store credentials securely
5. Schedules automate execution

**Workflow**:
1. Create scripts for individual tasks
2. Combine scripts into flows
3. Build apps for user interaction
4. Schedule for automation
5. Monitor via dashboard
