# Claude Agent Harness Module

Adapter module that registers the `claude-agent-sdk` harness with the core
agent-harness registry. This module owns every Claude-Agent-SDK-specific piece
of runtime: the `executeWithAgentSDK` primitive (`executor.ts`), the owner-
questions MCP bridge (`kota-tools-mcp.ts`), the claude-shaped query/option
declarations (`sdk-types.ts` — `SDKQueryOptions`, `SDKSystemPrompt`,
`SDKThinkingConfig`, `SDKQueryParams`, `SDKQueryFn`, `SDKModule`), the
adapter-private permission/setting literal types
(`ClaudeAgentSdkPermissionMode`, `ClaudeAgentSdkSettingSource`,
`ClaudeAgentSdkStepOverrides` in `executor.ts`), and the adapter that
translates the KOTA-native `AgentHarnessRunOptions` (autonomy mode, tools,
prompt, owner-questions) into SDK wire shape. This module owns the
`KotaTool` ↔ claude-agent-sdk tool-definition translation at the
native-loop seam (see `src/core/agent-harness/AGENTS.md`). The harness-
neutral wire-frame declarations (`KotaAgentMessage`,
`AgentDecisionAttribution`, `AgentCanUseTool`) live in
`src/core/agent-harness/` because the workflow runtime consumes them
directly; nothing in core imports `@anthropic-ai/claude-agent-sdk`.

- Importing the module is side-effect free. The module declares its adapter
  through `KotaModule.agentHarnesses`; `ModuleLoader` registers it during load
  and withdraws that exact registration during unload. Module-lifecycle tests
  load it through the host; isolated harness-consumer fixtures may explicitly
  register the adapter they exercise, but must never rely on an import side
  effect.
- Guardrails (tool allow/deny lists, MCP servers, composed `canUseTool`) are
  passed in through `AgentHarnessRunOptions` and applied by the underlying
  SDK call. The harness-neutral commit + daemon guards live in
  `src/core/agent-harness/guards.ts`; callers compose those and hand the
  result to `runAgentHarness` through the neutral `canUseTool` field.
- Scope policy is enforced at the harness boundary through the SDK's
  `canUseTool` callback. `scope-policy-guard.ts` binds Claude built-in tool
  names to KOTA effects and owning modules, denies unknown tools, applies
  write/module/external-effect decisions plus the current autonomy cap, and
  queues confirmation outcomes. Each callback reads the workflow's current
  revisioned authority before deciding. Keep that binding aligned when Claude
  adds a built-in tool; an unbound tool must remain fail-closed. Bash uses the
  same compound local/network invocation classifier as KOTA execution tools.
- Named-agent write scope is a separate final `canUseTool` guard. It validates
  Claude's effective built-in tool input against the declared scope roots
  plus the isolated per-run output directory, after caller and scope-policy
  callbacks have run, so neither can widen the destination.
- Evidence-review read scope is also enforced through the pre-tool hook for
  read built-ins and sandboxed Bash because the SDK may auto-approve those
  without calling `canUseTool`. Opaque Bash remains a write-capable operation
  and is denied for review-only invocations.
- Claude command execution also runs in the SDK's fail-closed OS sandbox. The
  workspace stays writable while the machine-authority directory is denied;
  `canUseTool` text classification is defense in depth, not the authority
  boundary.
- Owner-questions surface is adapter-owned: when `askOwner` is present, the
  adapter merges `createOwnerQuestionMcpServers(source)` into the SDK's
  `mcpServers` map. Callers never inject that MCP server themselves.
- The claude-agent-sdk in-process `sdk` MCP variant (`createSdkMcpServer`,
  `{type: "sdk", name, instance}`) is adapter-private. The neutral
  protocol covers only the transport variants (`stdio | sse | http`);
  `executor.ts` exports `ClaudeAgentMcpServers` as the adapter-internal
  extended map that combines the neutral variants with the live in-process
  entry, and the adapter is the only place the two views meet. Neutral
  callers cannot pass in-process servers directly; route any future
  claude-specific in-process tool through this adapter's owner-questions-
  style internal wiring rather than re-adding an in-process field to the
  neutral shape.
- The adapter maps KOTA's neutral `autonomyMode` to the SDK's native
  permission knob: `autonomous` → guarded `default`, `passive` →
  `default`, `supervised` → throws (the SDK has no operator-approval-queue
  routing). Callers that omit `autonomyMode` get the `autonomous` default.
  Per-step overrides live on the workflow step's
  `harnessOptions["claude-agent-sdk"]` block (see
  `src/core/agent-harness/AGENTS.md`); the adapter's `validateStepOptions`
  is the only place the claude-specific permission/setting literals live.
  The validated fragment travels through `harnessOverrides` on the neutral
  run options as opaque `AgentHarnessStepOverrides`. Setting-source
  defaults to `["project"]` inside the adapter when the override is unset.
- Declared capabilities: `askOwnerToolName =
  "mcp__kota_owner_questions__ask_owner"`, `emitsAgentMessageStream = true`.
- The claude-SDK `PermissionResult` TS type marks `updatedInput` optional on
  the `allow` branch, but the SDK's runtime zod schema rejects responses
  without it. All permission callbacks route through
  `normalizePermissionResult` / `normalizeCanUseTool` (applied automatically
  by `buildQueryOptions`); do not pass a raw `canUseTool` to `sdkQuery`.
- Tests that need to mock `executeWithAgentSDK` mock
  `#modules/claude-agent-harness/executor.js` directly — the harness-neutral
  seam (`#core/agent-harness/runner.js`) stays visible in test code, so
  non-claude adapters are not silently routed through a claude-shaped mock.

Native conversations mirror through the SDK SessionStore port with eager flush
into core-assigned protected storage. Identity is captured from SDK initialization
and successful mirror writes, before a final result. Resume uses the exact native
id with a fresh query contract; older native histories may be imported through
the SDK reader. A pre-tool hook protects transcript paths even for auto-approved
built-ins, and the shell sandbox denies native transcripts and the complete
canonical and workspace conversation stores, including sibling owners and retired
generations. Mirror failure fails visibly and retains the provider-native transcript.
