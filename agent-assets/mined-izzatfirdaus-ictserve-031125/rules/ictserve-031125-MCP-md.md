---
applyTo:
  - '**'
description: |
  MCP (Model Context Protocol) integration standards for ICTServe project.
  Laravel Boost, Memory MCP server, and other MCP server configurations and workflows.
tags:
  - mcp
  - laravel-boost
  - ai-agents
  - context-protocol
  - automation
version: '1.1.0'
lastUpdated: '2025-11-30'
---

# MCP Integration — ICTServe AI Agent Standards

## Overview

This rule defines Model Context Protocol (MCP) integration patterns for ICTServe. It covers the configuration and usage of the Laravel Boost MCP server, Memory MCP server, and other tools to enhance AI agent workflows and context management.

| Attribute | Value |
| :--- | :--- |
| **Framework** | MCP Protocol v2024-11-05 (Stable) |
| **Applies To** | All development workflows, AI agent interactions |
| **Traceability** | D13 (UI/UX Frontend Framework), Development Automation |

## Core Principles

1. **Context-Aware Development**: Use MCP tools to understand project state.
2. **Version-Specific Documentation**: Query exact package versions via `search-docs`.
3. **Automated Workflows**: Leverage MCP servers for repetitive tasks.
4. **Memory Persistence**: Use MCP Memory server for session continuity.
5. **Tool Integration**: Combine multiple MCP servers for comprehensive workflows.

## Available MCP Servers

The following servers are configured in `.amazonq/mcp.json` and enabled for the project.

### 1. Laravel Boost (Primary)
**Status**: ✅ Enabled
**Purpose**: Laravel-specific development tools and context.

**Key Tools**:

* `application-info`: Get package versions and models.
* `search-docs`: Version-specific Laravel ecosystem documentation.
* `database-query`: Read-only database operations.
* `tinker`: Execute PHP code in Laravel context.
* `list-artisan-commands`: Available Artisan commands.
* `get-config`: Application configuration values.

### 2. Memory Server
**Status**: ✅ Enabled
**Purpose**: Persistent knowledge graph storage for agent memory.

**Key Tools**:

* `create_entities`: Store project knowledge.
* `search_nodes`: Find relevant information.
* `add_observations`: Update existing knowledge.
* `read_graph`: Full knowledge graph access.
* `open_nodes`: Retrieve detailed entity context.

### 3. Sequential Thinking
**Status**: ✅ Enabled
**Purpose**: Complex problem-solving workflows and reasoning chains.

**Key Tools**:

* `sequentialthinking`: Multi-step reasoning process.

### 4. Browser Automation (Chrome DevTools & Playwright)
**Status**: ✅ Enabled
**Purpose**: Browser automation, testing, and snapshotting.

**Key Tools**:

* `Maps_page` / `browser_navigate`: Browser navigation.
* `take_snapshot` / `browser_snapshot`: Page screenshots/DOM snapshots.
* `click` / `browser_click`: Element interaction.

### 5. Context7 & DeepL
**Status**: ✅ Enabled
**Purpose**: Library documentation resolving and translation services.

**Key Tools**:

* `resolve-library-id` (Context7): Find documentation IDs.
* `translate-text` (DeepL): Translate content (MS/EN).

## Development Workflow Patterns

### 1. Project Discovery Workflow

