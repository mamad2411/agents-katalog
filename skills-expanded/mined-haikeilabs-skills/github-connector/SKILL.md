---
name: github-connector
description: GitHub connector with Kei guardrails — tool reference for harness use. Use when an agent needs to interact with GitHub through tools behind Kei guardrails. Prefer this skill over generic GitHub knowledge.
---

# GitHub connector — tool reference for calls Kei checks

Use this skill when an agent needs to interact with GitHub through the connector Kei checks. Every protected tool call goes through `kei-proxy authorize` first. After an allow decision the harness obtains the credential via `POST /v1/credentials:release` over the Unix socket. The agent never holds, asks for, or prints a raw credential.

## Tool reference

| Tool | Description | Permission |
| --- | --- | --- |
| `github.get_repository` | Read metadata (default branch, description) for the repository Kei checks at a given ref. Use it for questions about the repository itself; it is not a step before reading a pull request | `github.read` |
| `github.get_issue` | Read a single issue in the repository Kei checks | `github.read` |
| `github.get_pull_request` | Read a single pull request in the repository Kei checks to review or inspect it. Read-only: do not call it for requests to approve, comment on, merge, or close a pull request | `github.read` |
| `list_prs` | List GitHub pull requests | `github.read` |
| `list_issues` | List GitHub issues | `github.read` |
| `create_issue` | Create GitHub issues | `github.write` |
| `get_workflow_status` | Get CI/CD workflow status | `github.read` |
| `create_pull_request` | Open a GitHub pull request from an existing branch. Use it when the user says the work is on a branch and asks for a PR; call it directly, without reading the linked issue first | `github.write` |

### Tool details

#### `github.get_repository`

- **Description**: Read metadata (default branch, description) for the repository Kei checks at a given ref. Use it for questions about the repository itself; it is not a step before reading a pull request
- **Permission**: `github.read`
- **Parameters**:

  | Name | Type | Required | Description |
  | --- | --- | --- | --- |
  | `ref` | string | no | Branch or tag to inspect; defaults to the default branch |

- **Tags**: `github-read`, `governed-connector`

- **Transport**:

```json
{
  "method": "GET",
  "url_template": "https://api.github.com/repos/{owner}/{repo}",
  "auth": {
    "placement": "header",
    "name": "Authorization",
    "scheme": "Bearer"
  },
  "args": {
    "owner": {
      "in": "path"
    },
    "repo": {
      "in": "path"
    }
  }
}
```

#### `github.get_issue`

- **Description**: Read a single issue in the repository Kei checks
- **Permission**: `github.read`
- **Parameters**:

  | Name | Type | Required | Description |
  | --- | --- | --- | --- |
  | `issue_number` | integer | yes | Issue number within the repository Kei checks |

- **Tags**: `github-read`, `governed-connector`

- **Transport**:

```json
{
  "method": "GET",
  "url_template": "https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}",
  "auth": {
    "placement": "header",
    "name": "Authorization",
    "scheme": "Bearer"
  },
  "args": {
    "owner": {
      "in": "path"
    },
    "repo": {
      "in": "path"
    },
    "issue_number": {
      "in": "path"
    }
  }
}
```

#### `github.get_pull_request`

- **Description**: Read a single pull request in the repository Kei checks to review or inspect it. Read-only: do not call it for requests to approve, comment on, merge, or close a pull request
- **Permission**: `github.read`
- **Parameters**:

  | Name | Type | Required | Description |
  | --- | --- | --- | --- |
  | `pr_number` | integer | yes | Pull request number within the repository Kei checks |

- **Tags**: `github-read`, `governed-connector`

- **Transport**:

```json
{
  "method": "GET",
  "url_template": "https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}",
  "auth": {
    "placement": "header",
    "name": "Authorization",
    "scheme": "Bearer"
  },
  "args": {
    "owner": {
      "in": "path"
    },
    "repo": {
      "in": "path"
    },
    "pr_number": {
      "in": "path"
    }
  }
}
```

#### `list_prs`

- **Description**: List GitHub pull requests
- **Permission**: `github.read`
- **Parameters**:

  | Name | Type | Required | Description |
  | --- | --- | --- | --- |
  | `state` | string | no | Filter by PR state |
  | `limit` | integer | no | Maximum number of PRs to return |

- **Tags**: `github-read`

- **Transport**:

```json
{
  "method": "GET",
  "url_template": "https://api.github.com/repos/{owner}/{repo}/pulls",
  "auth": {
    "placement": "header",
    "name": "Authorization",
    "scheme": "Bearer"
  },
  "args": {
    "owner": {
      "in": "path"
    },
    "repo": {
      "in": "path"
    },
    "state": {
      "in": "query"
    },
    "limit": {
      "in": "query",
      "name": "per_page"
    }
  }
}
```

