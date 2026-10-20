---
name: pawn-mysql-samp-expert
description: >
  Expert guidance for developing Pawn scripts (SA-MP / Open.mp / Pawn Compiler 3.10.10) using the
  mysql_samp plugin by NullSablex. Use this skill whenever the user asks about: connecting to MySQL
  from a SA-MP or Open.mp gamemode, writing non-blocking queries with mysql_query / mysql_pquery,
  reading cache results (cache_get_value_name_*, cache_get_row_count), using the built-in ORM
  (orm_create, orm_addvar_*, orm_select, orm_save), handling OnQueryError, migrating from MySQL
  R41-4, or any mysql_samp native/forward. Also triggers for questions about SA-MP/Open.mp database
  architecture, player data persistence patterns, SQL injection prevention in Pawn, or general
  mysql_samp lifecycle and deployment. Always consult this skill before answering any question that
  involves mysql_samp, mysql_query, cache_*, orm_*, or persistent storage in SA-MP/Open.mp.
---

# Pawn mysql_samp Expert

You are an expert in **mysql_samp** — the modern, Rust-written MySQL plugin for SA-MP and Open.mp.
Below is a compact, authoritative reference covering everything you need to help a user. For
deep-dive details, load the appropriate reference file from `references/`.

---

## Quick orientation

| Topic | Reference file | When to load |
|---|---|---|
| Full API table (55 natives + 1 forward) | `references/api-reference.md` | Signature lookup, param clarification |
| Connection & options | `references/connection-options.md` | mysql_connect, mysql_close, mysql_status, options |
| Queries & mysql_format | `references/queries.md` | mysql_query, mysql_pquery, mysql_format, mysql_escape_string |
| Cache system | `references/cache.md` | cache_*, persistent caches, limits |
| ORM | `references/orm.md` | orm_create, orm_addvar_*, CRUD, orm_apply_cache |
| Error handling | `references/errors.md` | mysql_errno, mysql_error, OnQueryError, logs |
| Security | `references/security.md` | SQL injection, escape rules, resource limits |
| Migration from R41-4 | `references/migration.md` | Breaking changes, porting patterns |
| Patterns & examples | `references/patterns-and-examples.md` | Practical recipes, connection, queries, ORM, cache, shutdown |

---

## Core mental model

```
mysql_connect → connection id (g_mysql)
  └─ mysql_query / mysql_pquery → worker thread
       └─ result pushed onto cache stack
            └─ callback() fires on next tick
                 ├─ cache_get_row_count()
                 ├─ cache_get_value_name_*(row, "col", ...)
                 └─ cache is popped when callback returns
```

- **Every query is non-blocking.** Results arrive inside a callback; the server never stalls.
- **mysql_query = FIFO order.** Callbacks fire in submission order even if queries finish out of order.
- **mysql_pquery = parallel.** No ordering guarantee — use for fire-and-forget writes or independent reads.
- **Cache is automatic.** It's active only inside the callback. Call `cache_save()` to persist it beyond the callback.
- **ORM wraps the pattern.** It generates SELECT/INSERT/UPDATE/DELETE SQL from Pawn variable bindings, still using the same threaded pipeline.

---

## Must-know idioms

### 1. Minimal connection + query + callback

```pawn
#include <a_samp>
#include <mysql_samp>

new g_mysql;

public OnGameModeInit()
{
    g_mysql = mysql_connect("127.0.0.1", "root", "password", "samp_db");
    if (mysql_errno() != MYSQL_OK)
    {
        new msg[256];
        mysql_error(0, msg);
        printf("[MySQL] connect failed: %s", msg);
        return 1;
    }

    mysql_query(g_mysql, "SELECT id, name FROM players LIMIT 5", "OnPlayersLoaded");
    return 1;
}

forward OnPlayersLoaded();
public OnPlayersLoaded()
{
    new rows = cache_get_row_count();
    for (new i = 0; i < rows; i++)
    {
        new id   = cache_get_value_name_int(i, "id");
        new name[MAX_PLAYER_NAME];
        cache_get_value_name(i, "name", name);
        printf("Player #%d: %s", id, name);
    }
}

public OnGameModeExit()
{
    mysql_close(g_mysql);
    return 1;
}
```

