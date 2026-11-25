---
name: surrealdb-canonical-layer
description: Verify a SurrealDB-backed canonical layer directly, over the `surrealdb` MCP server, instead of writing a disposable Node script per check. Use whenever the user asks to confirm a batch of writes landed correctly ("did the FreedomFest speakers get tagged right", "do these people have an org relationship", "check that event's rows aren't duplicated"), whenever a new client/event/import needs its data audited for coherence, whenever setting up SurrealMCP for a new project, or when the user mentions "SurrealDB", "canonical layer", "client_access tagging", "affiliation edge", or names this skill directly. Encodes augment-it's live schema (persons/organizations/affiliations/observations/events) as the worked example, the per-table client_access shape (string[] on most tables, singular string on observations — a real inconsistency, not a typo), the flag-don't-fix verification discipline, and the read-only-vs-full-CRUD tradeoff of the official surrealmcp server. Generalizes past augment-it to any project (dididecks-ai, memopop-ai) that adopts the same schemaless-canonical-layer + observations-as-log pattern.
---

# SurrealDB Canonical-Layer Verification

A SurrealDB-backed canonical layer (persons/organizations/affiliations plus a
schemaless `observations` log, all multi-tenant via `client_access`) is
first live in `augment-it`, and the pattern — canonical entities + an
append-only observation log + client-scoped visibility — is the kind of
shape other Lossless projects (`dididecks-ai`, `memopop-ai`) are likely to
reach for too. This skill is the discipline for **querying that layer
directly to verify a batch of writes landed correctly**, replacing the
previous habit of writing a fresh disposable Node script
(`connect → signin → use → query`, deleted after) for every check.

Companion piece: `search-lossless-corpus` does the same job for the Chroma
corpus (MCP for raw access, a skill for the discipline on top). This skill
copies that shape for SurrealDB.

## Prerequisite — the `surrealdb` MCP server

Each project that wants this skill needs its own project-scoped `.mcp.json`
entry pointing at [surrealmcp](https://github.com/surrealdb/surrealmcp), the
official SurrealDB MCP server. It's a Rust binary with exactly two
distribution paths — build from source (`cargo install --path .`) or the
`surrealdb/surrealmcp:latest` Docker image. There's no npm/PyPI package, so
it can't be invoked the one-line `uvx`/`npx` way the `chroma` MCP server is.

**augment-it's wiring** (the reference implementation — copy this shape into
a new project rather than re-deriving it):

- `augment-it/scripts/mcp-surrealdb.sh` — a wrapper script that sources
  `.env` **relative to its own location** (`$(dirname "${BASH_SOURCE[0]}")`),
  not `$PWD` and not the launching shell's exported environment, then execs
  `docker run --rm -i --pull always -e SURREALDB_URL=... surrealdb/surrealmcp:latest start`.
  This matters because Claude Code's `${VAR}` expansion in `.mcp.json` only
  reads variables **already exported in the shell that launched `claude`**
  — it does not read `.env` files — and this repo's habit is sourcing `.env`
  per-command (`set -a; source ./.env; set +a`), not exporting at shell
  startup. The wrapper script sidesteps that dependency entirely.
- `augment-it/.mcp.json`:
  ```json
  {
    "mcpServers": {
      "surrealdb": {
        "command": "${CLAUDE_PROJECT_DIR:-.}/scripts/mcp-surrealdb.sh"
      }
    }
  }
  ```
  `${CLAUDE_PROJECT_DIR:-.}` (not a hardcoded absolute path) keeps this
  portable across machines — Claude Code sets that variable to the project
  root when spawning the server.
- Env vars the wrapper maps from this project's existing `SURREAL_*` names
  (`.env`) to surrealmcp's expected `SURREALDB_*` names: `SURREAL_URL` →
  `SURREALDB_URL`, `SURREAL_NS` → `SURREALDB_NS`, `SURREAL_DB` →
  `SURREALDB_DB`, `SURREAL_USER` → `SURREALDB_USER`, `SURREAL_PASS` →
  `SURREALDB_PASS`.
- After adding or editing `.mcp.json`, the tools don't appear in an
  *already-running* Claude Code session — reconnect (`/mcp`) or start a new
  session. `claude mcp list` from a shell confirms connectivity
  independently of whether the current chat session has picked up the
  new tools yet.

