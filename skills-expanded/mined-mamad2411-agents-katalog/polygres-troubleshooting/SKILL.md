---
name: polygres-troubleshooting
description: Diagnose Polygres CLI, Runtime API, control-plane, Postgres, job, migration, and retrieval failures using public read-only evidence. Use when a user reports an error, timeout, partial failure, readiness problem, ambiguous project, import or migration issue, or broken graph, vector, text, or hybrid retrieval. Do not use private observability systems, undocumented endpoints, or mutating repair actions while diagnosing.
---

# Polygres Troubleshooting

Use read-only checks first. Resolve context, preserve evidence, classify the
failure boundary, and recommend the smallest safe correction. Do not mutate
while diagnosing.

## Workflow

1. Read the installed `polygres --help` and command-specific help before using
   a command. Installed behavior is the source of truth for CLI compatibility.
2. Resolve identity, configuration source, and one exact project using
   `references/context-and-connectivity.md`. Stop on an ambiguous project.
3. Capture the symptom, timestamp, sanitized command or SDK call, exit code or
   exception type, `request_id`, job ID, and whether pagination returned a
   cursor.
4. Inspect project and database evidence with
   `references/projects-and-database.md`.
5. For import job or migration failures, use
   `references/jobs-and-migrations.md`. For graph, vector, text, hybrid, or
   readiness failures, use `references/retrieval.md`.
6. Classify the fault as CLI/local configuration, control-plane, Runtime API,
   Postgres/database or pooler, or asynchronous job state. Use
   `references/errors-and-escalation.md` for typed SDK errors and escalation.
7. Re-check status before retry. Recommend a corrective action, but obtain
   explicit approval and delegate supported mutations to `$polygres-cli` or
   application changes to `$polygres-sdk`.

## Evidence rules

- Use only commands confirmed by installed help and public `$polygres-sdk`
  methods. Never guess a private endpoint or use internal observability.
- Preserve request and job IDs exactly. Distinguish absent evidence from a
  successful check.
- Never log a database password, API key, authorization header, connection
  string containing credentials, or full environment output.
- Do not retry validation, authentication, permission, or compatibility errors
  as if they were transient. Bound any retry for a rate limit or timeout.
- Report pagination and partial failure explicitly; a successful first page or
  one healthy subsystem does not prove the whole operation succeeded.

## Diagnostic report

- **Resolved identity:** account identity or the exact reason it is unknown.
- **Resolved project:** exact project ID or the ambiguity that blocked selection.
- **Symptom:** observable failure and affected operation.
- **Observed evidence:** sanitized statuses, exception classes, and timestamps.
- **Likely cause:** evidence-backed classification with confidence.
- **Safe checks performed:** public read-only commands and SDK calls used.
- **Corrective action:** smallest documented action, not yet performed.
- **Approval or escalation:** approval needed or escalation destination.
- **IDs retained:** request IDs, job IDs, and cursors without secrets.
- **Unknowns:** missing, stale, incompatible, or contradictory evidence.

## Boundaries

- Do not mutate while diagnosing, rotate credentials, retry jobs, apply
  migrations, rebuild graph resources, or start a vector reindex.
- Do not call an undocumented or private route and do not query a private
  observability system.
- Do not claim root cause when evidence supports only a likely boundary.
