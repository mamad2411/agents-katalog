---
name: herdr-background-shell
description: Use when running long-lived commands, servers, watchers, build processes, parallel shell tasks, or any background terminal work outside the main Pi session. All background shells live in one named tab with named panes.
---

# Herdr Background Shell

Run shell commands in a dedicated background tab without blocking the master Pi session. Every pane is named. Multiple shells share one tab.

## Precondition

```bash
test "$HERDR_ENV" = 1 || { echo "Not inside Herdr"; exit 1; }
```

## Create Background Tab

One tab per task group. All background shells for that group go here. Never create a tab per shell.

```bash
read -r WORKSPACE MASTER_PANE < <(
  herdr pane list | python3 -c '
import json, sys
for pane in json.load(sys.stdin)["result"]["panes"]:
    if pane["focused"]:
        print(pane["workspace_id"], pane["pane_id"])
        break
else:
    raise SystemExit("No focused master pane")'
)

BG_SLUG="<short-descriptive-slug>"         # e.g. "dev-server", "build-watch"
BG_LABEL="bg-$BG_SLUG"
TAB_RESULT=$(herdr tab create --workspace "$WORKSPACE" --label "$BG_LABEL" --no-focus)
BG_TAB=$(printf '%s' "$TAB_RESULT" | python3 -c 'import json,sys; print(json.load(sys.stdin)["result"]["tab"]["tab_id"])')
BG_ROOT_PANE=$(printf '%s' "$TAB_RESULT" | python3 -c 'import json,sys; print(json.load(sys.stdin)["result"]["root_pane"]["pane_id"])')
```

## Name and Use First Shell

Every pane must be named before use. Name describes what runs there.

```bash
BG_PANE="$BG_ROOT_PANE"
herdr pane rename "$BG_PANE" "bg-$BG_SLUG-1"
herdr pane run "$BG_PANE" "cd '$PWD'"
```

Then run a command:

```bash
herdr pane run "$BG_PANE" "npm run dev"
# or send without immediate Enter, then send keys:
herdr pane send-text "$BG_PANE" "cargo watch -x test"
herdr pane send-keys "$BG_PANE" Enter
```

## Add More Shells

When a second background shell is needed, split from root pane `right`, split from new right pane `down` for third, always alternating direction so layout stays balanced. All shells share the same `BG_TAB`.

```bash
# Second shell: split existing pane right
NEW_PANE=$(herdr pane split "$BG_PANE" --direction right --no-focus \
  | python3 -c 'import json,sys; print(json.load(sys.stdin)["result"]["pane"]["pane_id"])')
BG_PANE="$NEW_PANE"
herdr pane rename "$BG_PANE" "bg-$BG_SLUG-2"
herdr pane run "$BG_PANE" "cd '$PWD'"

# Third shell: split newest pane down
NEW_PANE=$(herdr pane split "$BG_PANE" --direction down --no-focus \
  | python3 -c 'import json,sys; print(json.load(sys.stdin)["result"]["pane"]["pane_id"])')
BG_PANE="$NEW_PANE"
herdr pane rename "$BG_PANE" "bg-$BG_SLUG-3"
herdr pane run "$BG_PANE" "cd '$PWD'"
```

Keep a running list of pane IDs in an array so you can target them later:

```bash
BG_PANES=("$BG_ROOT_PANE")
# after each split:
BG_PANES+=("$NEW_PANE")
```

## Run Commands in a Specific Shell

```bash
herdr pane run "bg-$BG_SLUG-1" "echo hello"
herdr pane send-text "bg-$BG_SLUG-2" "make test"
herdr pane send-keys "bg-$BG_SLUG-2" Enter
```

## Read Output

```bash
herdr pane read "bg-$BG_SLUG-1" --source recent --lines 40
herdr pane read "bg-$BG_SLUG-2" --source recent-unwrapped --lines 80
```

## Wait for Output

```bash
herdr wait output "bg-$BG_SLUG-1" --match "ready" --timeout 60000
```

## Clean Up