### 2. Passing playerid (or other context) into the callback

```pawn
// At query site — "d" = int, forwarded as the first param of the callback
mysql_query(g_mysql, query, "OnPlayerLoaded", "d", playerid);

forward OnPlayerLoaded(playerid);
public OnPlayerLoaded(playerid)
{
    if (cache_get_row_count() > 0)
    {
        new name[MAX_PLAYER_NAME];
        cache_get_value_name(0, "name", name);
        printf("Player %d: %s", playerid, name);
    }
}
```

### 3. Building safe queries with mysql_format

```pawn
new query[256];
mysql_format(g_mysql, query, sizeof(query),
    "SELECT * FROM players WHERE name = '%s' AND level >= %d",
    player_name, min_level);
mysql_query(g_mysql, query, "OnResult");
```

- `%s` / `%e` → auto-escaped (safe for user input)
- `%d` / `%i` → integer, `%f` → float
- `%r` → raw, **not** escaped (only for compile-time constants like table names)
- Never use SA-MP's `format()` to build SQL — it doesn't escape.

### 4. Always implement OnQueryError

```pawn
public OnQueryError(errorid, const error[], const callback[], const query[], connId)
{
    printf("[MySQL ERROR %d] %s", errorid, error);
    printf("  Callback: %s | ConnId: %d", callback, connId);
    // query[] contains the exact SQL — log it if safe to do so
    return 1;
}
```

### 5. ORM — player data lifecycle

```pawn
enum pInfo { pId, pName[MAX_PLAYER_NAME], pLevel, Float:pMoney }
new PlayerInfo[MAX_PLAYERS][pInfo];
new PlayerORM [MAX_PLAYERS];

stock SetupPlayerORM(playerid)
{
    new oid = orm_create("players", g_mysql);
    PlayerORM[playerid] = oid;
    orm_addvar_int   (oid, PlayerInfo[playerid][pId],    "id");
    orm_addvar_string(oid, PlayerInfo[playerid][pName],  MAX_PLAYER_NAME, "name");
    orm_addvar_int   (oid, PlayerInfo[playerid][pLevel], "level");
    orm_addvar_float (oid, PlayerInfo[playerid][pMoney], "money");
    orm_setkey(oid, "id");
}

// On connect: look up or create
public OnPlayerConnect(playerid)
{
    SetupPlayerORM(playerid);
    GetPlayerName(playerid, PlayerInfo[playerid][pName], MAX_PLAYER_NAME);

    new query[128];
    mysql_format(g_mysql, query, sizeof(query),
        "SELECT * FROM players WHERE name = '%s' LIMIT 1",
        PlayerInfo[playerid][pName]);
    mysql_query(g_mysql, query, "OnPlayerLookup", "d", playerid);
    return 1;
}

forward OnPlayerLookup(playerid);
public OnPlayerLookup(playerid)
{
    if (cache_get_row_count() > 0)
    {
        orm_apply_cache(PlayerORM[playerid]);
    }
    else
    {
        // New player — INSERT and capture auto-increment id
        PlayerInfo[playerid][pLevel] = 1;
        PlayerInfo[playerid][pMoney] = 0.0;
        orm_insert(PlayerORM[playerid], "OnPlayerCreated", "d", playerid);
    }
    return 1;
}

forward OnPlayerCreated(playerid);
public OnPlayerCreated(playerid)
{
    PlayerInfo[playerid][pId] = cache_insert_id();
    return 1;
}

// On disconnect: save (UPDATE if id > 0, INSERT if id == 0) then destroy
public OnPlayerDisconnect(playerid, reason)
{
    orm_save   (PlayerORM[playerid]);
    orm_destroy(PlayerORM[playerid]);
    return 1;
}
```

---

## Key rules to enforce in generated code

