---
name: oxygen-custom-http
description: Turn a public HTTPS API into OXYGEN catalog tools with a custom integration manifest: operations, fields and auth, server-side credentials, dry runs and live calls, tool columns, and safe removal.
---

# Bring your own API

Read [the runtime contract](../../../docs/runtime-contract.md). A custom integration turns a public HTTPS API into workspace tools named `custom_http.<slug>.<operation>`. Credentials are stored encrypted and injected server-side.

1. Write a JSON manifest: `slug`, `name`, `baseUrl`, `auth` (none, bearer, API key header or query, basic) and `operations` (method, path, effect, fields with location path, query or body). Never put a secret in the manifest.
2. `oxygen custom-integrations apply --manifest ./api.json --json` saves it and calls nothing.
3. Attach the credential from a local `.env` file with `oxygen custom-integrations connect <slug> --secrets-file <file> --json`, or on the Connections page.
4. Inspect and dry-run: `oxygen tools get custom_http.<slug>.<operation> --json`, then `tools run ... --mode dry_run`. Review the endpoint and inputs before a live call.
5. Bind row work with a tool column, preview one row, then run a bounded batch.

Custom HTTP charges 0 OXYGEN credits; the upstream API's charges are yours, so agree a scope and an upstream ceiling first. Live writes need explicit approval and `--approved`. Removal previews first and deletes the stored credential, not the key at the provider.

A public read-only API without auth (for example a DNS-over-HTTPS resolver for SPF records) needs no credential. Inside a Workflow, a plain GET can also use the native `oxygen.http_json_request` step.
