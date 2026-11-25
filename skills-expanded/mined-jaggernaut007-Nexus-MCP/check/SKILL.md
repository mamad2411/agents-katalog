---
name: check
description: Check the current change for callers, route users, edge function users, table users and tests that the diff did not update. Runs the offline `nexus-mcp-ci check` and explains each finding.
model: sonnet
disable-model-invocation: true
---

# Check this change

Run it after an edit, before a commit or a pull request. The user starts it with
`/nexus-mcp:check`. It adds no tokens to a session until then.

1. **Find a runner.** Use the first that works: `nexus-mcp-ci`, then
   `uvx --python 3.12 nexus-mcp-ci`. The folder needs an index. If the answer is exit code 3,
   call the `index` tool with the folder, or run `<runner> index .`, and run the check again.

2. **Run the check.** Use `<runner> check . --format json`. Add `--staged` to check only the
   staged changes, or `--base <commit>` to compare with another commit.

3. **Read the result.** Each entry in `findings` has a `severity`, the `symbol` that changed,
   the `caller` (or the file and line of a reference) that the diff did not update, and the
   `reason`. `affected_tests` lists the tests that reach the change.
   - `high`: the symbol was removed or its parameters changed, a route no longer serves a path,
     or a column was dropped. Open each caller and fix it, or say why it stays as it is.
   - `medium` and `low`: look at the caller. Many are fine.

4. **Run `affected_tests`**, then report: the findings that you fixed, the findings that stay and
   why, and the tests that you ran.

The check is static and name-based: a dynamic call, a callback, a computed URL and a string
reference are not seen. An empty result does not prove that nothing breaks. The Stop hook of this
plugin runs the same check at the end of each turn and speaks only for a new `high` finding.
Set `NEXUS_HOOK=off` to silence it.
