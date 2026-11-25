---
name: n8n-instance-ops
description: >-
  Operate a live n8n instance for a customer engagement: deploy an edit to a
  running workflow, activate/deactivate, flush the activation cache, move
  workflow JSON in and out over the API or CLI, and reason about webhook
  reachability and auth. Use when the task is to run, deploy, activate, edit, or
  troubleshoot a workflow that is ALREADY LIVE on an instance (not build one from
  scratch), for example "push this node change to the dev instance", "my DB edit
  is not taking effect", "the workflow will not activate", "the webhook 404s",
  "export these workflows to the repo", "which environment am I pointed at". For
  BUILDING workflows (nodes, expressions, Code nodes, validation) use the
  authoring skills instead. For choosing between several MCP-connected instances
  use n8n-multi-instance. For standing up or hardening an instance use
  n8n-self-hosting.
---

# n8n instance ops

Operating a live instance. The authoring skills tell you how to BUILD a workflow.
This one tells you how to run, deploy, edit, and troubleshoot one that is already
running on a customer's box.

Scope boundaries, so you load the right thing:

| Task | Skill |
|---|---|
| Which of several MCP-connected instances am I on | `n8n-multi-instance` |
| Standing up / hardening / scaling an instance | `n8n-self-hosting` |
| Building or changing what a workflow does | the authoring set (see bottom) |
| Promotion between environments, RBAC, licensing | `n8n-enterprise-delivery` |
| Running, deploying, activating, debugging a live workflow | **this skill** |

---

## Rule 0: know which environment you are pointed at, every time

An engagement has more than one instance and they look identical from the API.
Before any write, resolve the target explicitly.

- Credentials come from the engagement `.env`, never from memory and never
  inline: `N8N_API_URL_DEV` / `N8N_API_KEY_DEV`, `..._STAGING`, `..._PROD`.
- Confirm with `GET /api/v1/workflows?limit=1` and check you recognize the data,
  or `n8n_health_check` over MCP.
- **Default every operation to dev.** Staging and prod are named targets only.
- Prod is not in managed-mode MCP by default. Prod changes go through the
  customer's promotion path (source-control environment sync on Enterprise, or a
  reviewed manual import), not an ad-hoc API write.

Naming lies. "dev" on a customer's box is sometimes the live runtime and "prod"
is sometimes a decommissioned shell. Ask what actually serves traffic; do not
infer it from the hostname.

---

## Reaching the API

- Base: `{N8N_API_URL}/api/v1`, header `X-N8N-API-KEY: <key>`.
- Public API must be enabled on the instance (`N8N_PUBLIC_API_DISABLED` unset,
  and on licensed tiers the API can be turned off per-instance in settings).
- Core shapes:
  - `GET /workflows?limit=&cursor=&active=&tags=&projectId=`
  - `GET /workflows/{id}` (full nodes + connections)
  - `POST /workflows` (create; mints a NEW id)
  - `PUT /workflows/{id}` (full replace)
  - `POST /workflows/{id}/activate` and `/deactivate`
  - `GET /executions?workflowId=&status=`, `GET /executions/{id}?includeData=true`
  - `GET /credentials/schema/{type}` (schema only; the API never returns values)

### PUT is a full replace with a strict allowlist

`PUT /workflows/{id}` accepts only `name`, `nodes`, `connections`, `settings`.
Send `id`, `active`, `tags`, `createdAt`, or an unknown `settings` key and it
rejects the request. Round-trip pattern: `GET`, mutate, strip everything outside
the allowlist, `PUT`. Whitelist `settings` to
`saveExecutionProgress` / `saveDataSuccessExecution` / `saveDataErrorExecution` /
`saveManualExecutions` / `executionOrder` / `timezone` / `errorWorkflow` /
`executionTimeout`.

### The API cannot do everything

No endpoint for: activating a workflow's credentials, editing credential values,
triggering a non-webhook trigger, or reading a workflow that is mid-`waiting`.
When an ops task needs one of those, the path is the UI or the CLI, not a
cleverer API call. Say so rather than inventing an endpoint.

---

## The activation cache: the single biggest time sink

n8n snapshots a workflow's JSON **at the moment it receives an activation
event**. After that, executions run from the cached snapshot (visible as
`execution_data.workflowData`), not from the current row in the database.

Consequences:

- A direct database `UPDATE` on the workflow row lands in the DB and **never
  reaches the running trigger**.
- Container lifecycle does not refresh it. `restart`, and even `down && up`, do
  not re-read a workflow that was already active.
- An API `PUT` does not reliably propagate to the running trigger on its own.

**Flush it by forcing an activation event: deactivate, then activate.**
UI toggle off/on, or `POST /workflows/{id}/deactivate` then `/activate`. Follow
every programmatic edit to an active workflow with that pair.

**Verify at runtime, not at the write.** "The PUT returned 200" is not success.
Diff the stored workflow against the newest execution's `workflowData`, or just
run it and confirm the new behavior. If they differ, the cache is stale.

