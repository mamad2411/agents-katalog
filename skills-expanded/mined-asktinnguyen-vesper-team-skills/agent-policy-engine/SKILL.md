---
name: agent-policy-engine
description: "This skill should be used when implementing a persona-level hard-deny policy system for AI agent applications. It applies when building runtime tool-gating that blocks dangerous operations regardless of user permission settings — covering file I/O, shell commands, MCP servers/tools, API endpoints, and network requests. Use when the user asks to add security policies, permission layers, tool deny-lists, role-based presets, or agent sandboxing to their application."
---

# Agent Policy Engine

Implement a persona-level hard-deny policy system for AI agent applications. The engine loads JSON
permission configs, validates them with Zod, compiles into efficient runtime structures (RegExp/Set),
and checks every tool call before permission mode logic runs.

## When to Use

- Adding per-role tool restrictions to an AI agent application
- Building a deny-list layer that the agent cannot override at runtime
- Implementing preset security profiles (research, reviewer, engineer, admin)
- Gating file access, shell commands, MCP tools, API calls, or network requests
- Adding a policy editor UI with live validation and tool testing

## Architecture Overview

### Five-Level Config Hierarchy

The policy engine operates as the innermost enforcement layer of a cascading configuration
hierarchy. See `references/hierarchical-scoping.md` for the full scoping model.

```
Level 1: Global Defaults        (app config.json)
Level 2: Workspace Config       (project config.json + allow-list permissions.json)
Level 3: Persona Defaults       (role personas.json + deny-list permissions.json)
Level 4: Session Snapshot        (frozen at creation — permissionMode, providerId, personaId)
Level 5: Runtime Enforcement     (PreToolUse: deny-first → mode → allow-list)
```

Settings resolve using first-wins logic (explicit options beat persona, which beats workspace,
which beats global). Sessions snapshot their resolved config at creation time for isolation.

### Dual Permission System

Two distinct `permissions.json` files serve complementary purposes:

- **Workspace permissions** (allow-list, additive) — customizes what's auto-approved in Explore mode
- **Persona policy** (deny-list, subtractive) — blocks tools regardless of any mode or setting

These never conflict because they answer different questions. Allow-lists extend defaults;
deny-lists override everything. See `references/hierarchical-scoping.md` for details.

### Three-Layer Enforcement Model

```
Layer 1: Hard-Deny Policy   (immutable, checked first — this skill)
    ↓ if allowed
Layer 2: Permission Modes   (user-controlled: safe/ask/auto)
    ↓ if allowed
Layer 3: Tool Execution
```

The hard-deny layer runs **before** permission modes in the agent's `PreToolUse` hook. A denied
tool never reaches permission logic, making policies immutable at runtime.

### Permission Escalation Guard

When a persona requests `defaultPermissionMode: 'allow-all'`, it requires explicit opt-in via
`allowPermissionModeEscalation: true`. Without the flag, the persona cannot escalate permissions
and the safer workspace/global default applies instead.

### File Organization Pattern

```
packages/shared/src/agent/
├── persona-policy-types.ts    # Schema + presets + summary (browser-safe)
├── persona-policy.ts          # Loader + compiler + checker (Node-only)
└── path-matching.ts           # Shared glob/regex/command utilities

apps/{platform}/
├── resources/permissions/default.json  # Default allow-list for safe mode
└── src/main/personas-ipc.ts           # IPC for load/save/test policy
```

**Critical split:** Types and presets in a browser-safe module (Zod + pure data). Loader/compiler/checker
in a Node-only module (uses `fs`, `path`).

## Implementation Steps

### Step 1: Define the Policy Schema

Create the Zod schema with all-optional fields. Reference `references/schema.md` for the complete
schema specification and field documentation.

Key design decisions:
- All fields optional so `{}` is a valid policy that denies nothing
- Presets provide role-based defaults users can customize after applying
- `BashPattern` supports both plain string and `{ pattern, comment }` for documented rules
- Use `z.safeParse()` everywhere — never throw on invalid user input

### Step 2: Build Path Matching Utilities

Create shared utilities for glob-to-regex conversion and command extraction. These are used by both
the policy checker and permission mode logic.

Required functions:
- `expandHome(path)` — resolve `~` to home directory
- `globToRegex(pattern)` — convert `**`, `*`, `?` globs to anchored RegExp
- `getBaseCommand(command)` — extract base command, with special handling for compound commands like `git push`
- `matchesGlobPatterns(filePath, patterns)` — test path against glob array

See `references/path-matching.md` for implementation details and edge cases.

### Step 3: Implement the Compiler

The compiler converts validated JSON into optimized runtime structures. Compilation happens **once**
at session/persona load — never on every tool call.

```typescript
interface CompiledPolicy {
  deniedReadGlobs: RegExp[]              // Glob → RegExp, O(n) check
  deniedWriteGlobs: RegExp[]             // Glob → RegExp, O(n) check
  deniedBashBaseCommands: Set<string>    // O(1) lookup, lowercased
  deniedBashPatterns: Array<{ regex: RegExp; comment?: string }>
  deniedMcpServers: Set<string>          // O(1) server-level block
  deniedMcpTools: Set<string>            // O(1) tool-level block
  deniedApiPatterns: Array<{ method?: string; pathRegex: RegExp }>
  webFetchDenied: boolean                // Single boolean check
  rawConfig: PolicyConfig                // Preserved for serialization
}
```

**Error handling:** Skip invalid patterns silently during compilation. Never crash the agent over
a malformed regex. Log warnings but continue.

See `references/compiler.md` for the full compilation logic and API pattern format.

### Step 4: Implement the Checker

The `checkHardDeny()` function dispatches on tool name and returns a structured deny payload or null:

