---
name: antigravity-hooks
description: Guide and best practices for creating, configuring, and testing Google Antigravity Hooks. Use this skill when asked to define, create, inspect, debug, or write hooks.json configurations and hook script files.
---

# Google Antigravity Hooks Guide

Google Antigravity Hooks provide a high-performance, event-driven interception mechanism across the agent lifecycle. They enable developers to observe, validate, mutate, gate, or inject behaviors into agent turns, tool invocations, and termination sequences.

This guide details official hook configurations, named hook groups, event contracts, input/output schemas, supported tools catalog, the Unified Hook Engine architecture (`HookEngine`, `HookPipeline`, `BaseHook`), pure permission and session resolution, skill resolution, modern entrypoint runner scripts, zero-mock testing strategies, and a troubleshooting matrix.

---

## 1. Configuration & Scope

Hooks are configured via `hooks.json` files and evaluated across three distinct Antigravity product environments and hierarchical scopes:

### Environment Locations & Discovery

| Environment | Scope | Location | Notes / Controls |
|---|---|---|---|
| **Antigravity 2.0** | Workspace<br>Global | `<workspace>/.agents/hooks.json`<br>`~/.gemini/config/hooks.json` | View and toggle hooks from **Settings > Customizations > Hooks**.<br>`<app_data_dir>`: `~/.gemini/antigravity` |
| **Antigravity CLI** | Workspace<br>Global<br>Plugin | `<workspace>/.agents/hooks.json`<br>`~/.gemini/config/hooks.json`<br>`<plugin_root>/hooks.json` | Inspect all active hooks interactively in TUI with `/hooks`.<br>`<app_data_dir>`: `~/.gemini/antigravity-cli`<br>*(Official warning: Hooks in `settings.json` are not loaded)* |
| **Antigravity IDE** | Workspace<br>Global | `<workspace>/.agents/hooks.json`<br>`~/.gemini/config/hooks.json` | Manage active hooks from **… > Customizations > Hooks** in agent panel.<br>`<app_data_dir>`: `~/.gemini/antigravity-ide` |

> [!WARNING]
> **CLI Configuration Note**: Hooks in `settings.json` are not loaded. Hooks must be placed in `hooks.json` under `<workspace>/.agents/hooks.json`, `~/.gemini/config/hooks.json`, or `<plugin_root>/hooks.json`.

### Configuration Schemes

Antigravity supports two configuration structures in `hooks.json`:

#### A. Named Hook Groups (Workspace & Global Configuration)

Named hook groups organize hook handlers into logical, self-contained units (e.g., security gates, linters, observability monitors) that can be individually enabled, disabled, or shared:

```json
{
  "session-init": {
    "SessionStart": [
      {
        "type": "command",
        "command": "./scripts/session-init.sh",
        "timeout": 10
      }
    ]
  },
  "my-linter-hook": {
    "PostToolUse": [
      {
        "matcher": "run_command",
        "hooks": [
          {
            "type": "command",
            "command": "./scripts/lint.sh",
            "timeout": 10
          }
        ]
      }
    ]
  },
  "safety-gate": {
    "enabled": false,
    "PreToolUse": [
      {
        "matcher": "run_command",
        "hooks": [
          {
            "command": "./scripts/safety-check.sh"
          }
        ]
      }
    ]
  },
  "reminder": {
    "PreInvocation": [
      {
        "type": "command",
        "command": "./scripts/reminder.sh"
      }
    ]
  }
}
```

#### B. Plugin Root Hooks Format & Template Rendering

