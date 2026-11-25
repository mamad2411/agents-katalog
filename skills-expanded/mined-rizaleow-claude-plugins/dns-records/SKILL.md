---
description: Read, validate, and edit DNS records on Hostinger-managed domains via `hostinger-cli dns`. Use when the user wants to inspect a DNS zone, add/change/remove records, or restore from a snapshot.
---

# DNS records via `hostinger-cli`

## Preflight

1. `command -v hostinger-cli` — install via `brew install rizaleow/tap/hostinger-cli` if absent.
2. `hostinger-cli auth status` — instruct `hostinger-cli auth login` if not authenticated.

## Commands

| Goal | Command |
| --- | --- |
| Read zone | `hostinger-cli dns zone get --domain example.com -o json` |
| Update records (apply patch JSON) | `hostinger-cli dns zone update --domain example.com --body @patch.json` |
| Delete records | `hostinger-cli dns zone delete --domain example.com --body @delete.json` |
| Reset to defaults | `hostinger-cli dns zone reset --domain example.com` |
| Validate without applying | `hostinger-cli dns zone validate --domain example.com --body @patch.json` |
| List snapshots | `hostinger-cli dns snapshot list --domain example.com -o json` |
| Get snapshot | `hostinger-cli dns snapshot get --domain example.com --snapshot-id <id> -o json` |
| Restore snapshot | `hostinger-cli dns snapshot restore --domain example.com --snapshot-id <id>` |

## CRITICAL: `update` replaces records by type

`dns zone update` is a **type-scoped replacement**: every record type
included in the body REPLACES all existing records of that type for that
host. To add a single A record without losing the others, you MUST:

1. Read current records: `dns zone get --domain X -o json`.
2. Build a JSON body that includes the existing entries *plus* the new
   one for each type you touch.
3. **Validate first**: `dns zone validate --domain X --body @patch.json`.
4. Apply: `dns zone update --domain X --body @patch.json`.

When in doubt, take a snapshot implicitly by reading the zone and saving
the JSON locally before editing.

## Body shape

The `--body` argument accepts inline JSON or `@path/to/file.json`. The
schema mirrors the Hostinger DNS API zone payload — typically a `zone`
array of `{ name, type, ttl, records: [{ content }] }` objects. Run
`hostinger-cli dns zone update --help` to see the latest schema hint,
or fetch a current zone with `dns zone get` and use that as your
template.

## Patterns

- **Always validate before update.** `validate` returns the same errors
  as `update` without mutation.
- **TTL hygiene.** Use a low TTL (e.g. 300s) when planning to revert
  quickly; raise it back once stable.
- **Apex CNAME.** Hostinger rejects CNAME at the zone apex — use an A/AAAA
  record there instead.
- **Snapshot before risky edits.** If you don't have an explicit
  snapshot endpoint to call, save the `dns zone get` JSON to disk first
  so you can rebuild the zone manually if needed.
