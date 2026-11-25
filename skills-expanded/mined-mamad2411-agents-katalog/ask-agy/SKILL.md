---
name: ask-agy
description: Asks Antigravity CLI for coding assistance. Use for getting a second opinion, code generation, debugging, or delegating coding tasks.
allowed-tools: Bash(agy *)
---

# Ask Antigravity

Executes the local `agy` CLI (Antigravity) to get coding assistance.

**Note:** This skill requires the `agy` CLI to be installed and available in your system's PATH. If `agy` is missing, run `agy install` to configure shell paths. (Antigravity also ships an IDE binary named `antigravity` — that is the editor, not the CLI. Do not invoke `antigravity` as a CLI fallback.)

## Quick start

Run a single query with `-p` (non-interactive print mode):

```bash
agy -p "Your question or task here"
```

## Common options

| Option | Description |
|--------|-------------|
| `-p`, `--print`, `--prompt` | Non-interactive mode (required for scripting) |
| `-c`, `--continue` | Continue the most recent conversation |
| `--conversation <id>` | Resume a previous conversation by ID |
| `-i`, `--prompt-interactive` | Run an initial prompt interactively and continue the session |
| `--dangerously-skip-permissions` | Auto-approve all tool permission requests without prompting |
| `--sandbox` | Run in a sandbox with terminal restrictions enabled |
| `--add-dir <path>` | Add a directory to the workspace (repeatable) |
| `--print-timeout <duration>` | Timeout for print mode wait (default `5m0s`) |

> For all available options and subcommands (`changelog` / `install` / `plugin` / `update`), run `agy --help`.

## Examples

**Ask a coding question:**

```bash
agy -p "How do I implement a binary search in Python?"
```

**Continue the most recent session:**

```bash
agy -c "Now add error handling to that function"
```

**Resume a specific conversation by ID:**

```bash
agy --conversation <conversation-id> "Refine the previous answer"
```

**Let Antigravity make changes automatically:**

```bash
agy --dangerously-skip-permissions -p "Refactor this function to use async/await"
```

**Run in sandbox mode:**

```bash
agy --sandbox -p "Experiment with a new approach to this problem"
```

## Notes

- The `-p` flag runs Antigravity non-interactively and outputs the result to stdout
- Authentication and shell paths are configured via `agy install`; refer to `agy --help` for details
- `--dangerously-skip-permissions` bypasses all tool permission prompts — use with care
- The command inherits the current working directory
