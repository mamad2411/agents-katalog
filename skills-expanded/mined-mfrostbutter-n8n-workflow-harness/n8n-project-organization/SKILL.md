---
name: n8n-project-organization
description: >-
  Organize workflows and credentials on an n8n instance: which project, which
  folder, which tags, and which project owns each credential. Use before the
  first deploy of any demo, PoC or engagement build, when a workflow is being
  created or moved on an instance, when a credential is created or has to
  follow a workflow into a team project, when an instance has grown a flat list
  of untagged workflows, and whenever the user says project, folder, tag,
  organize, "put it in a project", "move the credential", "who owns this", or
  organize place stops on a scope check. Every workflow is tagged, in a project
  and in a folder before it is considered built; lint --require-placement and
  organize place refuse anything else. Covers the placement declared in the
  workflow JSON, the organize tool, the credential-follows-the-workflow rule
  and its API, and the audit.
---

# Organizing an n8n instance: projects, folders, tags, credentials

A workflow that is not placed is not built. Every demo, PoC and engagement
workflow carries its placement in its JSON, `organize place` applies it after
the create, and `organize audit` reports what drifted. The rule exists because
an instance with ninety untagged workflows at the root of a personal project is
where every "which one is live" conversation goes to die, and because a
workflow moved into a team project without its credentials fails at runtime
after a clean deploy.

Scope boundaries:

| Task | Skill |
|---|---|
| Roles, RBAC matrices, SSO provisioning, what projects do and do not isolate | `n8n-enterprise-delivery` |
| The create itself, activation, publish state | `n8n-instance-ops` |
| Moving a workflow between environments | `n8n-promotion-pipeline` |
| Folder CRUD through the community MCP (`n8n_manage_folders`), data tables through `n8n_manage_datatable` | `n8n-mcp-tools-expert` |

## The rule

Before a workflow is created anywhere, its JSON names:

```json
"tags":    ["acme", "order-intake", "api"],
"project": "Acme Corp",
"folder":  "Order intake"
```

- **`tags`**: a customer or product tag, a build tag, a role tag. At least one;
  three is the pattern. Lowercase, hyphenated, reused across the instance.
- **`project`**: a team project by name, or `personal`. One project per
  customer on a shared build instance; one per department or team on the
  customer's own instance (that is what they will bill by). `personal` is for
  throwaway probes only, and the audit lists them.
- **`folder`**: a path (`A/B`), one folder per build. The project root is not
  organized; `place` refuses an empty folder.

`./scripts/lint-workflow.sh --require-placement` fails the file offline when
any of the three is missing; `npm run lint` and the CI templates pass the flag.
`./scripts/organize.sh place` checks the rest against the instance before it
writes: the project exists, and it can reach every credential and every Data
Table the nodes bind. A generator that writes workflow JSON writes these three
keys. The keys are not part of the n8n schema; the public API ignores them on
a create and `export-all` does not emit them, so keep them in the repo copy and
carry them across an export (`wf-diff` ignores them).

Four things are project-scoped: workflows, folders, credentials, Data Tables.
A build moves as a set or it does not run.

Role tags, keep the vocabulary small: `api` (a webhook entry point),
`sub-workflow`, `agent`, `stand-in` (a mock that will not be promoted), `ops`
(error workflow, seed, housekeeping), `monitoring`, `deprecated`.

## The tool

`scripts/organize.mjs` (wrapper `./scripts/organize.sh`), Node built-ins only.
Defaults to dev; a named environment needs its own `N8N_API_URL_<ENV>` and
`N8N_API_KEY_<ENV>` pair, since every command here writes.

| Command | Does |
|---|---|
| `./scripts/organize.sh audit [env]` | Every project with its workflow, folder, credential and data table counts; untagged workflows; workflows left in a personal project when the instance has team projects; credential and data table scope violations. `RESULT: ok` or findings, exit 1 on findings. Run it at the start of a session on a shared instance and before a handoff. |
| `./scripts/organize.sh place <file\|dir> [env] [--dry-run]` | For every workflow JSON with an id: move the credentials only this batch uses into the project, transfer the workflow, create the folder path, set the folder, replace the tags, verify. Dry run prints the plan and writes nothing. |
| `./scripts/organize.sh credentials <name>... --to <project> [--env e] [--force]` | Transfer credentials into a team project. Refuses when a workflow outside the project still uses one, because the move takes it away from that workflow; `--force` moves it anyway and says how many lost access. The guard asks before a forced move. |
| `./scripts/organize.sh tables <name>... --to <project> [--env e] [--no-rows]` | Copy data tables into a project (schema, rows), archive the originals, print the id map to rebind the nodes with. |
| `./scripts/organize.sh project <name> [env]` | Create a team project if it is missing (licensed instances only). |

`place` transfers first, then sets the folder with a `PUT`, then the tags,
and only then reads the publish state back, because the folder write creates a
version. On an active workflow that leaves an unpublished draft; the report
says so, and `publish_workflow` on the official server clears it.

## Credentials follow the workflow

A workflow in a team project executes only with credentials that project owns
or has been shared with. Nothing warns at create time; the first execution
fails with "node does not have access to credential". So:

