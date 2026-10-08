---
name: torlvesk-tickets
description: Fictional command-line precedent lookup over an embedded vendor ticket archive.
---

# torlvesk: tickets

A fictional, deterministic command-line surface. This skill owns the entire
provider contract — invocation syntax, input schema, output schema, and
authentication mechanics. Workspace tool-use definitions carry only company
policy and never restate anything on this page.

## Invocation

Run the adjacent `cli.mjs` executable with flag arguments:

```
node cli.mjs --vendor-role <slug> --signature <text> [--limit <n>]
```

- `--vendor-role`: the descriptive vendor role slug to search
  (lowercase kebab, e.g. `analytics-data-vendor`).
- `--signature`: the failure signature text to match (3–512 characters).
- `--limit`: optional maximum row count; whole number of at least 1,
  clamped to 8.

Any unknown flag, duplicate flag, missing value, or out-of-shape value is
refused with exit code 2 and no output. The executable opens no sockets,
spawns no processes, and reads no files except its adjacent embedded corpus.
When the optional `ROSTER_WORKFLOW_PROVIDER_LOG` environment variable names a
writable path, it appends one JSON line per invocation recording the parsed
flag map and the result count — nothing else.

## Output

One JSON document: `results` is an array of archive rows carrying
`ticket_id`, `failure_signature`, `accepted_fix`, `vendor_role`, and
`resolved_at`, in corpus order. Vendor identities are descriptive role
strings; owner references are role strings, never personal names.

## Authentication

None. This fixture is credential-free by construction. A real deployment
would resolve ambient credentials outside the workspace; credential material
never belongs in authored workspace files.
