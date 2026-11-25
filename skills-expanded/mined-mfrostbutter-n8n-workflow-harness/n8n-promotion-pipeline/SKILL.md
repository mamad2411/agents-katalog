---
name: n8n-promotion-pipeline
description: >-
  Move n8n workflows between environments the supported way: the official
  @n8n/cli promotion environments (provider, one environment per direction,
  connect, promote, list-changes, reviewed-commit apply), .n8np package export and import with
  conflict and binding policies, source-control pull, and the gates that run
  before any of them. Use when the task is to promote dev to staging or prod,
  set up a promotion environment or Git provider, review what differs between a
  project and its branch, apply a reviewed commit, export or import a package,
  wire credential or data-table bindings across instances, build a CI promotion
  job, or decide between native promotion, source-control environments, package
  files and the harness deploy script. Not for building a workflow (authoring
  skills) or editing a live one in place (n8n-instance-ops).
---

# n8n promotion pipeline

Rewritten 2026-11-17 from `@n8n/cli` 0.27.0, the pin and the npm `latest`
tag (`n8n-cli --help` and the skill the package ships). The 1.x line is
tagged `rc`; the pin stays on `latest`. The CLI is official
(`github.com/n8n-io/n8n`, package `@n8n/cli`). Re-check the command surface
with `npx @n8n/cli@<pin> --help` when the pin moves; this file is a cache of
that output, not the source.

Run the CLI as `npx n8n-cli` only after `npm ci`, or as `npx @n8n/cli@0.27.0`.
The bare name `n8n-cli` on the npm registry is an unrelated third-party
package, and `npx n8n-cli` downloads it when the pinned one is not installed.

**Model change at 0.25.0.** Up to 0.24.0 a promotion *connection* held both
directions as `configs.promote` and `configs.apply`, each cloned with
`clone <id> <direction>`. From 0.25.0 a promotion *environment* is one
direction on one repository, created and connected on its own; the topic is
`promotion-environment`, `clone` is `connect`, `set-config` is `update` with
`settings`, and `--expectedConfigId` is `--expectedEnvironmentId`. Run
end to end on a licensed n8n 2.48.6 on 2026-11-19 with a GitHub repository
over an SSH deploy key: provider `create`, environment `create`, `connect`,
`get`, `list-changes` in both directions, `promote-selection`,
`apply-selection` with the three `--expected-*` flags (exit 0, and exit 3 on
a stale SHA), `add-project`, `remove-project`, `disconnect`. Written from the
CLI's help only, not run: the full `promote` and `apply`, exit 4 and
`apply-continue`, `create-missing-projects`, a GitLab provider.

**The CLI version has to match the instance.** The package and promotion
request bodies are strict and change between releases, in both directions: a
CLI newer than the instance fails the same way as one that is older.
`package export` answering `request/body must NOT have additional properties`
is that mismatch, not a bad workflow. Measured 2026-11-16 and 2026-11-17:

| Instance | `package export` accepted | Rejected |
|---|---|---|
| n8n 2.35.5 | 0.14.0, 0.15.0 | 0.16.0 through 0.27.0 |
| n8n 2.44.6 | 0.23.0 through 1.2.1 | 0.22.0 |
| n8n 2.48.6 | 0.27.0 | not tested |

`promotion-provider` and `promotion-environment` answer 404 on n8n 2.35.5
(promotions arrive in 2.40). On n8n 2.48.6 with 0.27.0 the routes answer,
`package export` works for a workflow and for a project, and a key without
the `promotions:*` scopes gets `403 Forbidden` on every promotion command:
an API key keeps the scopes it was created with, so a key older than the
feature needs replacing. So 0.27.0 is the harness default for a current
instance, and an engagement pins the release that its own instance accepts:
try `npx @n8n/cli@<version> package export -w <id>` on dev, write the version
that works into the engagement `CLAUDE.md`, and move it with every n8n
upgrade. For a pre-0.25 CLI the promotion topic is `promotion-connection` and
the flags are the old names (`@n8n/cli@0.24.0 --help`).

The question this skill answers: a workflow works on dev. How does it reach
production so that a reviewer saw it, the target has what it needs, and
nothing arrives by hand?

## Four ways a workflow moves, and when each is right

