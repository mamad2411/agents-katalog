---
name: pawn-a-mysql-samp-expert
description: >
  Expert guidance for Pawn (SA-MP/Open.mp) scripts using BlueG's/maddinat0r's classic MySQL
  plugin (a_mysql, pBlueG/SA-MP-MySQL, final release R41-4). Use for: mysql_connect, threaded
  queries (mysql_tquery/mysql_pquery), legacy blocking mysql_query, cache_* functions
  (cache_get_value_name_int, cache_get_row_count — destination is BY REFERENCE here), the ORM
  system (orm_create, orm_addvar_*, orm_select/orm_load, orm_save), mysql_format/
  mysql_escape_string, OnQueryError, mysql_connect_file/mysql.ini, MySQLOpt options, or any
  MySQL:/Cache:/ORM:/MySQLOpt: tag from a_mysql.inc. Also covers DB architecture, login/register
  systems, R39/R40/R41 version differences, sampctl/pawn.json packaging, and distinguishing this
  older C++ plugin from the newer Rust-based mysql_samp/NullSablex plugin (opposite cache
  calling convention). Consult before answering anything involving a_mysql, mysql_tquery,
  cache_get_value_*, orm_*, or persistent MySQL storage tied to BlueG/pBlueG/maddinat0r.
---

# Pawn a_mysql (BlueG/SA-MP-MySQL) Expert

You are an expert in **BlueG's MySQL plugin** (repo `pBlueG/SA-MP-MySQL`, include `a_mysql.inc`,
developed by maddinat0r) — historically *the* MySQL plugin for SA-MP, final release **R41-4**
(Sep 2017), C++ plugin linked against `libmysqlclient`/MariaDB Connector/C. This is a **different,
older plugin** from the newer Rust-based `mysql_samp` (NullSablex) — do not mix their APIs up.
If the user's code/questions show signs of the newer plugin (return-value cache reads, `%s` auto-
escaping, no `MySQL:`/`Cache:`/`ORM:` tags), point this out — see `references/plugin-disambiguation.md`.

---

## Quick orientation

| Topic | Reference file | When to load |
|---|---|---|
| Full native/forward signatures | `references/api-reference.md` | Signature lookup, param order |
| Connection, options, mysql.ini | `references/connection.md` | mysql_connect, mysql_connect_file, MySQLOpt |
| Queries (tquery/pquery/query) | `references/queries.md` | Threaded vs unthreaded, format specifiers |
| Cache system (BY-REF!) | `references/cache.md` | cache_get_*, cache_save, multi-result sets |
| ORM | `references/orm.md` | orm_create, orm_addvar_*, CRUD, orm_load vs orm_select |
| Errors & OnQueryError | `references/errors.md` | mysql_errno, error codes, OnQueryError |
| Security | `references/security.md` | SQL injection, %e vs %s, mysql_escape_string |
| Version history (R5→R41-4) | `references/version-history.md` | "what changed in R40", legacy R5-R8 code |
| sampctl / pawn.json | `references/sampctl-packaging.md` | dependency management, build pipeline |
| mysql_samp vs a_mysql | `references/plugin-disambiguation.md` | telling the two plugins apart |
| Common forum/issue errors | `references/troubleshooting.md` | plugin won't load, GLIBCXX, connection refused |

## Scripts & assets

| File | Purpose |
|---|---|
| `scripts/validate_a_mysql.py` | Lints a `.pwn` file for the by-ref cache anti-pattern, mysql_samp-only natives, unescaped `format()`-built SQL, missing `OnQueryError`/`forward`, missing `mysql_errno` checks, and ORM/cache resource leaks. Run it on any a_mysql code before presenting it. |
| `scripts/gen_a_mysql.py` | Generates ready-to-compile boilerplate: `connection`, `query-callback`, `login-orm`, `login-cache`, `mysql-ini`. Prefer this over hand-writing common scaffolding. |
| `assets/players_schema.sql` | Example `CREATE TABLE` schema (players + logs) consumable by `mysql_tquery_file`. |
| `assets/pawn.json.template` | Starter sampctl manifest with `pBlueG/SA-MP-MySQL:R41-4` pinned. |
| `assets/mysql.ini.template` | Starter connection file for `mysql_connect_file()`. |
| `assets/full_login_example.pwn` | Complete, heavily-commented login/register reference combining ORM + dialogs + timers, modeled on the official `example_scripts/`. |
| `evals/` | Trigger eval (description quality) and a static code-correctness eval for the validator script — see `evals/README.md`. |