1. **Create the credential in the project from the start.** `POST /credentials`
   takes `projectId`; `n8n_manage_credentials` and the UI's project picker do
   the same. A credential made in your personal project and used from a team
   project is a time bomb.
2. **When a batch moves, its exclusive credentials move with it.** `place`
   computes this: a credential whose every live user is in the batch is
   transferred (`PUT /credentials/{id}/transfer`). One that another workflow
   still uses is a stop, not a move.
3. **A shared credential gets a project-scoped copy.** A `Postgres (shared)`
   credential serving six workflows in the build and five outside it cannot
   move without breaking the five. The project gets `Postgres (Acme Corp)`,
   same endpoint, created with `projectId`, and the build is repointed.
   Sharing a credential across projects exists in the UI only; the public API
   can transfer, not share, so do not plan an automation around sharing.
4. **Transfer removes the old owner.** `shared` on the credential afterwards
   lists the destination only. There is no undo except another transfer.
5. **Check with the list, not the workflow.** `GET /credentials` returns
   `shared[]` with project id, name and role; that is the only place
   ownership is visible. `credential:user` in that list is a share, not
   ownership; it is enough for execution.

## Data Tables are project-scoped too, and do not transfer

A Data Table node resolves its table inside the workflow's own project. The
first execution after a move fails with `Data table with ID '...' could not be
found in this project`. The public API has no transfer for tables, so:

1. `organize.sh tables <name>... --to <project>` recreates each table inside
   the project (`POST /data-tables` with `projectId`, same columns in the same
   order), copies the rows page by page, renames the original
   `zz-archived-<date>-<name>` (archive, never delete) and prints the old to
   new id map.
2. Rebind the nodes. The node holds the table **id**, not the name, so every
   `dataTableId.value` changes: in a generator that is one ids file; by hand it
   is one node at a time. Then update the workflow.
3. Re-seed what the build seeds (config tables), rerun the smoke test.

The audit and `place` check this the same way they check credentials: a table
outside the workflow's project is a stop, with the command named. Create
tables in the project from day one (`projectId` on create; `create_data_table`
on the official server and `n8n_manage_datatable` on the community one take
it), and name the project in the table name only when one instance holds
several environments.

## Reading placement back

The public API tells you less than it accepts:

- A workflow's project: `GET /workflows/{id}` has `shared[]`; the entry with
  `role: workflow:owner` carries `projectId`. The list endpoint filters by
  `projectId`.
- A workflow's folder: write-only. `parentFolderId` goes in on `PUT
  /workflows/{id}` and never comes back. Verify through the folder:
  `GET /projects/{p}/folders/{f}` reports `totalWorkflows` (recursive).
- Folder listing: `GET /projects/{p}/folders?take=100&skip=0` with `count`.
  The `filter` query parameter rejects JSON that contains reserved
  characters, so list and match client-side. `projectId` may be the literal
  `personal`.
- Tags: `PUT /workflows/{id}/tags` replaces the whole set; names resolve to
  ids through `GET /tags`, creating what is missing.

## Transfer and the running workflow

`PUT /workflows/{id}/transfer` with `destinationProjectId` keeps the workflow
active and keeps its id, webhooks and executions. On n8n 2.35 a set of nineteen
workflows moved live without a redeploy of the gateway in front of them. Two
things to do anyway:

- Run the build's smoke or golden set after the move. The runtime check that
  matters is the credential one above, and only an execution proves it.
- Re-read the publish state (`versionId == activeVersionId`). A folder write is
  a `PUT` and therefore a new version; a sub-workflow (Execute Workflow
  Trigger) published through the container CLI needs that publish again after
  any `PUT`, which is why `place` runs before the publish, not after.

## Starting a new build

1. `./scripts/organize.sh audit dev`. Know what is there before adding to it.
2. Project: an existing one for the customer, or `organize.sh project "<Customer>"`
   on a licensed instance. On Community there is only `personal`; say so in
   `AGENTS.md` and use the folder for the structure.
3. Credentials in that project, by name (`Postgres (acme)`, `Acme API (dev)`);
   the environment in the name when there are several.
4. Workflow JSON with `tags`, `project`, `folder`. A generator writes them.
   `./scripts/lint-workflow.sh <file> --require-placement` before the create.
5. Create it on dev (`n8n_create_workflow`, or `create_workflow_from_code` on
   the official server), write the returned id into the repo copy, then
   `./scripts/organize.sh place <file> dev`.
6. `./scripts/organize.sh audit dev` again; `RESULT: ok` is the bar.

## Retrofitting a grown instance

`audit` lists the untagged and the personal-project workflows. Take them one
build at a time: write the three keys into the exported JSON, `place --dry-run
<dir>`, read the credential plan, create the project-scoped copies the plan
asks for, `place <dir>`, run the build's smoke test. A snapshot of the live JSON
before the first move is the rollback point (`export-all` and a commit),
because a transfer has no undo and a folder is never readable back.

## What projects do not do

Projects are access separation inside one instance, not isolation: one
encryption key, one execution table, instance-global variables and tags. The
chargeback a customer wants per project is an Insights filter on `projectId`
for executions and a custom build for anything else. Detail and the role
matrices: `n8n-enterprise-delivery`.