Same trap applies to MCP partial updates: `n8n_update_partial_workflow` saves,
but the live trigger keeps its snapshot until you toggle.

### Edit paths, in order of preference

1. **UI edit + Save.** A UI save reactivates, which flushes the cache for free.
   Default for one-off edits during a working session.
2. **API `PUT`** (or MCP partial update) + explicit deactivate/activate. Default
   for scripted, repeatable, or bulk edits, and the only path that is
   reviewable in git.
3. **Direct database write.** Last resort, and it carries the full cache trap.
   Only when the API is unavailable, and never on a customer's prod.

---

## Activation failures

A workflow that refuses to go active usually hits one of these:

- **A trigger node with no credential.** Some nodes (email send/trigger types
  among them) block activation entirely until a credential is bound. The error
  points at the node, not at the credential.
- **Webhook or form path collision.** Two workflows claiming the same path
  produce a 409 on activate. This is why you `PUT` an existing workflow rather
  than `POST` a new one when fixing in place: `POST` mints a new id and can
  collide on the path.
- **A form-trigger path edit while active.** Changing a form or webhook path on
  a live workflow needs deactivate, edit, activate. Editing in place leaves the
  old path registered.
- **Credential bound by id but not name (or the reverse).** See below.

---

## Credentials bind by id AND name

A node's `credentials` block carries both an `id` and a `name`. Import a
workflow into another instance and the id will not resolve, so the node shows
"credential not found" even when a credential with the same name exists. Fix by
rewriting the credential block to the target instance's real id, then reactivate.

This is why workflow JSON is not portable across instances by itself, and why
promotion between environments has to remap credentials (or use environment sync
on licensed tiers, which moves credential **stubs** only, never values).

---

## Export and import

**CLI (on the instance host):**

```
n8n export:workflow --all --output=workflows.json
n8n export:workflow --all --separate --output=./workflows/
n8n import:workflow --separate --input=./workflows/
n8n import:credentials --input=creds.json   # decrypted values, handle with care
```

Gotcha: `export:workflow --all` without `--separate` writes a **JSON array**;
`import:workflow --separate` expects a directory of **flat single-workflow
objects**. Round-tripping the array file through `--separate` fails. Either
export with `--separate` in the first place, or split the array yourself before
importing.

**API (from your machine):** `GET /workflows` paginated, then `GET
/workflows/{id}` per workflow to get nodes and connections (the list endpoint
does not include them). This is the path that keeps workflow JSON in the
engagement repo as source of truth.

Whatever the direction: **exported workflow JSON embeds credential references,
internal hostnames, and sometimes literal config values.** Scan before it lands
in a repo.

---

## Webhooks

- Path shape: `{N8N_BASE_URL}/webhook/<path>` for production,
  `/webhook-test/<path>` for the editor's Test-step listener. Test URLs only
  answer while the editor is listening.
- **A webhook does not exist until the workflow is active.** An inactive
  workflow 404s the production path. That is the first thing to check on a
  reported 404.
- The instance's advertised URL matters. Behind a proxy, set `WEBHOOK_URL` (and
  `N8N_HOST`/`N8N_PROTOCOL`) or n8n hands out URLs that resolve internally only.
