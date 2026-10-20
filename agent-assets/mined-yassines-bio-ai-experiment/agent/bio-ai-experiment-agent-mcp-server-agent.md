# MCP Server Development Agent — DEPRECATED / DESCOPED

> **This role is deprecated and should not be dispatched.**
>
> MCP (Model Context Protocol) servers are **not being built** for this project,
> and none are planned. The owner decided not to pursue an MCP interface.
>
> The project's interface direction is instead **robust, drop-in POSIX CLIs**
> that are retro-compatible with the upstream tools (getopt-style flag bundling,
> POSIX short + GNU long options, `--`/`-` handling, clean exit codes). This work
> is largely complete via `cliflag.Parse` and per-tool flag retro-compatibility.
>
> See [`../../mcp-servers/README.md`](../../mcp-servers/README.md),
> [`../../docs/CLI_CONVENTIONS.md`](../../docs/CLI_CONVENTIONS.md), and
> [`../../PROJECT_STATUS.md`](../../PROJECT_STATUS.md). Do not start MCP work.

---

## Historical purpose (retained for context only)

This agent was originally responsible for creating MCP servers that wrapped the
Go tools so they could be driven by Large Language Models — designing server
architecture, exposing tool functionality over the MCP protocol, handling
serialization and streaming, and documenting/testing the integration.

That scope has been dropped. The bioinformatics tools are accessed directly as
command-line programs, which any agent or human can invoke without an additional
protocol layer.