| Mechanism | What it is | Use when |
|---|---|---|
| **Promotion environments** (`n8n-cli promotion-*`) | Instance-to-instance through a Git repo. Source instance `promote`s (export, commit, push); target instance `apply`s (reset to branch tip, import). Reviewed-commit apply pins the exact SHA a human reviewed. | Licensed customer with two or more instances and a Git host. The default for an enterprise engagement. |
| **Source control environments** (Settings > Environments; `n8n-cli source-control pull`) | Each instance bound to a branch. Push from dev, PR between branches, pull on prod. The older feature; still the one with the in-product UI. | Customer already runs it, or wants the editor-side push button. One direction per instance. |
| **Packages** (`n8n-cli package export|import`, `.n8np`, beta) | A file carrying selected workflows, folders or projects plus stubs, with explicit conflict and binding policies on import. | Air-gapped targets, one-off migrations, moving a demo into a customer tenant, seeding a tenant from a template set. |
| **Harness deploy** (`./scripts/deploy.sh <file> [env] [--confirm]`, public API) | `validate` and `lint-workflow --require-tags --require-placement` first, then create or update by id or name, placement (transfer, folder, tags), read-back compared with the file. Never activates. | Dev, and community edition instances where none of the above exists. Never the production path on a licensed customer. |

Decide on day one, write it into the engagement `CLAUDE.md` under Promotion
path, and never mix two mechanisms on one target: each assumes it owns the
instance's state.

**Community edition** has no promotions, no environments and no team
projects or folders over the public API (`/projects` is 403, the folder routes
403 or 404, `n8n-cli project list` fails on the license). The path is the
harness deploy: one `workflows/<env>/` per instance, `deploy.sh <file> dev`
on the build instance, `deploy.sh <file> prod --confirm` on the second with
its own `N8N_API_URL_PROD` pair; placement is tags only, with
`N8N_PLACEMENT_FOLDERS=skip` set in that instance's `.env` so `place` and
`deploy` do not stop on the missing folder (they say it once and move on).
Credentials and variables are recreated on the target by name from the
`lint-workflow` manifest. `package export` and `import` do work on community
edition for a one-off move; `promotion-*` and `source-control` do not.

## What travels and what never does

Same rule for all three product mechanisms:

- Travels: workflow JSON, tags, folders, projects, credential **stubs**
  (id, name, type, expression-valued fields only), variable **stubs** (id,
  name), data table **schemas**.
- Never travels: credential values, variable values, data table rows,
  execution history, the encryption key, instance settings.
- Package export has `--credentialExportPolicy expression-values-only|no-values`
  and `--includeVariableValues`; literal credential values never travel under
  any policy.
