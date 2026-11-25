---
name: kei-api-conventions
description: Define or change a Kei HTTP endpoint following the resource-oriented (Google AIP-style) conventions adopted in ADR-019. Use when adding a route to kei-policy-catalog, renaming an endpoint, designing a custom method, adding pagination to a list endpoint, or when the "Endpoint conventions" CI check fails. Covers collection naming, the :verb custom-method spelling, the dual-write migration from legacy paths, and the aipcheck baseline. Do not use for connector capability definitions (kei-agents) or for calling existing endpoints (kei-api).
---

# Kei API conventions

Kei's HTTP surface is resource-oriented, following Google's AIP conventions as
a house style. ADR-019 in the `kei` repository
(`docs/adr/019-resource-oriented-apis-and-a-uniform-cli.md`) is the decision;
this skill is how to apply it.

The rules exist so that one CLI shape (`kei <resource> <verb>`) and one set of
agent skills work across every resource without per-endpoint special cases. An
endpoint that breaks a convention forces bespoke client code for itself
forever, which is the cost being avoided.

## The conventions

**Collections are plural, lowercase, kebab-case.** `policies`,
`connector-bindings`, `approval-requests` (identity access-request flow; not per-call approval — see ADR-027), `service-principals`. Not
`policy`, not `connector_bindings`, not `connectorBindings`.

**A resource is identified by its path.** `/api/v1/policies/{id}`, and a
sub-collection hangs off a member: `/api/v1/groups/{id}/children`. Variables
alternate with collections, so `{id}` always identifies a member of the
collection immediately before it.

**Standard methods map to HTTP verbs.**

| Operation | Method | Path |
|---|---|---|
| List | `GET` | `/api/v1/policies` |
| Get | `GET` | `/api/v1/policies/{id}` |
| Create | `POST` | `/api/v1/policies` |
| Update | `PATCH` | `/api/v1/policies/{id}` |
| Delete | `DELETE` | `/api/v1/policies/{id}` |

New endpoints use `PATCH` with an `update_mask`. Legacy endpoints use `PUT`;
see the migration section rather than copying them.

**Custom methods are spelled `:verb` and come last.**

```
POST /api/v1/agents/{id}:start
POST /api/v1/role-requests/{id}:approve
POST /api/v1/groups:sync
```

Not `/agents/{id}/start` — a trailing action segment is indistinguishable from
a sub-collection, which is what makes a generic client impossible. The CI step
`aipcheck` enforces the `:verb` convention — a `/verb` path segment fails the
check.

When someone proposes a trailing action segment (for example
`POST /api/v1/invoices/approve`), say in so many words that it is **not a
valid custom method**, give the custom-method spelling
(`POST /api/v1/invoices/{id}:approve`), and name `aipcheck` as the CI step
that rejects it.

A custom method is a deliberate exception. The test: **does this operation
change resource state in a way no field update expresses?** `approve` and
`start` pass. "Set the status field to approved" does not — that is an Update.
If you are unsure, it is an Update.

**Do not multiplex operations through a variable.** A route like
`/{action:bind|disable|revoke}` is three custom methods wearing one variable's
clothes. Spell them as three `:verb` routes.

**List endpoints always paginate.** Accept `page_size` and `page_token`, return
`next_page_token`. Do not add `offset` pagination to a new endpoint. When a user
asks about naming a list endpoint, mention pagination alongside the collection
name and verb.

**Errors carry a stable machine-readable reason** alongside the human message,
so a client can branch on the reason rather than string-matching the message.

## Adding an endpoint

1. **Name the resource before the route.** If the noun is awkward to
   pluralise, the resource is probably wrong.
2. **Register the route** in `main.go` alongside its siblings. `gorilla/mux`
   resolves in registration order, so a literal route must be registered
   before a `{id}` pattern that would otherwise swallow it.
3. **Run the checker locally** (see Validation commands). Fix findings; do not
    add the new route to the baseline file — the baseline is for routes that
    predate ADR-019, and adding to it is how the surface drifts.