**Always run `scripts/validate_a_mysql.py` on any non-trivial a_mysql code you write or are asked
to review** — it catches the by-reference cache mistake and several other issues mechanically,
faster and more reliably than eyeballing it.

---

## Core mental model

```
mysql_connect() → MySQL:handle (tagged!)
  ├─ mysql_tquery()  → background thread → callback() on next server tick (RECOMMENDED)
  ├─ mysql_pquery()  → background thread, parallel/out-of-order, no transactions
  └─ mysql_query()   → BLOCKS THE SERVER until done (legacy, avoid) → returns Cache:id directly

Inside callback (or after mysql_query/cache_set_active):
  cache_get_row_count(dest)              // BY REFERENCE — fills `dest`, returns 1/0
  cache_get_value_name_int(row, "col", dest)   // BY REFERENCE
  cache_get_value_index(row, col, dest[])      // string, writes into dest[]
```

**This is the single most important gotcha vs. the modern plugin**: every `cache_get_*` /
`cache_is_*` native in a_mysql writes its result into a **reference parameter** and returns
`1`/`0` for success/failure. It does **NOT** return the value directly.

```pawn
// CORRECT for a_mysql (BlueG):
new rows;
cache_get_row_count(rows);          // by-ref — rows is now populated

new money;
cache_get_value_name_int(0, "money", money);   // by-ref

// WRONG — this is the mysql_samp (NullSablex) style, will not compile against a_mysql:
new rows = cache_get_row_count();   // a_mysql's cache_get_row_count returns 1/0, not the count!
```

---

## Must-know idioms

### 1. Minimal connection + threaded query + callback

```pawn
#include <a_samp>
#include <a_mysql>

new MySQL:g_SQL;

public OnGameModeInit()
{
    g_SQL = mysql_connect("127.0.0.1", "root", "password", "samp_db");
    if (g_SQL == MYSQL_INVALID_HANDLE || mysql_errno(g_SQL) != 0)
    {
        print("[MySQL] connection failed");
        return 1;
    }

    mysql_tquery(g_SQL, "SELECT id, name FROM players LIMIT 5", "OnPlayersLoaded");
    return 1;
}

forward OnPlayersLoaded();
public OnPlayersLoaded()
{
    new rows;
    cache_get_row_count(rows);

    new name[MAX_PLAYER_NAME], id;
    for (new i = 0; i < rows; i++)
    {
        cache_get_value_index_int(i, 0, id);
        cache_get_value_index(i, 1, name);
        printf("Player #%d: %s", id, name);
    }
    return 1;
}

public OnGameModeExit()
{
    mysql_close(g_SQL);
    return 1;
}
```

### 2. Building safe queries — `%e` escapes, `%s` does NOT

```pawn
new query[256];
mysql_format(g_SQL, query, sizeof(query),
    "SELECT * FROM players WHERE name = '%e' AND level >= %d",
    player_name, min_level);
mysql_tquery(g_SQL, query, "OnResult");
```

This is the **opposite convention** of the newer mysql_samp plugin. In a_mysql:
- `%e` → escaped string (use for any value from outside your code)
- `%s` → raw string, **NOT escaped** (only for trusted compile-time text)
- `%d`/`%i` → int, `%f` → float, `%x`/`%X` → hex, `%o` → octal, `%u` → unsigned

### 3. Passing context (playerid) through the callback

```pawn
new query[128];
mysql_format(g_SQL, query, sizeof(query),
    "SELECT * FROM players WHERE id = %d", target_id);
mysql_tquery(g_SQL, query, "OnPlayerLoaded", "d", playerid);

forward OnPlayerLoaded(playerid);
public OnPlayerLoaded(playerid)
{
    new rows;
    cache_get_row_count(rows);
    if (rows > 0)
    {
        new name[MAX_PLAYER_NAME];
        cache_get_value_name(0, "name", name);
        printf("player %d: %s", playerid, name);
    }
    return 1;
}
```

Format specifiers for the **callback** parameter list (different table from `mysql_format`!):

