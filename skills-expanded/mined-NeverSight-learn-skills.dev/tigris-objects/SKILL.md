---
name: tigris-objects
description: Use when uploading, downloading, listing, moving, deleting, or presigning objects in Tigris Storage
---

# Tigris Object Operations

## Quick Reference

| Command                                    | Description                              |
| ------------------------------------------ | ---------------------------------------- |
| `tigris ls [path]`                         | List objects under a bucket/prefix       |
| `tigris cp <src> <dest>`                   | Copy files local↔remote or remote↔remote |
| `tigris mv <src> <dest>`                   | Move/rename objects within Tigris        |
| `tigris rm <path>`                         | Delete objects or folders                |
| `tigris touch <path>`                      | Create an empty object                   |
| `tigris stat <path>`                       | Show object metadata or storage stats    |
| `tigris presign <path>`                    | Generate a presigned URL                 |
| `tigris objects list <bucket>`             | List objects (low-level)                 |
| `tigris objects get <bucket> <key>`        | Download an object (low-level)           |
| `tigris objects put <bucket> <key> <file>` | Upload an object (low-level)             |
| `tigris objects delete <bucket> <key>`     | Delete an object (low-level)             |
| `tigris objects set <bucket> <key>`        | Update object settings (low-level)       |

## URI Scheme

Remote paths use `t3://bucket/key` or `tigris://bucket/key`. Bare `bucket/key` paths are also accepted.

## Unix-Style Commands (primary interface)

### `tigris ls [path]` (alias: `list`)

List all buckets (no arguments) or objects under a bucket/prefix path.

```bash
tigris ls                                  # list all buckets
tigris ls my-bucket                        # list objects in bucket
tigris ls my-bucket/images/                # list objects under prefix
tigris ls t3://my-bucket/prefix/
```

| Flag                 | Alias        | Description                            | Default |
| -------------------- | ------------ | -------------------------------------- | ------- |
| `--snapshot-version` | `--snapshot` | Read from a specific bucket snapshot   |         |
| `--format`           | `-f`         | Output format (`json`, `table`, `xml`) | `table` |
| `--json`             |              | Output as JSON                         |         |

### `tigris cp <src> <dest>` (alias: `copy`)

Copy files between local filesystem and Tigris, or between paths within Tigris. At least one side must be a remote `t3://` path. Quote wildcard patterns to prevent shell expansion.

```bash
tigris cp ./file.txt t3://my-bucket/file.txt               # upload
tigris cp t3://my-bucket/file.txt ./local-copy.txt          # download
tigris cp t3://my-bucket/src/ t3://my-bucket/dest/ -r       # remote-to-remote
tigris cp ./images/ t3://my-bucket/images/ -r               # recursive upload
```

| Flag          | Alias | Description                                       |
| ------------- | ----- | ------------------------------------------------- |
| `--recursive` | `-r`  | Copy directories recursively                      |
| `--format`    | `-f`  | Output format (`json`, `table`; default: `table`) |
| `--json`      |       | Output as JSON                                    |

### `tigris mv <src> <dest>` (alias: `move`)

Move (rename) objects within Tigris. Both source and destination must be remote paths. Quote wildcard patterns to prevent shell expansion.

```bash
tigris mv t3://my-bucket/old.txt t3://my-bucket/new.txt -f
tigris mv t3://my-bucket/old-dir/ t3://my-bucket/new-dir/ -rf
tigris mv my-bucket/a.txt my-bucket/b.txt -f
```

| Flag          | Alias | Description                                       |
| ------------- | ----- | ------------------------------------------------- |
| `--recursive` | `-r`  | Move directories recursively                      |
| `--force`     | `-f`  | Skip confirmation prompt                          |
| `--format`    |       | Output format (`json`, `table`; default: `table`) |
| `--json`      |       | Output as JSON                                    |

### `tigris rm <path>` (alias: `remove`)

Remove a bucket, folder, or object from Tigris. A bare bucket name deletes the bucket itself. Quote wildcard patterns to prevent shell expansion.

```bash
tigris rm t3://my-bucket/file.txt -f
tigris rm t3://my-bucket/folder/ -rf
tigris rm t3://my-bucket -f                                 # deletes the bucket
tigris rm "t3://my-bucket/logs/*.tmp" -f                    # wildcard delete
```

| Flag          | Alias | Description                                       |
| ------------- | ----- | ------------------------------------------------- |
| `--recursive` | `-r`  | Remove directories recursively                    |
| `--force`     | `-f`  | Skip confirmation prompt                          |
| `--format`    |       | Output format (`json`, `table`; default: `table`) |
| `--json`      |       | Output as JSON                                    |

### `tigris touch <path>`

Create an empty (zero-byte) object at the given bucket/key path.

```bash
tigris touch my-bucket/placeholder.txt
tigris touch t3://my-bucket/logs/
```

| Flag       | Alias | Description                                       |
| ---------- | ----- | ------------------------------------------------- |
| `--format` | `-f`  | Output format (`json`, `table`; default: `table`) |
| `--json`   |       | Output as JSON                                    |

### `tigris stat [path]`

Show storage stats (no args), bucket info, or object metadata.

```bash
tigris stat                                # overall storage stats
tigris stat t3://my-bucket                 # bucket info
tigris stat t3://my-bucket/my-object.json  # object metadata
```

