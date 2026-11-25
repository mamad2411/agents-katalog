---
name: t3-create-task
description: Creates T3 Code conversations through T3's own tools or its native CLI. Use when the user explicitly asks to start a T3 task or hand off the current conversation to T3 Code.
---

# Create a T3 task

Create only after the user's explicit request. Require an actionable prompt and
preserve the objective, constraints, working directory and completion criteria.
Use T3's own tools or official CLI, not a direct database write or a third-party
handover tool.

## 1. Choose the route and discover its capabilities

Two official routes create threads:

- **T3 tools**: a session running inside T3 Code has an MCP server exposing
  `t3_thread_launch` and related tools. The server name carries an instance
  suffix, so find the tools by name. Use this route whenever it is present: it
  sets reasoning effort, attaches an existing worktree, sets modes and returns
  the thread `link`, which the CLI cannot do.
- **CLI**: every other session (Claude Code, Codex, a plain terminal).

| Operation | T3 tools | CLI |
|---|---|---|
| Providers, models, options | `orchestrator_capabilities` | `thread list --json` (see step 2) |
| Find or register a project | `t3_project_list`, `t3_project_create` | `thread list --project`, `project add` |
| Launch | `t3_thread_launch` | `thread start` |
| Follow-up or correction | `t3_thread_send` | `thread send` |
| Change model settings | `t3_thread_configure` | none; per-thread app controls |
| Inspect | `t3_thread_read`, `t3_thread_list` | `thread show`, `thread list` |

For the CLI, use `scripts/t3.sh` in this skill. It resolves the app-owned
launcher, then PATH; `T3_CLI_BIN` explicitly selects another installed
executable. `T3CODE_HOME` selects a non-default T3 data directory using T3's own
convention.

```bash
bash ~/.agents/skills/t3-create-task/scripts/t3.sh --version
bash ~/.agents/skills/t3-create-task/scripts/t3.sh thread start --help
```

Read installed help before dispatch; it is the syntax authority. If the server
is stopped, check `t3 service status` or open the desktop app with
`t3 app "$repo"`. Preserve server, auth and permission settings; the CLI handles
short-lived authentication without exposing tokens.

**Complete when:** the chosen route supports launch, multiline prompts,
structured output and the requested workspace controls. If it does not, report
the missing capability rather than downloading a different server version silently.

## 2. Resolve the project and workspace

Resolve another named repo through `where-is`; the current task's exact repo
path needs no repeated search. Check its branch and dirty state. Confirm T3
recognizes it: match `workspaceRoot` in `t3_project_list`, or run the read-only
CLI command:

```bash
bash ~/.agents/skills/t3-create-task/scripts/t3.sh thread list --project "$repo" --json
```

An empty thread list can be valid. A missing project requires registering it
explicitly with `t3_project_create` (pass `workspaceRoot`), the app or the CLI
`project add` command. Ask only when the destination cannot be inferred safely.

Choose the workspace deliberately:

- Fresh repo task: a new worktree from the verified Git remote default branch,
  unless the user requests another starting point. T3 tools:
  `workspaceStrategy: { type: "worktree", baseRef }`. CLI: `--worktree "$base_ref"`.
  Let T3 name the branch; set `branch` / `--branch` only for an explicitly
  requested name.
- Explicit current-checkout task or context-only handoff: T3 tools
  `{ type: "root" }`; CLI omits `--worktree`. This uses the registered project's
  root, not necessarily the caller's cwd.
- Existing-worktree handoff: T3 tools
  `{ type: "existing_worktree", worktreePath }`. The CLI cannot attach one: a
  nested path passed as `project` resolves to the registered project root. From
  a CLI-only session, ask about the checkout.

Inherit runtime and interaction modes. T3 tools inherit them when omitted and
cannot exceed the caller's. Do not force full access. Use Anthropic Claude Opus
5.5 with medium reasoning effort for every T3 task, unless the user explicitly
overrides this preference for that task. Never use Codex for a T3 task when Opus
5.5 is available. Do not silently substitute a different provider, model, or
effort if the requested combination is unavailable. Report the limitation and
ask how to proceed. Leave project/global defaults unchanged.

Display labels are not identifiers. Resolve the real provider instance and model IDs:

- T3 tools: `providerInstanceId`, model `id` and option ids from
  `orchestrator_capabilities`; pass them in `modelSelection`.
- CLI: identify the provider and model IDs for Anthropic Claude Opus 5.5 from
the app or existing thread metadata. Pass `--provider` and `--model` together.

Treat reasoning effort as per-thread model configuration; prompt text and
composer defaults do not establish it. Always set medium effort. T3 tools: pass it in
`modelSelection.options` at launch, or set it afterwards with
`t3_thread_configure`. The CLI has no effort setting: disclose the gap, pause the
newly started thread, set it through per-thread app controls, then resume that
same thread. Verify the next active run matches the requested provider, model
and effort.

After an uncertain launch, list the project's threads and inspect the run
before retrying; neither route has a retry key. Send corrections or missing
context to that same thread with `t3_thread_send` or `thread send`, preserving
history and completed actions, rather than launching a duplicate.

**Complete when:** the registered project, actual checkout, starting point and
provider, model, effort and modes match the user's task.

## 3. Prepare and dispatch once

For a conversation handoff, read [HANDOFF.md](HANDOFF.md) before writing the prompt.

T3 tools: pass the brief as `message` to `t3_thread_launch`, with `title`,
`projectId`, `modelSelection` and `workspaceStrategy`.

CLI: keep prompt files outside a public repository, with private file
permissions. Use stdin so multiline context and shell metacharacters remain literal:

```bash
bash ~/.agents/skills/t3-create-task/scripts/t3.sh thread start \
  "$repo" - --title "$title" \
  --provider "$provider_instance" --model "$model" --json < "$prompt_file"
```

Append the chosen worktree flags when needed.

Dispatch asynchronously by default. Wait (`t3_thread_wait`, or the CLI's `--wait`)
only for a bounded task whose reply is needed here; a run may take a long time.
`--wait` exits 1 when the run fails and 2 when the agent stops for an answer.
Answer exit 2 with `thread send "$thread_id" -` on stdin, not a new launch.

Save `threadId`, `projectId`, `runId` and `link`.

## 4. Verify and return

T3 tools: `t3_thread_read` with a low `limit`, and `t3_thread_configure` with only
`threadId` to read the provider, model, options and modes.

CLI:

```bash
bash ~/.agents/skills/t3-create-task/scripts/t3.sh thread show \
  "$thread_id" --messages 2 --json
```

Its JSON carries `branch` and `worktreePath` for the workspace check, but may
omit reasoning effort; verify effort through per-thread app controls.

Verify prompt, project, workspace and run state. Report any setting you cannot
verify. Dispatch success is not task completion. Return title, the thread's
`link` verbatim and verified state. Reveal the conversation when useful. Use
only an app/CLI-provided thread link; Codex task directives do not apply.
