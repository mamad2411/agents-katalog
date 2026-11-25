---
name: request-eagle-cli
description: Load when the user asks to use request-eagle-cli or to inspect, edit, or run saved requests or flows, manage collections, or change settings in Request Eagle. Do not load merely because a task involves developing Request Eagle or automating its desktop UI.
---

# Request Eagle CLI

Start with `request-eagle-cli --help`. Discover usage through subcommand help
and JSON commands through `request-eagle-cli schema`. Use the installed CLI's
help and schema as the command reference.

If the binary is missing, see [installation instructions](../../docs/cli.md#install).

- Work with saved data. Close the desktop app before edits and reopen it to
  reload changes; unsaved drafts and open tabs are outside this interface.
  In the app's agent panel, the app stays open and reloads collections and
  flows after each turn.
- Use paths and IDs returned by the CLI. Read a request before updating it:
  updates replace the complete request, so preserve fields outside the task.
- Pass JSON through stdin with `call -`, especially when it contains secrets.
- Inspect saved scripts, including collection scripts from `collections.get`,
  before opting into their execution.
- Check the JSON result, HTTP or gRPC status, and script test results. Exit
  code 0 means execution completed; error statuses and failed assertions can
  still occur.
- For flows, read `flows.blocks` before building one and `flows.get` before
  updating one. Try FQL with `fql.evaluate`. After `flows.run`, check its
  `status` and each block's `error`.
