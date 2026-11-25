---
name: jira-acli-operations
description: Complete protocol for all acli Jira operations — authentication, work items,
    fields, projects, boards, sprints, filters, and dashboards.
category: Atlassian Jira
---

# Jira acli Operations Skill

> **Skill ID:** `jira-acli-operations`<br>
> **Version:** 2.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

Comprehensive reference for all `acli jira` operations — authentication, work
item CRUD, comments, links, attachments, watchers, fields, projects, boards,
sprints, filters, and dashboards.

***

## Environment & Dependencies

### 1.1 Required Tool

| Tool | Verification | Installation |
| :--- | :--- | :--- |
| `acli` | `which acli` | `brew install acli` or
`npm install -g @atlassian/cli` |

### 1.2 Authentication Verification

Verify authentication before any operation:

```bash
acli jira auth status
```

Expected output: `✓ Authenticated` with the site name.

> **Note:** `acli jira workitem list --max 1` does NOT exist in current acli
> versions — the auth check above is the reliable form.

If not authenticated, follow the [auth login](#221-login) procedure.

***

## Authentication (`acli jira auth`)

### 2.1.1 Login

```bash
# Web browser OAuth (recommended)
acli jira auth login --web

# API token (headless)
acli jira auth login \
  --site "mysite.atlassian.net" \
  --email "user@atlassian.com" \
  --token < token.txt
```

### 2.1.2 Status

```bash
acli jira auth status
```

### 2.1.3 Switch Account

```bash
# Interactive
acli jira auth switch

# By site and/or email
acli jira auth switch --site mysite.atlassian.net --email user@atlassian.com
```

### 2.1.4 Logout

```bash
acli jira auth logout
```

***

## Work Items (`acli jira workitem`)

### 2.2.1 Create

```bash
acli jira workitem create \
  --project "AES" \
  --summary "Implement System Memory on Table Broker Page" \
  --description "$(cat <<'EOF'
h2. Description

h3. PR Link
N/A

h3. Project
System Memory

h3. Epic
Systems Memory
[Epic Link|https://<org>.atlassian.net/browse/AES-53]
EOF
)" \
  --type "Task" \
  --parent "AES-53"
```

| Flag | Purpose | Example |
| :--- | :--- | :--- |
| `--project` | Project key | `AES` |
| `--summary` | Ticket title | `Implement System Memory...` |
| `--description` | Body (plain or ADF) | Heredoc string |
| `--type` | Issue type | `Task`, `Bug`, `Story`, `Epic` |
| `--parent` | Epic parent key | `AES-53` |
| `--assignee` | Assignee email or account ID | `@me` / `default` /
`user@atlassian.com` |
| `--label` | Labels (comma-separated) | `system-memory,frontend` |
| `--from-file` | Read summary/desc from file | `workitem.txt` |
| `--from-json` | Full definition from JSON | `workitem.json` |
| `--editor` | Open interactive editor | |
| `--json` | Output as JSON | |

### 2.2.2 Create Bulk

```bash
# From CSV
acli jira workitem create-bulk --from-csv issues.csv

# From JSON
acli jira workitem create-bulk --from-json issues.json

# Generate JSON template
acli jira workitem create-bulk --generate-json
```

CSV columns: `summary`, `projectKey`, `issueType`, `description`, `label`,
`parentIssueId`, `assignee`.

### 2.2.3 View

```bash
# Default fields
acli jira workitem view AES-940

# Custom fields
acli jira workitem view AES-940 --fields summary,comment,description

# All fields  (the ONLY --fields value that returns custom fields; see §2.2.4a)
acli jira workitem view AES-940 --fields '*all'

# Exclude a field
acli jira workitem view AES-940 --fields '-description'

# Open in web browser
acli jira workitem view AES-940 --web

# JSON output
acli jira workitem view AES-940 --json
```

### 2.2.4 Search

```bash
# By JQL
acli jira workitem search --jql "project = AES AND status = 'In Progress'"

# Paginate all results
acli jira workitem search --jql "project = AES" --paginate

# Count only
acli jira workitem search --jql "project = AES" --count

# With custom fields
# NOTE: `search` never returns custom fields (see §2.2.4a). For a custom field
# value, search by key/summary first, then `view --fields '*all'` per item.
acli jira workitem search --jql "project = AES" --fields "key,summary,assignee"

# By filter ID
acli jira workitem search --filter 10001

# Open in browser
acli jira workitem search --jql "project = AES" --web

# Output formats
acli jira workitem search --jql "project = AES" --json
acli jira workitem search --jql "project = AES" --csv

# Limit results
acli jira workitem search --jql "project = AES" --limit 50
```

### 2.2.4a JQL and `--fields` Pitfalls (read before any custom-field query)

These are the failure modes that silently produce **empty or wrong** results
(and that this skill's examples do not otherwise warn about):

1. **`--fields` with a space-containing name is rejected, and the error is
   misleading.** `acli` strips the space and the parser then complains about a
   field *name* that does not exist:
   ```bash
   acli jira workitem search --jql "project = AES" --fields "Release Status"
   # ✗ Error: field 'ReleaseStatus' is not allowed
   ```
   **Fix:** never pass a spaced field name to `--fields`. Use `'*all'`
   (see §2.2.3) and read the field out of the returned JSON.

2. **`search` NEVER returns custom fields, even with `--fields '*all'`.** A
   field like `Release Status` (customfield_10252) is present on the issue but
   absent from `search` output. Filtering by its value in Python over `search`
   results therefore matches **zero** items. You must fetch each item with
   `view --fields '*all'` to see custom fields.

3. **`*all` is the only `--fields` value that returns custom fields.** Plain
   field lists (even `'*all'` minus one) can omit them; when you need a custom
   field, always use `'*all'`.

4. **JQL field names with spaces must be double-quoted; values containing
   reserved words must be quoted too.** `status`, `not`, `and`, `or`, `for`,
   `in` are reserved. Wrong quoting yields cryptic errors such as
   *"expecting operator but got 'status'"* or *"the character 'for' is a
   reserved jql word"*.
   ```bash
   # correct:
   acli jira workitem search --jql '"Release Status" = "Ready for release"'
   # also works (field name without spaces):
   acli jira workitem search --jql 'Release Status = "Ready for release"'
   ```

5. **Never interpolate JQL into a shell string.** A JQL literal that itself
   contains quotes (e.g. `"Release Status" = "Ready for release"`) is mangled by
   shell/`f-string` quote-nesting, and the resulting error blames the *JQL*,
   not the quoting. Pass the JQL as a single argv element — i.e. call acli via
   a subprocess argument list
   (`["acli","jira","workitem","search","--jql", jql, "--json"]`), exactly as
   `jira-workitem-hierarchy-report/scripts/jira-hierarchy-report.py` does.

6. **`--count` emits a human preamble, not pure JSON.** Its stdout is
   `Number of work items in the search: <n>` — parse from the tail, do not
   `json.loads` it.

7. **`acli jira field` cannot list a field's options** (only create/update/
   delete). To discover the valid option strings of a single-select custom
   field, use the helper script
   `scripts/discover-select-options.py --field "Release Status"`, which probes
   JQL (`IS NOT EMPTY`, `= '<guess>'`, `NOT IN (...)`) and reads the exact
   option text from a `view --fields '*all'` of a straggler.

### 2.2.5 Edit (Update Fields)

```bash
# By key
acli jira workitem edit --key "AES-940" --summary "New Summary"

# By JQL (bulk)
acli jira workitem edit --jql "project = AES" --assignee "user@atlassian.com"

# By filter
acli jira workitem edit --filter 10001 --description "Updated" --yes
```

| Flag | Purpose | Example |
| :--- | :--- | :--- |
| `-s, --summary` | Update summary | `"New Summary"` |
| `-d, --description` | Update description (plain/ADF) | `"New desc"` |
| `--description-file` | Read description from file | `desc.txt` |
| `-a, --assignee` | Assignee email/ID | `@me` / `default` |
| `--remove-assignee` | Clear assignee | |
| `-l, --labels` | Set labels | `bug,frontend` |
| `--remove-labels` | Remove labels | `bug` |
| `-t, --type` | Change issue type | `Bug` |
| `--ignore-errors` | Continue on error | |
| `--from-json` | Edit from JSON file | |
| `--json` | Output as JSON | |
| `-y, --yes` | Skip confirmation | |

### 2.2.6 Transition (Change Status)

```bash
# By key
acli jira workitem transition --key "AES-940" --status "Done"

# By JQL (bulk)
acli jira workitem transition --jql "project = AES" --status "In Progress"

# By filter
acli jira workitem transition --filter 10001 --status "To Do" --yes
```

### 2.2.7 Assign

```bash
# Self-assign
acli jira workitem assign --key "AES-940" --assignee "@me"

# Assign to user
acli jira workitem assign --jql "project = AES" --assignee "user@atlassian.com"

# Assign to project default
acli jira workitem assign --filter 10001 --assignee "default"

# Bulk assign from file
acli jira workitem assign --from-file "issues.txt" --remove-assignee --json
```

### 2.2.8 Clone

```bash
# Clone to same project
acli jira workitem clone --key "AES-940"

# Clone to different project
acli jira workitem clone --key "AES-940" --to-project "OTHER"

# Bulk clone by JQL
acli jira workitem clone --jql "project = AES" --to-project "OTHER"

# Clone from file
acli jira workitem clone --from-file "issues.txt" --to-site "other.atlassian.net"
```

### 2.2.9 Archive / Unarchive

```bash
# Archive by key
acli jira workitem archive --key "AES-940"

# Archive by JQL
acli jira workitem archive --jql "project = AES AND status = Done"

# Archive from file
acli jira workitem archive --from-file "issues.txt" --yes

# Unarchive
acli jira workitem unarchive --key "AES-940"
acli jira workitem unarchive --from-file "issues.txt" --yes
```

### 2.2.10 Delete

```bash
acli jira workitem delete --key "AES-940"
acli jira workitem delete --jql "project = OLD"
acli jira workitem delete --filter 10001 --yes
acli jira workitem delete --from-file "issues.txt" --yes
```

### 2.2.11 Comments

> **Note on inlineCard (rich link) format**: The `acli` CLI produces only
> plain-text comments. To create Jira comments with **inlineCard** rendering
> (embedded PR cards via `[url|url|smart-link]` wiki markup), use the
> [`jira-inlinecard-comment`](../jira-inlinecard-comment/SKILL.md) base skill
> instead — it calls the Jira REST API v2 directly.

#### Create Comment

```bash
# By key
acli jira workitem comment create --key "AES-940" --body "Comment text"

# By JQL
acli jira workitem comment create \
  --jql "key = AES-940" \
  --body "https://github.com/org/repo/pull/574"

# From file
acli jira workitem comment create --jql "key = AES-940" --body-file comment.txt

# Edit last comment from same author
acli jira workitem comment create --key "AES-940" --body "Updated" --edit-last

# Interactive editor
acli jira workitem comment create --key "AES-940" --editor
```

#### List Comments

```bash
acli jira workitem comment list --key AES-940
acli jira workitem comment list --key AES-940 --json
acli jira workitem comment list --key AES-940 --limit 100 --order "-created"
acli jira workitem comment list --key AES-940 --paginate
```

#### Update Comment

```bash
acli jira workitem comment update \
  --key AES-940 \
  --id 10001 \
  --body "Updated comment text"

# From file
acli jira workitem comment update \
  --key AES-940 --id 10001 --body-file comment.txt

# With visibility
acli jira workitem comment update \
  --key AES-940 --id 10001 \
  --body "Internal" --visibility-role "Administrators"

acli jira workitem comment update \
  --key AES-940 --id 10001 \
  --body "Team update" --visibility-group "dev-team" --notify
```

#### Delete Comment

```bash
acli jira workitem comment delete --key AES-940 --id 10023
```

#### Comment Visibility Options

```bash
# List project roles
acli jira workitem comment visibility --role --project AES

# List groups
acli jira workitem comment visibility --group
```

### 2.2.12 Links

#### Create Link

```bash
acli jira workitem link create --out AES-940 --in AES-941 --type "Blocks"

# From CSV (columns: outward, inward, type; first row is header)
acli jira workitem link create --from-csv links.csv

# From JSON
acli jira workitem link create --from-json links.json

# Generate JSON template
acli jira workitem link create --generate-json
```

#### List Links

```bash
acli jira workitem link list --key AES-940
acli jira workitem link list --key AES-940 --json
```

#### Delete Link

```bash
acli jira workitem link delete --id 10001
acli jira workitem link delete --from-json links.json
acli jira workitem link delete --from-csv links.csv
```

#### List Link Types

```bash
acli jira workitem link type
acli jira workitem link type --json
```

### 2.2.13 Attachments

```bash
# List
acli jira workitem attachment list --key AES-940
acli jira workitem attachment list --key AES-940 --json

# Delete
acli jira workitem attachment delete --id 12345
```

### 2.2.14 Watchers

```bash
# List
acli jira workitem watcher list --key AES-940
acli jira workitem watcher list --key AES-940 --json

# Remove
acli jira workitem watcher remove --key AES-940 --user "5b10ac8d82e05b22cc7d4ef5"
```

***

## Fields (`acli jira field`)

### 2.3.1 Create Custom Field

```bash
# Text field
acli jira field create \
  --name "Customer Name" \
  --type "com.atlassian.jira.plugin.system.customfieldtypes:textfield"

# Select field with searcher
acli jira field create \
  --name "Priority Level" \
  --type "com.atlassian.jira.plugin.system.customfieldtypes:select" \
  --searcher-key "com.atlassian.jira.plugin.system.customfieldtypes:multiselectsearcher"

# Date picker with description
acli jira field create \
  --name "Release Date" \
  --type "com.atlassian.jira.plugin.system.customfieldtypes:datepicker" \
  --description "The planned release date for this feature"
```

### 2.3.2 Update Field

```bash
acli jira field update \
  --id customfield_12345 \
  --name "New Name" \
  --description "Updated description"

# From JSON
acli jira field update --id customfield_12345 --from-json field-update.json
```

### 2.3.3 Delete / Restore Field

```bash
# Delete (moves to trash)
acli jira field delete --id customfield_12345

# Restore from trash
acli jira field cancel-delete --id customfield_12345
```

***

## Projects (`acli jira project`)

### 2.4.1 List

```bash
acli jira project list
acli jira project list --limit 50 --json
acli jira project list --recent
acli jira project list --paginate
```

### 2.4.2 View

```bash
acli jira project view --key AES
acli jira project view --key AES --json
```

### 2.4.3 Create

```bash
# Clone from existing
acli jira project create \
  --from-project "TEMPLATE" \
  --key "NEWPROJ" \
  --name "New Project" \
  --description "Project description" \
  --url "https://example.com" \
  --lead-email "user@atlassian.com"

# From JSON
acli jira project create --from-json project.json
acli jira project create --generate-json
```

### 2.4.4 Update

```bash
acli jira project update \
  --project-key "TEAM1" \
  --key "TEAM" \
  --name "New Name" \
  --description "Updated" \
  --url "https://new.url" \
  --lead-email "newlead@atlassian.com"

# From JSON
acli jira project update --project-key "TEAM1" --from-json project.json
```

### 2.4.5 Archive / Restore / Delete

```bash
acli jira project archive --key "TEAM"
acli jira project restore --key "TEAM"
acli jira project delete --key "TEAM"
```

***

## Boards (`acli jira board`)

### 2.5.1 Search

```bash
acli jira board search
acli jira board search --name "My Board"
acli jira board search --type scrum
acli jira board search --project AES
acli jira board search --limit 100 --paginate --json
```

### 2.5.2 Get Details

```bash
acli jira board get --id 123
acli jira board get --id 123 --json
```

### 2.5.3 Create

```bash
# Scrum board for a project
acli jira board create \
  --name "My Scrum Board" \
  --type scrum \
  --filter-id 10040 \
  --location-type project \
  --project "AES"

# Kanban board
acli jira board create \
  --name "Kanban Board" \
  --type kanban \
  --filter-id 10040 \
  --location-type project \
  --project "PROJ"

# Personal user board
acli jira board create \
  --name "Personal Board" \
  --type scrum \
  --filter-id 10040 \
  --location-type user
```

### 2.5.4 List Sprints / Projects

```bash
# Sprints on a board
acli jira board list-sprints --id 123
acli jira board list-sprints --id 123 --state active,closed
acli jira board list-sprints --id 123 --paginate --json

# Projects on a board
acli jira board list-projects --id 123
acli jira board list-projects --id 123 --paginate --csv
```

### 2.5.5 Delete

```bash
acli jira board delete --id 123
acli jira board delete --id 123,456,789 --yes
```

***

## Sprints (`acli jira sprint`)

### 2.6.1 Create

```bash
# Minimal
acli jira sprint create --name "Sprint 1" --board 5

# With dates and goal
acli jira sprint create \
  --name "Sprint 2" \
  --board 5 \
  --start 2025-01-01 \
  --end 2025-01-14 \
  --goal "Prepare for Q1 release"
```

### 2.6.2 View

```bash
acli jira sprint view --id 123
acli jira sprint view --id 123 --json
```

### 2.6.3 Update

```bash
# Name and goal
acli jira sprint update --id 37 --name "Sprint 1 - Final" --goal "Complete all Q1"

# State
acli jira sprint update --id 37 --state closed

# Dates
acli jira sprint update --id 37 --start "2025-01-01" --end "2025-01-14"
```

### 2.6.4 List Work Items

```bash
acli jira sprint list-workitems --sprint 1 --board 6
acli jira sprint list-workitems --sprint 1 --board 6 --fields "key,summary,status"
acli jira sprint list-workitems --sprint 1 --board 6 --jql "priority = High"
acli jira sprint list-workitems --sprint 1 --board 6 --paginate --json
```

### 2.6.5 Delete

```bash
acli jira sprint delete --id 37
acli jira sprint delete --id 37,42,55 --yes
```

***

## Filters (`acli jira filter`)

### 2.7.1 Search

```bash
acli jira filter search
acli jira filter search --owner "user@atlassian.com" --name "report"
acli jira filter search --limit 50 --json --paginate
```

### 2.7.2 Get

```bash
acli jira filter get --id 12345
acli jira filter get --id 12345 --json
acli jira filter get --id 12345 --web
```

### 2.7.3 List (My / Favourites)

```bash
acli jira filter list --my
acli jira filter list --favourite
acli jira filter list --my --json
```

### 2.7.4 Update

```bash
acli jira filter update \
  --id 10001 \
  --name "My Updated Filter" \
  --description "New description" \
  --jql "project = TEST AND status = Open"

# With share permissions (JSON array)
acli jira filter update --id 10001 --share-permissions '[{"type":"group","groupname":"jira-developers"}]'
```

### 2.7.5 Add Favourite

```bash
acli jira filter add-favourite --filter-id 10001
```

### 2.7.6 Change Owner

```bash
acli jira filter change-owner --id "123,124,125" --owner "newowner@atlassian.com"
acli jira filter change-owner --from-file filter-ids.txt --owner "newowner@atlassian.com"
```

### 2.7.7 Columns

```bash
# Get
acli jira filter get-columns --key FILTER-123
acli jira filter get-columns --key FILTER-123 --json

# Reset
acli jira filter reset-columns --id FILTER-123
```

***

## Dashboards (`acli jira dashboard`)

### 2.8.1 Search

```bash
acli jira dashboard search
acli jira dashboard search --owner "user@atlassian.com" --name "report"
acli jira dashboard search --limit 10 --json --paginate
```

***

## Common Workflows

### 2.9.1 Code Migration → Jira → PR → Comment

1. **Analyze** codebase to identify pages needing migration.
2. **Run** `git status` / `git log` to understand current branch state.
3. **Create** a Jira work item under the epic for each page.
4. **Implement** the code changes.
5. **Create** a Pull Request via `gh pr create`. If `gh` is unavailable, use
   `POST /repos/{owner}/{repo}/pulls` per [GitHub REST API Fallback](../github-rest-api-fallback/SKILL.md) §3.
   If `gh` is installed but `gh auth status` fails, defer to
   [Git / GitHub Auth Fallback](../git-github-auth-fallback/SKILL.md) §3.4 before retrying.
6. **Comment** the PR URL on the Jira ticket:

   ```bash
   acli jira workitem comment create \
     --jql "key = AES-941" \
     --body "https://github.com/org/repo/pull/575"
   ```

### 2.9.2 Bulk Create Tickets Under an Epic

```bash
items=(
  "Summary 1|Description 1"
  "Summary 2|Description 2"
)
for item in "${items[@]}"; do
  IFS='|' read -r summary description <<< "$item"
  acli jira workitem create \
    --project "AES" \
    --summary "$summary" \
    --description "$description" \
    --type "Task" \
    --parent "AES-53"
done
```

### 2.9.3 List All Open Tickets in a Project

```bash
acli jira workitem search \
  --jql "project = AES AND status NOT IN (Done, Closed)" \
  --fields "key,summary,assignee,status,priority" \
  --paginate
```

### 2.9.4 Batch Transition (Move Done Tickets to Closed)

```bash
acli jira workitem transition \
  --jql "project = AES AND status = Done" \
  --status "Closed" \
  --yes
```

***

## SSOT Compliance

| Standard | Rule/Skill | Location |
| :--- | :--- | :--- |
| Git atomic commits | Git Atomic Commit Skill |
[`../git-atomic-commit-construction/SKILL.md`](../git-atomic-commit-construction/SKILL.md) |
| GitHub PR creation | GitHub Workflow Creation |
[`../github-workflow-creation/SKILL.md`](../github-workflow-creation/SKILL.md) |
| Jira hierarchy reports | Jira Work Item Hierarchy Report |
[`../jira-workitem-hierarchy-report/SKILL.md`](../jira-workitem-hierarchy-report/SKILL.md) |
| Markdown linting | Markdown Generation Skill |
[`../markdown-generation/SKILL.md`](../markdown-generation/SKILL.md) |
| Skill metadata structure | Skill Factory Skill |
[`../skill-factory/SKILL.md`](../skill-factory/SKILL.md) |

***

## Related Conversations & Traceability

| Session | Date | Context |
| :--- | :--- | :--- |
| Jira acli skill creation | 2026-05-08 | Created from AES-940/941/942
migration session; comprehensive acli Jira reference |
