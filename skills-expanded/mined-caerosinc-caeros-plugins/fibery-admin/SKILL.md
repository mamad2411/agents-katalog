---
name: fibery-admin
description: Fibery workspace operations - import or sync data from external tools via connectors, audit the activity history to find what changed or what was deleted, and check who can access which spaces, databases, and entities. Use when getting data into Fibery, investigating a disappeared or unexpectedly changed entity, or answering access and permission questions.
---

# Fibery workspace operations

Three jobs live here: getting data in, finding out what happened, and knowing
who can see what.

## Getting data in

Fibery separates three things, and the user's answer changes what you build:

- **Import** is a one-time copy. The data becomes ordinary Fibery entities you
  can edit freely.
- **Integration / continuous sync** keeps a database mirrored from the source.
  Synced fields are typically read-only in Fibery, and the source stays
  authoritative.
- **Two-way sync** is only available for specific connectors.

`get_connectors_list` returns the catalog with, for each connector, its `id`
and whether it supports import, import into an existing database, and
continuous synchronization. Read those flags rather than assuming: most
connectors cannot import into an existing database, only into a new one.

The catalog covers Jira, Linear, GitHub, GitLab, Bitbucket, Notion, Airtable,
Trello, Asana, ClickUp, Productboard, Intercom, Zendesk, Discourse, HubSpot,
Stripe, Chargebee, Braintree, Slack, Email, Google Calendar, Readwise,
Markdown, CSV, and Fibery itself, among others.

### Before calling `get_manual_import_link`

You must have all three answers. Ask if you do not:

1. Where is the data coming from?
2. One-time import, or continuous sync?
3. Into a new or existing Space, and which one? If the target Space or Database
   does not exist, check `schema`, and ask the user to create it or offer to
   create it with `fibery-schema` first.

```json
{"spaceName": "Product", "isSync": true, "connectorId": "notion-app", "dbName": "Task"}
```

The tool returns a link the **user** opens to finish the connection and
authorize the source. You cannot complete the import yourself. Say that
plainly rather than implying the data is on its way.

If the source has no connector, CSV is the fallback: offer to extract the data
into CSV and import through `csv-connector`, which is one of the few that can
import into an existing database.

## Auditing history

`search_history` searches the workspace activity log. Every parameter is
optional; the default is the last 24 hours, up to 50 items.

Actions: `created`, `updated`, `deleted`, `collectionItemAdded`,
`collectionItemRemoved`, `archived`, `restored`, `permissionsChanged`.

You can also filter by `authorUserId`, `entityId`, `entityPublicId` (requires
`database`), `entityName`, `entityState` (`EXIST`, `DELETED`, `ARCHIVED`), and
`schemaChange` (`fieldChange`, `databaseChange`, `spaceChange`).

### Three traps

**Automatic changes are hidden by default.** Changes from automations,
integrations, formulas, and auto-linking are filtered out. For a database
created by an integration, that filter removes *everything* and you get an
empty result that looks like "nothing happened". Pass
`excludeAutomaticChanges: null` to include them.

**`database` must be the exact full `Space/Database` name.** A bare `"Task"`
fails with `Database "X" not found`. Confirm against `schema` first.

**Results are paginated and may be partial.** If the response has
`hasNext: true`, you have seen a slice. Call again with `sinceItem` set to the
previous response's cursor and repeat until `hasNext` is false. Reporting a
first page as if it were the whole answer is a real failure mode here.

The range between `since` and `until` cannot exceed 12 months.

### Investigating a vanished entity

```json
{"database": "Projects/Task", "actions": ["deleted", "archived"]}
```

Archived is recoverable and deleted generally is not, so establishing which one
happened is the first useful thing you can tell the user.

Full history of one entity:

```json
{"entityPublicId": "42", "database": "Projects/Task"}
```

## Access and permissions

`display_schema_capabilities` returns the current user's access per space and
per database. Pass `spaces` to scope it, or omit for the whole workspace.

Each entry is one of:

- `'no-access'`
- `'entity-level'`, meaning no space or database grant, but access to at least
  one entity through an entity-level template
- `{level, templateId, isDefault, url}` for standard template-based access,
  where `isDefault: false` means a custom template
- `'derived-per-field'`, which applies only to `fibery/file` and
  `comments/comment`

The response also carries `levelInfo` describing what each level actually
permits, so you can explain a grant rather than just naming it.

`display_entity_capabilities_via_sharing` goes one level deeper for specific
databases, returning three separate paths to entity access: `entityLevelGrants`
(shared directly), `indirectEntityLevelGrants` (propagated from a related
entity), and `assigneeGrants` (granted by an assignment rule on a People
field). Assignee grants are sampled, up to 10 entities per rule, so treat that
list as illustrative rather than complete.

### The rule that governs all of it

**Capabilities accumulate. They never override.** Space-level, database-level,
per-entity grants, and propagation from related entities all add together. To
work out what someone can do with a specific entity, take the union of every
source. Never conclude "no access" from one source alone.

Note also that these tools report the **current user's** access, the account
the MCP server is connected with. They do not answer "what can Alice see"
unless the session belongs to Alice.

## Why access matters for every other Fibery task

An empty query result has two very different explanations: the data is not
there, or the user cannot see it. Before telling someone their database is
empty, check `display_schema_capabilities` for that database. Reporting a
permission boundary as missing data sends people looking for a problem that
does not exist.