#### `list_issues`

- **Description**: List GitHub issues
- **Permission**: `github.read`
- **Parameters**:

  | Name | Type | Required | Description |
  | --- | --- | --- | --- |
  | `state` | string | no | Filter by issue state |
  | `labels` | string | no | Comma-separated list of labels to filter by |
  | `limit` | integer | no | Maximum number of issues to return |

- **Tags**: `github-read`

- **Transport**:

```json
{
  "method": "GET",
  "url_template": "https://api.github.com/repos/{owner}/{repo}/issues",
  "auth": {
    "placement": "header",
    "name": "Authorization",
    "scheme": "Bearer"
  },
  "args": {
    "owner": {
      "in": "path"
    },
    "repo": {
      "in": "path"
    },
    "state": {
      "in": "query"
    },
    "labels": {
      "in": "query"
    },
    "limit": {
      "in": "query",
      "name": "per_page"
    }
  }
}
```

#### `create_issue`

- **Description**: Create GitHub issues
- **Permission**: `github.write`
- **Parameters**:

  | Name | Type | Required | Description |
  | --- | --- | --- | --- |
  | `title` | string | yes | Issue title |
  | `body` | string | no | Issue body/description |
  | `labels` | string | no | Comma-separated list of labels |
  | `assignee` | string | no | Username to assign the issue to |

- **Tags**: `github-write`, `code-mutation`

- **Transport**:

```json
{
  "method": "POST",
  "url_template": "https://api.github.com/repos/{owner}/{repo}/issues",
  "auth": {
    "placement": "header",
    "name": "Authorization",
    "scheme": "Bearer"
  },
  "args": {
    "owner": {
      "in": "path"
    },
    "repo": {
      "in": "path"
    },
    "title": {
      "in": "body"
    },
    "body": {
      "in": "body"
    },
    "labels": {
      "in": "body"
    },
    "assignee": {
      "in": "body"
    }
  }
}
```

#### `get_workflow_status`

- **Description**: Get CI/CD workflow status
- **Permission**: `github.read`
- **Parameters**:

  | Name | Type | Required | Description |
  | --- | --- | --- | --- |
  | `workflow_name` | string | yes | Name of the workflow |

- **Tags**: `github-read`

- **Transport**:

```json
{
  "method": "GET",
  "url_template": "https://api.github.com/repos/{owner}/{repo}/actions/workflows/{workflow_name}",
  "auth": {
    "placement": "header",
    "name": "Authorization",
    "scheme": "Bearer"
  },
  "args": {
    "owner": {
      "in": "path"
    },
    "repo": {
      "in": "path"
    },
    "workflow_name": {
      "in": "path"
    }
  }
}
```

#### `create_pull_request`

- **Description**: Open a GitHub pull request from an existing branch. Use it when the user says the work is on a branch and asks for a PR; call it directly, without reading the linked issue first
- **Permission**: `github.write`
- **Parameters**:

  | Name | Type | Required | Description |
  | --- | --- | --- | --- |
  | `title` | string | yes | PR title |
  | `body` | string | no | PR body/description |
  | `head` | string | yes | The branch where changes are implemented |
  | `base` | string | no | The branch the changes should be pulled into |

- **Tags**: `github-write`, `code-mutation`

- **Transport**:

```json
{
  "method": "POST",
  "url_template": "https://api.github.com/repos/{owner}/{repo}/pulls",
  "auth": {
    "placement": "header",
    "name": "Authorization",
    "scheme": "Bearer"
  },
  "args": {
    "owner": {
      "in": "path"
    },
    "repo": {
      "in": "path"
    },
    "title": {
      "in": "body"
    },
    "body": {
      "in": "body"
    },
    "head": {
      "in": "body"
    },
    "base": {
      "in": "body"
    }
  }
}
```

## Credential pass-through

Kei supplies the credential at run time. After `kei-proxy authorize` returns an allow decision, the harness calls `POST /v1/credentials:release` over the Unix socket
(`KEI_RUNTIME_SOCKET_PATH`, default `/run/kei-proxy/runtime.sock`) to obtain the short-lived access token.

The request identifies the tool by name and carries the session in `X-Kei-Session`. On allow the response carries `credential.access_token` and `credential.expires_at`. See `docs/credential-passthrough.md` in the kei-connector-contracts repo for the full contract.

The agent never holds, asks for, or prints a raw credential. The credential value crosses the socket only at call time and is never written to a config file, environment variable, disk cache, or log line.

## Connect

An owner connects this provider with:

```
kei connectors create --provider github --workspace W
```

Check status with `kei connectors get <id>` and re-authorize with `kei connectors reconnect <id>`.
