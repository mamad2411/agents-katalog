---
name: jira-skills
description: Search and view on-prem Jira issues from the command line using direct REST calls, repo-local config, and OS-native commands on Linux and Windows.
compatibility: Requires on-prem Jira, PAT authentication, repo-root `JIRA_SKILLS.config`, `curl` and `jq` on Linux, and PowerShell on Windows.
metadata:
  author: Tao Lian
  version: "1.0"
---

# Jira Skills

Read on-prem Jira issue data without requiring the standalone `jira` executable. This skill supports only:

- Search/list issues
- View issue details
- Search/list Epics
- Show issues linked to an Epic

This skill is limited to read-only issue discovery, Epic discovery, Epic-linked issue lookup, and detail lookup on on-prem Jira.

## When to Use

- User asks to search for Jira issues in natural language
- User wants a list of recent, assigned, filtered, or project-scoped issues
- User wants to list or search for Epics in a project
- User wants to view the issues linked to a specific Epic
- User wants to view the details for a specific issue key
- User wants plain-text terminal output by default, or JSON output when needed

## Prerequisites

1. Create a repo-root file named `JIRA_SKILLS.config` if it does not already exist.
2. Add the required keys:

```ini
JIRA_BASE_URL=https://jira.example.com
JIRA_PAT=your-personal-access-token
JIRA_PROJECT_KEY=PROJ
```

3. Keep `JIRA_SKILLS.config` out of version control via the repo-root `.gitignore`.
4. On Linux, make sure `curl` and `jq` are available.
5. On Windows, use PowerShell with `Invoke-RestMethod`.

If `JIRA_SKILLS.config` is missing or required keys are empty, stop and ask the user to fix the config before running Jira requests.

## Supported Requests

- "Show my in-progress bugs in PROJ"
- "List recent issues for PROJ"
- "List epics in PROJ"
- "Show recent epics for PROJ"
- "Find open issues assigned to me"
- "View PROJ-123"
- "Show issues in Epic EPIC-123"
- "Show issues in Epic EPIC-123 as JSON"
- "Show PROJ-123 as JSON"

If a request is ambiguous, ask a clarifying question before generating JQL.

## Linux Setup Snippet

```bash
set -a
source ./JIRA_SKILLS.config
set +a
```

## Linux Issue Search

```bash
set -a
source ./JIRA_SKILLS.config
set +a

JQL='project = "'"$JIRA_PROJECT_KEY"'" ORDER BY created DESC'

curl --silent --show-error \
  --header "Authorization: Bearer $JIRA_PAT" \
  --header "Accept: application/json" \
  --get \
  --data-urlencode "jql=$JQL" \
  --data-urlencode "maxResults=20" \
  --data-urlencode "fields=summary,status,assignee" \
  "$JIRA_BASE_URL/rest/api/2/search" \
| jq -r '.issues[] | "\(.key)\t\(.fields.summary)\t\(.fields.status.name)\t\(.fields.assignee.displayName // "Unassigned")"'
```

## Linux Epic Search

```bash
set -a
source ./JIRA_SKILLS.config
set +a

JQL='project = "'"$JIRA_PROJECT_KEY"'" AND issuetype = Epic ORDER BY updated DESC'

curl --silent --show-error \
  --header "Authorization: Bearer $JIRA_PAT" \
  --header "Accept: application/json" \
  --get \
  --data-urlencode "jql=$JQL" \
  --data-urlencode "maxResults=20" \
  --data-urlencode "fields=summary,status" \
  "$JIRA_BASE_URL/rest/api/2/search" \
| jq -r '.issues[] | "\(.key)\t\(.fields.summary)\t\(.fields.status.name)"'
```

```bash
set -a
source ./JIRA_SKILLS.config
set +a

EPIC_KEY="EPIC-123"

curl --silent --show-error \
  --header "Authorization: Bearer $JIRA_PAT" \
  --header "Accept: application/json" \
  "$JIRA_BASE_URL/rest/agile/1.0/epic/$EPIC_KEY/issue?maxResults=20" \
| jq -r '.issues[] | "\(.key)\t\(.fields.summary)\t\(.fields.status.name)\t\(.fields.assignee.displayName // "Unassigned")"'
```

### Translation Notes

- "my in-progress bugs" -> `assignee = currentUser() AND status = "In Progress" AND issuetype = Bug`
- "recent issues in PROJ" -> `project = PROJ ORDER BY created DESC`
- "open issues assigned to me" -> `assignee = currentUser() AND statusCategory != Done ORDER BY updated DESC`
- "list epics in PROJ" -> `project = PROJ AND issuetype = Epic ORDER BY updated DESC`
- "recent epics for PROJ" -> `project = PROJ AND issuetype = Epic ORDER BY created DESC`
- "issues in Epic EPIC-123" -> `GET /rest/agile/1.0/epic/EPIC-123/issue`

If the server cannot resolve `currentUser()` or the request is still ambiguous, ask the user for an explicit assignee, Epic key, or project key.

## Linux Issue View

