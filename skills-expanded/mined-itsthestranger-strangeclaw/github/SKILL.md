---
name: github
description: Work with the GitHub REST API using configured auth, issues, pull requests, and repository contents.
version: 1.0.0
tags: [api, github, repository]
---

# GitHub API

## When To Use
Use this skill when a task requires interacting with the GitHub REST API: creating issues, listing pull requests, reading repository contents, inspecting repository metadata, or diagnosing GitHub API errors.

## Integration And Broker Rules
Use `http_request` with `integration: "github"` for all GitHub API calls that require configured access.

- Integration names are an authorization boundary. Use only names listed in execution context under `Configured integrations`.
- Never set `Authorization` or other protected auth headers directly. Credentials are injected by the host-side broker.
- Never ask the user to paste raw API tokens into task text.
- If `integration: "github"` is unavailable or broker denies access, report inability with broker reason.

## Workflow
1. Identify the GitHub owner, repository, and operation.
2. Ask for missing owner/repo/path/branch details before calling the API.
3. Use `http_request` with `integration: "github"` for private repositories, writes, and authenticated reads.
4. Follow pagination only until the requested data is complete.
5. Inspect status codes, response body `message`, and `documentation_url` fields on errors.
6. If broker returns `policy_denied`, include `requested_method`, `requested_url`, and `reason` in your report and do not retry the same denied request.
7. If broker returns `rate_limited`, wait and retry once, or report the limitation when waiting is not appropriate.
8. Summarize created issues, pull request lists, or file content findings.

## Repository Coordinates
Repository endpoints use path variables `owner` and `repo`. Ask the user for these if they are not in the task. Include `ref=<branch_or_sha>` when the task targets a specific branch, tag, or commit.

## Endpoint Patterns And Request Shapes
Use base URL `https://api.github.com`.

Create an issue (`POST /repos/{owner}/{repo}/issues`):

```json
{
  "method": "POST",
  "url": "https://api.github.com/repos/<owner>/<repo>/issues",
  "integration": "github",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": "{\"title\":\"Bug report\",\"body\":\"Steps to reproduce...\"}"
}
```

Optional issue fields include `assignees`, `labels`, and `milestone` when the user provides them or asks for them.

List pull requests (`GET /repos/{owner}/{repo}/pulls`):

```json
{
  "method": "GET",
  "url": "https://api.github.com/repos/<owner>/<repo>/pulls?state=open&per_page=100",
  "integration": "github",
  "headers": {},
  "body": null
}
```

Useful query parameters include `state`, `head`, `base`, `sort`, `direction`, `per_page`, and `page`.

Read repository contents (`GET /repos/{owner}/{repo}/contents/{path}`). Omit `{path}` to list the repository root:

```json
{
  "method": "GET",
  "url": "https://api.github.com/repos/<owner>/<repo>/contents/<path>?ref=<branch_or_sha>",
  "integration": "github",
  "headers": {},
  "body": null
}
```

File response shape can be metadata JSON (with `content` and `encoding`) or raw text depending on accepted media type configured by policy defaults. If metadata JSON is returned for files, decode Base64 `content` before reasoning over text.

Read repository metadata (`GET /repos/{owner}/{repo}`) when you need default branch, visibility, or permission indicators.

## Pagination
GitHub REST list endpoints commonly use `per_page` and `page`, and may include a `Link` response header with `rel="next"`. Continue pagination only until the requested information is complete. If `Link` contains a next URL, call that URL directly with the same integration.

## Rate Limits And Errors
Important response headers can include rate-limit state such as remaining requests and reset time. For 403 responses, inspect the body and headers to distinguish missing permission from rate limiting.

- 400: malformed query or payload.
- 401: integration credential invalid or missing.
- 403: insufficient permission, secondary rate limit, or primary rate limit.
- 404: repository/resource missing or token lacks access to a private repository.
- 409: merge or state conflict depending on endpoint.
- 422: validation failed, often duplicate issue data or invalid field values.
- 429: rate limited; retry once with wait or report limitation.

Report GitHub's `message` field and any relevant `documentation_url`, but avoid echoing credentials.
