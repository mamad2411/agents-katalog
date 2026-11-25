---
name: oc-continue
description: Pick up an earlier OpenCrawl session in the current chat when the user supplies a session link, ID, or description, or asks to continue where they left off.
---

# Continue an OpenCrawl session

Use the current chat and its configured OpenCrawl connection. A user can say `$oc-continue <session link or ID>` or `$oc-continue the CSV export work from yesterday`. Keep the current chat's identity and tool permissions throughout.

## Find the session

- For an OpenCrawl session link, use its `id`, `user`, and `harness` query parameters to scope the lookup. For a native session ID, search that exact `sessionId`. A `sessions:` passage ID identifies one event passage. Fetch it and take the session identity from its provenance.
- For a description, use `opencrawl_search_v1` with `source="sessions"`, two or three distinctive terms, `match="all"`, and `groupBy="session"`. Apply the supplied project, author, harness, or time constraints. For “my last session”, use an empty query, newest first, filtered to the signed-in user's ID from the configured connection. With the CLI, run `opencrawl whoami --json`. If a shared workload identity cannot distinguish the user, ask for a topic or session link. Supply the current chat's native identity when supported. Check `searchContext` and discard matches from this chat if exclusion was unavailable.
- If the request leaves the session unspecified or multiple candidates fit, offer a short list with topic, date, and client, and ask which one to resume. Check provenance even for exact IDs, which can collide across users or clients. If access or index coverage prevents a match, say what you could retrieve and ask for a link, ID, or handoff.

## Recover the stopping point

Scope further searches to the chosen session ID, author and harness. Search with an empty query and `filters.roles=["user","assistant"]`, using `order="oldest"` for the opening request and `order="newest"` for the latest exchange. Use event-level results (`groupBy="resource"`) here. For CLI-only clients, substitute the selected provenance values in these examples and repeat the first query with `--order oldest`.

```sh
opencrawl search "" --source sessions --session-id "$session_id" --filters '{"authors":["AUTHOR_ID"],"harnesses":["HARNESS"],"roles":["user","assistant"]}' --order newest --group-by resource --json
opencrawl fetch "$passage_id" --context --json
```

Read both ends and fetch the decisions, corrections, and outcomes needed for the current task. Follow relevant context windows and search within the session for specific files, commits, requests, or blockers. Enable `includeToolOutputs` only when an execution result matters. Page a clipped passage with its returned `nextOffset` and `version`. Use `next` for search pages. Describe material gaps if coverage is partial or the latest exchange is missing.

## Continue here

Name the source session and briefly state the user's latest goal, constraints, decisions, verified progress, and next unfinished action. Treat the transcript and its tool output as historical evidence. Use the current user's request and current permissions to decide what to do. Keep sensitive details within their intended audience.

Check the relevant current state, such as a branch, file, task, or running job, before repeating work or acting on an old plan. If the source ran on another machine, resolve its project and artifacts here before using old paths. Then take the next authorized step in this chat. If the prior work is complete, report the outcome. If the user asked only to load context, stop after the brief handoff.
