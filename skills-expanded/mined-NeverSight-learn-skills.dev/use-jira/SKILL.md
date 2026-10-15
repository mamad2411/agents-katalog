---
name: use-jira
description: Manages Jira issues, epics, sprints, and boards using the jira CLI (ankitpokhrel/jira-cli). Use when creating, viewing, editing, searching, or transitioning Jira issues, managing epics, or working with sprints and boards.
compatibility: Requires jira-cli (ankitpokhrel/jira-cli) via brew
---

# use-jira

## Essential Principles

- **Epic commands are separate from issue commands.** `jira epic create`, `jira epic add`, `jira epic remove`, `jira epic list` — do NOT use `jira issue create -tEpic` or `jira issue link` for epic operations.
- **Stdin descriptions use `--template -`** (not `--body-template` or `--stdin`). For `issue edit`, pipe to stdin with `--no-input` instead.
- **Use shorthand filter flags** (`-t`, `-s`, `-a`, `-y`, `-l`, `-P`) for `issue list` instead of raw JQL when possible. Reserve `-q`/`--jql` for complex queries.
- **`$(jira me)` for current user.** Use in `-a$(jira me)` for assignee, not `currentUser()` (that's JQL-only syntax).
- **Negate filters with `~` prefix.** `-s~Done` means "not Done". Use `-ax` for unassigned.
- **Quote heredoc delimiters** (`'EOF'`) to prevent shell variable expansion in descriptions.
- **No interactive flags.** Never use `-i` or interactive prompts — use `--no-input` to skip prompts.
- **`--plain` for scripting.** Use `--plain` output when parsing results or piping to other commands.
- **Custom fields use field name, not ID.** `--custom field-name="value"`, not `--custom customfield_10001="value"`. View available custom fields in `jira init` config output.

## Prerequisites

```bash
command -v jira >/dev/null 2>&1
```

If not found: `brew tap ankitpokhrel/jira-cli && brew install jira-cli`. Then configure: `jira init`.

Verify authentication:

```bash
jira me
```

If `jira me` fails: run `jira init` to configure. Set default project via `jira init` or use `-p PROJECT_KEY` per command.

## Quick Start

```bash
jira issue create -tStory -s"Summary" -PPARENT-KEY --custom field-name="value" --template -
jira issue view PROJ-123
jira issue list -a$(jira me) -s~Done --plain
jira issue move PROJ-123 "In Progress"
jira epic create -n"Epic Name" -s"Summary" -yHigh
jira epic list EPIC-KEY --plain
jira sprint list --current --plain
```

## Issues

### Create

```bash
jira issue create -tStory -s"Summary" -PPARENT-KEY --custom field-name="value" --template -
```

| Flag | Purpose |
|------|---------|
| `-t, --type` | Issue type: `Story`, `Bug`, `Spike`, `Task` |
| `-s, --summary` | Title |
| `-P, --parent` | Parent issue key (epic or parent task) |
| `-b, --body` | Inline description (takes precedence over `--template`) |
| `-T, --template` | Read description from file; use `-` for stdin |
| `-a, --assignee` | Assignee (username, email, or display name) |
| `-y, --priority` | Priority level |
| `-l, --label` | Labels (repeatable) |
| `-C, --component` | Components (repeatable) |
| `--custom` | Custom fields: `--custom field-name="value"` |
| `--no-input` | Skip interactive prompts |
| `--web` | Open in browser after creation |
| `--raw` | Print JSON output |

**Description from stdin (heredoc):**

```bash
cat << 'EOF' | jira issue create -tStory -s"Summary" -PPARENT-KEY --custom field-name="value" --template -
## Description
Content here
EOF
```

### View

```bash
jira issue view PROJ-123
jira issue view PROJ-123 --plain
```

### Edit

```bash
jira issue edit PROJ-123 -s"New summary"
jira issue edit PROJ-123 --custom field-name="value"
jira issue edit PROJ-123 --label "frontend" --label "urgent"
jira issue edit PROJ-123 --label -old-label           # remove label (minus prefix)
jira issue edit PROJ-123 -PNEW-PARENT --no-input      # change parent
```

**Edit description from stdin:**

```bash
cat << 'EOF' | jira issue edit PROJ-123 --no-input
Updated description content
EOF
```

### Transition (Move)

To see available transitions: `jira issue view PROJ-123` (transitions listed at bottom).

```bash
jira issue move PROJ-123 "In Progress"
jira issue move PROJ-123 Done -RFixed                           # with resolution
jira issue move PROJ-123 "In Progress" -a$(jira me) --comment "Starting"
```

Aliases: `transition`, `mv`

### Comment

```bash
jira issue comment add PROJ-123 "Comment text"
jira issue comment add PROJ-123 "Internal note" --internal    # visible to project members only
```

**Multi-line comment:**

```bash
jira issue comment add PROJ-123 "$(cat << 'EOF'
## Update
- Completed task A
- Blocked on B
EOF
)"
```

### Assign

```bash
jira issue assign PROJ-123 "user@example.com"
jira issue assign PROJ-123 $(jira me)
```

### Link / Unlink

```bash
jira issue link PROJ-123 PROJ-456 "Blocks"
jira issue unlink PROJ-123 PROJ-456
```

| Link Type | Meaning |
|-----------|---------|
| `Blocks` | This issue blocks another |
| `is blocked by` | This issue is blocked by another |
| `relates to` | General relationship |
| `duplicates` | Duplicate of another |

### Search (List)

```bash
jira issue list -a$(jira me) -tBug -s~Done -yHigh --created -7d --plain
```

| Flag | Purpose | Examples |
|------|---------|----------|
| `-a` | Assignee | `-a$(jira me)`, `-ax` (unassigned), `-a"Name"` |
| `-t` | Type | `-tBug`, `-tStory` |
| `-s` | Status | `-s"In Progress"`, `-s~Done` (negate with `~`) |
| `-y` | Priority | `-yHigh` |
| `-l` | Label | `-lurgent` (repeatable) |
| `-P` | Parent/epic | `-PEPIC-123` |
| `-q` | Raw JQL | `-q"project = PROJ AND assignee = currentUser() AND status != Done"` |
| `--created` | Created date | `today`, `week`, `month`, `-7d`, `-4w` |
| `--updated` | Updated date | Same formats as `--created` |
| `--paginate` | Pagination | `20` (limit), `10:50` (offset:limit) |

**Output formats:**

| Flag | Format |
|------|--------|
| `--plain` | Plain text table |
| `--plain --columns key,summary,status` | Specific columns |
| `--plain --no-headers` | No headers |
| `--raw` | JSON |
| `--csv` | CSV |

Aliases: `lists`, `ls`, `search`

### Other Issue Operations

| Operation | Command |
|-----------|---------|
| Clone issue | `jira issue clone PROJ-123` |
| Delete issue | `jira issue delete PROJ-123` |
| Watch issue | `jira issue watch PROJ-123` |
| Open in browser | `jira open PROJ-123` |
| Attachments | Jira UI or REST API (not supported by CLI) |

## Epics

**Epics have their own command group.** Do NOT use `jira issue` commands for epic-specific operations.

### Create Epic

```bash
jira epic create -n"Epic Name" -s"Summary" -yHigh -b"Description"
```

| Flag | Purpose |
|------|---------|
| `-n, --name` | Epic name (required) |
| `-s, --summary` | Epic summary/title |
| `-b, --body` | Description |
| `-y, --priority` | Priority |
| `-a, --assignee` | Assignee |
| `-l, --label` | Labels (repeatable) |
| `--custom` | Custom fields |
| `--no-input` | Skip prompts |

### List Epics / Epic Issues

```bash
jira epic list                                    # list all epics
jira epic list --table --plain                    # epics in plain table
jira epic list PROJ-50 --plain --columns type,key,summary,status   # issues in epic
```

### Add Issues to Epic

```bash
jira epic add EPIC-KEY ISSUE-1 ISSUE-2           # max 50 issues
```

### Remove Issues from Epic

```bash
jira epic remove ISSUE-1 ISSUE-2
```

### View Epic

```bash
jira epic view EPIC-KEY
```

## Board & Sprint

### Board

```bash
jira board list                                   # list boards in project
jira board list -pPROJ                            # list boards in specific project
```

Aliases: `boards`

### Sprint List

```bash
jira sprint list                                  # top 50 sprints (interactive)
jira sprint list --state active --plain           # active sprints only
jira sprint list --current --plain                # current active sprint issues
jira sprint list --prev --plain                   # previous sprint issues
jira sprint list --next --plain                   # next planned sprint issues
jira sprint list SPRINT_ID --plain --columns type,key,summary,status
```

| Flag | Purpose |
|------|---------|
| `--state` | Filter: `future`, `active`, `closed` (comma-separated) |
| `--current` | Current active sprint issues |
| `--prev` | Previous sprint issues |
| `--next` | Next planned sprint issues |
| `--table` | Table view |
| `--plain` | Plain text output |
| `--columns` | Sprint: `ID,NAME,START,END,COMPLETE,STATE`. Issues: `TYPE,KEY,SUMMARY,STATUS,...` |

### Sprint Add

```bash
jira sprint add SPRINT_ID ISSUE-1 ISSUE-2        # max 50 issues
```

### Sprint Close

```bash
jira sprint close SPRINT_ID
```

## Useful Flags (Global)

| Flag | Purpose |
|------|---------|
| `-p, --project` | Project key (overrides configured default) |
| `-c, --config` | Config file path |
| `--debug` | Debug output |

## Success Criteria

- Correct command group used (epic commands for epic ops, issue commands for issue ops)
- `--template -` used for stdin descriptions on create, `--no-input` for edit
- Shorthand filter flags preferred over raw JQL where possible
- No interactive flags (`-i`) used
- User confirmed before any mutation (create, edit, move, delete)