```bash
set -a
source ./JIRA_SKILLS.config
set +a

ISSUE_KEY="PROJ-123"

curl --silent --show-error \
  --header "Authorization: Bearer $JIRA_PAT" \
  --header "Accept: application/json" \
  "$JIRA_BASE_URL/rest/api/2/issue/$ISSUE_KEY?fields=summary,issuetype,status,priority,assignee,reporter,description" \
| jq -r '"Key: \(.key)\nSummary: \(.fields.summary)\nType: \(.fields.issuetype.name)\nStatus: \(.fields.status.name)\nPriority: \(.fields.priority.name // "None")\nAssignee: \(.fields.assignee.displayName // "Unassigned")\nReporter: \(.fields.reporter.displayName // "Unknown")\nDescription: \(.fields.description // "")"'

echo
echo "Comments:"

curl --silent --show-error \
  --header "Authorization: Bearer $JIRA_PAT" \
  --header "Accept: application/json" \
  "$JIRA_BASE_URL/rest/api/2/issue/$ISSUE_KEY/comment?maxResults=50&orderBy=-created" \
| jq -r '
    if (.comments | length) == 0 then
      "None"
    else
      (.comments
      | map(
          "- \(.author.displayName // "Unknown") | \(.created // "Unknown")\n  \((.body // "") | gsub("\r\n|\r|\n"; "\n  "))"
        )
      | join("\n\n"))
    end'
```

```bash
set -a
source ./JIRA_SKILLS.config
set +a

ISSUE_KEY="PROJ-123"

curl --silent --show-error \
  --header "Authorization: Bearer $JIRA_PAT" \
  --header "Accept: application/json" \
  "$JIRA_BASE_URL/rest/api/2/issue/$ISSUE_KEY"
```

## Windows PowerShell Setup Snippet

```powershell
Get-Content .\JIRA_SKILLS.config | ForEach-Object {
    if ($_ -match '^\s*#' -or $_ -notmatch '=') { return }
    $name, $value = $_ -split '=', 2
    Set-Item -Path "Env:$name" -Value $value
}
```

## Windows Issue Search

```powershell
Get-Content .\JIRA_SKILLS.config | ForEach-Object {
    if ($_ -match '^\s*#' -or $_ -notmatch '=') { return }
    $name, $value = $_ -split '=', 2
    Set-Item -Path "Env:$name" -Value $value
}

$jql = 'project = "' + $env:JIRA_PROJECT_KEY + '" ORDER BY created DESC'
$searchUri = $env:JIRA_BASE_URL + '/rest/api/2/search?jql=' + [uri]::EscapeDataString($jql) + '&maxResults=20&fields=summary,status,assignee'
$headers = @{
    Authorization = "Bearer $($env:JIRA_PAT)"
    Accept = 'application/json'
}

$response = Invoke-RestMethod -Method Get -Uri $searchUri -Headers $headers
$response.issues | ForEach-Object {
    $assignee = if ($null -ne $_.fields.assignee) { $_.fields.assignee.displayName } else { 'Unassigned' }
    '{0}`t{1}`t{2}`t{3}' -f $_.key, $_.fields.summary, $_.fields.status.name, $assignee
}
```

## Windows Epic Search

```powershell
Get-Content .\JIRA_SKILLS.config | ForEach-Object {
    if ($_ -match '^\s*#' -or $_ -notmatch '=') { return }
    $name, $value = $_ -split '=', 2
    Set-Item -Path "Env:$name" -Value $value
}

$jql = 'project = "' + $env:JIRA_PROJECT_KEY + '" AND issuetype = Epic ORDER BY updated DESC'
$searchUri = $env:JIRA_BASE_URL + '/rest/api/2/search?jql=' + [uri]::EscapeDataString($jql) + '&maxResults=20&fields=summary,status'
$headers = @{
    Authorization = "Bearer $($env:JIRA_PAT)"
    Accept = 'application/json'
}

$response = Invoke-RestMethod -Method Get -Uri $searchUri -Headers $headers
$response.issues | ForEach-Object {
    '{0}`t{1}`t{2}' -f $_.key, $_.fields.summary, $_.fields.status.name
}
```

```powershell
Get-Content .\JIRA_SKILLS.config | ForEach-Object {
    if ($_ -match '^\s*#' -or $_ -notmatch '=') { return }
    $name, $value = $_ -split '=', 2
    Set-Item -Path "Env:$name" -Value $value
}

$epicKey = 'EPIC-123'
$searchUri = $env:JIRA_BASE_URL + '/rest/agile/1.0/epic/' + $epicKey + '/issue?maxResults=20'
$headers = @{
    Authorization = "Bearer $($env:JIRA_PAT)"
    Accept = 'application/json'
}

