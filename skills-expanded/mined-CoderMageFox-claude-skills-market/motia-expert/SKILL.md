---
name: motia-expert
description: Comprehensive Motia backend framework expert. Use when building APIs, background jobs, workflows, AI agents, or event-driven applications with Motia. Covers TypeScript/Python steps, flows, plugins, and configuration.
---

# Motia Expert Skill

Complete guide for building event-driven backends with Motia.

---

## What is Motia?

Motia is a **modern backend framework** that unifies:
- **APIs**: HTTP endpoints with auto-generated docs
- **Background Jobs**: Async task processing
- **Workflows**: Event-driven multi-step flows
- **AI Agents**: LLM integrations with tools

**Key Features**:
- Code-first approach (TypeScript, JavaScript, Python)
- Built-in observability and state management
- Visual workbench for debugging
- Plugin ecosystem

---

## Quick Reference

### Core Concepts

| Concept | Description | File Pattern |
|---------|-------------|--------------|
| **Step** | Single unit of work | `*.step.ts` |
| **Flow** | Group of related steps | `flows: ['flow-name']` |
| **Event** | Message between steps | `emits: ['event.name']` |
| **Plugin** | Extend functionality | `plugins: [...]` |

### Step Types

| Type | Purpose | Trigger |
|------|---------|---------|
| `api` | HTTP endpoint | HTTP request |
| `event` | Event handler | Event emission |
| `cron` | Scheduled task | Cron schedule |
| `noop` | Utility step | Manual/testing |

---

## Detailed Guides

- **[steps.md](steps.md)** - Step development guide
- **[flows.md](flows.md)** - Flow and event patterns
- **[plugins.md](plugins.md)** - Plugin configuration
- **[config.md](config.md)** - Project configuration

---

## Project Structure

```
my-motia-project/
├── motia.config.ts      # Main configuration
├── package.json
├── steps/               # Step definitions
│   ├── api-step.step.ts
│   ├── event-handler.step.ts
│   └── cron-job.step.ts
├── src/                 # Shared code
│   ├── services/
│   └── lib/
└── .motia/              # Generated files
```

---

## Best Practices

### ✅ Do
- Use typed schemas (Zod/Pydantic)
- Emit events for async operations
- Use plugins for cross-cutting concerns
- Keep steps focused and small

### ❌ Don't
- Put business logic in config
- Skip error handling
- Create circular event dependencies
- Hardcode configuration values
