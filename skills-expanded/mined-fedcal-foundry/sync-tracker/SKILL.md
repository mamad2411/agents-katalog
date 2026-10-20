---
name: sync-tracker
description: Detect which issue tracker a project actually uses, read its board, and normalise every item into tracker-item.v1 so flow metrics and sprint reports never touch a provider payload. Covers GitHub Issues, Jira Cloud, Linear and GitLab, resolves state through status categories rather than renameable names, reads transition history for cycle time, and reports every field it could not map instead of guessing. Use before any forecast, sprint report or tracker migration, and whenever a project's work lives somewhere other than GitHub. Not for deciding priority, not for repository governance, not for posting notifications.
argument-hint: "[--provider github|jira|linear|gitlab] [--project KEY] [--since 90d] [--no-history] [--dry-run]"
user-invocable: true
agent: foundry-pmo:tracker-operator
model: sonnet
effort: medium
metadata:
  foundry.vertical: management
  foundry.io: "live tracker -> tracker-item.v1[] + handoff.v1"
license: Apache-2.0
---

# Sync tracker

One command, four providers, one output shape. Everything downstream reads `tracker-item.v1` and
stays provider-independent; changing tracker rewrites the mapping in this skill and nothing else.

`--dry-run` shows the calls without executing them. Credentials are read from the environment and
never printed, never written into an artifact.

## Step 1 — Detect the provider

Skip if `--provider` was given. Otherwise decide from signals and **report which one decided**:

```bash
git remote -v
```

| Signal | Provider |
|---|---|
| remote host `github.com` | `github` |
| remote host is a GitLab instance | `gitlab` |
| `.foundry/tracker.json` names one | that one — it outranks remotes |
| branches match `[A-Z][A-Z0-9]+-\d+` | probably `jira`; confirm, do not conclude |
| `LINEAR_API_KEY` set | `linear` |

Signals conflict routinely — code on GitHub, work in Jira is the normal enterprise case. Ask once,
record the answer in `.foundry/tracker.json`, never ask again.

## Step 2 — Preflight

```bash
gh auth status
```

```bash
curl -sS -u "$JIRA_EMAIL:$JIRA_API_TOKEN" "$JIRA_BASE_URL/rest/api/3/myself"
```

```bash
glab auth status
```

Missing credentials is not a failure to work around: emit the exact calls, produce no items, set
`handoff.v1.status: blocked`. A synthesised board is worse than no board.

## Step 3 — Read

**GitHub**

```bash
gh issue list --state all --limit 500 --json number,title,body,state,stateReason,labels,assignees,milestone,createdAt,updatedAt,closedAt,url
```

Transitions come from the timeline endpoint per issue; that is one call per item, so respect
`--since` and cache. Without it, set `flow.historyRead: false`.

**Jira**

```bash
curl -sS -u "$JIRA_EMAIL:$JIRA_API_TOKEN" -G "$JIRA_BASE_URL/rest/api/3/search" \
  --data-urlencode "jql=project = $JIRA_PROJECT_KEY AND updated >= -90d ORDER BY created ASC" \
  --data-urlencode "expand=changelog" \
  --data-urlencode "maxResults=100"
```

Page with `startAt` until `startAt + maxResults >= total`. Resolve custom fields by **name**
through `/rest/api/3/field` — never hardcode `customfield_10016`, which differs per instance.

**Linear** — GraphQL at `https://api.linear.app/graphql`, `Authorization: $LINEAR_API_KEY`,
requesting the `history` connection for transitions.

**GitLab**

```bash
glab api "projects/:id/issues?updated_after=$SINCE&per_page=100"
```

Transitions come from the resource state and label event endpoints.

## Step 4 — Normalise

Map to `tracker-item.v1`. Two rules decide the quality of everything computed downstream:

- **Jira: map on `statusCategory.key`** (`new` / `indeterminate` / `done`), not `status.name`.
  Names get renamed; categories survive. A mapping built on names breaks the first time somebody
  renames "In Progress" to "Doing", and it breaks silently.
- **Never merge `done` and `cancelled`.** GitHub `stateReason: not_planned`, Jira's Won't Do and
  Duplicate resolutions, Linear's Cancelled and GitLab's closed-unmerged all mean closed without
  delivery. Counting them as throughput inflates every forecast built on this data.

Anything without an honest destination becomes `type: unmapped` or `state: unmapped`, with
`nativeType` / `nativeState` carrying the provider's own word. **Report the unmapped count in the
summary.** A normalisation that reports zero unmapped items on a real board has almost certainly
forced values into the nearest bucket.

For transitions, take the **earliest** entry into an in-progress state. A reopened item that
passed through twice otherwise reports an impossibly short cycle time.

## Step 5 — Write and verify

Write the array through `mcp__plugin_foundry-core_foundry__blackboard_write`, which validates
against `tracker-item.v1` before anything reaches disk. Writing with `Write` instead only triggers
the non-blocking `PostToolUse` validator, after the invalid file already exists.

Self-checks before reporting success:

- every item has `sourceId`, `sourceUrl`, `nativeState`;
- the count matches what the provider reported as total;
- no item has `state: done` with `closedAt` absent;
- no token, cookie or auth header appears anywhere in the output.

## Step 6 — Report

`handoff.v1` with counts by state, the unmapped list, `flow.historyRead` coverage as a
percentage, and every degradation applied. Return only the artifact path plus a summary
≤ 300 tokens.

## Degradation

| Condition | Behaviour |
|---|---|
| no credentials | emit calls, `status: blocked`, no items |
| read-only token | normalise fully; list skipped mutations with the scope each needs |
| `--no-history` or history forbidden | `flow.historyRead: false` on every item; say prominently that cycle time is now unavailable and only lead time can be computed |
| Jira custom field lookup fails | omit `estimate` and `sprint`; never guess a field id |
| rate limited | honour `Retry-After`, resume from the last page, report the pause |

## Refusals

- Synthesising items, dates or states that were not read.
- Fuzzy-matching an item by title similarity — a wrong match overwrites somebody else's work.
- Writing a credential into any artifact or commit.
- Bulk-migrating between providers without a verified ten-item pilot first.

## Progressive disclosure

- `references/provider-apis.md` — pagination, auth and history per provider, with exact calls.
- `references/state-mapping.md` — the default mapping table and how to override it in
  `.foundry/tracker.json`.
- `references/migration.md` — the three things that always break in a tracker migration.
