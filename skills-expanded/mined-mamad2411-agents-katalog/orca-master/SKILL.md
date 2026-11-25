---
name: orca-master-skill
description: Master skill that unlocks the full potential of all Orca skills, plugins, and MCP tools working together.
---

# Orca Master Skill

This is the master orchestration skill that unlocks the full power of Orca.

## How to Use This Skill

When a task is received, analyze it and automatically invoke the most relevant skills from the full arsenal below. Multiple skills can be combined for complex tasks.

## Full Skill Arsenal

### Built-in MCP Skills (8)
| Skill | Capability |
|-------|-----------|
| `computer-use` | System-level automation: mouse, keyboard, screen capture |
| `linear-tickets` | Create and manage Linear tickets from chat |
| `orca-cli` | Execute Orca CLI commands and workflows |
| `orca-emulator` | Manage iOS/Android emulators from chat |
| `orca-emulator-android` | Android-specific emulator lifecycle management |
| `orca-linear` | Advanced Linear project management |
| `orca-per-workspace-env` | Isolate environment per workspace |
| `orchestration` | Multi-agent task coordination and delegation |

### Workflow Skills (2)
| Skill | Capability |
|-------|-----------|
| `change-handoff` | Prepare precise handoff for unfinished work |
| `repository-review` | Review repo changes for correctness & security |

### Development Skills (15)
| Skill | Capability |
|-------|-----------|
| `python_coding` | Python development, debugging, best practices |
| `javascript_coding` | JavaScript/TypeScript development |
| `fullstack-development` | End-to-end web app development |
| `code-architecture` | Software architecture & system design |
| `api-design` | REST, GraphQL, gRPC, WebSocket API design |
| `testing-strategy` | Comprehensive testing (unit, integration, E2E) |
| `code-review` | Multi-dimensional code review |
| `debugging-master` | Systematic debugging & root cause analysis |
| `git-workflow` | Advanced Git operations & branching |
| `performance-optimization` | Profiling and optimization across the stack |
| `security-audit` | Security auditing for code, deps, infra |
| `devops-automation` | CI/CD, containers, IaC, observability |
| `cloud-native` | Cloud-native patterns, serverless, service mesh |
| `data-science` | ML lifecycle: data exploration to production |
| `mcp-integration` | MCP tool discovery and orchestration |

### Auxiliary Skills (4)
| Skill | Capability |
|-------|-----------|
| `documentation` | API documentation, Swagger/OpenAPI |
| `humanizer` | Natural language response shaping |
| `token-optimization` | Token efficiency for long conversations |
| `troubleshooting` | General troubleshooting framework |
| `system-prompt-engineering` | Advanced prompt engineering |

### Installed Plugins (8)
| Plugin | Type |
|--------|------|
| `orca-navigation-shortcuts` | Keybindings for Orca views |
| `orca-multipass-recipes` | Multipass VM recipes |
| `orca-portuguese` | Brazilian Portuguese localization |
| `orca-workflow-skills` | Planning, review, handoff skills |
| `orca-midnight-theme` | Dark theme for coding |
| `orca-nord-theme` | Nord color scheme |
| `orca-minimal-icons` | Monochrome file icons |
| `orca-solarized-terminal` | Solarized terminal colors |

## Task Routing Matrix

When a task arrives, route to the most relevant skills:

| Task Keywords | Primary Skills | Supporting Skills |
|--------------|---------------|-------------------|
| Build/create/develop app | `fullstack-development` | `api-design`, `code-architecture`, `testing-strategy` |
| Debug/fix error | `debugging-master` | `troubleshooting`, `performance-optimization` |
| Review code/PR | `code-review`, `repository-review` | `security-audit`, `testing-strategy` |
| Deploy/CI/CD | `devops-automation` | `cloud-native`, `performance-optimization` |
| Security/audit | `security-audit` | `code-review`, `debugging-master` |
| Architecture/design | `code-architecture` | `api-design`, `cloud-native` |
| ML/data | `data-science` | `python_coding`, `performance-optimization` |
| Git/repo | `git-workflow` | `change-handoff`, `code-review` |
| Performance/slow | `performance-optimization` | `debugging-master`, `token-optimization` |
| Test/coverage | `testing-strategy` | `code-review`, `debugging-master` |
| Orca/internal | `orca-cli`, `mcp-integration` | `orchestration`, `orca-per-workspace-env` |
| Emulator/device | `orca-emulator`, `orca-emulator-android` | `debugging-master` |
| Project management | `orca-linear`, `linear-tickets` | `change-handoff` |
| Documentation | `documentation` | `api-design`, `system-prompt-engineering` |

## Multi-Skill Orchestration Pattern

For complex tasks, combine skills in sequence:

```
1. ANALYZE → Break down the task into sub-tasks
2. ROUTE → Map each sub-task to the appropriate skill
3. EXECUTE → Run skills in dependency order
4. VALIDATE → Use code-review + testing-strategy to verify
5. HANDOFF → Use change-handoff if work is incomplete
```

## Unlocking Full Potential

To get the absolute most out of this skill set:

1. **Chain skills**: Use `code-architecture` → `fullstack-development` → `testing-strategy` → `code-review` → `devops-automation` for a complete build cycle
2. **Parallel agents**: Use `orchestration` to run multiple skills concurrently on different aspects of a task
3. **Context injection**: Use `system-prompt-engineering` to craft optimal prompts for each sub-task
4. **Memory anchoring**: Use `token-optimization` to maintain context across long sessions
5. **Tool augmentation**: Use `mcp-integration` to discover and call external tools dynamically
6. **Iterative refinement**: Use `debugging-master` + `performance-optimization` in a loop for continuous improvement
