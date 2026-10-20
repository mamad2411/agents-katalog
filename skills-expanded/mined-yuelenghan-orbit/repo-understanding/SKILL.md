---
name: repo-understanding
description: Use when an AI agent needs grounded repository context before implementation, review, or diff-impact analysis, and the needed understanding should be cached locally for reuse.
metadata:
  author: Orbit contributors
  version: "0.1.0"
---

# Repo Understanding

Use this skill as a thin repository-understanding surface for AI agents.

This skill is a source-first local analysis helper and a code-heavy carve-out within Orbit. It is not a scenario router and should keep its local-only CLI and cache lifecycle intact.

## Inputs

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `REPO_ROOT` | Yes | Local repository root to analyze | `/path/to/workspace/sample-org/sample-service` |
| `ACTION` | Yes | One of `refresh`, `search`, `explain`, `diff-impact` | `search` |
| `MODE` | For `refresh` | One of `full`, `incremental`, `semantic-only` | `incremental` |
| `ANNOTATIONS_FILE` | For `refresh` with `MODE=semantic-only` | Local path to the semantic annotations payload to merge | `/tmp/semantic-annotations.json` |
| `QUERY` | For `search` | Story text, AC, bug description, or intent text | `login timeout after token refresh` |
| `TARGET` | For `explain` | File path or `path:symbol` selector | `src/auth/service.ts:refreshToken` |
| `BASE_REF` | Optional | Git base ref for diff impact | `origin/master` |

Ask for any missing required inputs in one plain-text message. Do not guess outside `REPO_ROOT`.

## Before You Start

Read:

- `references/usage.md`
- `references/commands.md`

This skill is local-only in `v1`. It must not start a dashboard, depend on the upstream `Understand-Anything` checkout at runtime, or create PRs, Jira tickets, or Confluence pages.

## Local Persistence

Persist local state under:

```text
~/.config/repo-understanding/
```

Use that root as the local cache base. Store repository-specific data under:

```text
~/.config/repo-understanding/repos/<repo-fingerprint>/
```

Use each per-repo directory for `manifest.json`, `structure-index.json`, `semantic-cache.json`, `diff-cache/`, `snapshots/`, and `logs/`.

## Workflow

1. Run `refresh` before the first `search`, `explain`, or `diff-impact` call for a repository.
2. Use `search` to map Story text or bug text to likely files and symbols.
3. Use `explain` to assemble grounded local context for the top candidate files or symbols.
4. Use `diff-impact` after a patch plan or local changes exist.

## Forbidden Behavior

- no dashboard startup
- no ReactFlow or browser token behavior
- no dependency on an external upstream checkout
- no direct Jira, Confluence, Bitbucket, or Jenkins orchestration from this skill
- no semantic cache entries without provenance fields

## Completion

A `repo-understanding` call is complete only when:

- the requested action succeeds against local cache or explicitly reports the missing cache reason
- every returned node is traceable to repository paths or symbols
- semantic fields are clearly marked as cached annotations instead of source-of-truth structure
