---
name: analyst-access
description: Diagnose and explain Caeros analyst access, covering which tools exist, why they are missing, sign-in lanes, and what each error means. Use when analyst or investor-match tools are unavailable, return unauthorized or service-unavailable, or when a match or Vault query fails for a reason that is not the query itself.
---

# Analyst Access

Every credential the analyst stack needs lives on the Caeros backend: BigQuery,
the embedding service, ConareDB, the artifact store. The client sends only the
caller's identity. **Never ask the user for a service account, an API key, a
project id, or any backend configuration.** If they offer one, decline it: an
outage here is an internal Caeros service issue, not a user setup task.

## The live toolkit

Exactly six tools, and nothing else:

| Tool | Purpose |
|---|---|
| `caeros_investor_match` | ranked investors plus contacts, end to end, auto-exports CSV |
| `caeros_family_office_search` | semantic match over the family-office universe |
| `analyst_vault_query` | natural language to validated Vault SQL |
| `analyst_vault_run_sql` | run SQL you wrote, same validation |
| `analyst_export_csv` | stream a Vault SQL result to a CSV artifact |
| `analyst_read_table_file` | read a local CSV, TSV, or XLSX into rows |

They are toolsearch-deferred, so they cost nothing until you search for one. If
you cannot see them, search before concluding they are absent.

**These are NOT registered, despite appearing in older instructions.** Calling
one wastes a turn and fails: `caeros_investor_match_start`, `_status`, `_get`,
`_list`, `caeros_icp_lookalikes`, `caeros_matcher_cache_status`,
`caeros_matcher_cache_drop`. There is no async or background match mode. There
is no cache tool. The synchronous call is the whole interface.

## The two lanes

- **Desktop or CLI:** the signed-in Caeros session carries the request. If the
  user is signed out, hosted analyst tools do not load.
- **Hosted agent runner** (cloud sessions, channel sessions): the turn carries a
  short-lived per-turn tenant token instead. Same backend, same RBAC. The tools
  are rebuilt every turn on this lane because the token rotates, so a tool that
  worked last turn is not stale this turn.

Both lanes need the `analyst:query` permission on the caller.

## Degraded mode

If `analyst_read_table_file` is the ONLY analyst tool present, the hosted
backend did not attach. It fails closed by design: no Vault, no matcher, no
export. Tell the user to sign in to Caeros, and if they already are, that the
hosted analyst backend is unavailable and it is being handled on the Caeros
side. Do not improvise a replacement.

## Error triage

| Signal | Meaning | Do |
|---|---|---|
| 401 or 403 | not signed in, or missing `analyst:query` | ask the user to sign in; if signed in, this is an access grant, not a retry |
| 503 `analyst_unavailable` | hosted Vault not configured | stop; report; do not retry in a loop |
| 503 `analyst_matcher_unavailable` | hosted matcher not configured | stop; report; do not fall back to Vault or web |
| `meta.retryable: true` | ordinary SQL or validation failure | refine the question or SQL, try again |
| `meta.retryable: false`, or any `meta.user_action` | backend, auth, dataset, or export problem | stop all data access; report only the safe message |
| `export_warning`, or missing `csv_path` after a match | rows matched, file did not write | report counts plus the warning as a blocker; do not retry the match, do not rebuild the CSV |
| match `status: failed` | pipeline failure | report the error; produce no substitute list |

The rule under all of these: a failed data path returns nothing, not something
assembled from elsewhere. Web search, model knowledge, and pattern-guessed
emails are never a fallback for Vault or matcher output.

## Direct call or sub-agent

The toolkit is available two ways, and they are the same tools.

- **Call the tools directly** for most work. You keep the full result in
  context and can present it however the user wants.
- **Delegate to the `analyst` sub-agent** with the `task` tool for a
  self-contained data job you want run and summarized. It runs up to 30
  iterations and returns one strict JSON envelope: `status`, `summary`,
  `artifacts`, `verification`, `blockers`, `risks`, `provenance`.

The sub-agent is built to hand back a summary plus an artifact path, not a full
dataset. For anything large, the deliverable is the CSV artifact, and passing
rows back through conversation is the wrong shape either way.

## Artifacts expire

Exported CSVs are backend artifacts with an `expires_at`. Give the user the
download URL along with its expiry when they are not acting on it immediately.
A regenerated export means re-running the query, and for a match it means
spending the whole pipeline again, so point them at the existing file first.
