---
name: graphql-api-apps
description: Develop applications, dashboards, integrations and scripts that consume the JSON-SCADA GraphQL API served at /apollo by the server_realtime_auth module. Covers JWT authentication and RBAC behavior, the full schema (realtime tags, active alarms, SOE events, historical data, commands with acknowledgment tracking, alarm/event acknowledgment, point property updates, users/roles/audit trail), error codes, query limits, polling patterns, client code snippets, and the standalone PostGraphile historian server. Use when the user asks to build an app, web page, service, Node-RED/n8n flow, or script that reads or writes JSON-SCADA data via GraphQL, asks about the /apollo endpoint, or asks how to query tags/events/history or send commands programmatically with GraphQL.
---

# Building Apps with the JSON-SCADA GraphQL API

## Overview

JSON-SCADA exposes a GraphQL API at the **`/apollo`** access point, served by the
`server_realtime_auth` module (default `http://127.0.0.1:8080/apollo`, same HTTP server
that hosts the AdminUI and the OPC-like `/Invoke` API). It is an Apollo Server with
introspection enabled — any GraphQL client (Apollo Sandbox, Insomnia, Postman, curl,
graphql-request, Apollo Client) can discover the full schema.

It provides typed access to:

* **Realtime data** — tags/points with flexible filtering, station (group1) / bay (group2) listings, active alarms.
* **Events** — SOE (sequence of events) queries with time ranges, priorities, aggregation.
* **History** — raw historical values from the PostgreSQL/TimescaleDB historian.
* **Operation** — issue commands (controls) and track their acknowledgment, acknowledge
  alarms/events, silence beep, update point properties (annotations, notes, limits,
  alarm disabling, value substitution).
* **Administration** — users, roles, system settings, protocol configuration, audit trail.

Everything respects the same RBAC user rights as the rest of the platform.

Authoritative references in this repo:

* `src/server_realtime_auth/graphql-server.js` — the implementation, SDL schema is inline (single source of truth).
* `src/server_realtime_auth/README.md` — "GraphQL API" section with examples; also documents the `/Invoke` API and the roles schema.
* `src/graphql-server/` — separate standalone PostGraphile server for the SQL historian (see last section).

When the GraphQL API lacks something (e.g. server push), fall back to the `/Invoke` API
documented in the same README.

## Authentication

1. **Sign in** to obtain a JWT (the API shares auth with the whole platform):

```js
const res = await fetch(BASE + '/Invoke/auth/signin', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ username: 'admin', password: 'jsonscada' }),
})
// token arrives BOTH in the response cookie and can be reused from it:
const token = (res.headers.get('set-cookie') || '').match(/x-access-token=([^;]+)/)?.[1]
```

2. **Send the token** on every GraphQL request as the `x-access-token` **header** or
   **cookie**. Browser apps served from the same origin get the cookie automatically
   after login (use `credentials: 'include'`).

3. Sign out via `POST /Invoke/auth/signout`.

**Gotcha:** requests without a valid token do **not** get a GraphQL-shaped error. The
auth middleware answers `200` with `{ ok: false, message: 'Access not allowed...' }`.
Treat a response without a `data` key as "re-authenticate".

**No unauthenticated mode:** `/apollo` always enforces the token check, there is no way to
disable authentication in `server_realtime_auth`.

The endpoint path can be changed with the `JS_GRAPHQL_AP` environment variable (default `/apollo`).

## Calling the API

Plain HTTP POST is enough — no client library required:

```js
async function gql(query, variables) {
  const res = await fetch(BASE + '/apollo', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'x-access-token': token },
    body: JSON.stringify({ query, variables }),
  })
  const body = await res.json()
  if (!('data' in body) && body.ok === false) throw new Error('not authenticated')
  if (body.errors) throw new Error(body.errors[0].message + ' [' + body.errors[0].extensions?.code + ']')
  return body.data
}
```

## Queries