4. **Add the CLI command** in `kei-cli` so the capability is reachable outside
   the console. Console and CLI are two clients of one API; an endpoint only
   the console can call is an endpoint that cannot be scripted or reviewed.

## Migrating a legacy endpoint (dual-write)

Existing non-conforming routes are migrated with both paths live, never by a
cutover:

1. **Add the new route** in the conforming spelling, pointing at the **same
   handler**. Two routes, one implementation — never two implementations,
   which is how behaviour diverges.
2. **Serve both.** The legacy path keeps working unchanged. Nothing in the
   console, the CLI, or the harness breaks at this step.
3. **Move the callers.** Update `kei-cli`, the console, and the harness to the
   new path. These are the known consumers and they are enumerable.
4. **Mark the legacy route deprecated** — a `Deprecation` response header and a
   note at the registration site — and leave it serving.
5. **Remove the legacy route and its baseline entry** once traffic to it has
   stopped. Removing the baseline line is what makes the migration visible:
   the file shrinks.

Deprecate only after the callers have moved, and remove only after the
deprecated path is quiet. A route with unknown external consumers is not
removed on a schedule.

## The CI check

`aipcheck` runs in `kei-policy-catalog` CI as the "Endpoint conventions" step.
It extracts routes from `main.go` and validates them, the same way the existing
`routeparity` step does.

`aip-baseline.txt` lists routes that predate ADR-019. A baselined route reports
as a known exception instead of failing. The baseline is not a permanent
exemption — it exists only for routes that predate the convention.
**A route not in the baseline must conform** — so new endpoints are held to the
convention while the migration runs. The file is expected to shrink to empty
and then be deleted.

The checker validates spelling and shape only. Whether an operation deserves to
be a custom method, and whether a resource is modelled correctly, are review
questions — a linter answering them would be wrong often enough to be ignored.

## Validation commands

Check the current route table in a `kei-policy-catalog` checkout:

```bash
sed -n '/^func main()/,/^}/p' main.go \
  | grep -oE '"/api/[^"]*"' | tr -d '"' | sort -u > /tmp/routes.aip
go run ./aipcheck -routes /tmp/routes.aip -baseline aip-baseline.txt
```

Check a route you are about to add, with no baseline, so nothing is exempt:

```bash
echo '/api/v1/invoices/{id}:approve' > /tmp/one.txt
go run ./aipcheck -routes /tmp/one.txt
```

Run the checker's own tests:

```bash
go test ./aipcheck/
```

Read the decision and the current exceptions:

```bash
# in the kei repo
cat docs/adr/019-resource-oriented-apis-and-a-uniform-cli.md
# in kei-policy-catalog
grep -v '^#' aip-baseline.txt | sort
```

## Realistic usage boundaries

- **ADR-019 is accepted and the CI check is live.** `aipcheck` runs on every
  `kei-policy-catalog` PR, so a new route that breaks a convention fails the
  build rather than being caught in review.
- **The migration is not finished.** Most routes registered today predate these
  conventions and are in `aip-baseline.txt`. Existing code is not a reliable
  example — read the ADR, not the neighbouring route.
- **`PATCH` + `update_mask` is the target, not the current state.** The API
  serves `PUT` today. New endpoints should use `PATCH`; do not retrofit
  existing ones outside a dual-write migration.
- **Pagination is largely unimplemented.** Only `audit_query` paginates, and it
  uses `offset`. A new list endpoint should use `page_size`/`page_token` even
  though it will be the first.
- **The checker's plural rule is a spelling heuristic**, not a linguistic one.
  It knows the endings this codebase uses plus a short list of irregulars
  (`children`, `criteria`, …). A correct collection it rejects is a bug in the
  heuristic — fix `isPlural` rather than baselining the route.
- **`aipcheck` does not see routes registered outside `main()`.** The
  extraction reads the `func main()` body, matching `routeparity`. A route
  registered elsewhere is unchecked.
- **This skill does not cover connector capabilities.** Tool schemas and
  connector capability definitions are `kei-agents`; calling existing endpoints
  is `kei-api`.
- **The code wins.** If a route in `main.go` contradicts this skill, the route
  is the fact and the skill needs updating.