- Since n8n 2.41.0 (PR n8n-io/n8n#39091, 2026-09-18) the exported package
  keeps `versionId` and `publishedVersionId` in `workflow-metadata.json`, not
  in `workflow.json`, so a publish no longer dirties the content file.
  Packages exported before that fail metadata validation on import.

Consequence: every target needs its credential values, variable values and
data table rows set up as **environment setup**, before the first apply.
`scripts/lint-workflow.sh` prints the list (the promotion manifest) per
workflow.

## Gates before anything is promoted

Run in this order on the source side. All offline, all in `scripts/`.

1. `drift-check.sh dev` clean: the repo and the instance agree, so what you
   review is what will move.
2. `validate.sh <file>` on every changed workflow: well-formed.
3. `lint-workflow.sh workflows/dev --require-tags`: no environment literal
   hosts, every credential named, no `$env`, tags present, error workflow set,
   and the manifest of credentials and variables the target must already have.
4. `wf-diff.sh <base> <head>` on each changed file: the semantic change a
   reviewer signs off on, not a canvas move.
5. The customer's review: a pull request on the promotion branch, or
   `list-changes` output pasted into the change ticket.

The CI templates in the engagement scaffold run 2 to 4 on every push.

## Promotion environments, end to end

Prerequisites: licensed instance with the promotions module; an API key whose
scopes include `promotions:*` (plus `variable:list` for promote when
workflows reference variables); a Git repository the customer owns; the CLI
pinned in the engagement (`npm i --save-exact @n8n/cli@0.27.0`) or run as
`npx @n8n/cli@0.27.0`. Configure with `N8N_URL` and `N8N_API_KEY` from the
engagement `.env`, never flags on the command line.

```bash
# 1. Provider: who may talk to the Git host. SSH returns a deploy key to add.
echo '{"name":"Customer GitLab","type":"git","auth":{"authType":"ssh-key","keyType":"ed25519"}}' \
  | n8n-cli promotion-provider create --stdin --json > provider.json
jq -r '.id' provider.json             # providerId for step 2
jq -r '.publicKey' provider.json      # add as a read-write deploy key

# 2. One environment per direction, each on the instance that uses it.
n8n-cli promotion-environment create --file=promote.json   # on the source instance
n8n-cli promotion-environment create --file=apply.json     # on the target instance

# 3. Connect each environment (for Git: clones its branch). Connecting one does not ready the other.
n8n-cli promotion-environment connect <promoteId>
n8n-cli promotion-environment connect <applyId>

# 4. Source side: see what differs, then promote.
n8n-cli promotion-environment list-changes <projectId> promote
n8n-cli promotion-environment promote <promoteId> -m "CR-1234: order intake v3"

# 5. Target side: review, then apply exactly the reviewed commit.
n8n-cli promotion-environment list-changes <projectId> apply --sort=updatedAt --order=desc --json > reviewed.json
jq '{commitSha, changes}' reviewed.json
n8n-cli promotion-environment apply <applyId> \
  --expectedEnvironmentId=<applyId> \
  --expectedBranch=$(n8n-cli promotion-environment get <applyId> --jq '.settings.branchName') \
  --expectedCommitSha=<full sha from reviewed.json>
```

Take the commit SHA from the same `list-changes` response as the rows; a
second request can read a newer commit. For one project the last two steps
are `promote-selection <projectId> -w <workflowId> -m "<ticket>"` on the
source and `apply-selection <projectId> -w <workflowId>` with the same three
`--expected-*` flags on the target. `list-changes ... apply` reports each
workflow as `new`, `modified` or absent when it already matches the branch,
and an apply of a `modified` workflow overwrites the target's copy with the
branch's.

`promote.json` (instance scope; a `projects`-scoped environment links team
projects with `add-project`):

```json
{
  "name": "Production",
  "scope": "instance",
  "providerId": "<provider id>",
  "remote": { "schemaVersion": 1, "remoteUrl": "git@gitlab.example.com:ops/n8n-flows.git" },
  "direction": "promote",
  "settings": { "schemaVersion": 1, "baseBranchName": "main", "createBranchOnPromotion": true }
}
```

`apply.json` is the same with `"direction": "apply"` and
`"settings": { "schemaVersion": 1, "branchName": "main" }`. The settings must
match the direction; direction and scope cannot change after the create.

`createBranchOnPromotion: true` is what gives the customer a pull request:
promote pushes a branch, the PR merges to `main`, prod applies `main`. With
`false`, promote pushes straight to the base branch and the review gate is
gone. Required field either way.

A provider of `"type": "gitlab"` (base URL in `config`, access token as
`auth.password`) can list what its token sees: `promotion-provider
list-repositories <id>` gives `remoteUrl` and `fullPath`, `list-branches <id>
<fullPath>` marks the default branch. Read both from there instead of typing
them.

### Exit codes that matter

| Exit | Meaning | Do |
|---|---|---|
| 0 | Applied | Verify with a real execution on the target, then record it |
| 3 | `source-changed`: the branch moved since the reviewed SHA | Review again. Nothing was imported |
| 4 | `blocked`: preflight found missing bindings, access or conflicts | Fix what `--json` lists under `preflight`, then run the printed `apply-continue` with the same three `--expected-*` values. Nothing was imported |

Always pass all three `--expected-*` flags or none. The SHA must be the full
SHA. Check `$?` or the `status` field before reading `counts`.

### Behaviors to design around

- `promote` exports **all team projects** on an instance-scoped environment.
  On a shared instance that puts every team's workflows in one repository.
  To promote one project, use `promote-selection <projectId> -w <id>...`
  against the instance promote environment: only the selected workflows, the
  folders that hold them and their tags are written.
- **Promote needs an instance-scoped environment on n8n 2.48.6.** A
  `projects`-scoped promote environment can be created, linked and connected,
  and `list-changes` reads through it, but `promote-selection` answers
  `Promote is only available on an instance environment. Project environments
  are not supported yet.` A `projects`-scoped **apply** environment works:
  `apply-selection` imported through one.
- The repository layout promote writes: `n8n/manifest.json`,
  `n8n/projects/<name>-<id>/project.json`, folders nested under it as
  `folders/<name>-<id>/folder.json`, each workflow as
  `workflows/<slug>-<id>/workflow.json` plus `workflow-metadata.json`, and
  `n8n/tags/<name>-<id>/tag.json`. That is the path a reviewer sees in the PR.
- `-m` is optional on `promote`; without it the commit message is generated.
  Always pass the change ticket.
- `promote` refuses a workflow on the branch that moved to a personal
  project (apply would delete it on the target), and a workflow or folder
  that moved to another team project while its old project still exists.
- `apply` moves workflows and folders within their project to match the
  branch and renames folders to the branch's names. A workflow or folder the
  branch and the instance hold in different projects is refused before any
  write.
- A team project that exists only in the package must exist on the target
  first: `list-missing-projects <applyId>`, then `create-missing-projects
  <applyId> [--admin <projectId>=<userId>]` creates it empty with the same
  id (exit 1 when one fails), then `apply-selection` per project.
- `apply-continue --confirmDestructiveChanges` also applies data table
  changes that remove or retype columns and deletes team projects the
  package does not hold. Never in CI; a human reads the preflight first.
- `apply` **resets the local checkout to the branch tip and overwrites the
  instance** to match. Workflows on the target that the branch does not
  carry are at risk; `apply-selection` removes instance workflows the project
  owns whose ids are absent from the branch. Export the target first
  (`export-all.sh prod` and commit) as the rollback point.
- `--force` on promote overwrites a diverged remote branch. Not in CI.
- `authType: token` means HTTP(S) username and password, not a Git host API
  token. `publicKey` is null for a token provider.
- `update` with `settings` replaces the whole settings object; send every
  setting.
- A project can have one project-scoped environment per direction; a
  direction without one uses the instance environment.
- `disconnect <id>` removes the local checkout and keeps the environment.
- A provider cannot be deleted while an environment uses it, and updating a
  provider's `auth` replaces the credentials of every environment on it.

## Packages

```bash
n8n-cli package export -p <projectId> -o release-2026-10-19.n8np \
  --versionPolicy published-strict \
  --credentialExportPolicy no-values \
  --dependencyPolicy fail

n8n-cli package import --file release-2026-10-19.n8np -p <targetProjectId> \
  --conflictPolicy new-version \
  --publishingPolicy preserve-published-state \
  --credentialMatchingMode name-and-type --credentialMissingMode must-preexist \
  --variableMissingMode must-preexist \
  --dataTableMissingMode create --dataTableSchemaConflictPolicy fail \
  --overwriteDeletionPolicy archive \
  --bindings '{"credentials":{"<sourceId>":"<targetId>"}}'
```

Policies worth stating in the handoff: `published-strict` refuses to export a
workflow that has unpublished changes, so what ships is what runs;
`must-preexist` for credentials and variables turns a missing value into a
failed import instead of a workflow that starts and fails later;
`overwriteDeletionPolicy archive` keeps the archive-not-delete rule.
New workflows always take the package ids (`--idPolicy source` is the only
value since 0.25.0), which is what makes sub-workflow references survive;
matched workflows keep their target ids. `--credentialConflictPolicy`
defaults to `keep-existing`: a matched credential on the target is never
renamed or rewritten unless the handoff says `overwrite`. Packages also carry
Agents (`--agentId` on export).

## Source-control environments

The older model: Settings > Environments binds an instance to a branch, push
from the editor, `n8n-cli source-control pull` on the target (or the UI).
Detail, including the no-conflict-detection rule and the one-direction-per-
instance rule, is in `n8n-enterprise-delivery/SOURCE_CONTROL.md`. Prefer
promotion environments for a new engagement; they carry reviewed-commit apply
and per-project scope, which environments do not.

## CI shape

Source instance, on merge to the promotion branch (or on a schedule):

```
export-all (source) -> commit -> validate + lint + wf-diff on the PR
  -> human review -> promotion-environment promote -m "<ticket>"
```

Target instance, on approval:

```
export-all (target) + commit        # rollback point
  -> list-changes apply --json      # capture commitSha
  -> apply --expected-*             # exit 3 or 4: stop, nothing imported
  -> health-check + a real execution of each changed workflow
```

Secrets in CI: `N8N_URL` and `N8N_API_KEY` per instance as masked variables.
The promotion API key is powerful (`promotions:*` plus whatever else it
carries); scope it to the project where the instance supports it, rotate it on
team change, and never reuse the dev key on prod.

## Handoff wording

Under Promotion in the customer's `HANDOFF.md`: the mechanism chosen and why
the other three were not; the environment names and ids per direction, scope, repo and branches; who
reviews and where (PR, ticket); the exact apply command with the three
`--expected-*` flags; what exit 3 and exit 4 mean and who acts; the
environment-setup list (credentials, variables, data table rows) per target;
and the rollback (`export-all` snapshot plus `apply` of the previous SHA).

## Related

- `CLI_REFERENCE.md` in this directory: the command and flag tables for
  `@n8n/cli` 0.27.0.
- `n8n-enterprise-delivery`: license tiers, RBAC, external secrets, the
  promotion checklist.
- `n8n-workflow-as-code`: making the diff a reviewer sees readable.
- `n8n-instance-ops`: the activation cache, which still applies after an
  apply that republishes a workflow.
