---
name: n8n-upgrade-plan
description: >-
  Plan and execute an n8n version upgrade on a customer instance without
  breaking the workflows that run there: inventory the node types and
  typeVersions in use, pull the breaking changes between the current and target
  versions from the docs server, decide what to re-test, take the rollback
  snapshot, upgrade, and reconcile the drift the upgrade creates. Use when the
  task mentions upgrading n8n, "is version X safe", a customer asking which
  version to run, doctor reporting a version gap, an n8n-mcp pin that trails
  the instance, or typeVersion drift after an upgrade. Not for upgrading the
  harness's own MCP server pin (knowledge/registry.yaml and the customer
  harness docs cover that).
---

# n8n upgrade plan

An upgrade is the one change that touches every workflow at once. The
customer's `RUNBOOKS/upgrade-n8n-safely.md` in the care kit holds the
operator steps; this skill is the engineering plan around it.

## 1. Know what runs

```bash
./scripts/doctor.sh prod                      # current version, reachability
./scripts/drift-check.sh prod                 # repo must agree with the instance first
./scripts/node-inventory.sh workflows/prod    # node types, typeVersions, mixed versions
```

The inventory is the list to check. A node type the estate does not use cannot
break the upgrade. Mixed versions of one type mean two code paths to test, not
one.

## 2. Pull the breaking changes

On the docs server (`n8n-docs`, no credentials), for each type in the
inventory:

```
get_node({ nodeType: "nodes-base.httpRequest", mode: "versions" })
get_node({ nodeType: "nodes-base.httpRequest", mode: "breaking" })
get_node({ nodeType: "nodes-base.httpRequest", mode: "migrations" })
```

`versions` lists the typeVersions the bundled n8n knows; `breaking` the
behavior changes between them; `migrations` what to change in parameters.
The bundled n8n version is in `tools_documentation()`; if it is older than the
target, bump the pin first (the registry flags this) or read the release notes
by hand at `docs.n8n.io/changelog/release-notes`.

Then the release notes for the range, for the changes no node schema carries:
env var renames and removals, task-runner defaults, database migrations,
licence or module changes (`N8N_DISABLED_MODULES`), and anything marked
"breaking" in a minor. Write the list into the change ticket.

## 3. Decide the test set

Re-test, in this order, on dev after the dev upgrade:

1. Every workflow with a node type that has a breaking entry in the range.
2. Every workflow with mixed versions of one type.
3. Every workflow with a Code node (runner changes), a webhook (path and auth
   handling), or an AI node (model and tool-calling changes land often).
4. One of everything else, by tag.

Existing eval datasets run as-is; `n8n-enterprise-delivery/EVAL_LOOP.md`.

## 4. Rollback point, then upgrade dev

```bash
./scripts/export-all.sh dev && git add -A && git commit -m "snapshot dev before upgrade to <x.y.z>"
```

Plus the database backup the runbook prescribes; the export is the workflow
rollback, the database backup is the instance rollback. Upgrade dev, run the
test set, read executions, not just status codes.

## 5. Reconcile the drift the upgrade made

An upgrade bumps `typeVersion` on nodes it migrates. `drift-check` will report
it as a parameter or typeVersion change. That drift is real and the decision
is explicit:

- adopt: `export-all`, review the diff with `wf-diff`, commit, so the repo
  carries the migrated version;
- or redeploy from the repo, if the migration changed behavior you do not want
  and the old typeVersion still runs on the new release.

Never leave the repo and the instance disagreeing after an upgrade; the next
promotion would carry the wrong version.

## 6. Promote the upgrade

Staging then prod through the customer's change window, same snapshot and
test discipline, same drift reconciliation. Record versions, dates and the
breaking-change list in `INSTANCE.md` and the runbook.

## Related

- `n8n-self-hosting/DAY2.md`: the upgrade mechanics per deployment shape.
- `n8n-instance-ops`: activation cache after a restart; webhooks after a
  proxy change.
- `n8n-gotchas`: version-boundary removals.
- `knowledge/registry.yaml` in the harness: when the n8n-mcp pin or the
  vendored skills trail the instance version.
