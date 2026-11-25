---
name: mukhon-plugin-manager
description: Comprehensive management, packaging, registration, and lifecycle standard for Antigravity and agent plugins. Covers creating plugin bundles (skills, agents, rules, MCP servers, hooks), validating plugin.json manifests, enabling/disabling plugins, and structuring sovereign distribution packages. Use when authoring, modifying, or auditing plugin bundles.
license: MIT
---

# MUKHON Plugin Manager

Architectural standard and operational lifecycle guide for managing, packaging, and registering plugins across the Antigravity ecosystem.

## When to Use This Skill

- Authoring a new plugin bundle containing skills, rules, agents, hooks, and MCP servers.
- Structuring and validating `plugin.json` manifests.
- Enabling, disabling, or managing installed plugins via standard platform tools.
- Preparing plugin packages for sovereign open-source release with standard MIT licensing.

---

## 1. Plugin Anatomy & Directory Structure

A plugin is a namespaced bundle that installs, enables, and disables as an atomic unit:

```
my-plugin/
├── plugin.json               # Required: Manifest declaring metadata & components
├── SKILL.md                  # Optional: Top-level entrypoint skill
├── skills/                   # Modular skills bundled in this plugin
│   └── my-skill/
│       └── SKILL.md
├── agents/                   # Subagents bundled in this plugin
│   └── code-auditor.toml
├── rules/                    # Context rules injected into agent sessions
│   └── AGENTS.md
├── mcp_config.json           # Model Context Protocol server registrations
├── hooks.json                # Event hooks (pre-tool, post-tool, startup)
└── assets/
    └── logo.svg              # 128x128 transparent vector logo
```

---

## 2. Manifest Standard (`plugin.json`)

The `plugin.json` file defines the plugin identity and declares its bundled components:

```json
{
  "name": "mukhon-dev-tools",
  "displayName": "MUKHON Developer Tools",
  "version": "1.0.0",
  "description": "Sovereign developer utilities, automated testing workflows, and UI tokens for MUKHON.",
  "author": "MUKHON Platform Authors",
  "license": "MIT",
  "logo": "assets/logo.svg",
  "suggestedPrompts": [
    "Run full-stack verification test suite",
    "Audit active skills with SkillSpector",
    "Inspect PostgreSQL connection pool health"
  ]
}
```

### Key Field Invariants

| Field | Type | Requirement | Guidelines |
| :--- | :--- | :--- | :--- |
| `name` | `string` | **Mandatory** | Lowercase kebab-case unique identifier (`mukhon-*`). |
| `displayName` | `string` | Optional | Human-readable title displayed in UI headers and menus. |
| `version` | `string` | Recommended | Semantic versioning (`X.Y.Z`). |
| `description` | `string` | **Mandatory** | 1–2 sentences explaining what the bundle provides. |
| `license` | `string` | **Mandatory** | `MIT` standard. |
| `logo` | `string` | Optional | Relative path to SVG or PNG square asset ($\ge 128 \times 128$). |
| `suggestedPrompts` | `string[]` | Optional | Exactly 3 action-oriented starter prompts for UI card rendering. |

---

## 3. Bundling Customizations

### A. Skills (`skills/`)
Place any reusable domain knowledge or workflow instructions inside `skills/<skill-name>/SKILL.md`. Ensure all commands use pinned packages (e.g. `@scope/pkg@1.2.3`).

### B. Rules (`rules/AGENTS.md`)
Rules are permanently loaded into the agent context whenever the plugin is enabled. Use rules strictly for non-negotiable architectural invariants (e.g. database safety, no auto-commit policies).

### C. Model Context Protocol (`mcp_config.json`)
Register tool servers that the plugin exposes:

```json
{
  "mcpServers": {
    "mukhon-inspector": {
      "command": "node",
      "args": ["dist/mcp-server.js"],
      "env": {}
    }
  }
}
```

---

## 4. Lifecycle & Safety Invariants

1. **Atomic Enable / Disable**: Turning off a plugin disables all of its skills, agents, rules, and MCP servers simultaneously without leaving orphaned processes.
2. **Namespace Collision Prevention**: Always prefix MCP servers and skills with the plugin name to prevent collisions with user-level tools.
3. **Zero Raw Credential Baking**: Never commit `.env` files or hardcoded API keys inside a plugin directory. Read all secrets from environment variables.
4. **Security Vetting**: Every plugin package must be scanned with `skillspector scan <dir> --no-llm` and verify at **0 / 100 (SAFE)** before publishing.