Top-level keys in `hooks.json` (and `hooks.template.json`) are **named hook groups**—for example, `"hooks"` below acts as the group name containing the lifecycle event entries (`SessionStart`, `PreInvocation`, etc.). Plugins can commit a portable `hooks.json` directly or bundle `hooks.template.json` with dynamic placeholders to render machine-specific bindings into `hooks.json` during setup:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "type": "command",
        "command": "{{PYTHON}} {{PLUGIN_DIR}}/scripts/session_start.py",
        "timeout": 5
      }
    ],
    "PreInvocation": [
      {
        "type": "command",
        "command": "{{PYTHON}} {{PLUGIN_DIR}}/scripts/pre_invocation.py",
        "timeout": 8
      }
    ],
    "PreToolUse": [
      {
        "matcher": "^(write_to_file|replace_file_content|multi_replace_file_content|write_file|edit_file|run_command)$",
        "hooks": [
          {
            "type": "command",
            "command": "{{PYTHON}} {{PLUGIN_DIR}}/scripts/pre_tool_use.py",
            "timeout": 5
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "^(invoke_subagent|write_to_file|replace_file_content|multi_replace_file_content|write_file|edit_file)$",
        "hooks": [
          {
            "type": "command",
            "command": "{{PYTHON}} {{PLUGIN_DIR}}/scripts/post_tool_use.py",
            "timeout": 5
          }
        ]
      }
    ],
    "Stop": [
      {
        "type": "command",
        "command": "{{PYTHON}} {{PLUGIN_DIR}}/scripts/stop.py",
        "timeout": 5
      }
    ]
  }
}
```

> [!IMPORTANT]
> **Cross-Platform Template Rendering (`hooks.template.json` -> `hooks.json`) vs. Portable Relative Commands**:
> 1. **POSIX Shell vs Windows Variables**: Hardcoding Windows `%USERPROFILE%` fails on Linux and macOS because POSIX shells (`/bin/sh`) do not expand `%USERPROFILE%`, causing `FileNotFoundError`.
> 2. **Python Binary Discrepancies**: On Linux and macOS, the system Python 3 runtime is typically named `python3`, whereas on Windows it is often `python`.
> 3. **Portable Relative Commands vs Explicit Paths**:
>    - Because Antigravity executes hook command processes with their working directory (`cwd`) set to the directory containing `hooks.json` (`<plugin_root>` for plugin hooks), portable relative commands such as `"uv run python ./scripts/pre_tool_use.py"` or `"node ./scripts/policy.mjs"` work out-of-the-box for `agy plugin install` across platforms without template pre-processing.
>    - For installations desiring explicit runtime/interpreter pinning or custom paths (e.g. `$ANTIGRAVITY_PLUGINS_DIR`), `hooks.template.json` supports rendering explicit `{{PYTHON}}` and `{{PLUGIN_DIR}}` bindings via:
>      ```bash
>      python scripts/setup_hooks.py [--python <path>] [--plugin-dir <path>]
>      ```
>    - A portable `hooks.json` (using relative commands such as `"uv run python ./scripts/..."`) is committed to version control for out-of-the-box `agy plugin install`, while `hooks.template.json` and `scripts/setup_hooks.py` remain available when machine-specific absolute paths need to be rendered.

#### C. Plugin Working Directory (`CWD`) & Injected Environment Variables

When executing hook handlers, Antigravity establishes clear boundaries between the hook process environment and the agent's workspace:
1. **Hook Process Working Directory (`CWD`)**: Antigravity executes hook command processes with their working directory (`cwd`) set to **the directory containing `hooks.json`** (`<plugin_root>` for plugin hooks), **NOT** the active workspace directory!
2. **Payload Reflection**: In contrast, the `cwd` field inside the `stdin` JSON payload always reflects the **agent's active workspace directory** (where the agent executes project commands by default).
3. **Injected Environment Variables (`PLUGIN_ROOT` & `PLUGIN_DATA`)**:
   - Command hooks bundled with a plugin automatically receive `PLUGIN_ROOT` and `PLUGIN_DATA` environment variables (the same paths provided to the plugin's MCP servers):
     - `PLUGIN_ROOT`: The absolute path of the read-only plugin root directory (`~/.gemini/config/plugins/<plugin-name>`).
     - `PLUGIN_DATA`: The absolute path of the persistent, writable data directory allocated for the plugin outside any project workspace.
   - Note: Variables are injected into the hook process environment (e.g., accessed in Python via `os.environ["PLUGIN_DATA"]` or in bash via `"$PLUGIN_DATA"`), rather than substituted directly into the `command` string.
4. **Implications for Plugin Authors**:
   - **Relative Script Paths**: Because hooks run inside `<plugin_root>`, commands can cleanly use relative paths directly (such as `"node ./scripts/policy.mjs"` or `"uv run python ./scripts/pre_tool_use.py"`).
   - **Workspace File Access**: When a hook needs to inspect, lint, or validate files in the user's project, it must resolve paths against `context.cwd` or entries in `context.workspace_paths` from the `stdin` payload, rather than relying on `os.getcwd()`.
   - **Self-Location in Python**: Python scripts can locate bundled assets relative to `Path(__file__).resolve().parent.parent` or `os.environ.get("PLUGIN_ROOT", Path(__file__).resolve().parent.parent)`.

### Handler Properties & Defaults

Within any hook definition list:
- **`type`**: Execution handler type. Currently only `"command"` is supported. Defaults to `"command"`.
- **`command`**: Command line string executed as a child process. Hook inputs are passed via standard input (`stdin`), and hook responses are captured from standard output (`stdout`).
- **`timeout`**: Maximum execution time in seconds. Defaults to `30` seconds if not specified.
- **`enabled`**: Boolean flag indicating if the hook or group is active. Defaults to `true`.

### Matcher Rules (`PreToolUse` & `PostToolUse`)

For `PreToolUse` and `PostToolUse`, the `matcher` property specifies which tool calls trigger the hook using Regular Expressions matching against the Tool Name:

- **Wildcard Matcher (`""` or `"*"` or `".*"`):** Matches all tools.
- **Exact Tool Matcher (`"run_command"`):** Matches exactly `run_command`.
- **Alternation / Exact Group (`"run_command|read_file"` or `"^(write_to_file|replace_file_content|multi_replace_file_content|write_file|edit_file|run_command)$"`):** Matches either designated tool. Matchers should cover both current runtime tool names (`read_file`, `write_file`, `edit_file`) and legacy aliases (`view_file`, `write_to_file`, `replace_file_content`, `multi_replace_file_content`).
- **Prefix Matching (`"browser_.*"`):** Matches all tools starting with a prefix (e.g. `browser_click`, `browser_navigate`).

> [!NOTE]
> For `SessionStart`, `PreInvocation`, `PostInvocation`, and `Stop`, the structure is simpler (a list of handlers directly under the event key) and the `matcher` is ignored.

---

## 2. Lifecycle Events & Input/Output Contracts

Every hook handler communicates with Antigravity via JSON over standard I/O:
- **Input (`stdin`)**: Clean JSON payload containing execution context and event details.
- **Output (`stdout`)**: Structured JSON contract returned by the handler. Diagnostic logs and debugging messages MUST be sent to standard error (`stderr`).

### Common Input Fields (Standard on all events)

All lifecycle events provide the following base context fields on `stdin` (keys use camelCase):

| Field | Type | Description |
|---|---|---|
| `conversationId` | `string` | Unique UUID identifying the active agent conversation session. |
| `hookEventName` | `string` | The lifecycle event currently executing, exactly as written in `hooks.json` (e.g. `"SessionStart"`, `"PreInvocation"`, `"PreToolUse"`, `"PostToolUse"`, `"Stop"`). |
| `workspacePaths` | `string[]` | Array of absolute paths to currently opened workspace folders. |
| `cwd` | `string` | The agent's active working directory where commands run by default (note: this is **not** the hook process's CWD, which is the directory containing `hooks.json`). |
| `transcriptPath` | `string` | Absolute path to persistent `transcript.jsonl` conversation logs: `<app_data_dir>/brain/<conversationId>/.system_generated/logs/transcript.jsonl`. |
| `artifactDirectoryPath` | `string` | Absolute path to the conversation artifacts directory: `<app_data_dir>/brain/<conversationId>`. |
| `modelName` | `string` | Identifier of the active language model (e.g. `gemini-3.6-flash-medium`, `gemini-4-carbon`). |
| `lastUserInput` | `string` | *(Optional, primarily in `PreInvocation`)* Raw text of the user's latest prompt turn. Enables direct prompt inspection with zero additional disk I/O. |

---

### A. `SessionStart`

- **Trigger**: Executed once when a conversation session is initiated, before any user turns, prompts, or model invocations take place.
- **Purpose**: Initial environment configuration, injecting repository-level guidelines or system prompts, bootstrapping session state, and workspace validation.

#### `SessionStart` Stdin Payload
```json
{
  "conversationId": "b67d4ce2-1b29-4e25-8598-e6636a3171aa",
  "hookEventName": "SessionStart",
  "workspacePaths": ["C:/Users/user/project"],
  "cwd": "C:/Users/user/project",
  "transcriptPath": "C:/Users/user/.gemini/antigravity/brain/b67d4ce2-1b29-4e25-8598-e6636a3171aa/.system_generated/logs/transcript.jsonl",
  "artifactDirectoryPath": "C:/Users/user/.gemini/antigravity/brain/b67d4ce2-1b29-4e25-8598-e6636a3171aa",
  "modelName": "gemini-3.6-flash-medium"
}
```

#### `SessionStart` Stdout Response Contract
```json
{
  "injectSteps": [
    {
      "systemMessage": {
        "systemMessage": "Repository Guidelines: Follow strict typing and modular architecture.",
        "metadata": {
          "source": "session_bootstrap",
          "priority": "high",
          "user_markdown": "### Workspace Initialized\nActive repository guidelines loaded."
        }
      }
    }
  ]
}
```

- **`injectSteps` (array of objects, optional)**: Steps to inject into the initial conversation context (same schema as `PreInvocation` inject steps):
  - `systemMessage` (`object`): Injects or augments system instructions. Object structure: `{"systemMessage": {"systemMessage": "<instruction_text>", "metadata": <optional_metadata_dict>}}`.
    - **`metadata.user_markdown`**: To render Markdown directly in the chat UI without sending the display text to the model, set `metadata.user_markdown`. The UI renders it inline instead of a collapsible "System Message" row, while the model sees only the `systemMessage` text (leave `systemMessage` as `""` if sending no text to the model).
  - `ephemeralMessage` (`string`): *(Deprecated — use `systemMessage` instead; converted to a hidden system message)*. Kept for backward compatibility.
  - `userMessage` (`string`): Synthesized user prompt appended to the session.

---

### B. `PreInvocation`

- **Trigger**: Executed immediately prior to dispatching user input or conversation steps to the model.
- **Purpose**: System prompt augmentation, dynamic skill loading, rules injection, prompt safety gating, and context preservation.

#### `PreInvocation` Stdin Payload
```json
{
  "conversationId": "b67d4ce2-1b29-4e25-8598-e6636a3171aa",
  "hookEventName": "PreInvocation",
  "invocationNum": 0,
  "initialNumSteps": 1,
  "lastUserInput": "Build the feature now",
  "workspacePaths": ["C:/Users/user/project"],
  "cwd": "C:/Users/user/project",
  "transcriptPath": "C:/Users/user/.gemini/antigravity/brain/b67d4ce2-1b29-4e25-8598-e6636a3171aa/.system_generated/logs/transcript.jsonl",
  "artifactDirectoryPath": "C:/Users/user/.gemini/antigravity/brain/b67d4ce2-1b29-4e25-8598-e6636a3171aa",
  "modelName": "gemini-3.6-flash-medium"
}
```

> [!TIP]
> **Native `lastUserInput` Prompt Extraction**:
> Antigravity provides the native `lastUserInput` string property directly in the top-level `PreInvocation` stdin JSON payload. Hooks should extract `payload.get("lastUserInput")` directly for high-performance prompt analysis and keyword matching with zero additional disk I/O.
> 
> Reading and parsing `transcriptPath` (JSONL) is strictly a fallback mechanism for backward compatibility when running in environments where `lastUserInput` is omitted or empty.

#### `PreInvocation` Stdout Response Contract
```json
{
  "injectSteps": [
    {
      "systemMessage": {
        "systemMessage": "Enforce strict verification before tool use.",
        "metadata": {
          "source": "pre_invocation",
          "user_markdown": "🛡️ **Policy Active**: Strict verification enabled for this turn."
        }
      }
    },
    {
      "userMessage": "Synthetic prompt addition for the current turn."
    }
  ],
  "terminationBehavior": ""
}
```

Or when blocking/canceling a prompt:
```json
{
  "injectSteps": [
    {
      "errorMessage": {
        "userMessage": "Prompt blocked by security policy: Destructive SQL operations are prohibited."
      }
    }
  ],
  "terminationBehavior": "terminate"
}
```

- **`injectSteps` (`array of objects`, optional)**: List of steps to inject into the conversation trajectory before the model is called. Supported step types:
  - `systemMessage` (`object`): Out-of-band system instructions for the agent: `{"systemMessage": {"systemMessage": "...", "metadata": {...}}}`. Persists in conversation trajectory across turns (requires a nested object, not a plain string).
    - **`metadata.user_markdown`**: Renders Markdown inline in the chat UI without sending the display text to the model. The model only reads the inner `systemMessage` text (or nothing if set to `""`).
  - `userMessage` (`string`): A plain string message from the user.
  - `ephemeralMessage` (`string`): *(Deprecated — use `systemMessage` instead; converted to a hidden system message)*. Transient system message supported for backward compatibility.
  - `errorMessage` (`object`): Displays an error message to the user without sending it to the model. Structure: `{"userMessage": "<error text>"}`.
    - Marks the turn as errored with a non-zero exit code in non-interactive `-p` mode.
    - Does **not** stop execution on its own unless paired with `"terminationBehavior": "terminate"`.
  > [!WARNING]
  > Note: `"toolCall"` is **NOT** a valid step type for `injectSteps` in `PreInvocation`. Only `systemMessage`, `userMessage`, `ephemeralMessage` (deprecated), and `errorMessage` objects are supported.
- **`terminationBehavior` (`string`, optional)**: Controls execution flow before calling the model:
  - `"terminate"`: Stops execution immediately before calling the model (pair with an injected `errorMessage` to display a block message to the user).
  - `""` (or omitted): Proceeds to the model call (default).

---

### C. `PostInvocation`

- **Trigger**: Executed immediately after each model invocation completes.
- **Purpose**: Evaluates completion criteria, controls turn continuation, or halts execution loops.

#### `PostInvocation` Stdin Payload
Same as `PreInvocation` input fields (`invocationNum`, `initialNumSteps`, `hookEventName`, and common fields).

#### `PostInvocation` Stdout Response Contract
```json
{
  "injectSteps": [
    {
      "systemMessage": {
        "systemMessage": "Task incomplete: You still have pending verification tests to execute."
      }
    }
  ],
  "terminationBehavior": "force_continue"
}
```

- **`injectSteps` (`array of objects`, optional)**: Steps to inject after the invocation completes (accepts the same step schemas as `PreInvocation`).
- **`terminationBehavior` (`string`, optional)**: Controls execution flow after injection:
  - `"force_continue"`: Forces the execution loop to continue.
  - `"terminate"`: Forces the loop to terminate (pair with an injected `errorMessage` to show a block message).
  - `""` (or omitted): Normal lifecycle progression.

---

### D. `PreToolUse`

- **Trigger**: Executed immediately before running a tool call matching the configured `matcher`.
- **Purpose**: Security evaluation, parameter validation, role-based access control, tool argument shallow overrides, and dynamic permission overrides.

#### `PreToolUse` Stdin Payload
```json
{
  "conversationId": "b67d4ce2-1b29-4e25-8598-e6636a3171aa",
  "hookEventName": "PreToolUse",
  "stepIdx": 2,
  "toolCall": {
    "id": "toolu_01",
    "name": "run_command",
    "args": {
      "CommandLine": "npm test",
      "Cwd": "C:/Users/user/project",
      "WaitMsBeforeAsync": 5000
    }
  },
  "workspacePaths": ["C:/Users/user/project"],
  "cwd": "C:/Users/user/project",
  "transcriptPath": "C:/Users/user/.gemini/antigravity/brain/b67d4ce2-1b29-4e25-8598-e6636a3171aa/.system_generated/logs/transcript.jsonl",
  "artifactDirectoryPath": "C:/Users/user/.gemini/antigravity/brain/b67d4ce2-1b29-4e25-8598-e6636a3171aa",
  "modelName": "gemini-3.6-flash-medium"
}
```

- **`toolCall.id` (`string`)**: Unique identifier for this proposed tool invocation (e.g. `"toolu_01"`).
- **`toolCall.name` (`string`)**: The name of the tool proposed for execution (e.g. `"run_command"`, `"write_file"`).
- **`toolCall.args` (`object`)**: Key-value map of arguments passed to the tool call.
- **`stepIdx` (`int`)**: 0-based index of the current step in the trajectory.

#### `PreToolUse` Stdout Response Contract
```json
{
  "decision": "allow",
  "reason": "Test suite verified by security policy.",
  "permissionOverrides": [
    "command(npm test)",
    "read_file(C:/Users/user/project/*)"
  ],
  "overwrite": {
    "CommandLine": "npm test -- --ci",
    "WaitMsBeforeAsync": 10000
  }
}
```

- **`decision` (`string`)**:
  - `"allow"`: Tool execution proceeds immediately without prompting the user.
  - `"auto_approve"`: Automatically approves tool execution when default policy would otherwise prompt the user, while still respecting user-defined custom rules and restrictions (ranks between `"allow"` and `"ask"`).
  - `"deny"`: Tool execution is blocked; the `reason` is returned to the model as the tool error.
  - `"ask"`: Prompts the user for interactive approval before running.
  - `"force_ask"`: Forces a confirmation prompt even if prior automated rules allowed it.
  - `"deny_unless_prior_grant"`: Denies execution unless an explicit permission grant was previously given.
- **`reason` (`string`, optional)**: Explanation displayed to the user or passed back to the model.
- **`permissionOverrides` (`string[]`, optional)**: Array of permission strings granted for subsequent actions (e.g. `["command(npm test)", "read_file(/path/*)"]`).
- **`overwrite` (`object`, optional)**: Object specifying tool input arguments to override before tool execution.
  - **Sequential Shallow Merge**: When multiple hooks execute in a pipeline, their `overwrite` dictionaries are shallow-merged sequentially in pipeline order (`tool_input.update(hook_res.overwrite)`). Later hooks override overlapping keys from earlier hooks. If the final merged dictionary is non-empty, it is included in the output `{"overwrite": merged_overwrites}`.
  - **Use Cases & Scenarios**:
    1. **Parameter Hardening & Safe Defaults**: Enforcing required security or non-interactive flags (e.g. appending `--ci` or `--batch` to `CommandLine`, capping timeouts or `WaitMsBeforeAsync`).
    2. **Path Sanitization & Sandbox Redirection**: Rewriting target file paths (e.g. redirecting writes from sensitive system directories to `.scratch/` or workspace-relative directories).
    3. **Argument Mutation Without Turn Rejection**: Correcting known model tool argument mistakes (e.g. converting `Overwrite: false` to `true` when appending, or fixing malformed options) without failing the tool execution or generating a reject error.

---

### E. `PostToolUse`

- **Trigger**: Executed immediately after a tool call completes execution.
- **Purpose**: Output auditing, post-action linter verification, comment checking, and artifact validations.

#### `PostToolUse` Stdin Payload
```json
{
  "conversationId": "b67d4ce2-1b29-4e25-8598-e6636a3171aa",
  "hookEventName": "PostToolUse",
  "stepIdx": 2,
  "toolCall": {
    "id": "toolu_01",
    "name": "write_file",
    "args": {
      "Path": "C:/Users/user/project/src/index.ts",
      "Content": "console.log('hello');",
      "Overwrite": true
    }
  },
  "error": "",
  "workspacePaths": ["C:/Users/user/project"],
  "cwd": "C:/Users/user/project",
  "transcriptPath": "C:/Users/user/.gemini/antigravity/brain/b67d4ce2-1b29-4e25-8598-e6636a3171aa/.system_generated/logs/transcript.jsonl",
  "artifactDirectoryPath": "C:/Users/user/.gemini/antigravity/brain/b67d4ce2-1b29-4e25-8598-e6636a3171aa",
  "modelName": "gemini-3.6-flash-medium"
}
```

- **`toolCall.id` (`string`)**: Unique identifier corresponding to the `PreToolUse` tool call (e.g. `"toolu_01"`).
- **`error` (`string`)**: Empty string `""` if the tool succeeded; contains the failure message if execution failed.
- **`stepIdx` (`int`)**: 0-based index of the tool step within the current turn.

#### `PostToolUse` Stdout Response Contract
```json
{}
```

> [!IMPORTANT]
> The official Antigravity standard response contract for `PostToolUse` requires `stdout` to be strictly empty JSON `{}`. Any non-empty response triggers protojson unmarshal errors in the standard tool runner. All diagnostic logging, linter outputs, or warnings MUST be directed to `stderr` (which is safely surfaced in logs and agent debugging streams without breaking protojson deserialization).

---

### F. `Stop`

- **Trigger**: Executed when the agent session or execution loop is preparing to terminate.
- **Purpose**: Verifies task completion, enforces verification steps, cleans up background processes, and permits loop re-entry.

#### `Stop` Stdin Payload
```json
{
  "conversationId": "b67d4ce2-1b29-4e25-8598-e6636a3171aa",
  "hookEventName": "Stop",
  "executionNum": 1,
  "terminationReason": "NO_TOOL_CALL",
  "error": "",
  "fullyIdle": true,
  "continuationActive": false,
  "workspacePaths": ["C:/Users/user/project"],
  "cwd": "C:/Users/user/project",
  "transcriptPath": "C:/Users/user/.gemini/antigravity/brain/b67d4ce2-1b29-4e25-8598-e6636a3171aa/.system_generated/logs/transcript.jsonl",
  "artifactDirectoryPath": "C:/Users/user/.gemini/antigravity/brain/b67d4ce2-1b29-4e25-8598-e6636a3171aa",
  "modelName": "gemini-3.6-flash-medium"
}
```

- **`executionNum` (`int`)**: Sequence number of the execution attempt (0 for the initial attempt).
- **`continuationActive` (`boolean`)**: `true` while the agent is executing work that a `Stop` hook requested in this turn (`executionNum > 0`); `false` again once a new user message starts a turn. Check this property to avoid infinite continuation loops!
- **`terminationReason` (`string`)**: The reason why the execution is stopping. Supports both high-level aliases and official protojson `ExecutorTerminationReason` enum names:
  - `"model_stop"` / `"NO_TOOL_CALL"`: Normal turn completion (model finished without calling a tool).
  - `"max_steps_exceeded"` / `"MAX_INVOCATIONS"`: Reached the maximum invocation limit for the turn.
  - `"MAX_FORCED_INVOCATIONS"`: Reached the limit of forced continuation steps.
  - `"MAX_TOKEN_BUDGET_EXCEEDED"`: Consumed the maximum allowed token budget.
  - `"error"` / `"ERROR"`: Execution terminated due to a system error.
  - `"USER_CANCELED"`: Canceled by user intervention.
  - `"TERMINAL_STEP_TYPE"`: Execution stopped on a terminal step type.
  - `"TERMINAL_CUSTOM_HOOK"`: Terminated early by a custom `PreInvocation` or `PostInvocation` hook.
  - `"INJECTED_RESPONSE"`: Terminated after an injected response step.
- **`error` (`string`)**: Error description if termination was caused by a fault; empty string otherwise.
- **`fullyIdle` (`boolean`)**: `true` if all background commands, processes, and subagents have completed; `false` if active background tasks are still running.

#### `Stop` Stdout Response Contract
```json
{
  "decision": "continue",
  "reason": "Tests have not yet been executed. You must run 'npm test' before ending this session."
}
```
Or to allow normal termination:
```json
{}
```

- **`decision` (`string`, required if continuing)**:
  > [!IMPORTANT]
  > **Strict Stop Decision Contract**: **ONLY `"decision": "continue"` prevents the agent from stopping and re-enters the execution loop.** Any other value (including `"block"`, unrecognized strings, or `{}`) allows the agent to stop! Never return `"block"` expecting to prevent termination.
  - `"decision": "continue"`: Cancels the shutdown sequence and forces the agent back into the execution loop. The companion `reason` message is injected as a system message to prompt the agent to complete remaining work.
  - `{}` (empty JSON object) or omitting `decision`: Permits normal termination and shutdown of the agent session.
- **`reason` (`string`, optional)**: If `decision` is `"continue"`, this message is injected as an out-of-band system message into the conversation to instruct the agent on what work remains.

> [!TIP]
> **Continuation Safety Pattern**:
> ```python
> if context.continuation_active:
>     return HookResult()  # Do not ask to continue again in a loop
> if not tests_passed:
>     return HookResult(decision="continue", reason="Please run tests to verify changes.")
> return HookResult()
> ```

---

## 3. Supported Antigravity Tools Catalog

Antigravity provides standard tools organized into six functional categories. Matchers in `PreToolUse` and `PostToolUse` can inspect, gate, or mutate arguments for any of these tool calls. Matchers should account for both current runtime tool names and legacy tool aliases:

### 1. File & Directory Tools
- **`read_file`** *(Current Runtime)*: Reads file content (supports text, image, pdf, video, or audio files).
  - *Arguments*: `Path` (string, required), `StartLine` (int, optional), `EndLine` (int, optional), `ByteOffset` (int, optional).
- **`view_file`** *(Legacy Alias)*: Reads file content (supports text and binary media).
  - *Arguments*: `AbsolutePath` (string, required), `StartLine` (int, optional), `EndLine` (int, optional), `IsSkillFile` (bool, optional), `ContentOffset` (int, optional).
- **`view_file_outline`** / **`view_code_item`** *(Legacy Read Aliases)*: Structural inspection tools for viewing high-level outlines or individual symbol items.
- **`write_file`** *(Current Runtime)*: Creates a new file, or appends/overwrites an existing file.
  - *Arguments*: `Path` (string, required), `Content` (string, required), `Overwrite` (bool, optional), `Append` (bool, optional).
- **`write_to_file`** *(Legacy Alias)*: Creates or overwrites files.
  - *Arguments*: `TargetFile` (string, required), `Overwrite` (bool, required), `CodeContent` (string, required), `Description` (string, required), `IsArtifact` (bool, optional), `ArtifactMetadata` (object, optional).
- **`edit_file`** *(Current Runtime)*: Edits a single contiguous block of text in an existing file.
  - *Arguments*: `Path` (string, required), `Target` (string, required), `Replacement` (string, required).
- **`replace_file_content`** *(Legacy Alias)*: Replaces a single contiguous code block in a file.
  - *Arguments*: `TargetFile` (string, required), `Instruction` (string, required), `Description` (string, required), `AllowMultiple` (bool, required), `TargetContent` (string, required), `ReplacementContent` (string, required), `StartLine` (int, required), `EndLine` (int, required), `TargetLintErrorIds` (string[], optional).
- **`multi_replace_file_content`** *(Legacy Alias)*: Makes multiple, non-contiguous edits to the same file.
  - *Arguments*: `TargetFile` (string, required), `Instruction` (string, required), `Description` (string, required), `ReplacementChunks` (array of chunk objects with `StartLine`, `EndLine`, `TargetContent`, `ReplacementContent`, required), `TargetLintErrorIds` (string[], optional), `ArtifactMetadata` (object, optional).
- **`list_dir`**: Lists directory entries and metadata.
  - *Arguments*: `DirectoryPath` (string, required).
- **`find_by_name`**: Fast file/directory search via glob patterns.
  - *Arguments*: `SearchDirectory` (string, required), `Pattern` (string, required), `Type` (`"file" | "directory" | "any"`, optional), `Excludes` (string[], optional), `Extensions` (string[], optional), `FullPath` (bool, optional), `MaxDepth` (int, optional).

### 2. Search & Research Tools
- **`grep_search`**: Fast text searches within specific paths using ripgrep.
  - *Arguments*: `SearchPath` (string, required), `Query` (string, required), `IsRegex` (bool, optional), `CaseInsensitive` (bool, optional), `Includes` (string[], optional), `MatchPerLine` (bool, optional).
- **`search_web`**: Performs a general web search.
  - *Arguments*: `query` (string, required), `domain` (string, optional).
- **`read_url_content`**: Fetches and converts static HTTP URLs to markdown.
  - *Arguments*: `Url` (string, required).

### 3. System & Execution Tools
- **`run_command`**: Executes shell commands on the host machine.
  - *Arguments*: `CommandLine` (string, required), `Cwd` (string, required), `WaitMsBeforeAsync` (int, required), `RunPersistent` (bool, optional), `RequestedTerminalID` (string, optional), `IsDaemon` (bool, optional), `toolSummary` (string, optional).
- **`manage_task`**: Interacts with background tasks.
  - *Arguments*: `Action` (`'list' | 'kill' | 'status' | 'send_input'`, required), `TaskId` (string, optional), `Input` (string, optional).
- **`schedule`**: Sets timers or recurring cron tasks.
  - *Arguments*: `Prompt` (string, required), `DurationSeconds` (int, optional), `CronExpression` (string, optional), `MaxIterations` (int, optional).
- **`list_permissions`**: Lists active permissions granted for the current session.
  - *Arguments*: None.
- **`ask_permission`**: Programmatically requests additional scoped permissions.
  - *Arguments*: `Action` (string, required), `Target` (string, required), `Reason` (string, required).

### 4. Agent Collaboration & Multi-Agent Orchestration Tools
- **`invoke_subagent`**: Spawns specialized subagents to execute concurrent tasks.
  - *Arguments*: `Subagents` (array of subagent specs: `Prompt`, `Role`, `TypeName`, `Workspace` (optional: `'inherit' | 'branch' | 'share'`), `Model` (optional: `'inherit' | 'flash' | 'flash_lite' | 'pro'`)).
- **`define_subagent`**: Creates and registers a dynamic custom subagent persona.
  - *Arguments*: `name` / `Name` (string, required), `description` / `Description` (string, required), `system_prompt` / `SystemPrompt` (string, required), `enable_mcp_tools` / `EnableMCPTools` (bool, optional), `enable_write_tools` / `EnableWriteTools` (bool, optional), `enable_subagent_tools` / `EnableSubagentTools` (bool, optional).
- **`send_message`**: Communicates with other agents (parent, children, or peers).
  - *Arguments*: `Recipient` (string, required), `Message` (string, required).
- **`manage_subagents`**: Lists or terminates active subagents.
  - *Arguments*: `Action` (`'list' | 'kill' | 'kill_all'`, required), `ConversationIds` (string[], optional).
- **`run_workflow`**: Coordinates multi-agent Dynamic Workflows via scripted Python control flow (`/run-workflow`).
  - *Arguments*: Workflow script execution parameters.
- **`swarm`**: Launches and manages collaborative agent swarms communicating over a shared live message board (`/swarm`).
- **`exit_plan_mode`**: In Orchestrator mode, transitions from the read-only planning phase (Gemini 4 Carbon/Argon) to active implementation (Gemini 4 Hydrogen).
- **`search_marketplace`**: Searches for plugins and extensions in the Antigravity Marketplace.
  - *Arguments*: Search query and filters.
- **`list_plugin_accounts`**: Lists authenticated accounts, credentials, and configuration states for installed plugins.

### 5. Interaction & Media Tools
- **`ask_question`**: Asks the user interactive questions with optional choices.
  - *Arguments*: `questions` (array of objects with `question`, `options`, `is_multi_select`, required).
- **`generate_image`**: Creates or edits images and UI mockups (powered by Nano Banana 2).
  - *Arguments*: `Prompt` (string, required), `ImageName` (string, required), `ImagePaths` (string[], optional).

### 6. MCP (Model Context Protocol) Tools
- **`call_mcp_tool`**: Calls a lazily-loaded MCP tool.
  - *Arguments*: `ServerName` (string, required), `ToolName` (string, required), `Arguments` (object, required).
- **`list_resources`**: Lists available resources from an MCP server.
  - *Arguments*: `ServerName` (string, required).
- **`read_resource`**: Retrieves content of a specified MCP resource.
  - *Arguments*: `ServerName` (string, required), `Uri` (string, required).

---

## 4. Unified Hook Engine Architecture

The **Unified Hook Engine** provides a modular pipeline architecture replacing fragmented standalone scripts. It handles stream configuration, strongly typed context parsing, sequential pipeline execution with error containment, and schema-compliant serialization.

```
                  +-----------------------------------+
                  |         Antigravity Loop          |
                  +-----------------------------------+
                                    | (JSON via stdin)
                                    v
                  +-----------------------------------+
                  |  Entrypoint (e.g. pre_tool_use.py)|
                  +-----------------------------------+
                                    | 5-line delegation
                                    v
                  +-----------------------------------+
                  |           HookEngine              |
                  +-----------------------------------+
                    |               |               |
          parse_payload()     build_context()   serialize_output()
                    |               |               ^
                    v               v               |
            +-----------------------------------------------+
            |                 HookPipeline                  |
            |  +---------------+     +---------------+      |
            |  | BaseHook 1    | --> | BaseHook 2    | ...  |
            |  +---------------+     +---------------+      |
            +-----------------------------------------------+