| Query | Purpose |
|---|---|
| `serverInfo` | name, version, `authenticationEnabled`, `mongoConnected` |
| `me` | username + combined role `rights` (use to enable/disable UI features) |
| `tags(filter, limit, skip, sortBy, sortDesc)` | flexible realtime point query |
| `tagsCount(filter)` | count matching points (for pagination) |
| `tag(tag)` / `tagById(id)` | single point by tag name / numeric point key |
| `groups1` / `groups2(group1)` | distinct station / bay names with point counts |
| `activeAlarms(group1, group2, limit)` | alarmed + out-of-normal points, most recent alarms first |
| `soeEvents(filter, limit, ascending)` | SOE events; defaults to last hour when no time range given |
| `historicalData(tags, timeBegin, timeEnd, limit)` | raw historian values; defaults to last hour |
| `commandStatus(commandHandle)` | acknowledgment state of an issued command |
| `userActions(filter, limit, skip)` | audit trail (admin only) |
| `users` / `roles` / `systemSettings` | administration (admin only) |
| `protocolDriverInstances` / `protocolConnections` | protocol config (credentials never exposed) |

`TagFilter` fields: `tags`, `ids`, `group1`, `group2`, `group3`, `type`
(digital/analog/string/json), `origin` (supervised/command/calculated/manual),
`alarmed`, `alarmDisabled`, `invalid`, `frozen`, `alerted`, `isEvent`, `substituted`,
`commandBlocked`, `tagContains`, `descriptionContains` (case-insensitive substrings).
All conditions AND-ed.

`SoeFilter` fields: `tags`, `group1List`, `priorityLte`, `timeBegin`, `timeEnd`,
`useSourceTime` (filter/sort by field timestamp instead of server timestamp),
`aggregate` (group by tag, latest event + `count` per tag), `includeRemoved`
(include `ack: 2` events).

Typical selections:

```graphql
{
  tags(filter: { group1: "KAW2", invalid: false }, limit: 500) {
    _id tag value valueString invalid alarmed timeTag description unit type
  }
  activeAlarms(limit: 100) { tag description valueString timeTagAlarm priority }
  soeEvents(filter: { priorityLte: 3 }, limit: 200) {
    eventId tag eventText timeTagAtSource timeTagAtSourceOk ack priority group1
  }
  historicalData(tags: ["KAW2KPR21------A"], timeBegin: "2026-07-18T00:00:00Z") {
    tag values { value valueBool invalid isDigital timeTag timeTagAtSource }
  }
}
```

## Mutations

| Mutation | Right required | Notes |
|---|---|---|
| `issueCommand(tagOrId, value, valueString)` | `sendCommands` + station in `group1CommandList` | returns `commandHandle`; `$$`-prefixed tags queue directly without point lookup |
| `ackEvents(action, tag, eventId)` | `ackEvents` | actions: `ACK_ONE_EVENT` (needs `eventId`), `ACK_POINT_EVENTS` (needs `tag`), `ACK_ALL_EVENTS`, `REMOVE_ONE_EVENT`, `REMOVE_POINT_EVENTS`, `REMOVE_ALL_EVENTS` |
| `ackAlarms(action, tagOrId)` | `ackAlarms` | actions: `ACK_ONE_ALARM` (needs `tagOrId`), `ACK_ALL_ALARMS`, `SILENCE_BEEP` |
| `updateTagProperties(tagOrId, properties)` | per property | `annotation`→`enterAnnotations`, `notes`→`enterNotes`, `loLimit`/`hiLimit`/`hysteresis`→`enterLimits`, `alarmDisabled`→`disableAlarms`, `substituted`+`newValue`→`substituteValues` |

`tagOrId` accepts a tag name or a numeric point key as string ("2001").

### Command flow (the important pattern)

Commands are **asynchronous**: the mutation only queues the command; a protocol driver
delivers it and reports back. Poll `commandStatus` until it leaves `PENDING`
(give up after ~10 s):

```js
const { issueCommand } = await gql(`mutation ($t: String!, $v: Float) {
  issueCommand(tagOrId: $t, value: $v) { ok commandHandle } }`,
  { t: 'KAW2AL-21XCBR5238----KCmd', v: 1 })

for (let i = 0; i < 20; i++) {
  await new Promise((r) => setTimeout(r, 500))
  const { commandStatus } = await gql(
    `{ commandStatus(commandHandle: "${issueCommand.commandHandle}") { status cancelReason ackTimeTag } }`)
  if (commandStatus.status !== 'PENDING') break // ACK_OK | ACK_FAIL | CANCELLED
}
```

Commands and property changes are automatically logged to the SOE list and to the
`userActions` audit trail — apps do not need to log them again.

## RBAC behavior your app must expect