When background shells are no longer needed, close all at once:

```bash
herdr tab close "$BG_TAB"
```

If you didn't keep `BG_TAB`, find it:

```bash
herdr tab list --workspace "$WORKSPACE" | python3 -c '
import json, sys
for tab in json.load(sys.stdin)["result"]["tabs"]:
    if tab["label"] == "'"$BG_LABEL"'":
        print(tab["tab_id"])
'
```

## Constraints

| Rule                   | Enforcement                                                      |
| ---------------------- | ---------------------------------------------------------------- |
| One tab per task group | `tab create --workspace "$WORKSPACE" --label "bg-$BG_SLUG"` once |
| Named panes            | `pane rename` before any command                                 |
| Master stays focused   | `--no-focus` on tab create and split                             |
| All shells simple      | Plain zsh/bash/fish shell, not Pi                                |
| Clean up when done     | `tab close "$BG_TAB"` after task group complete                  |

## Examples

### Dev server with file watcher

```bash
BG_SLUG="dev"
TAB_RESULT=$(herdr tab create --workspace "$WORKSPACE" --label "bg-dev" --no-focus)
BG_TAB=$(printf '%s' "$TAB_RESULT" | python3 -c 'import json,sys; print(json.load(sys.stdin)["result"]["tab"]["tab_id"])')
ROOT=$(printf '%s' "$TAB_RESULT" | python3 -c 'import json,sys; print(json.load(sys.stdin)["result"]["root_pane"]["pane_id"])')

herdr pane rename "$ROOT" "bg-dev-server"
herdr pane run "$ROOT" "npm run dev"

SPLIT=$(herdr pane split "$ROOT" --direction right --no-focus | python3 -c 'import json,sys; print(json.load(sys.stdin)["result"]["pane"]["pane_id"])')
herdr pane rename "$SPLIT" "bg-dev-watcher"
herdr pane run "$SPLIT" "npm run watch:css"

herdr wait output "$ROOT" --match "ready" --timeout 30000
herdr pane read "$ROOT" --source recent --lines 20

# Later: clean up
herdr tab close "$BG_TAB"
```

### Parallel test runners

```bash
BG_SLUG="tests"
TAB_RESULT=$(herdr tab create --workspace "$WORKSPACE" --label "bg-tests" --no-focus)
BG_TAB=$(printf '%s' "$TAB_RESULT" | python3 -c 'import json,sys; print(json.load(sys.stdin)["result"]["tab"]["tab_id"])')
P1=$(printf '%s' "$TAB_RESULT" | python3 -c 'import json,sys; print(json.load(sys.stdin)["result"]["root_pane"]["pane_id"])')
herdr pane rename "$P1" "bg-tests-unit"
herdr pane run "$P1" "npm test -- --watch"

P2=$(herdr pane split "$P1" --direction right --no-focus | python3 -c 'import json,sys; print(json.load(sys.stdin)["result"]["pane"]["pane_id"])')
herdr pane rename "$P2" "bg-tests-integration"
herdr pane run "$P2" "npm run test:integration"

# Check results later
herdr pane read "$P1" --source recent --lines 50
herdr pane read "$P2" --source recent --lines 50
herdr tab close "$BG_TAB"
```

### Background process with output check

```bash
BG_SLUG="migration"
TAB_RESULT=$(herdr tab create --workspace "$WORKSPACE" --label "bg-migration" --no-focus)
BG_TAB=$(printf '%s' "$TAB_RESULT" | python3 -c 'import json,sys; print(json.load(sys.stdin)["result"]["tab"]["tab_id"])')
P1=$(printf '%s' "$TAB_RESULT" | python3 -c 'import json,sys; print(json.load(sys.stdin)["result"]["root_pane"]["pane_id"])')
herdr pane rename "$P1" "bg-migration-run"
herdr pane run "$P1" "npm run db:migrate"
herdr wait output "$P1" --match "migration complete" --timeout 120000
herdr pane read "$P1" --source recent --lines 30
herdr tab close "$BG_TAB"
```
