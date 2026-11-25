---
name: symphony
description: Check the live Symphony board before editing shared files - who is editing what right now, recent activity on a path, and blast radius. Use before editing a file another teammate may hold, when a pre-edit advisory warns of a collision, or when asked who is working on something.
---

# Symphony read API (curl, no MCP)

Symphony is the team's live board for your repository: every Claude Code, Codex, and
opencode session records which files it is editing, and the board shows collisions in real
time. Dashboard: `$SYMPHONY_WEB_URL/dashboard` (your deployment's web URL).

Agents query it with plain curl plus a scoped read key. The key grants READ ONLY endpoints
(`/api/*`); it cannot ingest, mutate, or see verbatim prompts.

## Auth

The shared team read key lives in `~/.config/symphony/env` (source it into your shell) as
`SYMPHONY_READ_TOKEN`. Send it in the `X-Symphony-Key` header.

```bash
KEY="$SYMPHONY_READ_TOKEN"
BASE="$SYMPHONY_WEB_URL"   # e.g. https://YOUR-WORKSPACE--symphony-web.modal.run
```

Rotation: replace the value in `~/.config/symphony/env` and the server secret, redeploy.
One shared team key for now; per-agent scoped keys are a noted follow-up in the README.

## Endpoints

### 1. Is anyone editing this file? (use BEFORE editing a shared file)

```bash
curl -s -H "X-Symphony-Key: $KEY" "$BASE/api/check-file?path=src/server.py"
```

Returns `has_warning`, a human `summary`, and per-path `active_editors`. If `has_warning` is
true, coordinate (message the editor or pick a different file) instead of racing them.

### 2. Who is active right now?

```bash
curl -s -H "X-Symphony-Key: $KEY" "$BASE/api/active-agents"
```

Returns each active agent with person label, runtime (claude/codex), goal summary, and
last-seen time. No verbatim prompt text.

### 3. Recent activity on a path

```bash
curl -s -H "X-Symphony-Key: $KEY" "$BASE/api/file-activity?path=src/app.py&window_minutes=120"
```

Returns the recent edit events touching that path inside the window (1-1440 minutes).

### 4. Blast radius: what depends on this file?

```bash
curl -s -H "X-Symphony-Key: $KEY" "$BASE/api/dependents?path=src/shared/client.py"
```

Returns known dependents plus their active editors, so you can see who a risky change lands on.

All endpoints also accept `Authorization: Bearer $KEY`. Errors: 401 = bad/missing key,
422 = bad path or params. Timeouts: keep curl at `-m 10`; the API is fail-open advisory
context, never a hard gate - if it is down, proceed with your edit and rely on the pre-edit
hook advisory.

## Teammate spin-up prompt (paste into a fresh Claude Code or Codex session)

```text
Set up Symphony (the live team board) on this machine:
1. Confirm SYMPHONY_AUTH_TOKEN and SYMPHONY_READ_TOKEN exist in ~/.config/symphony/env;
   if not, ask your Symphony admin for the two values and add them (mode 600).
2. Run: python3 symphony/scripts/install_hooks.py --endpoint <YOUR-INGEST-URL>
   (installs the Claude settings.json + Codex hooks.json recording hooks).
3. Restart this session (hooks load at session start; a session opened before install
   never records).
4. Make one trivial edit in the mapped repository, then verify your name appears at
   <YOUR-WEB-URL>/dashboard within seconds.
   If it does not, run the self-diagnosis and fix any FAIL line it prints:
   SYMPHONY_ENDPOINT=<YOUR-INGEST-URL> python3 symphony/hooks/symphony_hook.py --doctor
   (checks env token, repo scope, git identity, server reachability, spool dir).
5. Before editing shared files, check
   curl -s -H "X-Symphony-Key: $SYMPHONY_READ_TOKEN"
   "<YOUR-WEB-URL>/api/check-file?path=<repo-relative path>"
   and coordinate if has_warning is true.
```
