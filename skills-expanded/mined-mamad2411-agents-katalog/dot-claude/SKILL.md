---
name: dot-claude
description: 'Configure and manage Claude Code (.claude) workspace settings, permissions, and tool hooks.'
license: MIT
---

# dot-claude

<!-- markdownlint-disable MD013 MD023 MD031 MD032 -->

## WHEN TO USE

- Configuring allowed tools and bash permissions for Claude Code.
- Defining PreToolUse or PostToolUse hooks for specific commands or file edits.
- Setting up environment variables, enabling LSP plugins, or managing marketplaces for Claude Code.
- Analyzing or updating the `.claude/settings.json` workspace configuration.

## WHEN NOT TO USE

- When working with the Anthropic Claude API or Claude documentation.
- When configuring generic coding standard rules instead of Claude-specific behavior.

## Core Process

1. **Locate or Create Configuration**: Ensure the `.claude` directory exists at the root of the project.
2. **Define Permissions**: Use `.claude/settings.json` to explicitly allow specific Bash commands to prevent Claude Code from blocking them.
3. **Configure Hooks**: Set up `PreToolUse` or `PostToolUse` hooks in `settings.json` to enforce safety checks, trigger auto-formatting, or log activity.
4. **Manage Plugins & Marketplaces**: Enable required tools like language servers (`pyright-lsp`), specify environment variables, or add external marketplaces using `/plugin marketplace add <url>`.

## Plugin Marketplaces

Claude Code supports extending its functionality via plugins from external marketplaces.

- **Add a Marketplace**: Use the CLI command to register a new plugin source.
  ```bash
  /plugin marketplace add https://example.com/path/to/marketplace.json
  ```
  > **Security Note**: The URL above is an example placeholder. Only add marketplaces you trust, as enabling external plugins executes third-party code.

- **Project-Level Configuration**: Add marketplaces to `.claude/settings.json` to share them with the team.
  ```json
  {
    "extraKnownMarketplaces": {
      "example-marketplace": {
        "source": {
          "source": "url",
          "url": "https://example.com/path/to/marketplace.json"
        }
      }
    },
    "enabledPlugins": {
      "example-plugin@example-marketplace": true
    }
  }
  ```

- **Official Documentation**: Refer to [Claude Code Plugin Marketplaces](https://code.claude.com/docs/en/plugin-marketplaces.md) for more details.

### plugin.json Minimal Format

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "Clear, concise description of what this plugin does"
}
```

Only `name` is required. Version and description are highly recommended.

## Best Practices

- **Explicit Permissions**: Instead of granting broad permissions, use precise glob patterns (e.g., `Bash(uv tool *)`).
- **Hook Activity Logging**: Redirect output from hooks into a specific log file like `.claude/hook-activity.log` to trace tool side effects.
- **Fail-Safe Hooks**: Ensure `PreToolUse` hooks return appropriate exit codes (e.g., `exit 2`) to block destructive commands.

## Common Pitfalls

- **JSON Syntax Errors**: `settings.json` must be strictly valid JSON, without trailing commas or comments.
- **Overly Broad Matchers**: Be precise with `matcher` regex in hooks to avoid triggering scripts unnecessarily (e.g., `Edit|Write` vs just `Bash`).

## References

- [Example settings.json](references/vojay-dev/settings.json)
