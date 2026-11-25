---
name: orbyn-mcp-builder
description: "Design, build and evaluate a Model Context Protocol (MCP) server in TypeScript or Python with Anthropic's bundled guide and evaluation harness. Use when creating or reworking an MCP server or its tools; for model-powered app behavior use orbyn-ai-application."
---

# MCP server builder

Follow the consuming project's instructions and requested scope; use the
[portable defaults](../orbyn-workflow/references/project-policy.md) only where guidance is missing.

Read [the bundled guide](references/upstream/anthropic-mcp-builder/SOURCE.md) in full,
then only the reference it points to for your language: the
[TypeScript](references/upstream/anthropic-mcp-builder/reference/node_mcp_server_v2.md)
or [Python](references/upstream/anthropic-mcp-builder/reference/python_mcp_server.md)
guide, the [best practices](references/upstream/anthropic-mcp-builder/reference/mcp_best_practices.md)
and the [evaluation guide](references/upstream/anthropic-mcp-builder/reference/evaluation.md).

## Where these rules override the source

1. **Use the project's stack.** An existing server keeps its language and SDK. For a
   new one, choose with [stack selection](../orbyn-stack-selection/SKILL.md) when the
   choice is open.
2. **Fetch docs with the host's own tool.** Where the source says "WebFetch", use
   whatever web or documentation tool the host has; offline, say which current fact
   is unverified.
3. **Design the tools as a contract.** Each tool's name, inputs, errors, authority and
   side effects follow [orbyn-backend-design](../orbyn-backend-design/SKILL.md) and the
   tool-design guidance in [orbyn-ai-application](../orbyn-ai-application/SKILL.md).
   A tool that writes, sends or deletes says so and needs the user's confirmation path.
4. **Secrets stay out of code.** Credentials come from the environment or the host's
   secret store, never from tool arguments or the repository.
5. **Evaluations cost money.** `scripts/evaluation.py` calls a model. Run it only
   with the user's OK, and report the model and the result.
6. **Installing is a change.** Ask before adding SDK packages to the project.

## Source and updates

Bundled from [anthropics/skills](https://github.com/anthropics/skills/tree/2c5958ecac7cee2b583967a2c4981d0f4a75c579/skills/mcp-builder)
at `2c5958e`, Apache-2.0, with its `LICENSE.txt` and a `snapshot.json` of file hashes.
Refresh it with [upstream review](../orbyn-upstream-review/SKILL.md).
