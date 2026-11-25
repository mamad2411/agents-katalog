---
name: projects-v2
description: "Reads and writes GitHub Projects v2 boards with gh project or GraphQL: the Status field, item lists, adding issues. Use when a board carries issue status, a sweep must read every board item, or gh reports a missing project scope. Not for labels or parents (use backlog-hygiene-github)."
allowed-tools: Bash(gh auth status), Bash(gh project list *), Bash(gh project view *), Bash(gh project field-list *), Bash(gh project item-list *), Bash(gh issue view *)
license: MIT
---

# Projects v2

A board's single-select Status field holds exactly one value per item, so it cannot carry the
conflicting states that labels can. `backlog-hygiene-github` covers choosing between labels and a
board; this skill is the calls. Reads are pre-approved; adding items and setting fields ask first.

The `gh project` commands cover most work. Raw GraphQL (node ids, paging, mutations, cost) is in
[references/graphql.md](references/graphql.md), for what they do not expose.

## Access and scope

`gh auth login` does not request the `project` scope, so check `gh auth status` first. If neither
`project` nor `read:project` is listed, stop and ask the user to add it in their own terminal
(`gh auth refresh -s project`, or `-s read:project` for a read-only sweep). It opens a browser,
so do not run it from an agent session. The org GitHub App does not hold a Projects permission,
so an unattended run cannot use it here; say so and ask the owner rather than widening the App.

The error without the scope names it
(`missing required scopes [read:project]`, or "The 'projectV2' field requires one of the following
scopes"): the command is right and the token is not, so leave the command alone. On an
organization board with the scope present, `Resource not accessible` usually means the token still
needs SSO authorization for that organization.

Without `gh`: the GitHub MCP server's `projects` toolset (not in its default set) has
`projects_list`, `projects_get` and `projects_write` (`add_project_item`, and `update_project_item`
with `updated_field: {"name": "Status", "value": "<option>"}`). With neither, ask for the output of
`gh project item-list … --format json` and print the edits for the user to run.

## Step 1: Find the board

```bash
gh project list --owner <owner> --format json --jq '.projects[] | "\(.number)\t\(.title)"'
```

Closed projects are hidden unless `--closed` is passed; a closed board is not a place for new work.

## Step 2: Map the Status options to core states

```bash
gh project field-list 7 --owner <owner> --format json \
  --jq '.fields[] | select(.name == "Status") | {id, options: [.options[] | {id, name}]}'
```

Map every option onto one of the seven core states in the Status mapping of the project's
`## Issue tracker` section (`issue-tracker-core:tracker-discipline`, rules 2 and 4). A board with
only "Todo / In Progress / Done" folds `backlog` into `ready` and `in-review` into `in-progress`,
and has nothing for `parked` or `declined`. Either add the missing options or record how each
missing state is carried, so nobody reads more into "In Progress" than it says.

Option ids change when someone edits the field. Read them in the same run that uses them rather
than storing them in a skill, config file or memory note.

## Step 3: Read every item

```bash
gh project item-list 7 --owner <owner> --limit 1000 --format json \
  --jq '"read \(.items | length) of \(.totalCount)", (.items[] | "\(.content.number // "draft")\t\(.status // "no status")\t\(.content.title)")'
```

Field values appear under camel-cased field names (`status`, `priority`). When "read N of M" shows
N below M, raise `--limit`; a sweep over a partial board reports a clean result that is not.
`--query` filters on the server with the board's filter syntax, for example
`--query "is:issue is:open -status:Done"`.

Sweeps worth running:

- open issues with no Status (`no status` in the output above);
- items whose Status is the `done` option while the issue is still open, or the reverse;
- items in the `in-review` option with no linked pull request (compare with
  `gh issue list --search 'is:open -linked:pr'`).

## Step 4: Add an issue and set its Status

Add at creation, or later (both need the `project` scope; they take the board's title):

```bash
gh issue create --title "<title>" --project "<board title>" --body-file -
gh issue edit 123 --add-project "<board title>"
```

Set the Status by option name:

```bash
gh project item-edit 7 --owner <owner> --url https://github.com/<owner>/<repo>/issues/123 --field Status --value "In Progress"
```

Older `gh` without `--url`/`--field`/`--value` needs the ids: add the item with
`gh project item-add 7 --owner <owner> --url <issue-url> --format json --jq .id` (prints the
`PVTI_…` item id), read the project id with `gh project view 7 --owner <owner> --format json --jq .id`,
then run `gh project item-edit --id <PVTI_…> --project-id <PVT_…> --field-id <PVTSSF_…>
--single-select-option-id <option-id>`, writing each id literally. Versions are in
`issue-lifecycle-github`'s `references/gh-versions.md`.

Clear a field with `gh project item-edit --id <PVTI_…> --project-id <PVT_…> --field-id <field-id> --clear`.

## Examples

<example>
The Status mapping says the board carries state. Issue #123 starts work.
Run `gh project item-edit 7 --owner acme --url https://github.com/acme/api/issues/123 --field
Status --value "In Progress"`, then read it back with `gh issue view 123 --json projectItems`.
Post the start comment with `issue-lifecycle-github`.
</example>

<example>
A weekly sweep prints "read 100 of 342". The result covers under a third of the board. Rerun with
`--limit 1000` before reporting anything.
</example>

## Verify

After a write, read the item back from the issue side:

```bash
gh issue view 123 --json projectItems --jq '.projectItems[] | "\(.title)\t\(.status.name)"'
```

The board title and the Status option you set must both appear. For a sweep, the report includes
"read N of M" with N equal to M.