1. **Always check `mysql_errno()` after `mysql_connect`** — return value `0` means failure but `mysql_errno(0)` confirms it.
2. **Always guard cache reads**: `if (cache_get_row_count() > 0)` before accessing any row.
3. **Use `mysql_format` with `%s`** for any user-supplied string going into SQL.
4. **Never double-escape**: don't call `mysql_escape_string` and then pass the result through `%s` — `%s` escapes again.
5. **`orm_apply_cache` must be called inside a query callback** while the cache is active.
6. **`orm_setkey` is required** before `orm_select`, `orm_update`, `orm_delete`.
7. **`cache_save()` to persist results** beyond the callback scope; pair with `cache_delete(id)` when done.
8. **Implement `OnQueryError`** — silent query failures are the #1 debugging obstacle.
9. **`mysql_tick()` is not needed** on modern SA-MP/Open.mp with mysql_samp — it's kept only for backward compat.
10. **Prefer `mysql_query` (FIFO)** for dependent chains; use `mysql_pquery` for independent parallel writes.

---

## Installation summary

| Server | Step |
|---|---|
| SA-MP | Copy `.so`/`.dll` → `plugins/`; add `plugins mysql_samp.so` (or `.dll`) to `server.cfg`; copy `.inc` to `pawno/include/` (Windows) or `include/` (Linux) |
| Open.mp native (recommended) | Copy binary → `components/`; no config.json entry needed; auto-discovered |
| Open.mp legacy | Copy binary → `plugins/`; add to `legacy_plugins` in `config.json` |

No `libmysqlclient` or any system library is required — the plugin is self-contained.

---

## Plugin constants cheatsheet

```pawn
// Connection options
MYSQL_OPT_PORT            // 0  int
MYSQL_OPT_SSL             // 1  int (bool)
MYSQL_OPT_SSL_CA          // 2  string (path, not yet wired through)
MYSQL_OPT_CONNECT_TIMEOUT // 3  int (seconds)
MYSQL_OPT_AUTO_RECONNECT  // 4  int (bool, default true)

// Plugin error codes
MYSQL_OK                       // 0
MYSQL_ERROR_CONNECTION_FAILED  // 1
MYSQL_ERROR_INVALID_OPTIONS    // 2
MYSQL_ERROR_INVALID_CONNECTION // 3
MYSQL_ERROR_PING_FAILED        // 4
MYSQL_ERROR_QUERY_FAILED       // 5
MYSQL_ERROR_NO_CACHE_ACTIVE    // 6
MYSQL_ERROR_INVALID_ORM        // 7
MYSQL_ERROR_ORM_KEY_NOT_SET    // 8

// Log levels
MYSQL_LOG_NONE    // 0
MYSQL_LOG_ERROR   // 1
MYSQL_LOG_WARNING // 2
MYSQL_LOG_INFO    // 3
MYSQL_LOG_ALL     // 4 (default)

// ORM errno
ORM_OK      // 0
ORM_NO_DATA // 1
```

---

## Common MySQL server error codes (OnQueryError.errorid)

| Code | Cause |
|---|---|
| 1045 | Access denied (wrong user/password) |
| 1049 | Unknown database |
| 1062 | Duplicate entry (UNIQUE / PRIMARY KEY violation) |
| 1064 | SQL syntax error |
| 1146 | Table does not exist |
| 1451 | Foreign-key constraint blocked the operation |
| 2002 | Host unreachable |
| 2006 | MySQL server has gone away |
| 0 | Transport/IO error (TCP drop) — auto-reconnect retries once if enabled |

---

## Troubleshooting checklist

- **Server freezes on start** → check `mysql_errno()` after connect; a blocking connect was removed in this plugin (all queries are async).
- **Callback never fires** → check `forward` declaration matches the name string in `mysql_query`; check `OnQueryError` for errors.
- **cache_get_row_count() returns -1** → you are reading the cache outside a callback without `cache_set_active`.
- **ORM data not saved** → ensure `orm_setkey` is called; ensure the key column binding has a non-zero value for UPDATE to trigger.
- **Double-backslash in saved strings** → you called `mysql_escape_string` on input and also used `%s` in `mysql_format`; remove the manual escape call.
- **Queries pile up, callbacks lag** → use `mysql_pquery` for independent writes; check `mysql_unprocessed_queries()`.
- **"mysql.log" has no detail** → check the `logs/` directory is writable by the server process.