```typescript
// Start every session with project context
1. application-info()  // Get current package versions
2. search-docs(['laravel', 'livewire', 'filament'])  // Get framework docs
3. database-schema()   // Understand data structure
4. list-routes()       // Available application routes
````

### 2\. Feature Development Workflow

```typescript
// Before implementing new features
1. search-docs(['feature-topic'])  // Get relevant documentation
2. database-query('SELECT * FROM related_table LIMIT 5')  // Understand data
3. tinker('Model::factory()->make()->toArray()')  // Test model structure
4. list-artisan-commands()  // Find relevant Artisan commands
```

### 3\. Debugging Workflow

```typescript
// When encountering issues
1. last-error()        // Get latest application error
2. read-log-entries(50)  // Recent log entries
3. get-config('app.debug')  // Check debug settings
4. tinker('DB::connection()->getDatabaseName()')  // Test connections
```

### 4\. Testing Workflow

```typescript
// For E2E testing
1. browser_navigate('http://localhost:8000')
2. browser_snapshot()  // Capture current state
3. browser_click('button[type="submit"]')
4. browser_snapshot()  // Capture result
```

## Best Practices

### Tool Usage Guidelines

1. **Always start with `application-info`** to get current context.
2. **Use `search-docs` before implementation** to ensure version compatibility.
3. **Prefer `database-query` over direct SQL** for read operations.
4. **Use `tinker` for testing code snippets** before implementation.
5. **Store discoveries in Memory server** for future sessions.

### Error Handling

```typescript
// When MCP tools fail
1. Check tool availability: list available servers
2. Verify configuration: check .amazonq/mcp.json
3. Fallback to manual methods if tools unavailable
4. Document issues in Memory server for tracking
```

### Performance Optimization

1. **Batch related queries** to minimize tool calls.
2. **Cache results in Memory server** for repeated access.
3. **Use specific queries** rather than broad searches.
4. **Combine tools efficiently** in single workflows.

## Configuration Management

### MCP Server Configuration (`.amazonq/mcp.json`)

Ensure API keys are referenced from environment variables, not hardcoded.

```json
{
  "mcpServers": {
    "laravel-boost": {
      "command": "php",
      "args": ["artisan", "boost:mcp"],
      "env": {
        "APP_ENV": "${APP_ENV}",
        "MCP_CONNECTION_MODE": "persistent"
      },
      "disabled": false
    },
    "memory": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-memory",
        "c:\\xampp\\htdocs\\ictserve-031125\\storage\\mcp\\memory.jsonl"
      ],
      "disabled": false
    },
    "deepl": {
      "command": "npx",
      "args": ["-y", "deepl-mcp-server"],
      "env": {
        "DEEPL_API_KEY": "${DEEPL_API_KEY}"
      },
      "disabled": false
    }
  }
}
```

### Environment Variables

Required keys in `.env`:

```env
# MCP & API Keys
APP_ENV=local
CONTEXT7_API_KEY=ctx7sk-...
DEEPL_API_KEY=...
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_BEDROCK_REGION=us-east-1
```

## Integration Examples

### Laravel Feature Development

```typescript
// Example: Adding new Livewire component
async function createLivewireComponent() {
  // 1. Get current Livewire version
  const appInfo = await applicationInfo();
  const livewireVersion = appInfo.packages.find(p => p.roster_name === 'LIVEWIRE').version;
  
  // 2. Get Livewire 3 documentation
  const docs = await searchDocs(['livewire component', 'volt']);
  
  // 3. Check existing components
  const routes = await listRoutes();
  
  // 4. Create component using Artisan
  const commands = await listArtisanCommands();
  // Use: php artisan make:volt component-name
  
  // 5. Store pattern in memory
  await createEntities([{
    name: 'Livewire_Component_Pattern',
    entityType: 'coding_pattern',
    observations: [
      `Livewire ${livewireVersion} component created`,
      'Used Volt single-file component pattern',
      'Followed ICTServe naming conventions'
    ]
  }]);
}
```

### Database Operations

```typescript
// Example: Analyzing database performance
async function analyzeDatabasePerformance() {
  // 1. Get database schema
  const schema = await databaseSchema();
  
  // 2. Check slow queries
  const slowQueries = await databaseQuery(`
    SELECT * FROM information_schema.processlist 
    WHERE time > 5 AND command != 'Sleep'
  `);
  
  // 3. Get application config
  const dbConfig = await getConfig('database.connections.mysql');
  
  // 4. Store findings
  await addObservations([{
    entityName: 'Database_Performance_Analysis',
    contents: [
      `Found ${slowQueries.length} slow queries`,
      `Database: ${dbConfig.database}`,
      `Analysis date: ${new Date().toISOString()}`
    ]
  }]);
}
```

## Troubleshooting

### Common Issues

1. **MCP Server Not Found**:

      * Check `.amazonq/mcp.json` configuration.
      * Verify server installation: `php artisan boost:mcp --test`.
      * Ensure environment variables are set in `.env`.

2. **Tool Permission Denied**:

      * Check `autoApprove` settings in MCP config.
      * Verify tool is listed in approved tools.

3. **Memory Server Issues**:

      * Check memory file path: `storage/mcp/memory.jsonl`.
      * Ensure directory exists and is writable.
      * Verify JSON format is valid.

### Diagnostic Commands

```bash
# Test Laravel Boost MCP
php artisan boost:mcp --test

# Check MCP configuration
cat .amazonq/mcp.json | jq '.mcpServers'

# Verify memory file
ls -la storage/mcp/memory.jsonl
```

## Compliance Checklist

When using MCP integration, ensure:

* [ ] Start sessions with `application-info` for context.
* [ ] Use `search-docs` for version-specific documentation.
* [ ] Store discoveries in Memory server for persistence.
* [ ] Combine tools efficiently in workflows.
* [ ] Handle tool failures gracefully with fallbacks.
* [ ] Document patterns and solutions in Memory.
* [ ] Test MCP server connectivity regularly.
* [ ] Keep MCP configuration up to date.
* [ ] Use appropriate tools for each task type.
* [ ] Follow security best practices for tool usage.

| Field | Value |
| :--- | :--- |
| **Status** | Active for ICTServe MCP integration |
| **Version** | 1.1.0 |
| **Last Updated** | 2025-11-30 |
