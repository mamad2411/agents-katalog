---
name: cf-backup
description: Back up a Cloudflare account's D1 databases and KV namespaces to a local timestamped folder without writing anything to Cloudflare. Exports each D1 database to .sql, saves every KV key with its value (base64 for binary), metadata and expiration in files `wrangler kv bulk put` can restore, writes a manifest with the sha256 of every file plus a RESTORE.md with the exact restore commands (never runs them), and can verify or prune backups later. Use for "back up my D1 database", "export my KV", "backup Cloudflare data", "snapshot my Worker's data", "before I run a migration", before a bulk delete or schema change, or when restoring from one of these backups.
---

# cf-backup

`scripts/cf-backup.mjs` is zero-dependency Node 22+ and uses the user's existing wrangler login. Run `npx wrangler whoami` first. If it says not logged in, ask the user to run `npx wrangler login`.

```
node cf-backup.mjs --dry-run                        # ALWAYS first: databases, namespaces, key counts, request estimate
node cf-backup.mjs                                  # everything, into ~/cf-backups/cf-backup-<UTC stamp>/
node cf-backup.mjs --d1 my-db --kv orders,sessions  # only these (names, titles or ids)
node cf-backup.mjs --out D:\backups --keep 7        # then delete older backups this tool made there
node cf-backup.mjs --account <id>                   # login sees several accounts (or set CLOUDFLARE_ACCOUNT_ID)
node cf-backup.mjs verify <backupDir>               # re-hash every file, replay the SQL in SQLite, decode every KV entry
node cf-backup.mjs prune <outDir> --keep 7 --dry-run
node cf-backup.mjs --local --cwd <project> --d1 my-db --kv <namespace-id>   # wrangler dev state
```
Exit codes: 0 ok, 1 finished with problems (listed, backup marked incomplete), 2 refused or bad usage.

## Rules
- Read-only towards Cloudflare. Never run a RESTORE.md command unless the user asks to restore. Then show the command, and restore into a new database or namespace unless they say otherwise.
- Backups are user data. Never `cat`, print or paste the SQL or KV files, and never commit them. Report counts and sizes only. To check one, run `verify`.
- Tell the user before the first D1 export: **a D1 database can't serve queries while its export runs** (wrangler's own warning). Small databases take seconds; schedule big ones for a quiet time.
- The script refuses an `--out` inside a git work tree. Pass `--allow-git` only if the user confirms that folder is git-ignored. Each backup also gets a `.gitignore` containing `*`.
- Before a migration: back up, run `verify`, then migrate. `--keep` only prunes after a complete run, only folders with a cf-backup manifest, and only for the same account.

## What a backup contains
```
cf-backup-20261115-051528Z/
  .gitignore          "*" plus a do-not-commit warning
  manifest.json       counts, sizes, sha256 per file, timestamps, D1 row counts, Time Travel bookmark, failed keys
  RESTORE.md          exact restore commands, not run
  d1/<db>.sql         wrangler d1 export output
  kv/<title>__<id8>/part-0001.json   JSON array, one {key,value,base64?,expiration?,metadata?} per line, ≤64 MiB per file
```

## How it reads
- **REST API** with the token from the wrangler login (`wrangler auth token`, never printed), or `CLOUDFLARE_API_TOKEN`. It falls back to wrangler subcommands (`--via wrangler`) if no token is available.
- **KV**: keys are listed 1,000 per request. Values come from bulk reads, 100 per request. Binary values come back from those as U+FFFD, so the script re-reads them one at a time, byte for byte. `--exact` reads every value that way.
- **Rate limits**: Cloudflare allows 1,200 requests per 5 minutes per user, shared with the dashboard. The script defaults to 3 requests/s (`--rps`) with 6 in flight (`--concurrency`). On a 429 it waits for `Retry-After`; on 5xx and network errors it retries with exponential backoff (8 tries). 3,000 text keys take about 33 requests. 3,000 binary keys take about 17 minutes.
- **D1**: `wrangler d1 export <db> --remote --output … -y`. The dump is replayed into in-memory SQLite (`node:sqlite`) to count rows, and the Time Travel bookmark is recorded.

## Restoring (from RESTORE.md)
```
npx wrangler d1 create my-db-restored
npx wrangler d1 execute my-db-restored --remote --file "d1/my-db.sql" -y
npx wrangler kv bulk put "kv/orders__3f9a1c2e/part-0001.json" --namespace-id <id> --remote
```
- The SQL creates its tables, so it fails on a database that still has them. Restore into a new one and repoint the binding.
- `kv bulk put` overwrites keys with the same name and leaves other keys alone. It rejects entries whose expiration has already passed, so remove those first.
- Within Time Travel's window (7 days on Free, 30 on Paid), `wrangler d1 time-travel restore <db> --bookmark=<from RESTORE.md>` rolls the live database back without the file. It replaces the current data.

## Limits
- wrangler can't export D1 databases that contain virtual tables (FTS5).
- KV listing is eventually consistent. Keys deleted mid-backup are counted as "deleted while reading". Keys that fail are listed in `manifest.json` under `failedKeys`, and the run exits 1.
- `wrangler kv bulk put` refuses metadata that isn't a JSON object. Such keys go to `nonobject-metadata-*.json`, with a curl restore command.
- The wrangler transport can't read keys that start with `-` (yargs treats them as flags). The REST transport can. `--local` runs one wrangler process at a time because parallel ones lock miniflare's SQLite.
