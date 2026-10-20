---
name: devtools-pro
description: "CLI tools, VS Code extensions, SDKs, developer experience, API design. Use when building or improving developer tooling."
---

# DevTools Pro

## Purpose

Build developer tools that developers love: CLI tools, VS Code extensions, SDKs, API clients, and documentation. Developer experience is the product.

## When to Use

**Use this when:**
- Building a CLI tool, VS Code extension, language SDK, or API client library for other developers
- Designing developer-facing documentation, onboarding flows, or getting-started guides
- Reviewing an existing devtool for DX quality: help text, error messages, output formats, config file handling

**Use this ESPECIALLY when:**
- The tool will be distributed publicly (npm, Homebrew, VS Code Marketplace) and first-impressions DX is a differentiator
- You are designing a typed SDK that needs autocomplete, generated types from an OpenAPI spec, and retry/backoff logic
- The CLI or extension needs to handle auth token storage, multi-account configs, and credential refresh

**Don't skip when:**
- Error messages from the tool will be the primary debugging surface for end users — actionable, contextual errors are required
- The extension or CLI interacts with long-running operations and lacks progress indicators or cancellation support
- The SDK wraps a paid API and must expose rate-limit feedback so callers can implement backpressure

## Core Patterns

### 1. CLI Tool Structure (Go/Node)

```
cli/
  cmd/
    root.go         ← cobra/cli root command
    projects.go     ← `cli projects list`
    config.go       ← `cli config set`
    auth.go         ← `cli login`
  internal/
    api/
      client.go     ← HTTP client
    config/
      manager.go    ← Config file management
    output/
      table.go       ← Table formatter
      json.go
    auth/
      token.go
  main.go
```

### 2. CLI Command Pattern

```go
// cobra CLI example (Go)
var projectsCmd = &cobra.Command{
    Use:   "projects",
    Short: "Manage projects",
    RunE: func(cmd *cobra.Command, args []string) error {
        client := api.NewClient(config.GetToken())

        format, _ := cmd.Flags().GetString("format")
        projects, err := client.ListProjects()
        if err != nil {
            return fmt.Errorf("failed to list projects: %w", err)
        }

        switch format {
        case "json":
            return output.JSON(os.Stdout, projects)
        default:
            output.Table(os.Stdout, projects, []string{"ID", "Name", "Status"})
            return nil
        }
    },
}

func init() {
    projectsCmd.Flags().StringP("format", "f", "table", "Output format (table|json)")
    rootCmd.AddCommand(projectsCmd)
}
```

### 3. VS Code Extension

```typescript
// extension.ts
import * as vscode from 'vscode'

export function activate(context: vscode.ExtensionContext) {
  // Register command
  const disposable = vscode.commands.registerCommand('seniordev.createProject', async () => {
    const name = await vscode.window.showInputBox({
      prompt: 'Project name',
      placeHolder: 'my-awesome-project',
      validateInput: (value) => value.length > 0 ? null : 'Name is required',
    })
    if (!name) return

    // Show progress
    await vscode.window.withProgress({
      location: vscode.ProgressLocation.Notification,
      title: 'Creating project...',
    }, async (progress) => {
      progress.report({ message: 'Setting up...' })
      await api.createProject(name)
      vscode.window.showInformationMessage(`Project '${name}' created!`)
    })
  })

  context.subscriptions.push(disposable)
}
```

### 4. SDK Design

```typescript
// Client SDK for your API
export class SeniorDevClient {
  private client: HttpClient

  constructor(config: { apiKey: string; baseUrl?: string }) {
    this.client = new HttpClient({
      baseURL: config.baseUrl || 'https://api.seniordev.com/v1',
      headers: { Authorization: `Bearer ${config.apiKey}` },
      timeout: 10000,
    })
  }

  // Typed methods with autocomplete
  projects = {
    list: (params?: PaginationParams) =>
      this.client.get<PaginatedResponse<Project>>('/projects', { params }),
    get: (id: string) =>
      this.client.get<Project>(`/projects/${id}`),
    create: (data: CreateProjectInput) =>
      this.client.post<Project>('/projects', data),
    update: (id: string, data: Partial<Project>) =>
      this.client.patch<Project>(`/projects/${id}`, data),
    delete: (id: string) =>
      this.client.delete(`/projects/${id}`),
  }

  tasks = {
    list: (projectId: string) => this.client.get(`/projects/${projectId}/tasks`),
    create: (projectId: string, data: CreateTaskInput) => this.client.post(`/projects/${projectId}/tasks`, data),
  }
}
```

### Checklist

- [ ] CLI: help text, autocomplete, --version, --help
- [ ] CLI: JSON output flag, human-readable default
- [ ] CLI: progress indicators for long operations
- [ ] CLI: config file in standard location (~/.config/app/config.yaml)
- [ ] CLI: error messages are actionable
- [ ] SDK: typed, documented, autocompletable
- [ ] SDK: retry with backoff for transient errors
- [ ] SDK: rate limit handling
- [ ] Extension: activation events are specific (not *)
- [ ] Extension: status bar indicators for long operations
- [ ] Docs: getting started in < 5 minutes

## Related Skills

- **code-reviewer** — REST/GraphQL API design for the service your SDK or CLI wraps; ensures the surface your tool exposes is coherent
- **backend-senior-engineer** — server-side implementation of the API endpoints consumed by your SDK or CLI
- **frontend-senior-engineer** — web-based developer portals, interactive API explorers, and documentation sites that complement the CLI/SDK
- **test-engineer** — contract tests, integration tests against a sandbox API, and CLI golden-output tests
- **security-reviewer** — credential storage, token scoping, and supply-chain risks in CLI distribution (npm, Homebrew formulas)
- **observability-pro** — telemetry and error reporting within the SDK or CLI (opt-in usage analytics, crash reporting)
- **devops-release-engineer** — publishing pipelines for npm packages, GitHub Releases, VS Code Marketplace submissions, and Homebrew taps
- **performance-engineer** — SDK connection pooling, request batching, and CLI startup-time profiling