**Read-write, not read-only — flagged, not solved.** The credentials the
wrapper uses are the same full read-write credentials the application
services already use, and surrealmcp additionally exposes **Cloud instance
management** (create/pause/resume a SurrealDB Cloud instance) — capability
none of augment-it's own services need or use. This is more blast radius
than a verification connector strictly requires. If SurrealDB Cloud offers a
scoped read-only role, provisioning one specifically for MCP use is worth
doing before this becomes routine infrastructure rather than an occasional
verification tool — until then, treat every query through this connector
with the same care as a direct production database session, and never issue
a `Create`/`Update`/`Delete`/`Relate`/Cloud-instance tool call from a
verification pass without the user's explicit ask.

## The verification discipline

Given a batch of writes (an event import, a CSV run, a new client's first
data), confirm three things — **flag gaps, don't silently fix them**:

1. **The rows exist** with the fields the write path is supposed to set.
2. **Client tagging is correct on every row**, checked explicitly — never
   assumed from a filtered query (see below, this is the part that's easy
   to get wrong).
3. **The relationships exist** where the write path is supposed to create
   them (e.g., a person → org affiliation edge, an event-tie observation).

A gap is not automatically a bug. A person with no org affiliation can be a
correct outcome (skip is first-class in augment-it's design — not every
speaker's org is known or resolvable). An org created independently of any
person can be correct too. Report what's there and let the user judge
whether a given gap is expected or a real defect — don't auto-patch rows
during a "just verifying" pass.

### Client tagging is its own explicit check

**Do not infer correct tagging from a `WHERE client_access CONTAINS $client`
filter that returned rows** — that only proves the filter works on the rows
that already have the tag; it says nothing about rows from the same batch
that got created *without* it (e.g., a bug in a write path that forgets to
stamp `client_access`). Those rows would be invisible to the client's own UI
filters but still sitting in the shared multi-tenant table — exactly the
kind of gap a "does the data exist" check alone misses.

Re-run the same query **without** the client filter (scoped instead by
`source` or a time window), then check the tagging field on every row that
comes back:

```sql
-- Wrong way to "verify" tagging — this only proves the filter itself works:
SELECT * FROM persons WHERE client_access CONTAINS 'reach-edu';

-- Right way — pull everything from the batch, then inspect the field per row:
SELECT id, name, client_access FROM persons
  WHERE source = 'person-db-resolver' AND first_seen_at > time::now() - 3d;
```

**The tagging field is not the same shape on every table** — document this
precisely per project rather than assuming one shape everywhere. In
augment-it:

| Table | Field | Shape |
|---|---|---|
| `persons`, `organizations`, `events` | `client_access` | `string[]` (a row can be visible to more than one client) |
| `affiliations` (the `RELATE` edge itself) | `client_access` | `string[]` |
| `observations` | `client` | **singular `string`** — a real inconsistency in the schema as it stands, not a typo to silently "fix" without checking every write path first |
| `events` | `client` **and** `client_access` | both — redundant but real; check both when auditing this table |

## Query recipes (augment-it's live schema)

Raw SurrealQL, not a wrapper API — the MCP server just gives query access,
so these are copy-adapt starting points, run through whichever tool the
`surrealdb` MCP server exposes for raw queries (check the connected
session's tool list — the official server documents `Query`, `Select`,
`Insert`, `Create`, `Upsert`, `Update`, `Delete`, `Relate`, plus connection
and SurrealDB Cloud management tools; exact MCP-facing tool names depend on
the server key chosen in `.mcp.json`, e.g. `mcp__surrealdb__query`).

**Everything from a batch, by source, recent window** (the base pattern —
adapt the `source` value and window per check):

```sql
SELECT id, name, client_access, source, first_seen_at FROM persons
  WHERE first_seen_at > time::now() - 3d
    AND (source = 'person-db-resolver' OR source CONTAINS 'freedomfest')
  ORDER BY first_seen_at ASC;
```

**A person's affiliations** (empty result is not automatically a gap — see
above):

```sql
SELECT id, out.slug AS org_slug, out.complete_name AS org_name, kind,
       client_access, added_at
  FROM affiliations WHERE in = $person_id;
```

**All observations for a subject** (`observed_at` must be in the
projection to `ORDER BY` it — SurrealDB 2.x requirement, easy to trip on):

```sql
SELECT predicate, object, client, observed_at FROM observations
  WHERE subject = $person_id ORDER BY observed_at ASC;
```

**Everything tied to one event:**

```sql
SELECT * FROM events WHERE slug = 'freedomfest-2026';
-- then cross-reference observations WHERE predicate IN
-- ['speaker_at','sponsor_of','exhibitor_at','attended','partner_of']
-- AND object = <that event's id>
```

