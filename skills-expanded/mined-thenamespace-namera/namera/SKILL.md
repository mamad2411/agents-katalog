---
name: namera
description: Build with Namera or use its accounts, session keys, transactions and signatures through the SDK, CLI or MCP.
---

# Namera

Namera gives agents access to accounts through scoped session keys. Use the SDK
for application code, the CLI for terminal work, or connected MCP tools for
account operations. Follow the user's choice when they specify an interface.

## Find the right guide

Read the relevant reference, then open the linked docs for working examples and
current parameters. Load only what the task needs.

- [SDK](references/sdk.md): authentication, accounts, session keys and signing.
- [CLI](references/cli.md): terminal setup, commands and automation.
- [MCP](references/mcp.md): client connection, authorization and tool access.
- [Transactions](references/transactions.md): transfers, simulation, gas and status.
- [Templates](references/templates.md): reusable permissions and custom builders.

The references link to Markdown exports. Use [llms.txt](https://namera.ai/llms.txt)
to find other pages or [llms-full.txt](https://namera.ai/llms-full.txt) when broader
context is needed.

## Before acting

Use the actual account, network and session key from configuration or authenticated
reads. Check its installed permissions; documentation IDs and recipients are examples.
Keep credentials in the documented environment-variable, browser or keyring flow.

If access is denied, explain the missing permission. Do not widen authority or
change a gas budget to make an operation succeed.
