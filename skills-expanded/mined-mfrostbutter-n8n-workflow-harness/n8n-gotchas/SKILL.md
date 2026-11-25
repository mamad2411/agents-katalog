---
name: n8n-gotchas
description: >-
  Field-discovered n8n behaviors that are correct-looking but wrong, collected
  from real builds. Use as a lookup when something in n8n "succeeded" but did not
  actually take effect, when a workflow behaves differently than its JSON says,
  when an edit does not reach the running trigger, when a node returns success
  with no result, or when an error message points at the wrong cause. Also read
  it before a first build on a new instance so the known traps are already
  loaded. Complements the authoring skills (which cover correct usage); this file
  covers the places where correct usage still surprises you.
---

# n8n gotchas

Behaviors that cost real hours. Each entry: the symptom, the cause, the fix.
Grows in place; add an entry the day you lose time to something new.

Ordered by how often they bite.

---

## Silent success

Things that report success and do nothing.

### An edit that never reaches the running trigger

**Symptom:** you change a workflow (DB write, API `PUT`, MCP partial update),
the call returns success, and executions keep running the old logic.

**Cause:** n8n caches the workflow JSON at the moment of the **activation
event**. Executions run from that snapshot. Container restarts do not re-read it.

**Fix:** deactivate then activate. Verify against a fresh execution, not against
the write's return code. Full treatment in `n8n-instance-ops`.

### An API edit that an open editor tab silently reverts

**Symptom:** you `PUT` a workflow (or use an MCP partial update), the call returns
success, a read-back confirms the change, and the next run executes the old code
anyway. Read the workflow again and your edit is gone.

**Cause:** the editor is a competing writer, not a view. A browser tab holding the
workflow keeps its own full copy in memory, and saving or pressing Test pushes that
whole copy back, including nodes you never touched. Whoever writes last wins, and
the tab wins by default because the human is still clicking.

**Fix:** do not write over the API while the workflow is open in a tab. If you must,
have the human hard-reload the tab afterwards and confirm the changed node body by
eye before running. Compare `updatedAt` and `versionId` before and after: an
`updatedAt` **later than the failing execution** is the tell that a browser save
landed on top of you.

**Observed 2026-08-26 on 2.35.5:** one Code node was fixed over the API three times
and reverted twice by the same open tab. A node **added** in the same edit survived,
because the tab picked it up on a page load, while the edited node body did not. So
partial survival is normal and makes the revert harder to spot. The fastest exit is
to hand the human the code and let them paste it in the tab that is winning.

### A tool sub-node with `onError` set, which makes the agent invent an answer

**Symptom:** an AI Agent answers plausibly but wrongly. The execution is green, the
tool node shows as run, no error appears anywhere, and the tool's output is an empty
array (`"ai_tool": [[]]`). Called directly, the same sub-workflow returns correct
data.

**Cause:** `onError: "continueErrorOutput"` on a node connected by `ai_tool`. A
sub-node has no error output to route to, so the failure is swallowed and the tool
returns nothing. The model receives an empty tool result and fills the gap from its
own priors.

**Fix:** remove `onError` from tool sub-nodes. Handle failure at the workflow level
instead. This overrides the general advice to set `continueErrorOutput` on tool
sub-workflows, which is correct for `main` connections and wrong here.

**Why it is worse than it sounds:** the fabrication is fluent and on-topic. Observed
2026-08-23 on 2.35.5: an entitlement-gated data tool went silent and the agent
produced a polite, well-formed access refusal that was indistinguishable from the
real one. Nothing downstream can tell the difference. Always verify a tool's output
is non-empty, not just that the run succeeded.

### A tool node the agent cannot call, because only half the node exists

**Symptom:** an AI Agent reports that a tool "encountered an error during
execution" and quotes `The node '<type>' has a 'supplyData' method but no
'execute' method`. The workflow validates, the canvas looks right, the `ai_tool`
wire is there.

**Cause:** the AI Agent at typeVersion 3.x invokes tools through the node's
`execute` method. Some tool nodes only ship `supplyData`, which is what the older
agent versions used. Those nodes still render, still connect, and still fail.

**Fix:** check the node class before you wire it. Inside the container:

```bash
podman exec <container> node -e '
const o = new (require("<path>/ToolX.node.js").ToolX)();
const vs = o.nodeVersions ? Object.keys(o.nodeVersions) : o.description.version;
console.log(vs);
if (o.nodeVersions) for (const v of vs)
  console.log(v, typeof o.nodeVersions[v].supplyData, typeof o.nodeVersions[v].execute);
