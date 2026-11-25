---
name: keeper-notation
description: Construct safe Keeper CLI calls - Keeper notation (keeper://) for addressing a single field, record UIDs vs titles, scoped field selection, and region hosts for ksm and keeper. Foundational patterns for every other Keeper skill. Use whenever building a ksm or keeper command that references a record, addressing a field with notation, choosing which field to return, or reasoning about which region a tenant lives in.
---

# Keeper CLI Patterns

Every Keeper CLI - `ksm` and `keeper` (Commander) - addresses records the same
way. Get this right once and every workflow is fast, scoped, and safe.

## Keeper notation (address one field)

Notation is how you ask for a single field instead of a whole record:

```text
keeper://<record-uid-or-title>/<type>/<name>
```

- `<type>` is `field`, `custom_field`, or `file`.
- Standard fields: `keeper://8f8I-OqPV58o2r91wVgZ_A/field/password`, `.../field/login`.
- Custom fields by label: `keeper://My App/custom_field/api_key`.
- Array indexing: `.../custom_field/links[]` (all), `.../custom_field/links[1]` (2nd).
- Escape `/`, `\`, `[`, `]` inside a title/label/filename with a backslash - they are notation delimiters.
- If a UID begins with `-`, prefix the path with `-- ` so it is not read as a flag.

```bash
ksm secret get keeper://<UID>/field/password        # one field only
DB_PASS="keeper://<UID>/field/password" ksm exec -- myapp   # inject, never print
```

Prefer single-field notation over `ksm secret get -u <UID> --json` so unrelated
secret material never enters context. Full syntax: the keeper-secrets skill's
`references/keeper-notation.md` in this plugin and
[Keeper notation docs](https://docs.keeper.io/keeperpam/secrets-manager/about/keeper-notation).

## UID vs title

A record **UID** (e.g. `8f8I-OqPV58o2r91wVgZ_A`) is the stable, unambiguous
key - always prefer it for mutating or sensitive calls. Titles are convenient
for search but can collide, so resolve a title to a single UID
(`ksm secret list`, Commander `search`) and **disambiguate** before acting.
Reference records to the user by title *and* UID, never by their contents.

## Field selection (least exposure)

Default to requesting the one field needed. Only fetch a full record when the
task genuinely needs multiple fields, and even then never echo secret-typed
fields (password, key, token, TOTP seed, certificate) into output.

## Region hosts

Keeper runs regional data centers; a tenant lives in exactly one:

| Region | Commander server | KSM hostname |
|--------|------------------|--------------|
| US | `keepersecurity.com` | `US` |
| EU | `keepersecurity.eu` | `EU` |
| AU | `keepersecurity.com.au` | `AU` |
| CA | `keepersecurity.ca` | `CA` |
| JP | `keepersecurity.jp` | `JP` |
| US GOV | `govcloud.keepersecurity.us` | `US_GOV` |

Set with `ksm profile init --hostname <host>` and Commander's server setting.
Auth or 404 errors on otherwise-correct calls usually mean the wrong region.

## Safe handling (applies to every call)

Keeper is zero-knowledge. Never print a secret value into a transcript, log,
or tool argument. Return only the requested field, reference records by
title/UID, confirm before any rotate/update or session launch, and treat every
retrieval as an audited event.