```

### 4.1 Core Abstractions & Data Contracts

Located in [`scripts/hooks/models.py`](file:///scripts/hooks/models.py) and [`scripts/hooks/engine.py`](file:///scripts/hooks/engine.py):

#### Data Contracts (`models.py`)
```python
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

class LifecycleEvent(Enum):
    SESSION_START = "SessionStart"
    PRE_INVOCATION = "PreInvocation"
    POST_INVOCATION = "PostInvocation"
    PRE_TOOL_USE = "PreToolUse"
    POST_TOOL_USE = "PostToolUse"
    STOP = "Stop"

class AgentRole(Enum):
    ORCHESTRATOR = "orchestrator"
    WORKER = "worker"
    RESEARCH = "research"
    UNKNOWN = "unknown"

@dataclass(frozen=True)
class HookContext:
    lifecycle: LifecycleEvent
    conversation_id: str
    cwd: str
    tool_name: str | None = None
    tool_input: dict[str, Any] = field(default_factory=dict)
    tool_output: str | None = None
    tool_error: str | None = None
    user_prompt: str | None = None
    raw_payload: dict[str, Any] = field(default_factory=dict)
    step_idx: int | None = None
    model_name: str | None = None
    hook_event_name: str | None = None
    tool_call_id: str | None = None
    continuation_active: bool = False
    workspace_paths: list[str] = field(default_factory=list)
    transcript_path: str | None = None
    artifact_directory_path: str | None = None
    invocation_num: int | None = None
    execution_num: int | None = None