| Flag                 | Alias        | Description                            | Default |
| -------------------- | ------------ | -------------------------------------- | ------- |
| `--snapshot-version` | `--snapshot` | Read from a specific bucket snapshot   |         |
| `--format`           | `-f`         | Output format (`json`, `table`, `xml`) | `table` |
| `--json`             |              | Output as JSON                         |         |

## Presigned URLs

### `tigris presign <path>`

Generate a presigned URL for temporary access to an object without credentials.

```bash
tigris presign my-bucket/file.txt
tigris presign t3://my-bucket/report.pdf --method put --expires-in 7200
tigris presign my-bucket/image.png --format json
tigris presign my-bucket/data.csv --access-key tid_AaBb
```

| Flag           | Alias | Description                                                           | Default |
| -------------- | ----- | --------------------------------------------------------------------- | ------- |
| `--method`     | `-m`  | HTTP method (`get`, `put`)                                            | `get`   |
| `--expires-in` | `-e`  | URL expiry time in seconds                                            | `3600`  |
| `--access-key` |       | Access key ID for signing (resolved from credentials if not provided) |         |
| `--format`     | `-f`  | Output format (`url`, `json`)                                         | `url`   |
| `--json`       |       | Output as JSON                                                        |         |

**Use cases:**

- Temporary sharing of private objects (GET)
- Client-side uploads without exposing credentials (PUT)

## Low-Level `objects` Subcommand

For programmatic and granular control over individual objects.

### `tigris objects list <bucket>` (alias: `l`)

List objects in a bucket, optionally filtered by a key prefix.

```bash
tigris objects list my-bucket
tigris objects list my-bucket --prefix images/
tigris objects list my-bucket --json
```

| Flag                 | Alias        | Description                                              |
| -------------------- | ------------ | -------------------------------------------------------- |
| `--prefix`           | `-p`         | Filter objects by key prefix                             |
| `--snapshot-version` | `--snapshot` | Read from a specific bucket snapshot                     |
| `--format`           | `-f`         | Output format (`json`, `table`, `xml`; default: `table`) |
| `--json`             |              | Output as JSON                                           |

### `tigris objects get <bucket> <key>` (alias: `g`)

Download an object by key. Prints to stdout by default, or saves to a file with `--output`.

```bash
tigris objects get my-bucket config.json
tigris objects get my-bucket archive.zip --output ./archive.zip --mode stream
```

| Flag                 | Alias        | Description                                                                |
| -------------------- | ------------ | -------------------------------------------------------------------------- |
| `--output`           | `-o`         | Output file path (prints to stdout if not specified)                       |
| `--mode`             | `-m`         | Response mode: `string` (loads into memory) or `stream` (writes in chunks) |
| `--snapshot-version` | `--snapshot` | Read from a specific bucket snapshot                                       |
| `--format`           | `-f`         | Output format (`json`, `table`; default: `table`)                          |
| `--json`             |              | Output as JSON                                                             |

### `tigris objects put <bucket> <key> <file>` (alias: `p`)

Upload a local file as an object. Content-type is auto-detected from extension unless overridden.

```bash
tigris objects put my-bucket report.pdf ./report.pdf
tigris objects put my-bucket logo.png ./logo.png --access public --content-type image/png
```

| Flag             | Alias | Description                             | Default   |
| ---------------- | ----- | --------------------------------------- | --------- |
| `--access`       | `-a`  | Access level (`public`, `private`)      | `private` |
| `--content-type` | `-t`  | Content type (auto-detected if omitted) |           |
| `--format`       | `-f`  | Output format (`json`, `table`, `xml`)  | `table`   |
| `--json`         |       | Output as JSON                          |           |

### `tigris objects delete <bucket> <key>` (alias: `d`)

Delete one or more objects by key. Accepts comma-separated keys.

```bash
tigris objects delete my-bucket old-file.txt --force
tigris objects delete my-bucket file-a.txt,file-b.txt --force
```

| Flag              | Description                                       |
| ----------------- | ------------------------------------------------- |
| `--force`         | Skip confirmation prompt                          |
| `--format` / `-f` | Output format (`json`, `table`; default: `table`) |
| `--json`          | Output as JSON                                    |

### `tigris objects set <bucket> <key>` (alias: `s`)

Update settings on an existing object such as access level or key name.

```bash
tigris objects set my-bucket my-file.txt --access public
tigris objects set my-bucket my-file.txt --access private
```

| Flag        | Alias | Description                                       |
| ----------- | ----- | ------------------------------------------------- |
| `--access`  | `-a`  | Access level (`public`, `private`) — required     |
| `--new-key` | `-n`  | Rename the object to a new key                    |
| `--format`  | `-f`  | Output format (`json`, `table`; default: `table`) |
| `--json`    |       | Output as JSON                                    |

## Common Patterns

```bash
# Recursive upload
tigris cp ./dist/ t3://my-bucket/static/ -r

# Download an entire directory
tigris cp t3://my-bucket/backups/ ./local-backups/ -r

# Wildcard delete (quote the pattern!)
tigris rm "t3://my-bucket/logs/*.tmp" -rf

# Generate a presigned upload URL for client-side uploads
tigris presign my-bucket/user-uploads/photo.jpg --method put --expires-in 600
```
