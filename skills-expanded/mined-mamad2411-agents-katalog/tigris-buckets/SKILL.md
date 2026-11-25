---
name: tigris-buckets
description: Use when creating, configuring, or deleting Tigris buckets — includes regions, tiers, CORS, migrations, TTL, notifications, snapshots, and forks
---

# Tigris Bucket Management

## Quick Reference

| Command                                   | Description                                   |
| ----------------------------------------- | --------------------------------------------- |
| `tigris mk <name>`                        | Create a bucket (or folder with trailing `/`) |
| `tigris buckets list`                     | List all buckets                              |
| `tigris buckets get <name>`               | Inspect bucket details                        |
| `tigris buckets delete <name>`            | Delete a bucket                               |
| `tigris buckets set <name>`               | Update bucket settings                        |
| `tigris buckets set-ttl <name>`           | Configure object expiration                   |
| `tigris buckets set-locations <name>`     | Set data locations                            |
| `tigris buckets set-migration <name>`     | Configure shadow bucket migration             |
| `tigris buckets set-transition <name>`    | Configure storage class transitions           |
| `tigris buckets set-notifications <name>` | Configure event webhooks                      |
| `tigris buckets set-cors <name>`          | Configure CORS rules                          |
| `tigris snapshots list <bucket>`          | List bucket snapshots                         |
| `tigris snapshots take <bucket>`          | Take a snapshot                               |

## Create a Bucket

### `tigris mk <path>` (alias: `create`)

Create a bucket (bare name) or a folder inside a bucket (trailing `/`). Supports `t3://` and `tigris://` URI prefixes.

```bash
tigris mk my-bucket
tigris mk my-bucket --access public --locations iad
tigris mk my-bucket/images/                              # creates a folder
tigris mk t3://my-bucket
tigris mk my-fork --fork-of my-bucket
tigris mk my-fork --fork-of my-bucket --source-snapshot 1765889000501544464
```

### `tigris buckets create <name>` (alias: `c`)

Same as `mk` but under the `buckets` subcommand.

```bash
tigris buckets create my-bucket
tigris buckets create my-bucket --access public --locations iad
tigris buckets create my-bucket --enable-snapshots --default-tier STANDARD_IA
tigris buckets create my-fork --fork-of my-bucket
tigris buckets create my-fork --fork-of my-bucket --source-snapshot 1765889000501544464
```

**Flags:**

