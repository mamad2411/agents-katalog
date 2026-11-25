---
name: codebase-intel
description: Gives the agent the recorded "why" behind a codebase before it changes it, and records new whys as it makes decisions, through the codebase-intel MCP server. Use at the start of any coding session in a repo with a .codebase-intel/ directory, before making a structural choice (new module, library or algorithm pick, architecture boundary, reversing earlier work), after making one, and when the user asks why some code exists, what breaks if a file changes, or which rules a file must follow.
license: MIT
compatibility: Requires the codebase-intel MCP server (pip install codebase-intel, v0.3.0 or later) registered with the agent, and a repo initialized with `codebase-intel init`. Works with any MCP-capable agent.
---

# codebase-intel

codebase-intel keeps a committed, journal-backed **intent graph** of why the code is the way it is, plus a code graph and quality contracts. Use it so you don't re-decide things the team already decided, and so the next session inherits what you decided in this one.

## Setup check

If the `bootstrap`, `check_precedent`, `record_why` and `get_intent` tools aren't available, the server isn't connected. Tell the user how to connect it rather than guessing:

```bash
pip install -U codebase-intel
codebase-intel init .            # once per repo
codebase-intel intent-migrate    # if the repo has v1 decision records
```

```json
{ "mcpServers": { "codebase-intel": { "command": "codebase-intel", "args": ["serve", "."] } } }
```

For many repos: `codebase-intel register <path>` for each, then serve with `["serve", "--auto"]`.

## The loop

### 1. Start the session with `bootstrap`

Call `bootstrap(task="<what the user asked for>")` **before** reading files. It returns system orientation plus the whys relevant to the task within a token budget (default 4000; raise `budget_tokens` for broad tasks). Read files only for what it can't answer.

### 2. Before a structural choice, call `check_precedent`

Call it before you add a module, pick a library or algorithm, move an architecture boundary, or undo existing work. Pass `query` (what you're about to decide) and `files` (what you'll touch).

- **Active precedent:** follow it, or tell the user plainly that you're proposing to overturn it and why.
- **Superseded precedent:** the team tried that and changed course. Don't silently repeat it.
- **Nothing found:** proceed. Then record your decision (step 3).

### 3. After a structural decision, call `record_why`

Record it when you make it, not at the end of the session:

| Field | What to put |
|---|---|
| `title` | Short name, e.g. "Token bucket for rate limiting" |
| `why` | Constraints, alternatives rejected, trade-off taken. Not a restatement of the code. |
| `level` | 0 system topology · 1 service/module · 2 component/flow · 3 function/decision (default) |
| `files` | The files or directories the decision anchors to |
| `supersedes` | Node ID of the decision this replaces, if any |
| `parent_id` | Higher-level node it belongs under, if known |

Don't record trivial edits such as renames, formatting, or bug fixes that don't change a design. The pre-commit gate (`codebase-intel install-hooks`) flags structural changes that have no recorded why, so skipping step 3 surfaces as a warning at commit time.

### 4. Answering "why does this exist?"

- `get_intent(file="<path>")` returns every why anchored to a file.
- `get_intent(node_id="<id>")` returns one node with its parents and children.
- `get_intent(level=0)` returns the system-level picture.
- `get_intent()` with no arguments returns coverage stats.

## Other tools worth using

- `impact_analysis` before changing a widely imported file ("what breaks?").
- `get_contracts` for the files you're editing, then follow those rules.
- `get_context` when you need files, decisions, and contracts assembled together within a budget.
- `check_drift` before trusting an old decision on code that has moved a lot.

## Trust tiers

Every why carries a tier. Say which one you're relying on when it matters:

- `confirmed`: a human reviewed it. Treat it as a team decision.
- `asserted`: an agent recorded it. Treat it as strong context, not law.
- `derived` / `mined`: inferred from code or git history. Verify before relying on it.

Whys you record are `asserted`. A human promotes them with `codebase-intel intent-confirm <node-id>`. Never claim a why is confirmed when it isn't.

## When the server is unavailable

Don't stop work. Fall back to reading the code. If the CLI is installed, a human or agent can still record a decision with:

```bash
codebase-intel why "<title>" "<reason>" -f <file>
```

Tell the user that context came from files rather than the intent graph, so they know it may be missing recorded decisions.