$response = Invoke-RestMethod -Method Get -Uri $searchUri -Headers $headers
$response.issues | ForEach-Object {
    $assignee = if ($null -ne $_.fields.assignee) { $_.fields.assignee.displayName } else { 'Unassigned' }
    '{0}`t{1}`t{2}`t{3}' -f $_.key, $_.fields.summary, $_.fields.status.name, $assignee
}
```

### PowerShell Translation Notes

- Use the same JQL intent mapping as the Linux examples.
- Prefer `currentUser()` in JQL for "my" and "assigned to me" requests.
- Use `issuetype = Epic` for Epic lists.
- Use `GET /rest/agile/1.0/epic/{epicIdOrKey}/issue` for issues in an Epic.
- If the request is missing a clear Epic key or project context, ask a clarifying question.
- If the server does not support the intended lookup cleanly, ask the user for a concrete assignee, Epic key, or issue key.

## Windows Issue View

```powershell
Get-Content .\JIRA_SKILLS.config | ForEach-Object {
    if ($_ -match '^\s*#' -or $_ -notmatch '=') { return }
    $name, $value = $_ -split '=', 2
    Set-Item -Path "Env:$name" -Value $value
}

$issueKey = 'PROJ-123'
$issueUri = $env:JIRA_BASE_URL + '/rest/api/2/issue/' + $issueKey + '?fields=summary,issuetype,status,priority,assignee,reporter,description'
$headers = @{
    Authorization = "Bearer $($env:JIRA_PAT)"
    Accept = 'application/json'
}

$issue = Invoke-RestMethod -Method Get -Uri $issueUri -Headers $headers
$commentUri = $env:JIRA_BASE_URL + '/rest/api/2/issue/' + $issueKey + '/comment?maxResults=50&orderBy=-created'
$commentsResponse = Invoke-RestMethod -Method Get -Uri $commentUri -Headers $headers
$priority = if ($null -ne $issue.fields.priority) { $issue.fields.priority.name } else { 'None' }
$assignee = if ($null -ne $issue.fields.assignee) { $issue.fields.assignee.displayName } else { 'Unassigned' }
$reporter = if ($null -ne $issue.fields.reporter) { $issue.fields.reporter.displayName } else { 'Unknown' }
$comments = if ($null -ne $commentsResponse.comments -and $commentsResponse.comments.Count -gt 0) {
    ($commentsResponse.comments | ForEach-Object {
        $author = if ($null -ne $_.author) { $_.author.displayName } else { 'Unknown' }
        $created = if ($null -ne $_.created) { $_.created } else { 'Unknown' }
        $body = if ($null -ne $_.body) { ($_.body -replace "(`r`n|`n|`r)", "`n  ") } else { '' }
        "- $author | $created`n  $body"
    }) -join "`n`n"
} else {
    'None'
}
@(
    "Key: $($issue.key)"
    "Summary: $($issue.fields.summary)"
    "Type: $($issue.fields.issuetype.name)"
    "Status: $($issue.fields.status.name)"
    "Priority: $priority"
    "Assignee: $assignee"
    "Reporter: $reporter"
    "Description: $($issue.fields.description)"
    ""
    "Comments:"
    $comments
) -join "`n"
```

```powershell
Get-Content .\JIRA_SKILLS.config | ForEach-Object {
    if ($_ -match '^\s*#' -or $_ -notmatch '=') { return }
    $name, $value = $_ -split '=', 2
    Set-Item -Path "Env:$name" -Value $value
}

$issueKey = 'PROJ-123'
$issueUri = $env:JIRA_BASE_URL + '/rest/api/2/issue/' + $issueKey
$headers = @{
    Authorization = "Bearer $($env:JIRA_PAT)"
    Accept = 'application/json'
}

Invoke-RestMethod -Method Get -Uri $issueUri -Headers $headers | ConvertTo-Json -Depth 100
```

## Output Modes

- Default: plain-text issue summaries with comments for fast terminal reading
- Optional: raw JSON when the user asks for JSON output or needs the full response payload

## Error Handling

- Missing `JIRA_SKILLS.config`: tell the user to create it in the repo root with `JIRA_BASE_URL`, `JIRA_PAT`, and `JIRA_PROJECT_KEY`
- Missing config values: list the missing keys and stop
- Ambiguous request: ask a clarifying question instead of guessing
- `401` or `403`: explain that the PAT or Jira permissions may be wrong
- `404`: explain that the issue key or Epic key was not found
- Empty search results: report that no issues matched the request
- Empty Epic search results: report that no Epics matched the request
- Empty Epic issue search: report that no issues were found for that Epic
- Issues with no comments: show `Comments:` followed by `None`

## REST Notes

- Search/list operations use Jira's search endpoint with JQL
- Issue details use Jira's issue endpoint with an issue key
- Epic details use the same issue endpoint because Epics are still issues in Jira
- "Me" and "my" requests should prefer `currentUser()` in JQL when supported by the server
- Use `/rest/agile/1.0/epic/{epicIdOrKey}/issue` for issues linked to an Epic

## Limitations

- On-prem Jira only
- PAT authentication only
- Read-only issue search/list, Epic search/list, Epic-linked issue lookup, and issue view only
- No Jira Cloud support
- No write actions or Jira management workflows beyond issue search/list, Epic search/list, Epic-linked issue lookup, and issue view
- No Epic creation or Epic membership management
- No dependency on the standalone `jira` executable