| Char | Type |
|---|---|
| `d`/`i` | integer |
| `s` | string |
| `f` | float |
| `b` | boolean |
| `a` | array (followed by `d`/`i` for length; length is also passed to the callback) |
| `r` | reference (pass a cell/array by reference) |

### 4. Always implement OnQueryError

```pawn
public OnQueryError(errorid, const error[], const callback[], const query[], MySQL:handle)
{
    printf("[MySQL ERROR %d] %s", errorid, error);
    printf("  Callback: %s | Handle: %d", callback, _:handle);
    printf("  Query: %s", query);
    return 1;
}
```

### 5. ORM — full player lifecycle

```pawn
enum E_PLAYER
{
    ID,
    Name[MAX_PLAYER_NAME],
    Float:PosX, Float:PosY, Float:PosZ,
    Money,
    ORM:ORM_ID,
}
new Player[MAX_PLAYERS][E_PLAYER];

stock SetupPlayerORM(playerid)
{
    Player[playerid][ORM_ID] = orm_create("players", g_SQL);

    orm_addvar_int   (Player[playerid][ORM_ID], Player[playerid][ID],    "id");
    orm_addvar_string(Player[playerid][ORM_ID], Player[playerid][Name],  MAX_PLAYER_NAME, "name");
    orm_addvar_int   (Player[playerid][ORM_ID], Player[playerid][Money], "money");
    orm_addvar_float (Player[playerid][ORM_ID], Player[playerid][PosX],  "pos_x");
    orm_addvar_float (Player[playerid][ORM_ID], Player[playerid][PosY],  "pos_y");
    orm_addvar_float (Player[playerid][ORM_ID], Player[playerid][PosZ],  "pos_z");

    orm_setkey(Player[playerid][ORM_ID], "id");
}

public OnPlayerConnect(playerid)
{
    SetupPlayerORM(playerid);
    GetPlayerName(playerid, Player[playerid][Name], MAX_PLAYER_NAME);

    // orm_select (a.k.a. orm_load) only works if the key var already has a valid value.
    // For login-by-name lookups, run a manual SELECT first, then orm_apply_cache.
    new query[128];
    mysql_format(g_SQL, query, sizeof(query),
        "SELECT * FROM players WHERE name = '%e' LIMIT 1", Player[playerid][Name]);
    mysql_tquery(g_SQL, query, "OnPlayerLookup", "d", playerid);
    return 1;
}

forward OnPlayerLookup(playerid);
public OnPlayerLookup(playerid)
{
    new rows;
    cache_get_row_count(rows);

    if (rows > 0)
    {
        orm_apply_cache(Player[playerid][ORM_ID], 0);
        printf("loaded %s (id=%d)", Player[playerid][Name], Player[playerid][ID]);
    }
    else
    {
        // new player — orm_insert will populate the key (ID) via cache_insert_id internally
        orm_insert(Player[playerid][ORM_ID], "OnPlayerRegistered", "d", playerid);
    }
    return 1;
}

forward OnPlayerRegistered(playerid);
public OnPlayerRegistered(playerid)
{
    printf("new player registered with id %d", Player[playerid][ID]);
    return 1;
}

public OnPlayerDisconnect(playerid, reason)
{
    orm_save(Player[playerid][ORM_ID]);
    orm_destroy(Player[playerid][ORM_ID]);
    return 1;
}
```

---

## Key rules to enforce in generated code

1. **`MySQL:`, `Cache:`, `ORM:`, `MySQLOpt:` are real Pawn tags** in this plugin — always declare
   variables with them (`new MySQL:g_SQL;`, `new Cache:result;`, `new ORM:orm_id;`). Omitting the
   tag still compiles (tags are just compiler warnings) but loses type-safety and is bad style.
2. **Every `cache_get_*`/`cache_is_*` native uses a reference parameter** — `new x; cache_get_row_count(x);`
   not `new x = cache_get_row_count();`. This is the #1 source of confusion vs. the newer plugin.
3. **`%e` escapes, `%s` does not** in `mysql_format`. Never put raw user/player input through `%s`.
4. **Prefer `mysql_tquery` over `mysql_query`.** `mysql_query` is unthreaded and blocks the entire
   server until the query returns — only acceptable for one-off startup/admin tasks, never in
   hot paths like `OnPlayerConnect`.