| Tool Category | Tools | Deny Source | Strategy |
|---|---|---|---|
| File reads | Read, Glob, Grep | `deniedReadGlobs` | RegExp on file_path |
| File writes | Write, Edit, MultiEdit | `deniedWriteGlobs` | RegExp on file_path |
| Bash | Bash | `deniedBashBaseCommands` + `deniedBashPatterns` | Set lookup then RegExp |
| MCP | `mcp__<server>__<tool>` | `deniedMcpServers` + `deniedMcpTools` | Set lookup (server first) |
| API | `api_<name>` | `deniedApiPatterns` | Method + path RegExp |
| WebFetch | WebFetch | `webFetchDenied` | Boolean |

Always return structured payloads (not just boolean) including tool name, reason, matched rule,
and policy file path — so the UI can tell users exactly what to edit.

See `references/checker.md` for the complete checker implementation and deny payload format.

### Step 5: Integrate with Agent PreToolUse Hook

Hook the checker into the agent SDK's tool execution pipeline:

```typescript
PreToolUse: [async (input) => {
  // 1. HARD-DENY — runs first, overrides everything
  if (this.personaPolicy) {
    const deny = checkHardDeny(input.tool_name, input.tool_input, this.personaPolicy)
    if (deny) return blockWithReason(formatDenyMessage(deny))
  }
  // 2. Permission mode logic runs only if policy allows
  // ...
}]
```

Critical: the policy check MUST run before permission mode logic. Add `setPersonaPolicy(policy)`
method to the agent class for runtime updates when persona switches.

### Step 6: Build IPC Handlers (Desktop/Electron)

Three IPC handlers for runtime policy management:

| Handler | Purpose | Returns |
|---------|---------|---------|
| `POLICY_GET` | Load existing policy for editing | `{ rawJson, parsed, summary }` |
| `POLICY_SAVE` | Validate + persist to disk | `{ success, summary, issues? }` |
| `POLICY_TEST` | Test tool against policy without executing | `{ allowed, message }` |

The test handler compiles the policy and runs `checkHardDeny()` internally — essential for
building user confidence in policy configuration.

### Step 7: Build the Policy Editor UI

Provide a settings modal with:
- JSON textarea with real-time Zod validation error display
- Preset dropdown with role descriptions for quick-apply
- Policy tester: tool name + JSON input fields → shows if blocked/allowed
- Summary badge showing deny rule counts per category

See `references/ui-patterns.md` for component patterns and state management.

### Step 8: Add Role Presets

Define four escalating-access presets. See `references/presets.md` for the complete preset
definitions and the rationale behind each.

| Preset | Writes | Shell | Credentials | Destructive |
|--------|--------|-------|-------------|-------------|
| research | Blocked | Mutations blocked | Readable | All blocked |
| reviewer | Allowed | rm/sudo/git push blocked | Readable | rm -rf / blocked |
| engineer | Allowed | sudo blocked | Hidden (.env, .pem, .key) | rm -rf / blocked |
| admin | Allowed | Allowed | Allowed | Minimal |

### Step 9: Write Tests

Test every deny category independently. See `references/testing.md` for the test matrix covering:
- File path glob matching (read and write separately)
- Bash base command denial and regex pattern matching
- MCP server-level vs tool-level blocking precedence
- API pattern matching with and without HTTP method
- WebFetch boolean flag
- Load/save round-trip validation
- Preset enforcement
- Edge cases: empty policy, invalid regex in config, paths with `~`

### Step 10: Implement Hierarchical Scoping

Place the policy engine within a cascading config hierarchy. See `references/hierarchical-scoping.md`
for the complete pattern including:

- Five-level resolution: Global → Workspace → Persona → Session → Runtime
- First-wins resolution with null-coalescing chains
- Session snapshotting (freeze config at creation time for isolation)
- Dual permission system (additive allow-list + subtractive deny-list)
- Permission escalation guards for auto-approve mode

Key implementation points:
- Resolve all settings at session creation, store as snapshot in session record
- Never reference live config during session execution — only the snapshot
- Guard `allow-all` permission mode with explicit `allowPermissionModeEscalation` flag
- Make workspace permissions additive-only (can extend defaults, never restrict them)

## Design Principles

1. **Deny-list, not allow-list** — policies block specific operations; everything else passes to permission modes
2. **Immutable at runtime** — agent cannot modify its own policy during execution
3. **Fail-open on compilation errors** — skip invalid patterns, never crash the agent
4. **Structured deny payloads** — include tool name, reason, matched rule, policy path for debugging
5. **Browser/Node split** — types and presets browser-safe, Node APIs only in loader/compiler
6. **Compile-once, check-many** — O(n) compilation at start, efficient checks per tool call
7. **Two-tier bash matching** — fast Set lookup for base commands, then regex for full command patterns
8. **Session-level snapshotting** — freeze resolved config at session creation for isolation across restarts
9. **Dual permission files** — allow-lists (workspace) and deny-lists (persona) are complementary, never conflicting
10. **Escalation guards** — auto-approve mode requires explicit opt-in flag to prevent misconfigured persona bypasses

## Common Pitfalls

- **Don't check policy on every compilation** — compile once at session start, store the result
- **Don't use allow-lists for the policy layer** — deny-lists compose better across presets and custom rules
- **Don't let the agent modify its own policy** — policy files must be edited by the user, not the agent
- **Don't throw on invalid regex** — wrap in try/catch, skip silently, log warning
- **Don't forget the `formatDenyMessage()`** — users need to know which file to edit to unblock themselves
- **Don't mix policy types** — persona policies (hard-deny) are distinct from workspace permissions (explore mode allow-list)
