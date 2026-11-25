---
name: cb-analytics-security
description: |
  Use this skill when the user wants to manage Couchbase users, groups,
  roles, or check permissions on the cluster — creating service accounts,
  rotating passwords, granting analytics privileges, or auditing who can do
  what. Trigger when they mention "user", "group", "role", "RBAC",
  "permission", "upsert_user", "check_permissions", "local domain",
  "external domain", or "analytics_reader" / "analytics_admin".
license: MIT
---

# Couchbase RBAC via cb-analytics-mcp

You have 9 RBAC tools: list/get/upsert/delete user, list/upsert/delete group,
list roles, and check permissions.

## The two domains

Couchbase users live in one of two domains:

- **local** — created and managed inside Couchbase itself.
- **external** — authenticated via LDAP / SAML / PAM, mirrored locally with
  role bindings.

Every user-related tool takes a `domain` argument. If you list users without
a domain you get both.

## Role-spec format

`roles` is a single comma-separated string, never a list. Each role can be
unscoped or scoped:

```
analytics_reader[*]                       # all buckets
analytics_select[bucket1]                 # one bucket
analytics_select[bucket1:scope1]          # one scope
analytics_admin[*],query_select[bucket1]  # multiple roles
```

Use `list_roles()` first if you don't know what's available — it returns
every role the cluster supports, with descriptions.

## Creating a service account

For Claude itself, or any automation, create a least-privileged user:

```
upsert_user(
    domain="local",
    username="cb-mcp",
    roles="analytics_reader[*],analytics_select[*]",
    password="<generated>",
    full_name="cb-analytics-mcp service account"
)
```

**Never** use `analytics_admin` or `cluster_admin` for the MCP server's
cluster credentials in production. Grant only what the workflow needs.

## Password handling

The password is passed as a plain string into the tool and immediately
wrapped in `SecretStr` inside the impl, then unwrapped only at the HTTP
boundary. The audit log redacts it. That said:

- Generate strong passwords (`secrets.token_urlsafe(32)`).
- Rotate by calling `upsert_user` again with a new `password`.
- Never echo a password back to the user in chat.

## Checking permissions

`check_permissions(permissions="cluster.analytics!read,cluster.admin!write")`
returns a dict mapping each permission to `true`/`false` for the currently
authenticated user (the one in `CB_ANALYTICS_USERNAME`). Use this when:

- A tool returns `AnalyticsAuthError` and you want to confirm whether RBAC
  is the cause.
- You're auditing what the service account can actually do.

## Groups

Groups bundle role assignments and apply them to multiple users. Workflow:

1. `upsert_group("analytics-readers", roles="analytics_reader[*]", description="Read-only analytics users")`
2. `upsert_user(..., roles="local:analytics-readers")` to assign by group
   reference (Couchbase 7.2+).

## What to avoid

- Don't grant `cluster_admin` to "make things work" — find the specific role.
- Don't delete a user before deleting / reassigning what they own (libraries,
  active requests).
- Don't store passwords in the cluster config file. Use environment vars or
  a secrets manager instead.
- Don't echo a generated password back to the chat — show it once via a
  side channel (1Password, vault, etc.) and ask the user to confirm it's
  stored.

## Rate limits & safety

Security/RBAC tools split across two categories:

- **`read`** (60/sec): `list_users`, `get_user`, `list_groups`,
  `list_roles`, `check_permissions`.
- **`write`** (1/sec, intentionally tight): `upsert_user`, `delete_user`,
  `upsert_group`, `delete_group`.

The 1/sec write limit is deliberate — RBAC changes are durable cluster
state and the typical error mode is "did something irreversible
quickly". Bulk-provisioning users from a roster? Sequence them, accept
the ~1 second per user.

If `RateLimitExceeded` comes back on an `upsert_user` or `delete_user`,
honour `retry_after_sec`. Don't retry-storm.

Reads (`list_users`, `check_permissions`, etc.) share the global `read`
bucket. If you're auditing a permissions matrix, batch — one
`list_users` then targeted `check_permissions` calls is friendlier than
calling `get_user` per user-per-role combination.

Worth noting: rate limits are per **API key**, not per cluster. If a
single bearer token is doing both heavy RBAC bulk-load AND read-heavy
inspection at the same time, they contend for separate buckets, but the
bulk-load can starve other writes on the same key. Use distinct API
keys per workload if this matters.

## Related skills

- `cb-analytics-mcp-setup` — the MCP server's own credentials (`CB_ANALYTICS_USERNAME`, `MCP_API_KEY`) are configured here, not via RBAC tools
- `cb-analytics-cluster` — `who_am_i` to verify the effective role of the current MCP connection