5. **`mysql_query` (legacy, unthreaded) returns a `Cache:` id directly** — this is the ONE
   query native that doesn't use a callback; you must `cache_delete()` the result yourself when
   `use_cache = true`, or you leak memory.
6. **The callback must be `forward`ed** as a public function — a missing `forward` is a silent
   bug (the callback is just never called, with no compile error).
7. **`orm_apply_cache` needs an active cache** — call it inside the query callback (or under
   `cache_set_active`), never standalone.
8. **`orm_load` is a literal alias of `orm_select`** — both exist in the wiki/code; prefer
   `orm_select` for newer scripts, but recognize `orm_load` in legacy code (it's the same function).
9. **Implement `OnQueryError`** — undetected query failures (syntax errors, lost connections,
   duplicate keys) are otherwise completely silent.
10. **`mysql_close` blocks until the queue drains** — calling it in `OnGameModeExit` after queuing
    a final "set everyone offline" UPDATE is the standard, safe pattern.
11. **Format spec tables differ between `mysql_format` and the threaded-query callback** — see the
    two separate tables in `references/queries.md`. Mixing them up (e.g. using `%e` in a callback
    format string) is a common bug.

---

## Installation summary (R41-4)

| Step | Detail |
|---|---|
| 1 | Download the release archive matching your OS/arch from GitHub Releases |
| 2 | Extract into the SA-MP server root — this drops the plugin binary into `plugins/` and the include into `pawno/include/` (or `qawno/include/`) |
| 3 | `server.cfg`: add `plugins mysql` (Windows) or `plugins mysql.so` (Linux) |
| 4 | `#include <a_mysql>` in your script |

**Requires** `libmysqlclient`/MariaDB Connector/C as a 32-bit (i686) system library on Linux — use
`mysql_static.so` if you can't install it. On Windows, requires the matching VC++ x86 redistributables.

---

## Quick version cheatsheet

| Version | Significance |
|---|---|
| R5–R8 | Pre-history; threaded support was inconsistent (R7 dropped it briefly) |
| R39.x | Stable pre-R40 API: by-ref cache, but simpler tags, HTML logging |
| **R40** | **Massive breaking release** — introduced `MySQL:`/`Cache:` tags, swapped `mysql_connect` param order, moved connection options to `mysql_init_options`/`mysql_set_option`, multi-result-set support, new logging system |
| R41–R41-4 | Stabilization: `mysql_error`, `mysql_tquery_file`, SSL caveats, log/crash fixes. **R41-4 is the final release.** |

See `references/version-history.md` for the full annotated changelog and migration notes between
R39 and R40 specifically (the only truly breaking jump in the plugin's history).

---

## Troubleshooting checklist

- **Plugin fails to load (Linux)**: `GLIBCXX_3.4.15 not found` → upgrade gcc/distro; missing
  `libmysqlclient_r.so.18` → install 32-bit MySQL client library, or use `mysql_static.so`.
- **Plugin fails to load (Windows)**: missing VC++ 2010/2012/2015 x86 redistributables, or (on
  Windows <10) the Universal CRT update.
- **`symbol __cxa_pure_virtual` error**: 64-bit `libmysqlclient` installed instead of 32-bit, or
  use `mysql_static.so`.
- **"undefined symbol" at compile time**: include not in `pawno/include` (or wrong compiler
  include path); check `#include <a_mysql>` not `<mysql_samp>`.
- **Server freezes during gameplay**: `mysql_query` (unthreaded) used outside startup code —
  switch to `mysql_tquery`.
- **`cache_get_row_count` "returns 0" / wrong values**: forgetting it's a by-ref native — check
  the return value (1/0 success) and read the variable you passed in, don't use the call result.
- **Callback "never fires"**: missing `forward` declaration, or callback name typo (it's a string).
- **Duplicate connection log spam**: by design — the plugin opens `2 + pool_size` real connections
  per handle; this is expected, not a bug.
- **`ORM_NO_DATA` / no row applied**: `orm_apply_cache` called without an active cache, or called
  outside the query callback.
- **`mysql_connect` returns `MYSQL_INVALID_HANDLE`**: always immediately check
  `mysql_errno(handle)` and log `mysql_error()` — host/credentials/firewall are the usual causes.