**Duplicate detection** — candidate matching (fuzzy name, LinkedIn URL) can
still miss a duplicate when the operator clicks "create" instead of
reviewing candidates, or when the same person's name varies across rows
(e.g., a title prefix present on one row and stripped on another). A quick
smell test after any batch: group by lowercased name within the batch
window and eyeball anything with count > 1.

```sql
SELECT name, count() FROM persons
  WHERE first_seen_at > time::now() - 3d
  GROUP BY name;
```

## Schema reference — augment-it (source of truth: the code, not this file)

If this drifts, trust `services/record-surrealdb-resolver/src/resolver.ts`
and `.../person-resolver.ts` in the `augment-it` repo, plus
`context-v/plans/Person-Aware-Canonical-Resolver-Extension.md` there — this
section is a snapshot, not the contract.

- **`persons`** — `id`, `person_uuid` (the wire-safe handle; RecordIds don't
  survive JSON/NATS round-trips), `name`, `linkedin_profile_url`, `headline`,
  `source`, `client_access: string[]`, `first_seen_at`/`last_seen_at`,
  `first_touched_by`/`last_touched_by`.
- **`organizations`** — `id`, `slug` (the cross-wire identity, never the
  RecordId), `complete_name`, `conventional_name`, `aliases: string[]`,
  `org_links`/`org_corpus`/`media_streams`, `domains`, `client_access:
  string[]`, `source`.
- **`affiliations`** — a real `RELATE` edge, TWO shapes in one table
  (since 2026-07-27, per augment-it's
  `context-v/plans/Org-Relations-Parent-Child-Peer-Plus-Org-Tags.md` and
  `services/record-surrealdb-resolver/src/org-relations.ts`):
  - person→org: `in` (person) → `out` (org), `kind` (the role/title
    string), `client_access: string[]`, `added_at`, plus the rating
    fields (`relevance` etc.).
  - **org→org** (explicit discriminator `edge_type: 'org_org'`): canonical
    direction `in` = child → `out` = parent, `rel: 'child_of' | 'peer'`,
    open-vocabulary `kind` (`funder_of`, `partners_with`, `agency_of`,
    `initiative_of`, `fund_of`, …), free-text `description`,
    `client_access`, `added_at`. One edge per org pair; parent/child/peer
    is projected at read time relative to the queried org. **Peer is the
    normal shape** — kinds like `funder_of`/`agency_of` ride peer edges;
    hierarchy is the special case (operator ruling 2026-07-27). When auditing, filter
    explicitly: person-side reads rely on `in.person_uuid` being present,
    org-side reads on `edge_type = 'org_org'`.
- **`observations`** — schemaless log, `subject`/`predicate`/`object`/
  `source`/`observed_at`/`client: string` (singular). Predicates grow
  freely: `has_name`, `has_linkedin_url`, `affiliated_with`, `located_in`,
  the event-tie family `speaker_at`/`sponsor_of`/`exhibitor_at`/
  `attended`/`partner_of`, the org-relation trail `related_to` /
  `relation_removed`, and `has_tag` — which since 2026-07-27 also tags
  **organizations** (subject = org RecordId; values like `Initiative`,
  `Program`, `Funder`, `Think-Tank` — per-client, deliberately never a
  field on the shared org row; vocabulary rides `tag_vocab`).
- **`events`** — `slug`, `name`, `client: string`, `client_access:
  string[]`, `source`, `first_seen_at`.

## Adapting this skill to a new project

When `dididecks-ai` or `memopop-ai` (or any future project) adopts
SurrealDB for a canonical layer:

1. Copy augment-it's `.mcp.json` + wrapper-script shape (Prerequisite
   section above) rather than re-deriving the env-var-expansion workaround.
2. Add that project's own schema reference section to this skill (or a
   sibling section) — don't assume augment-it's table names or the
   `client_access` shape-per-table transfer unchanged; verify against that
   project's actual write paths the same way this file cites augment-it's.
3. The verification discipline (flag-don't-fix, tagging-is-its-own-check,
   relationships-checked-explicitly) is project-agnostic and carries over
   directly.

## See also

- `search-lossless-corpus` — the Chroma precedent this skill's shape (MCP
  for access, skill for discipline) is copied from.
- `augment-it/context-v/plans/SurrealDB-MCP-Plus-Skill-for-Canonical-Layer-Verification.md`
  — the plan this skill was built from.
- `augment-it/context-v/plans/Person-Aware-Canonical-Resolver-Extension.md`
  — the schema and write path this skill reads, doesn't reinvent.
- [SurrealMCP GitHub](https://github.com/surrealdb/surrealmcp)