@dataclass
class HookResult:
    injected_steps: list[dict[str, Any]] = field(default_factory=list)
    decision: str | None = None  # "allow" | "deny" | "ask" | "auto_approve" | "force_ask" | "deny_unless_prior_grant" | "force_continue" | "terminate" | "block"
    reason: str | None = None
    additional_context: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    permission_overrides: list[str] = field(default_factory=list)
    overwrite: dict[str, Any] | None = None
    error_message: str | None = None
```

#### Base Hook & Pipeline (`engine.py`)
```python
from abc import ABC, abstractmethod
import sys
from scripts.hooks.models import HookContext, HookResult

class BaseHook(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """Unique descriptive name for the hook."""
        ...

    @abstractmethod
    def execute(self, context: HookContext) -> HookResult:
        """Executes logic against strongly typed context."""
        ...

class HookPipeline:
    def __init__(self, hooks: list[BaseHook] | None = None) -> None:
        self.hooks: list[BaseHook] = list(hooks) if hooks else []

    def register(self, hook: BaseHook) -> None:
        self.hooks.append(hook)

    def run(self, context: HookContext) -> list[HookResult]:
        results: list[HookResult] = []
        for hook in self.hooks:
            try:
                res = hook.execute(context)
                if res is not None:
                    results.append(res)
            except Exception as e:
                # Error containment: isolate failure to stderr, prevent crashing agent
                sys.stderr.write(f"[HookEngine] Error in hook '{hook.name}': {e}\n")
        return results
```

---

### 4.2 Custom Hook Implementations

#### 1. Security Gate Hook (`PreToolUse`)
```python
from scripts.hooks.engine import BaseHook
from scripts.hooks.models import HookContext, HookResult

class DestructiveCommandGateHook(BaseHook):
    @property
    def name(self) -> str:
        return "destructive_command_gate"

    def execute(self, context: HookContext) -> HookResult:
        if context.tool_name == "run_command":
            cmd = context.tool_input.get("CommandLine", "")
            if any(danger in cmd for danger in ["rm -rf /", "drop database", "mkfs"]):
                return HookResult(
                    decision="deny",
                    reason=f"Blocked dangerous command: '{cmd}'",
                )
            if "npm test" in cmd:
                return HookResult(
                    decision="allow",
                    permission_overrides=["command(npm test)"]
                )
        return HookResult(decision="allow")
```

#### 2. Continuation Enforcer Hook (`Stop`)
```python
from scripts.hooks.engine import BaseHook
from scripts.hooks.models import HookContext, HookResult

class StopVerificationGuardHook(BaseHook):
    @property
    def name(self) -> str:
        return "stop_verification_guard"

    def execute(self, context: HookContext) -> HookResult:
        # Check continuation_active to prevent infinite loops if already running a continuation turn
        if context.continuation_active:
            return HookResult()
        # Prevent stopping if tests have not been executed
        if context.execution_num and context.execution_num < 3:
            return HookResult(
                decision="continue",
                reason="Verification required: Please run the test suite before ending the session."
            )
        # Note: ONLY decision="continue" prevents stopping. Any other value (or empty result) allows the agent to stop.
        return HookResult()
```

#### 3. Context Injector Hook (`PreInvocation`)
```python
from scripts.hooks.engine import BaseHook
from scripts.hooks.models import HookContext, HookResult

class ProjectGuidelineInjectorHook(BaseHook):
    @property
    def name(self) -> str:
        return "project_guideline_injector"

    def execute(self, context: HookContext) -> HookResult:
        if context.invocation_num == 0:
            return HookResult(injected_steps=[
                {
                    "systemMessage": {
                        "systemMessage": f"Active in: {context.cwd}. Adhere to strict type-safety.",
                        "metadata": {
                            "user_markdown": f"ℹ️ Active workspace: `{context.cwd}`"
                        }
                    }
                }
            ])
        return HookResult()
```

#### 4. Prompt Guard & Cancellation Hook (`PreInvocation`)
```python
from scripts.hooks.engine import BaseHook
from scripts.hooks.models import HookContext, HookResult

class PromptSafetyGuardHook(BaseHook):
    @property
    def name(self) -> str:
        return "prompt_safety_guard"

    def execute(self, context: HookContext) -> HookResult:
        # Direct zero-overhead prompt access via context.user_prompt
        user_prompt = context.user_prompt or ""
        if "DROP DATABASE" in user_prompt.upper():
            return HookResult(
                injected_steps=[{
                    "errorMessage": {
                        "userMessage": "Unauthorized prompt: Destructive SQL operations are blocked"
                    }
                }],
                decision="terminate",
                reason="Prompt rejected by database protection policy"
            )
        return HookResult()
```

---

### 4.3 Pure Permission & Session Resolution

Access control is decoupled into an I/O discovery seam and a pure policy evaluation engine:

1. **[`SessionResolver`](file:///scripts/hooks/session.py)**:
   - Reads `.system_generated/logs/transcript.jsonl` under `<app_data_dir>/brain/<conversationId>`.
   - Resolves subagent `TypeName` from prior `invoke_subagent` calls.
   - Maps agent types to [`AgentRole.ORCHESTRATOR`](file:///scripts/hooks/models.py) (e.g. Sisyphus, Atlas, Prometheus) or [`AgentRole.WORKER`](file:///scripts/hooks/models.py) (e.g. Hephaestus, Explore, Librarian).

2. **[`PermissionPolicy`](file:///scripts/hooks/permission.py)**:
   - Contains zero filesystem access or log parsing.
   - Pure function: `evaluate(role: AgentRole, tool_name: str, target_path: str | None) -> PermissionDecision`.
   - **Orchestrator Rules**: Cannot directly edit source files (`.py`, `.ts`, `.js`); must delegate via `invoke_subagent` or limit edits to documentation and plans.
   - **Worker Rules**: Allowed to edit source files; barred from modifying `.agents/` configurations and plugin root definitions.

```python
from scripts.hooks.models import AgentRole
from scripts.hooks.permission import PermissionPolicy

# Deterministic pure evaluation
decision = PermissionPolicy.evaluate(
    role=AgentRole.ORCHESTRATOR,
    tool_name="write_to_file",
    target_path="src/index.ts"
)
# Result: decision.allowed == False, decision.decision == "ask"
```

---

### 4.4 Modular Skill Resolution

The [`SkillResolver`](file:///scripts/hooks/skill_resolver.py) resolves skill directories in strict precedence order:
1. Workspace Local: `<workspace>/skills/<name>/SKILL.md`, `<workspace>/.agents/skills/...`
2. Plugin Bundled: `<plugin_root>/skills/<name>/SKILL.md`
3. Sibling Plugins: `<plugins_dir>/*/skills/<name>/SKILL.md`
4. User Config: `~/.gemini/config/skills/<name>/SKILL.md`
5. Builtin Skills: `~/.gemini/antigravity/builtin/skills/<name>/SKILL.md`

Discovered skill documentation is wrapped into standard XML injection blocks:
```xml
<skill-instruction>
... SKILL.md contents ...
</skill-instruction>
```

---

### 4.5 Modern Entrypoint Runner Scripts

Each entrypoint script is a concise 5-line delegation wrapper around `HookEngine`:

#### `scripts/pre_invocation.py`
```python
import sys
from scripts.hooks.engine import HookEngine, LifecycleEvent

def main() -> int:
    return HookEngine.run(LifecycleEvent.PRE_INVOCATION, sys.stdin)

if __name__ == "__main__":
    sys.exit(main())
```

#### `scripts/pre_tool_use.py`
```python
import sys
from scripts.hooks.engine import HookEngine, LifecycleEvent

def main() -> int:
    return HookEngine.run(LifecycleEvent.PRE_TOOL_USE, sys.stdin)

if __name__ == "__main__":
    sys.exit(main())
```

#### `scripts/post_tool_use.py`
```python
import sys
from scripts.hooks.engine import HookEngine, LifecycleEvent

def main() -> int:
    return HookEngine.run(LifecycleEvent.POST_TOOL_USE, sys.stdin)

if __name__ == "__main__":
    sys.exit(main())
```

#### `scripts/stop.py`
```python
import sys
from scripts.hooks.engine import HookEngine, LifecycleEvent

def main() -> int:
    return HookEngine.run(LifecycleEvent.STOP, sys.stdin)

if __name__ == "__main__":
    sys.exit(main())
```

---

## 5. Testing Best Practices & Zero-Mock Seams

The Unified Hook Engine allows direct, in-memory testing without patching standard library modules (`builtins.open`, `sys.stdin`, `sys.stdout`):

### 1. In-Memory `HookContext` Testing
```python
from scripts.hooks.models import HookContext, LifecycleEvent
from my_hooks import DestructiveCommandGateHook

def test_command_gate_denies_rm_rf():
    hook = DestructiveCommandGateHook()
    context = HookContext(
        lifecycle=LifecycleEvent.PRE_TOOL_USE,
        conversation_id="test-conv-uuid",
        cwd="/workspace",
        step_idx=0,
        tool_name="run_command",
        tool_input={"CommandLine": "rm -rf /"}
    )
    result = hook.execute(context)
    assert result.decision == "deny"
    assert "Blocked dangerous command" in result.reason
```

### 2. Pure Permission Testing
```python
from scripts.hooks.models import AgentRole
from scripts.hooks.permission import PermissionPolicy

def test_orchestrator_denied_source_code_edit():
    decision = PermissionPolicy.evaluate(
        role=AgentRole.ORCHESTRATOR,
        tool_name="write_to_file",
        target_path="src/app.py"
    )
    assert not decision.allowed
    assert decision.decision == "ask"
```

### 3. Pipeline Error Containment Testing
```python
from scripts.hooks.engine import BaseHook, HookPipeline
from scripts.hooks.models import HookContext, HookResult, LifecycleEvent

class FaultyHook(BaseHook):
    @property
    def name(self) -> str:
        return "faulty_hook"
    def execute(self, context: HookContext) -> HookResult:
        raise RuntimeError("Disk failure")

class GoodHook(BaseHook):
    @property
    def name(self) -> str:
        return "good_hook"
    def execute(self, context: HookContext) -> HookResult:
        return HookResult(decision="allow")

def test_pipeline_isolates_fault():
    pipeline = HookPipeline([FaultyHook(), GoodHook()])
    context = HookContext(lifecycle=LifecycleEvent.PRE_TOOL_USE, conversation_id="c1", cwd="/app")
    results = pipeline.run(context)
    assert len(results) == 1
    assert results[0].decision == "allow"
```

---

## 6. Production Best Practices & Troubleshooting Matrix

### Best Practices

1. **Standard Output Cleanliness**:
   - Only write valid JSON to `stdout`.
   - Direct all debugging, diagnostics, and stack traces to `sys.stderr`.
2. **Cross-Platform UTF-8 Streams**:
   - Ensure streams use UTF-8: `sys.stdin.reconfigure(encoding='utf-8')` and `sys.stdout.reconfigure(encoding='utf-8')`.
3. **Execution Timeouts**:
   - Keep hook execution fast (< 5s). Avoid blocking network requests or expensive operations.
4. **Subagent Awareness**:
   - Inspect `conversationId` and parent session transcripts to adapt behaviors between orchestrators and workers.
5. **Path Formatting & Cross-Platform Template Rendering**:
   - In `hooks.template.json`, use template placeholders `{{PYTHON}}` and `{{PLUGIN_DIR}}` with forward slashes (`/`).
   - Hardcoding Windows `%USERPROFILE%` fails on POSIX shells (`/bin/sh`) on Linux/macOS. Always render `hooks.json` from `hooks.template.json` using `setup_hooks.py` or the installers (`install.sh`, `install.ps1`).

### Troubleshooting Matrix

| Symptom | Probable Cause | Corrective Action |
|---|---|---|
| Hook does not execute | Incorrect matcher regex, file path error, or `"enabled": false` | Verify regex with test strings, ensure script exists at relative path, and check `enabled: true`. |
| Hook fails with FileNotFoundError (literal `%USERPROFILE%`) on Linux/macOS | POSIX shell does not expand `%USERPROFILE%` Windows variables | Run `python scripts/setup_hooks.py` or `install.sh` to render `hooks.json` from `hooks.template.json`. |
| Hook fails with FileNotFoundError (Errno 2) in external workspace | Antigravity runs hook commands with CWD set to the directory containing `hooks.json` (`<plugin_root>` for plugins), while `stdin.cwd` is the workspace | Use portable `<plugin_root>`-relative commands (e.g. `"uv run python ./scripts/..."` or `"node ./scripts/..."`) which work out-of-the-box for `agy plugin install`, or render explicit absolute paths via `scripts/setup_hooks.py`. |
| Hook fails with SyntaxError (unterminated string literal) | Windows `cmd.exe /c` strips outer double quotes around inline `python -c "..."` commands | Eliminate double quotes and inline scripts; use clean template pointing directly to script file. |
| Agent runtime JSON error | Non-JSON text printed to `stdout` by hook script | Redirect all `print(...)` and diagnostic logging statements to `sys.stderr`. |
| Hook execution timeout | Script blocked on stdin reading or hanging subprocess | Read full stdin synchronously (`sys.stdin.read()`), ensure subprocess timeouts, and keep operations lightweight. |
| Permission overrides ignored | `permissionOverrides` passed as `{}` instead of `string[]` | Return a string array format, e.g. `["command(npm test)", "read_file(/path/*)"]`. |
| PostInvocation loop not forcing continue | Returned `"decision": "force_continue"` instead of `terminationBehavior` | Update return payload to use `"terminationBehavior": "force_continue"`. |
| Stop loop repeating infinitely | Stop hook unconditionally returning `"decision": "continue"` | Check `continuationActive` (`context.continuation_active`) on `stdin` (`true` while executing `Stop` hook work this turn), or track turn counter (`executionNum`) to allow shutdown when verifications finish. |
| Stop decision "block" vs "continue" confusion | Assuming `"decision": "block"` prevents termination | **ONLY `"decision": "continue"` prevents stopping and re-enters the execution loop; any other value (including `"block"` or `{}`) allows the agent to stop.** Return `"continue"` with a descriptive `reason` to keep working. |
| PreInvocation cancellation not halting turn | Returning top-level string `errorMessage` or omitting `"terminationBehavior": "terminate"` | Return `{"injectSteps": [{"errorMessage": {"userMessage": "..."}}], "terminationBehavior": "terminate"}` (`errorMessage` must be an object inside `injectSteps` paired with `terminate`). |
| Role resolution returns ORCHESTRATOR | Transcript missing from brain logs directory | Ensure path `<app_data_dir>/brain/<conversationId>/.system_generated/logs/transcript.jsonl` exists; fallback to default is expected behavior. |
| Skill instructions not loading | `SKILL.md` missing or outside resolution directories | Check directory precedence order (workspace -> plugin -> user config -> builtin). |
