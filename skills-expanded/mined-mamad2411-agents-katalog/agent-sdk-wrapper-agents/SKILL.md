# Agent notes

- Keep docs short: API usage, limits and commands. Never mention downstream
  projects or narrate development history.
- Python SDK imports belong in `packages/python/src/agent_sdk_wrapper/providers/`;
  TypeScript SDK imports belong in `packages/typescript/src/providers/`.
  Adapter tests may import SDK types.
- Keep final Docker images Ubuntu-based. Python gets runtimes from Python SDKs;
  do not install Node/npm or standalone CLIs there. TypeScript has its own image
  and build-context ignore file; exclude host node_modules and generated files.
  The gVisor Python example also includes Node/git to run its target Node project;
  its provider runtimes still come from Python SDKs.
- Keep `.env`, `.claude/`, `results/`, caches and generated artifacts out of git.
- Shared automation uses Bash or Node. Python tooling stays in `packages/python/`.
- Prefix language-specific Compose services with `python-` or `typescript-`;
  neither language is the default. Shared example services use neutral names.
- Keep dependencies minimal: Node's test runner, exact SDK pins and lockfiles,
  npm install scripts disabled. Verify registry metadata/advisories. Use a
  seven-day cooldown unless a newer release is explicitly requested.
- Provider/model resolution belongs in the wrapper; `codex` aliases `openai`.
  Reject unsupported combinations with `ConfigError`.
- `check_runtime()` / `checkRuntime()` validate requests before availability.
- Default tests stay offline. Python live tests use Compose. TypeScript live
  tests require `AGENT_SDK_WRAPPER_TS_RUN_INTEGRATION=1` and provider keys.
- Input token totals include cache; output totals include reasoning.
  Claude `usage` excludes subagents: prefer `model_usage` / `modelUsage`, using
  `usage` only when that map is absent/empty. Never add both; cost includes subagents.
- Every Python event union member needs a shared schema branch,
  `testing.event_from_dict` case and trace-viewer rendering. TypeScript uses a
  subset; keep its exhaustive schema checks and shared replay fixtures aligned.
- `RunStarted` includes prompt and system prompt. Preserve empty/redacted
  `Thinking` events when reasoning occurred; both providers reason by default.
- Classify terminal provider failures even when the SDK never raises:
  specific `error_type` and `retryable`, not a generic error.
- Signal-killed runtimes raise `ProcessTerminatedError`, never `TransientError`.
- Changes to Python `_tool_server_script()` or `mcp` require the real offline
  MCP handshake test. The generated server supports `FastMCP` and `MCPServer`.
- Fault tests use local mock endpoints: Claude `ANTHROPIC_BASE_URL` via `env`;
  Codex `model_providers.<id>.base_url`. Use 4xx for terminal paths; runtimes
  internally retry 429/5xx. Neither SDK provides fault injection.
