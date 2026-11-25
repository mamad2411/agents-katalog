---
name: web-terminal-acp-ops
description: >
  Use the bundled HTTP CLI to operate Web Terminal ACP: list clients/windows,
  create terminal windows, send input to clients, capture or wait for terminal
  output, search/read project todo cards, create/edit/dispatch project todo
  cards on the source or a target client, inspect linked artifacts and agent
  preview input/output, and create/read artifact plugin preview sessions.
---

# Web Terminal ACP Ops

Use this skill when an agent needs to inspect or operate Web Terminal from a managed agent window.

The bundled CLI talks directly to the Web Terminal HTTP API using `WEB_TERMINAL_SERVER_URL`, `WEB_TERMINAL_CLIENT_ID`, `WEB_TERMINAL_WINDOW_ID`, and `WEB_TERMINAL_AGENT_OPS_TOKEN` from the managed window environment.

The CLI uses `/api/agent-ops/*` endpoints. These endpoints require an agent ops token when authentication is enabled, not a browser session token. Managed Web Terminal windows receive `WEB_TERMINAL_AGENT_OPS_TOKEN` automatically; outside that environment, pass `--ops-token`, `--source-client-id`, and `--source-window-id` explicitly.

Use it for:

- Client/window operations: list schedulable clients, list active windows on a client, create a window, send terminal input to a client/window, capture terminal output, and wait for output text.
- Project todo/card operations: search cards, read a card by todo ID, create cards, edit card fields, and dispatch cards to an agent-client. Todo writes default to the source client and support an explicit target client.
- Project todo/card context: read description, relationships, requested/linked artifact IDs, compact agent turns, worktree data, review targets, and review runs.
- Agent preview input/output: read the agent-record chat/detail for a window ID from a todo run, assigned terminal, review window, artifact `ephemeral_window_id`, or card-provided preview/window ID.
- Artifact inspection: list terminal or project artifacts, read artifact JSON/content/metadata/status/errors by `artifact_id`, read rendered artifact HTML, and resolve a todo card's artifact link `id` through `read-card-artifact`.
- Artifact plugin preview sessions: create/update the live preview bound to this source window, list previews for a window, read a preview's input components/output JSON/status/errors, and read rendered preview HTML.

## CLI

From this skill directory, run the bundled script with Python:

```bash
python3 scripts/web-terminal-acp-ops.py list-clients
python3 scripts/web-terminal-acp-ops.py list-windows <client-id>
python3 scripts/web-terminal-acp-ops.py capture-output <client-id> <window-id> --history-lines 80
python3 scripts/web-terminal-acp-ops.py send-input <client-id> <window-id> 'pwd' --append-enter
python3 scripts/web-terminal-acp-ops.py wait-for-output <client-id> <window-id> 'ready' --timeout-seconds 30
python3 scripts/web-terminal-acp-ops.py search-project-todos 'search terms' --project-path /workspace/project
python3 scripts/web-terminal-acp-ops.py read-project-todo <todo-id>
python3 scripts/web-terminal-acp-ops.py create-project-todo --project-path /workspace/project --target-client-id <client-id> --title 'Implement feature' --description 'Details'
python3 scripts/web-terminal-acp-ops.py patch-project-todo <todo-id> --project-path /workspace/project --status BLOCKED --clear-description
python3 scripts/web-terminal-acp-ops.py dispatch-project-todo <todo-id> --project-path /workspace/project --target-client-id <client-id> --agent codex --command 'codex --model gpt-5.5' --dispatch-mode compose --prompt 'Work on this card'
python3 scripts/web-terminal-acp-ops.py read-agent-preview <client-id> <window-id> --limit 200
python3 scripts/web-terminal-acp-ops.py list-artifacts <client-id> <window-id>
python3 scripts/web-terminal-acp-ops.py read-artifact <client-id> <window-id> <artifact-id>
python3 scripts/web-terminal-acp-ops.py read-card-artifact <todo-id> <card-artifact-link-id-or-artifact-id>
python3 scripts/web-terminal-acp-ops.py read-artifact-html <client-id> <window-id> <artifact-id>
python3 scripts/web-terminal-acp-ops.py upsert-artifact-plugin-preview --title 'Draft' --python-source-file plugin.py --prompt-template-file prompt.txt --html-template-file template.html --json-schema-file schema.json
python3 scripts/web-terminal-acp-ops.py read-artifact-plugin-preview <preview-id>
```

The CLI prints JSON by default. Global options such as `--compact`, `--raw`, `--server-url`, and `--ops-token` must appear before the subcommand, for example `python3 scripts/web-terminal-acp-ops.py --compact read-project-todo <todo-id>`; argparse rejects them after the subcommand. Commands that return HTML print a JSON-encoded string unless `--raw` is passed.

## Notes

- Use this from a Web Terminal managed agent window. Outside that environment, pass `--server-url`, `--source-client-id`, `--source-window-id`, and usually `--ops-token` for tests/debugging.
- The target client/window IDs come from `list-clients` and `list-windows`.
- Todo write commands default to the token's source client from `WEB_TERMINAL_CLIENT_ID`. Use `--target-client-id <client-id>` on `create-project-todo`, `patch-project-todo`, or `dispatch-project-todo` to operate on another schedulable client, such as `code-server`.
- `--source-client-id` and `--source-window-id` identify the calling managed window. They are required outside Web Terminal managed windows, but they are not the way to select the card's target client when `--ops-token` is present; use `--target-client-id` instead.
- Use `--body-json` or `--body-json-file` on todo write commands when you need fields not exposed as first-class CLI flags.
- Use `search-project-todos` to find Kanban cards by title/description/project/status/assigned agent; add `--project-path` to constrain results to one project.
- When a project todo/card is mentioned as `@[其它需求：$Title|<todo-id>]`, pass `<todo-id>` to `read-project-todo` before acting. Its `artifacts` list contains both the card artifact link `id` and the underlying terminal `artifact_id`; either can be passed to `read-card-artifact`.
- To inspect a todo run's agent preview, use the run `window_id` with `read-agent-preview`. To inspect a live artifact agent terminal, use the card artifact `ephemeral_window_id` with `capture-output` or `read-agent-preview` when agent records are available.
- `upsert-artifact-plugin-preview` binds the preview to this source window and returns a stable `id`. Reuse the same preview ID while iterating so the current terminal's Artifacts tab updates in place.
- Terminal input/output correctness still comes from Web Terminal server streams; do not infer screen state from local echoes.