else console.log(typeof o.supplyData, typeof o.execute);'
```

A version showing `function undefined` cannot be driven by a 3.x agent.

**Observed 2026-09-03 on 2.35.5:** `toolHttpRequest` maxes out at version 1.1 and
has `supplyData` only, so a 3.x agent cannot call it at all. `toolWorkflow` v2.x
has both. Wrap the HTTP call in a sub-workflow and attach that as the tool. This
is not a workaround: the capability then enters the same governed catalogue as
every other sub-agent, and identity is plumbed by the workflow rather than filled
in by the model.

### MCP tag operations that no-op

**Symptom:** `addTag` / `removeTag` returns `success: true`, the tag does not
change, and a warning mentions `Cannot read properties of undefined (reading
'toLowerCase')`.

**Cause:** the operation takes the tag **name string** under the key `tag`.
Passing `tagId` or `name` is accepted and ignored.

**Fix:** `{ type: 'removeTag', tag: 'my tag name' }`. Verify by re-listing.

### A calendar or shared-resource node that returns zero with no error

**Symptom:** a node reads a resource the user can see in the picker and returns 0
items in a fraction of a second, no error.

**Cause:** the OAuth credential authenticates as an identity that is *subscribed*
to the resource but does not own it. Subscription is not read access to item
detail.

**Fix:** do not chase the time window or the filter. Check which identity the
credential holds. Either use an owning identity, or bypass OAuth with a direct
feed/API read plus a parsing Code node.

### A write to the wrong instance

**Symptom:** a read returns unfamiliar data, or an object you know exists returns
`NOT_FOUND`.

**Cause:** the session is targeting a different instance than you think. Reads
and non-credential writes misroute **silently**.

**Fix:** re-resolve the target before concluding anything was deleted. See
`n8n-multi-instance`.

---

## Expressions and data flow

### Object literals inside `{{ }}` break the expression extender

**Symptom:** `ExpressionExtensionError: invalid syntax`, non-deterministically,
on an expression that looks fine and that works verbatim in another node.

**Cause:** n8n pre-parses the whole `{{ }}` to inject its `.extend()` helpers. An
inline object literal trips that parser. An empty `|| {}` and a bare `undefined`
inside `{{ }}` break it reliably.

**Fix:** build the value in a Code node, reference it bare:
`={{ $json.payload }}`. For flat HTTP bodies use `specifyBody: "keypair"` with
one simple expression per field. Spacing the braces does not fix it.

### `$json` gets replaced by whatever ran last

**Symptom:** a Code node or a Data Loader embeds the wrong object, often an API
response instead of the document you assembled.

**Cause:** `$json` is the *current* item. Any node between your producer and your
consumer replaces it.

**Fix:** reference the producer by name:
`={{ $('Assemble Document').item.json.text }}`. In "run once for all items" mode
prefer `$input.first().json` over bare `$json`.

### Binary data in a Code node is not base64

**Symptom:** decoded content is garbage; a downstream model reports the file as
corrupted.

**Cause:** with filesystem binary mode, `item.binary.data.data` is the literal
marker `filesystem-v2`, and `.id` is a path, not content.

**Fix:** `const buf = await this.helpers.getBinaryDataBuffer(0, 'data');`
Works for both memory and filesystem modes. Or use an Extract From File node.

### A downloaded text document carries a BOM

**Symptom:** the first field of a parse is subtly wrong, or a heading match
fails on line 1 only.

**Fix:** `text.replace(/^﻿/, '')` before parsing or embedding.

---

## Activation and triggers

### A workflow that will not activate

Check, in order: a trigger node missing a required credential (some node types
block activation outright); a webhook or form **path collision** with another
workflow (409); an edit made to a path while the workflow was active.

### Editing a form or webhook path in place

**Symptom:** the old path still answers, the new one 404s.

**Fix:** deactivate, edit, activate. The registration happens on activation.

### Form-completion nodes leave the execution in `waiting`

**Symptom:** the execution never appears finished; the executions list does not
show it.

**Cause:** a form flow parks in the `waiting` state by design. Waiting
executions are not in the standard list.

**Fix:** read the execution by id (or from logs). When referencing an earlier
form node's data, use `.first()` rather than assuming a current item.

### The Wait node's limit reads the wrong response

**Symptom:** a Wait configured with a limit resolves after 24h instead of the
intended window.

**Cause:** the limit expression resolves against the most recent HTTP response
rather than your intended data node.

**Fix:** reference the data node explicitly: `$('Data Node').first().json...`.

### Non-webhook triggers cannot be fired externally

Manual, Schedule, and polling triggers reject API/MCP execution ("workflow
cannot be triggered externally"). Add a temporary Webhook trigger plus a seed
node for testing, and remove it before handoff. Reactivating a polling trigger
**resets its baseline**, so re-seed test data each cycle.

### The CLI cannot run a Data Table node, whatever the module env says

**Symptom:** `n8n execute --id <id>` fails at the first Data Table node with
`Attempted to use Data table node but the module is disabled`, on an instance
where data tables plainly work: the UI lists them, the public API reads and
writes their rows.

**Cause:** modules load per process. The server process enables the data table
module; the `execute` command starts its own process that does not. The error
names the module, so it reads as an instance misconfiguration and sends you
into compose files that are already correct.

**Fix:** run it from the UI, or from a trigger the main process handles.
Setting `N8N_ENABLED_MODULES=data-table` on the exec does not help. Since
manual triggers cannot be fired externally either (above), the working recipe
for verifying a data table workflow without a human at the canvas is the same
temporary Webhook trigger: wire it, activate, `curl` it, then remove it and
redeploy clean.

**Observed 2026-08-26 on 2.35.5.**

### A polling trigger on its own output folder self-triggers

**Symptom:** a workflow that writes a file into a watched location loops.

**Fix:** write generated output to a different location than the one the trigger
watches. Folder triggers are typically non-recursive, which hides the loop until
volume grows.

---

## Portability

### Credentials bind by id AND name

**Symptom:** an imported workflow shows "credential not found" on an instance
that has a credential with exactly that name.

**Cause:** the node's `credentials` block carries both `id` and `name`; the id
is instance-local.

**Fix:** remap credential ids on import, then reactivate. This is why raw
workflow JSON is not portable and why environment sync moves credential **stubs
only**, never values.

### The workflow API has no upsert, so a second run forks the workflow

**Symptom:** you re-run a promotion or sync script and the target now has two
workflows with the same name. Worse, if the script keeps an id map, the map now
points at the copy, so your next update lands on the copy while the published,
verified original goes stale.

**Cause:** `POST /api/v1/workflows` always creates. There is no upsert, and
nothing about the response tells you a same-named workflow already existed.

**Fix:** keep an id map keyed by the source workflow's id, refuse to create when
the map already has an entry, and require an explicit update flag that `PUT`s to
the mapped id. When you do repair a fork, fix the map **before** the next update,
not after: deleting the copy while the map still points at it silently sends the
next write to a dead id.

Observed 2026-09-04. Related: sub-workflow references are by id, so a fork also
means half your callers point at one copy and half at the other.

### A create rejected whole because one node names an unknown credential

**Symptom:** `POST /api/v1/workflows` returns 400 `The workflow you are trying to
save contains credentials that are not shared with you`. Nothing is created, and
the message names no node.

**Cause:** the node's `credentials` block carries an instance-local id. On the
target that id belongs to nobody, and the create fails as a whole rather than
warning on the one node.

**Fix:** strip credential blocks during promotion and let a human pick them in
the UI. Promotion moves credential **stubs**, never values. To find the offender,
diff the credential ids in your payload against what the target actually has;
note the public API has no credential-list endpoint, so read the ids off an
existing workflow on that instance instead.

### Cloud validates credentials on publish; the CLI does not

**Symptom:** a workflow that published cleanly on a self-hosted or container
instance refuses to publish on Cloud: `Cannot publish workflow: 1 node have
configuration issues: Node "X": Missing required credential: <type>`.

**Cause:** `publish:workflow` on the container does not validate node
configuration. Cloud does, at publish time.

**Why it bites harder than it looks:** an unpublishable sub-workflow makes every
caller unpublishable too, because a caller cannot be published while it
references an unpublished sub-workflow. One node with a missing credential can
therefore block a whole chain that worked fine on the build instance.

**Fix:** attach the credential, or disable the node so the rest of the chain can
publish. Either way, "it published on the build instance" is not evidence it will
publish on the target. Observed 2026-09-04 on 2.35.5 vs Cloud.

### CLI export/import array mismatch

**Symptom:** `import:workflow --separate` fails on a file produced by
`export:workflow --all`.

**Cause:** `--all` without `--separate` writes a JSON **array**;
`import --separate` wants a directory of **flat** single-workflow objects.

**Fix:** export with `--separate`, or split the array before importing.

### API `PUT` rejects fields it just gave you

**Symptom:** `PUT /workflows/{id}` 400s on a body you got from `GET`.

**Cause:** the update allowlist is `name`, `nodes`, `connections`, `settings`
only, and unknown `settings` keys are rejected.

**Fix:** strip everything else and whitelist `settings` keys before the `PUT`.

### Data table rows have no `DELETE` on the collection

**Symptom:** `DELETE /api/v1/data-tables/{id}/rows` returns
`405 DELETE method not allowed`, on the same path where `GET` and `POST` work.

**Cause:** row deletion lives on sub-routes. `DELETE .../rows/clear` empties the
table. `DELETE .../rows/delete` takes a **required** `filter` query param, by
design, so that emptying a table has to be the thing you asked for.

**Fix:** `/api/v1/openapi.yml` is served off the instance without auth and is
that version's own truth about the routes. Read it instead of guessing, which
also surfaces `dryRun` on the filtered delete.

### A workflow moved into a project runs without its credentials and Data Tables

**Symptom:** `PUT /workflows/{id}/transfer` returns 204, the workflow is active
in the new project, and the first execution fails: "node does not have access
to credential", or `Data table with ID '...' could not be found in this
project`.

**Cause:** credentials and Data Tables are project-scoped like workflows, and
a transfer moves only the workflow. Credentials have their own transfer
endpoint; Data Tables have none, and the node binds the table by id.

**Fix:** move the build as a set. Credentials used only by the batch:
`PUT /credentials/{id}/transfer`. A credential other workflows share: a copy
created with `projectId`. Data Tables: recreate in the project, copy the rows,
rebind the node ids, archive the originals. `./scripts/organize.sh` in the toolkit does
each step, and `place` refuses the workflow until the project can reach
everything it binds. Full treatment in `n8n-project-organization`.
Found 2026-10-19 on n8n 2.35.5 when a five-workflow build went 0/5 on its
smoke run right after a clean transfer.

### Exported workflow JSON leaks

Workflow JSON embeds credential references, internal hostnames, sometimes literal
config. Scan before it enters a repo or a ticket. Never import a customer's
workflows wholesale into a testbed for that reason.

---

## Canvas and layout

- **Stickies need a header band.** Reserve roughly 300 px of height for the
  title area or the content renders truncated. Full sizing math in
  `n8n-canvas-docs`.
- **Default node pitch is too tight** (~220 px) for wide stage stickies. Spread
  the nodes first, then place stickies.
- **PATCH, do not re-POST**, when fixing an existing workflow: a fresh `POST`
  mints a new id and can collide on a webhook/form path.
- **Color key** used across these builds: green = human touchpoint, red =
  critical/failure path, blue = logic, orange = boundary, gray = documentation.

---

## Validation false positives

- **Parallel branch off one output.** Wiring a Respond node and a work branch to
  the same output is a deliberate pattern (answer fast, keep working). The
  validator flags the Respond node as a misplaced error handler. Ignore it; a
  live execution is the arbiter.
- Validation passing means the JSON is well-formed, not that the workflow is
  correct. Always re-`GET` after a write and inspect `connections`.

---

## Infrastructure-shaped surprises

### The encryption key takes everything with it

A changed `N8N_ENCRYPTION_KEY` invalidates every stored credential and API key at
once, presenting as `invalid signature` on a key that worked yesterday. Pin it
explicitly, never generate it per deploy, and treat any change as a
credential-rotation event. Details in `n8n-instance-ops`.

### Webhook URLs behind a proxy

If n8n hands out URLs that only resolve internally, set `WEBHOOK_URL` (plus
`N8N_HOST` / `N8N_PROTOCOL`). Browser callers additionally need the origin in
`N8N_CORS_ALLOW_ORIGIN` and a restart.

### Curl through a CDN without a User-Agent

A missing UA gets bot-flagged independently of any rule you configured. Always
send one when testing a webhook through a CDN or WAF.

### Version-boundary removals

Before assuming a feature exists, check the instance version against known
removals: Python in the Code node moved to external task runners (no in-process
Pyodide), and MySQL was dropped as a supported n8n database. A workflow that
"used to work" may be hitting a removal, not a bug.

---

## Adding an entry

Keep the three-part shape: **symptom** a person would actually type, **cause**,
**fix**. One entry per behavior. If it belongs to a single skill's domain and is
not surprising, put it in that skill instead; this file is for the traps.