* If the user's roles define a `group1List`, every tag/event/history/groups query is
  silently **filtered** to those stations (internal points `_id` -1/-2 stay readable).
  Direct lookups (`tag`, `tagById`) of an out-of-scope point throw `FORBIDDEN`.
* `users`, `roles`, `systemSettings`, `userActions` and the legacy `getUsers`/`getUserByName`
  require an **admin** role (checked against the database, not just the token).
* Command permission is re-checked in the database at mutation time
  (`sendCommands` right + the point's `group1` vs `group1CommandList`).
* Read `me { rights { ... } }` at startup to build the UI (hide command buttons without
  `sendCommands`, etc.), but always handle `FORBIDDEN` errors anyway.

## Error handling

GraphQL errors carry `extensions.code`:

| Code | Meaning |
|---|---|
| `FORBIDDEN` | missing user right or out-of-scope point |
| `BAD_USER_INPUT` | missing/invalid argument (bad ObjectId, no value, etc.) |
| `NOT_FOUND` | command point / point not found |
| `SERVICE_UNAVAILABLE` | MongoDB or the PostgreSQL historian is unreachable |

Partial failures follow normal GraphQL semantics: `data` may coexist with `errors`.

## Data type conventions

* **`Tag` timestamps are epoch milliseconds (Float)** — e.g. `timeTag`, `timeTagAlarm`,
  and the fields inside `sourceDataUpdate`. Convert with `new Date(ms)`.
* **Newer types use the `DateTime` scalar (ISO-8601 strings)** — `SoeEvent`,
  `HistoryPoint`, `CommandStatus`, `UserAction`, and all time arguments
  (`timeBegin`, `timeEnd`, ...). Send ISO strings or epoch ints.
* `JSONValue` is an arbitrary JSON scalar (`valueJson`, `location`, `stats`, `properties`).
* Digital point semantics: `value` 0/1; display texts in `stateTextTrue/False`;
  event texts in `eventTextTrue/False`. History rows expose `isDigital`/`valueBool`.
* SOE `ack`: 0 = unacknowledged, 1 = acknowledged, 2 = removed from list.

## Limits, pagination, freshness

* `limit` defaults to 1000, hard cap 20000 (history: 50000). Page with `skip` + `sortBy`
  and use `tagsCount` for totals.
* `soeEvents` and `historicalData` default to the **last hour** when no time range is given.
* There are **no GraphQL subscriptions**. For live dashboards poll `tags`/`activeAlarms`/
  `soeEvents` (1–5 s intervals are typical for the platform). Request only the fields you
  render — the resolver cost is dominated by document count, not fields.
* Prefer one combined query document over many small requests (single round trip).

## Legacy queries (kept for backward compatibility, avoid in new apps)

`getUsers`, `getUserByName`, `getTagsByGroup1`, `getTags`, `getTag`,
`getProtocolDriverInstances`, `getProtocolConnections` — same behavior as their modern
counterparts (`users`, `tags(filter: ...)`, `tag`, ...).

## Local development / testing recipe

Run the API without touching a production system (bundled runtimes on Windows):

```sh
# throwaway MongoDB (platform-windows bundles mongod 8.x; no --nojournal flag)
platform-windows/mongodb-runtime/bin/mongod.exe --port 27999 --dbpath <scratch>/mdata --bind_ip 127.0.0.1

# minimal config file: { "nodeName": "test", "mongoConnectionString": "mongodb://127.0.0.1:27999/json_scada_test", "mongoDatabaseName": "json_scada_test" }
cd src/server_realtime_auth
JS_CONFIG_FILE=<scratch>/config.json JS_HTTP_PORT=18080 JS_JWT_SECRET=test node index.js
```

Seed `users` (bcryptjs-hashed `password`) and `roles` documents to test RBAC; the roles
schema is documented in `src/server_realtime_auth/README.md`. Point the historian queries
at any PostgreSQL with a `hist(tag, value, flags bit(8), time_tag, time_tag_at_source)`
table using standard libpq env vars (`PGHOST`, `PGPORT`, `PGDATABASE`, `PGUSER`, ...).

## Standalone PostGraphile historian server (optional)

`src/graphql-server/` is a separate, auth-less PostGraphile server that auto-exposes the
SQL historian schema (default `http://127.0.0.1:4000/graphiql`, env-configurable — see its
README). Use it only for SQL-side exploration/reporting on trusted networks; apps should
normally use `/apollo`, which covers history via `historicalData` with RBAC.