- **Auth is the workflow's job unless the edge enforces it.** Assume anything
  under `/webhook/*` is reachable by whoever can reach the host. If a webhook
  needs auth, enforce it inside the workflow (header auth on the Webhook node, a
  shared-secret check, or the customer's gateway policy). Confirm with the
  customer where the boundary actually is; do not assume their WAF or SSO covers
  the webhook paths, since path-level bypasses for webhooks are a common and
  deliberate configuration.
- Browser callers need the origin in `N8N_CORS_ALLOW_ORIGIN` plus a restart. A
  healthy preflight returns 204 with an `access-control-allow-origin` echo.
- When curl-testing through a CDN or WAF, send a `User-Agent`. A missing UA gets
  bot-flagged independently of any rule you configured.

---

## Triggering for a test

- The API and MCP can only fire **webhook-shaped** triggers (webhook, form,
  chat). Manual, Schedule, and polling triggers return "workflow cannot be
  triggered externally".
- To exercise a Schedule- or poll-triggered flow, add a **temporary Webhook
  trigger** plus a seed node that emits what the real trigger would, wired into
  the first real node. Harden that first node to accept either source:

  ```javascript
  let meta = {};
  try { meta = $('Real Trigger').item.json; } catch (e) { meta = $json || {}; }
  ```

  Activate, call it, inspect, then remove the temporary branch before handoff.
- **Reactivating a polling trigger resets its baseline.** Only items created
  after reactivation fire, so re-seed test data after every edit cycle.
- Workflows in the `waiting` state are invisible to the executions list. Read
  them by id, or from the instance logs.

---

## Encryption key: the failure that looks like everything else

Every stored credential and API key is encrypted with the instance's
`N8N_ENCRYPTION_KEY`. If that key changes, every credential fails to decrypt and
every API key returns `invalid signature` at once.

- Set it explicitly and pin it. If it is unset, n8n generates one and writes it
  into its data directory; a rebuild that loses that directory loses every
  credential.
- Never let a deploy script shell-evaluate the env file if it contains command
  substitution, and never template the key from a random generator that runs per
  deploy.
- **Changing the key is a credential-rotation event**, not a fix: existing
  credentials and API keys become unreadable and must be recreated. Schedule it
  as a maintenance window.
- Diagnostic: sudden `invalid signature` on a key that worked, plus
  "could not decrypt" on credentials, equals a key change. Do not chase the API.

---

## Field gotchas worth keeping loaded

- **Object literals inside `{{ }}` break the expression extender.**
  `={{ JSON.stringify({ ... }) }}` in an HTTP Request `jsonBody` fails
  non-deterministically with `ExpressionExtensionError: invalid syntax`. Build
  the body in a Code node and reference it bare: `jsonBody: "={{ $json.rpc }}"`.
  For flat bodies, use `specifyBody: "keypair"` with simple per-field
  expressions instead.
- **A `responseMode: responseNode` webhook needs
  `onError: "continueRegularOutput"`**, or validation rejects it ("webhooks
  should always send a response, even on error").
- **In a Code node, read upstream data by node name**, not `$json`, whenever
  another node sits between producer and consumer. An HTTP node's response
  replaces `$json` and quietly poisons downstream references.
- **Binary in a Code node is not base64.** With filesystem binary mode,
  `item.binary.data.data` is the literal marker `filesystem-v2`. Use
  `await this.helpers.getBinaryDataBuffer(0, 'data')`.
- **MCP tag operations take the tag NAME under the key `tag`.** `tagId` or
  `name` returns `success: true` and silently no-ops. Verify by re-listing.
- **The validator flags deliberate parallel branches** (a Respond node and a
  work branch off the same output) as an error-handler mistake. That is a false
  positive; a live execution is the arbiter, not the linter.

---

## The toolkit

Every engagement directory and every client care kit carries the same scripts in
`scripts/`. Node built-ins only, no packages. Use them rather than hand-rolling
API calls, and trust them over your own reasoning when the two disagree.

| Command | When |
|---|---|
| `./scripts/doctor.sh [env]` | Start of a session, or when something feels wrong. Checks env, reachability, API capability, repo state. |
| `./scripts/health-check.sh [hours]` | Before diagnosing. Instance up, workflows active, recent failures, and which workflows are inactive. |
| `./scripts/drift-check.sh [env]` | Before trusting `workflows/`. Exit 1 on drift. |
| `./scripts/export-all.sh [env]` | Before every change. The rollback point. |
| `./scripts/validate.sh <file>` | Before every deploy. Offline, no instance needed. |

### Drift is the check people skip

`drift-check` compares the repository against what is actually deployed. It
ignores canvas positions, node ids, timestamps, pinned data, and sticky notes; it
reports parameters, connections, credentials, typeVersions, disabled nodes, and
active state. A node moved on the canvas is not drift. A changed parameter is.

Three outcomes and what each means:

- **ONLY ON INSTANCE** — a workflow was built in the UI and never exported. It
  has no rollback point. Export it before anything else happens to it.
- **CHANGED** — the canvas and the repo disagree. Someone edited live, or a
  change never reached the instance. Find out which before you touch it.
- **ONLY IN REPO** — deleted or renamed on the instance, or never deployed.

Resolving drift by blindly exporting is how a deliberate change gets erased, and
resolving it by blindly deploying is how a live fix gets reverted. Read the diff.

## Ops checklist

1. **Which environment?** Resolve from the engagement `.env`. Default dev. Prod
   only by name and only through the agreed promotion path.
2. **Read/trigger only?** MCP is fine.
3. **Editing node JSON?** UI Save, else API `PUT` with the field allowlist. DB
   write is last resort.
4. **Edited programmatically?** Deactivate, then activate. A restart is not
   enough.
5. **Verify at runtime.** Fresh execution shows the new behavior, or it did not
   ship.
6. **Webhook 404?** Workflow active? Production vs test path? Advertised
   `WEBHOOK_URL` correct?
7. **`invalid signature` / credentials broken?** Suspect the encryption key
   before anything else.
8. **Moving workflows between instances?** Remap credential ids, scan the JSON
   for embedded hostnames and values, then reactivate.
9. **Building, not operating?** Wrong skill.

---

## Authoring skills (not ops)

`using-n8n-mcp-skills` (router), `n8n-mcp-tools-expert`, `n8n-workflow-patterns`,
`n8n-node-configuration`, `n8n-expression-syntax`, `n8n-validation-expert`,
`n8n-code-javascript`, `n8n-code-python`, `n8n-code-tool`, `n8n-agents`,
`n8n-subworkflows`, `n8n-error-handling`, `n8n-binary-and-data`.