| Flag                 | Alias           | Description                                                       | Default    |
| -------------------- | --------------- | ----------------------------------------------------------------- | ---------- |
| `--access`           | `-a`            | Access level (`public`, `private`)                                | `private`  |
| `--public`           |                 | Shorthand for `--access public`                                   |            |
| `--locations`        | `-l`            | Bucket location (see [Locations](#locations))                     | `global`   |
| `--default-tier`     | `-t`            | Default storage tier (see [Storage Tiers](#storage-tiers))        | `STANDARD` |
| `--enable-snapshots` | `-s`            | Enable snapshots for the bucket                                   | `false`    |
| `--fork-of`          | `--fork`        | Create as a fork (copy-on-write clone) of the named source bucket |            |
| `--source-snapshot`  | `--source-snap` | Fork from a specific snapshot (requires `--fork-of`)              |            |
| `--format`           | `-f`            | Output format (`json`, `table`)                                   | `table`    |
| `--json`             |                 | Output as JSON                                                    |            |
| `--consistency`      | `-c`            | **(Deprecated)** Use `--locations` instead                        |            |
| `--region`           | `-r`            | **(Deprecated)** Use `--locations` instead                        |            |

## List Buckets

### `tigris buckets list` (alias: `l`)

List all buckets in the current organization.

```bash
tigris buckets list
tigris buckets list --json
tigris buckets list --forks-of my-bucket
```

| Flag              | Description                                                 |
| ----------------- | ----------------------------------------------------------- |
| `--forks-of`      | Only list buckets that are forks of the named source bucket |
| `--format` / `-f` | Output format (`json`, `table`, `xml`; default: `table`)    |
| `--json`          | Output as JSON                                              |

## Inspect a Bucket

### `tigris buckets get <name>` (alias: `g`)

Show details for a bucket including access level, region, tier, and custom domain.

```bash
tigris buckets get my-bucket
tigris buckets get my-bucket --json
```

| Flag              | Description                                              |
| ----------------- | -------------------------------------------------------- |
| `--format` / `-f` | Output format (`json`, `table`, `xml`; default: `table`) |
| `--json`          | Output as JSON                                           |

## Delete a Bucket

### `tigris buckets delete <name>` (alias: `d`)

Delete one or more buckets by name. Accepts comma-separated names.

```bash
tigris buckets delete my-bucket --force
tigris buckets delete bucket-a,bucket-b --force
```

| Flag              | Description                                       |
| ----------------- | ------------------------------------------------- |
| `--force`         | Skip confirmation prompt                          |
| `--format` / `-f` | Output format (`json`, `table`; default: `table`) |
| `--json`          | Output as JSON                                    |

## Update Bucket Settings

### `tigris buckets set <name>` (alias: `s`)

Update settings on an existing bucket.

```bash
tigris buckets set my-bucket --access public
tigris buckets set my-bucket --locations iad,fra --cache-control 'max-age=3600'
tigris buckets set my-bucket --custom-domain assets.example.com
```

| Flag                          | Description                                                                            |
| ----------------------------- | -------------------------------------------------------------------------------------- |
| `--access`                    | Bucket access level (`public`, `private`)                                              |
| `--locations`                 | Bucket locations (see [Locations](#locations))                                         |
| `--enable-delete-protection`  | Enable delete protection (`true`/`false`)                                              |
| `--cache-control`             | Default cache-control header value                                                     |
| `--custom-domain`             | Custom domain for the bucket                                                           |
| `--allow-object-acl`          | Enable object-level ACL (`true`/`false`)                                               |
| `--disable-directory-listing` | Disable directory listing (`true`/`false`)                                             |
| `--enable-additional-headers` | Enable additional HTTP headers like `X-Content-Type-Options: nosniff` (`true`/`false`) |
| `--region`                    | **(Deprecated)** Use `--locations` instead                                             |
| `--format`                    | Output format (`json`, `table`; default: `table`)                                      |
| `--json`                      | Output as JSON                                                                         |

## Bucket Configuration Commands

### `tigris buckets set-ttl <name>`

Configure object expiration (TTL) on a bucket.

```bash
tigris buckets set-ttl my-bucket --days 30
tigris buckets set-ttl my-bucket --date 2026-06-01
tigris buckets set-ttl my-bucket --disable
```

| Flag        | Alias | Description                                               |
| ----------- | ----- | --------------------------------------------------------- |
| `--days`    | `-d`  | Expire objects after this many days                       |
| `--date`    |       | Expire objects on this date (ISO-8601, e.g. `2026-06-01`) |
| `--enable`  |       | Enable TTL (uses existing lifecycle rules)                |
| `--disable` |       | Disable TTL on the bucket                                 |

### `tigris buckets set-locations <name>`

Set the data locations for a bucket.

```bash
tigris buckets set-locations my-bucket --locations iad
tigris buckets set-locations my-bucket --locations iad,fra
tigris buckets set-locations my-bucket --locations global
```

| Flag          | Alias | Description                                                        |
| ------------- | ----- | ------------------------------------------------------------------ |
| `--locations` | `-l`  | Bucket location(s) — comma-separated (see [Locations](#locations)) |

### `tigris buckets set-migration <name>`

Configure data migration from an external S3-compatible source bucket. Tigris pulls objects on demand from the source (shadow bucket pattern).

```bash
tigris buckets set-migration my-bucket \
  --bucket source-bucket \
  --endpoint https://s3.amazonaws.com \
  --region us-east-1 \
  --access-key AKIA... \
  --secret-key wJal...

# Enable write-through (writes go to both source and Tigris)
tigris buckets set-migration my-bucket \
  --bucket source-bucket \
  --endpoint https://s3.amazonaws.com \
  --region us-east-1 \
  --access-key AKIA... \
  --secret-key wJal... \
  --write-through

# Disable migration
tigris buckets set-migration my-bucket --disable
```

**Migration workflow:** Point Tigris at your existing S3-compatible bucket. Tigris serves objects on demand — when a request hits Tigris and the object isn't cached yet, it fetches from the source. Over time, all accessed objects are pulled into Tigris. Use `--write-through` to also push new writes back to the source during migration.

| Flag              | Alias      | Description                                        |
| ----------------- | ---------- | -------------------------------------------------- |
| `--bucket`        | `-b`       | Name of the source bucket to migrate from          |
| `--endpoint`      | `-e`       | Endpoint URL of the source S3-compatible service   |
| `--region`        | `-r`       | Region of the source bucket                        |
| `--access-key`    | `--key`    | Access key for the source bucket                   |
| `--secret-key`    | `--secret` | Secret key for the source bucket                   |
| `--write-through` |            | Enable write-through mode                          |
| `--disable`       |            | Disable migration and clear all migration settings |

### `tigris buckets set-transition <name>`

Configure a lifecycle transition rule. Automatically move objects to a different storage class after a number of days or on a specific date.

```bash
tigris buckets set-transition my-bucket --storage-class STANDARD_IA --days 30
tigris buckets set-transition my-bucket --storage-class GLACIER --date 2026-06-01
tigris buckets set-transition my-bucket --enable
tigris buckets set-transition my-bucket --disable
```

| Flag              | Alias | Description                                                   |
| ----------------- | ----- | ------------------------------------------------------------- |
| `--storage-class` | `-s`  | Target storage class (`STANDARD_IA`, `GLACIER`, `GLACIER_IR`) |
| `--days`          | `-d`  | Transition objects after this many days                       |
| `--date`          |       | Transition objects on this date (ISO-8601)                    |
| `--enable`        |       | Enable lifecycle transition rules                             |
| `--disable`       |       | Disable lifecycle transition rules                            |

### `tigris buckets set-notifications <name>`

Configure object event notifications. Sends webhook requests to a URL when objects are created, updated, or deleted.

```bash
tigris buckets set-notifications my-bucket --url https://example.com/webhook
tigris buckets set-notifications my-bucket --url https://example.com/webhook --token secret123
tigris buckets set-notifications my-bucket --url https://example.com/webhook --username admin --password secret
tigris buckets set-notifications my-bucket --url https://example.com/webhook --filter 'WHERE `key` REGEXP "^images"'
tigris buckets set-notifications my-bucket --enable
tigris buckets set-notifications my-bucket --disable
tigris buckets set-notifications my-bucket --reset
```

| Flag         | Alias | Description                                       |
| ------------ | ----- | ------------------------------------------------- |
| `--url`      | `-u`  | Webhook URL (must be `http` or `https`)           |
| `--filter`   | `-f`  | SQL WHERE clause to filter events by key          |
| `--token`    | `-t`  | Token for webhook authentication                  |
| `--username` |       | Username for basic webhook authentication         |
| `--password` |       | Password for basic webhook authentication         |
| `--enable`   |       | Enable notifications (uses existing config)       |
| `--disable`  |       | Disable notifications (preserves existing config) |
| `--reset`    |       | Clear all notification settings                   |

### `tigris buckets set-cors <name>`

Configure CORS rules on a bucket. Each invocation adds a rule unless `--override` or `--reset` is used.

```bash
tigris buckets set-cors my-bucket --origins '*' --methods GET,HEAD
tigris buckets set-cors my-bucket --origins https://example.com --methods GET,POST --headers Content-Type,Authorization --max-age 3600
tigris buckets set-cors my-bucket --origins https://example.com --override
tigris buckets set-cors my-bucket --reset
```

| Flag               | Alias | Description                                           |
| ------------------ | ----- | ----------------------------------------------------- |
| `--origins`        | `-o`  | Allowed origins (comma-separated, or `*` for all)     |
| `--methods`        | `-m`  | Allowed HTTP methods (comma-separated)                |
| `--headers`        |       | Allowed request headers (comma-separated, or `*`)     |
| `--expose-headers` |       | Response headers to expose (comma-separated)          |
| `--max-age`        |       | Preflight cache duration in seconds (default: `3600`) |
| `--override`       |       | Replace all existing CORS rules instead of appending  |
| `--reset`          |       | Clear all CORS rules                                  |

## Snapshots

Snapshots are point-in-time, read-only copies of a bucket's state. The bucket must be created with `--enable-snapshots`.

### `tigris snapshots list <bucket>` (alias: `l`)

List all snapshots for a bucket, ordered by creation time.

```bash
tigris snapshots list my-bucket
tigris snapshots list my-bucket --json
```

| Flag              | Description                                              |
| ----------------- | -------------------------------------------------------- |
| `--format` / `-f` | Output format (`json`, `table`, `xml`; default: `table`) |
| `--json`          | Output as JSON                                           |

### `tigris snapshots take <bucket> [name]` (alias: `t`)

Take a new snapshot of the bucket's current state. Optionally provide a name.

```bash
tigris snapshots take my-bucket
tigris snapshots take my-bucket my-snapshot
```

## Forks

Forks are copy-on-write clones of a bucket. They are instant, free, and isolated — writes to the fork do not affect the source bucket.

### Create a fork

```bash
# Preferred: use mk or buckets create with --fork-of
tigris mk my-fork --fork-of my-bucket
tigris mk my-fork --fork-of my-bucket --source-snapshot 1765889000501544464

# Equivalent via buckets create
tigris buckets create my-fork --fork-of my-bucket
tigris buckets create my-fork --fork-of my-bucket --source-snapshot 1765889000501544464
```

### List forks

```bash
tigris buckets list --forks-of my-bucket
```

> **Deprecated commands:** `tigris forks list` and `tigris forks create` still work but are deprecated. Use `tigris buckets list --forks-of` and `tigris mk --fork-of` instead.

## Reference Tables

### Storage Tiers

| Tier                      | Value         | Description                                                                          |
| ------------------------- | ------------- | ------------------------------------------------------------------------------------ |
| Standard                  | `STANDARD`    | Default. High durability, availability, and performance for frequently accessed data |
| Infrequent Access         | `STANDARD_IA` | Lower-cost for data accessed less frequently but requiring rapid access when needed  |
| Archive                   | `GLACIER`     | Low-cost for long-term data archiving with infrequent access                         |
| Instant Retrieval Archive | `GLACIER_IR`  | Lowest-cost for long-lived, rarely accessed data requiring retrieval in milliseconds |

### Locations

| Name         | Value    | Description                |
| ------------ | -------- | -------------------------- |
| Global       | `global` | Global (default)           |
| USA          | `usa`    | Restrict to USA            |
| Europe       | `eur`    | Restrict to Europe         |
| Amsterdam    | `ams`    | Amsterdam, Netherlands     |
| Frankfurt    | `fra`    | Frankfurt, Germany         |
| Sao Paulo    | `gru`    | Sao Paulo, Brazil          |
| Ashburn      | `iad`    | Ashburn, Virginia (US)     |
| Johannesburg | `jnb`    | Johannesburg, South Africa |
| London       | `lhr`    | London, United Kingdom     |
| Tokyo        | `nrt`    | Tokyo, Japan               |
| Chicago      | `ord`    | Chicago, Illinois (US)     |
| Singapore    | `sin`    | Singapore, Singapore       |
| San Jose     | `sjc`    | San Jose, California (US)  |
| Sydney       | `syd`    | Sydney, Australia          |

### Consistency Levels (deprecated — use `--locations` instead)

| Level   | Value     | Description                                                           |
| ------- | --------- | --------------------------------------------------------------------- |
| Default | `default` | Strict read-after-write in same region, eventual consistency globally |
| Strict  | `strict`  | Strict read-after-write globally (higher latency)                     |
